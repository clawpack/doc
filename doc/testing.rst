
.. _testing:

===================================================================
Regression tests
===================================================================

Many repositories have a subdirectory named `tests` that contain a few
regression tests that run very quickly and check that a few numbers
determined from the solution agree with values stored in the example
directories.  For example, to run some quick tests of `amrclaw`::

    cd $CLAW/amrclaw/tests
    make tests

will run several tests and report the results.

More extensive tests can be performed by running all of the examples in the
`examples` directory and comparing the resulting plots against those
archived in the :ref:`galleries`.  This can be done, for example in
`amrclaw`, via::

    cd $CLAW/amrclaw/examples
    make tests

This takes much longer to run. 
