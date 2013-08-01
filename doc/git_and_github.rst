
.. _git_and_github:

Using Git and GitHub
====================

.. include:: gitwash/git_links.inc

.. note::
   Thanks to `gitwash <https://github.com/matthew-brett/gitwash>`_ there
   is now a better version of this workflow description in
   :ref:`using-git`.  (Now out of date!)

.. note:: Clawpack is an "organization" on GitHub, which means that it is
   comprised of several distinct repositories.  See :ref:`developers` to
   get started working with the repositories.

.. _git_fork:

Forking a repository
----------------------

As a first step you should create your own github account if you do not
already have one.  Follow the instructions after clicking `Create a free
account` on the `Pricing and Signup <https://github.com/plans>`_ page of
`<https://github.com/>`_.

Follow the directions about setting up ssh keys too.

Once you have an account, log in.  Then go to 
`<https://github.com/organizations/clawpack>`_
and click on the repository you want to work on.  
You can now click on the *Fork* link to create a fork of this repository in
on your own Github account.



Cloning from github
-------------------

See :ref:`developers`.


Tips on using Git
-----------------

To appear.


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

