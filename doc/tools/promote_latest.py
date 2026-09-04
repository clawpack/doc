#!/usr/bin/env python
"""
Promote the latest documentation version to the root of a multi-version build.

This replaces the manual procedure that used to be documented in howto_doc.rst
and implemented by doc/fix_links_top_level.py.  The original text of that
script is preserved below because it is the only written record of *why* the
step exists:

    Script to use with this code for making multi-version docs:
        https://holzhaus.github.io/sphinx-multiversion/master/index.html

    Using sphinx-multiversion creates a _build/html directory that has a
    subdirectory for each version.  But the current version .html files are not
    in _build/html so you can only reach them if you point to a specific
    version.

    We copy _build/html/* to $CLAW/clawpack.github.org/ for hosting on the web.

    We want e.g. www.clawpack.org/installing.html to point to the current
    release (without having to specify e.g.
    www.clawpack.org/v5.6.1/installing.html).  This can be accomplished by
    copying the v5.6.1/* files up a level, but then the links in the sidebar
    don't work properly for reaching other versions.

    This script fixes those links.

Why this exists as a script rather than two shell lines
-------------------------------------------------------
The documented procedure was::

    cd _build/html
    cp -r v5.7.x/* .   # replace v5.7.x with the current version
    python ../../fix_links_top_level.py

That had three problems:

1. The version number was hardcoded in prose, so it had to be remembered at
   release time.  We read ``smv_latest_version`` from ``conf.py`` instead, so
   there is exactly one place to update.

2. ``cp -r v5.7.x/*`` does not match dotfiles, so ``.nojekyll`` (and
   ``CNAME``, ``.buildinfo``) were never promoted to the root.  The published
   site has a root ``.nojekyll`` only because nothing has ever deleted it --
   and without it GitHub Pages would refuse to serve the ``_static`` and
   ``_sources`` directories.  We copy the directory *contents* including
   dotfiles.

3. ``fix_links_top_level.py`` only rewrote ``*.html``, ``riemann/*.html`` and
   ``pyclaw/*.html``, so pages nested any deeper kept a wrong number of
   ``../`` segments in their version-switcher links.  We rewrite every HTML
   file at whatever depth it happens to live.

How the link rewrite works
--------------------------
``sphinx_multiversion.sphinx.VersionInfo.vpathto`` builds each switcher link as
a path relative to the *current page*, from one version directory across to
another::

    <html>/v5.14.x/about.html         -> "../dev/about.html"
    <html>/v5.14.x/pyclaw/about.html  -> "../../dev/pyclaw/about.html"

i.e. a page at depth ``d`` inside its version directory gets ``d + 1`` leading
``../`` segments.  Promoting that version's tree up one level (to the site
root) removes one level of nesting, so every such link needs exactly one fewer
``../``.  At depth 0 there is no ``../`` left, so the link becomes ``./``.

We match on the *exact* version directory names taken from the build, e.g.
``../dev/`` and ``../../v5.12.x/``, rather than on the ``../dev`` / ``../v5``
substrings the old script used.  That matters: a substring rewrite of ``../v5``
would also corrupt an ordinary relative link to any path beginning with
``v5``, and it silently did nothing for versions not named ``dev`` or ``v5*``.
"""

import argparse
import os
import re
import shutil
import sys

# Directory holding this script (doc/tools), and the Sphinx source dir (doc).
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.dirname(TOOLS_DIR)


def read_latest_version(conf_py):
    """Return ``smv_latest_version`` as declared in *conf_py*.

    Parsed textually rather than by importing conf.py: importing it pulls in
    the whole Sphinx configuration (and the clawpack packages autodoc needs),
    which we neither want nor need in order to read one string.
    """
    with open(conf_py, "r") as f:
        source = f.read()

    match = re.search(
        r"""^smv_latest_version\s*=\s*['"]([^'"]+)['"]""",
        source,
        re.MULTILINE,
    )
    if match is None:
        sys.exit(
            "%s does not define smv_latest_version; cannot tell which "
            "version to promote to the site root." % conf_py
        )
    return match.group(1)


