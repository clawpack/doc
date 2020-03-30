.. _first_run_fortran:

Testing your Fortran installation and running an example
=============================================================

This assumes that you have downloaded the Fortran components of Clawpack,
see :ref:`install_fortran`.

First ensure that you have :ref:`setenv`
and that you have the :ref:`install_prerequisites`.

As a first test of the Fortran code, try the following::

    cd $CLAW/classic/tests
    nosetests -sv

(You may need to install `nose <https://nose.readthedocs.io/en/latest/>`_
if `nosetests` is not on your system.)

This will run several tests and compare a few numbers from the solution with
archived results.  The tests should run in a few seconds and 
you should see output similar to this::

    runTest (tests.acoustics_1d_heterogeneous.regression_tests.Acoustics1DHeterogeneousTest) ... ok
    runTest (tests.acoustics_3d_heterogeneous.regression_tests.Acoustics3DHeterogeneousTest) ... ok
    runTest (tests.advection_2d_annulus.regression_tests.Advection2DAnnulusTest) ... ok

    ----------------------------------------------------------------------
    Ran 3 tests in 4.639s
    OK


There are similar `tests` subdirectories of `$CLAW/amrclaw` and
`$CLAW/geoclaw` to do quick tests of these codes.


Running an example
------------------

Many examples of Clawpack simulations can be seen in the :ref:`galleries`.


Classic
-------

A simple 1-dimensional acoustics equations can be solved
using the code in `$CLAW/classic/examples/acoustics_1d_example1
<_static/classic/examples/acoustics_1d_example1/README.html>`__.

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

More examples
-------------

There are additional examples in these directories:

    * `$CLAW/classic/examples`
    * `$CLAW/amrclaw/examples`
    * `$CLAW/geoclaw/examples`

You might also want to download the :ref:`apps`, which contains additional
examples.
