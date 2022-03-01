
.. _fgmax:

=====================
Fixed grid monitoring
=====================

.. warning::

   This feature has been modified and this documentation describes 
   the version introduced in 5.7.0.

See also:

 - :ref:`fgmax_tools_module`
 - :ref:`setrun_fgmax` - For adding fgmax data to `setrun.py`

GeoClaw has the capability to monitor the maximum value of
certain quantities on a specified fixed
"fgmax grid" by interpolating from the AMR grids active at each time step,
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

**New in v5.7.0:** One can also specify a set of fgmax point by providing a
data file in the style of a topography DEM file with `topo_type==3`, but in
which the values provided are either 0 or 1 instead of topography values, with
1 indicating that a point should be used as an fgmax point, 0 indicating it
should not be used.  This is particularly convenient if you want to select
fgmax points that are a subset of points on a DEM.  This option is described
more below under `point_style==4`.

**New in v5.7.0:** Most fgmax information is now most easily set
in `setrun.py` and is written out to the file `fgmax_grids.data`
when this script is executed, e.g. by "`make data`".   The information
required is described below.  See also :ref:`setrun_fgmax`.

This is an improved version of the algorithms used in much earlier versions of
GeoClaw, and now  
correctly interpolates when a grid point lies near the junction of two
grid patches, which was not always handled properly before.
The earlier version can still be used for outputing results at intermediate
times on a fixed grid (see :ref:`fgout`), but is not recommended for the purpose
of monitoring maxima or arrival times.  

.. _fgmax_input:

Input file specification 
-------------------------

**(Changed in Clawpack 5.7.0.)**

The GeoClaw Fortran code reads in one or more files that specify grid(s) for
monitoring values during the computation.  

The fgmax grid(s) are specified to GeoClaw in 
`setrun.py` by setting `rundata.fgmax_data.fgmax_grids`
to be a list of objects of class `fgmax_tools.FGmaxGrid`.
The order the files appear in this list determines the number assigned to
this grid (starting with 1) that may be needed for processing or plotting
the results.  The output appears in files such as `_output/fgmax0001.txt`.

**New in v5.7.0:** You can now assign numbers to each fgmax gauge
using the `fgno` attribute, described below, rather than being numbered
sequentially by order specified in the `setrun.py` file.

Currently at most 50 fgmax grids are allowed by default.  If you need more,
you can adjust the parameter `FG_MAXNUM_FGRIDS` in
`$CLAW/geoclaw/src/2d/shallow/fgmax_module.f90` and the do `make new` to
recomile everything that depends on this module.   

Each `fgmax_tools.FGmaxGrid` object (`fg`, for example)
describing a grid of points has the following attributes::

    fg.fgno
    fg.tstart_max   
    fg.tend_max  
    fg.dt_check
    fg.min_level_check
    fg.arrival_tol
    fg.interp_method
    fg.point_style
    
These are explained further below.

Additional attributes depend on the value of `fg.point_style`.

Different point styles
^^^^^^^^^^^^^^^^^^^^^^

**If `fg.point_style == 0`,** an arbitrary collection of `(x,y)` points is allowed.
In this case you can either set 

    fg.npts 
    
to the number of points and 

    fg.X
    fg.Y

to lists (or numpy arrays) of the coordinates, or you can set

    fg.npts = 0
    
and set

    fg.xy_file
    
to a string with the path to a file of the form:

    npts      # number of points
    x1 y1     # first point
    x2 y2     # second point
    ...       # etc.

These points need not lie on a regular grid and can be specified in any order.

**If `point_style == 1`,** a 1-dimensional transect of points is specified by
the attributes::

    fg.npts       # number of points to generate
    fg.x1, fg.y1     # first point
    fg.x2, fg.y2     # last point

**If `point_style == 2`,** a 2-dimensional cartesian of points is specified by
the attributes::

    fg.nx, fg.ny     # number of points in x and y  (nx by ny grid)
    fg.x1, fg.y1     # lower left corner of cartesian grid
    fg.x2, fg.y2     # upper right corner of cartesian grid

**If `point_style == 3`,** a 2-dimensional logically rectangular array
of points is specified by the attributes::

    fg.n12, fg.n23     # number of points along adjacent edges (see below)
    fg.x1, fg.y1       # first corner of grid
    fg.x2, fg.y2       # second corner of grid
    fg.x3, fg.y3       # third corner of grid
    fg.x4, fg.y4       # fourth corner of grid

