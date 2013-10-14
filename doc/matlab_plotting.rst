
.. _matlabplots:

***************************************
Plotting using Matlab
***************************************

.. _Matlab: http://www.mathworks.com

Before version 4.3, Clawpack used `Matlab`_ (Mathworks, Inc.) for plotting and visualizing
results of simulations. For this purpose, an extensive set of plotting
tools were developed.  These are still available in
`$CLAW/visclaw/src/matlab`.  The user interface for these routines is
essentially unchanged from the previous versions, although several new
features have been added.


These graphics tools extend standard
Matlab plotting routines by allowing for easy plotting of both 2d and
3d adaptively refined mesh data produced from AMRClaw and solutions on
2d manifolds, produced from either single grid Clawpack, or AMRClaw.
In each of these cases, the user can easily
switch on or off the plotting of grid lines (on a per-level basis),
contour lines, isosurfaces, and AMR patch borders, cubes and other
graphical items.  In 3d, the user can create a custom set of slices,
and then loop through the slices in the x,y or z directions.  All
visualization assumes finite volume data, and individual plot
"patches" use cell-averaged values to color mesh cells directly.  No
graphical interpolation is done when mapping to the colormap.

.. _setting_up_matlab:

Environment variables
---------------------------------------
To use the Matlab plotting tools with Clawpack, the user will need to
first be sure that the necessary Matlab routines are on the Matlab
search path.  This can be done by explicitly setting the MATLABPATH
environment variable.  In bash, this is done via

  $ export MATLABPATH ${CLAW}/visclaw/src/matlab

Alternatively, one can permanently add this directory to the Matlab search path
using the Matlab "pathtool" command::

  >> pathtool

.. _create_output_for_matlab:

Creating output files
---------------------
To visualize output using Matlab plots, first produce output files from an example using::

  $ make .output

This will build the executable 'xclaw', run the Python script
'setrun.py' to create necessary input files for the executable, and
finally run the executable to create output files.  These output files
will be stored by default in the directory '_output'.

.. _plot_matlab:

The plotclaw command
--------------------
Once we have output files, e.g. 'fort.q0000', 'fort.q0001', and so on, and corresponding
fort.t0000' or 'fort.t0001' files, we plot them in Matlab by entering
at the Matlab prompt one of the following::

  >> plotclaw1

or::

  >> plotclaw2

or::

  >> plotclaw3

depending on whether you are plotting one, two or three dimensional output.

Initially, you will be prompted as whether you want to run a file `setplot_file`_.  For
example::

  >> plotclaw2

  plotclaw2  plots 2d results from clawpack or amrclaw
  Execute setplot2 (default = yes)?

The 'setplot.m' file should be located in the working directory, but
can be anywhere on the Matlab path. This file contains initial
settings for the plot needed before the plot can be created.  The file
is run by default.

Successively hitting [enter] steps through and plots data from each of the fort files in order.  In
one and two dimensions, this plotting prompt is::

  Frame 2 at time t = 0.2
  Hit <return> for next plot, or type k, r, rr, j, i, q, or ?

In three dimensions, one can optionally step through user defined slices of data by entering
'x', 'y' or 'z' at the command prompt::

  Frame 1 at time t = 0.0625
  Hit <return> for next plot, or type k, r, rr, j, i, x, y, z, q, or ?

The explanations for each prompt option are giving by entering '?'::

  Frame 2 at time t = 0.2
  Hit <return> for next plot, or type k, r, rr, j, i, q, or ?  ?

  Hit <return> for next plot, or type k, r, rr, j, i, q, or ?  ?
    k  -- keyboard input.  Type any commands and then "return"
    r  -- redraw current frame, without re-reading data
    rr -- re-read current file,and redraw frame
    j  -- jump to a particular frame
    i  -- info about parameters and solution
    x  -- loop over slices in x direction (3d only)
    y  -- loop over slices in y direction (3d only)
    z  -- loop over slices in z direction (3d only)
    q  -- quit

