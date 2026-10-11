"""
Tests for tools/promote_latest.py.

Runnable either directly (``python tools/test_promote_latest.py``) or under
pytest.  These build a synthetic multi-version tree rather than invoking
Sphinx, so they are fast and have no dependency on the doc toolchain.

The link shapes asserted here come from
``sphinx_multiversion.sphinx.VersionInfo.vpathto``, which emits a switcher
link with ``depth + 1`` leading ``../`` segments for a page at ``depth``
inside its version directory.
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_latest  # noqa: E402


def build_tree(root):
    """Create a synthetic sphinx-multiversion output tree under *root*."""
    html = os.path.join(root, "html")
    for sub in (
        "v5.14.x/pyclaw/evolve",
        "v5.14.x/_static",
        "dev/pyclaw",
        "v5.12.x",
    ):
        os.makedirs(os.path.join(html, sub))

    # Depth 0 page in the version being promoted.  The last link is a decoy:
    # it starts with "../v5" but is not a version directory, so the old
    # substring-based rewrite would have corrupted it.
    depth0 = (
        '<a href="../dev/index.html">dev</a>\n'
        '<a href="../v5.12.x/index.html">v5.12.x</a>\n'
        '<a href="_static/style.css">css</a>\n'
        '<a href="../v5wxyz/thing.html">not a version</a>\n'
    )
    for name in ("index.html", "about.html"):
        with open(os.path.join(html, "v5.14.x", name), "w") as f:
            f.write(depth0)

    depth1 = (
        '<a href="../../dev/pyclaw/about.html">dev</a>\n'
        '<a href="../../v5.12.x/pyclaw/about.html">v5.12.x</a>\n'
        '<a href="../_static/style.css">css</a>\n'
    )
    with open(os.path.join(html, "v5.14.x", "pyclaw", "about.html"), "w") as f:
        f.write(depth1)

    # Depth 2 -- the case fix_links_top_level.py never reached.
    depth2 = '<a href="../../../dev/pyclaw/evolve/limiters.html">dev</a>\n'
    with open(
        os.path.join(html, "v5.14.x", "pyclaw", "evolve", "limiters.html"), "w"
    ) as f:
        f.write(depth2)

    # Dotfiles that `cp -r <version>/*` would have skipped.
    open(os.path.join(html, "v5.14.x", ".nojekyll"), "w").close()
    with open(os.path.join(html, "v5.14.x", "CNAME"), "w") as f:
        f.write("www.clawpack.org\n")

    with open(os.path.join(html, "dev", "index.html"), "w") as f:
        f.write('<a href="../v5.14.x/index.html">latest</a>\n')
    with open(os.path.join(html, "v5.12.x", "index.html"), "w") as f:
        f.write("older\n")

    conf = os.path.join(root, "conf.py")
    with open(conf, "w") as f:
        f.write("smv_latest_version = 'v5.14.x'\n")

    return html, conf


def read(*parts):
    with open(os.path.join(*parts)) as f:
        return f.read()


def test_promote_rewrites_links_at_every_depth():
    root = tempfile.mkdtemp()
    try:
        html, conf = build_tree(root)
        promote_latest.main([html, "--conf", conf])

        # Depth 0: one ../ segment removed, so ./ remains.
        top = read(html, "index.html")
        assert '<a href="./dev/index.html">' in top
        assert '<a href="./v5.12.x/index.html">' in top
        # A same-directory asset link must be untouched...
        assert '<a href="_static/style.css">' in top
        # ...and so must a non-version path that merely looks like one.
        assert '<a href="../v5wxyz/thing.html">' in top

        # Depth 1: two segments become one.
        d1 = read(html, "pyclaw", "about.html")
        assert '<a href="../dev/pyclaw/about.html">' in d1
        assert '<a href="../v5.12.x/pyclaw/about.html">' in d1
        assert '<a href="../_static/style.css">' in d1

        # Depth 2: three become two.  This is the regression the old script
        # left on the live site.
        d2 = read(html, "pyclaw", "evolve", "limiters.html")
        assert '<a href="../../dev/pyclaw/evolve/limiters.html">' in d2
    finally:
        shutil.rmtree(root)


def test_promote_carries_dotfiles():
    root = tempfile.mkdtemp()
    try:
        html, conf = build_tree(root)
        promote_latest.main([html, "--conf", conf])

        # Without these GitHub Pages would not serve _static/_sources, and the
        # custom domain would be dropped.
        assert os.path.isfile(os.path.join(html, ".nojekyll"))
        assert read(html, "CNAME").strip() == "www.clawpack.org"
    finally:
        shutil.rmtree(root)


def test_version_directories_are_left_alone():
    root = tempfile.mkdtemp()
    try:
        html, conf = build_tree(root)
        before_latest = read(html, "v5.14.x", "index.html")
        before_dev = read(html, "dev", "index.html")

        promote_latest.main([html, "--conf", conf])

        # The per-version trees are correct as built; rewriting them would
        # break the switcher inside each version.
        assert read(html, "v5.14.x", "index.html") == before_latest
        assert read(html, "dev", "index.html") == before_dev
    finally:
        shutil.rmtree(root)


def test_missing_latest_version_is_an_error():
    root = tempfile.mkdtemp()
    try:
        html, conf = build_tree(root)
        with open(conf, "w") as f:
            f.write("smv_latest_version = 'v9.9.x'\n")

        try:
            promote_latest.main([html, "--conf", conf])
        except SystemExit as exc:
            assert exc.code != 0
            assert "v9.9.x" in str(exc.code)
        else:
            raise AssertionError("expected a non-zero exit")
    finally:
        shutil.rmtree(root)


def test_empty_build_is_an_error():
    root = tempfile.mkdtemp()
    try:
        html = os.path.join(root, "html")
        os.makedirs(html)
        conf = os.path.join(root, "conf.py")
        with open(conf, "w") as f:
            f.write("smv_latest_version = 'v5.14.x'\n")

        try:
            promote_latest.main([html, "--conf", conf])
        except SystemExit as exc:
            assert exc.code != 0
        else:
            raise AssertionError("expected a non-zero exit")
    finally:
        shutil.rmtree(root)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print("ok  %s" % test.__name__)
    print("\n%d passed" % len(tests))
