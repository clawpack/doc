
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

The Matlab search path
----------------------
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
To visualize Clawpack output using the Matlab plotting routines, first
produce output files from an example using::

  $ make .output

This will build the appropriate Clawpack executable, create necessary input files
for the executable, and
finally run the executable to create output files.  These output files
are stored by default in the directory '_output'.

.. _plotclaw:

The plotclaw command
--------------------
Once output files, e.g. 'fort.q0000', 'fort.q0001', and so on, and
corresponding fort.t0000' or 'fort.t0001' files have been created, the
user can plot them in Matlab by entering one of
the following commands (depending on whether the output is one,
two or three dimensional) at the Matlab prompt::

  >> plotclaw1

or::

  >> plotclaw2

or::

  >> plotclaw3

Initially, the user is prompted to run a file `setplot`_.  For
example::

  >> plotclaw2

  plotclaw2  plots 2d results from clawpack or amrclaw
  Execute setplot2 (default = yes)?

The setplot file sets various parameters in the base workspace needed
to create the plot (see below for more details on this file).
Entering [enter] at this prompt will run the file.

Successively hitting [enter] steps through and plots data from each of
the fort files in order.  In one and two dimensions, this plotting
prompt is::

  Frame 2 at time t = 0.2
  Hit <return> for next plot, or type k, r, rr, j, i, q, or ?

In three dimensions, one can optionally step through user defined slices of data by entering
'x', 'y' or 'z' at the command prompt::

  Frame 1 at time t = 0.0625
  Hit <return> for next plot, or type k, r, rr, j, i, x, y, z, q, or ?

A description of the plot prompt options is given by entering '?'::

  Frame 2 at time t = 0.2
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

After the graphics routines have created the plot, but before the user
is returned to the plot prompt, a file `afterframe`_ is called.  This
file contains user commands to set various plot properties.  See below
for more details on what the user might wish to include in this file.

.. _setplot:

The setplot file
----------------
The properties of the Matlab plot are controlled through two main
user-defined files located, typically, in the current working
directory.  The first of these files, the 'setplot' file (e.g. setplot1.m, setplot2.m or
setplot3.m) control basic plot properties that must be known before the plot is created.
Such properties include

 * component of q to plot, (.e.g. rho=1,  rhou=2, rhov=3 and so on).
 * a user defined quantity (e.g. pressure or velocity) to plot,
 * the maximum number of frames to plot
 * the location of the output files
 * the line type or symbol type for 1d plots or scatter plots.  Different symbols or line types can be specified for each AMR level.
 * the plot type, e.g. a pseudo-color plot, a Schlieren type plot or a scatter plot.
 * grid mappings for mapped grids or manifold calculations,
 * user defined slices through the data (3d data)
 * isosurface properties (3d plots)

A typical setplot file might contain the following parameter settings::

  % -----------------------------------------------
  % file: setplot2.m (not all parameters are shown)
  % -----------------------------------------------
  OutputDir = '_output';
  PlotType = 1;                % Create a pseudo-color plot
  mq = 1;                      % which component of q to plot
  UserVariable = 0;            % set to 1 to specify a user-defined variable
  UserVariableFile = ' ';      % name of m-file mapping data to q
  MappedGrid = 0;              % set to 1 if mapc2p.m exists for nonuniform grid
  MaxFrames = 1000;            % max number of frames to loop over
  MaxLevels = 6;               % max number of AMR levels
  ...

One of the main uses of the 'keyboard' option described in the `plotclaw`_ section is to
allow the user to temporarily change the value of plotting parameters set in the setplot file.

To ensure that the required set of variables is defined, the user is encouraged to
create and modify a local copy of setplot1.m, setplot2.m or setplot3.m found in
'${CLAW}visclaw/src/matlab'.

To get more help on what types of settings can be specified in the setplot file,
enter the following command::

  >> help setplot

Each of the examples in Clawpack include a 'setplot' file which you
can browse to get an idea as to what can be put in the file.

.. _afterframe:

The afterframe file
-------------------
The 'afterframe.m' script is the second file which control aspects of the
plot and is called after the plot has been created. The following are
commonly set in the afterframe file:

 * set axis limits and scaling
 * add a 1d reference solution (1d plots and scatter plots)
 * print out the current frame to a png, jpg or other graphics format file.
 * add, show or hide contour lines on slices (2d/3d)
 * show or hide AMR patch and cube borders (2d/3d)
 * modify the colormap (2d/3d)
 * set the color axis (2d/3d)
 * show or hide grid lines on different AMR levels (2d/3d)
 * add lighting to isosurfaces (3d)
 * hide or show isosurfaces (3d)
 * show or hide slices (3d)

A typical 'afterframe' file might contain the following commands::

  % -----------------------------------------------
  % file: afterframe.m
  % -----------------------------------------------
  axis([-1 1 -1 1]);      % Set the axis limits
  daspect([1 1 1]);       % Set the aspect ratio

  colormap(jet);

  showpatchborders;       % Show outlines of AMR patch borders
  showgridlines(1:2);     % Show gridlines on level 1 and 2 grids

  cv = linspace(-1,1,21); % Values for contour levels
  cv(cv == 0) = [];
  drawcontourlines(cv);   % add contour lines to a plot

  caxis([-1 1]);          % Set the color axis

  shg;                    % Bring figure window to the front

  fstr = framename(Frame,'frame0000','png','_plots');
  print('-dpng',fstr);       % Create .png file of figure.

  clear afterframe;

The final 'clear' statement is added so that any modifications that
the user makes to the afterframe file while stepping through plot
frames will take effect immediately.

When plotting results from AMR runs, the user can also create an
'aftergrid.m' file.  This file will be called after each individual
grid of data is plotted.

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


Output files not found
``````````````````````
The following error message indicates that the output files have not been found::

  Hit <return> for next plot, or type k, r, rr, j, i, x, y, z, q, or ?

  Frame 2 (./fort.t0002) does not exist ***


  Frame 2(ascii) does not exist ***

Be sure to check that that the variable 'OutputDir', set in the setplot file, points to
the proper location of the output files that you wish to plot.
Second, double check that you actually have fort.[t/q]XXXX files in that directory.

MaxFrames not set
`````````````````
The error message below most likely means that a 'setplot' script
containing a definition for MaxFrames was not run::

  >> plotclaw2

  plotclaw2  plots 2d results from clawpack or amrclaw
  Execute setplot2 (default = yes)? no

  MaxFrames parameter not set... you may need to execute setplot2

To correct this problem, the user should make sure that they have
local copy of a setplot file in their working directory, that it
defines the required set of variables and that it is run at least once before
the plotclaw command.

Switching examples
``````````````````
The graphics are controlled to a large extent using variables that are
set in the Matlab base workspace.  This can lead to unpredictable results
when switching between Clawpack examples.

To illustrate what can go wrong, suppose one sets::

  MappedGrid = 1;         % assumes that mapc2p file exists

in the setplot file for one example, and then switches to a second
example which is not a simulation on a mapped grid. If the variable
'MappedGrid' is not explicitly set to zero in the setplot file for the
second example, the Matlab routines will look for a grid mapping file
'mapc2p.m' which may not be found for the second example.

To avoid such potential clashes of variables, the
user is strongly encouraged to enter the command::

  >> clear all;

before switching examples.  This will clear the base workspace of
all plotting parameters and avoid potential conflicts in base variable settings.

The user is also encouraged to issue a command::

  >> close all

in situations where the one example explicitly sets plotting features such as a colormap,
or axes scaling that are not overridden by subsequent plot commands.

.. _matlab_gallery:

Matlab Gallery
--------------
The interested user is encouraged to browse the `Matlab Gallery`_ for
examples of the types of plots that can be created with the Clawpack Matlab
plotting routines.

.. _Matlab Gallery: http://math.boisestate.edu/~calhoun/visclaw/matlab_gallery/test_graphics/index.html