The corners should define a convex quadrilateral (ordered clockwise around the
perimeter).  An array of points will be defined as the intersection points of
two sets of lines.  The first set is obtained by connecting `n12`
equally spaced points on the side from `(x1,y1)` to `(x2,y2)` with the same
number of points equally spaced on the side from `(x3,y3)` to `(x4,y4)`.
The second set of lines is obtained by connecting `n23` equally spaced
points on the side from `(x2,y2)` to `(x3,y3)` with the same 
number of points equally spaced on the side from `(x4,y4)` to `(x1,y1)` 

**If `point_style == 4`,** a file is expected that has the form of a 
topofile with `topo_type == 3` as described in :ref:`topo`.
This file has a header that describes a uniform 2d grid of points, followed
by one line for each row of the grid (moving from north to south).
Unlike a standard topofile, the values are not topography elevations,
however, but are either 1 or 0,  with the value 1 indicating that this point
should be used as an fgmax point.

Other tools are available to construct such a file by preprocessing a
topography DEM and selecting only the points that satisfy certain criteria.
For example, if we only want to capture onshore inundation depths and it is
known that regions above a certain elevation will always stay dry, then we
may want to select only points that are onshore and below this elevation.
See :ref:`marching_front` for more details and examples.

Other attributes
^^^^^^^^^^^^^^^^

The standard required attributes for any `fgmax_tools.FGmaxGrid` object are:
  
  * `fgno` : int
  
    The number of this fgmax grid, should be a positive integer with at most
    4 digits since the output file will then have the form `fgmax0001.txt`,
    for example, if `fgno = 1`.  If these are not specified then they will
    be numbered sequentially based on the order they are specified 
    in the `fgmax_grids` list.
     
  
  * `tstart_max` : float
  
    Starting time to monitor maximum.  Often we only want to monitor on the
    finest grids around the location of interest, and only after waves arrive,
    and this can be chosen correspondingly.
     
  
  * `tend_max` : float
  
    Ending time to monitor maximum.  Set to e.g. `1e9` to monitor until end
    of simulation
  
  * `dt_check` : float
  
    Time increment for monitoring maximum and arrivals.  
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
  
    But also note that if we monitor over multiple levels then we also keep
    track of what level the current maximum was computed on.  If the level
    at this point is greater than the level used for the current maximum 
    (because new finer grids were introduced since the last monitor time)
    then the old maximum is discarded and the current value as used as to
    reinitialize the maximum at this point. 
  
  * `arrival_tol` : float
  
    The time reported as the "arrival time" is the first time the value
    of the surface elevation is greater than `sea_level` + `arrival_tol`.
  
    Note that this captures the first positive wave but doesn't capture
    the time of arrival of the first wave if it is a leading depression
    rather than a positive wave.
  
  * `interp_method` : int
  
    The method to be used to interpolate from finite volume cell averages
    in GeoClaw to pointwise values at the fgmax points.
  
    The default is 0, meaning we take the value directly from the cell 
    average in the grid cell containing the fgmax point (zero-order piecewise
    constant interpolation).
  
    Setting to 1 will instead use bilinear interpolation between 4 cell 
    centers.  This is not recommended since it can give spurious results near
    the margins of the flow. See below, :ref:`fgmax_interp`.  
  


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
to 1, 2, or 5.  This value is read in from the data file `fgmax_grids.data`
and can be set by specifying the value of
`rundata.fgmax_data.num_fgmax_val` in `setrun.py`.  

.. _fgmax_interp:

Choice of interpolation procedure
---------------------------------

Before v5.7.0, the choice of interpolation procedure was governed by use of
the library routine `geoclaw/src/2d/shallow/fgmax_interpolate.f90` (for 
bilinear interpolation) or `geoclaw/src/2d/shallow/fgmax_interpolate0.f90` (for 
constant interpolation).

**Starting in v5.7.0,** there is a single library routine 
`geoclaw/src/2d/shallow/fgmax_interp.f90` and the choice is controlled by
the `fg.interp_method` parameter described above.

Setting `fg.interp_method = 0` is recommended since
interpolating the fluid depth and the topography
separately and then computing the surface elevation by adding these
may give unrealistic high values.  For example if one cell has topo `B = -2`
and `hmax = 6` (so `eta = B+hmax = 4`) and the neighboring cell has `B = 50`
and `hmax = 0` then 1D linear interpolation to the midpoint would give
`B = 24` and `hmax = 3` and hence `eta = 27` as the surface elevation at
a point that apparently gets wet, much higher than the actual surface
elevation in the wet finite volume cell.


.. _fgmax_example:

A simple example
----------------

