
.. _howto_release:

Guide for doing a Clawpack release
===================================

This is the procedure used to do a new official release of Clawpack.

Preparation
-----------

Make sure all your subrepositories are up to date and clean::

    cd $CLAW
    git co master
    git pull
    source pull_all.sh  # to make sure all subrepos are up to date

    python $CLAW/clawutil/src/python/claw_git_status.py

Check the output of this last commands in the files `claw_git_status.txt`
and `claw_git_diffs.txt` to make sure you don't have any uncommitted changes.
    
Run all the examples as described in `CLAW/doc/gallery/README.md
<https://github.com/clawpack/doc/blob/master/gallery/README.md>`_
as required for building the galleries, and check all the resulting plots to
make sure everything looks correct.

Version numbers
---------------

Change the version number in `clawpack/clawpack/__init__.py`.
Initially set it to e.g. v5.4.1rc-alpha, then to the final release number.

The version number is also set in `clawpack/setup.py` and should be changed
there to be consistent with `clawpack/clawpack/__init__.py`

Release candidates
------------------

Make sure all repositories are checked out to the master branch and are up to
date with the main Clawpack repositories and clean, as described in the
preparation step above.


After following the preparation instructions above, do the following::

    cd $CLAW
    git checkout -b v5.4.1rc-alpha    # change to appropriate name for this rc
    git add -u .
    git commit -m "v5.4.1rc-alpha release candidate"
    git push <your fork>

Then do a PR on https://github.com/clawpack/clawpack.

Create a tar file and a Github release
--------------------------------------

We generally do this step for a release candidate first, and then
do the same for the final release.  For release candidates, modify the
version number to include `5.4.1rc-alpha`, for example.

**NOTE:** Once one or more release candidates have been tested, the final
such PR  should contain a change of the version number in the file
`$CLAW/setup.py` and in `$CLAW/clawpack/__init__.py` to the full version,
e.g. `5.4.1`.

Once the PR has been merged::

    cd $CLAW
    git co master
    git pull
    source pull_all.sh  # to make sure all subrepos are up to date
    
