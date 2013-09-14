
.. _developers:

**************************************
Developers' Guide
**************************************

See :ref:`git-resources` for some useful links.

.. _developers_gitclone:

Cloning the most recent code from Github
---------------------------------------------------

You can create a read-only development version of Clawpack via::

    git clone git://github.com/clawpack/clawpack.git
    cd clawpack
    python setup.py git-dev

This downloads the following clawpack modules as subrepositories checked out at
specific commits (as opposed to the tip of a branch). 

* `<https://github.com/clawpack/pyclaw>`_  (Python code, some of which is
  needed also for Fortran version)
* `<https://github.com/clawpack/clawutil>`_ (Utility functions,
  Makefile.common used in multiple repositories)
* `<https://github.com/clawpack/classic>`_  (Classic single-grid code)
* `<https://github.com/clawpack/amrclaw>`_ (AMR version of Fortran code)
* `<https://github.com/clawpack/riemann>`_  (Riemann solvers)
* `<https://github.com/clawpack/visclaw>`_  (Python graphics and
  visualization tools)
* `<https://github.com/clawpack/geoclaw>`_  (GeoClaw)


This should give a snapshot of the repositories that work well together.
(Note that there are many inter-dependencies between code in the
repositories and checking out a different commit in one repository may break
things in a different repository.)

If you want to also install the PyClaw Python components, you can then do::

    pip install -e .

If you want to use the Fortran versions in `classic`, `amrclaw`, `geoclaw`,
etc., you need to set environment variables and proceed as described at
:ref:`setenv`.

.. _setup_dev:


Installation instructions for developers
---------------------------------------------------

Install a read-only copy of all the main repositories as described above in
:ref:`developers_gitclone`.

**Important Note:** The repositories will each be checked out to a specific commit and
will probably be in a detached-head state.  You will need to checkout
`master` in each repository to see the current head of the master branch.

You should never commit to `master`, only to a feature branch, so
the `master` branch should always reflect what's in the main 
*clawpack* repository.  You can update it to reflect any changes via::

        git checkout master
        git fetch origin
        git merge origin/master

or simply::

        git pull origin master:master

Remember that you need to do this in each repository before running anything
to make sure everything is up to date with *master*.

.. _dev_remote:

Setting a remote to point to your fork
---------------------------------------

If you plan to make changes and issue pull requests to one or more
repositories, you will need to do the following steps for each such
repository:

#. Go to `<http://github.com/clawpack>`_ and fork the repository to your own
   Github account.  (Click on the repository name and then the *Fork* button
   at the top of the screen.)

#. Add a *remote* pointing to your repository.  For example, if you have
   forked the `amrclaw` repository to account `username`, you would do::

        cd amrclaw
        git remote add username git@github.com:username/amrclaw.git

   You should push only to this remote, not to `origin`, e.g.::

        git push username



You might also want to clone some or all of the following repositories:

* `<https://github.com/clawpack/doc>`_  (documentation)
* `<https://github.com/clawpack/apps>`_  (To collect applications)
* `<https://github.com/clawpack/regression>`_  (Regression tests)
* `<https://github.com/clawpack/clawpack-4.x>`_  (Previous versions, 4.6)

These are not brought over by cloning the top `clawpack` super-repository.
You can get one of these in read-only mode by doing, e.g.::

    git clone git://github.com/clawpack/doc.git

Then go through the above steps to add a remote to your own fork of the
repository if you plan to modify and issue pull requests.

Modifying code
--------------

Before making changes, you generally want to make sure *master* is up to
date::

        git checkout master
        git pull 

Then create a new branch based on `master` for any new commits::

        git checkout -b new_feature master

        # make some changes
        # git add the modified files
        git commit -m "describe the changes"

Now make changes, add and commit them, 
and then push to your own fork::

        git push username new_feature


If you want these changes pulled into *master*, 
you can issue a pull request from the github page for your fork of this
repository (make sure to select the correct branch of your repository).

**Note:** If you accidentally commit to `master` rather than creating a
feature branch first, you can easily recover::

    git checkout -b new_feature

will create a new branch based on the current state and history (including
your commits to `master`) and you can just continue adding additional 
commits.

The only problem is your `master` branch no longer agrees with the history
on Github and you want to throw away the commits you made to `master`.  The
easiest way to do this is just to make sure you're on a different branch,
e.g., ::

    git checkout new_feature

and then::

    git branch -D master
    git checkout -b master origin/master

This deletes your local branch named `master` and recreates a branch with
the same name based on `origin/master`, which is what you want.

.. _developers_pr:

Pull requests
-------------

Before issuing a pull request, you should make sure you have not broken
anything:  

#. Make sure you are up to date with *master*::

        git checkout master
        git pull 

   If this does not say "Already up-to-date" then you might want to rebase
   your modified code onto the updated master.  With your feature branch
   checked out, you can see what newer commits have been added to *master*
   via::

        git checkout new_feature
        git log HEAD..master

   If your new feature can be added on to the updated master, you can rebase::

        git rebase master

   which gives a cleaner history than merging the branches.

#.  Run the appropriate regression tests.  If you have modified code
    in pyclaw or riemann, then you should run the pyclaw tests.  First,
    if you have modified any Fortran code, you need to recompile::

        cd clawpack/
        pip install -e .

    Then run the tests::

        cd pyclaw
        nosetests

    If any tests fail, you should fix them before issuing a pull request.

To issue a pull request (PR), go to the Github page for your fork of the
repository in question, select the branch from which you want the pull
request to originate, and then click the *Pull Request* button.

.. _test_pr:

Testing out a pull request
--------------------------

To test out someone else's pull request, follow these  instructions:
For
example, if you want to try out a pull request coming from a branch named
*bug-fix* from user *rjleveque* to the *master* branch of
the *amrclaw* repository, you would do::

    cd $CLAW/amrclaw   # (and make sure you don't have uncommitted changes)
    git checkout master
    git pull  # to make sure you are up to date

    git checkout -b rjleveque-bug-fix master
    git pull https://github.com/rjleveque/amrclaw.git bug-fix

This puts you on a new branch of your own repository named
*rjleveque-bug-fix* that has the proposed changes pulled into it.

Once you are done testing, you can get rid of this branch via::

    git checkout master
    git branch -D rjleveque-bug-fix

    

.. _toplevel_pr:

Top level pull requests
-----------------------

The top level *clawpack* repository keeps track of what versions of the
subrepositories work well together.

If you make pull requests in two different repositories that are linked, say
to both *pyclaw* and *riemann*, then you should also push these changes to
the top-level *clawpack* repository and issue a PR for this change::

    cd $CLAW   # top-level clawpack repository
    git checkout master
    git pull
    git checkout -b pyclaw-riemann-changes
    git add pyclaw riemann
    git commit -m "Cross-update pyclaw and riemann."
    git push username pyclaw-riemann-changes



Git workflow
------------

See :ref:`git-resources` for useful links.



