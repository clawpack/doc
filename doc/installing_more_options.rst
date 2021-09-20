:orphan:

.. _installing_more_options:

*******************************************
Additional options for installing Clawpack
*******************************************

See also:

* :ref:`installing`
* :ref:`installing_pip`

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

    tar -xzf clawpack-v5.8.0.tar.gz
    cd clawpack-v5.8.0
    export CLAW=/full/path/to/clawpack-v5.8.0  # in bash
    
The last command sets an environment variable if you are using the bash shell.
The syntax may be different in other shells.  Replace `/full/path/to`
with the appropriate full path.
    
You must also add `$CLAW` to your `PYTHONPATH` environment variable, 
see :ref:`python_path`.

Alternatively, rather than setting `PYTHONPATH` you can use `pip` to install
this version.  See :ref:`pip_version

or
 
 - Use `pip` to install this version of Clawpack::
 
    cd $CLAW
    pip install --user -e .   # note trailing dot indicating "this directory"

This is preferable to many users than using the environment variable
`PYTHONPATH`, but will also attempt to compile the Riemann solvers 
    
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
    git submodule init      # for repositories pyclaw, clawutil, visclaw, etc.
    git submodule update    # clones all the submodule repositories
    pip install --user -e . # note trailing dot indicating "this directory"
    export CLAW=/full/path/to/clawpack



.. _installing_docker:
    
Docker
------

Instead of installing Clawpack and all its dependencies, another alternative
is :ref:`docker_image`.  The Docker image already contains not only Clawpack
but also all the :ref:`prereqs`.

.. _installing_aws:


.. _install_pyclaw_parallel:

Installing PyClaw for parallel processing with PETSc
----------------------------------------------------

First, install Clawpack.  Then see the install instructions for :ref:`parallel`.

Alternatively, you may use the following shell scripts (assembled by Damian San Roman)
to install everything:

 -  Linux machine or Beowulf Cluster: https://gist.github.com/sanromd/9112666
 -  Mac OS X: https://gist.github.com/sanromd/10374134



Next steps:
===========

Once Clawpack is installed, you can go to one of the following pages to get
started:

- :ref:`first_run_pyclaw`
- :ref:`first_run_fortran`



.. _installing_pipintro:

*********
Old stuff
*********

pip install
-----------

The recommended approach is to use `pip install`. 
It is also possible to have multiple versions of Clawpack installed and
switch between them (i.e., modify your Python path) using `pip`. 
(see :ref:`installing_pip`)
If you plan to do this, or if you also wish to directly use the Fortran
variants of Clawpack (classic, AMRClaw, and/or GeoClaw), then we recommend 
using the following version of the `pip install` command 
**(you might want to first read the notes below to see if you
want to change anything in this command)**::  

    pip install --src=$HOME/clawpack_src --user -e \
        git+https://github.com/clawpack/clawpack.git@v5.8.0#egg=clawpack-v5.8.0 \
        --use-deprecated=legacy-resolver


This will download Clawpack (via a git clone) into the directory
`$HOME/clawpack_src/clawpack-v5.8.0`.  The top 
installation directory can be changed by modifying the ``--src`` target 
(or omit this part to put it in your current working directory).
If you have already downloaded Clawpack via a different mechanism then
see :ref:`pip_switch_version` rather than using the above command.


See :ref:`clawpack_components` for a list of what's included in this top
level directory.

**Note:** Using pip to install will also check some python
:ref:`prereqs` and may update these on your system, and will use 
`f2py <https://numpy.org/doc/stable/f2py/>`__ 
to  convert Fortran Riemann solvers to Python versions.  
(This is really only needed if you plan to use :ref:`pyclaw`.)
See :ref:`installing_options` if you want more control.

The ``--user`` flag is necessary if you are installing on a shared computer
where you do not have root access.  If you do have root access and want it
to be available to all users, you can omit this flag.  

The ``-e`` flag makes it an "editable" install, leaving the source code in
place and allowing you to modify it if desired.
(Otherwise, by default, pip would move the python code to some
`site-packages` directory and delete everything else.)

In order to use the Fortran codes within Clawpack, 
you should then set the environment
variable `CLAW` to point to the `clawpack-v5.8.0` directory within
the installation directory `$HOME/clawpack_src`, and `FC` to point
to the desired Fortran compiler, e.g. in the bash shell::

    export CLAW=$HOME/clawpack_src/clawpack-v5.8.0
    export FC=gfortran

See :ref:`setenv` for more information.   

For more discussion of `pip` installation, and troubleshooting hints, see
:ref:`installing_pip`.


.. _installing_options:

Other Installation Options
=====================================

In general, *installing* Clawpack requires downloading some version 
and then setting
paths so that Python import statements (and possibly Fortran Makefiles) find
the desired version.  Switching between versions already on your computer
simply requires resetting paths.  For hints and troubleshooting, see:

 - :ref:`setenv`
 - :ref:`python_path`
 - :ref:`installing_pip`

Note that if you wish to use the Python version of PDE solvers in 
:ref:`pyclaw`, these require precompiling the Fortran Riemann solvers using
`f2py <https://numpy.org/doc/stable/f2py/>`__  
to create Python versions. 
This is also done by `pip install`, along with setting paths.
Switching versions by resetting paths does not require recompiling these
solvers.

If you are only using the Fortran solvers 
(when using :ref:`contents_fortcodes`) then Python versions of the Riemann
solvers are not required.  In this case, any problems that arise
from the use of `f2py` can be avoided by simply setting paths in a
different manner.

Rather than using `pip`, there are several other options for using
Clawpack that may be useful depending on your needs.  These are summarized
in :ref:`installing_more_options`, including:

 - :ref:`installing_tarfile`
 - :ref:`install_dev`
 - :ref:`installing_docker`
 - :ref:`install_pyclaw_parallel`

**Python path:**
If you download a tarfile or use `git clone` to download a version, you can
still use `pip install` to set the Python path appropriately. 
See :ref:`installing_pip` for details.

If you are *not* using `pip` to set paths, then you will need to set
the `PYTHONPATH`
environment variable to point to a particular version of Clawpack,
but this is `not recommended <https://orbifold.xyz/pythonpath.html>`_.
See :ref:`python_path` for more details and tips on sorting out your path.
