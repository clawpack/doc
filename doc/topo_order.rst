

.. _topo_order:

*****************************************************************
Topography file ordering
*****************************************************************

.. warning :: This feature has bugs in v5.13.0 and v5.13.1 and should not
   be used in those versions.  These bugs were fixed (we hope) in v5.14.0.
   See :ref:`release_5_14_0` for more discussion.


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
would be considered finer in this case, with a relative tolerance of
0.001 used to judge whether the resolutions are the same).

.. warning :: This relative tolerance was introduced in v5.14.0,
   and in previous versions rounding errors in `dx` and/or `dy` could
   have resulted in a different ordering, and possibly different
   simulation results.

Starting in v5.14.0, there is a `setrun.py` parameter
`rundata.topo_data.override_order` that is set to `False` by default to
produce the default behavior described above.

If `setrun.py` specifies::

    rundata.topo_data.override_order = True

then the preference order is no longer based on the computed
resolution. Instead it is assumed that the topo files in
`rundata.topo_data.topofiles` are ordered from least preferable to most
preferable (so normally you would list the coarsest DEM first, going down to
the finest DEM, in order to reproduce the default behavior).
This allows precise specification of the order of preference.

Resolution of dtopo files
-------------------------

Note that internally GeoClaw creates a topo array from each topofile read
in that has the initial topography.  If one or more dtopo files are also
specified, which specify motion of the topography, then these internal
topo arrays are modified as the simulation proceeds to incorporate this dtopo.
The dtopo files may have different resolution than any of the topo files, and
at any rate the information from the dtopo files is interpolated into each
topo array that it overlaps at each time step while the ground motion is
active (as determined by the final time in the dtopo file).

Internally GeoClaw also creates a set of `topo_for_dtopo` arrays that have
exactly the same extent and resolution as each dtopo file, and with topo values
that are interpolated from the best available topo data (based on the ordering
as discussed above, which has already been performed when these new arrays
are filled).

These arrays are then handled as any other topo arrays would be, and are
inserted into the ranking of topo arrays according to an algorithm described
below.  So when the cell-average topo value `B` must be computed in a
finite volume cell on a grid patch (either at the time of regridding or because
the topo has changed due to dtopo), these `topo_for_dtopo` arrays may be used
along with the original topo arrays at any point where they provide the
best resolution according to the ranking algorithm.

The reason for introducing these new  `topo_for_dtopo` arrays is that the
dtopo might be specified on a much finder grid than the underlying topo
in the same geographic region.  For example, a submarine slump landslide
might be specified on a 2" dtopo file on the continental shelf, in a region
where the best ocean topography is on a 15" grid.  We do not want to lose
the resolution of the dtopo when transferring it to topo grids, and so it
would not be sufficient to only transfer it to the 15" grid and use that to
set cell values `B` (at least not when the computational grid cell has
finer resolution than 15").
Instead we interpolate the 15" ocean topo to the new
2" `topo_for_dtopo` array and give this higher priority than the 15" topo
array in the landslide region.

Once the original topo arrays have been ordered as discussed above,
the algorithm for inserting the `topo_for_dtopo` arrays into this ordering
is to insert it as far down in the ranking as possible (lowest priority)
with the constraint that all topo arrays with higher priority should have
finer resolution.  So in the example above, the 2" `topo_for_dtopo` array
would have higher priority than the 15" ocean topo, but would generally
have lower priority than any finer-resolution coastal topo arrays that
might overlap the dtopo extent (since those arrays not only have better topo
values but also have the dtopo interpolated to their resolution).
