
.. _testing:

===================================================================
Testing your installation
===================================================================

PyClaw Tests
------------

You can exercise all the tests in PyClaw by running the following command from 
the base of the `pyclaw directory`:

.. code-block:: console

    cd $CLAW/pyclaw
    pytest


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

If you want to add a new regression test using the new `pytest` framework, you can follow along with this example for the acoustics_1d_example1 test.  If something more complicated is needed, take a look at the other tests available in the packages, or reach out to the developers for help.

Adding a Test for `acoustics_1d_example1`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create a new file in the `examples/acoustics_1d_example1` directory called `test_acoustics_1d_example1.py` by:

.. code-block:: console

    touch examples/acoustics_1d_example1/test_acoustics_1d_example1.py

and place the following content in it:

.. code-block:: python
    :linenos:

    #!/usr/bin/env python

    from pathlib import Path
    import pytest

    import clawpack.classic.test as test


    def test_acoustics_1d_example1(tmp_path: Path, save: bool):
        runner = test.ClassicTestRunner(
            tmp_path=tmp_path,
            test_path=Path(__file__).parent,
        )

        # Set data using default setrun.py file in local directory.  If you want
        # to override this then hand it another setrun.py
        runner.set_data()

        runner.rundata.clawdata.num_output_times = 2
        runner.rundata.clawdata.tfinal = 1.0
        runner.rundata.clawdata.output_t0 = False

        runner.write_data()

        # Build xclaw and execute code
        runner.executable_name = "xclaw"
        runner.build_executable()
        runner.run_code()

        # Check t=0.5 and t=1.0, we are looking at both the pressure and velocity
        # in this test so need to specify those indices
        runner.check_frame(1, indices=(0, 1), save=save)
        runner.check_frame(2, indices=(0, 1), save=save)

    if __name__=="__main__":
        pytest.main([__file__])

This file is executable from the command line.  The middle section modifies what is in the local `setrun.py` file to make the test small and deterministic.  The final section runs the test when the file is executed from the command line.  You can run this test with:

.. code-block:: console

    python test_acoustics_1d_example1.py

or with:

.. code-block:: console

    pytest test_acoustics_1d_example1.py


2. We now need to generate the expected results for this test.  To do this, run the test with the `--save` option:

.. code-block:: console

    pytest test_acoustics_1d_example1.py --save

This will run the test and save the results in a directory called `regression_data` in the same directory as the test.  This file contains the expected results for the test, which will be used to compare against future runs of the test.  Note that if you would like to see the full output of the test, you can add `--basetemp=./test_output` to the command above, which will save the output from the test into the directory `test_output`.


3. Now you can run the test without the `--save` option to check that it is working properly.  If the test passes, you should see output similar to this:

.. code-block:: console

    ============================= test session starts ==============================
    platform darwin -- Python 3.8.10, pytest-7.1.2, pluggy-1.0.0
    rootdir: /path/to/clawpack/classic/examples/acoustics_1d_example1
    collected 1 item

    test_acoustics_1d_example1.py .                                         [100%]

    ============================== 1 passed in 5.00s ===============================

To complete the test you will want to add the test script `test_acoustics_1d_example1.py` add the regression data to the repository.

==============
Legacy Testing
==============

Tests via `nose` are no longer supported, but if you have an older version of
Clawpack installed and `nostests` available, you can still run the old tests.
These are not as comprehensive as the new `pytest` tests, but they can be useful
for checking that your installation is working properly.


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
