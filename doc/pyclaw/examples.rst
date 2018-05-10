:group: pyclaw

.. _examples:

========================================
Working with PyClaw's built-in examples
========================================
PyClaw comes with many example problem scripts that can be
accessed from the module `clawpack.pyclaw.examples`.
If you have downloaded the PyClaw source, you can find them
in the directory `clawpack/pyclaw/examples/`.
These examples demonstrate the kinds of things that can be done
with PyClaw and are a great way to learn how to use PyClaw.  

Running and plotting examples
=============================

Interactively in IPython
++++++++++++++++++++++++
A built-in example can be run and plotted as follows::

    from clawpack.pyclaw import examples
    claw = examples.shock_bubble_interaction.setup()
    claw.run()
    claw.plot()

To run and plot a different example, simply replace `shock_bubble_interaction`
with another example name.  A number of keyword arguments may be passed to
the setup function; see its docstring for details.
These usually include the following:

   * ``use_petsc``: set to 1 to run in parallel

   * ``solver_type``: set to ``classic`` or ``sharpclaw``

   * ``iplot``: set to 1 to automatically launch interactive plotting after running.
     Note that this shouldn't be used in parallel, as every process will try to plot.

   * ``htmlplot``: set to 1 to automatically create HTML plot pages after running.

   * ``outdir``: the name of the subdirectory in which to put output files.  Defaults to
     ``./_output``.


From the command line
+++++++++++++++++++++
If you have downloaded the Clawpack source, you can run
the examples from the command line.
Simply do the following at the command prompt::

    $ cd clawpack/pyclaw/examples/acoustics_1d_homogeneous
    $ python acoustics.py iplot=1

You can run any of the examples similarly by going to the appropriate directory and
executing the Python script.  For convenience, the scripts are set up to pass any
command-line options as arguments to the setup function.


Built-in examples
=========================
You can see results from many of the examples in the :ref:`galleries`.


Adding new examples
========================================
If you have used PyClaw, we'd love to add your application to the built-in scripts.
Please contact us on the `claw-users Google group <http://http://groups.google.com/group/claw-users>`_
or just issue a `pull request on Github <http://github.com/clawpack/pyclaw/pulls>`_.


