.. _topodata_format:

topo.data File Format
=====================

.. note::
   ``topo.data`` is generated automatically by ``make data`` or by calling
   :meth:`TopographyData.write() <clawpack.geoclaw.data.TopographyData.write>`.
   It is not intended to be hand-authored.  The format is tied to the GeoClaw
   version; files generated with an older build may be incompatible with a
   newer Fortran binary.

Overview
--------

``topo.data`` is read by the Fortran routine ``read_topo_settings`` in
``topo_module.f90``.  It describes every topography file used in a simulation:
how to locate the file, its format type, and preprocessing parameters to apply
at load time.

The file has two sections:

1. A 3-line **global header**.
2. One **per-file block** for each topography file.


Global Header (3 lines)
-----------------------

::

    <topo_missing>      # replace no_data_value in topofile
    <test_topography>   # (Type topography specification)
    <ntopofiles>        # number of topo files

``topo_missing``
    Float sentinel (default ``99999.0``).  Fortran replaces each file's own
    ``no_data_value`` with this value after loading.

``test_topography``
    Integer.  ``0`` = use the file list that follows.  Values ``1``–``3``
    select built-in analytic test bathymetries (jump discontinuity, oceanic
    shelf); in those cases no per-file blocks are written.

``ntopofiles``
    Integer count of per-file blocks that follow.

.. note::
   ``override_order`` is a Python-only attribute of
   :class:`~clawpack.geoclaw.data.TopographyData`; it controls how Python
   sorts the files before writing but is **not** written to ``topo.data``.


Per-File Block (9 lines, all types)
------------------------------------

One block follows for each topography file, in priority order (finest
resolution first; see :ref:`priority_convention` below).

::

    '<absolute_path>'           # topo_path
    <topo_type>                 # topo_type
    <x1> <x2> <y1> <y2>        # crop_extent [x1 x2 y1 y2]
    <coarsen>                   # coarsen
    <buffer>                    # buffer
    <x_align> <y_align>         # align [x y]
    <x_shift>                   # x_shift
    <z_shift>                   # z_shift
    T|F                         # negate_z

``topo_path``
    Absolute path to the topography file, single-quoted.

``topo_type``
    Integer format code: ``2`` (one-value-per-line ASCII), ``3`` (row-major
    ASCII), ``4`` (NetCDF), ``5`` (GeoTIFF).  Negative values (e.g. ``-2``)
    apply an additional sign flip to Z on load (Fortran convention).

``crop_extent``
    Four floats: ``x1 x2 y1 y2`` defining a bounding box.
    Sentinel ``"0. 0. 0. 0."`` means no cropping (sentinel is safe because
    a valid extent requires ``x1 < x2`` and ``y1 < y2``).

``coarsen``
    Integer stride factor for subsampling (``1`` = no coarsening).

``buffer``
    Integer number of grid points to retain outside the crop region on each
    side (``0`` = no buffer).

``align``
    Two floats: ``x_align y_align`` alignment target for subsampled grids.
    Sentinel ``"0. 0."`` means no alignment constraint.

``x_shift``
    Float added to all x coordinates after loading (``0`` = no shift).

``z_shift``
    Float added to all non-missing elevation values (``0`` = no shift).

``negate_z``
    ``T`` or ``F``.  If ``T``, all elevation values are negated after loading,
    independently of the ``topo_type`` sign convention.

.. _netcdf_descriptor_block:

