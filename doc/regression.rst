.. _regression:

==================
Regression testing
==================

.. contents::
   :depth: 2

Clawpack includes a number of tests that can be used to check for a working
installation or to see whether new changes to the code have broken anything.  

Running the tests
=================

If you use multiple git branches, before running the tests you should check that
you have checked out appropriate branches of all relevant repositories; see :ref:`git_versions`.

PyClaw
------

Regression tests can be performed via::

    cd $CLAW/pyclaw/examples
    nosetests

For more details, see :ref:`pyclaw_testing`.
(You may need to install `nose <https://nose.readthedocs.io/en/latest/>`_
if `nosetests` is not on your system.)

Fortran codes
-------------

A few quick tests can be perfomed of the `classic`, `amrclaw`, or `geoclaw`
codes by running `make tests` in the corresponding `tests` subdirectory, e.g.::

    cd $CLAW/classic/tests
    make tests

This uses `nosetests` to run a few Python scripts that in turn run the
Fortran codes and then compare a small set of values derived from the output
of the run with values that are stored in these directories.
If one of these tests fails then there is a problem to be investigated, but
these tests do not provide good coverage of the code or check that
everything is working properly.

A somewhat more complete set of tests can be run by executing all of the
codes in the `examples` subdirectories and comparing the resulting plots
with those archived in the :ref:`galleries`.  An attempt at automating this 
can be found in the `$CLAW/amrclaw/examples` directory, which uses the
`imagediff` tool described below.  This is still under development.


Travis continuous integration
-----------------------------

Most Clawpack git repositories now contain a file `.travis.yml` at the top
level so that every time a pull request is issued on Github, a basic set of
tests is run.  This uses the `Travis continuous integration
<https://travis-ci.org/>`_ platform.  Shortly after a PR is issued, Travis
will run the commands in the `.travis.yml` and report the results on the 
PR page.  Look for a green check mark (good) or a red X (bad) next to a commit
hash and click on it to see the Travis output.  
`[Sample output] <https://travis-ci.org/clawpack/clawpack/builds/15269312>`_


Diff tools for checking test output
===================================

chardiff tool for line-by-line comparison of output files
---------------------------------------------------------

If `_output_old` and `_output_new` are two sets of output files from old and
new versions of a code, then it is often useful to do a line by line
comparison of all of the files in each directory and display any
differences.  Standard tools such as `xxdiff` in linux or `opendiff` on a
Mac are not very good for this since they try to match up blocks of lines to
give the best match and may not compare the files line by line.

The Python script `$CLAW/clawutil/src/python/clawutil/chardiff.py` can be
used for this purpose::

    $ python $CLAW/clawutil/src/python/clawutil/chardiff.py _output_old _output_new

will create a new directory with html files showing all differences.  It can
also be used to compare two individual files.  See the docstring for more
details.

imagediff tool for pixel comparison of plots
--------------------------------------------

If `_plots_old` and `_plots_new` contain two sets of plots that we hope are
identical, the Python script
`$CLAW/clawutil/src/python/clawutil/imagediff.py` can be used to compare
the corresponding images in each directory and produce html files
that show each pair of images side by side.  If the images are not
identical it also shows an image indicating which pixels are different
in the two::

    $ python $CLAW/clawutil/src/python/clawutil/imagediff.py _plots_old _plots_new

will create a new directory with html files showing all differences.  It can
also be used to compare two individual files.  See the docstring for more
details.


.. _pyclaw_testing:

Running and writing tests in PyClaw
===================================

Running the tests
-----------------

The PyClaw test suite is built around `nosetests
<http://nose.readthedocs.org/en/latest/>`_ for automatic test discovery, with
supplementary functionality from the :mod:`pyclaw.util` module.  To run the
complete test suite with helpful output, issue the following command at the 
top-level of the pyclaw source directory::

    nosetests -vs

To run the parallel versions of the tests (if petsc4py is installed), run::

    mpirun -n 4 nosetests -vs

Replace 4 with the number of processes you'd like test on.  
Try prime numbers if you're really trying to break things!

The `-vs` switch tells nose to be verbose and to show you stdout, which can be
useful when debugging tests.  To run the tests with less output, omit the
`-vs`.

Running serial tests simultaneously
-----------------------------------

When running the tests, if your machine has multiple cores you can take
advantage of them by doing::

    nosetests -vs --processes=2

(replace "2" with the number of processes you want to spawn). However, using
large numbers of processes occasionally causes spurious failure of some tests
due to issues with the operating system.  If you see this behavior, it's best 
to run the tests in serial or with a small number of processes.

Running a specific test
-----------------------

The PyClaw tests are associated with particular applications in the examples/ sub-
directory of the primary repository directory.  If you want to run tests for a
specific application, simply specify the directory containing the application
you are interested in::

   nosetests -vs examples/acoustics_3d_variable

You can also specify a single file to run the tests it contains.

Doctests
--------

Several of the main PyClaw modules also have doctests (tests in their
docstrings). You can run them by executing the corresponding module::

    cd $PYCLAW/src/pyclaw
    python grid.py
    python state.py

If the tests pass, you will see no output.  You can get more output by using 
the `-v` option::

    python state.py -v

Writing New Tests
-----------------

If you contribute new functionality to PyClaw, it is expected that you will also
write at least one or two new tests that exercise your contribution, so that
further changes to other parts of PyClaw or your code don't break your feature.

This section describes some functions in `pyclaw.util` that facilitate testing.
You do not have to use any of the functionality offered by `pyclaw.util`, but it
may simplify your test-writing and allow you to check more cases than you would
easily specify by hand.

The most important function in :mod:`pyclaw.util` is
:func:`pyclaw.util.gen_variants`, which allows you to perform combinatorial
testing without manually specifying every feature you'd like to perform.
Currently, :func:`~pyclaw.util.gen_variants` can multiplicatively exercise
kernel_languages (Fortran or Python) and pure PyClaw or PetClaw implementations.
This allows you to write one function that tests four variants.

Another function provided by :mod:`~pyclaw.util` is
:func:`pyclaw.util.test_app`. The :func:`~pyclaw.util.test_app` function will
run an application as if started from the command line with the specified
keyword arguments passed in.  This is useful for testing specific code that does
not necessarily work with :mod:`petclaw`, for example, and is not expected to.

You will notice that both :func:`~pyclaw.util.gen_variants` and
:func:`~pyclaw.util.test_app` require a `verifier` method as an argument. 
These functions both effectively run tests and verify output with the following
function calls::
 
        output = application(**kwargs)
        check_values = verifier(output)

The `verifier` method needs to return `None` if there is no problem with the
output, or a sequence of three values describing what was expected, what it
received, and more details about the error.  A very simple `verifier` method
that you can use is :func:`pyclaw.util.check_diff`, which can use either an
absolute tolerance or a relative tolerance to compare an expected value against
the test output from the application.

See `examples/acoustics_1d_homogeneous/test_acoustics.py` for a comprehensive example
of how to use :func:`~pyclaw.util.gen_variants` and
:func:`~pyclaw.util.check_diff`. See `examples/shallow_sphere/test_shallow_sphere.py`
for an example that uses :func:`~pyclaw.util.test_app` and also loads a known
solution from disk using numpy.

