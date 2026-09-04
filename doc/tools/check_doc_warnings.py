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

Because autodoc imports the clawpack packages, the set of warnings depends on
the build environment.  Regenerate the baseline (``--update``) in the same
environment the CI workflow uses so the signatures agree.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile


# tools/ -> doc/doc (source dir) -> .../clawpack (the $CLAW root)
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(TOOLS_DIR)
CLAW_ROOT = os.path.abspath(os.path.join(SRC_DIR, os.pardir, os.pardir))
BASELINE = os.path.join(TOOLS_DIR, 'doc_warnings_baseline.txt')

# A sphinx warning line looks like one of:
#   /abs/path/foo.rst:123: WARNING: message
#   /abs/path/mod.py:docstring of pkg.mod.Cls:7: ERROR: message
#   WARNING: message                         (no location)
_WARNING_RE = re.compile(
    r'^(?P<loc>.*?)(?:: )?(?P<level>WARNING|ERROR|SEVERE|CRITICAL): '
    r'(?P<msg>.*)$'
)


def _relativize(path: str) -> str:
    """Return *path* relative to the $CLAW root when possible, else unchanged."""
    if not path:
        return path
    abspath = path if os.path.isabs(path) else os.path.join(SRC_DIR, path)
    try:
        rel = os.path.relpath(abspath, CLAW_ROOT)
    except ValueError:  # different drive on Windows
        return path
    # Only rewrite paths that actually live under the $CLAW root.
    return rel if not rel.startswith(os.pardir) else path


def _normalize_location(loc: str) -> str:
    """Drop absolute prefixes and volatile line numbers from a warning's location.

    ``/abs/mod.py:docstring of pkg.Cls:7`` -> ``geoclaw/.../mod.py:docstring of pkg.Cls``
    ``/abs/foo.rst:123``                    -> ``doc/doc/foo.rst``
    """
    if not loc:
        return ''
    parts = loc.split(':')
    filepart = _relativize(parts[0])
    # Keep descriptive middle components (e.g. "docstring of ..."), drop pure
    # line numbers so unrelated edits that shift lines don't churn the baseline.
    rest = [p for p in parts[1:] if not p.strip().isdigit()]
    return ':'.join([filepart] + rest)


def _signature(match: 're.Match[str]') -> str:
    loc = _normalize_location(match.group('loc').strip())
    level = match.group('level')
    msg = ' '.join(match.group('msg').split())
    if loc:
        return f'{loc}: {level}: {msg}'
    return f'{level}: {msg}'


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
    header = (
        "# Baseline of pre-existing Clawpack documentation warnings.\n"
        "# Generated by tools/check_doc_warnings.py --update.\n"
        "# `make checkwarnings` fails only on warnings NOT listed here.\n"
        "# Regenerate in the same environment the CI workflow uses.\n"
    )
    with open(BASELINE, 'w', encoding='utf-8') as fh:
        fh.write(header)
        for sig in sorted(signatures):
            fh.write(sig + '\n')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true',
                        help='rewrite the baseline from this run instead of comparing')
    parser.add_argument('--strict', action='store_true',
                        help='ignore the baseline and fail on ANY warning')
    args = parser.parse_args(argv)

    current = collect_warnings()

    if args.update:
        write_baseline(current)
        print(f"Wrote {len(current)} warning(s) to {os.path.relpath(BASELINE, CLAW_ROOT)}")
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
