.. _installing:

**************************************
Installation instructions
**************************************

.. _install_pyclaw:

Simple install (install PyClaw and VisClaw only)
------------------------------------------------
If you will only use PyClaw, everything is handled by pip::

    pip install clawpack

Do not use this if you intend to run Classic, AMRClaw, or GeoClaw (see next section).

.. _install_clawpack:

Full install (install all packages)
---------------------------------------
First::

    wget https://github.com/clawpack/clawpack/releases/download/5.0.0rc-alpha/clawpack-rc-alpha.tar.gz
    tar -xzvf clawpack-rc-alpha.tar.gz
    cd clawpack
    python setup.py install

If you will use Classic/AMRClaw/GeoClaw, you must also :ref:`setenv`.
If you wish to avoid compiling the PyClaw source, see :ref:`fortran_only`.


.. _first_run:

Running an example
------------------
Many examples of Clawpack simulations can be seen in the :ref:`galleries`.

**Using PyClaw.** To run an example and plot the results using PyClaw, simply do the following
(starting from your `clawpack` directory)::

    cd pyclaw/examples/euler_2d
    python shock_bubble_interaction.py iplot=1

That's it.  For next steps with PyClaw, see :ref:`basics`.

**Using Classic.**
First ensure that you have :ref:`setenv`.
A simple 1-dimensional acoustics equations can be solved
using the code in `$CLAW/classic/examples/acoustics_1d_example1`, as
illustrated in :ref:`gallery_classic_amrclaw`.

Move to this directory via::

    cd $CLAW/classic/examples/acoustics_1d_example1

You can try the following test in this directory, or you may want to first
make a copy of it (see the instructions in :ref:`copyex`).

The Makefiles are set up to do dependency checking so that in many
application directories you can simply type::

  $ make .plots

and the Fortran code will be compiled, data files created, the code
run, and the results plotted automatically, resulting in a set of webpages
showing the results.

However, if this is your first attempt to run a code, it is useful to go
through these steps one at a time, both to understand the steps and so that
any problems with your installation can be properly identified.

You might want to start by examining the Makefile.  This sets a number of
variables, which at some point you might need to modify for other examples,
see :ref:`makefiles` for more about this.  At the bottom of the Makefile is
an `include` statement that points to a common Makefile that is used by most
applications, and where all the details of the make process can be found.

To compile the code, type::

  $ make .exe    

If this gives an error, see :ref:`trouble_makeexe`.

This should compile the example code (after first compiling the required
library routines) and produce an executable named `xclaw` in this directory.

Before running the code, it is necessary to also create a set of data files
that are read in by the Fortran code.  This can be done via::
  
  $ make .data

If this gives an error, see :ref:`trouble_makedata`.

This uses the Python code in `setrun.py` to create data files that have the
form `*.data`.  

Once the executable and the data files all exist, we can run the code.  The
recommended way to do this is to type::

  $ make .output

If this gives an error, see :ref:`trouble_makeoutput`.

Before running the code a subdirectory `_output` is created
and the output of the code (often a large number of files) is directed to
this subdirectory.  This is convenient if you want to do several runs with
different parameter values and keep the results organized.  After the code
has run you can rename the subdirectory, or you can modify the variable
`OUTDIR` in the Makefile to direct results to a different directory.  See
:ref:`makefiles` for more details.  Copies of all the data files are also
placed in the output directory for future reference.



**Plotting the results.**  
Once the code has run and the files listed above have been created, there are several
options for plotting the results.  

To try the Python tools, type::

  $ make .plots

If this gives an error, see :ref:`trouble_makeplots`.

If this works, it will create a subdirectory named `_plots` that contains a number of
image files (the `*.png` files) and a set of html files that can be used to view the
results from a web browser.  See :ref:`plotting_makeplots` for more details.

An alternative is to view the plots from an interactive Python session, as described in
the section :ref:`plotting_Iplotclaw`.

If you wish to use Matlab instead, see :ref:`matlabplots`.

Other visualization packages could also be used to display the results, but you will need
to figure out how to read in the data.  See :ref:`fortfiles` for information about the
format of the files produced by Clawpack.


.. _fortran_only:

Installing without compiling PyClaw
-----------------------------------
If you get errors in the compilation step when using `pip install` or
`python setup.py install`, please `let us know <claw-users@googlegroups.com>`_
or `raise an issue <https://github.com/clawpack/clawpack/issues>`_.
You can still use the Fortran codes (AMRClaw, GeoClaw, and Classic) by doing
the following::

    wget https://github.com/clawpack/clawpack/releases/download/5.0.0rc-alpha/clawpack-rc-alpha.tar.gz
    tar -xzvf clawpack-rc-alpha.tar.gz
    cd clawpack
    python setup.py symlink-only

Next :ref:`setenv`.  You must then also set your PYTHONPATH manually::

    export PYTHONPATH=$CLAW:$PYTHONPATH


Alternative ways of running Clawpack
------------------------------------
**Virtual Machine.**
An alternative to installing the prerequisites and Clawpack itself is to use the
:ref:`vm`.

.. Broken link:
.. **Cloud Computing.**
.. Another alternative is to run Clawpack on the Cloud, see :ref:`aws`.


Prerequisites
-------------

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
 - Python Version 2.5 or above (but **not** 3.0 or above, which is not backwards compatible)
 - `NumPy <http://www.numpy.org/>`_  (for PyClaw/VisClaw)
 - `matplotlib <http://matplotlib.org/>`_ (for PyClaw/VisClaw)

See :ref:`python` for information on
installing the required modules and to get started using Python if
you are not familiar with it.


.. _install_from_git:

Developer install
---------------------

Clawpack 5.0 can be obtained by cloning a number of repositories
from `<https://github.com/clawpack>`_.  This is advised
for those who want to help
develop Clawpack or to have the most recent bleeding edge version.
See :ref:`developers_gitclone`  and :ref:`setup_dev` for instructions.


.. _setenv:

Set environment variables
-----------------------------
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
    

.. _first_test:

Testing your installation 
-------------------------
**PyClaw.**
To run the PyClaw tests, starting from your `clawpack` directory::

    cd pyclaw
    nosetests

This should return 'OK'.

**Classic.**
As a first test of the Fortran code, try the following::

    cd $CLAW/classic/tests
    make tests

This will run several tests and compare a few numbers from the solution with
archived results.  The tests should run in a few seconds.

There are similar `tests` subdirectories of `$CLAW/amrclaw` and
`$CLAW/geoclaw` to do quick tests of these codes.