def find_version_dirs(html_dir):
    """Return the version directory names in *html_dir*, sorted.

    sphinx-multiversion writes one directory per built ref into the output
    root and nothing else, so the immediate subdirectories *are* the versions.
    This must be called before anything is copied to the root, since promoting
    adds the latest version's own subdirectories (pyclaw/, riemann/, ...)
    alongside them.
    """
    return sorted(
        name
        for name in os.listdir(html_dir)
        if os.path.isdir(os.path.join(html_dir, name))
    )


def copy_to_root(html_dir, latest):
    """Copy the contents of ``html_dir/latest`` up into ``html_dir``.

    Includes dotfiles (``.nojekyll``, ``CNAME``, ``.buildinfo``), which the
    documented ``cp -r <version>/*`` silently skipped.  Existing files are
    overwritten; unrelated files already at the root are left alone, so this
    is additive with respect to anything the build did not produce.
    """
    src = os.path.join(html_dir, latest)
    for name in sorted(os.listdir(src)):
        src_path = os.path.join(src, name)
        dest_path = os.path.join(html_dir, name)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dest_path)


def build_replacements(version_dirs, depth):
    """Return (old, new) link-prefix pairs for a page at *depth*.

    A page at depth ``d`` in a version directory refers to sibling versions
    with ``d + 1`` leading ``../`` segments; once promoted to the root it
    needs ``d``.  Depth 0 has no segments left, so it becomes ``./``.
    """
    old_prefix = "../" * (depth + 1)
    new_prefix = "../" * depth if depth else "./"
    return [
        ("%s%s/" % (old_prefix, version), "%s%s/" % (new_prefix, version))
        for version in version_dirs
    ]


def fix_links(html_dir, version_dirs, latest):
    """Rewrite version-switcher links in the promoted copy at the root.

    Walks only the files that were promoted -- the version directories
    themselves are correct as built and must not be touched.
    """
    n_files = 0
    n_edits = 0

    for dirpath, dirnames, filenames in os.walk(html_dir):
        rel_dir = os.path.relpath(dirpath, html_dir)
        if rel_dir == ".":
            # Don't descend into the version directories; their links are
            # already right, and rewriting them would break them.
            dirnames[:] = [d for d in dirnames if d not in version_dirs]
            depth = 0
        else:
            depth = len(rel_dir.split(os.sep))

        replacements = build_replacements(version_dirs, depth)

        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            path = os.path.join(dirpath, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            original = text
            for old, new in replacements:
                text = text.replace(old, new)

            if text != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                n_edits += 1
            n_files += 1

    print(
        "Rewrote version links in %d of %d promoted HTML file(s) "
        "(promoted version: %s)" % (n_edits, n_files, latest)
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "html_dir",
        nargs="?",
        default=os.path.join(DOC_DIR, "_build", "html"),
        help="multi-version build output directory "
        "(default: doc/_build/html)",
    )
    parser.add_argument(
        "--conf",
        default=os.path.join(DOC_DIR, "conf.py"),
        help="path to conf.py, read for smv_latest_version "
        "(default: doc/conf.py)",
    )
    args = parser.parse_args(argv)

    html_dir = os.path.abspath(args.html_dir)
    if not os.path.isdir(html_dir):
        sys.exit(
            "%s does not exist; run `make versions` first." % html_dir
        )

    latest = read_latest_version(args.conf)
    version_dirs = find_version_dirs(html_dir)

    if not version_dirs:
        sys.exit(
            "%s contains no version directories; `make versions` did not "
            "produce a usable build." % html_dir
        )

    if latest not in version_dirs:
        sys.exit(
            "smv_latest_version is %r but %s contains only %s.\n"
            "Either the whitelists in conf.py exclude the latest version, or "
            "smv_latest_version is stale."
            % (latest, html_dir, ", ".join(version_dirs))
        )

    if not os.path.isfile(os.path.join(html_dir, latest, "index.html")):
        sys.exit(
            "%s has no index.html; refusing to promote an incomplete build."
            % os.path.join(html_dir, latest)
        )

    print("Promoting %s to the root of %s" % (latest, html_dir))
    print("Versions in this build: %s" % ", ".join(version_dirs))

    copy_to_root(html_dir, latest)
    fix_links(html_dir, version_dirs, latest)

    if not os.path.isfile(os.path.join(html_dir, "index.html")):
        sys.exit("promotion did not produce %s/index.html" % html_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
