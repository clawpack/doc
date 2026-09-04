
.. _howto_doc:

Guide for updating this documentation
=============================================

See also the README.md at https://github.com/clawpack/doc.

The `clawpack/doc <https://github.com/clawpack/doc>`_ repository is not
included in the Clawpack distribution and must be cloned separately if you
want to work with these files.

After cloning into the `$CLAW` directory, the restructured text
files for the main documentation are in `$CLAW/doc/doc`.  All files
related to the gallery are in `$CLAW/doc/gallery`.  As of Version
5.4.1, these two subdirectories are separate Sphinx projects 

They used to be connected using 
`intersphinx <http://www.sphinx-doc.org/en/stable/ext/intersphinx.html>`_.  
but this was dropped in v5.7.x.

Git branches and tags
---------------------

Older versions of the documentation used to be tagged for each minor
release, e.g. `v5.6.1`.  Starting with v5.7.0, these are now only tagged
with the major release, e.g. `v5.7.x`.  

The side menu on the Sphinx pages now lists only these major tags. The
assumption is that any changes within e.g. the 5.7 version are minor enough
that the documentation should not change substantially.

There are two active **branches** at any time, one for the current major
release, e.g. `v5.7.x`, and one named `dev` for the development of documenation
for features not yet released.  When a new major release is done the
`v5.7.x` branch will be retired, creating a `v5.7.x` tag instead along with
a new `v5.8.x` branch.

As documents are improved, continue to update the current release branch,
e.g. `v5.7.x`, and also merge these changes in to the `dev` branch.  In
general `dev` should be up to date with the current release branch along
with perhaps some new documentation for features not in the current
release.

Note that the file `conf.py` contains the version number.  Please insure
that the `dev` branch and current release branch each have the correct
thing. This can easily get messed up when merging from one branch to the
other.  One way to help avoid this is to always merge via, e.g.::

    git checkout dev
    git merge v5.7.x --no-ff --no-commit 

and then check before doing the merge commit to make sure `conf.py` hasn't
been improperly changed.  If it has, and that's the only change to this
file, you can do::

    git reset HEAD conf.py
    git checkout conf.py

and check that it's correct before committing via e.g.::

    git commit -m "merged recent v5.7.x changes into dev"
    

Configuration and style files
-----------------------------

The general look of the documentation and various things that appear on each
page are controlled by the following files:

 - `conf.py` includes the version number, sets the `html_theme`, as well as
   setting paths to extensions and various other sphinx settings.
 - `_themes/flask_local/layout.html` determines the menus at the top
 - `_static/clawlogo.jpg` is the Clawpack logo put on each page
 - `_static/clawicon.ico` is the icon that appears on browser tabs
 - `_templates/index.html` contains the main landing page
 
.. _howto_doc_release:

Updating the docs for a new release
-----------------------------------

When updating the documentation for a new release, see also
:ref:`howto_release_doc` for a list of necessary changes.


Before proceeding, first make sure other repositories are checked out to
master, since some pages now have literalinclude's that bring in code 
(e.g. setaux_defaults.rst, etc).
**Note: This is no longer true.**

To create html files from the dev branch only, for example::

    cd $CLAW/doc/doc
    git checkout dev
    make html

The `Makefile` has been modified so that `make html` does this::

    sphinx-build -b html . _build1/html

To view the files, point your browser to `$CLAW/doc/doc/_build1/html/index.html`

Note that we suggest using `_build1` when building a single version so this
can be quickly rebuilt when writing and editing documentation.


.. _howto_doc_warnings:

Checking for documentation warnings
-----------------------------------

Sphinx does not fail the build on reStructuredText or docstring problems
(a missing blank line before a list, a bad cross reference, an autodoc import
issue, and so on).  Historically these warnings were also *embedded* into the
rendered HTML as "System Message" boxes (via `keep_warnings = True` in
`conf.py`) while not being obvious on the command line, so they could slip
onto the website unnoticed.  `keep_warnings` is now `False`, and the
following `make` targets let you catch warnings before they are merged.

To fail on any warning that is **new** relative to a committed baseline
(`tools/doc_warnings_baseline.txt`)::

    cd $CLAW/doc/doc
    make checkwarnings

