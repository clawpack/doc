:group: pyclaw

.. _pyclaw_plotting:

=======================
Plotting PyClaw results
=======================
PyClaw relies on the 
`VisClaw package <http://github.com/clawpack/visclaw/>`_ for easy plotting, although
it is of course possible to load the output into other visualization packages.
VisClaw supports 1D and 2D plotting; for 3D plotting, we recommend using the
`old Clawpack MATLAB routines <http://depts.washington.edu/clawpack/users-4.6/matlab_plotting.html>`_
for now.

This page gives some very basic information; for more detail, see :ref:`plotting`
in VisClaw's documentation.


Basics
=======
VisClaw includes routines for creating HTML and LaTex plot pages or plotting interactively.
These require a `setplot.py` file that defines the plotting parameters;
see :ref:`plotting_python`.
for more information.  Once you have an appropriate `setplot.py` file,
there are some convenience functions in `$PYCLAW/src/petclaw/plot.py`
for generating these plots.  Assuming you have output files in `./_output`
(which is the default), you can generate HTML pages with plots from Python via

.. doctest::

    >>> from clawpack.pyclaw import plot
    >>> plot.html_plot() # doctest: +SKIP

This will generate HTML pages with plots and print out a message with the
location of the HTML file.  To launch an interactive plotting session
from within Python, do

.. doctest::

    >>> from clawpack.pyclaw import plot
    >>> plot.interactive_plot() # doctest: +SKIP

To see a list of commands available in the resulting interactive environment,
type "?" or see :ref:`plotting_Iplotclaw`.

Plotting result from parallel runs
========================================
By default, when running in parallel, PyClaw outputs data in a binary format.
In order to plot from such files, just replace ``pyclaw`` with ``petclaw`` in the
commands above; e.g.

.. doctest::

    >>> from clawpack.petclaw import plot
    >>> plot.interactive_plot() # doctest: +SKIP

