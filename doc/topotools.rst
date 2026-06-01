
.. _topotools:

Python tools for working with topo and dtopo
--------------------------------------------

.. seealso::
   - :ref:`topo`
   - :ref:`topo_order`
   - :ref:`topodata_format`


Preprocessing attributes
~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`~clawpack.geoclaw.topotools.Topography` objects support seven
preprocessing attributes that are applied automatically by
:meth:`~clawpack.geoclaw.topotools.Topography.read` in this order:

1. ``negate_z`` — flip sign of Z (independent of ``topo_type < 0``).
2. ``z_shift`` — add a constant to all non-missing Z values.
3. ``x_shift`` — add a constant to all x coordinates.
4. ``crop_extent``, ``buffer``, ``align``, ``coarsen`` — crop and subsample
   via :meth:`~clawpack.geoclaw.topotools.Topography.crop`.

Set them before calling ``read()``::

   from clawpack.geoclaw.topotools import Topography

   t = Topography()
   t.crop_extent = [-100., -60., 10., 50.]
   t.coarsen = 2
   t.z_shift = 10.0
   t.read('bathymetry.nc', topo_type=4)

See :ref:`setrun_topo_preprocessing` for a full attribute table with types
and defaults, and non-obvious behavior notes.


Lazy-load pattern for NetCDF (read_header)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For NetCDF files (``topo_type=4``),
:meth:`~clawpack.geoclaw.topotools.Topography.read_header` uses
:class:`~clawpack.geoclaw.netcdf_utils.TopoInspector` to detect coordinate
variable names via CF conventions (``standard_name``, ``axis``, or common
fallback names such as ``lon``/``lat``, ``x``/``y``).  After calling
``read_header()``, ``extent`` and ``delta`` are populated without loading the
elevation array.  Accessing ``Z`` triggers a deferred ``read()``:

.. code-block:: python

   t = Topography()
   t.path = 'large_dem.nc'
   t.topo_type = 4
   t.read_header()     # fast: reads coordinate arrays only
   print(t.extent)     # available immediately
   print(t.delta)      # available immediately
   z = t.Z             # triggers full read on first access

This pattern is also used internally by ``TopographyData._compute_priority_order``
to determine file resolution without loading elevation data.


.. deprecated::
   ``topo_type=1`` (three-column ``x y z`` ASCII, one point per line) is
   deprecated.  Reading emits a ``DeprecationWarning``; writing also emits a
   ``DeprecationWarning``; setting any preprocessing attribute before reading
   raises ``NotImplementedError``.

   To convert a type-1 file::

       t = Topography()
       t.read('old.tt1', topo_type=1)   # DeprecationWarning
       t.write('new.tt2', topo_type=2)  # save as type 2

   Genuinely unstructured (scattered) point data cannot be converted this
   way and must be gridded externally (e.g. ``scipy.interpolate``, GMT)
   before use in GeoClaw.


.. toctree::
   :maxdepth: 1

   topotools_module
   dtopotools_module
   geoclaw_util_module
   kmltools_module
