
.. _howto_release:

Guide for doing a Clawpack release
===================================

This is the procedure for an official release of Clawpack, e.g. `v5.15.0`.
For building and publishing the documentation itself, see :ref:`howto_doc`.

Both guides live in the `clawpack/doc` repository as `doc/howto_release.rst`
and `doc/howto_doc.rst`, and are linked from the repository's `README.md`
and from :ref:`developers`.

In the commands below, `5.x.x` is the new version, `5.y.y` the previous one,
and `5.x` the series (the doc branch for the 5.15 series is `v5.15.x`).
The `upstream` remote is assumed to point at `github.com/clawpack/<repo>`
(not your fork) and you need push permission there.

.. _howto_release_automation:

What is automated and what is not
---------------------------------

Almost all of a release is done by hand.  The automation is limited to
checking and publishing:

=====================================================  =====================================
Step                                                   How it happens
=====================================================  =====================================
Version numbers, release candidate PR, tags            **Manual**
Tar file and GitHub release                            **Manual**
PyPI upload                                            **Manual** (`python -m build`, `twine`)
Zenodo and OSF archives                                **Manual**
Release notes page, doc version bumps                  **Manual** (edit `.rst` files)
New doc branch, retire old one to a tag                **Manual** (git)
Check that an install imports everything it ships      Automatic: `clawpack/clawpack` CI
                                                       (`installed-imports.yml`) on every PR
                                                       and nightly
Check the doc version set and release source trees     Automatic: `make check-versions`, run
                                                       before every multiversion build
Build docs for a PR                                    Automatic: `docs.yml` (warnings) and
                                                       `docs-publish.yml` (preview artifact)
Publish `www.clawpack.org/dev/`                        Automatic on every merge to `dev`
Publish the top-level site and all release versions    **Manual trigger**: Actions tab, then
                                                       approve (see :ref:`howto_doc_publish_ci`)
Gallery                                                **Manual**: run examples, build, rsync
Apps repository, Docker image                          **Manual**
=====================================================  =====================================

.. _howto_release_checklist:

Release checklist
-----------------

Do these in order.  Each step links to its details below.

#. :ref:`Prepare <howto_release_prepare>`: all repos on `master`, up to date
   and clean; run the gallery examples and look at the plots.
#. :ref:`Bump the version number <howto_release_version>` in
   `clawpack/clawpack` (three files).
#. :ref:`Release candidate <howto_release_rc>`: PR to `clawpack/clawpack`,
   optionally a pre-release tar file on GitHub.  Repeat until happy.
#. :ref:`Final PR and tar file <howto_release_tarfile>`: set the full version,
   merge, build the tar file, draft the GitHub release.
#. :ref:`Tag every repository <howto_release_tag>` with `v5.x.x`.
#. :ref:`Upload to PyPI <howto_release_pypi>` (test PyPI first).
#. :ref:`Archive on Zenodo and OSF <howto_release_archive>`; note the new DOI.
#. :ref:`Update the documentation <howto_release_doc>`: release notes page,
   version numbers, DOI, release-refs row, and for a new 5.x series the new
   doc branch.  Then publish the full site.
#. :ref:`Rebuild the gallery <howto_release_gallery>` and publish it.
#. :ref:`Update the apps repository <howto_release_apps>`.
#. :ref:`Update the Docker image <howto_release_docker>`.

.. _howto_release_prepare:

Preparation
-----------

Make sure all your subrepositories are up to date and clean::

    cd $CLAW
    git checkout master
    git pull
    source pull_all.sh  # to make sure all subrepos are up to date

    python $CLAW/clawutil/src/python/claw_git_status.py

Check the output of the last command in the files `claw_git_status.txt`
and `claw_git_diffs.txt` to make sure you don't have any uncommitted changes.

Run all the examples as described in `$CLAW/doc/gallery/README.md
<https://github.com/clawpack/doc/blob/dev/gallery/README.md>`_
as required for building the galleries, and check all the resulting plots to
make sure everything looks correct.

