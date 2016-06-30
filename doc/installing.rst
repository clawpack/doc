.. _installing:

**************************************
Installation instructions
**************************************

To replace :ref:`installing_old`.

.. contents::
   :depth: 2

Please `register
<http://depts.washington.edu/clawpack/register/index.html>`_ if you have not
already done so.  This is purely optional, but is useful in helping us track
the extent of usage.

Note that any of these installations also includes :ref:`visclaw` for plotting.

See also:

* :ref:`install_prerequisites`
* :ref:`clawpack_packages`
* :ref:`changes`
* :ref:`previous`
* :ref:`trouble_installation`

.. _install_pyclaw:

Install only PyClaw (serial)
=====================================

This works if you only wish to use the :ref:`pyclaw` Python interface 
(but **not** run Fortran codes from the Classic, :ref:`amrclaw`,
or :ref:`geoclaw` portions of Clawpack).  For more information, see
:ref:`clawpack_packages`

If you wish to install just PyClaw, everything can be handled by pip::

    pip install clawpack

Next go to :ref:`first_run_pyclaw`.


.. _install_fortran:

Install Fortran packages and Python tools
==========================================

This works if you wish to use the 
Fortran codes from the Classic, :ref:`amrclaw`, or :ref:`geoclaw` portions of
Clawpack, and the associated Python
tools (as needed for specifying input in `setrun.py`, plotting results with
`setplot.py` and :ref:`visclaw`, etc.)

First, download a tar file of the latest release:

* `https://github.com/clawpack/clawpack/releases/download/v5.3.1/clawpack-5.3.1.tar.gz
  <https://github.com/clawpack/clawpack/releases/download/v5.3.1/clawpack-5.3.1.tar.gz>`_

Alternatively, tarfiles for releases are also archived on 
`Zenodo <https://zenodo.org>`_ with
permanent DOIs.  The most recent release can be found at:
`10.5281/zenodo.50982 <http://dx.doi.org/10.5281/zenodo.50982>`_

See :ref:`clawpack_components` for a list of what's included in this tar file.

Save this tar file in the directory where you want the top level of the
clawpack tree to reside.  Then untar using the command::   

    tar -xzvf clawpack-5.3.1.tar.gz


Then move into the top level directory::

    cd clawpack-5.3.1
    pwd

The `pwd` command should print the `/full/path/to/top/level` that you
will need in the next step

.. _setenv:

Set environment variables
-------------------------

To use the Fortran versions of Clawpack you will need to set the
environment variable `CLAW` to point to the top level of clawpack tree
and adjust your `PYTHONPATH` to include the same directory.
In the bash shell these can be set via::

    export CLAW=/full/path/to/top/level
    export PYTHONPATH=$CLAW:$PYTHONPATH

You also need to set `FC` to point to the desired Fortran compiler,
e.g.::

    export FC=gfortran   # or other preferred Fortran compiler

Consider putting the two commands above in a file that is executed every
time you open a new shell or terminal window.  On Linux machines
with the bash shell this is generally the file `.bashrc` in your home
directory.  On a Mac it may be called `.bash_profile`.

If your environment variable `CLAW` is properly set, the command ::

    ls $CLAW

should list the top level directory, and report for example::

    CITATION.md changes.md  clawutil/   riemann/
    README.md   classic/    geoclaw/    setup.py
    amrclaw/    clawpack/   pyclaw/     visclaw/

 
.. _install_symlink:

Create symbolic links
---------------------

Then you should be able to do::

    cd $CLAW   # assuming this environment variable was properly set
    python setup.py symlink-only

This last step creates some symbolic links (in the directory
`$CLAW/clawpack`) that are needed in order for import
statements to work properly in Python.  You should now be able to start a
Python (or IPython) shell (from any directory)
and do the following command, for example, with no error:

    >>> from clawpack import visclaw

If not then either your `$PYTHONPATH` environment variable is not set
properly, or the required symbolic links were not created.

Next go to :ref:`first_run_fortran`.



.. _install_fortran_pyclaw:

Install for using both Fortran and PyClaw components
=====================================================

If you have installed using the procedure just described to 
:ref:`install_fortran` and you also want to use :ref:`pyclaw` (to run Clawpack
solvers directly from Python), then you can add one more step::

    cd $CLAW
    python setup.py install

This will compile a lot of Fortran code using `f2py` and will produce a lot of 
output, so you might want to redirect the output, e.g. ::

    python setup.py install > install_output.txt

If you get compilation errors in this step, you can still use the
Fortran codes (and associated Python tools) without problems.

To experiment with :ref:`pyclaw`, jump to :ref:`first_run_pyclaw`.  

    >>> from clawpack import visclaw


.. _install_pyclaw_parallel:

Install only PyClaw (for running in parallel)
================================================
First, install :ref:`pyclaw` as explained above.  Then see the install instructions
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


.. _install_alternatives:

Running Clawpack on a VM or in the Cloud
========================================
**Virtual Machine.**
An alternative to installing the :ref:`install_prerequisites` 
and Clawpack itself is to use the :ref:`vm`.


**Cloud Computing.**

* :ref:`pyclaw` can be installed and run in the cloud for free on 
  http://wakari.io or http://cloud.sagemath.com; see :ref:`cloud`.
* All of Clawpack can be run on AWS using the :ref:`aws`.



.. _install_prerequisites:

Installation Prerequisites
================================================

**Operating system:**

- Linux
- Mac OS X (you need to have the `Xcode developer tools
  <http://developer.apple.com/technologies/tools/xcode.html>`_ installed in
  order to have "make" working)

Much of Clawpack will work under Windows using Cygwin, but this is not officially
supported.

**Fortran:**

- `gfortran <http://gcc.gnu.org/wiki/GFortran>`_ or another F90 compiler

See :ref:`fortran_compilers` for more about which compilers work well with
Clawpack.
For Mac OSX, see `hpc.sourceforge.net <http://hpc.sourceforge.net/>`_ for
some installation options.

**Python:**

- Python Version 2.7 or above (but **not** 3.0 or above, which is not backwards compatible)
- `NumPy <http://www.numpy.org/>`_  (for PyClaw/VisClaw)
- `matplotlib <http://matplotlib.org/>`_ (for PyClaw/VisClaw)

The `Anaconda Python Distribution <https://docs.continuum.io/anaconda/index>`_
is an easy way to get all of these. 
See :ref:`python` for more information on
installing the required modules and to get started using Python if
you are not familiar with it.

  

