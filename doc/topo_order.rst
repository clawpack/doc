

.. _topo_order:

*****************************************************************
Topography file ordering
*****************************************************************

.. seealso::
   - :ref:`topo`

To compute the cell-averaged topography value in each computational cell,
the default approach in GeoClaw is to use the finest topography available at
each point in the cell. Since each topofile (DEM) is on a rectangular grid with
regular spacing `dx` and `dy`, the resolutions are compared by computing the
cell areas `dx*dy`.  If two or more topofiles overlap a point in the cell
then the finer one is used.

This usually works fine but may not always be what is wanted. In particular
there may be two DEMs at essentially the same resolution, but one is a more
recent and hence a better dataset to use
(but perhaps covers a smaller area, so the
older DEM is also needed outside this area).  In this case we want to
guarantee that the newer one is used where available.  Even if the
resolutions are essentially identical, `dx*dy` maybe be slightly different
(perhaps at the roundoff level) and so it could be that the older one is viewed
as "finer" and would be used preferentially.  Even if `dx*dy` is exactly the
same, it is not obvious which one would be used in GeoClaw.
(The one listed later in `rundata.topo_data.topofiles`
would be considered finer in this case.)

Starting in v5.13.0, there is a new `setrun.py` parameter
`rundata.topo_data.override_order` that is set to `False` by default to
produce the default behavior described above.

If `setrun.py` specifies::

    rundata.topo_data.override_order = True

then the preference order is no longer based on the computed
resolution. Instead it is assumed that the files in
`rundata.topo_data.topofiles` are ordered from least preferable to most
preferable (so normally you would list the coarsest DEM first, going down to
the finest DEM, in order to reproduce the default behavior).  
This allows precise specification of the order of preference.