This does a full re-parse using the lightweight `dummy` builder (no HTML is
written) and compares the result against the baseline, which records the
warnings that already existed when the check was introduced.  Only newly
introduced warnings cause a non-zero exit, so you can fix the backlog
gradually without the check going red on unrelated pages.

If you intentionally add or remove warnings (e.g. after fixing a batch of
them), regenerate and commit the baseline::

    make checkwarnings-update

To ignore the baseline entirely and report **every** remaining warning --
the goal once the backlog has been driven to zero -- use::

    make checkwarnings-strict

The same check runs in CI (`.github/workflows/docs.yml`) on pull requests to
`dev` and the current release branch.  Because `autodoc` imports the clawpack
packages, CI installs them with `pip`; the optional parallel package
`petclaw` (and `petsc4py`) is not installed but is instead listed in
`autodoc_mock_imports` in `conf.py`.

.. note::

   The exact set of warnings depends on which packages are importable, so the
   baseline is environment dependent.  Regenerate it in the same environment
   the CI workflow uses (see `tools/requirements-docs.txt`); the workflow can
   be run manually to produce an updated baseline as an artifact.

**Possible future enhancements:**

- Extend the same warning check to the separate `gallery` Sphinx project
  (`$CLAW/doc/gallery`), which first requires running the examples that
  generate its figures.
- Turn off `keep_warnings` in `gallery/conf.py` and `doc/pyclaw/conf.py`
  (used only for standalone pyclaw builds) for consistency.
- Once the baseline is empty, switch CI to `make checkwarnings-strict` and
  optionally enable nitpicky (`-n`) cross-reference checking.
- Migrate off `sphinx-multiversion`, which is unmaintained and pins the
  toolchain to `sphinx < 9` (it calls `Config.read()` positionally, and Sphinx
  9.0 made those arguments keyword-only).  This bound lives in
  `tools/requirements-docs.txt`.
- Restore `v5.1.x`--`v5.6.x` to the multiversion build, or formally retire
  them.  Their `conf.py` refers to a `plot_directive` extension that no longer
  resolves, so `sphinx-multiversion` skips them and only their long-published
  HTML remains on the site.


To generate docs including previous versions
--------------------------------------------

If you have just done a new major release, first see :ref:`howto_doc_major`
below.

The instructions below make webpages that list v5.7.x, v5.8.x, etc. and allow
viewing docs that may be more relevant to a previous version of Clawpack.

This should be done when you are close to pushing changes to the website,
otherwise the above approach works fine and shows the current state of the
documentation based on files in your working directory.

This can take longer since it rebuilds pages for all versions.

As of v5.7.x, we are now using 
`sphinx-multiversion <https://holzhaus.github.io/sphinx-multiversion/master/index.html>`__
instead of 
`sphinxcontrib-versioning <https://github.com/sphinx-contrib/sphinxcontrib-versioning>`__.


To make pages that show previous Clawpack versions, first install
`sphinx-multiversion <https://holzhaus.github.io/sphinx-multiversion/master/index.html>`__.

Insure that any changes you want to show up in multiversion docs has been
committed to some branch (normally `dev` if you have been adding something new).

And then do this::

    cd $CLAW/doc/doc
    make versions-publish

That single target does the whole job: a clean multiversion build followed by
the promotion step described below.  It is equivalent to::

    make clean-versions      # rm -rf _build
    make versions            # sphinx-multiversion . _build/html
    make versions-promote    # python tools/promote_latest.py _build/html

To view the result, point your browser to `_build/html/index.html`, which is
the current release, and from there you should be able to navigate to other
versions.

Unlike `sphinxcontrib-versioning`, this uses your local branches and tags
rather than the versions on Github.  It lists two branches under "Latest
Versions" and the whitelisted tags as "Older Versions".  The branches are set
to `dev` and the most recent version, by this line of `conf.py`::

    smv_branch_whitelist = r'^(dev|v5\.14\.x)$'

This should be updated for a new version, along with `smv_latest_version`.

