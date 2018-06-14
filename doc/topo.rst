

.. _topo:

*****************************************************************
Topography data
*****************************************************************

.. seealso::
   - :ref:`topotools`
   - :ref:`grid_registration`
   - :ref:`tsunamidata`

The :ref:`geoclaw` software for flow over topography requires at least one
topo file to be input, see :ref:`setrun_geoclaw`.

Currently topo files are restricted to three possible formats as ASCII files, or
NetCDF files are also allowed.

In the descriptions below it is assumed that the topo file gives the
elevation of the topography (relative to some reference level) as a value of
z at each (x,y) point on a rectangular grid.  Only uniformly spaced
rectangular topo grids are currently recognized.  

More than one topo file can be specified (see :ref:`setrun_topo`) that might
cover overlapping regions at different resolutions.  The union of all the
topo files should cover the full computational domain specified (and may
extend outside it).  Internally in :ref:`geoclaw` a single
piecewise-bilinear function is constructed from the union of the topo files,
using the best information available in regions of overlap.  This function
is then integrated over computational grid cells to obtain the single topo value
in each grid cell needed when solving depth averaged equations such as the
shallow water equations with these finite volume methods.  Note that this
has the feature that if a grid cell is refined at some stage in the
computation, the topo used in the fine cells have an average value that is
equal to the coarse cell value.  This is crucial in maintaining the
ocean-at-rest steady state, for example.

.. warning:: Some changes were made in version 5.5.0 that affect how
   topofiles with `topo_type in [2,3]` 
   are interpreted for files with a header specifying
   `xllcorner` and `yllcorner`.  
   This may cause computed results to differ from previous results using
   the same topofiles if the header contains this specification.
   See :ref:`grid_registration` for more details on this `llcorner`
   registration.
   The description below has been modified to use `lower` registration,
   equivalent to `llcenter` registration.

The recognized topotypes are:

  **topotype = 1**

    x,y,z values on each line, progressing from upper left (NW) corner across
    rows (moving east), then down in standard GIS form.  
    The size of the grid and spacing
    between the grid points is deduced from the data.  

    *Example:* The data below would be used in the GeoClaw code
    to define a bilinear function
    over the domain  0. <= x <= 10. and  20. <= y <= 30.
    that decreases (deeper water) as you move to the east or to the south::

            0.  30.  -1000.
            10. 30.  -2000.
            0.  20.  -3000.
            10. 20.  -4000.

    These files are larger than necessary since they store the x,y values at
    each point even though the points are required to be equally spaced.
    Many data sets come this way, but note that you can convert a file of
    this type to one of the more compact types below using::
    
        [insert python code]



  **topotype = 2**

    The file starts with a header consisting of 6 lines containing::

      XXX  mx
      XXX  my
      XXX  xlower | xllcenter | xllcorner
      XXX  ylower | yllcenter | yllcorner
      XXX  cellsize
      XXX  nodataval

    and is followed by mx*my lines containing the z values at each x,y,
    again progressing from upper left (NW) corner across
    rows (moving east), then down in standard GIS form.  
    The lower left corner of the grid
    is *(xlower, ylower)* and the distance between grid points in both
    x and y is *cellsize*.  The value *nodataval* indicates what value of z
    is specified for missing data points (often something like -9999 in data
    sets with missing values).

    Note: 

     - The value `XXX` and the label (e.g. `xlower`) can appear in
       either order in each of the header lines.  
     - the `cellsize` line can include two values `dx, dy` rather than a single
       value, in case the spacing is different in `x` and `y`.

    *Example:*  For the same example as above, the topo file with
    topotype==2 and `lower` registration would be::

      2         mx
      2         my
      0.        xlower
      20.       ylower
      10.       cellsize
      -9999     nodatavalue
      -1000.
      -2000.
      -3000.
      -4000.

    This file would be interpreted the same way if `llcenter` registration
    was specified on lines 3 and 4, but differently if `llcorner`
    was specified -- see :ref:`grid_registration`.

  **topotype = 3**

    The file starts with a header consisting of 6 lines as for *topotype=2*,
    followed by *my* lines, each containing *mx* values for one row of data
    (ordered as before, so the first line of data is the northernmost line
    of data, going from west to east).

    *Example:*  For the same example as above, the topo file with
    topotype==3 and `lower` registration would be::

      2         mx
      2         my
      0.        xlower
      20.       ylower
      10.       cellsize
      -9999     nodatavalue
      -1000.  -2000.
      -3000.  -4000.

    This file would be interpreted the same way if `llcenter` registration
    was specified on lines 3 and 4, but differently if `llcorner`
    was specified -- see :ref:`grid_registration`.

    Note: 

     - The value `XXX` and the label (e.g. `xlower`) can appear in
       either order in each of the header lines.  
     - the `cellsize` line can include two values `dx, dy` rather than a single
       value, in case the spacing is different in `x` and `y`.

    This is essentially the same as the `ESRI ASCII Raster format
    <http://resources.esri.com/help/9.3/arcgisengine/java/GP_ToolRef/spatial_analyst_tools/esri_ascii_raster_format.htm>`_,
    but it is important to note which grid registration is used.
    NCEI and etopo1 data sets generally have this format with `llcorner`
    registration!  See :ref:`grid_registration` for more details.

  **topotype = 4**

    This file type is not ASCII but rather in a NetCDF4 format supported by the
    `CF MetaData conventions (v. 1.6) <http://cfconventions.org>`_. Files 
    that conform to this standard can be read in by GeoClaw.  The `topotools`
    module also has support for reading and writing (including therefore 
    conversion) of these types of bathymetry files (see :ref:`topo_netcdf`
    below).  To use this functionality
    you will need to add *-DNETCDF* to the *FFLAGS* variable either by the
    command line or in the Makefile.