.. _howto_release_version:

Version numbers
---------------

Change the version number in these three files in `clawpack/clawpack`:

 - `clawpack/__init__.py` (`__version__`; the meson build reads the version
   from here via `metadata.py`)
 - `pyproject.toml` (`version`)
 - `setup.py` (`MAJOR`, `MINOR`, `MICRO`)

For a release candidate, use e.g. `5.x.xrc-alpha`; the final PR sets the
full version.

.. _howto_release_rc:

Release candidates
------------------

After the preparation and version steps above::

    cd $CLAW
    git checkout -b v5.x.xrc-alpha    # change to appropriate name for this rc
    git add -u .
    git commit -m "v5.x.xrc-alpha release candidate"
    git push <your fork>

Then open a PR on https://github.com/clawpack/clawpack.  Its
`installed-imports` check builds and installs the tree as the PR records it and
imports everything it ships; it must pass.

You can also build a tar file and draft a GitHub *pre-release* for the
candidate, as in the next step, so others can test it.

.. _howto_release_tarfile:

Final PR, tar file and GitHub release
-------------------------------------

Once one or more release candidates have been tested, the final PR sets the
full version number (e.g. `5.x.x`) in the three files above.

Once the PR has been merged::

    cd $CLAW
    git checkout master
    git pull
    source pull_all.sh  # to make sure all subrepos are up to date