Create tar file (first install https://github.com/Kentzo/git-archive-all)::

    cd $CLAW
    git-archive-all --prefix clawpack-v5.x.x/ clawpack-v5.x.x.tar
    gzip clawpack-v5.x.x.tar

(Note: best to use v5.x.x rather than just 5.x.x to be consistent with the
directory name created if following :ref:`installing_pip`.)

Draft a new release on the webpage
https://github.com/clawpack/clawpack/releases.
Indicate that it is pre-release if desired.

As a comment, add text such as::
    
    Download the clawpack-v5.x.x.tar.gz file below, not the other tar
    file of zip file. Those only include the top-level Clawpack directories and
    not all the submodules. 

Then attach the tar file `clawpack-v5.x.x.tar.gz` to be
included in the release by using the link "Attach binaries..." before
finalizing the release.  (You can go back and "Edit release" if necessary.)



Final release
--------------

After the release has been finalized, **tag all repositories**.  In the commands
below, it is assumed the remote `upstream` points to the main Github repos
(not your fork) and that you have push permission.  Change `5.x.x` to the
appropriate version number in these commands::

    cd $CLAW
    git checkout master; git pull # make sure up to date!
    git tag v5.x.x
    git push upstream v5.x.x

    cd ../pyclaw
    git checkout master; git pull # make sure up to date!
    git tag v5.x.x
    git push upstream v5.x.x

Do the same in all other repos (classic, amrclaw, geoclaw, clawutil, visclaw,
riemann).

Note these tags are used in the documentation for pages like
:ref:`changes_to_master` which generate diffs between the latest version and
the current master branch of each repository.


Pypi
----
To release on the pypi server (for installation via pip) we have to do a bit
of trickery.  We can't just follow the directions at https://packaging.python.org/tutorials/packaging-projects/
because we have a very non-Pythonic directory structure; in particular,
the subdirectories `clawpack/x/` do not have an `__init__.py`.

Here's what to do::

	cd $CLAW
	git-archive-all --prefix clawpack-x.x.x/ clawpack-x.x.x.tar

Then unpack the resulting tarball in another location.  Next::
	
        cd $CLAW
	python setup.py sdist
        cd dist

Now extract that resulting tarball.  Then copy the file PKG-INFO from this second tarball 
to the first one.  Finally, repack the first tarball and put it in `$CLAW/dist`::
	
	tar  -cvf clawpack-x.x.x.tar clawpack-x.x.x
	gzip clawpack-x.x.x.tar
        mv clawpack-x.x.x.tar $CLAW/dist

Upload to the testpypi server for testing (you will need to have created an account there)::
	
	cd ..
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

Test it::

	pip3 uninstall clawpack
	pip3 install —no-cache—dir —index-url https://test.pypi.org/simple/ clawpack
	
Once that works, do the real upload to pypi::

	twine upload dist/*


Zenodo 
------

Go to the `the Zenodo page <https://zenodo.org/>`_ 
and create a new upload for the latest tar file, following the framework of 
https://doi.org/10.5281/zenodo.820730, for example.  This will issue a new
DOI, which should be added to the page `$CLAW/doc/doc/releases.rst`.

Note that the Github repository is not linked to Zenodo for automatic uploading
on release since that would only archive a zip file of the main `clawpack`
repository.  Instead we want to archive the tar file containing all
subrepositories too.

Open Science Framework (OSF)
----------------------------

Go to https://osf.io/kmw6h/files/ and upload the latest tarfile to the set
of versions that can be accessed with the single DOI 
`10.17605/osf.io/kmw6h <https://doi.org/10.17605/osf.io/kmw6h>`__.

.. _howto_release_doc:

Updating the documentation
--------------------------

See :ref:`howto_doc` for general instructions on building the documentation
and galleries using Sphinx, and for how to push changes to Github so they
show up on the web.

Note that in the `clawpack/doc` repository there is no `master` branch.
There should be one corresponding to the latest release and
also a branch `dev` that has changes since the last release. For a new
release create a new branch from the `dev` branch with the version number,
and update `conf.py` for the new version.

When making changes for a new release, the following pages in the directory
`$CLAW/doc/doc` need to be updated:

 - A page like :ref:`release_5_4_0` needs to be created.  Copy
   `changes_to_master.rst` to `release_5_x_x.rst` for a new release `5.x.x`
   and then change `master` to `5_x_x` in each link to Github, so they have
   the form `v5.4.0...v5.4.1`, for example when going from 5.4.0 to 5.4.1.

 - Add to this page a brief summary of the major changes from the last
   release, using the diffs that show up in `changes_to_master.rst` as a guide.

 - Add and commit this new page, and also add a link to it to the file
   `releases.rst` (to show up in :ref:`releases`).

 - Modify the page `changes_to_master.rst` by replacing the previous version
   number (e.g. `5.y.y`) by the version number of the new release
   (e.g. `5.x.x`) so that links are comparing e.g. `v5.x.x...master`

 - Update `releases.rst` to include a link to the new version on Zenodo.
   Also update the bibtex and recommended citation in `about.rst`.

 - Modify several other files to point to the new version number, in particular
   `installing.rst` , `installing_pip.rst`, `installing_fortcodes.rst`,
   `contents.rst`, `docker_image.rst`.

 - Modify the main landing page `_templates/index.html` to cite the
   proper version number and DOI.
     
 - Update `conf.py` to the new version number, and also
   `$CLAW/doc/gallery/conf.py`  (For a major release.)

Updating the apps repository
----------------------------

Ideally all the apps in the :ref:`apps` should be rerun with the new release
and any issues fixed.  If old apps are modified, add a note to the
`README.rst` file in the directory that indicates when it was last updated
and to what release.  Some apps already have a section at the end of this
file of the form::

    Version history:
    ----------------

    - Updated for Clawpack 5.3.0 on 15 Sept 2015

    - Updated for Clawpack 5.4.0 on 4 Jan 2017



Updating the Dockerfile
-----------------------

See :ref:`docker_image` for instructions on using the docker image.

Note that unlike the tar file for a new release, the docker image includes
a clone of the `apps` repository, so it would be best to first update that
repository if necessary.

 - Clone the repository https://github.com/clawpack/docker-files 

 - Make a new `Dockerfile` for the new version by copying an old one
   and changing the version numbers in it.  Make any other changes needed
   for this new release.

 - See the `README.md` file in that repo for instructions on building an
   image and pushing it to dockerhub (which requires push permission).


