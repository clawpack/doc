
.. _regression:

==================
Regression testing
==================

When making changes to the Clawpack code base it is a good idea to perform
regression tests to insure that the changes have not broken anything.  

**Developing a general procedure for regression testing still needs to be done.**

**Also need a database for storing "correct" results from various versions
of the code.**

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

    $ python $CLAWUTIL/chardiff.py _output_old _output_new

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

    $ python $CLAWUTIL/imagediff.py _plots_old _plots_new

will create a new directory with html files showing all differences.  It can
also be used to compare two individual files.  See the docstring for more
details.

See also: :ref:`git_versions`.
