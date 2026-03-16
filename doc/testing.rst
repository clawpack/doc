
.. _testing:

===================================================================
Testing your installation
===================================================================

Fortran Regression Tests
-------------------------
The Fortran code in Clawpack has a suite of regression tests that can be run to
check that the code is working properly.  In each of the Fortran packages there
are a series of regression tests along side some of the examples as well as some
tests for Python functionality.  All these tests can be run by going to the base
directory of the corresponding pacakge and running::

    pytest

The most useful option for debugging a failing test is to use::
    
    pytest --basetemp=./test_output

which will save the output from the teset into the directory `test_output`.  The
package `pytetst` also has a number of additional debugging options that you can
use.  See the `pytest documentation <https://docs.pytest.org/>`_ for more
details.

Adding Regression Tests
-----------------------

:TODO: add instructions for adding regression tests here.

Old Testing
===========

PyClaw
------
If you downloaded Clawpack manually, you can test your :ref:`pyclaw`
installation as follows (starting from your `clawpack` directory)::


    cd pyclaw
    nosetests

This should return 'OK'.
(You may need to install `nose <https://nose.readthedocs.io/en/latest/>`_
if `nosetests` is not on your system.)

Classic
-------
As a first test of the Fortran code, try the following::

    cd $CLAW/classic/tests
    nosetests -sv


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


More extensive tests can be performed by running all of the examples in the
`examples` directory and comparing the resulting plots against those
archived in the :ref:`galleries`.  See also :ref:`regression`.
