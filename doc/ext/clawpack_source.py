"""
Document each version against the Clawpack source it shipped, and fail the
build when autodoc cannot import something.

sphinx-multiversion builds every version with *this* checkout's conf.py, and
conf.py puts one tree on sys.path: $CLAW, pinned in tools/clawpack-ref.txt to
current master.  A released version's .rst comes from its own tag, but without
this extension its API pages would be generated from master: renamed modules
fail to import (surge.storm -> met.storm emptied storm_module.html on every
release), and everything else silently documents code the release never had.

So, on ``config-inited``, a version listed in tools/clawpack-release-refs.txt
gets its own tree (``tools/fetch_clawpack_src.py --releases``) swapped onto
sys.path in place of $CLAW.  ``dev`` and plain single-version builds are left
alone.

autodoc reports an import failure as an ordinary warning, and a build that
emits one still succeeds -- with an empty page.  Every page here is expected to
import (tools/check_doc_env.py enforces that for dev before the build), so any
``autodoc: failed to import`` in any version fails the build.
"""

import importlib
import importlib.util
import logging
import os
import sys
import types

from sphinx.errors import ExtensionError

from clawroot import CLAW_SUBPATHS, claw_root, release_root


def _claw_paths(root):
    return [root] + [os.path.join(root, sub) for sub in CLAW_SUBPATHS]


def _install_imp_shim():
    """Python 3.12 removed ``imp``; v5.7.x's pyclaw does ``from imp import reload``.

    Only ``reload`` is provided, which is all any release uses.
    """
    if importlib.util.find_spec('imp') is None and 'imp' not in sys.modules:
        imp = types.ModuleType('imp')
        imp.reload = importlib.reload
        sys.modules['imp'] = imp


def _use_version_tree(app, config):
    version = getattr(config, 'smv_current_version', '') or ''
    root = release_root(version) if version else None
    if root is None:
        app.clawpack_root = claw_root()
        return

    root = os.path.realpath(root)
    stale = set(_claw_paths(claw_root()))
    sys.path[:] = [p for p in sys.path if p not in stale]
    sys.path[:0] = [root]
    sys.path.extend(_claw_paths(root)[1:])
    for name in [m for m in sys.modules
                 if m == 'clawpack' or m.startswith('clawpack.')]:
        del sys.modules[name]
    _install_imp_shim()
    app.clawpack_root = root
    print(f'clawpack_root ({version}) = {root}')


class _ImportFailures(logging.Handler):
    """Collects autodoc's import-failure warnings, wherever they are emitted."""

    def __init__(self):
        super().__init__(level=logging.WARNING)
        self.failures = set()

    def emit(self, record):
        try:
            message = record.getMessage()
        except Exception:
            return
        if 'failed to import' in message:
            self.failures.add(message.splitlines()[0])


def _check(app, exception, handler):
    if exception is not None:
        return
    root = app.clawpack_root
    clawpack = sys.modules.get('clawpack')
    if clawpack is not None and getattr(clawpack, '__file__', None):
        where = os.path.realpath(clawpack.__file__)
        if os.path.commonpath([where, os.path.realpath(root)]) != os.path.realpath(root):
            raise ExtensionError(
                f'clawpack was imported from {where}, not from the tree this '
                f'version documents ({root}).  An installed clawpack is '
                'shadowing it; build in a virtualenv without one.')
    if handler.failures:
        raise ExtensionError(
            f'autodoc could not import {len(handler.failures)} target(s) '
            f'from {root}; their API pages would be empty:\n  '
            + '\n  '.join(sorted(handler.failures)))


def setup(app):
    app.connect('config-inited', _use_version_tree, priority=100)
    handler = _ImportFailures()
    # Sphinx's loggers are all children of "sphinx"; a handler there sees
    # autodoc's warnings, including ones replayed from parallel workers.
    logging.getLogger('sphinx').addHandler(handler)

    def check_imports(app, exception):
        _check(app, exception, handler)

    app.connect('build-finished', check_imports)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
