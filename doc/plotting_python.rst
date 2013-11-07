
.. _plotting_python:

***************************************
Plotting options in Python
***************************************


Clawpack  includes utilities for plotting using Python.  Most of these
are defined in the `clawpack.visclaw` module.
In order to use these you will need to insure that you have the required
modules installed (see :ref:`python-install`).

See :ref:`python` for more information on Python and pointers to many tutorials.

.. plotting_makeplots:

Producing html plots from the command line
==========================================


In most Clawpack directories, typing::

  $  make .plots

will compile the code and run it (if necessary) and then
produce a set of html files that can be
used to view the resulting plots.  These will be in a subdirectory
of the current directory as specified by PLOTDIR in the Makefile.



Producing a latex file with plots from the command line
=======================================================

A latex file with all the plots can also be produced by :ref:`printframes`,
and is also typically controlled by options set in the file setplot.py.

Setting plot parameters with a setplot function
===============================================

Typically each applications directory contains a file :file:`setplot.py`, see for
example :ref:`plotexamples`.
This file should define a function `setplot(plotdata)` that sets various
attributes of an object plotdata of class :ref:`ClawPlotData`.

Documentation on how to create a setplot function and the various plotting
parameters that can be set can be found in the section :ref:`setplot`.

Examples can be found at :ref:`plotexamples`.

.. _plotting_Iplotclaw:

Interactive plotting with `Iplotclaw`
=======================================

For interactive plotting we suggest using `IPython
<http://ipython.org>`_, which is a nicer shell
than the pure python shell, with things like command completion and history.


Here's an example::

    $  ipython
    In [1]: from clawpack.visclaw.Iplotclaw import Iplotclaw
    In [2]: ip = Iplotclaw() 
    In [3]: ip.plotloop()
    Executing setplot ... 

    Interactive plotclaw with ndim = 1 ... 
    Type ? at PLOTCLAW prompt for list of commands

	Start at which frame [default=0] ? 
	Plotting frame 0 ... 
    PLOTCLAW >  n
	Plotting frame 1 ... 
    PLOTCLAW > q
    quitting...
    In [4]: 

Type `?` at the PLOTCLAW prompt or `?command-name` for more
information.  Most commonly used are n for next frame, p for previous frame
and j to jump to a different frame.  Hitting return at the prompt repeats
the previous command.

You can restart the plotloop later by doing::

    In [4]: ip.plotloop()

    Interactive plotclaw with ndim = 1 ... 
    Type ? at PLOTCLAW prompt for list of commands

	Start at which frame [default=1] ? 
	Replot data for frame 1 [no] ? 
    PLOTCLAW > 


By default it starts at the frame where you previously left off.

If you want to change plot parameters, the easiest way is to edit the file
setplot.py, either in a different window or, if you use vi, by::

    PLOTCLAW > vi setplot.py

and then re-execute the setplot function using::

    PLOTCLAW > resetplot

If you recompute results by running the fortran code again and want to plot
the new results (from this same directory), you may have to clear the frames
that have already been viewed using::

    PLOTCLAW > clearframes

Or you can redraw the frame you're currently looking at without clearing the
rest of the cached frame data by doing::

    PLOTCLAW > rr

To see what figures, axes, and items have been defined by *setplot*::

    PLOTCLAW > show
    
    Current plot figures, axes, and items:
    ---------------------------------------
      figname = Pressure, figno = 1
         axesname = AXES1, axescmd = subplot(1,1,1)
            itemname = ITEM1,  plot_type = 1d_plot
     
      figname = Velocity, figno = 2
         axesname = AXES1, axescmd = subplot(1,1,1)
            itemname = ITEM1,  plot_type = 1d_plot
 


Type "help" or "help command-name" at the prompt for more options.

Access to current_data
----------------------

If you are viewing plots in using Iplotclaw and want to explore the data for
some frame or make plots directly in your Python shell, the data that is
being plotted is available to you in attributes of the Iplotclaw instance.
For example::

    >>> ip = Iplotclaw();  ip.plotloop()

    Interactive plotting for Clawpack output... 

    Plotting data from outdir =  _output
        ...
        Plotting Frame 0 at t = 0.0
    PLOTCLAW > q
    quitting...

    >>> pd = ip.plotdata
    >>> cd = ip.current_data

The *cd* object contains the :ref:`current_data` used for the most recent
plot, while *pd* is the :ref:`ClawPlotData` object that
gives access to all the plotting parameters currently being used as well as
to methods such as *getframe* for retrieving other frames of data from this
computation.  

If you want to change the directory *outdir* where the frame data is coming
from, you could do, for example::

    >>> pd.outdir = "_output2"
    >>> ip.plotloop()
    ...
    PLOTCLAW > clearframes    # to remove old frames from cache
    PLOTCLAW > rr             # to redraw current frame number but with new data


.. _ipyclaw:


.. _printframes:

printframes 
===========


**Need to update**

The function pyclaw.plotters.frametools.printframes can be used to produce html and
latex versions of the plots::

   >>> from clawpack.visclaw.data import ClawPlotData
   >>> from clawpack.visclaw import frametools
   >>> plotclaw = ClawPlotData()
   >>> # set attributes as desired
   >>> frametools.printframes(plotclaw)

A convenience method of ClawPlotData is defined to apply this function,
e.g.::

   >>> plotclaw.printframes()

This function is automatically called by the "make .plots" option available
in most examples.
   

.. _plot_files:

Specifying what and how to plot
===============================

The first step in specifying how to plot is to create a :ref:`ClawPlotData`
object to hold all the data required for plotting.  This is generally done
by creating a file `setplot.py` (see below).

Note that when you use Iplotclaw to do interactive plotting, e.g.::

       >>> ip = Iplotclaw()

Then object `ip` will have an attribute plotdata that is a :ref:`ClawPlotData` 
object.  This object will have attribute setplot initialized to
'setplot.py', indicating that other attributes should be set by
executing the setplot function defined in the file 'setplot.py' in this
directory.

Once you have a :ref:`ClawPlotData` object you can set various attributes to
control what is plotted interactively if you want.  For example,::

      >>> plotdata.plotdir = '_plots'
      >>> plotdata.setplot = 'my_setplot_file.py'

will cause hardcopy to go to subdirectory _plots of the current directory and
will cause the plotting routines to execute::

      >>> from my_setplot_file import setplot
      >>> plotdata = setplot(plotdata)

before doing the plotting.

There are many other :ref:`ClawPlotData` attributes and methods.

Most example directories contain a file setplot.py that contains a
function setplot(). This function
sets various attributes of the :ref:`ClawPlotData`
object to control what figures, axes, and items should be plotted for each
frame of the solution.

For an outline of how a typical set of plots is specified, see
:ref:`setplot`.



