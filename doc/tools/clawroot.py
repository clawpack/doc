#!/usr/bin/env python
# encoding: utf-8
r"""
One definition of "which Clawpack source tree are we documenting?".

``conf.py`` and every tool under ``tools/`` must agree on this, or the warning
baseline stops being comparable: ``check_doc_warnings.py`` rewrites warning
locations relative to this root, so a tool that picks a different root produces
different signatures for the same warning.

The default is the parent of this repository -- the ordinary ``$CLAW`` layout,
where ``doc`` sits next to ``geoclaw``, ``pyclaw`` and the rest, and
``clawpack/__init__.py`` maps ``clawpack.geoclaw`` onto
``geoclaw/src/python/geoclaw``.

Setting ``CLAW`` overrides it.  That is how the docs get built against the
pinned tree (``tools/clawpack-ref.txt``, ``make claw-pin``) without anyone
having to move their checkout around, and it is what CI uses.

That answer is for ``dev`` and for single-version builds.  A *released*
version in a multiversion build is documented against its own release instead
(``tools/clawpack-release-refs.txt``): ``release_root`` says where that tree
is, and ``ext/clawpack_source.py`` swaps it in.
"""

from __future__ import annotations

import os
import re


TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(TOOLS_DIR)        # doc/doc -- the sphinx source dir

RELEASE_MANIFEST = os.path.join(TOOLS_DIR, 'clawpack-release-refs.txt')

# Where `make claw-releases` puts the release trees; $CLAW_VERSION_TREES
# overrides it (CI materialises them under $RUNNER_TEMP).
DEFAULT_RELEASE_TREES = os.path.join(SRC_DIR, os.pardir, '.claw-releases')

_SHA_RE = re.compile(r'^[0-9a-f]{40}$')

# Paths under a tree that conf.py puts on sys.path besides the root itself.
CLAW_SUBPATHS = ['amrclaw/doc', 'visclaw/doc', 'geoclaw/doc', 'pyclaw/src',
                 'riemann/src/python/riemann']

CLAW_ROOT_HELP = """\
The docs are built against a Clawpack source tree, selected by $CLAW and
defaulting to the parent of this repository.  To build against the pinned
tree instead:

    make claw-pin                 # clone tools/clawpack-ref.txt into ../.claw-pin
    CLAW=$(cd ../.claw-pin && pwd) make checkwarnings

Use a virtualenv with no clawpack installed: an editable or pip-installed
clawpack registers a meta-path finder that shadows the source tree no matter
what sys.path says."""


def claw_root() -> str:
    """Absolute path of the Clawpack source tree to document."""
    override = os.environ.get('CLAW')
    if override:
        return os.path.abspath(override)
    return os.path.abspath(os.path.join(SRC_DIR, os.pardir, os.pardir))


def read_release_manifest(path: str = RELEASE_MANIFEST) -> dict[str, str]:
    """``{doc version: clawpack/clawpack commit}`` from the release manifest."""
    releases: dict[str, str] = {}
    with open(path, encoding='utf-8') as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            fields = line.split()
            if len(fields) != 2:
                raise SystemExit(f'{path}:{lineno}: expected '
                                 f'"<doc version> <sha>", got: {line!r}')
            version, sha = fields
            if not _SHA_RE.match(sha):
                raise SystemExit(f'{path}:{lineno}: {version} is not pinned to '
                                 f'a full 40-character SHA: {sha!r}')
            if version in releases:
                raise SystemExit(f'{path}:{lineno}: {version} listed twice')
            releases[version] = sha
    return releases


def release_trees_dir() -> str:
    """Directory holding one materialised tree per released doc version."""
    return os.path.abspath(os.environ.get('CLAW_VERSION_TREES')
                           or DEFAULT_RELEASE_TREES)


def release_root(version: str) -> str | None:
    """The tree to document *version* against, or None if it is not a release.

    Raises if *version* is a release whose tree has not been materialised:
    falling back to $CLAW there is exactly the bug the manifest exists to
    prevent, so it has to be loud.
    """
    if version not in read_release_manifest():
        return None
    root = os.path.join(release_trees_dir(), version)
    if not os.path.exists(os.path.join(root, 'clawpack', '__init__.py')):
        raise RuntimeError(
            f'{version} is a released version, documented against its own '
            f'Clawpack tree, but there is none at\n  {root}\n'
            'Materialise the release trees first:\n\n'
            '    make claw-releases\n\n'
            'or point $CLAW_VERSION_TREES at a directory that has them.')
    return root
