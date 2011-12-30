
.. _git:

Using Git and GitHub
====================

.. include:: gitwash/git_links.inc

.. note::
   Thanks to `gitwash <https://github.com/matthew-brett/gitwash>`_ there
   is now a better version of this workflow description in
   :ref:`using-git`.

.. note:: Clawpack is an "organization" on GitHub, which means that it is
   comprised of several distinct repositories.  These pages can be used to
   manage any (or all) of the Clawpack repositories.  On this page the *doc*
   repository is used as an example.

Forking the repository
----------------------

As a first step you should create your own github account if you do not
already have one.  Follow the instructions after clicking `Create a free
account` on the `Pricing and Signup <https://github.com/plans>`_ page of
`<https://github.com/>`_.

Follow the directions about setting up ssh keys too.

Once you have an account, log in.  Then go to 
`<https://github.com/organizations/clawpack>`_
and click on the repository you want to work on.  
This repository on github will be called the *claworg repository* below
(because `clawpack` is an *organization* on github, meaning it is a
collection of repositories).  For more about the clawpack organization on
github, see `the Github plan <https://github.com/clawpack/doc/wiki/Github-plan>`_

Forking on github
-----------------

Suppose you want to fix a
typo in the documentation, for example.  Then you would click on the
`clawpack/doc` repository, which should take you to 
`<https://github.com/clawpack/doc>`_.

Now click on `Fork` near the top of this page, and create a fork on your own
account.  Once you go to this fork, you should see `username/doc` at the top
of the page, where `username` is your user name.

Cloning from github
-------------------

To create a clone on your own computer, first decide where you want this
directory to be. It may be convenient to create a directory `git/username`
to clone things from your `username` account.  (You might also want a
`git/clawpack` directory if you plan to clone things directly from the
`clawpack organization`.  You will probably only do this if you are a
developer who has permission to push directly into the `claworg` repository.)

Move into the desired directory, e.g. ::

    $ cd git/username

To create the clone, you need to give a command like::

    $ git clone git@github.com:username/doc.git

if you have ssh keys set up, or you can clone via http with::

    $ git clone https://username@github.com/username/doc.git

The box near the top of the webpage should show you exactly what to type.

In either case, this will create a directory named `doc`.

Deleting the master branch
--------------------------

Consider deleting your master branch as described at `deleting master on
github`_.  In the rest of this document *master* will refer to whatever name
you use instead.

Working in your clone
---------------------

Now do::

    $ cd doc
    $ git remote -v

This should show you that there is one
`remote` repository with the name `origin`, that you can both fetch from and
push to.  It should be the place you just cloned from.

Now suppose you modify a file::

    $ cd doc
    $ vi python.rst   # make a change

Then::

    $ git status | more

will show something like::

    # On branch master
    # Changes not staged for commit:
    #   (use "git add <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working
    #   directory)
    #
    #       modified:   python.rst
    #
    no changes added to commit (use "git add" and/or "git commit -a")

This indicates that the file has been changed but has not been added to the
index of files that will go into the next commit.

Staging files for the next commit
----------------------------------

To add it to the index (*stage it for the commit*), do::

    $ git add python.rst

or you can do::

    $ git add -u

to add all files that are being tracked that have modifications.

Now you should see::

    $ git status | more
    # On branch master
    # Changes to be committed:
    #   (use "git reset HEAD <file>..." to unstage)
    #
    #       modified:   python.rst
    #

Commiting changes
-----------------

You can now commit with::

    $ git commit -m "Fixed a typo"

This creates a new snapshot of the tracked files.

Push back to github
-------------------

To push this snapshot back to your github repository::

    $ git push origin master

Here `origin` means to push back to the remote named
`origin`, from which this clone originated,  and `master`
means to push to the master branch of that repository.  See below for more
about remotes and branches.

If you go back to the github webpage for your fork, you should see the
change has appeared there.

Pull requests
-------------

If you want this change to be incorporated back into the `claworg`
repository (the one you forked from in the Clawpack Organization), 
then on the github webpage for your
fork, you should see a button `pull request` up near the top.  Clicking on
this will prompt you for a message that will be sent to whoever the
gatekeeper is for this repository, who can then
merge your changes into `claworg` if he or she approves.


Fetching from a remote repository
---------------------------------

If you have more than one clone of your github repository (e.g. on two
different computers), then if you push changes from one clone back to github
you will probably want to fetch them from the other clone.  To fetch
changes, do::

    $ git fetch origin

This does not change your working directory, it just updates the information
git has stored in the hidden directory `.git` at the top level of your
clone, where a copy of all the history in the remote version (`origin`) is
stored.  

To see if there are differences between your working directory and the `master`
branch of the `origin` repository::

    $ git diff --name-status origin/master

to just list the files that are different, or::

    $ git diff origin/master 

to list all the diff's.

Merging into your working copy
------------------------------

Before merging any changes, make sure you do not have any uncommitted
changes in your working directory.  You should see::

    $ git status
    # On branch master
    nothing to commit (working directory clean)

To merge the changes in to your working directory.

    $ git merge origin/master

If this gives any messages about conflicts, you will have to edit the files
in question and decide which version of the conflicting lines you want to
keep, or merge them together by hand.  
See `git-merge documentation
<http://www.kernel.org/pub/software/scm/git/docs/git-merge.html>`_
for more about conflicts.

