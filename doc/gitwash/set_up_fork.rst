.. _set-up-fork:

==================
 Set up your fork
==================

.. note:: Clawpack is an "organization" on GitHub, which means that it is
   comprised of several distinct repositories.  These pages can be used to
   manage any (or all) of the Clawpack repositories, and in this documentation
   the string `REPOS` should be replaced by the specific repository name,
   e.g. *amrclaw*, *pyclaw*, *visclaw*, etc.


First you follow the instructions for :ref:`forking`.

Overview
========

::

   git clone git@github.com:your-user-name/REPOS.git
   cd REPOS
   git remote add upstream git://github.com/clawpack/REPOS.git

In detail
=========

Clone your fork
---------------

#. Clone your fork to the local computer with ``git clone
   git@github.com:your-user-name/REPOS.git``
#. Investigate.  Change directory to your new repo: ``cd REPOS``. Then
   ``git branch -a`` to show you all branches.  You'll get something
   like::

      * master
      remotes/origin/master

   This tells you that you are currently on the ``master`` branch, and
   that you also have a ``remote`` connection to ``origin/master``.
   What remote repository is ``remote/origin``? Try ``git remote -v`` to
   see the URLs for the remote.  They will point to your github fork.

   Now you want to connect to the upstream `Clawpack github`_ repository, so
   you can merge in changes from trunk.

.. _linking-to-upstream:

Linking your repository to the upstream repo
--------------------------------------------

::

   cd REPOS
   git remote add upstream git://github.com/clawpack/REPOS.git

``upstream`` here is just the arbitrary name we're using to refer to the
main Clawpack_ repository at `Clawpack github`_.

Note that we've used ``git://`` for the URL rather than ``git@``.  The
``git://`` URL is read only.  This means we that we can't accidentally
(or deliberately) write to the upstream repo, and we are only going to
use it to merge into our own code.

Just for your own satisfaction, show yourself that you now have a new
'remote', with ``git remote -v show``, giving you something like::

   upstream	git://github.com/clawpack/REPOS.git (fetch)
   upstream	git://github.com/clawpack/REPOS.git (push)
   origin	git@github.com:your-user-name/REPOS.git (fetch)
   origin	git@github.com:your-user-name/REPOS.git (push)

.. include:: links.inc

