
.. _netcdf_utils_module:

netcdf_utils module for NetCDF input
=====================================

.. seealso::
   - :ref:`netcdf_input`
   - :ref:`topotools_module`
   - :ref:`storm_module`

The ``netcdf_utils`` module provides the Python layer for reading NetCDF
topography and meteorological forcing files in GeoClaw.  It handles CF
attribute parsing, coordinate convention detection, unit resolution
(recognized non-contract units are converted via a scale factor; missing or
unrecognized units raise), and descriptor writing so that Fortran only needs
to open the file and read pre-validated indices.

The main classes are:

- :class:`~clawpack.geoclaw.netcdf_utils.NetCDFInspector` — base class;
  coordinate discovery, fill-value resolution, crop-bound validation.
- :class:`~clawpack.geoclaw.netcdf_utils.TopoInspector` — topography
  subclass; fill-value checking within the crop region, unit enforcement.
- :class:`~clawpack.geoclaw.netcdf_utils.MetInspector` — meteorological
  subclass; wind/pressure variable discovery, CF datetime decoding, unit
  resolution (recognized non-contract units converted, with a storm-format
  fallback for missing units; unrecognized units raise), and a magnitude
  sanity check.
- :class:`~clawpack.geoclaw.netcdf_utils.CFNormalizer` — adds or repairs
  CF attributes in place without modifying data values.
- :class:`~clawpack.geoclaw.netcdf_utils.DescriptorWriter` — writes the
  key=value topo descriptor lines or the ``&file_info`` / ``&variable_info``
  Fortran namelist blocks for met forcing.

Documentation auto-generated from the module docstrings
--------------------------------------------------------

.. automodule:: clawpack.geoclaw.netcdf_utils
   :members:
   :undoc-members:
   :show-inheritance:
