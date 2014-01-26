
.. _regression:

==================
Regression testing
==================

When making changes to the Clawpack code base it is a good idea to perform
regression tests to insure that the changes have not broken anything.  

See also: :ref:`git_versions`.

PyClaw
------

Regression tests can be performed via::

    cd $CLAW/pyclaw
    nosetests

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