The Fortran code will recognize headers for *topotype* 2
or 3 that have the labels first and then the parameter values.  
The order of lines is important.

It is also possible to specify values -1, -2, or -3 for *topotype*, in which
case the *z* values will be negated as they are read in (since some data
sets use different convensions for positive and negative values relative to
sea level). 

For :ref:`geoclaw` applications in the ocean or lakes (such as tsunami
modeling), it is generally assumed that *sea_level = 0* has been set in
:ref:`setrun_geoclaw` and that *z<0* corresponds to subsurface bathymetry
and *z>0* to topograpy above sea level.

.. _topo_sources:

Downloading topography files
----------------------------

The example
`$CLAW/examples/tsunami/chile2010
<claw/examples/tsunami/chile2010/README.html>`_
is set up to automatically download topo files via::

	$ make topo

See the `maketopo.py` file in that directory.

Other such examples will appear in the future.  

Several on-line databases are available for topograpy, see 
:ref:`tsunamidata` for some links.

Some Python tools for working with topography files are available, see
:ref:`topotools`.

.. _topo_netcdf:

NetCDF format
^^^^^^^^^^^^^

Topofiles can be read in netCDF format, either from local `.nc` files or
from some online databases that provide netCDF servers, e.g. the NOAA
THREDDS server.  Use the 
`topotools.read_netcdf <topotools_module.html#clawpack.geoclaw.topotools.read_netcdf>`_
function.  Note that this also allows reading in only a subset of the data,
both limiting the extent and the resolution, e.g. by sampling every other
point (by setting `coarsen=2`). This is particularly useful if you only want
a subset of a huge online netCDF file (e.g. coastal DEMs at 1/3 arcsecond
resolution are typically several gigabytes).

The dictionary `topotools.remote_topo_urls` contains some useful URLs for
etopo1 and a few other NOAA THREDDS datasets. This allows reading etopo1
data, for example, via::

    >>> from clawpack.geoclaw import topotools
    >>> topo1 = topotools.read_netcdf('etopo1',...)

See `$CLAW/geoclaw/tests/test_etopo1.py` for one example, in which a very
small patch from the global etopo1 database (which has 1 arcminute resolution)
is downloaded at different resolutions.

**Note:** Earlier versions of clawpack included `etopotools.py` providing a
different way to download subsampled etopo1 topography.  That has been
deprecated since the old way is no longer supported by NOAA and did not
always do the subsampling properly.

See also :ref:`grid_registration` for important information about the manner
in which the data downloaded should be interpreted.  For netCDF files the
data points are generally interpreted as pointwise values at the points
specified in the `lat` and `lon` arrays included in the file (or as
cell-averaged values with these points as the cell centers).

.. _topo_dtopo:

Topography displacement files
-----------------------------


For tsunami generation a file *dtopo* is generally used to specify the
displacement of the topography relative to that specified in the topo files.

Currently two formats are supported for this file: 

    **dtopotype=1:** 

    Similar to
    topo files with *topotype=1* as described above, except that each line
    starts with a *t* value for the time, so each line contains t,x,y,dz

    The x,y,dz values give the displacement dz at x,y at time t.  It is assumed
    that the grid is uniform and that the file contains mx*my*mt lines if mt
    different times are specified for an mx*my grid.  

    **dtopotype=3:** 

    Similar to
    topo files with *topotype=3* as described above, but the header is
    different, and contains lines specifying *mx, my, mt, xlower, ylower, t0,
    dx, dy*, and *dt*.  These are followed by *mt* sets of *my* lines, 
    each line containing *mx* values of *dz*.

The Okada model can be used to generate *dtopo* files from fault parameters,
as described in :ref:`okada`. 

Note that if the topography is moving, it is important to insure that the
time step is small enough to capture the motion.  Starting in Version 5.1.0,
there is a new parameter that can be specified in `setrun.py`
to limit the size time step used during the time when topography is moving. 
See :ref:`setrun_topo`.

.. _qinit_file:

qinit data file
---------------

Instead of (or in addition to) specifying a displacement of the topography
it is possible to specify a perturbation to the depth, momentum, or surface
elevation of the initial data.  This is generally useful only for tsunami
modeling where the initial data specified in the default *qinit.f90* function
is the stationary water with surface elevation equal to *sea_level* as set in
`setrun.py` (see :ref:`setrun_geoclaw`).  

Of course it is possible to copy the *qinit.f90* function to your
directory and modify it, but for some applications the initial elevation may
be given on grid of the same type as described above.  In this case file can
be provided as described at :ref:`setrun_qinit` containing this
perturbation.

The file format is similar to what is described above for *topotype=1*, but
now each line contains *x,y,dq* where *dq* is a perturbation to one of the 
components of *q* as specified by the value of *iqinit* specified (see
:ref:`setrun_qinit`).  If *iqinit = 4*, the value *dq* is instead the
surface elevation desired for the initial data and the depth *h* (first
component of *q*) is set accordingly.

