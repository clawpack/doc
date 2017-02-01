
.. _fgmax:

=====================
Fixed grid monitoring
=====================

.. warning::

   This feature has been modified and this documentation describes 
   the version introduced in 5.2.1.

See also:

 - :ref:`fgmax_tools_module` - Tools for working with fgmax files
 - :ref:`setrun_fgmax` - For adding fgmax data to `setrun.py`

GeoClaw has the capability to monitor certain quantities on a specified
"fixed grid" by interpolating from the AMR grids active at each time step,
or at specified time increments.
This is useful in particular to record the maximum flow depth observed at
each point over the course of a computation, or the maximum flow velocity,
momentum, or momentum flux.  These quantities are often of interest in
hazard modeling.

It is also possible to record the *arrival time* of a flow or wave at each
point on the grid.  

The "grids" do not have to be rectangular grids aligned with the
coordinate directions, but can consist of an arbitrary list of points
that could also be points along a one-dimensional transect or points
following a coastline, for example.  It is also possible to specify logically
rectangular grids of points covering an arbitrary quadrilateral.

Each grid is specified by an input file in a specified form described below.
The list of file names for desired grids is specified in the `setrun`
function, see :ref:`setrun_fgmax`.

This is an improved version of the algorithms used in earlier versions of
GeoClaw, and now  
correctly interpolates when a grid point lies near the junction of two
grid patches, which was not always handled properly before.
The earlier version can still be used for outputing results at intermediate
times on a fixed grid (see :ref:`fgout`), but is not recommended for the purpose
of monitoring maxima or arrival times.  

.. _fgmax_input:

Input file specification 
-------------------------

(changed in Clawpack 5.2.0.)

The GeoClaw Fortran code reads in one or more files that specify grid(s) for
monitoring values during the computation.  

The input file(s) are specified to GeoClaw by a list of file names set in
`setrun.py` by setting `rundata.fgmax_data.fgmax_files`.
The order the files appear in this list determines the number assigned to
this grid (starting with 1) that may be needed for processing or plotting
the results.

Currently at most 5 fgmax grids are allowed by default.  If you need more,
you can adjust the parameter `FG_MAXNUM_FGRIDS` in
`$CLAW/geoclaw/src/2d/shallow/fgmax_module.f90` and the do `make new` to
recomile everything that depends on this module.   

Each input file describing a grid of points has the following form::

    tstart_max  
    tend_max
    dt_check
    min_level_check
    arrival_tol
    point_style

followed by additional lines that depend on the value of `point_style`.

If `point_style == 0`, an arbitrary collection of `(x,y)` points is allowed
and all must be listed, preceeded by the number of points::

    npts      # number of points
    x1 y1     # first point
    x2 y2     # second point
    ...       # etc.

These points need not lie on a regular grid and can be specified in any order.

If `point_style == 1`, a 1-dimensional transect of points is specified by
the next three lines of the file, in the form::

    npts       # number of points to generate
    x1, y1     # first point
    x2, y2     # last point

If `point_style == 2`, a 2-dimensional cartesian of points is specified by
the next three lines of the file, in the form::

    nx, ny     # number of points in x and y  (nx by ny grid)
    x1, y1     # lower left corner of cartesian grid
    x2, y2     # upper right corner of cartesian grid

If `point_style == 3`, a 2-dimensional logically rectangular array
of points is specified by the next five lines of the file, in the form::

    n12, n23     # number of points along adjacent edges (see below)
    x1, y1       # first corner of grid
    x2, y2       # second corner of grid
    x3, y3       # third corner of grid
    x4, y4       # fourth corner of grid

The corners should define a convex quadrilateral (ordered clockwise around the
perimeter).  An array of points will be defined as the intersection points of
two sets of lines.  The first set is obtained by connecting `n12`
equally spaced points on the side from `(x1,y1)` to `(x2,y2)` with the same
number of points equally spaced on the side from `(x3,y3)` to `(x4,y4)`.
The second set of lines is obtained by connecting `n23` equally spaced
points on the side from `(x2,y2)` to `(x3,y3)` with the same 
number of points equally spaced on the side from `(x4,y4)` to `(x1,y1)` 

The other paramters in the input file are:

* `tstart_max` : float

  starting time to monitor maximum

* `tend_max` : float

  ending time to monitor maximum

* `dt_check` : float

  time increment for monitoring maximum and arrivals.  
  Interpolate to fixed grid and
  update values only if the time since the last updating exceeds this time
  increment.  Set to 0 to monitor every time step.

* `min_level_check` : integer

  Minimum AMR level to check for updating the maximum value observed and
  the arrival time.  
  Care must be taken in selecting this value since the maximum observed 
  when interpolating to a point from a coarse AMR level may be much larger
  than the value that would be seen on a fine grid that better resolves the 
  topography at this point.  Often AMR "regions" are used to specify that a
  fine grid at some level `L` should always be used in the region of
  interest over the time period from `start_max` to `tend_max`, and then 
  it is natural to set `min_level_check` to `L`.


* `arrival_tol` : float

  The time reported as the "arrival time" is the first time the value
  of the surface elevation is greater than `sea_level` + `arrival_tol`.


Tools to create a input file
-----------------------------

See class `FGmaxGrid` in the :ref:`fgmax_tools_module`.  The function
`FGmaxGrid.write_input_data` can be used to create an input file of the form
described above, and may be useful if you want to use Python to assist in
setting the parameters or defining a set of points to list with 
`point_style == 0`.

.. _fgmax_values:

Values to monitor
-----------------

