

.. _grid_registration:

*****************************************************************
Grid registration
*****************************************************************

.. seealso::
   - :ref:`topo`
   - :ref:`topotools`


GeoClaw `topo_type == 3` is
essentially the same as the `ESRI ASCII Raster format <http://resources.esri.com/help/9.3/arcgisengine/java/GP_ToolRef/spatial_analyst_tools/esri_ascii_raster_format.htm>`_
but it is important to note which grid registration is used.
(`topo_type == 2` uses the same header conventions, so this discussion also
applies to these files.)

See `this NOAA page <https://www.ngdc.noaa.gov/mgg/global/gridregistration.html>`_
and `the wikipedia ESRI grid page <https://en.wikipedia.org/wiki/Esri_grid>`_
for more about registration, with some useful figures.

The third and fourth lines of the header file contain labels that tell whether the
registration is `llcorner` (lower left corner) or `llcenter` (lower left center).
GeoClaw also recognizes `lower`, which is currently handled in a way 
equivalent to `llcenter`.  This is also the assumed default registration 
if the string is not one of these recognized values.

According to the documentation linked above for ESRI raster format, the topography
data given in the file should be viewed as **cell averages** of the topography over
DEM cells of dimension `dx` by `dy` where in this format `dx = dy` and is given by the
`cellsize` parameter. (We use DEM cell to denote the cell in the Digital Elevation
Model provided in the topofile, not be be confused with the computational grid
cells used by the finite volume method.)   

The **registration**
indicates whether the `(x,y)` (longitude, latitude) value given in the header
corresponds to the location of the lower left corner of the SW-most DEM cell, or to the
center of this cell.  Using the example from :ref:`topo`, a file containing::


      2         mx
      2         my
      0.        xllcenter
      20.       yllcenter
      10.       cellsize
      -9999     nodatavalue
      -1000.  -2000.
      -3000.  -4000.

would specify DEM cells with centers at `(0,30), (10,30), (0,20), (10,20)`, which
are the same points specified in the `topo_type == 1` example on :ref:`topo`.

By contrast, the file::

      2         mx
      2         my
      0.        xllcorner
      20.       yllcorner
      10.       cellsize
      -9999     nodatavalue
      -1000.  -2000.
      -3000.  -4000.

would specify DEM cells with lower left corners at the 4 points listed above, and
hence cell centers at `(5,35), (15,35), (5,25), (15,25)`.

In the GeoClaw Fortran code, we assume the DEM values are actually
pointwise values and these are used to construct a piecewise bilinear
function interpolating these values.  This function is then integrated
over the computational grid cells in order to get the
cell-averaged topography values that are stored in `aux(1,:,:)` and
used in the finite volume method.  The computational cells over
which this function is integrated can vary as adaptive refinement is performed.

If the topography is smoothly varying, then the cell average over a DEM cell
agrees with the pointwise value at the cell center, so for our purpose
it is best to view the DEM values as being located at cell centers.  Hence if
`llcorner` registration is specified, the lower left corner (and all other `(x,y)`
points spaced according to `cellsize`) should all be shifted by `cellsize/2` in
both `x` and `y` before being used.

Starting with Version 5.5.0, this is done in the Fortran code when the DEM topofile
is read in.  It is also done in the Python `topotools` module at the time of
reading the file, so the internal representation has `Topography.x` and
`Topography.y` corresponding to the cell centers or points where the data should be
interpreted in a pointwise view.  This is also best when producing contour plots,
for example.   When writing a topography file using `Topography.write()`, a new
optional argument `grid_registration` has been added.  The `(x,y)` values in the
header will be printed properly based on the registration chosen.

Note that if you use `Topography.crop()` with a `coarsen` parameter
in order to generate a coarser version of the DEM, this simply
subsamples the topography.  This followed by `Topography.write()`
should print out the proper `llcorner` or `llcenter` value for the
coarsened topography based on the location of the subsamples, but
`crop()` does not currently average topography over large cells as
the ESRI standard suggests should be done.  In the future a
`coarsen_method` parameter might be added to `crop()` to allow this.

Earlier versions of GeoClaw always viewed the `(x,y)` value in the header as the
location of the SW-most data point, i.e., always assumed `llcenter == lower`
registration.  So if you rerun a previous example that had a topofile specifying
`llcorner` in the header, the results may change since the DEM data will now be (more
properly) viewed as specified at slightly different points.  If you need to try to
reproduce your earlier results, you could change `llcorner` to `lower` in the
header lines, for example.

For GeoClaw `topo_type=1`, each row contains `x, y, z` data for a single
point and we interpret `z` as the pointwise data at the specified `x, y`.

NetCDF files
------------

For netCDF files the
data points are generally interpreted as pointwise values at the points
specified in the `lat` and `lon` arrays included in the file (or as
cell-averaged values with these points as the cell centers).

