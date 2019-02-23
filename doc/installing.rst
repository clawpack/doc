:orphan:

.. _installing:

**************************************
Installing Clawpack
**************************************

See also:

* :ref:`clawpack_packages`
* :ref:`changes`
* :ref:`previous`
* :ref:`trouble_installation`

**Prerequisites:** Before installing, check that you have the :ref:`prereqs`.


.. _installing_pipintro:

pip install
-----------

The recommended approach is to use `pip install`. 
It is also possible to have multiple versions of Clawpack installed and
switch between them (i.e., modify your Python path) using `pip`. 
(see :ref:`installing_pip`)
If you plan to do this, or if you also wish to directly use the Fortran
variants of Clawpack (classic, AMRClaw, and/or GeoClaw), then we recommend 
using the following version of the `pip install` command 
(you might want to first read the notes below to see if you
want to change anything in this command)::  

    pip install --src=$HOME/clawpack_src --user -e \
        git+https://github.com/clawpack/clawpack.git@v5.5.0#egg=clawpack-v5.5.0

This will install Clawpack into the directory
`$HOME/clawpack_src/clawpack-v5.5.0`, or the top 
installation directory can be changed by modifying the `--src` target.

See :ref:`clawpack_components` for a list of what's included in this top
level directory.

The `--user` flag is necessary if you are installing on a shared computer
where you do not have root access.  If you do have root access and want it
to be available to all users, you can omit this flag.  

The `-e` flag makes it an "editable" install, leaving the source code in
place and allowing you to modify it if desired.

In order to use the Fortran codes within Clawpack, 
you should then set the environment
variable `CLAW` to point to the `clawpack-v5.5.0` directory within
the installation directory `$HOME/clawpack_src`, and `FC` to point
to the desired Fortran compiler, e.g. in the bash shell::

    export CLAW=$HOME/clawpack_src/clawpack-v5.5.0
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

Rather than using `pip`, there are several other options for using
Clawpack that may be useful depending on your needs.  These are summarized
in :ref:`installing_more_options`, including:

 - :ref:`installing_tarfile`
 - :ref:`install_dev`
 - :ref:`installing_conda`
 - :ref:`installing_docker`
 - :ref:`installing_aws`
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

**Components:**
See :ref:`clawpack_components` for a list of what is generally included
under the top level `clawpack` directory when using any of the approaches below.
(And what is not included, e.g. the :ref:`apps`.)


Next steps:
===========

Once Clawpack is installed, you can go to one of the following pages to get
started:

- :ref:`first_run_pyclaw`
- :ref:`first_run_fortran`

