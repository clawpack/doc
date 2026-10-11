"""
Tests for tools/compare_autodoc.py.

Runnable either directly (``python tools/test_compare_autodoc.py``) or under
pytest.  The two "revisions" are git trees built with hash-object/mktree in a
throwaway repository, so no commits and no Sphinx are involved.
"""

import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import compare_autodoc  # noqa: E402


def page(entries):
    return ''.join('<dt class="sig sig-object py" id="x%d">\n' % i
                   for i in range(entries)) + '<p>text</p>\n'


def tree(repo, files):
    """Write *files* ({path: text}, one directory level at most) as a tree."""
    def blob(text):
        return subprocess.run(['git', '-C', repo, 'hash-object', '-w', '--stdin'],
                              input=text.encode(), capture_output=True,
                              check=True).stdout.decode().strip()

    def mktree(entries):
        listing = ''.join('%s %s %s\t%s\n' % e for e in entries)
        return subprocess.run(['git', '-C', repo, 'mktree'], input=listing.encode(),
                              capture_output=True, check=True).stdout.decode().strip()

    top, subdirs = [], {}
    for path, text in files.items():
        if '/' in path:
            d, name = path.split('/', 1)
            subdirs.setdefault(d, []).append(('100644', 'blob', blob(text), name))
        else:
            top.append(('100644', 'blob', blob(text), path))
    for d, entries in subdirs.items():
        top.append(('040000', 'tree', mktree(entries), d))
    return mktree(top)


def with_repo(test):
    def run():
        repo = tempfile.mkdtemp()
        try:
            subprocess.run(['git', 'init', '-q', repo], check=True)
            test(repo)
        finally:
            shutil.rmtree(repo)
    run.__name__ = test.__name__
    return run


@with_repo
def test_reports_emptied_and_shrunk_pages(repo):
    before = tree(repo, {'storm_module.html': page(22),
                         'v5.7.x/dtopo.html': page(73),
                         'v5.7.x/topo.html': page(34),
                         'about.html': '<p>no api</p>'})
    after = tree(repo, {'storm_module.html': page(0),
                        'v5.7.x/dtopo.html': page(59),
                        'v5.7.x/topo.html': page(35),
                        'about.html': '<p>still no api</p>'})
    rows = compare_autodoc.compare(repo, before, after)
    assert sorted(rows) == [('storm_module.html', 22, 0),
                            ('v5.7.x/dtopo.html', 73, 59),
                            ('v5.7.x/topo.html', 34, 35)]
    text = compare_autodoc.report(rows, limit=40)
    assert '2 page(s) lose entries, 1 of them down to zero' in text
    # Emptied pages are listed first.
    assert text.index('storm_module.html') < text.index('v5.7.x/dtopo.html')
    assert 'topo.html` |' not in text.replace('dtopo.html', '')


@with_repo
def test_no_drops(repo):
    before = tree(repo, {'a.html': page(3)})
    after = tree(repo, {'a.html': page(4) + '<p>edited</p>'})
    text = compare_autodoc.report(compare_autodoc.compare(repo, before, after), 40)
    assert 'No page loses entries.' in text


@with_repo
def test_added_and_deleted_pages(repo):
    before = tree(repo, {'gone.html': page(5), 'keep.html': page(1)})
    after = tree(repo, {'new.html': page(2), 'keep.html': page(1)})
    rows = sorted(compare_autodoc.compare(repo, before, after))
    assert rows == [('gone.html', 5, None), ('new.html', None, 2)]
    text = compare_autodoc.report(rows, 40)
    assert '| `gone.html` | 5 | - |' in text


@with_repo
def test_limit(repo):
    before = tree(repo, {'p%d.html' % i: page(5) for i in range(5)})
    after = tree(repo, {'p%d.html' % i: page(4) for i in range(5)})
    text = compare_autodoc.report(compare_autodoc.compare(repo, before, after), 2)
    assert '... 3 more' in text


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for test in tests:
        test()
        print('ok  %s' % test.__name__)
    print('\n%d passed' % len(tests))
