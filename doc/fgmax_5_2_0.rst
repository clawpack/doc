
.. _fgmax_5_2_0:

=====================
Fixed grid monitoring
=====================

.. warning::

   This feature has been modified and this documentation describes 
   the version introduced in 5.2.0.
   The documentation is also still incomplete.

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
following a coastline, for example.

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

The input file describing a grid of points has the following form::

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
three lines of the form::

    npts       # number of points to generate
    x1, y1     # first point
    x2, y2     # last point

If `point_style == 2`, a 2-dimensional cartesian of points is specified by
three lines of the form::

    nx, ny     # number of points in x and y  (nx by ny grid)
    x1, y1     # lower left corner of cartesian grid
    x2, y2     # upper right corner of cartesian grid

The output files will list values for the points in the same order as in the
input file.  See `fgmax_processing` for some hints on processing and
plotting the results.

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
the minimum depth at each point).  

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

An alternative version of this routine has been added in 5.2.0
that does piecewise constant interpolation instead. This simply uses the
value in the finite volume grid cell that contains the fixed grid
point (0 order extrapolation) and avoids problems sometimes seen when
doing linear interpolation near the margins of the flow.

This routine is in `fgmax_interpolate0.f90` and is now recommended.  
To use this routine, modify the `Makefile` in an application directory to
replace the line ::

      $(GEOLIB)/fgmax_interpolate.f90 \

by ::

      $(GEOLIB)/fgmax_interpolate0.f90 \


    

.. _fgmax_processing:

Processing and plotting fgmax output
------------------------------------
 
For an example see `apps/tsunami/chile2010_fgmax` in the :ref:`apps`.   
    

**Describe further.**