After fixing conflicts, you will have to::

    $ git add -u    # to add any changed files to the staging index
    $ git commit -m "merge message"

You only need to do this if there were conflicts.
If the merge worked, then by default git will automatically do a commit of
the result with a suitable merge message.   If you want to keep git from
doing this (so you can inspect the merge before committing it)::

    $ git merge --no-commit origin/master

Also note that sometimes git will not need to do a commit because your local
copy was a direct ancestor of the lastest version in `origin/master` (i.e.
you did not make any local commits since the time you cloned or the
last time you fetched and merged).  In this case, git can simply update your
working copy to bring it up to date with the latest commit in
`origin/master`.  This is called a *fast forward* merge.  

For more information see the  `git-merge documentation
<http://www.kernel.org/pub/software/scm/git/docs/git-merge.html>`_.


Pull
----

The command::

    $ git pull origin/master

does first a fetch and then a merge.  This is generally discouraged -- it's
safer and easier to see what's going on to first `fetch` and then `merge`
only after seeing what has changed.

Other remotes
-------------

When you clone a repository, there is a `remote` named `origin` that is
automatically created that corresponds to the repository you cloned from.

You can create other `remotes`.  For example, you might want to add a remote
named `claworg` that points to the clawpack organization repository
that you originally forked from on github.  This is useful if other
developers have made changes to the repository since you forked.  You
probably want to merge those changes into your local clone (from which you
can also push them back into your own github repository).

.. note:: Instead of `claworg` it is common to use `upstream` as a generic
   name, since this is the repository you forked from.

To add a remote::

    $ git remote add claworg git@github.com:clawpack/doc.git

Now you should see something like::

    $ git remote -v
    claworg git@github.com:clawpack/doc.git (fetch)
    claworg git@github.com:clawpack/doc.git (push)
    origin  https://rjleveque@github.com/rjleveque/doc.git (fetch)
    origin  https://rjleveque@github.com/rjleveque/doc.git (push)

To fetch all of the history of the `claworg` repository (including all
recent changes)::

    $ git fetch claworg

Now you can do the same things with `claworg/master` that you earlier did
with `origin/master`, e.g.  see what differences there are between
`claworg/master` and your working copy::

    $ git diff --name-status claworg/master

To merge any differences into your working copy::

    $ git merge claworg/master

Assuming the merge worked and was committed, you now probably want to
push the latest back to your
github repository (`origin`, which was originally forked from `claworg`)::

    $ git push origin/master

Branches
--------

By default there is always a branch named `master`.  If this is the only
branch, you will see::

    $ git branch
    * master

If you want to create a
branch on which to try something out, say a branch named `test`, you can
do::

    $ git checkout -b test
    Switched to a new branch 'test'

    $ git branch
      master
    * test

This shows there are two branches, and the asterisk shows which one is
checked out.

To switch back to the master branch::

    $ git checkout master
    Switched to branch 'master'

    $ git branch
    * master
      test

Notes:

* Creating a branch doesn't copy any files.  Initially it just gives a new
  name to the most recent commit.  Only if you start making new commits will
  the branches diverge.  You should check to make sure you know what branch
  you are on before committing.

If you later want to merge the branch `test` into `master`::

    $ git checkout master
    $ git status     # make sure it is clean: no uncommitted changes
    $ git diff test  # to see what difference there are
    $ git merge test # to merge differences into working copy

If you are done with the branch `test` you can delete it with::

    $ git branch -d test

Note that 
`origin/master` behaves like a branch and the notation indicates that it
refers to the the `master` branch of the remote repository named `origin`.
You can even check it out::

    $ git checkout origin/master

if you want to look around in it, but you won't be able to commit to it
since this isn't a real branch of your local repository.  You will get a
warning message to this effect if you give the above command.  You will also
see that you are not on a real branch if you do::

    $ git branch
    * (no branch)
      master
      test

To get back to your `master` branch, just do::

    $ git checkout master

Other useful commands
---------------------

To see a summary of commits::

    $ git log | more

To see a short one-line summary of commits::

    $ git log --pretty=oneline

To see the history and how different branches relate to one another, try::

    $ gitk &

See the `gitk introduction
<http://lostechies.com/joshuaflanagan/2010/09/03/use-gitk-to-understand-git/>`_
for more about this.

Other resources
---------------

See also:

*  :ref:`using-git`.
* `Fernando Perez's blog <http://fperez.org/py4science/git.html>`_ has many
  useful links to get started.  
* `Git Parable
  <http://tom.preston-werner.com/2009/05/19/the-git-parable.html>`_ gives a
  good intro to the concepts.
* `gitk introduction <http://lostechies.com/joshuaflanagan/2010/09/03/use-gitk-to-understand-git/>`_
  has a good description of merging.
* `<http://help.github.com/>`_
* `<http://gitref.org/index.html>`_
* `<http://progit.org/book/>`_ 
* `<http://www-cs-students.stanford.edu/~blynn/gitmagic/index.html>`_ More
  advanced tricks
* `<https://git.wiki.kernel.org/index.php/GitSvnCrashCourse>`_ Tips for users
  switching from Subversion.
* `<https://git.wiki.kernel.org/index.php/GitDocumentation>`_ Many more
  documentation links