.. warning::

   `sphinx-multiversion` only considers **local** branches and tags
   (`refs/heads/*` and `refs/tags/*`); it ignores remote-tracking refs such as
   `clawpack/v5.14.x` unless `smv_remote_whitelist` is set.  If you have never
   checked out the release branch, it will be missing from your build -- and
   because it is `smv_latest_version`, the site would end up with no top-level
   pages at all.  It also silently skips any ref whose `conf.py` fails to
   load.  `make versions` therefore runs a pre-flight check first::

       make check-versions

   which reports exactly which versions will be built and prints the
   `git branch` command for anything missing.  Tags `v5.1.x` through `v5.6.x`
   are known not to build with a current Sphinx (their `conf.py` refers to a
   `plot_directive` extension that no longer resolves); they are listed in
   `KNOWN_UNBUILDABLE` in `tools/check_versions.py`, and their already
   published HTML is left untouched by the deployment step.

Why the promote step is needed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`_build/html` contains a subdirectory for each version, but immediately after
`make versions` there are no `.html` files in its top level.  For the Clawpack
webpage we need to:

- Copy the files from the current version to the top level so that
  navigating to http://www.clawpack.org/installing.html,
  for example, goes to the current version of this document.

- Fix the links in the sidebars of each of these `.html` files so that clicking
  on `dev`, for example, takes you to http://www.clawpack.org/dev/installing.html

`make versions-promote` does both, via `tools/promote_latest.py`.  This used to
be a manual `cp -r v5.7.x/* .` plus `python ../../fix_links_top_level.py`; the
script replaces that because the manual form had to be edited by hand at each
release, skipped dotfiles (notably `.nojekyll`, without which GitHub Pages
will not serve `_static`), and only fixed links one or two directories deep.

You can sanity check the result before deploying::

    cd $CLAW/doc
    ./doc/tools/check_built_site.sh doc/_build/html

If you like what you see, you can push back to your fork and then issue a
pull request to have these changes incorporated into the documentation.

**Note:** We are no longer using `intersphinx` to link the gallery and the 
main doc pages together.   Instead there are hard links to `www.clawpack.org`
to go from one to the other.  So the old use of 
the environment variable `SPHINX_WEB` is now deprecated.

.. _howto_doc_major:

Updating for a new major version
--------------------------------

When updating a minor version, e.g. from v5.7.0 to v5.7.1, we will continue
to use the same branch v5.7.x.  You should just make sure the v5.7.x and dev
are up to date with each other at the time of release.

When updating to the next major version, e.g. from v5.7.x to v5.8.x, it is
necessary to do the following:

- Create a new branch v5.8.x from v5.7.x (or dev).

- Delete branch v5.7.x and replace it with a tag, so that the proper
  versions get included in the documentation when next it is built.

For example, this could be done as follows::

    git checkout v5.7.x       # assuming up to date with dev
    git checkout -b v5.8.x    # create new branch
    git branch -d v5.7.x      # remove old branch
    git push origin :v5.7.x   # delete branch on github
    git tag v5.7.x            # create new tag
    git push origin v5.8.x    # push new branch
    git push origin --tags    # push new tag



Updating the gallery
--------------------

The gallery webpages are now decoupled from the main sphinx pages, and reside
in `$CLAW/doc/gallery` rather than `$CLAW/doc/doc`.  

To remake the galleries, you need to first run all the examples that produce
results shown in the galleries.  

For detailed instructions, see `CLAW/doc/gallery/README.md
<https://github.com/clawpack/doc/blob/dev/gallery/README.md>`_.

Then do the following::

    cd $CLAW/doc/gallery
    make html

Note that we don't track past versions in the gallery.


Note that `doc/gallery/notebooks.rst` contains pointers to html versions of many
notebooks, stored in `doc/gallery/_static/notebooks`.  If any notebooks were
updated for this release, the corresponding html files should be too.
*(We should automate this).*

Updating the webpages
---------------------

The html files live in the repository
`clawpack/clawpack.github.com
<https://github.com/clawpack/clawpack.github.com>`_
which causes them to show up on the web at
`http://clawpack.github.io
<http://clawpack.github.io>`_.

.. _howto_doc_publish_ci:

Publishing with GitHub Actions (preferred)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`.github/workflows/docs-publish.yml` does the build and the push for you.
Pushing documentation changes to `dev` refreshes `www.clawpack.org/dev/`
automatically; a full-site publish (all versions plus the top-level pages) is
run on demand from the Actions tab via **Run workflow**, choosing:

`scope`
    `dry-run` builds and uploads the site as an artifact without writing
    anything; `dev-only` publishes just `dev/`; `full-site` publishes every
    version and the promoted top level.

