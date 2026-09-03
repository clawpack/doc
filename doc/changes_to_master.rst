:orphan:

.. _changes_to_master:

===============================
Changes to master since v5.14.0
===============================


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.14.0) on January 26, 2026.

These changes should appear in the next release.  If you need them now,
see :ref:`developers` for instructions on cloning and installing from the
master branch. 

To see documentation that has already been developed to accompany any new
features listed below, click on the "dev" branch of the documentation, in
the menu on the left hand side of this page.

Changes that are not backward compatible
----------------------------------------

- **NetCDF input units are now required, and recognized units are converted
  automatically (geoclaw).**  NetCDF input variables must declare a CF
  ``units`` attribute.  A variable already in the contract unit (topo/dtopo
  ``m``, wind ``m/s``, pressure ``Pa``) passes through unchanged; a
  *recognized* non-contract unit (e.g. ``km``/``cm``, ``hPa``/``mbar``,
  ``knots``, or a ``"hours since ..."`` time axis) is now **converted
  automatically** -- Python resolves it to a multiplicative scale factor that
  Fortran applies on read.  A **missing** ``units`` attribute or an
  **unrecognized** unit still raises a ``ValueError`` rather than being
  silently misread (met forcing falls back to the storm format's documented
  unit when the attribute is absent, e.g. NWS13/OWI pressure ``mbar``).  Pass
  ``assume_units`` (``TopoInspector`` / ``Topography.read`` via ``nc_params``,
  or ``MetInspector(assume_units=True)``) for a file that omits the attribute.
  A resolved field is also magnitude-checked: a pressure field mislabeled
  ``Pa`` but really ``hPa``/``mbar`` is auto-corrected with a warning, and a
  physically implausible field raises (bypass with ``skip_sanity_check``).
  Met NetCDF forcing requires a CF *absolute* datetime time axis; a bare
  numeric time axis with no reference date is rejected.  See
  :ref:`netcdf_input`.


General changes
---------------


Changes to classic
------------------


See `classic diffs
<https://github.com/clawpack/classic/compare/v5.14.0...master>`_

Changes to clawutil
-------------------


See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.14.0...master>`_

Changes to visclaw
------------------

 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.14.0...master>`_

Changes to riemann
------------------


See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.14.0...master>`_

Changes to amrclaw
------------------


See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.14.0...master>`_

Changes to geoclaw
------------------

- **Overview of changes related to topo and dtopo files**
  See :ref:`topochanges`.

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

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.14.0...master>`_


Changes to PyClaw
------------------


See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.14.0...master>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.14.0...master>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.13.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.14.0...master>`_
