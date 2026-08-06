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



Copied from :ref:`changes_to_master`
====================================


- **Topography preprocessing attributes.**
  :class:`~clawpack.geoclaw.topotools.Topography` now supports seven
  preprocessing attributes (``crop_extent``, ``coarsen``, ``buffer``,
  ``align``, ``x_shift``, ``z_shift``, ``negate_z``) that are applied
  automatically when :meth:`~clawpack.geoclaw.topotools.Topography.read`
  loads a file.  See :ref:`setrun_topo_preprocessing` for the full table
  and :ref:`topotools` for usage examples and operation order.

- **CF-aware NetCDF reading.**
  NetCDF topography files (``topo_type=4``) are now read via
  :class:`~clawpack.geoclaw.netcdf_utils.TopoInspector`, which auto-detects
  coordinate variable names using CF conventions (``standard_name``, ``axis``,
  and common fallback names).  Files with non-standard coordinate names and
  non-standard dimension orders are handled automatically.
  :meth:`~clawpack.geoclaw.topotools.Topography.read_header` also uses CF
  detection for type-4 files, enabling a lazy-load pattern where coordinates
  are available without loading the elevation array.
  See :ref:`topotools` for an example.

- **Python-owned priority ordering.**
  Topography files in ``topo.data`` are now sorted entirely in Python by
  :meth:`~clawpack.geoclaw.data.TopographyData._compute_priority_order`
  before writing.  Files are written coarsest-first (finest last), matching
  the traditional GeoClaw listing order; the last file listed in ``topo.data``
  is assigned rank 1 (highest priority) by Fortran, with no Fortran-side
  sorting.  ``rundata.topo_data.override_order = True`` preserves
  user-specified list order; when used, the finest (highest-resolution) file
  should be listed last.  See :ref:`topo_order`.

- **topo_type=1 deprecated.**
  Reading and writing ``topo_type=1`` (``x y z`` one-point-per-line ASCII)
  now emit a ``DeprecationWarning``.  Setting any preprocessing attribute
  before reading a type-1 file raises ``NotImplementedError``.  To convert::

      topo = Topography()
      topo.read('old.tt1', topo_type=1)   # gives DeprecationWarning
      topo.write('new.tt2', topo_type=2)

- **New** ``topo.data`` **format.**
  Each per-file block in ``topo.data`` now contains 9 lines (up from 2),
  recording all preprocessing attributes.  See :ref:`topodata_format` for
  the complete format specification.

- **dtopo NetCDF (**\ ``dtopo_type=4``\ **).**
  :class:`~clawpack.geoclaw.dtopotools.DTopography` reads and writes
  CF-compliant NetCDF dtopo files.  The optional ``time_reference`` attribute
  selects a CF datetime time axis (``units = "seconds since <ref>"``) that a
  plain ``xarray.open_dataset`` decodes to ``datetime64``; without it a bare
  ``units = "seconds"`` (simulation-relative) axis is written.  The reader
  scales the time axis by its CF ``units``, fixing an earlier bug where a
  ``"hours"``/``"minutes"`` axis was misread as seconds.  See
  :ref:`netcdf_input` and :ref:`dtopo_formats`.

- **NetCDF write dtype control.**
  ``Topography.write(topo_type=4, z_dtype=...)`` and
  ``DTopography.write(dtopo_type=4, dz_dtype=...)`` override the on-disk
  elevation/deformation dtype (default ``"float32"``; pass ``"float64"`` for
  full double precision).

- **Robust NetCDF file opening.**
  A NetCDF backend engine is now selected explicitly, so a valid file opens
  even when its name uses a non-standard extension (e.g. ``.dtt3``) that
  xarray's extension-based engine guessing would not recognize.