Create the tar file (first install https://github.com/Kentzo/git-archive-all)::

    cd $CLAW
    git-archive-all --prefix clawpack-v5.x.x/ clawpack-v5.x.x.tar
    gzip clawpack-v5.x.x.tar

(Use `v5.x.x` rather than just `5.x.x` to be consistent with the directory
name created if following :ref:`installing_pip`.)

Draft a new release at https://github.com/clawpack/clawpack/releases,
marked as a pre-release if appropriate.  As the description, add text such
as::

    Download the clawpack-v5.x.x.tar.gz file below, not the other tar
    file or zip file. Those only include the top-level Clawpack directories
    and not all the submodules.

Attach `clawpack-v5.x.x.tar.gz` to the release before publishing it.  (You
can go back and "Edit release" if necessary.)

.. _howto_release_tag:

Tag all repositories
--------------------

After the release has been published on GitHub, tag every repository::

    cd $CLAW
    git checkout master; git pull   # make sure up to date!
    git tag v5.x.x
    git push upstream v5.x.x

    for repo in pyclaw classic amrclaw geoclaw clawutil visclaw riemann; do
        (cd $CLAW/$repo && git checkout master && git pull &&
         git tag v5.x.x && git push upstream v5.x.x)
    done

These tags are used by :ref:`changes_to_master` and the release notes pages,
which link to GitHub diffs between versions.  The `clawpack/clawpack` tag's
commit is also what goes into `tools/clawpack-release-refs.txt` in the doc
repo (see :ref:`howto_release_doc`).

.. _howto_release_pypi:

PyPI
----

Build from a clean clone::

    git clone --recurse-submodules https://github.com/clawpack/clawpack.git
    cd clawpack
    git checkout v5.x.x
    git submodule update
    pip install build twine
    python -m build

To upload you need a PyPI account and must be listed as a maintainer of
Clawpack.  Upload to the test server first::

    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

Check that the page looks right and that it installs::

    pip uninstall clawpack
    pip install --no-cache-dir --index-url https://test.pypi.org/simple/ clawpack

Then do the real upload::

    twine upload dist/*

.. _howto_release_archive:

Zenodo and OSF
--------------

**Zenodo:** go to https://zenodo.org/ and create a new upload of the tar
file, following the framework of https://doi.org/10.5281/zenodo.820730, for
example.  This issues a new DOI, which goes into `releases.rst` and
`about.rst` (see :ref:`howto_release_doc`).

The GitHub repository is deliberately *not* linked to Zenodo: that would only
archive a zip of the top-level `clawpack` repository, not the tar file with
all the subrepositories.

**OSF:** upload the tar file to https://osf.io/kmw6h/files/, which keeps all
versions under the single DOI
`10.17605/osf.io/kmw6h <https://doi.org/10.17605/osf.io/kmw6h>`__.

.. _howto_release_doc:

Updating the documentation
--------------------------

All of this is in the `clawpack/doc` repository.  Details on building and
publishing are in :ref:`howto_doc`; the branch model is described in
:ref:`howto_doc_branches`.

**1. Release notes page** (on `dev`, in `doc/`):

 - Copy `changes_to_master.rst` to `release_5_x_x.rst`, change its label and
   title, and change `master` to `v5.x.x` in each GitHub link so they have the
   form `v5.y.y...v5.x.x`.
 - Add a brief summary of the major changes, using those diffs as a guide.
 - Add it to `releases.rst`, along with the new Zenodo DOI.
 - In `changes_to_master.rst`, replace `5.y.y` by `5.x.x` so that its links
   compare `v5.x.x...master`.

**2. Version numbers and citation:**

 - `about.rst`: the bibtex entry and recommended citation (new DOI).
 - `installing_pip.rst`, `installing_fortcodes.rst`, `contents.rst`,
   `docker_image.rst`: the version number.
 - `conf.py` on the release branch: `version` and `release` (e.g. `5.15` and
   `5.15.x`).  On `dev` these stay `dev`; check that a merge between the two
   branches has not swapped them (see :ref:`howto_doc_branches`).

**3. Release source tree** for the API pages: add (or, for a patch release,
update) the row for `v5.x` in `tools/clawpack-release-refs.txt`, naming the
commit of the `v5.x.x` tag in `clawpack/clawpack`::

    git -C $CLAW rev-parse v5.x.x^{commit}

`make check-versions` fails until the row is there.  See
:ref:`howto_doc_release_trees`.

**4. For a new 5.x series only** (e.g. 5.14.x to 5.15.x): follow
:ref:`howto_doc_major` to create the `v5.15.x` branch, retire `v5.14.x` to a
tag, and update `smv_branch_whitelist` and `smv_latest_version` in `conf.py`
and the branch lists in `.github/workflows/docs.yml` and
`.github/workflows/docs-publish.yml`.  For a patch release (e.g. 5.14.0 to
5.14.1) just make sure `dev` and `v5.14.x` are up to date with each other.

**5. Publish:** merge to `dev` (this republishes `dev/` automatically), then
run a `full-site` publish from the Actions tab so the top-level pages and the
release's version directory are rebuilt.  See :ref:`howto_doc_publish_ci`.

.. _howto_release_gallery:

Updating the gallery
--------------------

The gallery is not built by CI.  Run the examples, build, and rsync it as
described in :ref:`howto_doc_gallery`.

.. _howto_release_apps:

Updating the apps repository
----------------------------

Ideally all the apps in :ref:`apps` should be rerun with the new release
and any issues fixed.  If old apps are modified, add a note to the
`README.rst` file in the directory that indicates when it was last updated
and to what release.  Some apps already have a section at the end of this
file of the form::

    Version history:
    ----------------

    - Updated for Clawpack 5.3.0 on 15 Sept 2015

    - Updated for Clawpack 5.4.0 on 4 Jan 2017

.. _howto_release_docker:

Updating the Docker image
-------------------------

See :ref:`docker_image` for instructions on using the docker image.

Unlike the tar file, the docker image includes a clone of the `apps`
repository, so update that repository first if necessary.

 - Clone https://github.com/clawpack/docker-files
 - Make a new `Dockerfile` for the new version by copying an old one and
   changing the version numbers in it, plus any other changes needed.
 - See the `README.md` in that repo for building an image and pushing it to
   Docker Hub (which requires push permission).
