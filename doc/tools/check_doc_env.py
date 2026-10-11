#!/usr/bin/env python
# encoding: utf-8
r"""
Preflight the environment a Clawpack doc build needs, before Sphinx runs.

autodoc failures are reported as ordinary warnings buried in a long build log,
so an environment that cannot import Clawpack does not *fail* the build -- it
quietly produces a site whose API pages are empty.  That is exactly what
happened to the first docs-publish runs: CI had no sibling source tree, fell
back to a pip-installed clawpack with no dependencies, and emitted 36
``autodoc: failed to import`` warnings that nothing was watching.

This script front-loads that check.  It collects every autodoc target the
documentation actually references, imports each one, and asserts the module
resolved to the pinned source tree rather than to something on ``sys.path`` by
accident.  One legible error instead of 36 opaque warnings.

Usage
-----
    check_doc_env.py [--check-pin] [--verbose]

``--check-pin`` additionally requires the tree to match
``tools/clawpack-ref.txt``.  CI passes it, and so does
``make checkwarnings-update``, since a baseline written against an unpinned
tree is not reproducible.  A plain ``make checkenv`` does not, so a developer
with a slightly different checkout can still use it.

Failures are sorted into three kinds, because they have three different
remedies and printing one blanket suggestion for all of them wastes the
reader's time:

* the module is **absent from the tree** at ``$CLAW`` -- a stale checkout,
  e.g. a geoclaw pinned before the ``surge`` -> ``met`` rename;
* it is **on disk but not importable** -- almost always an installed clawpack
  whose file list, not the filesystem, decides what exists;
* it is a **third-party dependency** -- pin it or mock it.

That taxonomy is not theoretical.  A maintainer hit the first two at once and
was told to pin a dependency, which was the remedy for neither.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import os
import re
import sys
import traceback


# Also makes fetch_clawpack_src importable for --check-pin.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clawroot import CLAW_ROOT_HELP, SRC_DIR, claw_root  # noqa: E402

CLAW_ROOT = claw_root()

# The directive matters: `automodule:: X` means X is a module, while
# `autoclass:: X` means X is an attribute of the module X[:-1].  Conflating
# them hides real failures -- stripping the last component of a *module* name
# until something imports would happily "resolve" a broken
# clawpack.geoclaw.topotools to a perfectly healthy clawpack.geoclaw.
_AUTODOC_RE = re.compile(
    r'^\s*\.\.\s+auto(module|class|function|exception|data)::\s+(\S+)',
    re.MULTILINE)
_MODULE_DIRECTIVES = {'module'}


def _mocked_prefixes() -> list[str]:
    """The ``autodoc_mock_imports`` list from conf.py, read without importing it.

    conf.py has import-time side effects (it patches logging.config), so it is
    parsed rather than executed.
    """
    conf = os.path.join(SRC_DIR, 'conf.py')
    with open(conf, encoding='utf-8') as fh:
        text = fh.read()
    m = re.search(r'^autodoc_mock_imports\s*=\s*\[(.*?)\]', text,
                  re.MULTILINE | re.DOTALL)
    if not m:
        return []
    return re.findall(r'''['"]([^'"]+)['"]''', m.group(1))


def _missing_name(exc: BaseException) -> str | None:
    """The dotted name Python could not find, or ``None``.

    Three shapes, in order of reliability.  ``ModuleNotFoundError`` carries
    ``name``.  A failed ``from . import X`` raises a plain ``ImportError``
    whose ``name`` is the *package* and whose ``name_from`` is the attribute,
    so the module is the two joined -- that is the shape of the riemann
    failure, where the target that fails is not the module that is missing.
    Older interpreters may set neither, hence the message fallback.
    """
    name = getattr(exc, 'name', None)
    if isinstance(exc, ImportError) and not isinstance(exc, ModuleNotFoundError):
        name_from = getattr(exc, 'name_from', None)
        if name and name_from:
            return f'{name}.{name_from}'
    if name:
        return name

    text = str(exc)
    match = re.search(r"cannot import name '([^']+)' from '?([\w.]+)'?", text)
    if match:
        return f'{match.group(2)}.{match.group(1)}'
    match = re.search(r"No module named '([\w.]+)'", text)
    if match:
        return match.group(1)
    return None


def _source_path(dotted: str) -> tuple[str | None, list[str]]:
    """``(file the source tree provides or None, paths searched)``.

    Walks prefixes longest-first and resolves the remainder against the real
    ``__path__`` of the longest prefix that imports.  Shorter prefixes are
    tried when a longer one is itself broken, which is what makes
    ``clawpack.riemann.euler_mapgrid_3D_constants`` resolvable through
    ``clawpack.__path__`` even though importing ``clawpack.riemann`` is
    exactly what failed.
    """
    parts = dotted.split('.')
    searched: list[str] = []
    for split in range(len(parts) - 1, 0, -1):
        parent = '.'.join(parts[:split])
        module = sys.modules.get(parent)
        if module is None:
            try:
                module = importlib.import_module(parent)
            except Exception:
                continue
        for entry in getattr(module, '__path__', None) or []:
            base = os.path.join(entry, *parts[split:])
            for candidate in (base + '.py', os.path.join(base, '__init__.py')):
                searched.append(candidate)
                if os.path.exists(candidate):
                    return candidate, searched
    return None, searched


def _shadowing_install() -> tuple[str | None, list[str]] | None:
    """``(version, finder descriptions)`` if clawpack is installed here.

    Worth reporting even when the build then succeeds: an install decides
    what is importable by its own file list, so a doc build against one can
    disagree with the checkout for reasons no amount of ``$CLAW`` fiddling
    explains.
    """
    try:
        version = importlib.metadata.version('clawpack')
    except importlib.metadata.PackageNotFoundError:
        version = None

    finders = []
    for finder in sys.meta_path:
        cls = type(finder)
        module = cls.__module__ or ''
        if module.startswith('mesonpy') or cls.__name__.startswith('Mesonpy'):
            finders.append(f'{cls.__name__} (meson-python editable install)')
        elif module.startswith('__editable__'):
            finders.append(f'{cls.__name__} (setuptools editable install)')

    if version is None and not finders:
        return None
    return version, finders


def collect_targets() -> set[tuple[str, str]]:
    """Every ``(directive, dotted-name)`` pair the docs point autodoc at."""
    targets: set[tuple[str, str]] = set()
    for dirpath, dirnames, filenames in os.walk(SRC_DIR):
        dirnames[:] = [d for d in dirnames
                       if d not in ('_build', '_build1', '_static', '_templates')]
        for name in filenames:
            if not name.endswith('.rst'):
                continue
            with open(os.path.join(dirpath, name), encoding='utf-8',
                      errors='replace') as fh:
                targets.update(_AUTODOC_RE.findall(fh.read()))
    return targets


def _resolve(directive: str, target: str) -> tuple[str | None, BaseException | None]:
    """Import what *target* needs and return ``(module_name, error)``.

    For ``automodule`` the target is the module.  For everything else it is an
    attribute of its parent module, so the parent is imported and the attribute
    is required to exist -- which also catches a class that has been renamed
    out from under the docs.
    """
    if directive in _MODULE_DIRECTIVES:
        module, attr = target, None
    elif '.' not in target:
        return None, ImportError(f'{target!r} has no module part')
    else:
        module, attr = target.rsplit('.', 1)

    try:
        obj = importlib.import_module(module)
    except Exception as exc:
        return None, exc

    if attr is not None and not hasattr(obj, attr):
        return None, AttributeError(
            f'module {module!r} has no attribute {attr!r}')
    return module, None


def classify(error: BaseException) -> tuple[str, str | None, object]:
    """``(kind, missing name, evidence)`` for one import failure.

    ``absent``      a clawpack module the source tree does not contain;
                    evidence is the list of paths searched.
    ``unexposed``   a clawpack module that is on disk yet did not import;
                    evidence is the file.
    ``third_party`` a non-clawpack module; no evidence needed.
    ``attribute``   the module imported but the documented name is gone.
    ``unknown``     nothing identifiable; evidence is ``None``.
    """
    # AttributeError also carries `.name` (of the attribute), so it has to be
    # taken out before _missing_name mistakes it for a module.
    if isinstance(error, AttributeError):
        return 'attribute', getattr(error, 'name', None), None
    if not isinstance(error, ImportError):
        return 'unknown', None, None

    missing = _missing_name(error)
    if missing is None:
        return 'unknown', None, None
    if missing != 'clawpack' and not missing.startswith('clawpack.'):
        return 'third_party', missing, None
    path, searched = _source_path(missing)
    if path is not None:
        return 'unexposed', missing, path
    return 'absent', missing, searched


def _report_failures(failures: list[tuple[str, BaseException]],
                     install: tuple[str | None, list[str]] | None) -> None:
    """Print the failures grouped by kind, each with the remedy that fits."""
    groups: dict[str, list[tuple[str, BaseException, str | None, object]]] = {}
    for target, error in failures:
        kind, missing, evidence = classify(error)
        groups.setdefault(kind, []).append((target, error, missing, evidence))

    def header(text: str) -> None:
        print(f'\n{text}\n', file=sys.stderr)

    absent = groups.get('absent', [])
    if absent:
        header(f'{len(absent)} target(s) are not present in the source tree '
               f'at\n{CLAW_ROOT}:')
        for target, error, missing, searched in absent:
            print(f'  {target}\n      no {missing} anywhere under $CLAW',
                  file=sys.stderr)
            # Both spellings, module and package: for clawpack.geoclaw.met the
            # interesting one is met/__init__.py, not met.py.
            for candidate in (searched or [])[:2]:
                print(f'      looked for {candidate}', file=sys.stderr)
        print('\n  Your checkout predates these modules -- clawpack/clawpack\'s '
              'submodule\n  pointers lag its subrepos, and the surge -> met '
              'rename is the usual\n  culprit.  Update the submodules, or '
              'build against the pinned tree:\n\n'
              '      make claw-pin\n'
              '      CLAW=$(cd ../.claw-pin && pwd) make checkenv',
              file=sys.stderr)

    unexposed = groups.get('unexposed', [])
    if unexposed:
        header(f'{len(unexposed)} target(s) exist on disk but did not import:')
        for target, error, missing, path in unexposed:
            print(f'  {target}\n      needs {missing}, which is right here:\n'
                  f'      {path}', file=sys.stderr)
        if install is not None:
            version, finders = install
            print(f'\n  So the filesystem is not what decides here: clawpack '
                  f'{version or "?"} is installed in\n  this environment.',
                  file=sys.stderr)
            if finders:
                print(f'  Imports resolve through its\n      {finders[0]},',
                      file=sys.stderr)
            print('  and an install ships exactly the files listed in each '
                  'subpackage\'s\n  meson.build -- so a module that is '
                  'tracked and imported but unlisted is\n  missing for users '
                  'and present for you.  Fix it there, or build the docs\n  '
                  'in a virtualenv with no clawpack installed.',
                  file=sys.stderr)
        else:
            print('\n  Nothing is shadowing $CLAW, so this is not a packaging '
                  'problem: the\n  module is on disk and still failed to '
                  'import.  Read the error above --\n  the fault is inside '
                  'that module, or in what it imports.', file=sys.stderr)

    third_party = groups.get('third_party', [])
    if third_party:
        header(f'{len(third_party)} target(s) need a third-party package:')
        for target, error, missing, _ in third_party:
            print(f'  {target}\n      needs {missing}', file=sys.stderr)
        print('\n  Either pin it in tools/requirements-docs.txt or add it to '
              'autodoc_mock_imports\n  in conf.py -- a module must be one or '
              'the other, never neither, or local\n  and CI builds will '
              'disagree.', file=sys.stderr)

    attribute = groups.get('attribute', [])
    if attribute:
        header(f'{len(attribute)} target(s) import, but the documented name '
               'is gone:')
        for target, error, missing, _ in attribute:
            print(f'  {target}', file=sys.stderr)
            print('      ' + ''.join(traceback.format_exception_only(
                type(error), error)).strip(), file=sys.stderr)
        print('\n  The code was renamed out from under the docs.  Update the '
              'directive in the\n  .rst file, or restore the name.',
              file=sys.stderr)

    unknown = groups.get('unknown', [])
    if unknown:
        header(f'{len(unknown)} target(s) failed for reasons this script '
               'could not classify:')
        for target, error, _, _ in unknown:
            print(f'  {target}', file=sys.stderr)
            print('      ' + ''.join(traceback.format_exception_only(
                type(error), error)).strip(), file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check-pin', action='store_true',
                        help='also require the tree to match tools/clawpack-ref.txt')
    parser.add_argument('--verbose', action='store_true',
                        help='print every resolved module path')
    args = parser.parse_args(argv)

    print(f'$CLAW = {CLAW_ROOT}')

    install = _shadowing_install()
    if install is not None:
        version, finders = install
        print(f'note: clawpack {version or "(unknown version)"} is installed '
              'in this environment')
        if finders:
            print(f'      {finders[0]} takes precedence over $CLAW, so what '
                  'is importable is\n      decided by that install\'s file '
                  'list, not by the files in the checkout')
        else:
            print('      $CLAW goes ahead of it on sys.path, so the checkout '
                  'should win; the\n      checks below confirm it')

    shim = os.path.join(CLAW_ROOT, 'clawpack', '__init__.py')
    if not os.path.exists(shim):
        print(f'\nFAIL: {shim} is missing -- there is no Clawpack source tree '
              f'at\n{CLAW_ROOT}.\n\n' + CLAW_ROOT_HELP, file=sys.stderr)
        return 1

    sys.path.insert(0, CLAW_ROOT)

    if args.check_pin:
        import fetch_clawpack_src  # noqa: E402  (TOOLS_DIR is on sys.path)
        if fetch_clawpack_src.check(CLAW_ROOT) != 0:
            return 1

    # An editable/pip-installed clawpack registers a meta-path finder that wins
    # over sys.path, so getting this far does not guarantee we are documenting
    # the tree we chose.  Check the shim itself before anything else imports.
    import clawpack  # noqa: E402
    if os.path.commonpath([os.path.abspath(clawpack.__file__), CLAW_ROOT]) != CLAW_ROOT:
        print(f'\nFAIL: `import clawpack` resolved to\n  {clawpack.__file__}\n'
              f'which is outside {CLAW_ROOT}.\n\n' + CLAW_ROOT_HELP,
              file=sys.stderr)
        return 1

    mocked = _mocked_prefixes()
    targets = collect_targets()
    if not targets:
        print('FAIL: no autodoc directives found under '
              f'{SRC_DIR} -- has the doc layout changed?', file=sys.stderr)
        return 1

    failures: list[tuple[str, BaseException]] = []
    outside: list[tuple[str, str]] = []
    checked = 0

    for directive, target in sorted(targets, key=lambda t: t[1]):
        if any(target == p or target.startswith(p + '.') for p in mocked):
            continue
        module, error = _resolve(directive, target)
        if module is None:
            failures.append((target, error))
            continue
        checked += 1
        path = getattr(sys.modules.get(module), '__file__', None)
        if args.verbose:
            print(f'  ok  {target:<50} {path}')
        if path and target.startswith('clawpack.'):
            if os.path.commonpath([os.path.abspath(path), CLAW_ROOT]) != CLAW_ROOT:
                outside.append((target, path))

    if failures:
        print(f'\nFAIL: {len(failures)} autodoc target(s) cannot be imported.\n'
              'Their API pages would be silently empty in the built site.',
              file=sys.stderr)
        _report_failures(failures, install)
        return 1

    if outside:
        print('\nFAIL: clawpack modules resolved outside the source tree.\n'
              'autodoc would document an installed clawpack instead of the\n'
              'pinned checkout, so the docs and the code would drift apart.\n',
              file=sys.stderr)
        for target, path in outside:
            print(f'  {target}\n      {path}', file=sys.stderr)
        return 1

    print(f'ok   {checked} autodoc target(s) import from {CLAW_ROOT}')
    if mocked:
        print(f'ok   {len(mocked)} mocked prefix(es): {", ".join(mocked)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
