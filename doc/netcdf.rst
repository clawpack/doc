.. toctree::
   :maxdepth: 2

   user_guide
   developer_reference
   descriptor_format
   unit_contract
   coordinate_normalization
   technical_debt
   adding_met_field
   test_structure
   next_steps

.. _netcdf_input:

GeoClaw NetCDF Input System
===========================

This document covers the NetCDF input pipeline introduced in the
``refactor-netcdf-support`` PR (VERSION ?5.15?). It has two sections: a user
guide for scientists who want to use NetCDF files as input, and a developer
reference for those working on the implementation.

--------------

User Guide
----------

Topography from NetCDF
~~~~~~~~~~~~~~~~~~~~~~

GeoClaw can read topography/bathymetry directly from a NetCDF file
(``topo_type=4``). The file must contain a 2D elevation variable on a
regular latitude/longitude grid. Common sources include GEBCO, ETOPO,
NOAA coastal DEMs, and any file produced by standard GIS tools.

What GeoClaw handles automatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Longitude conventions: both [-180, 180] and [0, 360] are detected and
   normalized at runtime. You do not need to preprocess the file.
-  Latitude ordering: both S-to-N and N-to-S are handled correctly.
-  Dimension ordering: ``(lat, lon)`` and ``(lon, lat)`` are both
   supported.
-  Fill values: ``_FillValue`` and ``missing_value`` attributes are
   resolved automatically. If a fill value is found within your
   simulation domain, GeoClaw will abort with an error -- this is
   intentional, as missing bathymetry is a silent correctness hazard.

What your file must provide
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  A 2D variable containing elevation in **meters** (positive up,
   negative for ocean). If your file uses feet or another unit, use
   ``CFNormalizer`` to convert before running (see below).
-  1D coordinate variables for latitude and longitude with recognizable
   names (``lat``/``latitude``/``y`` and ``lon``/``longitude``/``x`` are
   all detected). Curvilinear (2D coordinate) grids are not currently
   supported for topography.

Registering a NetCDF topo file in setrun.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your file meets the above requirements, you can simply use the following in
``setrun.py``:

.. code:: python

   rundata.topo_data.topofiles.append([4, 'bathy.nc'])

This matches with what is expected for backwards compatibility.

If you want to specify crop bounds, or if GeoClaw cannot find the elevation
variable automatically, use ``topo_entries()`` to interrogate the file:

.. code:: python

   from clawpack.geoclaw.netcdf_utils import TopoInterrogator
   with TopoInterrogator('bathy.nc', crop_bounds=(-100, -60, 15, 35)) as intr:
       rundata.topo_data.topofiles.extend(intr.topo_entries())

``topo_entries()`` returns a list of ``[4, path, TopoMetadata]`` entries ready
to pass directly to ``topofiles``.  In the common case the list has one entry,
but it may contain two when the crop region straddles the file's longitude cut
point (e.g. a global file cropped across the dateline) — ``extend`` handles
both cases without extra logic.  GeoClaw's Python layer writes the necessary
descriptor information into ``topo.data`` automatically.

The elevation variable is found automatically using a two-step search:

1. **CF** ``standard_name`` **attribute** — variables whose ``standard_name``
   is one of ``surface_altitude``, ``height_above_mean_sea_level``,
   ``height_above_reference_ellipsoid``, ``bedrock_altitude``, ``altitude``,
   ``height``, or ``sea_floor_depth_below_geoid`` are matched first.
2. **Common variable names** — if no CF match is found, the variable name is
   checked against a built-in list that includes ``z``, ``elevation``,
   ``topo``, ``height``, ``altitude``, ``depth``, ``dem``, ``bathymetry``,
   ``bathy``, ``Band1``, and several capitalisation variants.

Pass ``var_name`` explicitly only when none of the names above match your file,
or when the file contains multiple variables that would both match and you need
to disambiguate::

   meta = TopoInterrogator('bathy.nc', var_name='my_elevation',
                           crop_bounds=(-100, -60, 15, 35)).interrogate_topo()

Coordinate names (``lon``/``latitude``/``x`` etc.) and dimension ordering are
always discovered automatically and never need to be specified.

Domain subsetting (crop)
^^^^^^^^^^^^^^^^^^^^^^^^

If your NetCDF file covers a larger area than your simulation domain
(common with global or regional datasets), pass ``crop_bounds`` to
``TopoInterrogator`` and use ``topo_entries()`` to register the file:

.. code:: python

   from clawpack.geoclaw.netcdf_utils import TopoInterrogator
   with TopoInterrogator('gebco_global.nc',
                         crop_bounds=(-100, -80, 20, 35)) as intr:
       rundata.topo_data.topofiles.extend(intr.topo_entries())

Only the subset is read into memory at runtime. The full file is never
loaded.

Checking CF compliance
^^^^^^^^^^^^^^^^^^^^^^

