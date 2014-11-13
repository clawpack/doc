.. _installing:

**************************************
Installation instructions
**************************************

.. contents::
   :depth: 2

Please `register
<http://depts.washington.edu/clawpack/register/index.html>`_ if you have not
already done so.  This is purely optional, but is useful in helping us track
the extent of usage.

Note that any of these installations also includes :ref:`visclaw` for plotting.

See also:

* :ref:`trouble_installation`
* :ref:`clawpack_packages`

.. _install_pyclaw:

Install only PyClaw (serial)
=====================================
If you wish to install just PyClaw, everything is handled by pip::

    pip install clawpack

Next go to :ref:`first_run`.



.. _install_clawpack:

Install all Clawpack packages
=====================================
First, download a tar file of the latest release:

* `https://github.com/clawpack/clawpack/releases/download/v5.2.2/clawpack-5.2.2.tar.gz
  <https://github.com/clawpack/clawpack/releases/download/v5.2.2/clawpack-5.2.2.tar.gz>`_
* :ref:`previous`
* :ref:`changes`


See :ref:`clawpack_components` for a list of what's included in this tar file.

Save this tar file in the directory where you want the top level of the
clawpack tree to reside.  Then untar using the command::   

    tar -xzvf clawpack-5.2.2.tar.gz


Then move into the top level directory::

    cd clawpack-5.2.2

Next install the Python components of Clawpack::

    python setup.py install

This will compile a lot of Fortran code using `f2py` and will produce a lot of 
output, so you might want to redirect the output, e.g. ::

    python setup.py install > install_output.txt

If you get compilation errors in this step, you can still use the
Classic, AMRClaw, and GeoClaw; see :ref:`install_no-pyclaw`.

If you only plan to use PyClaw, jump to :ref:`first_run`.  If you
plan to use Classic, AMRClaw, or GeoClaw continue with :ref:`setenv`.

.. _setenv:

Set environment variables
-------------------------
To use the Fortran versions of Clawpack you will need to set the
environment variable `CLAW` to point to the top level of clawpack tree
(there is no need to perform this step if you will only use PyClaw).
In the bash shell these can be set via::

    export CLAW=/full/path/to/top/level

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

    README.md       riemann/        pyclaw/
    amrclaw/        setup.py        clawutil/       
    geoclaw/        visclaw/        classic/        
 
Next go to :ref:`first_run`.


.. _install_no-pyclaw:

Install other packages without compiling PyClaw
================================================
If you get errors in the compilation step when using `pip install` or
`python setup.py install`, check :ref:`trouble_installation`. 
If your problem is not addressed there, please `let us know <claw-users@googlegroups.com>`_
or `raise an issue <https://github.com/clawpack/clawpack/issues>`_.
You can still use the Fortran codes (AMRClaw, GeoClaw, and Classic) by doing
the following.  

First, download a tarfile of the latest release as described in
:ref:`install_clawpack`.  

Next :ref:`setenv`.  You must then also set your PYTHONPATH manually::

    export PYTHONPATH=$CLAW:$PYTHONPATH

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

See :ref:`python` for information on
installing the required modules and to get started using Python if
you are not familiar with it.

  

.. _first_test:

Testing your installation 
================================================

PyClaw
------
If you downloaded Clawpack manually, you can test your PyClaw
installation as follows (starting from your `clawpack` directory)::

    cd pyclaw
    nosetests

This should return 'OK'.

Classic
-------
As a first test of the Fortran code, try the following::

    cd $CLAW/classic/tests
    make tests

This will run several tests and compare a few numbers from the solution with
archived results.  The tests should run in a few seconds.

There are similar `tests` subdirectories of `$CLAW/amrclaw` and
`$CLAW/geoclaw` to do quick tests of these codes.

See also :ref:`testing`.
