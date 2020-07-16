
.. _apps:

#################################
Clawpack Applications repository
#################################


More complex examples and applications are archived in the Github
`clawpack/apps` repository found at
`https://github.com/clawpack/apps <https://github.com/clawpack/apps>`_.

In particular, the directory `apps/fvmbook` contains many :ref:`fvmbook`.

The `Clawpack Gallery <http://www.clawpack.org/gallery/index.html>`__
shows results/animations from some selected examples in the `apps` repository.

These examples are not included in the basic Clawpack installation.
Users interested in obtaining this collection of applications can either
clone the repository using git::

    git clone git://github.com/clawpack/apps

or navigate to `https://github.com/clawpack/apps <https://github.com/clawpack/apps>`_
and click on the green "Code" button to see other options, such as downloading
a zip file.

Jupyter Notebooks
-----------------

The directory `apps/notebooks` contains a number of notebooks that illustrate
various aspects of Clawpack.  Many of these are also visible in rendered html
form in the 
`Gallery of Notebooks <http://www.clawpack.org/gallery/notebooks.html>`__.

Submodules
----------

The `apps` repository contains several 
`git submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`__
for collections of examples specific to some application.
This has the advantage that the submodules can be managed independent of the
main `apps` repository, perhaps by people who are not core Clawpack
developers.  (Contact us if you have a repository of examples you would like
to see added.)
Also each submodule may be of limited interest, and could contain some large
files that not every Clawpack user wants to download.

For example, after cloning the `apps` repository you will see a subdirectory
for storm surge modeling examples using GeoClaw named
`apps/surge-examples`, which initially is an empty directory.  The file
`apps/.gitmodules` shows that this is a submodule.
It also shows the url to the GitHub repository corresponding to this module
(where you could do a pull request, for example, if you find a bug).

If you want to add only the `surge-examples`, and not other submodules, 
you can do::

    git submodule update --init surge-examples

If you want to add all available submodules, leave off the submodule name::

    git submodule update --init

The `--init` flag is not needed (but won't hurt) if you are updating
a submodule that you have already initialized and cloned, e.g. if
the submodule maintainer has added new examples to it.


Examples included with Clawpack 
-------------------------------

Recall also that a few examples of how to use different flavors of 
Clawpack are included in every distribution of Clawpack, in the  directories

* `$CLAW/classic/examples`
* `$CLAW/amrclaw/examples`
* `$CLAW/geoclaw/examples`
* `$CLAW/pyclaw/examples`


These examples demonstrate some of the basic capabilities.
The plots resulting from running these examples should agree with those seen
in the `Clawpack Gallery <http://www.clawpack.org/gallery/index.html>`__.

