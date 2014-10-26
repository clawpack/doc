
.. _refinement:

*****************************************************************
AMR refinement criteria
*****************************************************************

Several parameters controlling refinement can be set in the `setrun`
function.  See :ref:`setrun_amrclaw` for further description of these.
Many of the parameters discussed below are attributes of `rundata.amrdata`
in `setrun.py`.

Every `regrid_interval` time steps on each level, the error is
estimated in all cells on grids at this level. Cells where some
refinement criteria are satisfied are flagged for refinement. Default
options for flagging are described below.  Additional cells surrounding
the flagged cells are also flagged to insure that moving features
of the solution (e.g. shock waves) do not escape from the region
of refinement before the next regridding time.  The number of buffer
cells flagged is specified by `regrid_buffer_width` and the number
of steps between regridding on each level is specified by
`regrid_interval`.  Typically these are equal (assuming the Courant
number is close to 1) and taken to be some small integer such as 2 or 3.

In addition to flagging individual cells based on the behavior of the
solution, it is also possible to specify that certain regions of the domain
should always be refined to a certain level (and/or never refined above 
some level).  This is described further in :ref:`refinement_regions`.
These regions are used in conjunction with the methods
described below to determine whether or not a given cell should be flagged
for refinement.   

The cells that have been flagged are then clustered into
rectangular regions to form grids at the next finer level. The clustering is
done in light of the tradeoffs between a few large grids (which usually
means refinement of many additional cells that were not flagged) or many
small grids (which typically results in fewer fine grid cells but more grids
and hence more overhead and less efficient looping over shorter rows of
cells). The parameter `clustering_cutoff` in amrNez.data is used to control this
tradeoff. At least this fraction of the fine grid cells should result from
coarse cells that were flagged as needing refinement. The value 
clustering_cutoff = 0.7 is usually reasonable.

.. _refinement_flagging:

Flagging criteria
-----------------

Two possible approaches to flagging individual 
cells for refinement (based on the behavior of the solution) are built into
AMRClaw.  (A different default approach is used in GeoClaw, see 
:ref:`refinement_geoclaw`).  

.. _refinement_flag2refine:

flag2refine
^^^^^^^^^^^

One approach to flagging cells for refinement (the default used in
most examples) is to set `flag2refine == True` and specify
a tolerance `flag2refine_tol`.  This indicates that the
library subroutine `$CLAW/amrclaw/src/Nd/flag2refine.f90` should
be used to flag cells for refinement.  This routine computes the
maximum max-norm of the undivided difference of :math:`q_{i,j}`
based its four neighbors in two space dimensions (or 6 neighbors in
3d).  If this is greater than the specified tolerance, then the
cell is flagged for refinement (subject to limitations imposed by
"regions").  The undivided difference (not divided by the mesh
width) is used, e.g.  :math:`|q(m,i+1,j) - q(m,i-1,j)|` for each
component :math:`m`.

Note that the user can change the criterion used for flagging cells by
modifying this routine -- best done by copying the library routine to your
application directory and modifying the `Makefile` to point to the modified
version.

.. _refinement_richardson:

Richardson extrapolation
^^^^^^^^^^^^^^^^^^^^^^^^^

The second approach to flagging individual cells is based on using Richardson
extrapolation to estimate the error in each cell.  This is used if
`flag_richardson == True`.    In this case a cell is flagged if the error
estimate exceeds the value `flag_richardson_tol`.  
Richardson estimation requires taking two time steps on the current grid and
comparing the result with what’s obtained by taking one step on a coarsened
grid.  
One time step on the fine grid is re-used, so only one additional time step
on the fine grid and one on a coarsened grid are required.
It is somewhat more expensive than the `flag2refine` approach,
but may be more useful for cases where the solution is smooth and undivided
differences do not identify the regions of greatest error.

**Note:** Both approaches can be used together: if 
`flag2refine == True` and `flag_richardson == True`
then a cell will be flagged if either of the corresponding specified
tolerances is exceeded.

.. _refinement_regions:

Specifying AMR regions
----------------------