Graphical features an be controlled from either the 'setplot' file, or the
'afterframe' file, described below.

.. _setplot_file:

The setplot file
----------------
The properties of the Matlab plot are controlled through two main
user-defined files located, typically, in the current working
directory.  The 'setplot' file (e.g. setplot1.m, setplot2.m or
setplot3.m) control basic plot properties that must be known before the plot is created.
Such properties include

 * the index of the system variable to plot,
 * a user defined quantity (e.g. pressure or velocity) to plot,
 * the maximum number of frames to plot
 * the location of the output files
 * the line type or symbol type for 1d plots or scatter plots.  Different symbols or line types an be specified for each AMR level.
 * whether to plot a pseudo-color plot, a Schlieren type plot or a scatter plot.
 * user defined slices through the data for 3d plots
 * add isosurfaces to 3d plots
 * Indicate whether grid mappings for mapped grids or manifold calculations should be used.

To get more help on what types of settings can be specified in the setplot file,
issue the following command::

  >> help setplot

Each of the
examples in Clawpack include a 'setplot' file which you can browse to get
an idea as to what can be put in the file.

.. _afterframe_file:

The afterframe file
-------------------
The 'afterframe.m' script is the second file which control aspects of the
plot and is called after the plot has been created.
Such commands allow the user to

 * set axis limits and scaling
 * add a 1d reference solution (1d plots and scatter plots)
 * print out the current frame to a png, jpg or other graphics format file.
 * add, show or hide contour lines on slices (2d/3d)
 * show or hide AMR patch and cube borders (2d/3d)
 * modify the colormap (2d/3d)
 * show or hide grid lines on different AMR levels (2d/3d)
 * add lighting to isosurfaces (3d)
 * hide or show isosurfaces (3d)
 * show or hide slices (3d)

The user is encouraged to browse the 'afterframe.m' file available
with each Clawpack example to get a better idea as to what one might
include in this file.

.. _matlab_help:

Getting help
-----------------------------------
To get help on any of the topics available in the Matlab graphics tools, you can always issue
the command::

  >> help clawgraphics

at the Matlab prompt.  This will bring up a list of topics which you can get further help on.

.. _base_variables:

Trouble shooting
----------------
Below are a few potential problems one can run into with the Matlab plotting routines.

Switching examples
``````````````````
The graphics are controlled to a large extent using variables that are
set in the Matlab base workspace.  This can cause problems when
switching between examples if a base variable for one example is not
explicitly set in a subsequent example.

To illustrate what can go wrong, suppose one sets::

  MappedGrid = 1;         % assumes that mapc2p file exists

in the setplot file for one example, and then switches to a second
example which is not a simulation on a mapped grid. If the variable
'MappedGrid' is not explicitly set to zero in the setplot file for the
second example, the Matlab routines will look for a grid mapping file
'mapc2p.f' which will not exist for the second example.

To avoid such potential clashes of variables between examples, the
user is strongly encouraged to issue::

  >> clear all;

before switching examples.  This will clear the global workspace of
all variables that might cause base variables settings to conflict.

Output files not found
``````````````````````
The following error message indicates that the output files have not been found::

  Hit <return> for next plot, or type k, r, rr, j, i, x, y, z, q, or ?

  Frame 2 (./fort.t0002) does not exist ***


  Frame 2(ascii) does not exist ***

Be sure to check that that the variable 'OutputDir', set in the setplot file, points to
the proper location of the output files that you wish to plot.
Second, double check that you actually have fort.[t/q]XXXX files in that directory.


.. _matlab_gallery:

Matlab Gallery
--------------
The interested user is encouraged to browse the `Matlab Gallery`_ for
examples of the types of plots available with the Clawpack Matlab
plotting routines.

.. _Matlab Gallery: http://math.boisestate.edu/~calhoun/visclaw/matlab_gallery/test_graphics/index.html
