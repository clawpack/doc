
.. _nearshore_interp:

=======================
Nearshore interpolation
=======================

Several Fortran routines in GeoClaw interpolate from the computational grids
to other specified points where output is desired
(typically using the finest AMR resolution available nearby at each desired
output time).  This includes:

- Gauge output (time series at specified locations), see :ref:`gauges`,
- `fgmax grids` (maximum of various quantities over the entire simulation at
  specified locations), see :ref:`fgmax`,
- `fgout grids` (output of various quantities on a fixed spatial grid at a 
  sequence of times), see :ref:`fgout`.

If the specified location is exactly at the center of a computational cell
at the finest AMR level present, then the value output is simply that cell
value (which in a finite volume method is really a cell average of the
quantity over the cell, but approximates the cell center value to 
:math:`O(\Delta x^2)` if the quantity is smoothly varying.

In general, however, the specified points may not lie at cell centers.  In
all the cases listed above, the default behavior is to use "zero-order
extrapolation" to determine the value at the point, meaning that the value
throughout each computational cell is approximated by a constant function
(zero degree polynomial) with value equal to the cell average.  Hence the
value that is output at any specified point is simply the cell average of
the (finest level) grid cell that the point lies within. 

One might think that a better approximation to the value at a point could be
obtained by using piecewise bilinear approximation (in two
dimensions):  Determine what set of four grid centers the point lies within
and construct the bilinear function :math:`a_0 + a_1x + a_2y + a_3xy`
that interpolates at these four points, and then evaluate the bilinear
interpolant at the point of interest.    If the function being approximated
were smooth then this would be expected to provide an :math:`O(\Delta x^2)`
approximation, whereas zero-order extrapolation is only :math:`O(\Delta x)`
accurate.

For GeoClaw simulations, however, we have found that it is best to use
zero-order extrapolation because piecewise bilinear interpolation can cause
problems and misleading results near the coastline, which is often the
region of greatest interest.

The problem is that interpolating the fluid depth `h` and the topography `B`
separately and then computing the surface elevation `eta` by adding these
may give unrealistic high values.  For example if one cell has topo `B = -2`
and `h = 6` (so `eta = B+h = 4`) and the neighboring cell has `B = 50`
and `h = 0`, so that `eta = B+h = 50`. In the latter case, the elevation
`eta` is simply the elevation of the land and this point is not wet, as
indicated by the fact that `h=0`.  But now if we use linear interpolation
(in 1D for this simple example) to the midpoint between these points,
interpolating the topography gives 
`B = 24` and interpolating the depth gives `h = 3`.
Hence we compute `eta = B+h = 27` as the surface elevation.
Since the point is apparently wet (`h > 0`), one might conclude that the sea
surface at this point is 27 meters above the initial sea level, whereas in
fact the sea level is never more than 6 meters above sea level. 