In addition to specifying a tolerance or other criteria for flagging
individual cells as described above, it is possible to specify regions of
the domain so that all points in the region, over some
time interval also specified, will be refined to at least some level
*minlevel* and at most some level *maxlevel*.
These are specified through the parameter `rundata.regiondata.regions` in
`setrun.py`.  
This is a list of lists, each of which specifies a region.  A new region can
be added via::

    rundata.regiondata.regions.append([minlevel,maxlevel,t1,t2,x1,x2,y1,y2])

This indicates that over the time period from `t1` to `t2`, cells in the
rectangle `x1 <= x <= x2` and `y1 <= y <= y2` should be refined to at least
`minlevel` and at most `maxlevel`.  

To determine whether a grid cell lies in one of the regions specified, the
center of the grid cell is used.  If a mapped grid is being used, the limits
for the regions should be in terms of the computational grid coordinates,
not the physical coordinates.

If a cell center lies in more than one specified region, then the
cell will definitely be flagged for refinement at level L (meaning it should
be covered by a Level L+1 grid) if *L+1 <= minlevel* for any of the regions,
regardless of whether the general flagging criteria hold or not.  
This means the smallest of the various *minlevel* parameters for any region
covering this point will take effect.  Conversely it will **not**
be flagged for refinement if *L+1 > maxlevel* for **all** regions that cover
this point.  This means the largest of the various *maxlevel* parameters for
any region covering this point will take effect.
(However, note that since flagged cells are buffered as described above by
flagging some adjacent cells, a cell may still end up flagged for refinement
even if the above tests say it should not be.)


For example, suppose that `amr_levels_max = 6` has been specified along
with these two regions::

    rundata.regiondata.regions.append([2, 5, 10.0, 30.0, 0.0, 0.5, 0.0, 0.5])
    rundata.regiondata.regions.append([3, 4, 20.0, 40.0, 0.2, 1.0, 0.2, 1.0])

The first region specifies that from time 10 to 30 there should be at least 2
levels and at most 5 levels of refinement for points in the spatial domain
`0 < x < 0.5` and `0 < y < 0.5`.  

The second region specifies that from time 20 to 40 there should be at least 3
level and at most 4 levels of refinement for points in the spatial domain
`0.2 < x < 1.0` and `0.2 < y < 1.0`.  

Note that these regions overlap in both space and time, and in regions of
overlap the *maximum* of the `minlevel` and also the *maximum* of the 
`maxlevel` parameters applies.  So in the above example, from time 20 to 30
there will be at least 3 levels and at most 5 levels in the region of
overlap, `0.2 < x < 0.5` and `0.2 < y < 0.5`.

Within these regions, how many levels are chosen at each point will be
determined by the *error flagging criteria*, i.e.  by the default
or user-supplied routine :ref:`refinement_flag2refine`,  or as
determined by :ref:`refinement_richardson`, as described above.

Points that are not covered by either region are not constrained by the
regions at all.   With `amr_levels_max = 6` then they might
be refined to any level from 1 to 6 depending on the error flagging criteria.

It is easiest to explain how this works by summarizing the implementation:

The regridding algorithm from level L to L+1 loops over all grid cells
at Level L and flags them or not based on the following criteria, where
`(xc,yc)` represents the cell center and `t` is the current regridding time:

* Initialize the flag by applying the error flagging criteria
  specified by Richardson extrapolation and/or the default or user-supplied
  routine `flag2refine` to determine whether this cell should be flagged.

* Loop over all regions (if any) for which `(xc,yc,t)` lies in the region
  specified.

TODO:  This might be wrong!!!  

  * If `L >= maxlevel` for *any* such region, set `flag = False` for this
    cell and go on to the next cell.

  * If `L < minlevel` for *every* such region, set `flag = True` and
    go on to the next grid cell.




.. _refinement_geoclaw:

Flagging criteria in GeoClaw
-----------------------------

In GeoClaw, a special `flag2refine` subroutine is defined.

TODO: need to describe geoclaw flag2refine.




