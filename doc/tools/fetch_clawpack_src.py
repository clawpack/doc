#!/usr/bin/env python
# encoding: utf-8
r"""
Materialise the pinned Clawpack source tree the docs are built against.

``doc/conf.py`` puts the *parent of this repository* on ``sys.path`` and relies
on clawpack/clawpack's ``clawpack/__init__.py`` shim to map ``clawpack.geoclaw``
onto ``geoclaw/src/python/geoclaw`` and friends.  autodoc therefore documents
source checkouts, and the doc build is reproducible only if those checkouts are
pinned.  The pins live in ``tools/clawpack-ref.txt``; this script turns them
into a real directory tree::

    <dest>/clawpack/__init__.py     the namespace shim (from the super-repo)
    <dest>/geoclaw/ ...             each subrepo, detached at its pinned SHA
    <dest>/doc/                     this repository (created by the caller)

Usage
-----
    fetch_clawpack_src.py <dest> [--reference DIR] [--quiet]
    fetch_clawpack_src.py <dest> --check

``--reference DIR`` treats ``DIR`` as a directory of existing Clawpack clones
(e.g. an ordinary ``$CLAW``) and borrows their objects, which makes a local
materialisation nearly instant and mostly offline.  Objects are copied rather
than shared, so the result stays valid if the reference clones later move.

``--check`` verifies an existing tree matches the manifest and exits non-zero
otherwise.  ``make checkwarnings-update`` uses it to refuse to write a baseline
from an unpinned tree.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys


TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(TOOLS_DIR, 'clawpack-ref.txt')

# The super-repo is checked out as <dest> itself, not <dest>/clawpack: it is
# what carries the clawpack/ shim package and the submodule directory layout.
SUPER_REPO = 'clawpack'

_SHA_RE = re.compile(r'^[0-9a-f]{40}$')


def read_manifest(path: str = MANIFEST) -> list[tuple[str, str]]:
    """Return the manifest as an ordered list of ``(repo, sha)`` pairs."""
    entries = []
    with open(path, encoding='utf-8') as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            fields = line.split()
            if len(fields) != 2:
                raise SystemExit(
                    f'{path}:{lineno}: expected "<repo> <sha>", got: {line!r}')
            repo, sha = fields
            if not _SHA_RE.match(sha):
                raise SystemExit(
                    f'{path}:{lineno}: {repo} is not pinned to a full '
                    f'40-character SHA: {sha!r}')
            entries.append((repo, sha))
    if not any(repo == SUPER_REPO for repo, _ in entries):
        raise SystemExit(f'{path}: no "{SUPER_REPO}" entry; the shim package '
                         'that makes `import clawpack.geoclaw` work comes '
                         'from the super-repo')
    return entries


def _run(cmd: list[str], cwd: str | None = None, quiet: bool = False) -> None:
    if not quiet:
        print('  $ ' + ' '.join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL if quiet else None)


def _head(repo_dir: str) -> str | None:
    """The checked-out SHA of *repo_dir*, or None if it is not a git repo."""
    try:
        out = subprocess.run(['git', '-C', repo_dir, 'rev-parse', 'HEAD'],
                             capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return out.stdout.strip()


def _materialise(repo: str, sha: str, target: str, reference: str | None,
                 quiet: bool) -> None:
    """Ensure *target* is a checkout of clawpack/<repo> detached at *sha*."""
    if _head(target) == sha:
        if not quiet:
            print(f'{repo}: already at {sha[:8]}')
        return

    url = f'https://github.com/clawpack/{repo}.git'
    if not os.path.isdir(os.path.join(target, '.git')):
        os.makedirs(target, exist_ok=True)
        clone = ['git', 'clone', '--quiet', '--no-checkout']
        if reference:
            ref_dir = os.path.join(reference, repo)
            if os.path.isdir(os.path.join(ref_dir, '.git')):
                # --dissociate copies the borrowed objects in, so the result
                # does not break if the reference clone is later pruned.
                clone += ['--reference-if-able', ref_dir, '--dissociate']
        _run(clone + [url, target], quiet=quiet)

    # `git fetch <url> <sha>` works for any commit the server will serve,
    # including ones not reachable from a branch tip we happen to have.
    _run(['git', '-C', target, 'fetch', '--quiet', '--tags', url, sha],
         quiet=quiet)
    _run(['git', '-C', target, 'checkout', '--quiet', '--detach', sha],
         quiet=quiet)
    print(f'{repo}: {sha[:8]}')


def materialise(dest: str, reference: str | None = None,
                quiet: bool = False) -> None:
    """Build the pinned $CLAW tree at *dest*."""
    entries = read_manifest()
    dest = os.path.abspath(dest)

    # The super-repo first: it owns <dest> itself, and the subrepos land in
    # the (empty) submodule directories it provides.
    for repo, sha in entries:
        target = dest if repo == SUPER_REPO else os.path.join(dest, repo)
        _materialise(repo, sha, target, reference, quiet)

    shim = os.path.join(dest, SUPER_REPO, '__init__.py')
    if not os.path.exists(shim):
        raise SystemExit(f'{shim} missing -- `import clawpack.geoclaw` cannot '
                         'work without the super-repo namespace shim')


def check(dest: str) -> int:
    """Report whether *dest* matches the manifest.  Returns an exit status."""
    entries = read_manifest()
    dest = os.path.abspath(dest)
    problems = []
    for repo, sha in entries:
        target = dest if repo == SUPER_REPO else os.path.join(dest, repo)
        head = _head(target)
        if head is None:
            problems.append(f'  {repo:<10} MISSING            (want {sha[:8]})')
        elif head != sha:
            problems.append(f'  {repo:<10} {head[:8]}  != pinned {sha[:8]}')

    if problems:
        print(f'{dest} does not match tools/clawpack-ref.txt:\n')
        print('\n'.join(problems))
        print('\nThe warning baseline is only reproducible against the pinned '
              'tree.\nRun `make claw-pin` to materialise it, or bump '
              'tools/clawpack-ref.txt.')
        return 1

    print(f'{dest} matches tools/clawpack-ref.txt ({len(entries)} repos).')
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dest', help='directory to build the $CLAW tree in')
    parser.add_argument('--reference', metavar='DIR',
                        help='borrow objects from existing clones under DIR')
    parser.add_argument('--check', action='store_true',
                        help='verify an existing tree instead of building one')
    parser.add_argument('--quiet', action='store_true',
                        help='only report the resulting SHAs')
    args = parser.parse_args(argv)

    if args.check:
        return check(args.dest)

    materialise(args.dest, args.reference, args.quiet)
    return 0


if __name__ == '__main__':
    sys.exit(main())
