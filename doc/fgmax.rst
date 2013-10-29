
.. _fgmax:

=====================
Fixed grid monitoring
=====================

.. warning::

   This feature is still under development and should be used with caution.
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

The input file describing a grid of points has the following form::

    tstart_max  
    tend_max
    dt_check
    min_level_check
    arrival_tol
    npts
    x1 y1
    x2 y2
    ...

with a total of 'npts' pairs of x-y coordinates specified.  These points
need not line on a regular grid and can be specified in any order.

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
`$CLAW/geoclaw/src/2d/shallow/fgmax_values.f90` monitors a single value
defined roughly to be the surface elevation `h + B` in wet cells and some
large negative number in dry cells.  

**Describe this better.**
    

.. _fgmax_processing:

Processing and plotting fgmax output
------------------------------------
 
For an example see `apps/tsunami/chile2010_fgmax` in the :ref:`apps`.   
    

**Describe further.**