NetCDF Descriptor Block (type 4 only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For ``topo_type = 4`` files, the 9-line block is followed immediately by a
CF descriptor block.  The descriptor is a sequence of ``key=value`` lines
terminated by a blank line, parsed by Fortran's ``read_netcdf_descriptor``.
Example::

    var_name=elevation
    lon_name=lon
    lat_name=lat
    lat_order=S_to_N
    dim_order=lat,lon
    lon_convention=180
    lon_offset=0.0
    source_units=m
    fill_action=abort

``lon_offset``
    Scalar added by Fortran to file longitudes to convert them to domain
    coordinates: ``x_domain = x_file + lon_offset``.  For files using the
    ``[0, 360]`` convention against a ``[-180, 180]`` domain, this is
    ``-360.0``.  Use
    :meth:`TopoInspector.topo_entries()
    <clawpack.geoclaw.netcdf_utils.TopoInspector.topo_entries>` to compute
    the correct value automatically.


Annotated Examples
------------------

Type-2 ASCII file, no preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    99999.0                    # replace no_data_value in topofile
    0                          # (Type topography specification)
    1                          # number of topo files

    '/data/etopo1.tt2'         # topo_path
      2                        # topo_type
    0. 0. 0. 0.                # crop_extent [x1 x2 y1 y2]
    1                          # coarsen
    0                          # buffer
    0. 0.                      # align [x y]
    0                          # x_shift
    0                          # z_shift
    F                          # negate_z

Type-4 NetCDF file, with crop and negate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    99999.0                    # replace no_data_value in topofile
    0                          # (Type topography specification)
    1                          # number of topo files

    '/data/gebco.nc'           # topo_path
      4                        # topo_type
    -100. -60. 10. 50.         # crop_extent [x1 x2 y1 y2]
    1                          # coarsen
    2                          # buffer
    0. 0.                      # align [x y]
    0                          # x_shift
    0                          # z_shift
    T                          # negate_z

    var_name=elevation
    lon_name=lon
    lat_name=lat
    lat_order=S_to_N
    dim_order=lat,lon
    lon_convention=180
    lon_offset=0.0
    source_units=m
    fill_action=abort


.. _priority_convention:

Priority Convention
-------------------

The first file block in ``topo.data`` is assigned **rank 1** by Fortran
(highest priority in overlap resolution).  Fortran stores this mapping in
``mtopoorder``: ``mtopoorder(1) = 1`` means file-index 1 → rank 1.

Python's :meth:`~clawpack.geoclaw.data.TopographyData._compute_priority_order`
sorts files by cell area ascending (finest = smallest ``dx * dy``) before
writing, so the finest file is automatically written first.

To override this sort and use your own ordering, set
``TopographyData.override_order = True``.  When ``True``, you are responsible
for placing the finest file first in ``topofiles``.

.. warning::
   ``override_order`` is a Python-only attribute.  It is **not** written to
   ``topo.data`` and has no Fortran-side counterpart.


Sentinel Values
---------------

+----------------+--------------------+--------------------------------------+
| Parameter      | Sentinel value     | Meaning                              |
+================+====================+======================================+
| ``crop_extent``| ``0. 0. 0. 0.``    | No cropping; use full file domain.   |
+----------------+--------------------+--------------------------------------+
| ``align``      | ``0. 0.``          | No alignment constraint.             |
+----------------+--------------------+--------------------------------------+
| ``negate_z``   | ``F``              | No sign flip.                        |
+----------------+--------------------+--------------------------------------+

Sentinel values are geometrically invalid as real parameters (a valid extent
requires ``x1 < x2``; a valid alignment is non-zero in typical cases) so
Fortran can unambiguously distinguish "not set" from a genuine value.


Deprecated Formats
------------------

In older setrun.py files, ``topofiles`` entries were plain Python lists or
dicts.  These are still accepted by
:class:`~clawpack.geoclaw.data.TopographyData` but emit a
``DeprecationWarning``.

**Old list format (deprecated):**

.. code-block:: python

   rundata.topo_data.topofiles.append([2, '/path/to/topo.tt2'])
   # or the older 6-element form (level/time info is ignored):
   rundata.topo_data.topofiles.append([2, 1, 5, 0.0, 1e10, '/path/to/topo.tt2'])

**Old dict format (deprecated):**

.. code-block:: python

   rundata.topo_data.topofiles.append({
       'topo_type': 2,
       'topo_path': '/path/to/topo.tt2',
       'extent': [-100., -60., 10., 50.],   # note: 'extent' → crop_extent
       'coarsen': 2,
   })

Note: the dict key ``'extent'`` maps to ``Topography.crop_extent``, **not**
to ``Topography.extent`` (which is a read-only property returning loaded-data
bounds).

**Recommended form:**

.. code-block:: python

   from clawpack.geoclaw.topotools import Topography

   t = Topography()
   t.path = '/path/to/topo.tt2'
   t.topo_type = 2
   t.crop_extent = [-100., -60., 10., 50.]
   t.coarsen = 2
   rundata.topo_data.topofiles.append(t)

**topo_type=1 (deprecated):**

Type-1 files (``x y z`` ASCII, one point per line) are still readable with a
``DeprecationWarning``, but preprocessing attributes (``crop_extent``,
``coarsen``, etc.) raise ``NotImplementedError``.  To convert::

    t = Topography()
    t.read('old_file.tt1', topo_type=1)   # DeprecationWarning
    t.write('new_file.tt2', topo_type=2)  # convert to type 2

For genuinely unstructured (scattered) point data, use
``scipy.interpolate``, GMT, or a similar tool to grid the data before use.
