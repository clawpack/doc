.. _following-latest:

=============================
 Following the latest source
=============================

.. note:: Clawpack is an "organization" on GitHub, which means that it is
   comprised of several distinct repositories.  These pages can be used to
   manage any (or all) of the Clawpack repositories, and in this documentation
   the string `REPOS` should be replaced by the specific repository name,
   e.g. *amrclaw*, *pyclaw*, *visclaw*, etc.


These are the instructions if you just want to follow the latest
*Clawpack* source, but you don't need to do any development for now.

The steps are:

* :ref:`install-git`
* get local copy of the git repository from github
* update local copy from time to time

Get the local copy of the code
==============================

From the command line::

   git clone git://github.com/clawpack/REPOS.git

You now have a copy of the code tree in the new ``REPOS`` directory.

Updating the code
=================

From time to time you may want to pull down the latest code.  Do this with::

   cd REPOS
   git pull

The tree in ``REPOS`` will now have the latest changes from the initial
repository.

.. include:: links.inc
