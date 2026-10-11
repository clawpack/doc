#!/usr/bin/env python
# encoding: utf-8
r"""
Report HTML pages whose autodoc content shrank between two site revisions.

The publish workflow's ``stage`` job runs this on the site clone, comparing the
published revision with the staged commit, and appends the report to the step
summary -- so whoever approves a publish sees which API pages lose entries
before anything goes live.

It exists because of the first full-site publish attempt: every release's
storm_module.html went from 22 documented entries to 0, which a file-count
diff shows as an ordinary modification.  Here that is a line of its own.

An "entry" is one ``<dt class="sig ...">``: a documented class, function,
method or attribute.  A drop is not necessarily wrong -- v5.7.x legitimately
loses classes its old pages documented from newer code -- so this reports and
does not fail.

Usage
-----
    compare_autodoc.py <site repo> <before rev> <after rev> [--limit N]

Revisions may be commits or trees.  Output is Markdown.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

ENTRY = b'<dt class="sig'


def changed_pages(repo: str, before: str, after: str) -> list[str]:
    out = subprocess.run(
        ['git', '-C', repo, 'diff', '--name-only', '--no-renames', before,
         after, '--', '*.html'],
        capture_output=True, check=True).stdout
    return [line for line in out.decode().splitlines() if line]


def count_entries(repo: str, specs: list[str]) -> dict[str, int | None]:
    """``{rev:path: entry count}`` for each spec; None where it does not exist.

    One `git cat-file --batch` for all of them: a full-site publish touches
    well over a thousand pages, and a process per blob is slow.
    """
    proc = subprocess.run(['git', '-C', repo, 'cat-file', '--batch'],
                          input=''.join(s + '\n' for s in specs).encode(),
                          capture_output=True, check=True)
    data, pos, counts = proc.stdout, 0, {}
    for spec in specs:
        end = data.index(b'\n', pos)
        header = data[pos:end].split()
        pos = end + 1
        if header[-1] == b'missing':
            counts[spec] = None
            continue
        size = int(header[2])
        counts[spec] = data[pos:pos + size].count(ENTRY)
        pos += size + 1
    return counts


def compare(repo: str, before: str, after: str) -> list[tuple[str, int | None, int | None]]:
    """``(page, before, after)`` for every changed page with autodoc entries."""
    pages = changed_pages(repo, before, after)
    counts = count_entries(repo, [f'{before}:{p}' for p in pages]
                           + [f'{after}:{p}' for p in pages])
    rows = []
    for page in pages:
        old, new = counts[f'{before}:{page}'], counts[f'{after}:{page}']
        if old or new:
            rows.append((page, old, new))
    return rows


def report(rows: list[tuple[str, int | None, int | None]], limit: int) -> str:
    total_old = sum(old or 0 for _, old, _ in rows)
    total_new = sum(new or 0 for _, _, new in rows)
    drops = sorted((r for r in rows if (r[2] or 0) < (r[1] or 0)),
                   key=lambda r: ((r[2] or 0) != 0, (r[2] or 0) - (r[1] or 0), r[0]))
    emptied = [r for r in drops if not r[2]]

    lines = ['### Autodoc entries on changed pages', '',
             f'{len(rows)} changed page(s) have API entries: '
             f'{total_old} before, {total_new} after.']
    if not drops:
        lines += ['', 'No page loses entries.']
        return '\n'.join(lines) + '\n'

    lines += ['', f'**{len(drops)} page(s) lose entries'
              + (f', {len(emptied)} of them down to zero' if emptied else '')
              + '.**  Check these before approving: a page emptied by an '
              'import failure looks like any other modification in the diff.',
              '', '| page | before | after |', '|---|---:|---:|']
    for page, old, new in drops[:limit]:
        lines.append(f'| `{page}` | {old if old is not None else "-"} '
                     f'| {new if new is not None else "-"} |')
    if len(drops) > limit:
        lines.append(f'| ... {len(drops) - limit} more | | |')
    return '\n'.join(lines) + '\n'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('repo')
    parser.add_argument('before')
    parser.add_argument('after')
    parser.add_argument('--limit', type=int, default=40,
                        help='most pages to list (default 40)')
    args = parser.parse_args(argv)
    sys.stdout.write(report(compare(args.repo, args.before, args.after),
                            args.limit))
    return 0


if __name__ == '__main__':
    sys.exit(main())