The values to be monitored are specified by the subroutine `fgmax_values`.
The default subroutine found in the library 
`$CLAW/geoclaw/src/2d/shallow/fgmax_values.f90` 
is now set up to monitor the
depth `h` (rather than the value `eta_tilde` used in Version 5.1)
and optionally will also monitor the speed :math:`s = \sqrt{u^2 + v^2}`
and three  other quantities (the momentum :math:`hs`, 
the momentum flux :math:`hs^2`, and :math:`-h`, which is useful to monitor
the minimum depth at each point, e.g. in a harbor where ships may be grounded).  

The values monitored by the default routine described above is determined
by the value of the `fgmax_module` variable `FG_NUM_VAL`, which can be set
to 1, 2, or 5.  This value is now read in from the data file `fgmax.data`
and can be set by specifying the value of
`rundata.fgmax_data.num_fgmax_val` in `setrun.py`.  

Choice of interpolation procedure
---------------------------------

The library routine `geoclaw/src/2d/shallow/fgmax_interpolate.f90` has
been improved in 5.2.0 to fix some bugs.  This routine does bilinear
interpolation the finite volume grid centers to the fixed grid in
order to update the maximum of values such as depth or velocity.

An alternative version of this routine was added in 5.2.0
that does piecewise constant interpolation instead. This simply uses the
value in the finite volume grid cell that contains the fixed grid
point (0 order extrapolation) and avoids problems sometimes seen when
doing linear interpolation near the margins of the flow.
(The surface elevation :math:`\eta = B + h` may be very large in a
neighboring dry cell and interpolating this sometimes gives non-physical large
values for the surface elevation in wet cells.)

This routine is in `fgmax_interpolate0.f90` and is now recommended.  

Starting in Version 5.4.0 this is the default that is specified in the
library `Makefile` found in `$CLAW/geoclaw/src/2d/shallow/Makefile.geoclaw`
(see :ref:`makefiles_library`).   

To switch back to the bilinear interpolation version, you can modify
your application `Makefile` to exclude the default routine and
include the desired routine, e.g.  you can use 
`this Makefile <_static/Makefile_geoclaw_bilinear_interp>`_
(modified if necessary for any other application-specific changes).



.. _fgmax_processing:

Processing and plotting fgmax output
------------------------------------

After GeoClaw has run, the output directory should contain the following
files:

 - `fort.FG1.valuemax` containing values at each fgmax grid point,
 - `fort.FG1.aux1` containing the bathymetry at each fgmax grid point.

If more than one fgmax grid was specified by `rundata.fgmax_data.fgmax_files`
then there will be similar files `fort.FG2.*`, etc.  They will be numbered in
the order they appear in the list of input files.

These files are most easily dealt with using :ref:`fgmax_tools_module` by
defining an object of class `fgmax_tools.FGmaxGrid` and using the  
class function `read_output` to read the output.  

For some examples, see `apps/tsunami/chile2010_fgmax` and 
`apps/tsunami/bowl_radial_fgmax` in the :ref:`apps`.   
Sample results appear in the :ref:`gallery_geoclaw`.

TODO:  Add a simple example here?

.. _fgmax_output_format:

Format of the output files
--------------------------

The paragraphs below describe in more detail the structure of the output files
for users who need to process them differently.

If `point_style == 0` for a grid then the points will be listed in the same
order as specified in the input file.  For other values of `point_style`
(1-dimensional transects or 2-dimensional arrays) the values will be output in
a natural order.  In all cases the first two columns of each output file are
the longitude and latitude of the point.

The remaining columns of `fort.FG1.aux1` contain the bathymetry (the first
component of the `aux` array in GeoClaw) interpolated to this fgmax grid
point.  There will be one column for each level of AMR (up to the number
specified in `setrun.py` by the parameter `amr_levels_max`).  These values are
initialize to `-0.99999000E+99` and only updated if interpolation at this
level is used to update a value at this particular grid point.  Values at
different levels may be needed to interpret the output stored
`fort.FG1.valuemax`, e.g. to determine if a point is onshore or off-shore, and
to compute the maximum surface elevation  at a point
:math:`\eta = h + B` from the maximum depth recorded at this point.

The file `fort.FG1.valuemax` contains the longitude and latitude of each point
in columns 1 and 2.  Column 3 contains the AMR level at which the maximum that
is recorded was observed.  (This is used to index into the array of bathymetry
values from `fort.FG1.aux1` when doing computations as described in the
previous paragraph).  

The **last** column of `fort.FG1.valuemax` contains the arrival time of the wave
at this grid point, as determined by the tolerance `arrival_tol` specified in
the input file.  The time reported as the "arrival time" is the first time the
value of the surface elevation is greater than `sea_level` + `arrival_tol`.
Points where this value is `-0.99999000E+99` never met this criterion, perhaps
because the point was never inundated.  

The intermediate columns of `fort.FG1.valuemax` contain the maximum observed
value of a quantity such as the flow depth along with the time at which the
maximum was observed.  How many values are recorded depends on the setting of 
`rundata.fgmax_data.num_fgmax_val` in `setrun.py`:  

 - If `rundata.fgmax_data.num_fgmax_val == 1`:
    - Column 4 contains maximum value of depth `h`,
    - Column 5 contains time of maximum `h`.

 - If `rundata.fgmax_data.num_fgmax_val == 2`:
    - Column 4 contains maximum value of depth `h`,
    - Column 5 contains maximum value of speed,
    - Column 6 contains time of maximum `h`,
    - Column 7 contains time of maximum speed.

 - If `rundata.fgmax_data.num_fgmax_val == 5`:
    - Columns 4,5,6,7,8 contain maximum value depth, speed, momentum, momentum
      flux, and `hmin`, respectively,
    - Columns 9,10,11,12,13 contain times the maximum was recorded, for each
      value above.

    
