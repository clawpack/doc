.. _netcdf_input:

.. warning ::  Many changes are being implemented in the way topo and dtopo
  files are handled, in both the Python tools and the Fortran code.
  See :ref:`topochanges` for a summary.

GeoClaw NetCDF Input System
===========================

This document covers the NetCDF input pipeline introduced in the
``refactor-netcdf-support``
[PR #701](https://github.com/clawpack/geoclaw/pull/701)
(merged but not yet released). It has two sections: a user
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

-  Units: a recognized non-contract unit (e.g. ``km``/``cm`` for elevation,
   ``hPa``/``mbar`` for pressure, ``knots`` for wind) is converted
   automatically. Python resolves the unit to a single multiplicative scale
   factor; Fortran applies it on read (in-memory Python reads convert
   directly). A missing or unrecognized unit is still an error -- see the
   per-variable notes below.
-  Longitude conventions: both [-180, 180] and [0, 360] are detected and
   normalized at runtime. You do not need to preprocess the file.
-  Latitude ordering: both S-to-N and N-to-S are handled correctly.
-  Dimension ordering: ``(lat, lon)`` and ``(lon, lat)`` are both
   supported.
-  Fill values: ``_FillValue`` and ``missing_value`` attributes are
   resolved automatically. If a fill value is found within your
   simulation domain, GeoClaw will abort with an error -- this is
   intentional, as missing bathymetry is a silent correctness hazard.
-  File extension: the NetCDF backend engine is selected explicitly, so a
   valid NetCDF file opens even when its name uses a non-standard
   extension (e.g. ``.dtt3``) that xarray's extension-based engine
   guessing would otherwise fail to recognize.

What your file must provide
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  A 2D variable containing elevation (positive up, negative for ocean),
   carrying a CF ``units`` attribute.  Meters (e.g. ``units = "m"``) is the
   contract unit; a variable in a **recognized** non-meter unit such as
   ``km`` or ``cm`` is **converted automatically** on read (a warning is
   emitted noting the conversion).  Units are still **required** and never
   assumed: a variable with **no** ``units`` attribute, or one whose unit is
   unrecognized, is rejected with an error rather than being silently
   misread.  For a file that is genuinely in meters but merely omits the
   attribute, opt in explicitly by passing ``assume_units='m'`` to
   ``TopoInspector`` (or ``nc_params={'assume_units': 'm'}`` to
   ``Topography.read``); ``assume_units`` also accepts a non-meter unit
   (e.g. ``'km'``), which is then converted.
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
variable automatically, use ``topo_entries()`` to inspect the file:

.. code:: python

   from clawpack.geoclaw.netcdf_utils import TopoInspector
   with TopoInspector('bathy.nc', crop_bounds=(-100, -60, 15, 35)) as insp:
       rundata.topo_data.topofiles.extend(insp.topo_entries())

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

   meta = TopoInspector('bathy.nc', var_name='my_elevation',
                        crop_bounds=(-100, -60, 15, 35)).inspect_topo()

Coordinate names (``lon``/``latitude``/``x`` etc.) and dimension ordering are
always discovered automatically and never need to be specified.

Domain subsetting (crop)
^^^^^^^^^^^^^^^^^^^^^^^^

If your NetCDF file covers a larger area than your simulation domain
(common with global or regional datasets), pass ``crop_bounds`` to
``TopoInspector`` and use ``topo_entries()`` to register the file:

.. code:: python

   from clawpack.geoclaw.netcdf_utils import TopoInspector
   with TopoInspector('gebco_global.nc',
                      crop_bounds=(-100, -80, 20, 35)) as insp:
       rundata.topo_data.topofiles.extend(insp.topo_entries())

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

Writing NetCDF topo files
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``topotools.Topography`` object can be written as a CF-compliant NetCDF
file (``topo_type=4``) that GeoClaw reads back through the same descriptor
mechanism::

   topo.write('bathy.nc', topo_type=4)                     # elevation float32
   topo.write('bathy.nc', topo_type=4, z_dtype='float64')  # full precision
   topo.write('bathy.nc', topo_type=4, compression=True)   # zlib-compressed

The elevation variable is written with ``units = "m"``.  It is stored on
disk as ``float32`` by default -- sub-millimeter precision for Earth
topography (``abs(Z) < 10000`` m) at half the file size -- and
``z_dtype='float64'`` selects full double precision.

Pass ``compression=True`` to zlib-compress the elevation variable (zlib level
1 with the byte ``shuffle`` filter).  The compressed file is a normal,
randomly-readable NetCDF -- the netCDF library decompresses on read, so no
reader or Fortran change is needed -- and is typically much smaller,
especially for sparse or smooth fields.  ``compression`` also accepts an
integer zlib level (``1``--``9``) or a dict of encoding options for full
control; the default ``None`` writes an uncompressed file, bit-identical to
before.

--------------

Seafloor deformation (dtopo) from NetCDF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Time-dependent seafloor deformation (dtopo) can also be read from and
written to CF-compliant NetCDF using ``dtopo_type=4`` (see :ref:`dtopo`):

.. code:: python

   from clawpack.geoclaw import dtopotools
   dtopo = dtopotools.DTopography('deformation.nc', dtopo_type=4)   # read
   dtopo.write('out.nc', dtopo_type=4)                             # write
   dtopo.write('out.nc', dtopo_type=4, dz_dtype='float64')         # full precision
   dtopo.write('out.nc', dtopo_type=4, compression=True)           # zlib-compressed

As with topography, the deformation contract unit is meters and it is stored
``float32`` by default (pass ``dz_dtype='float64'`` for full double
precision).  ``compression=True`` zlib-compresses the deformation variable
(and chunks it one time slice at a time, matching how Fortran reads it),
which shrinks a typical sparse dtopo file several-fold while remaining
directly readable; an integer level or a dict is also accepted.  A recognized non-meter unit (e.g. ``km``) is converted
automatically on read, exactly as for topography; a missing or unrecognized
unit raises.  (ASCII dtopo types remain meters-implied, unchanged.)

**Time axis.**  By default the time coordinate is written as a bare CF
duration, ``units = "seconds"``, holding simulation-relative times.  If you
set the optional ``time_reference`` attribute to a real-world epoch (for
example the earthquake origin time), the file is instead written with a CF
datetime axis, ``units = "seconds since <time_reference>"``::

   dtopo.time_reference = '2011-03-11T05:46:00'
   dtopo.write('out.nc', dtopo_type=4)

A datetime axis is more interoperable (a plain ``xarray.open_dataset`` or a
GIS tool decodes it to real timestamps) and round-trips back to the same
simulation-relative times.  On read, the time axis is interpreted using its
CF ``units``, so an axis in ``"minutes"``, ``"hours"``, or a
``"<unit> since <date>"`` datetime is scaled to seconds correctly rather
than assumed to already be in seconds.  Unlike met forcing, a bare
``"seconds"`` (relative) dtopo axis is allowed.

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

GeoClaw uses the following variables, whose **contract units** are shown.
A variable already in the contract unit passes through unchanged; a variable
in a recognized non-contract unit is converted automatically (see below):

============================= ==================================
Variable                      Contract unit
============================= ==================================
Wind (u-component, eastward)  m/s
Wind (v-component, northward) m/s
Surface pressure              Pa
Time                          CF datetime (``<unit> since <date>``)
============================= ==================================

**Unit conversion.**  A recognized non-contract unit -- ``hPa``/``mbar`` for
pressure, ``knots`` for wind -- is converted automatically: Python computes a
multiplicative scale factor and Fortran applies it on read (a warning notes
the conversion).  An unrecognized or dimensionally incompatible unit raises.

**Missing units.**  When a variable has **no** ``units`` attribute, GeoClaw
falls back to the unit documented by the storm *format* if it is known: for
NWS13/OWI files, pressure is taken as ``mbar`` (and converted to ``Pa``) and
wind as ``m/s``.  Otherwise a missing unit raises, unless you pass
``assume_units=True`` to ``MetInspector`` to declare that the variables are
already in contract units.

**Magnitude sanity check.**  After units resolve, GeoClaw runs a bounded
min/max check on wind and pressure.  A pressure field that is ~1000x too
small (unmistakably ``hPa``/``mbar`` that was mislabeled ``Pa``) is
auto-corrected with a warning; a pressure, wind, or elevation field that is
otherwise physically implausible raises.  Pass ``skip_sanity_check=True`` to
the inspector to bypass this for an exotic-but-valid file.

**Time axis.**  The time coordinate must be an absolute CF datetime axis --
``units`` of the form ``"<unit> since <date>"`` (e.g. ``"seconds since
2020-01-01"`` or ``"hours since 2020-01-01"``).  A non-second axis such as a
raw ERA5 ``"hours since ..."`` is scaled to seconds automatically (Python
records a ``time_scale`` that Fortran applies), so it no longer needs
pre-conversion.  A bare numeric/duration axis with no reference date is
rejected outright (see `Time handling`_ below).

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
   from clawpack.geoclaw.met.storm import Storm

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

**Advanced: pre-built MetInspector:**

If you need direct control over CF validation, unit checking, or
lon/lat convention detection before the descriptor is written, you can
construct a :class:`~clawpack.geoclaw.netcdf_utils.MetInspector`
explicitly and pass it via ``met_inspector``. When a pre-built
inspector is supplied, auto-discovery and ``var_mapping`` validation
are bypassed entirely:

.. code:: python

   from clawpack.geoclaw.netcdf_utils import MetInspector

   mi = MetInspector('path/to/forcing.nc',
                     variable_map={'wind_u': 'u10',
                                   'wind_v': 'v10',
                                   'pressure': 'msl'})
   storm.write('isaac.storm', file_format='data', met_inspector=mi)

.. note::

   ``dim_mapping`` is accepted by ``write()`` / ``write_data()`` for
   backwards compatibility but has no effect -- coordinate names are
   always discovered automatically via CF conventions.

.. note::

   ``storm.window`` (ramp width and application domain) and
   ``MetInspector``'s ``crop_bounds`` (read-time spatial subset of
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

   storm_time[i] = nint((raw[i] − raw[0]) * time_scale) + nint(nc_time_offset)

Subtracting ``raw[0]`` converts any absolute encoding to
elapsed-since-first-record; multiplying by ``time_scale`` converts the
file's CF time unit to seconds (``1.0`` for ``"seconds since ..."``,
``3600.0`` for ``"hours since ..."``, etc.); adding ``nc_time_offset`` then
anchors that to ``storm.time_offset``.  Both factors are resolved in Python
and written to the descriptor, so Fortran never parses CF time units --
it just multiplies.  ``write_data`` passes
``time_reference=storm.time_offset`` to ``MetInspector`` automatically; no
additional user action is needed.

The met time axis must be an absolute CF datetime axis -- ``units`` of the
form ``"<unit> since <date>"`` -- which xarray decodes to datetimes for the
offset computation above.  A non-second axis (e.g. a raw ERA5 ``"hours
since ..."``) is scaled to seconds via ``time_scale`` and no longer needs
pre-conversion.  A bare numeric/duration axis with no reference date is
**rejected** outright.  This parallels dtopo NetCDF, where Python collapses
the time axis to ``(t0, dt)`` in seconds (see
`Seafloor deformation (dtopo) from NetCDF`_).

Longitude convention
^^^^^^^^^^^^^^^^^^^^^^

Longitude convention ([0, 360] vs [-180, 180]) is detected and
normalized automatically by ``MetInspector``. ERA5 files that store
longitude in [0, 360] do not need to be preprocessed to [-180, 180]
before use. The detected convention is written to the descriptor and
Fortran applies index normalization at runtime without copying arrays.

--------------

Developer Reference
-------------------

Architecture overview
~~~~~~~~~~~~~~~~~~~~~

The system has a strict Python/Fortran split:

**Python** handles: file inspection, CF attribute parsing, coordinate
convention detection, fill value resolution, unit resolution (a recognized
non-contract unit becomes a multiplicative ``scale_factor``, and a
non-second time axis a ``time_scale``; missing/unrecognized units raise),
the magnitude sanity check, ``nc_time_offset`` computation (elapsed seconds
from ``storm.time_offset`` to the first record), crop bound validation, and
descriptor writing.

**Fortran** handles: opening the NetCDF file at runtime using
information from the descriptor, index arithmetic for coordinate
normalization (no data copies), domain subsetting via
``start``/``count`` arguments to ``nf90_get_var``, time-slice reads
for met forcing, multiplying each variable by its ``scale_factor`` on read,
and converting raw time values to seconds from ``storm.time_offset`` via
``nint((raw[i] − raw[0]) * time_scale) + nint(nc_time_offset)``.

All unit logic lives in Python; Fortran is a dumb multiplier.  Python
resolves every unit against the contract in ``GEOCLAW_NETCDF_UNITS``
(``units.py``) to a single ``scale_factor`` (defaulting to ``1.0``, so
contract-unit files are bit-identical) and Fortran applies it without
checking.

Class hierarchy (``netcdf_utils.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   NetCDFInspector
       - open file (xarray, Dask-lazy)
       - discover coordinate variables by name heuristics + CF standard_name
       - detect lon convention, lat order, dim order
       - resolve fill value (_FillValue wins over missing_value per CF spec)
       - validate crop bounds against file extent
       - output: NetCDFDescriptor dataclass

   TopoInspector(NetCDFInspector)
       - detect fill values within crop region (hard error)
       - resolve units -> scale_factor (convert recognized; reject missing/unknown)
       - magnitude sanity check on resolved elevation
       - no multi-file coverage logic (Fortran handles compositing)

   MetInspector(NetCDFInspector)
       - check wind_u, wind_v, pressure present and on same grid/time axis
       - resolve units -> per-variable scale_factor (+ format-unit fallback)
       - resolve non-second time axis -> time_scale
       - magnitude sanity check on resolved wind/pressure
       - decode CF datetime axis to seconds from offset (reject bare-numeric)
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
   x_name         = longitude
   y_name         = latitude
   lon_wrap_offset = 0.0
   y_increasing   = True
   dim_order      = lat,lon
   scale_factor   = 1.0
   fill_value     = -9999.0
   fill_action    = abort
   crop_bounds    = -100.0 -80.0 20.0 35.0

``fill_action = abort`` is the only supported value for topography.
``scale_factor`` is the multiplier Fortran applies to the elevation on read
(``1.0`` for a meters file; e.g. ``1000.0`` for a ``km`` file).
``crop_bounds`` is omitted if no crop is specified.

dtopo (lines in dtopo.data after the per-file block)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   var_name       = dz
   x_name         = longitude
   y_name         = latitude
   time_name      = time
   lon_wrap_offset = 0.0
   scale_factor   = 1.0
   y_increasing   = True
   dim_order      = time,lat,lon
   t0             = 0.0
   dt             = 10.0

``t0`` and ``dt`` give the first time and the uniform time step in simulation
**seconds**; Python collapses the CF time axis to these (scaling by the file's
CF ``units``), so Fortran never parses CF time for dtopo.  ``time_name`` is the
name of the time coordinate in the file.  ``scale_factor`` is the multiplier
Fortran applies to the deformation on read (``1.0`` for a meters file).

Met forcing (body of \*.storm after format header)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   &file_info
     x_name         = longitude
     y_name         = latitude
     time_name      = valid_time
     dim_order      = time,lat,lon
     lon_wrap       = 360
     y_increasing   = True
     fill_value     = -9999.0
     fill_action    = warn
     time_offset    = 0.0
     time_scale     = 1.0
   /
   &variable_info  var_name=u10    geoclaw_role=wind_u    scale_factor=1.0  /
   &variable_info  var_name=v10    geoclaw_role=wind_v    scale_factor=1.0  /
   &variable_info  var_name=msl    geoclaw_role=pressure  scale_factor=1.0  /

(``lon_wrap`` is written only for a geographic longitude axis; ``fill_value``
only when the file declares one; ``crop_bounds`` is carried by the top-level
``crop_extent`` line rather than the descriptor.)  ``time_scale`` is the
seconds-per-file-time-unit that Fortran multiplies the elapsed time by
(``1.0`` for ``"seconds since ..."``, ``3600.0`` for ``"hours since ..."``);
each ``&variable_info`` carries the per-variable ``scale_factor`` Fortran
applies to that field (e.g. ``100.0`` for an ``hPa``/``mbar`` pressure).

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

Python resolves each variable's ``units`` attribute against this contract:
a matching unit passes through (``scale_factor = 1.0``), a recognized
non-contract unit yields the multiplicative ``scale_factor`` written to the
descriptor, and a missing or unrecognized unit raises (met additionally
falls back to the storm format's documented unit when the attribute is
absent).  Fortran trusts the descriptor, multiplies by ``scale_factor``, and
never checks units.  If you add a new ``geoclaw_role``, add its contract unit
here first.

Fortran coordinate normalization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fortran applies coordinate normalization via index arithmetic only -- no
arrays are duplicated. The descriptor provides the longitude-wrap field
(``lon_wrap`` for met, ``lon_wrap_offset`` for topo) and the latitude order
(``y_increasing``); the reader uses these to compute correct indices when
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
   ``NetCDFInspector``. ``Storm.write_data`` now uses
   ``MetInspector`` for NetCDF met forcing (format 2), but falls back
   to ``util.get_netcdf_names`` for variable name discovery when no
   explicit ``var_mapping`` is provided. Full consolidation -- making
   ``util.get_netcdf_names`` delegate to ``NetCDFInspector`` and
   removing the duplicate -- remains a TODO.
-  WRF raw output requires ``MetPreprocessor`` for string-time decoding
   (``Times`` character array, not a numeric CF time variable) and
   curvilinear grid handling (``XLAT``/``XLONG`` are 2D time-varying
   arrays). A skip-marked test stub documents the gap in
   ``test_storm.py``.


Adding a new met forcing field (e.g. precipitation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Add the role and unit to ``GEOCLAW_NETCDF_UNITS`` in ``units.py``
2. Add detection logic to ``MetInspector`` for the new variable
3. ``DescriptorWriter`` requires no change -- new ``&variable_info``
   blocks are written automatically for any role the inspector
   returns
4. Add the Fortran reader logic in the storm NetCDF module to consume
   the new ``geoclaw_role`` value
5. Add unit tests in ``tests/netcdf/test_met_inspector.py``
6. Add a regression test in the appropriate storm surge example

Test structure
~~~~~~~~~~~~~~

::

   tests/netcdf/                        unit tests for netcdf_utils.py
       conftest.py                      in-memory NetCDF fixtures
       test_base_inspector.py
       test_topo_inspector.py
       test_met_inspector.py
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
   calls ``MetInspector`` and ``DescriptorWriter`` for NetCDF met
   forcing; the remaining step is to make ``util.get_netcdf_names``
   delegate to ``NetCDFInspector`` and remove the duplicate discovery
   logic in ``storm.py``
-  **WRF support**: implement ``MetPreprocessor`` to handle string-time
   axis and curvilinear grid; the skip-marked test stub in
   ``test_storm.py`` documents the expected interface
-  **Precipitation field**: reserved in ``GEOCLAW_NETCDF_UNITS``, add
   ``MetInspector`` detection and Fortran consumer
-  **Friction field**: same pattern as precipitation
-  **CLI tool**: expose ``CFNormalizer`` as a command-line utility for
   users who want to check or repair their NetCDF files before running
   GeoClaw
-  **Duplicate code audit**: other places in the GeoClaw codebase that
   do ad-hoc NetCDF variable discovery should be identified and migrated
   to ``NetCDFInspector``