`target_branch`
    `ci-preview` is a branch of `clawpack.github.com` that GitHub Pages does
    not serve, so you can inspect a real diff without affecting the live site.
    Use `master` only when you mean to publish.

`prune`
    Off by default.  When on, stale files *inside* rebuilt version directories
    are deleted.  Nothing outside them is ever removed.

The publish step waits for a reviewer to approve the `clawpack-org-website`
environment, and the run summary shows the diff and the previous site
revision, so you can see exactly what will change before approving and how to
roll back afterwards.

The gallery is *not* published by CI -- its pages and thumbnails have to be
generated by running the examples (see `gallery/README.md`), so it stays a
manual `rsync` as described below.

Publishing by hand
^^^^^^^^^^^^^^^^^^^

This still works and is the fallback if Actions is unavailable.  First create
the html files as described above, which should appear in
`doc/doc/_build/html` and `doc/gallery/_build/html`.

Commit any changed source files and
push to `clawpack/doc <https://github.com/clawpack/doc>`_.

Then do::

    cd $CLAW/clawpack.github.com
    git checkout master
    git pull origin  # make sure you are up to date before doing next steps!

    cd $CLAW/doc
    ./rsync_doc.sh

If you have updated the gallery, also do::

    ./rsync_gallery.sh

Both scripts refuse to run if there is no promoted build to copy, and neither
passes `--delete`: the published site contains many directories that no
current build produces (`gallery/`, `doxygen/`, `pdf/`, `notebooks/`, the
`v5.1.x`--`v5.6.x` trees, and more), and deleting them would take down large
parts of the website.  Set `DRYRUN=1` to see what would be copied.

Before committing, you can run the same guard CI uses::

    cd $CLAW/doc
    ./doc/tools/check_published_tree.sh ../clawpack.github.com doc/_build/html


Then move to the `clawpack.github.com` repository and 
add and commit any new or changed files. 
All files are needed, so ::

    cd $CLAW/clawpack.github.com
    git add . 

should work.  For the commit message you might want to add the commit
hash of the most recent commit in $CLAW/doc/doc::

    cd $CLAW/clawpack.github.com
    git add . 
    git commit -m "changes from doc/doc commit <hash>"

And finally push to the web::

    git push origin

which assumes that `origin` is
`git@github.com:clawpack/clawpack.github.com.git`.

It may take a few minutes for the updated webpages to appear at 
`<http://clawpack.github.io/>`_.

Note that `<http://clawpack.org>`_ and `<http://www.clawpack.com>`_
should also resolve properly to `<http://clawpack.github.io/>`_.
and that `www.clawpack.org` should appear in the browser address bar.  The
file `extra_files/CNAME` combined with settings on the domain server
`godaddy.com` determine this behavior.

.. _extra_files:

Extra files for webpages not built by Sphinx
---------------------------------------------

Any files placed in `$CLAW/doc/doc/extra_files` will be copied verbatim
(recursively for subdirectories) to the directory
`$CLAW/doc/doc/_build/html` when Sphinx is used to build the documentation.
These will be copied to `$CLAW/clawpack.github.com/` when the 
`rsync_clawpack.github.sh` script is run and hence will appear on the
webpages.   

For example, the file `$CLAW/doc/doc/extra_files/clawdev2013/index.html`
should appear at `<http://www.clawpack.org/clawdev2013/index.html>`_.

The files in `$CLAW/doc/doc/extra_files/links` provide redirects so that
links like `<http://www.clawpack.org/links/an11>`_ resolve properly to
webpages on the University of Washington server.  Links of this nature have
been provided in published paper and some contain large amounts of data that
have not been copied to Github.

Pages from other clawpack repositories
--------------------------------------

Some webpages are created within other clawpack repositories. 
For example, the page http://www.clawpack.org/geoclawdev-2020/
is modified by pushing changes to the master branch of the repository
`geoclawdev-2020 <https://github.com/clawpack/geoclawdev-2020>`__.
This is configured in that repository, in the `GitHub Pages` section found 
under `Settings`.

Other repositories that create webpages include:

- `geoclawdev-2018 <https://github.com/clawpack/geoclawdev-2018>`__
- `clawdev-2016 <https://github.com/clawpack/clawdev-2016>`__
    
