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

      t = Topography()
      t.read('old.tt1', topo_type=1)   # DeprecationWarning
      t.write('new.tt2', topo_type=2)

- **New** ``topo.data`` **format.**
  Each per-file block in ``topo.data`` now contains 9 lines (up from 2),
  recording all preprocessing attributes.  See :ref:`topodata_format` for
  the complete format specification.

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
