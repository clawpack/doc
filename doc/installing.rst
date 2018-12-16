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

**Register:** Please `register <http://depts.washington.edu/clawpack/register/index.html>`_
if you have not already done so.  This is very useful in helping
us track the extent of usage, and important to the :ref:`funding` agencies
who support this work.  Please also see :ref:`citing`.

**Prerequisites:** Before installing, check that you have the :ref:`prereqs`.

**Environment variables:**  
If you are using the Fortran versions in Classic, AMRClaw, or GeoClaw
then after installing you also need to set the `CLAW` environment variable,
and perhaps also the Fortran compiler variable `FC`.
For example (in a bash shell)::

    export CLAW=/full/path/to/clawpack  # to top level clawpack directory
    export FC=gfortran                  # or other preferred Fortran compiler

See :ref:`setenv` for more information.   

**Python path:**
Below we suggest using `pip install` to set up your Python path to point to
the desired version of Clawpack.  As long as the top level `clawpack`
directory is on your path, you should be able to import the necessary
modules in Python.  Instead of pip, you can also set the `PYTHONPATH`
environment variable to point to a particular version of Clawpack,
but this is `not recommended <https://orbifold.xyz/pythonpath.html>`_.
See :ref:`python_path` for more details and tips on sorting out your path.

**Components:**
See :ref:`clawpack_components` for a list of what is generally included
under the top level `clawpack` directory when using any of the approaches below.
(And what is not included, e.g. the :ref:`apps`.)

.. _installing_options:

Installation Options
=====================================

*Installing* Clawpack requires downloading some version and then setting
paths so that Python import statements (and possibly Fortran Makefiles) find
the desired version.  Before installing, read about environment
variables and Python path above if you haven't already.

Installing with `pip` also compiles Riemann solvers written in Fortran for
use in PyClaw.  If you get a Fortran error message when installing, see
:ref:`trouble_f2py`.  See also :ref:`prereqs_fortran`.


.. _installing_pipintro:

pip install
-----------

The recommended approach is to use `pip install`.  You can download
and install with a single command, and you can also use `pip` to
switch to a different version of Clawpack (i.e. to modify your
Python path) if you have reason to have multiple versions on your
computer.  

Depending on your needs, if you only want to use PyClaw it may be as simple as::

        pip install clawpack

but first see :ref:`installing_pip` for more discussion and instructions,
since we recommend a more complicated version of this command for most purposes.

.. _installing_tarfile:

tar file
--------

You can download the most recent (or certain previous versions) of Clawpack
as a tar file. After untarring this, you can use `pip install` (and set `CLAW` 
if necessary) to point to this version.

    - Most recent: `https://github.com/clawpack/clawpack/files/2330639/clawpack-v5.5.0.tar.gz
      <https://github.com/clawpack/clawpack/files/2330639/clawpack-v5.5.0.tar.gz>`_
    - :ref:`previous`  (also lists DOIs for recent versions, useful for
      :ref:`citing`)

After downloading a tar file you can do, e.g. ::

    tar -xzf clawpack-v5.5.0.tar.gz
    cd clawpack-v5.5.0
    pip install --user -e .   # note trailing dot indicating "this directory"
    export CLAW=/full/path/to/clawpack-v5.5.0
    
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

.. _installing_conda:

Using conda (does not require a Fortran compiler)
----------------------------------------------------------

You can install PyClaw and VisClaw only (without AMRClaw, GeoClaw, or Classic)
via the `conda package manager <http://conda.pydata.org/docs/index.html>`_.
Conda binaries are available for Mac OS X and Ubuntu Linux
(may work on other flavors of Linux), using Python 2.7 or 3.6.
See https://github.com/clawpack/conda-recipes.

From a terminal, simply do::

    conda install -c clawpack -c conda-forge clawpack

You might want to consider first creating a separate `conda environment
<http://conda.pydata.org/docs/using/envs.html>`_ if you want to separate
Clawpack and its dependencies from other versions of Python code. 


.. _installing_docker:
    
Docker
------

Instead of installing Clawpack and all its dependencies, another alternative
is :ref:`docker_image`.  The Docker image already contains not only Clawpack
but also all the :ref:`prereqs`.

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

