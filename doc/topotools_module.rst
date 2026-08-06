
.. _topotools_module:

topotools module for working with topography data
=================================================

.. warning ::  Many changes are being implemented in the way topo and dtopo
  files are handled, in both the Python tools and the Fortran code.
  See :ref:`topochanges` for a summary.
  
.. seealso::
   - :ref:`topo`
   - :ref:`netcdf_input`


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

   topo = Topography()
   topo.crop_extent = [-100., -60., 10., 50.]
   topo.coarsen = 2
   topo.z_shift = 10.0
   topo.read('bathymetry.nc', topo_type=4)

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

   topo = Topography()
   topo.path = 'large_dem.nc'
   topo.topo_type = 4
   topo.read_header()     # fast: reads coordinate arrays only
   print(topo.extent)     # available immediately
   print(topo.delta)      # available immediately
   z = topo.Z             # triggers full read on first access

This pattern is also used internally by ``TopographyData._compute_priority_order``
to determine file resolution without loading elevation data.


Vertical datum metadata
~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`~clawpack.geoclaw.topotools.Topography` and
:class:`~clawpack.geoclaw.dtopotools.DTopography` carry an optional ``datum``
attribute recording the vertical reference of the elevation/deformation data
(e.g. ``'MSL'`` or ``'NAVD88'``).  It defaults to ``None``, is populated from a
NetCDF ``vertical_datum`` (or ``datum``) attribute on read, and is written
back out on NetCDF write (``topo_type=4`` / ``dtopo_type=4``).  ASCII formats
have no datum field, so the value is not persisted for types 1/2/3.

The datum is **informational only** -- GeoClaw performs no vertical-datum
transformation and always uses the Z values as given.  As a guard, both
:meth:`~clawpack.geoclaw.data.TopographyData.write` (when producing
``topo.data``) and :meth:`~clawpack.geoclaw.data.DTopoData.write` (``dtopo.data``)
issue a warning if the files they are given carry more than one distinct
datum, since mixing vertical references without converting between them is a
likely error.


.. deprecated::
   ``topo_type=1`` (three-column ``x y z`` ASCII, one point per line) is
   deprecated.  Reading emits a ``DeprecationWarning``; writing also emits a
   ``DeprecationWarning``; setting any preprocessing attribute before reading
   raises ``NotImplementedError``.

   To convert a type-1 file::

       topo = Topography()
       topo.read('old.tt1', topo_type=1)   # DeprecationWarning
       topo.write('new.tt2', topo_type=2)  # save as type 2

   Genuinely unstructured (scattered) point data cannot be converted this
   way.  Either grid it externally (e.g. ``scipy.interpolate``, GMT) or use
   :meth:`~clawpack.geoclaw.topotools.Topography.interp_unstructured` (see
   `Gridding unstructured (scattered) data`_ below).


Gridding unstructured (scattered) data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GeoClaw's solvers require topography on a regular, logically rectangular grid
(Cartesian x-y in meters, or lon-lat -- see ``coordinate_system`` in
:ref:`setrun_geoclaw`), but survey or sounding data often comes as scattered
``(x, y, z)`` points.  A
:class:`~clawpack.geoclaw.topotools.Topography` constructed with
``unstructured=True`` holds such points in its ``x``, ``y``, and ``z``
arrays, and
:meth:`~clawpack.geoclaw.topotools.Topography.interp_unstructured`
interpolates them onto a regular grid, optionally filling gaps from one or
more coarser (structured or unstructured) "fill" topographies:

.. code-block:: python

   from clawpack.geoclaw.topotools import Topography

   # Scattered survey points (x, y, z)
   survey = Topography(unstructured=True)
   survey.x = x_points
   survey.y = y_points
   survey.z = z_values

   # A coarser regional DEM used to fill gaps between survey points
   regional = Topography(path='regional.tt3', topo_type=3)
   regional.read()

   survey.interp_unstructured(regional, extent=[x1, x2, y1, y2],
                              proximity_radius=100.0)
   survey.unstructured        # now False -- it holds a regular grid
   survey.write('combined.tt3', topo_type=3)

The grid spacing is taken from the minimum spacing of the scattered points
(bounded below by ``delta_limit`` meters) unless set explicitly with
``delta``.  A fill point is used only where it lies inside ``extent``, carries
valid data, and is more than ``proximity_radius`` meters from every scattered
point, so the higher-resolution survey data is preferred wherever it exists.
Missing fill values (``NaN`` in memory, or a numeric ``no_data_value``) are
dropped.  See
:meth:`~clawpack.geoclaw.topotools.Topography.interp_unstructured` for the
full set of parameters.


The notebook
`topotools_examples <http://www.clawpack.org/gallery/_static/notebooks/geoclaw/topotools_examples.html>`__
illustrates how to use some of the tools. **Needs to be updated.**


The file `$CLAW/geoclaw/tests/test_topotools.py` contains some tests of these
tools.  Looking at these test routines may also give some ideas on 
how to use them.  **Needs to be updated.**


Documentation auto-generated from the module docstrings
--------------------------------------------------------

.. automodule:: clawpack.geoclaw.topotools
   :members:

