.. _howto_doc:

Guide for updating this documentation
=============================================

This guide covers building, checking and publishing the Clawpack
documentation and gallery.  For the release procedure as a whole, see
:ref:`howto_release`.  Both guides live in the
`clawpack/doc <https://github.com/clawpack/doc>`_ repository as
`doc/howto_doc.rst` and `doc/howto_release.rst`, and its `README.md` links
to them.

The `clawpack/doc` repository is not included in the Clawpack distribution
and must be cloned separately, normally into `$CLAW/doc`.  The main
documentation sources are in `$CLAW/doc/doc` and the gallery in
`$CLAW/doc/gallery`; these are two separate Sphinx projects.

.. _howto_doc_tasks:

Quick reference
---------------

========================================================  =======================================
I want to...                                              See
========================================================  =======================================
Set up an environment that can build the docs             :ref:`howto_doc_env`
Preview my edit locally                                   :ref:`howto_doc_preview`
Check that I have not added Sphinx warnings               :ref:`howto_doc_warnings`
Build the whole multiversion site locally                 :ref:`howto_doc_versions`
Get my change onto www.clawpack.org                       :ref:`howto_doc_publish`
Update the docs for a new release                         :ref:`howto_release_doc`
Start a new 5.x series branch                             :ref:`howto_doc_major`
Update the gallery                                        :ref:`howto_doc_gallery`
========================================================  =======================================

**What is automated:** every PR to `dev` or the current release branch gets a
warning check (`.github/workflows/docs.yml`) and a downloadable single-version
preview (`.github/workflows/docs-publish.yml`).  Every merge to `dev`
republishes `www.clawpack.org/dev/` with no approval needed.  Everything else
-- the top-level pages, the release version directories and the gallery -- is
published only when a maintainer asks for it.

.. _howto_doc_env:

Setting up a build environment
------------------------------

`autodoc` documents a Clawpack **source tree**, not an installed clawpack (see
:ref:`howto_doc_pinned_tree`), so the build environment must *not* have
clawpack installed.  Most local build failures come from this.

#. Start from a shell with no Clawpack environment active: `deactivate` any
   virtualenv or conda env that has clawpack installed (in particular an
   editable `pip install -e`), and `unset PYTHONPATH`.
#. Create a fresh virtualenv and install the pinned toolchain from
   `doc/tools/requirements-docs.txt` (Python 3.12, as CI uses)::

       cd $CLAW/doc/doc
       python3.12 -m venv ~/.venvs/clawdoc
       source ~/.venvs/clawdoc/bin/activate
       pip install -r tools/requirements-docs.txt

   Do not use `pip install --user` inside a virtualenv; it is refused there.
   `sphinx-multiversion` is in the requirements file, so nothing else needs
   installing.
#. Check that autodoc can import everything from `$CLAW`::

       make checkenv

   This reports an installed clawpack shadowing the source tree, a stray
   `PYTHONPATH`, and any module that will not import.

.. _howto_doc_preview:

Previewing a change (single version)
------------------------------------

::

    cd $CLAW/doc/doc
    git checkout dev
    make html

This runs `sphinx-build -b html . _build1/html` on your working tree, against
whatever `$CLAW` points at.  Open `_build1/html/index.html` in a browser.
It is fast to rebuild, but it has no version sidebar and is **not**
publishable; `_build1` is kept separate from the multiversion `_build` so a
quick build never clobbers it.

The same build of each PR is attached to its `docs-publish` run as the
`docs-preview-<PR number>` artifact.

.. _howto_doc_warnings:

Checking for documentation warnings
-----------------------------------

Sphinx does not fail the build on reStructuredText or docstring problems
(a missing blank line before a list, a bad cross reference, an autodoc import
issue, and so on), and they are easy to miss on the command line.  The
following `make` targets catch them before they are merged.

To fail on any warning that is **new** relative to a committed baseline
(`tools/doc_warnings_baseline.txt`)::

    cd $CLAW/doc/doc
    make checkwarnings

This does a full re-parse using the lightweight `dummy` builder (no HTML is
written) and compares the result against the baseline.  Only newly
introduced warnings cause a non-zero exit, so the backlog can be fixed
gradually.

If you intentionally add or remove warnings (e.g. after fixing a batch of
them), regenerate and commit the baseline with `make checkwarnings-update` --
but see :ref:`howto_doc_pinned_tree` first, because it only produces a
reproducible result in the pinned environment.

To ignore the baseline entirely and report **every** remaining warning::

    make checkwarnings-strict

The same check runs in CI (`.github/workflows/docs.yml`) on pull requests to
`dev` and the current release branch.

.. note::

   One warning class is never baselined: `autodoc: failed to import` means
   the API pages for those modules come out **empty**.
   `check_doc_warnings.py` reports them separately and fails regardless, and
   `tools/check_built_site.sh` independently asserts that the built `dev`
   API pages contain generated content before anything is published.

.. _howto_doc_pinned_tree:

The pinned source tree
^^^^^^^^^^^^^^^^^^^^^^

`conf.py` puts `$CLAW` on `sys.path`, and the `clawpack/__init__.py` shim in
the `clawpack/clawpack` super-repo maps `clawpack.geoclaw` onto
`geoclaw/src/python/geoclaw`, and so on.  So the set of warnings depends on
which Clawpack you are pointing at as much as on the docs themselves, and two
files pin that:

`tools/requirements-docs.txt`
    the Sphinx toolchain and the third-party packages Clawpack imports, all
    at exact versions.

`tools/clawpack-ref.txt`
    each Clawpack repository, by commit.

`make claw-pin` clones the second into `$CLAW/doc/.claw-pin` (borrowing
objects from your own checkouts, so it takes seconds), and setting `CLAW`
selects it.  To regenerate the baseline, in the environment from
:ref:`howto_doc_env`::

    cd $CLAW/doc/doc
    make claw-pin
    CLAW=$(cd ../.claw-pin && pwd) make checkwarnings-update

Then commit `tools/doc_warnings_baseline.txt`.  `checkwarnings-update`
refuses to run against a tree that does not match the pin.

To bump the pinned Clawpack, edit `tools/clawpack-ref.txt` and repeat the
regeneration above in the same commit.

.. _howto_doc_release_trees:

Released versions: one source tree each
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`tools/clawpack-ref.txt` is the tree for `dev`.  A multiversion build documents
each **released** version against the code that release shipped instead:
`tools/clawpack-release-refs.txt` maps every built release (`v5.7.x`,
`v5.8.x`, ...) to the `clawpack/clawpack` commit of its newest patch tag, and
the subrepos come from that commit's submodule pointers.

This matters because `sphinx-multiversion` builds every version with *this*
checkout's `conf.py`.  Against one current tree, a release's API pages
document code it never had, and a module renamed since the release documents
nothing at all: `storm_module.html` came out empty on every release once
`surge.storm` became a re-export of `met.storm`, with no warning.

`make claw-releases` clones one tree per row into `$CLAW/doc/.claw-releases`
(borrowing objects from your checkouts, so all of them take about a minute),
and `ext/clawpack_source.py` swaps the right one onto `sys.path` as each
version starts.  `$CLAW_VERSION_TREES` points the build at trees somewhere
else.

Three checks keep this honest:

- `make check-versions` fails if a built release has no row in
  `tools/clawpack-release-refs.txt`, a row names a version that is not built,
  or a release tree is missing or at the wrong commit.
- The build fails if autodoc cannot import anything, in any version.  (That
  catches modules that are gone; it cannot catch the re-export case above,
  which imports fine and documents nothing.)
- The publish workflow's `stage` summary lists every page that loses API
  entries compared with the published site, before anyone approves a publish.

Releases before 5.8 import the `imp` module, which Python 3.12 removed;
`ext/clawpack_source.py` provides the one function they use.

.. _howto_doc_versions:

Building the multiversion site locally
--------------------------------------

This builds what www.clawpack.org shows: the current release at the top
level, plus `dev/`, `v5.13.x/`, ... each with a version sidebar.  You do not
need it to publish (CI does the same build; see :ref:`howto_doc_publish`),
but it is the way to check a change that affects several versions, or to
reproduce a CI failure.

`sphinx-multiversion` builds from committed git refs, never your working
tree, so commit what you want to see first.  Then, in the environment from
:ref:`howto_doc_env`, run these **in this order**::

    cd $CLAW/doc/doc
    git fetch upstream --tags            # all v5.*.x tags must exist locally
    git branch v5.14.x upstream/v5.14.x  # only if you have never checked it out
    make claw-pin                        # 1. dev's source tree
    make claw-releases                   # 2. one source tree per release
    CLAW=$(cd ../.claw-pin && pwd) make versions-publish   # 3. build + promote

Step 2 must come before step 3: without the release trees,
`make check-versions` (which `make versions` runs first) stops with a list of
what is missing.  Expect several minutes; add `SPHINXOPTS=--jobs=auto` to
build in parallel.

`make versions-publish` is equivalent to::

    make clean-versions      # rm -rf _build
    make versions            # check-versions, then sphinx-multiversion . _build/html
    make versions-promote    # python tools/promote_latest.py _build/html

Open `_build/html/index.html`, which is the current release.  To check the
result the way CI does::

    cd $CLAW/doc
    ./doc/tools/check_built_site.sh doc/_build/html

Which versions get built
^^^^^^^^^^^^^^^^^^^^^^^^

These lines of `conf.py` choose the versions::

    smv_tag_whitelist = r'^v\d+\.\d+\.x$'          # tags v5.7.x, v5.8.x, ...
    smv_branch_whitelist = r'^(dev|v5\.14\.x)$'    # dev + current release
    smv_latest_version = 'v5.14.x'                 # promoted to the top level

`make check-versions` prints exactly which versions will be built and why
any are missing.  Two traps it guards against:

- `sphinx-multiversion` only considers **local** branches and tags; it
  ignores remote-tracking refs such as `upstream/v5.14.x`.  If you have never
  checked out the release branch it is silently dropped -- and since it is
  `smv_latest_version`, the site would have no top-level pages.
  `check-versions` prints the `git branch` command to fix it.
- It silently skips any ref whose `conf.py` fails to load.  Tags `v5.1.x`
  through `v5.6.x` do this with a current Sphinx (their `conf.py` refers to a
  `plot_directive` extension that no longer resolves); they are listed in
  `KNOWN_UNBUILDABLE` in `tools/check_versions.py`, and their published HTML
  is left untouched by publishing.  Any *other* version dropping out is an
  error.

`make versions-promote` (`tools/promote_latest.py`) copies the
`smv_latest_version` directory to the top level, including dotfiles such as
`.nojekyll` that GitHub Pages needs, and rewrites the sidebar links there so
that e.g. `dev` points at `www.clawpack.org/dev/`.

.. _howto_doc_publish:

Publishing to www.clawpack.org
------------------------------

The html files live in the repository
`clawpack/clawpack.github.com
<https://github.com/clawpack/clawpack.github.com>`_, served by GitHub Pages
at `www.clawpack.org <http://www.clawpack.org>`_.  The file
`extra_files/CNAME`, together with the DNS settings for the domain, makes
`clawpack.org`, `www.clawpack.com` and `clawpack.github.io` all resolve
there.

.. _howto_doc_publish_ci:

Publishing with GitHub Actions (preferred)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`.github/workflows/docs-publish.yml` does the build and the push.

**A change on dev:** merge the PR.  `www.clawpack.org/dev/` is republished
automatically within a few minutes.  Nothing else to do.

**The top-level pages or a release version** (e.g. after a release, or
after merging a fix into the release branch):

#. Make sure the change is on `dev` (and, for the top level, merged into
   the current release branch -- see :ref:`howto_doc_branches`).
#. On GitHub go to **Actions -> docs-publish -> Run workflow**, choose the
   `dev` branch (deployments are only allowed from `dev`), and set:

   `scope`
       `dry-run` builds and uploads the site as an artifact without writing
       anything; `dev-only` publishes just `dev/`; `full-site` publishes every
       version and the promoted top level.

   `target_branch`
       `ci-preview` is a branch of `clawpack.github.com` that GitHub Pages
       does not serve, so you can inspect a real diff without affecting the
       live site.  Use `master` only when you mean to publish.

   `prune`
       Off by default.  When on, stale files *inside* rebuilt version
       directories are deleted.  Nothing outside them is ever removed.

#. Wait for the `stage` job.  Its run summary shows the diff of the commit
   that would be pushed, the previous site revision, any page that loses API
   entries, and how to roll back.  Read it.
#. Approve the `push` job (environment `docs-site`, which requires a
   reviewer).  It pushes exactly the commit `stage` showed.  If
   `clawpack.github.com` changed in between, `push` refuses and the workflow
   has to be re-run.

Dev-only publishes use the `docs-dev` environment, which has no reviewers:
they are additive inside `dev/` and checked automatically.  Both
environments hold the `CLAWPACK_SITE_DEPLOY_KEY` secret (the private half of
a write deploy key on `clawpack.github.com`).

The gallery is *not* published by CI; see :ref:`howto_doc_gallery`.

Publishing by hand
^^^^^^^^^^^^^^^^^^

This is the fallback if Actions is unavailable.

#. Build the site as in :ref:`howto_doc_versions`, and commit and push any
   changed sources to `clawpack/doc`.
#. Bring your clone of the site up to date::

       cd $CLAW/clawpack.github.com
       git checkout master
       git pull origin

#. Copy the build in (`DRYRUN=1` shows what would be copied), and run the
   same guard CI uses::

       cd $CLAW/doc
       ./rsync_doc.sh
       ./doc/tools/check_published_tree.sh ../clawpack.github.com doc/_build/html

   `rsync_doc.sh` refuses to run without a promoted build, and never deletes:
   the published site has many directories no current build produces
   (`gallery/`, `doxygen/`, `pdf/`, `notebooks/`, the `v5.1.x`--`v5.6.x`
   trees, and more).

#. Commit and push::

       cd $CLAW/clawpack.github.com
       git add .
       git commit -m "changes from doc commit <hash>"
       git push origin

It may take a few minutes for the pages to update.

.. _howto_doc_branches:

Git branches and tags
---------------------

There are two active **branches** at any time: one for the current release
series, e.g. `v5.14.x`, and `dev` for documentation of features not yet
released.  Older series are **tags** (`v5.7.x`, ..., `v5.13.x`), one per
series: changes within a series (5.14.0 to 5.14.1) are assumed small enough
not to need separate documentation.  (Before v5.7.0 each patch release was
tagged, e.g. `v5.6.1`.)

As documents are improved, update `dev` and merge into the current release
branch as appropriate; `dev` should contain everything in the release branch
plus documentation of unreleased features.

`conf.py` holds the version number (`version`/`release`), which differs
between the two branches and is easy to clobber in a merge.  Merge with::

    git checkout v5.14.x
    git merge dev --no-ff --no-commit

and check `conf.py` before committing.  If it was changed and that is the
only change to it::

    git restore --staged --worktree conf.py
    git commit -m "merge recent dev changes into v5.14.x"

.. _howto_doc_major:

Starting a new 5.x series
^^^^^^^^^^^^^^^^^^^^^^^^^

For a patch release (e.g. 5.14.0 to 5.14.1) keep using the `v5.14.x` branch;
just make sure it and `dev` are up to date with each other, and update the
`v5.14.x` row of `tools/clawpack-release-refs.txt`.

For a new series (e.g. 5.14.x to 5.15.x):

#. Create the new branch and retire the old one to a tag::

       git checkout v5.14.x       # up to date with dev
       git checkout -b v5.15.x
       git tag v5.14.x v5.14.x    # tag the old branch tip...
       git branch -D v5.14.x      # ...then remove the branch
       git push upstream v5.15.x
       git push upstream v5.14.x:refs/tags/v5.14.x
       git push upstream :refs/heads/v5.14.x

   (A branch and a tag with the same name confuse `git`; the explicit
   `refs/...` above avoid ambiguity.)

#. On `v5.15.x`, set `version`/`release` in `conf.py`.

#. On `dev`, in `conf.py`, set `smv_branch_whitelist` to
   `r'^(dev|v5\.15\.x)$'` and `smv_latest_version` to `'v5.15.x'`.

#. On `dev`, replace `v5.14.x` with `v5.15.x` in the `branches:` lists of
   `.github/workflows/docs.yml` and `.github/workflows/docs-publish.yml`,
   so PRs to the new release branch are checked.

#. Add the `v5.15.x` row to `tools/clawpack-release-refs.txt`.

#. Run `make check-versions`; it should list `v5.15.x` and `v5.14.x` (now
   a tag) among the versions built.

.. _howto_doc_gallery:

Updating the gallery
--------------------

The gallery lives in `$CLAW/doc/gallery`, a separate Sphinx project, and is
**not** built or published by CI: its pages and thumbnails come from running
the examples, which is too heavy for CI.  Past versions are not tracked.

#. Run all the examples that produce results shown in the galleries, as
   described in `$CLAW/doc/gallery/README.md
   <https://github.com/clawpack/doc/blob/dev/gallery/README.md>`_.
#. Build::

       cd $CLAW/doc/gallery
       make html

#. If any notebooks were updated, also update the html versions in
   `gallery/_static/notebooks` that `gallery/notebooks.rst` points to.
   *(We should automate this.)*
#. Publish by hand::

       cd $CLAW/doc
       ./rsync_gallery.sh

   then commit and push in `$CLAW/clawpack.github.com` as in the last step
   of publishing by hand above.

Configuration and style files
-----------------------------

The general look of the documentation is controlled by:

 - `conf.py`: the version number, `html_theme`, paths to extensions and the
   `sphinx-multiversion` settings.
 - `_themes/flask_local/layout.html`: the menus at the top.
 - `_static/clawlogo.jpg`: the Clawpack logo on each page.
 - `_static/clawicon.ico`: the icon on browser tabs.
 - `_templates/index.html`: the main landing page.

The main docs and the gallery link to each other with hard links to
`www.clawpack.org` (they no longer use `intersphinx`; the `SPHINX_WEB`
environment variable is obsolete).

.. _extra_files:

Extra files for webpages not built by Sphinx
---------------------------------------------

Any files placed in `$CLAW/doc/doc/extra_files` are copied verbatim
(recursively) into the built html, and so end up on the website.

For example, `$CLAW/doc/doc/extra_files/clawdev2013/index.html` appears at
`<http://www.clawpack.org/clawdev2013/index.html>`_.

The files in `$CLAW/doc/doc/extra_files/links` provide redirects so that
links like `<http://www.clawpack.org/links/an11>`_ resolve to webpages on the
University of Washington server.  Links of this nature have been given in
published papers and some point to large amounts of data that have not been
copied to GitHub.

Pages from other clawpack repositories
--------------------------------------

Some webpages are created within other clawpack repositories.
For example, http://www.clawpack.org/geoclawdev-2020/
is modified by pushing changes to the master branch of
`geoclawdev-2020 <https://github.com/clawpack/geoclawdev-2020>`__,
configured under `Settings -> Pages` in that repository.  Others include:

- `geoclawdev-2018 <https://github.com/clawpack/geoclawdev-2018>`__
- `clawdev-2016 <https://github.com/clawpack/clawdev-2016>`__

Possible future enhancements
----------------------------

- Extend the warning check to the `gallery` Sphinx project, which first
  requires running the examples that generate its figures.
- Turn off `keep_warnings` in `gallery/conf.py` and `doc/pyclaw/conf.py`
  (used only for standalone pyclaw builds) for consistency.
- Once the warning baseline is empty, switch CI to
  `make checkwarnings-strict` and optionally enable nitpicky (`-n`)
  cross-reference checking.
- Migrate off `sphinx-multiversion`, which is unmaintained and pins the
  toolchain to `sphinx < 9` (it calls `Config.read()` positionally, and
  Sphinx 9.0 made those arguments keyword-only).  This bound lives in
  `tools/requirements-docs.txt`.
- Restore `v5.1.x`--`v5.6.x` to the multiversion build, or formally retire
  them.  Only their long-published HTML remains on the site.