If you are unsure whether your file will be read correctly, the
``CFNormalizer`` utility can inspect and repair common issues:

.. code:: python

   from clawpack.geoclaw.netcdf_utils import CFNormalizer

   cf = CFNormalizer('path/to/bathymetry.nc')
   cf.report()          # prints any issues found
   cf.normalize('path/to/bathymetry_cf.nc')  # writes a corrected copy

``CFNormalizer`` adds missing ``standard_name``, ``axis``, and ``units``
attributes, and resolves ``_FillValue``/``missing_value`` conflicts. It
does not resample or reproject.

--------------

Storm surge met forcing from NetCDF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For storm surge simulations using full gridded met forcing (wind and
pressure fields), GeoClaw can read directly from a NetCDF file. This
replaces the need to convert to OWI ASCII format.

Supported source formats:

- **ERA5** (ECMWF reanalysis): detected automatically from CF attributes
- **NWS13** (OWI NetCDF): detected automatically
- **Generic CF-compliant NetCDF**: requires variable name mapping if
  names are non-standard

Not yet supported: raw WRF output (requires preprocessing due to
curvilinear grid and string-encoded time axis).

Required variables and units
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

GeoClaw expects the following in the NetCDF file **after any unit
conversion** (conversion happens automatically during Python
preprocessing):

============================= ================================
Variable                      Unit
============================= ================================
Wind (u-component, eastward)  m/s
Wind (v-component, northward) m/s
Surface pressure              Pa
Time                          seconds from user-defined offset
============================= ================================

If your file uses hPa/mbar for pressure or knots for wind,
``MetInterrogator`` will convert automatically.

Registering a NetCDF storm file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``setrun.py``:

.. code:: python

   surge_data.storm_specification_type = 'data'
   surge_data.storm_file = 'isaac.storm'

Then create the storm descriptor file, *e.g.* ``isaac.storm``. GeoClaw
uses a two-stage discovery process: standard variable names are found
automatically from CF ``axis`` / ``standard_name`` attributes and
built-in fallback lists; you only need to supply ``var_mapping`` for
roles whose names are non-standard. Coordinate names (``lon``, ``lat``,
``time``) are always discovered automatically and never need to be
specified.

**Case 1 — all standard names (ERA5 and similar):**

ERA5 variable names (``u10``, ``v10``, ``msl``) are in the built-in
fallback lists and are found automatically. No ``var_mapping`` is
required:

.. code:: python

   import numpy as np
   from clawpack.geoclaw.surge.storm import Storm

   storm = Storm()
   storm.time_offset = np.datetime64('2012-08-29')
   storm.file_format = 'netcdf'
   storm.file_paths = ['path/to/era5_forcing.nc']
   storm.write('isaac.storm', file_format='data')

**Case 2 — mixed: standard wind names, non-standard pressure:**

A common pattern when a file has multiple pressure fields (e.g. mean
sea-level and surface pressure) or a non-standard pressure variable
name. Specify only the roles that cannot be discovered automatically;
the rest are still found from the fallback lists:

.. code:: python

   storm.write('isaac.storm', file_format='data',
               var_mapping={'pressure': 'prmsl'})

Any name supplied in ``var_mapping`` is validated against the variables
actually present in the file before the descriptor is written, so a
typo raises an informative error immediately rather than producing
incorrect output silently.

**Case 3 — all non-standard names (e.g. NWS13/OWI-NetCDF):**

Supply all three roles explicitly when none of the variable names match
the built-in fallback lists:

.. code:: python

   storm = Storm()
   storm.time_offset = np.datetime64('2012-08-29')
   storm.file_format = 'nws13'
   storm.file_paths = ['path/to/nws13_forcing.nc']
   storm.write('isaac.storm', file_format='data',
               var_mapping={'wind_u': 'uwnd',
                            'wind_v': 'vwnd',
                            'pressure': 'press'})

**Advanced: pre-built MetInterrogator:**

If you need direct control over CF validation, unit checking, or
lon/lat convention detection before the descriptor is written, you can
construct a :class:`~clawpack.geoclaw.netcdf_utils.MetInterrogator`
explicitly and pass it via ``met_interrogator``. When a pre-built
interrogator is supplied, auto-discovery and ``var_mapping`` validation
are bypassed entirely:

.. code:: python

   from clawpack.geoclaw.netcdf_utils import MetInterrogator

   mi = MetInterrogator('path/to/forcing.nc',
                        variable_map={'wind_u': 'u10',
                                      'wind_v': 'v10',
                                      'pressure': 'msl'})
   storm.write('isaac.storm', file_format='data', met_interrogator=mi)

.. note::

   ``dim_mapping`` is accepted by ``write()`` / ``write_data()`` for
   backwards compatibility but has no effect -- coordinate names are
   always discovered automatically via CF conventions.

.. note::

   ``storm.window`` (ramp width and application domain) and
   ``MetInterrogator``'s ``crop_bounds`` (read-time spatial subset of
   the NetCDF file) are independent. Setting one does not affect the
   other.


Time handling
^^^^^^^^^^^^^^^

GeoClaw works in seconds relative to a user-defined reference time
(typically landfall or storm genesis). Set it when constructing the
storm:

.. code:: python

   storm.time_offset = np.datetime64('2012-08-29T00:00')  # landfall time

Python computes ``nc_time_offset`` — the elapsed seconds from
``storm.time_offset`` to the first record in the file — and writes it
to the descriptor. This value is independent of how the file encodes
time internally (Unix epoch, local epoch, hours-since-reference, etc.).

Fortran converts raw time values using:

.. code::

   storm_time[i] = raw[i] − raw[0] + nc_time_offset

Subtracting ``raw[0]`` converts any absolute encoding to
elapsed-since-first-record; adding ``nc_time_offset`` then anchors that
to ``storm.time_offset``. No unit conversion (hours→seconds,
days→seconds) is performed in Fortran: the descriptor stores
``nc_time_offset`` in seconds and the raw values are read as stored.
``write_data`` passes ``time_reference=storm.time_offset`` to
``MetInterrogator`` automatically; no additional user action is needed.

Longitude convention
^^^^^^^^^^^^^^^^^^^^^^

Longitude convention ([0, 360] vs [-180, 180]) is detected and
normalized automatically by ``MetInterrogator``. ERA5 files that store
longitude in [0, 360] do not need to be preprocessed to [-180, 180]
before use. The detected convention is written to the descriptor and
Fortran applies index normalization at runtime without copying arrays.

--------------

Developer Reference
-------------------

Architecture overview
~~~~~~~~~~~~~~~~~~~~~

The system has a strict Python/Fortran split:

**Python** handles: file interrogation, CF attribute parsing, coordinate
convention detection, fill value resolution, unit conversion,
``nc_time_offset`` computation (elapsed seconds from ``storm.time_offset``
to the first record), crop bound validation, and descriptor writing.

**Fortran** handles: opening the NetCDF file at runtime using
information from the descriptor, index arithmetic for coordinate
normalization (no data copies), domain subsetting via
``start``/``count`` arguments to ``nf90_get_var``, time-slice reads
for met forcing, and converting raw time values to seconds from
``storm.time_offset`` via ``raw[i] − raw[0] + nc_time_offset``.

Fortran assumes the unit contract from ``GEOCLAW_NETCDF_UNITS`` in
``units.py`` without checking. Python enforces it.

