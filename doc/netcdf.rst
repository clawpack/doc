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

GeoClaw NetCDF Input System
===========================

This document covers the NetCDF input pipeline introduced in the
``refactor-netcdf-support`` PR. It has two sections: a user guide for
scientists who want to use NetCDF files as input, and a developer
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

.. code:: python

   from clawpack.geoclaw.netcdf_utils import TopoInterrogator
   meta = TopoInterrogator('bathy.nc', var_name='z',
                           crop_bounds=(-100, -60, 15, 35)).interrogate_topo()
   rundata.topo_data.topofiles.append([4, 'bathy.nc', meta])

That is the only change required in most cases. GeoClaw's Python layer
interrogates the file when you run ``setrun.py`` and writes the
necessary descriptor information into ``topo.data`` automatically.
Variable and coordinate names are auto-detected from CF attributes where
possible; pass ``var_name``, ``lon_name``, or ``lat_name`` explicitly to
``TopoInterrogator`` if auto-detection fails.

Domain subsetting (crop)
^^^^^^^^^^^^^^^^^^^^^^^^

If your NetCDF file covers a larger area than your simulation domain
(common with global or regional datasets), you can crop at read time
without creating a smaller file:

.. code:: python

   topo_data.topofiles.append([4, 'gebco_global.nc',
                                {'crop_bounds': [-100, -80, 20, 35]}])

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

Then create the storm descriptor file, *e.g.* ``isaac.storm``, using the
Python API:

.. code:: python

   from clawpack.geoclaw.surge.storm import Storm
   import numpy as np

   storm = Storm()
   storm.time_offset = np.datetime64('2012-08-29')
   storm.file_format = 'netcdf'
   storm.file_paths = ['path/to/forcing.nc']
   storm.write('isaac.storm', file_format='data')

If your variable or dimension names are non-standard, provide a mapping:

.. code:: python

   storm.write('isaac.storm', file_format='data',
               dim_mapping={'t': 'valid_time'},
               var_mapping={'wind_u': 'u10', 'wind_v': 'v10',
                            'pressure': 'msl'})

Time handling
^^^^^^^^^^^^^

GeoClaw works in seconds from a user-defined offset (typically landfall
or storm genesis). All CF time decoding -- including calendar handling
and unit conversion from hours/days -- is done in Python. The Fortran
runtime sees only seconds from offset.

Set the offset when constructing the storm:

.. code:: python

   storm.time_offset = np.datetime64('2012-08-29T00:00')  # landfall time

--------------

Developer Reference
-------------------

Architecture overview
~~~~~~~~~~~~~~~~~~~~~

The system has a strict Python/Fortran split:

**Python** handles: file interrogation, CF attribute parsing, coordinate
convention detection, fill value resolution, unit conversion, time
decoding, crop bound validation, and descriptor writing.

**Fortran** handles: opening the NetCDF file at runtime using
information from the descriptor, index arithmetic for coordinate
normalization (no data copies), domain subsetting via
``start``/``count`` arguments to ``nf90_get_var``, and time-slice reads
for met forcing.

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
   lon_convention = 180
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

-  ``util.get_netcdf_names`` and the coordinate/variable discovery logic
   in ``NetCDFInterrogator`` are parallel implementations. They should
   be consolidated -- ``NetCDFInterrogator`` should be the single source
   and ``util.get_netcdf_names`` should delegate to it. This is deferred
   to the surge module refactor.
-  ``Storm.write(file_format="data")`` does not yet call
   ``DescriptorWriter`` directly for NetCDF storm entries. Currently the
   tests write descriptors manually. The integration should happen as
   part of the surge refactor.
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

-  **Surge module refactor**: consolidate ``util.get_netcdf_names`` into
   ``NetCDFInterrogator``, wire ``Storm.write`` to use
   ``DescriptorWriter``, clean up parallel discovery paths in
   ``storm.py``
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
