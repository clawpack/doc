#!/usr/bin/env python
# encoding: utf-8
r"""
Catch reStructuredText / docstring warnings in the Clawpack documentation.

Sphinx does not fail the build on docutils warnings (missing blank lines,
bad cross references, autodoc problems, ...).  With ``keep_warnings = False``
in ``conf.py`` these warnings are no longer embedded in the rendered HTML, so
this script provides a way to surface and gate on them.

It performs a *forced full re-parse* of the main documentation (the ``dummy``
builder, so no HTML is written) capturing every warning, normalises each one
into a stable, machine-independent signature, and compares the result against a
committed baseline:

    tools/doc_warnings_baseline.txt

Exit status / modes
-------------------
default    Fail (exit 1) if any warning appears that is NOT in the baseline.
           Resolved baseline entries are reported but do not fail the run.
--update   Rewrite the baseline from the current run instead of comparing.
           Use this to seed the baseline, or to shrink it after fixing (or
           intentionally adding) warnings, then commit the result.
--strict   Ignore the baseline entirely and fail if there are ANY warnings.
           This is the end goal once the baseline has been driven to empty.

Some warnings are never baselined at all -- see ``_ALWAYS_FAIL``.  An
``autodoc: failed to import`` means the API pages for that module come out
empty, which is a silent content loss no baseline should be allowed to hide.

Reproducibility
---------------
autodoc imports the Clawpack packages, so the set of warnings is a property of
the environment as much as of the docs.  Two things pin it:

    tools/requirements-docs.txt   the Sphinx toolchain and clawpack's deps
    tools/clawpack-ref.txt        the Clawpack source tree, by commit

Regenerate against both, in a virtualenv with no clawpack installed::

    make claw-pin
    CLAW=$(cd ../.claw-pin && pwd) make checkwarnings-update
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clawroot import SRC_DIR, TOOLS_DIR, claw_root  # noqa: E402

CLAW_ROOT = claw_root()
DOC_REPO = os.path.dirname(SRC_DIR)      # this repository's root
BASELINE = os.path.join(TOOLS_DIR, 'doc_warnings_baseline.txt')

# A sphinx warning line looks like one of:
#   /abs/path/foo.rst:123: WARNING: message
#   /abs/path/mod.py:docstring of pkg.mod.Cls:7: ERROR: message
#   WARNING: message                         (no location)
_WARNING_RE = re.compile(
    r'^(?P<loc>.*?)(?:: )?(?P<level>WARNING|ERROR|SEVERE|CRITICAL): '
    r'(?P<msg>.*)$'
)

# Warnings that must never be absorbed into the baseline, however long they
# have been around.  `autodoc: failed to import` means the API pages for those
# modules are *empty* in the built site -- a silent content loss that looks
# identical to a healthy build unless someone reads the log.  Baselining it
# once would hide it forever; the first docs-publish runs emitted 36 of these
# and would have published the result.
_ALWAYS_FAIL = (
    ('autodoc: failed to import',
     'autodoc could not import these -- their API pages would be EMPTY'),
)

# Absolute paths appear inside warning *messages* as well as in the location
# field: "duplicate label about, other instance in /abs/path/about.rst".  Left
# alone they make the baseline machine-specific.
_ABSPATH_RE = re.compile(r'(?<![\w/])(/[^\s:,()\'"]+)')


def _relativize(path: str) -> str:
    """Rewrite *path* into a form that does not depend on where things live.

    Two roots, because the docs and the code they document need not be in the
    same place any more: $CLAW can point at a pinned tree materialised
    somewhere else entirely (see clawroot.py).  The doc repository is anchored
    on its own so that `doc/doc/topo.rst` means the same thing either way --
    including in the default layout, where the repository sits inside $CLAW and
    both roots agree.
    """
    if not path:
        return path
    abspath = path if os.path.isabs(path) else os.path.join(SRC_DIR, path)

    for root, prefix in ((DOC_REPO, 'doc'), (CLAW_ROOT, '')):
        try:
            rel = os.path.relpath(abspath, root)
        except ValueError:  # different drive on Windows
            continue
        if not rel.startswith(os.pardir):
            return os.path.join(prefix, rel) if prefix else rel

    # An installed clawpack still yields a stable suffix, and keeping it
    # comparable makes a misconfigured build report a location a reader can act
    # on rather than a runner-specific absolute path.
    marker = '/site-packages/'
    if marker in abspath:
        return abspath.split(marker, 1)[1]
    return path


def _normalize_location(loc: str) -> str:
    """Drop absolute prefixes and volatile line numbers from a warning's location.

    ``/abs/mod.py:docstring of pkg.Cls:7`` -> ``docstring of pkg.Cls``
    ``/abs/foo.rst:123``                    -> ``doc/doc/foo.rst``

    Docstring warnings are keyed on the dotted name alone.  Where the module
    file lives depends on how Clawpack was made importable -- a source tree
    under $CLAW, or site-packages -- but ``clawpack.geoclaw.util.bearing`` is
    the same object either way, so it is the stable half of the location.
    """
    if not loc:
        return ''
    parts = loc.split(':')
    # Keep descriptive middle components (e.g. "docstring of ..."), drop pure
    # line numbers so unrelated edits that shift lines don't churn the baseline.
    rest = [p for p in parts[1:] if not p.strip().isdigit()]
    if any(p.strip().startswith('docstring of ') for p in rest):
        return ':'.join(p.strip() for p in rest)
    return ':'.join([_relativize(parts[0])] + rest)


def _scrub_message(msg: str) -> str:
    """Rewrite absolute paths embedded in a warning message.

    Sphinx names the *other* end of a conflict by absolute path, e.g.
    ``duplicate label about, other instance in /abs/doc/doc/about.rst``.
    Without this the baseline only matches the machine that wrote it.
    """
    return _ABSPATH_RE.sub(lambda m: _relativize(m.group(1)), msg)


def _signature(match: 're.Match[str]') -> str:
    loc = _normalize_location(match.group('loc').strip())
    level = match.group('level')
    msg = _scrub_message(' '.join(match.group('msg').split()))
    if loc:
        return f'{loc}: {level}: {msg}'
    return f'{level}: {msg}'


def _always_fail(signature: str) -> str | None:
    """The explanation for *signature* if it can never be baselined, else None."""
    for pattern, explanation in _ALWAYS_FAIL:
        if pattern in signature:
            return explanation
    return None


def collect_warnings() -> set[str]:
    """Run a dummy sphinx build and return the set of normalized warning signatures."""
    tmp = tempfile.mkdtemp(prefix='doc_warncheck_')
    warnfile = os.path.join(tmp, 'warnings.txt')
    doctrees = os.path.join(tmp, 'doctrees')
    outdir = os.path.join(tmp, 'out')
    cmd = [
        sys.executable, '-m', 'sphinx',
        '-b', 'dummy',      # parse only; write no output
        '-E',               # ignore cached environment: re-read every source
        '-q',               # quiet: only warnings/errors on the console
        '-w', warnfile,     # also capture warnings to a file
        '-d', doctrees,
        '.', outdir,
    ]
    # Run from the source dir so conf.py's relative paths match `make html`.
    proc = subprocess.run(cmd, cwd=SRC_DIR, capture_output=True, text=True)

    signatures: set[str] = set()
    if os.path.exists(warnfile):
        with open(warnfile, encoding='utf-8', errors='replace') as fh:
            for line in fh:
                line = line.rstrip('\n')
                m = _WARNING_RE.match(line)
                if m:
                    signatures.add(_signature(m))

    # A crash (bad conf.py, import failure that aborts the build) exits non-zero
    # and may leave no warning file: surface it rather than reporting "clean".
    if proc.returncode != 0 and not signatures:
        sys.stderr.write(
            "sphinx-build failed before producing warnings "
            f"(exit {proc.returncode}):\n"
        )
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        sys.exit(2)

    return signatures


def load_baseline() -> set[str]:
    if not os.path.exists(BASELINE):
        return set()
    with open(BASELINE, encoding='utf-8') as fh:
        return {
            line.rstrip('\n')
            for line in fh
            if line.strip() and not line.startswith('#')
        }


def write_baseline(signatures: set[str]) -> None:
    """Rewrite the baseline, refusing to record anything in ``_ALWAYS_FAIL``."""
    header = (
        "# Baseline of pre-existing Clawpack documentation warnings.\n"
        "# Generated by tools/check_doc_warnings.py --update.\n"
        "# `make checkwarnings` fails only on warnings NOT listed here.\n"
        "#\n"
        "# Reproducible only against the toolchain in tools/requirements-docs.txt\n"
        "# and the Clawpack source tree in tools/clawpack-ref.txt.  Regenerate\n"
        "# with `make claw-pin && CLAW=$(cd ../.claw-pin && pwd) make\n"
        "# checkwarnings-update` in a virtualenv with no clawpack installed.\n"
    )
    recorded = {sig for sig in signatures if _always_fail(sig) is None}
    with open(BASELINE, 'w', encoding='utf-8') as fh:
        fh.write(header)
        for sig in sorted(recorded):
            fh.write(sig + '\n')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true',
                        help='rewrite the baseline from this run instead of comparing')
    parser.add_argument('--strict', action='store_true',
                        help='ignore the baseline and fail on ANY warning')
    args = parser.parse_args(argv)

    current = collect_warnings()

    # Grouped by explanation so each class is reported once, with its reason.
    fatal: dict[str, list[str]] = {}
    for sig in current:
        explanation = _always_fail(sig)
        if explanation is not None:
            fatal.setdefault(explanation, []).append(sig)

    def report_fatal() -> None:
        for explanation, sigs in sorted(fatal.items()):
            print(f"\n{len(sigs)} warning(s) that are never baselined -- "
                  f"{explanation}:\n")
            for sig in sorted(sigs):
                print(f"  {sig}")
        print("\nThis usually means the environment, not the docs, is wrong: "
              "run\n`python tools/check_doc_env.py` for the underlying import "
              "errors.")

    if args.update:
        write_baseline(current)
        n = len(current) - sum(len(v) for v in fatal.values())
        # Relative to the sphinx source dir, not $CLAW: $CLAW may be a pinned
        # tree somewhere else entirely, and "../doc/tools/..." helps nobody.
        print(f"Wrote {n} warning(s) to {os.path.relpath(BASELINE, SRC_DIR)}")
        if fatal:
            report_fatal()
            return 1
        return 0

    if args.strict:
        if current:
            print(f"{len(current)} documentation warning(s) (strict mode):\n")
            for sig in sorted(current):
                print(f"  {sig}")
            return 1
        print("No documentation warnings.")
        return 0

    baseline = load_baseline()
    new = current - baseline
    resolved = baseline - current

    if resolved:
        print(f"{len(resolved)} baseline warning(s) no longer present "
              "(consider `make checkwarnings-update`):\n")
        for sig in sorted(resolved):
            print(f"  - {sig}")
        print()

    # Reported separately from `new`, and before it: when the environment is
    # broken these dominate the diff, and telling someone to run
    # `checkwarnings-update` would be exactly the wrong advice.
    if fatal:
        report_fatal()
        return 1

    if new:
        print(f"{len(new)} NEW documentation warning(s):\n")
        for sig in sorted(new):
            print(f"  {sig}")
        print("\nFix these, or run `make checkwarnings-update` if intentional.")
        return 1

    print(f"No new documentation warnings ({len(current)} known, baselined).")
    return 0


if __name__ == '__main__':
    sys.exit(main())