This is taken from
`$CLAW/geoclaw/examples/tsunami/radial-ocean-island-fgmax/setrun.py`, where
other point styles are also illustrated::


    from clawpack.geoclaw import fgmax_tools

    # Points on a uniform 2d grid:
    fg = fgmax_tools.FGmaxGrid()
    fg.point_style = 2  # uniform rectangular x-y grid
    fg.x1 = 14.25
    fg.x2 = 14.65
    fg.y1 = 50.10
    fg.y2 = 50.35
    fg.dx = 15/ 3600.  # desired resolution of fgmax grid
    fg.min_level_check = amrdata.amr_levels_max # which levels to monitor max on
    fg.tstart_max = 8000.  # just before wave arrives
    fg.tend_max = 1.e10    # when to stop monitoring max values
    fg.dt_check = 20.      # how often to update max values
    fg.interp_method = 0   # 0 ==> pw const in cells, recommended
    rundata.fgmax_data.fgmax_grids.append(fg)  # written to fgmax_grids.data


.. _fgmax_processing:

Processing and plotting fgmax output
------------------------------------

After GeoClaw has run, the output directory should contain 
files of this form for each fgmax grid:

 - `fgmax0001.txt`

**Note:** This file format is new in Version 5.7.0.  Previously two files
such as `fort.FG1.valuemax` and `fort.FG1.aux1` were created to each
fgmax grid.  Now the topo value at each grid point is included along with
the max values in the single file.

If more than one fgmax grid was specified by `rundata.fgmax_data.fgmax_grids`
then there will be similar files `fgmax0002.txt`, etc.  
They will be numbered in the order they appear in the list of input files in
`setrun.py` unless you explicitly set `fg.fgno` in which case these numbers
will be used.

These files are most easily dealt with using :ref:`fgmax_tools_module` by
defining an object of class `fgmax_tools.FGmaxGrid` and using the  
class function `read_output` to read the output.  

For an example of how to process and plot the fgmax results, see the
notebook `make_input_files.ipynb` in the directory
`$CLAW/geoclaw/examples/tsunami/radial-ocean-island-fgmax`.

For some other examples, see `apps/tsunami/chile2010_fgmax` and 
`apps/tsunami/bowl_radial_fgmax` in the :ref:`apps`.   
Sample results appear in the :ref:`gallery_geoclaw`.


.. _fgmax_output_format:

Format of the output files
--------------------------

The paragraphs below describe in more detail the structure of the output files
for users who need to process them differently.

If `point_style == 0` for a grid then the points will be listed in the same
order as specified in the input file.  For other values of `point_style`
(1-dimensional transects or 2-dimensional arrays) the values will be output in
a natural order.  

In all cases the first two columns of each output file are
the longitude and latitude of the point.

The columns of `fgmax0001.txt` contain the following values, where N refers
to the number of quantities of interest being monitored, as specified
by `rundata.fgmax_data.num_fgmax_val` and described further below:

  - Column 1: longitude
  - Column 2: latitude
  - Column 3: AMR level
  - Column 4: topo value B
  - Columns 5 to 5+N: maximum value recorded of each QoI
  - Columns 6+N to 5+2N: time max value was recorded
  - Column 6+2N: arrival time

The AMR level is the level of finest level grids covering this fgmax point
at the time the maximum was recorded.  

The "topo value B" is the value of the GeoClaw topography B
interpolated to the fgmax point on this AMR level (with the method
of interpolation being specified by `fg.interp_method`, as for the values).

The value of N above is assumed to be 1, 2, or 5 in the default
routines, as specified in `setrun.py` by the value of
`rundata.fgmax_data.num_fgmax_val`. The quantities monitored are:


 - If `rundata.fgmax_data.num_fgmax_val == 1`:
    - Column 5 contains maximum value of depth `h`,
    - Column 6 contains time of maximum `h`.

 - If `rundata.fgmax_data.num_fgmax_val == 2`:
    - Column 5 contains maximum value of depth `h`,
    - Column 6 contains maximum value of speed,
    - Column 7 contains time of maximum `h`,
    - Column 8 contains time of maximum speed.

 - If `rundata.fgmax_data.num_fgmax_val == 5`:
    - Columns 5,6,7,8,9 contain maximum value depth, speed, momentum, momentum
      flux, and `hmin`, respectively,
    - Columns 10,11,12,13,14 contain times the maximum was recorded, for each
      value above.


The **last** column of `fgmax0001.txt` contains the arrival time of the wave
at this grid point, as determined by the tolerance `arrival_tol` specified in
the input file.  The time reported as the "arrival time" is the first time the
value of the surface elevation is greater than `sea_level` + `arrival_tol`.
Points where this value is `-0.99999000E+99` never met this criterion, perhaps
because the point was never inundated.  

