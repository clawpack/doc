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
as a tar file. After untarring this, you can use `pip install` (and set `CLAW` 
if necessary) to point to this version.

Download a tar file from one of these sources:

  - `Clawpack releases on Github
    <https://github.com/clawpack/clawpack/releases>`_

  - The Zenodo link for the current release, listed at
    :ref:`releases`  (which also lists DOIs for recent versions, useful for
    :ref:`citing`)

After downloading a tar file you can do, e.g. ::

    tar -xzf clawpack-v5.6.1.tar.gz
    cd clawpack-v5.6.1
    pip install --user -e .   # note trailing dot indicating "this directory"
    export CLAW=/full/path/to/clawpack-v5.6.1
    
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

From a terminal, simply do::

    conda install -c clawpack -c conda-forge clawpack

You might want to consider first creating a separate `conda environment
<http://conda.pydata.org/docs/using/envs.html>`_ if you want to separate
Clawpack and its dependencies from other versions of Python code. 

See https://github.com/clawpack/conda-recipes.

.. _installing_docker:
    
Docker
------

Instead of installing Clawpack and all its dependencies, another alternative
is :ref:`docker_image`.  The Docker image already contains not only Clawpack
but also all the :ref:`prereqs`.

.. _installing_aws:
    
Launching an AWS instance with Clawpack installed
-------------------------------------------------

To appear.

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

