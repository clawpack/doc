:orphan:

.. _installing_fortcodes:

**********************************************
Options for installing Clawpack Fortran codes
**********************************************


This page describes ways to download and "install" Clawpack in a way that
the Fortran versions of the PDE solvers (:ref:`contents_fortcodes`)
can be used, along with Python codes that support these solvers, including
the visualization tools in VisClaw.  

If you plan to use the PDE solvers directly from :ref:`pyclaw`, please
see :ref:`installing` for other options.  If you are not sure, see
:ref:`clawpack_packages`

.. _installing_tarfile:

tar file
--------

You can download the most recent (or certain previous versions) of Clawpack
as a tar file. After untarring this, you can set environment variables
to point to this version.

Download a tar file from one of these sources:

- `Clawpack releases on Github    
  <https://github.com/clawpack/clawpack/releases>`_

- The Zenodo link for the current release, listed at
  :ref:`releases`  (which also lists DOIs for recent versions, useful for
  :ref:`citing`)

After downloading a tar file you can do, e.g. ::

    tar -xzf clawpack-v5.8.1.tar.gz
    cd clawpack-v5.8.1
    export CLAW=/full/path/to/clawpack-v5.8.1  # in bash
    
The last command sets an environment variable when using the bash shell.
The syntax may be different in other shells.  Replace `/full/path/to`
with the appropriate full path.
    
You must also add `$CLAW` to your `PYTHONPATH` environment variable, 
see :ref:`python_path`.

.. _install_dev:

git clone
---------

You can clone the git repositories from `<https://github.com/clawpack>`_.  
This is particularly useful if you
want the latest development version or a branch that is not in a release yet,
and/or if you plan to contribute to the code yourself via a pull request.
See :ref:`developers` for more details, but the basic commands are::

    git clone git://github.com/clawpack/clawpack.git
    cd clawpack
    git checkout v5.8.1     # or an older version; `git tag -l` to list options
    git submodule init      # for repositories pyclaw, clawutil, visclaw, etc.
    git submodule update    # clones all the submodule repositories
    export CLAW=/full/path/to/clawpack    # in bash

The last command sets an environment variable when using the bash shell.
The syntax may be different in other shells.  Replace `/full/path/to`
with the appropriate full path.
    
You must also add `$CLAW` to your `PYTHONPATH` environment variable, 
see :ref:`python_path`.

**Components:**
See :ref:`clawpack_components` for a list of what is generally included
under the top level `clawpack` directory when using any of these approaches.
(And what is not included, e.g. the :ref:`apps`.)

Next steps:
===========

Once Clawpack is installed, you can get started:

- :ref:`first_run_fortran`
- :ref:`trouble_installation`