Class hierarchy (``netcdf_utils.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   NetCDFInterrogator
       - open file (xarray, Dask-lazy)
       - discover coordinate variables by name heuristics + CF standard_name
       - detect lon convention, lat order, dim order
       - resolve fill value (_FillValue wins over missing_value per CF spec)
       - validate crop bounds against file extent
       - output: NetCDFDescriptor dataclass

   TopoInterrogator(NetCDFInterrogator)
       - detect fill values within crop region (hard error)
       - verify and convert units to contract
       - no multi-file coverage logic (Fortran handles compositing)

   MetInterrogator(NetCDFInterrogator)
       - check wind_u, wind_v, pressure present and on same grid/time axis
       - convert units to contract
       - decode CF time to seconds from offset
       - detect ensemble/member dimensions (hard error if non-singleton)
       - partial domain coverage is allowed (Fortran fills edges)

   DescriptorWriter
       - topo: writes key=value lines for inline inclusion in topo.data, using a 
         blank line to terminate the Fortran read loop
       - met: writes &file_info namelist block + repeated &variable_info
         blocks for *.storm file body

   CFNormalizer
       - adds/fixes CF attributes without modifying data
       - idempotent

Descriptor format
~~~~~~~~~~~~~~~~~

Topo (lines in topo.data after topo_type)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   var_name       = z
   lon_name       = longitude
   lat_name       = latitude
   lon_offset     = 0.0
   lat_order      = S_to_N
   dim_order      = lat,lon
   fill_value     = -9999.0
   fill_action    = abort
   crop_bounds    = -100.0 -80.0 20.0 35.0

``fill_action = abort`` is the only supported value for topography.
``crop_bounds`` is omitted if no crop is specified.

Met forcing (body of \*.storm after format header)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   # format: netcdf
   &file_info
     source_file    = /path/to/forcing.nc
     lon_name       = longitude
     lat_name       = latitude
     time_name      = valid_time
     dim_order      = time,lat,lon
     lon_convention = 360
     lat_order      = S_to_N
     fill_value     = -9999.0
     fill_action    = warn
     time_offset    = 0.0
     crop_bounds    = -100.0 -80.0 20.0 35.0
   /
   &variable_info  var_name=u10    geoclaw_role=wind_u    /
   &variable_info  var_name=v10    geoclaw_role=wind_v    /
   &variable_info  var_name=msl    geoclaw_role=pressure  /

The ``&variable_info`` blocks use a manually parsed key=value format
(not true repeated Fortran namelists) for compiler portability. Fortran
reads them in a loop until EOF. Adding new roles (precipitation,
friction) requires no change to the Fortran parser.

Unit contract
~~~~~~~~~~~~~

Defined in ``units.py``:

.. code:: python

   GEOCLAW_NETCDF_UNITS = {
       "topo":     "m",
       "wind_u":   "m/s",
       "wind_v":   "m/s",
       "pressure": "Pa",
       "time":     "s",
   }

All conversion happens in Python before the descriptor is written.
Fortran trusts the descriptor and never checks units. If you add a new
``geoclaw_role``, add its contract unit here first.

Fortran coordinate normalization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fortran applies coordinate normalization via index arithmetic only -- no
arrays are duplicated. The descriptor provides ``lon_convention`` and
``lat_order``; the reader uses these to compute correct indices when
calling ``nf90_get_var``. For crop bounds, ``start`` and ``count`` are
computed from the coordinate arrays at runtime.

All ``nf90_*`` calls go through a checked interface in
``topo_module.f90`` that prints a meaningful diagnostic and stops
cleanly on failure. This is important for SLURM batch jobs where a
silent Fortran ``STOP`` produces no useful output.

Known technical debt
~~~~~~~~~~~~~~~~~~~~

-  ``util.get_netcdf_names`` (in ``util.py``) remains a parallel
   implementation of variable name discovery alongside
   ``NetCDFInterrogator``. ``Storm.write_data`` now uses
   ``MetInterrogator`` for NetCDF met forcing (format 2), but falls back
   to ``util.get_netcdf_names`` for variable name discovery when no
   explicit ``var_mapping`` is provided. Full consolidation -- making
   ``util.get_netcdf_names`` delegate to ``NetCDFInterrogator`` and
   removing the duplicate -- remains a TODO.
-  WRF raw output requires ``MetPreprocessor`` for string-time decoding
   (``Times`` character array, not a numeric CF time variable) and
   curvilinear grid handling (``XLAT``/``XLONG`` are 2D time-varying
   arrays). A skip-marked test stub documents the gap in
   ``test_storm.py``.


Adding a new met forcing field (e.g. precipitation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Add the role and unit to ``GEOCLAW_NETCDF_UNITS`` in ``units.py``
2. Add detection logic to ``MetInterrogator`` for the new variable
3. ``DescriptorWriter`` requires no change -- new ``&variable_info``
   blocks are written automatically for any role the interrogator
   returns
4. Add the Fortran reader logic in the storm NetCDF module to consume
   the new ``geoclaw_role`` value
5. Add unit tests in ``tests/netcdf/test_met_interrogator.py``
6. Add a regression test in the appropriate storm surge example

Test structure
~~~~~~~~~~~~~~

::

   tests/netcdf/                        unit tests for netcdf_utils.py
       conftest.py                      in-memory NetCDF fixtures
       test_base_interrogator.py
       test_topo_interrogator.py
       test_met_interrogator.py
       test_descriptor_writer.py
       test_cf_normalizer.py

   tests/test_storm.py                  extended for ERA5 and NWS13 variants

   examples/tsunami/bowl-slosh-netcdf/  coordinate variant regression tests
   examples/tsunami/chile2010/          topotools write path + coord variants
   examples/storm-surge/isaac/          ERA5 and NWS13 met forcing regression

All test NetCDF files are generated in-memory or in ``tmp_path`` -- no
binary files are committed to the repository.

--------------

Next steps
----------

-  **Consolidate util.get_netcdf_names**: ``Storm.write_data`` now
   calls ``MetInterrogator`` and ``DescriptorWriter`` for NetCDF met
   forcing; the remaining step is to make ``util.get_netcdf_names``
   delegate to ``NetCDFInterrogator`` and remove the duplicate discovery
   logic in ``storm.py``
-  **WRF support**: implement ``MetPreprocessor`` to handle string-time
   axis and curvilinear grid; the skip-marked test stub in
   ``test_storm.py`` documents the expected interface
-  **Precipitation field**: reserved in ``GEOCLAW_NETCDF_UNITS``, add
   ``MetInterrogator`` detection and Fortran consumer
-  **Friction field**: same pattern as precipitation
-  **CLI tool**: expose ``CFNormalizer`` as a command-line utility for
   users who want to check or repair their NetCDF files before running
   GeoClaw
-  **Duplicate code audit**: other places in the GeoClaw codebase that
   do ad-hoc NetCDF variable discovery should be identified and migrated
   to ``NetCDFInterrogator``
