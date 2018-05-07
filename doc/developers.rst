.. _developers:

**************************************
Developers' Guide
**************************************

.. seealso::
    :ref:`contents-developers-resources`

.. contents::

Guidelines for contributing
==================================
When preparing contributions, please follow the guidelines in
:ref:`contribution`.  Also:

    * If the planned changes are substantial or will be backward-incompatible,
      it's best to discuss them on the `claw-dev Google group
      <http://groups.google.com/group/claw-dev>`_ before starting.
      
    * Make sure all tests pass and all the built-in examples run correctly.

    * Be verbose and detailed in your commit messages and your pull request.

    * It may be wise to have one of the maintainers look at your changes before
      they are complete
      (especially if the changes will necessitate modifications of tests
      and/or examples).

    * If your changes are not backward-compatible, your pull request should 
      include instructions for users to update their own application codes.

Reporting and fixing bugs
-------------------------
If you find a bug, post an issue with as much explanation as possible on the
appropriate issue tracker (for instance, the PyClaw issue tracker is at
https://github.com/clawpack/pyclaw/issues.  If you're looking 
for something useful to do, try tackling one of the issues listed there.

Developer communication
-----------------------
Developer communication takes place on the google group at
http://groups.google.com/group/claw-dev/, and (increasingly) within the issue
trackers on Github.


.. _setup_dev:


Installation instructions for developers
========================================

Cloning the most recent code from Github
----------------------------------------

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


Now install this version of Clawpack using::

    pip install -e .

The `-e` flag means that this is an editabl version of the Clawpack code
(rather than installing the original version in the `site-packages`
directory).

If you want to use the Fortran versions in `classic`, `amrclaw`, `geoclaw`,
etc., you need to set environment variables and proceed as described at
:ref:`setenv`.


Checking out the master branch on each repository
-------------------------------------------------

Following the instructions above gives you a top level `$CLAW` directory
that is checked out to the tip of the master branch, and each subrepository
will be checked out to a particular commit as specified by this master
branch.  For development work, You probably want to check out each
subrepository to the master branch as well.  The shell script 
`$CLAW/pull_all.sh` can be used to do this for all subrepositories (or look
at this file to see how to do it more selectively).  At a shell prompt,
type::

    source pull_all.sh

which will check out master on each repository and then do a `git pull` to
make sure it is up to date.  If you do this shortly after cloning all the
repositories, they should all have been up to date already.

Updating to the latest master branch
------------------------------------------

The script `pull_all.sh` can be used at any time to check out all
subrepositories to master and do a `git pull`.  This is handy if you want to
make sure your version of `master` is up to date in every repository.

You should first make sure that you do not have uncommitted changes in any
repository that might conflict with the `git checkout master` or
`git pull` commands.  You can do this easily with the command::

    python $CLAW/clawutil/src/python/clawutil/claw_git_status.py

and then check the files `claw_git_status.txt` and `claw_git_diffs.txt`,
which summarize the status of each subrepository.

Never commit to `master`
------------------------

You should never commit to `master`, only to a feature branch, so
the `master` branch should always reflect what's in the `master` branch on
the primary Github repositories.

You can update `master` to reflect any changes via the above approach (for
all subrepositories at once), or do `git checkout master` and then `git
pull` within any of the subrepositories separately.


.. _dev_remote:

Adding your fork as a remote
----------------------------

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

   provided you have ssh keys set up, or else:

        git remote add username htpps://github.com/username/amrclaw.git

   if you don't mind having to type your password whenever you push or pull.

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

Then go through the above steps to add your own fork as a remote 
if you plan to modify code and issue pull requests.

**Note:** The `git://github.com...` form of specifying a remote
clones the repository in a form
that does not allow pushing to it (unlike the `git@github.com:...` or
`https://github.com...` forms).  This is good practic so you do not
accidently try to push to the main clawpack repository rather than to your
own fork.

Modifying code
==============
Before making changes, make sure *master* is up to date::

        git checkout master
        git pull 

Then create a new branch based on `master` for any new commits::

        git checkout -b new_feature master

Now make changes, add and commit them, 
and then push to your own fork::

        # make some changes
        # git add the modified files
        git commit -m "describe the changes"

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

Issuing a pull request
----------------------

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

Testing a pull request
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

Top-level pull requests
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



Catching errors with Pyflakes and Pylint
===========================================

Pyflakes and Pylint are Python packages designed to help you catch errors or
poor coding practices.  To run pylint on the whole PyClaw package, do::

    cd $PYCLAW
    pylint -d C pyclaw

The `-d` option suppresses a lot of style warnings, since PyClaw doesn't
generally conform to PEP8.  To run pylint on just one module, use something
like::

    pylint -d C pyclaw.state

Since pylint output can be long, it's helpful to write it to an html file
and open that in a web browser::

    pylint -d C pyclaw.state -f html > pylint.html

Pyflakes is similar to pylint but aims only to catch errors.  If you
use Vim, there is a nice extension package 
`pyflakes.vim <https://github.com/kevinw/pyflakes-vim>`_
that will catch errors as you code and underline them in red.

Checking test coverage
========================
You can use nose to see how much of the code is covered by the current
suite of tests and track progress if you add more tests ::

    nosetests --with-coverage --cover-package=pyclaw --cover-html

This creates a set of html files in `./cover`, showing exactly which lines
of code have been tested.


Trouble-Shooting Tips
=====================
If you are having trouble installing or building Clawpack try out some of the
following tips:

 - Check to see if you have set the environment variable `FFLAGS` which may be
   overriding flags that need to be set.  This is especially important to check
   when building the PyClaw fortran libraries as a number of flags must be set
   for the Python bindings and will override the defaults.
