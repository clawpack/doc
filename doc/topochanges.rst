.. _topochanges:

*****************************************************************
Changes to topo and dtopo handling (planned for v5.15.0)
*****************************************************************

Many changes are being implemented in the way topo and dtopo
files are handled, in both the Python tools and the Fortran code.

.. warning :: Some of this work is still being debugged and code
   on the master branch may not work as advertised.  Interfaces
   and parameter names are still evolving.  Please test this code
   but be aware of these warnings.

.. seealso::
   - :ref:`topotools`
   - :ref:`topodata_format`
   - :ref:`netcdf_input`
   - :ref:`topotools`
   - :ref:`topo_order`
   - :ref:`dtopo`
   - :ref:`dtopotools`

Major changes to topo file handling
===================================

Cropping and coarsening or minor adjustments to a topo DEM
----------------------------------------------------------

In the Fortran GeoClaw code, rather than specifying a list of
topo files in `setrun.py`, we now list a set of topo grids. 
Each topography grid comes from a particular file, but has
additional parameters indicating if the DEM in the file should
be cropped or coarsened to create the topo grid (along with
other options, such as shifting the longitude by 360 degrees
or shifting the values vertically).  

This has several advantages:

- A single large topo DEM can be dynamically cropped and coarsened
  as needed, rather than potentially needing to make many smaller
  files with different extents or resolutions.  The same DEM can
  be used multiple times in the `setrun.py` to specify different
  topo grids with different extents and coarsening factors, if
  desired.

- If the same topo file is needed sometimes in latitude W (e.g.
  in modeling a nearfield tsunami on the US West Coast) and sometimes
  in longitude E (e.g. when modeling a farfield tsunami from Japan),
  you no longer need two versions of the large file with only one
  change in the header.

See :ref:`setrun_topo_preprocessing` for a full attribute table with types
and defaults, and non-obvious behavior notes.

NetCDF file handling
--------------------

Improvements have also been made in how netCDF files are used
in both Python and Fortran.  See :ref:`netcdf_input`.



Ordering of topo DEM priorities
-------------------------------

When creating grid cell topo values, normally the topo grids specified
are used with the finest available grid having highest priority.
However, this can be over-ridden as is sometime necessary as described
in :ref:`topo_order`.  Previously the ordering was figured out in the
Fortran code. Now the ordering is figured out in Python, in the process
of generating `topo.data` from `setrun.py`, and the order the grids
are listed in `topo.data` is exactly the order that will be used in
the Fortran code. This should make it easier for the user to confirm
the desired ordering is being used.


Major changes to dtopo file handling
====================================

NetCDF file handling
--------------------

Improvements have also been made in how netCDF files are used
in both Python and Fortran.  See :ref:`netcdf_input`.

