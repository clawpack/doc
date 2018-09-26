:orphan:

.. _installing:

**************************************
Installation options
**************************************

Please `register <http://depts.washington.edu/clawpack/register/index.html>`_
if you have not already done so.  This is very useful in helping
us track the extent of usage, and important to the :ref:`funding` agencies
who support this work.  Please also see :ref:`citing`.

If you will only use PyClaw and/or VisClaw, skip to :ref:`pyclaw_install` for
the simplest installation instructions.

Instead of installing Clawpack and all its dependencies, another alternative
is :ref:`docker_image`.

For installation of older versions, see :ref:`previous`.

**Prerequisites:** Before installing, check that you have the :ref:`prereqs`.


Install using pip
=====================================

This is the simplest approach, particularly if you already 
use `pip` for other purposes; see :ref:`installing_pip`.  

Unfortunately if this doesn't work it may be hard to debug what went wrong.

.. _installing_tarfile:

Install from a tarfile
=====================================

Download a tar file of the latest release:

* `https://github.com/clawpack/clawpack/files/2330639/clawpack-v5.5.0.tar.gz
  <https://github.com/clawpack/clawpack/files/2330639/clawpack-v5.5.0.tar.gz>`_
* :ref:`previous`
* :ref:`changes`


See :ref:`clawpack_components` for a list of what's included in this tar file.

Save this tar file in the directory where you want the top level of the
clawpack tree to reside.  Then untar using the command::   

    tar -xzvf clawpack-5.5.0.tar.gz

Then move into the top level directory::

    cd clawpack-5.5.0

Next install the Python components of Clawpack (but read the next two
paragraphs first)::

    python setup.py install

This will compile a lot of Fortran code using `f2py` for PyClaw and may
produce a lot of output.

If you get compilation errors in this step, or if you do not plan to use
PyClaw, you can still use the
Classic, AMRClaw, and GeoClaw version; see :ref:`install_no-pyclaw` below.

If you only plan to use PyClaw, jump to :ref:`first_run`.  If you
plan to use Classic, AMRClaw, or GeoClaw continue with :ref:`setenv` to
set the environment variables `CLAW` and `FC`.


.. _install_no-pyclaw:

Install other packages without compiling PyClaw
================================================
If you get errors in the compilation step when using `pip install` or
`python setup.py install`, check :ref:`trouble_installation`. 
If your problem is not addressed there, please `let us know <claw-users@googlegroups.com>`_
or `raise an issue <https://github.com/clawpack/clawpack/issues>`_.
You can still use the Fortran codes (AMRClaw, GeoClaw, and Classic) by doing
the following.  

First, download a tarfile of the latest release as described above in
the section :ref:`installing_tarfile`.  

Next :ref:`setenv`, including `CLAW`, `FC`, and  `PYTHONPATH`.

Then you should be able to do::

    cd $CLAW   # assuming this environment variable was properly set
    python setup.py symlink-only

This will create some symbolic links in the `$CLAW/clawpack` 
subdirectory of your top level Clawpack directory, but does not compile code
or put anything in your site-packages.
In Python you should now be able to do the following, for example::

    >>> from clawpack import visclaw

If not then either your `$PYTHONPATH` environment variable is not set
properly or the required symbolic links were not created.
See :ref:`setenv` for more information, and :ref:`python_path` if you are
having problems with importing Python modules.

Next go to :ref:`first_run`.

.. _install_pyclaw_parallel:

Install only PyClaw (for running in parallel)
================================================
First, install PyClaw as explained above.  Then see the install instructions
for :ref:`parallel`.

Alternatively, you may use the following shell scripts (assembled by Damian San Roman)
to install everything:

* Linux machine or Beowulf Cluster: https://gist.github.com/sanromd/9112666
* Mac OS X: https://gist.github.com/sanromd/10374134


.. _install_dev:

Install the latest development version
================================================

The development version of Clawpack can be obtained by cloning 
`<https://github.com/clawpack>`_.  This is advised for those who want to help
develop Clawpack or to have the most recent bleeding edge version.
See :ref:`setup_dev` for instructions.

.. _installing_conda:

Install using conda (does not require a Fortran compiler)
=========================================================

.. warning:: This is currently under development and not extensively tested.

.. warning:: Not yet updated to 5.5.0.

You can install PyClaw and VisClaw only (without AMRClaw, GeoClaw, or Classic)
via the `conda package manager <http://conda.pydata.org/docs/index.html>`_.
Conda binaries are available for Mac OS X and Ubuntu Linux
(may work on other flavors of Linux).

From a terminal, simply do::

    conda install -c clawpack -c conda-forge clawpack=5.4.1

You might want to consider first creating a separate `conda environment
<http://conda.pydata.org/docs/using/envs.html>`_ if you want to separate
Clawpack and its dependencies from other versions of Python code. 

See https://github.com/clawpack/conda-recipes.


.. _install_alternatives:

Running Clawpack on a VM 
========================

See :ref:`docker_image` to use Docker.

Other VM versions are currently out of date. Check back for updates to
this page.



Next steps:
===========

Once Clawpack is installed, you can go to one of the following pages to get
started:

- :ref:`first_run_pyclaw`
- :ref:`first_run_fortran`

