
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

**Note:** Starting in v5.6.0, a new approach is also available, see
:ref:`adjoint`.

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

**New in Version 5.7.0:** Although the regions described here are still
supported in v5.7.0, a more general form of :ref:`flagregions`
are also now supported and are recommended in general rather than
using what is described below.

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

Implementation
--------------

It is perhaps easiest to understand how this works by summarizing
the implementation.  Note the order in which different flagging
criteria are checked was modified in Version 5.5.0 in order to avoid
the more expensive options for grid cells that are either forbidden
from being refined or forced to be refined based on `regions` they
lie in.

The regridding algorithm from level L to L+1 loops over all grid patches
(in parallel when OpenMP is used with
more than one thread).  The cells on each patch are initially marked with 
`amrflags(i,j) = UNSET`, a special value (set in `amr_module.f90`).

In flagging based on regions: 

 * If the current level is less than the
   maximum of all `minlevel` values for regions that contain the cell, then it
   is marked with `amrflags(i,j) = DOFLAG`.

 * If the current level is greater than or equal to the
   maximum of all `maxlevel` values for regions that contain the cell, then it
   is marked with `amrflags(i,j) = DONTFLAG`.

If there are any cells in the patch that are still marked as `UNSET` after
checking all the regions, then if the `setrun` parameter `flag2refine` is
True, then the routine `flag2refine` is called.
The user may wish to create their own version of this routine.
The default library version was modified with the addition of the adjoint
option in Version 5.6.0 (see :ref:`adjoint`), and does one of two things:

 * If `adjoint_flagging` then it checks the inner product of the forward
   solution with all adjoints over the specified time period and if the
   magnitude is greater than `tolsp` the cell is marked `DOFLAG`.

 * Otherwise, the undivided difference of all components of `q` in each
   coordinate direction is computed, e.g. `abs(q(:,i+1,j) - q(:,i-1,j))` and
   `abs(q(:,i,j+1) - q(:,i,j-1))` in 2d, and if the maximum of these is 
   greater than `tolsp` the cell is marked `DOFLAG`.

If there are still any cells in the patch that are still marked as `UNSET`, 
then if the `setrun` parameter `flag_richardson` is
True, then the routine `errest` is called. This does flagging based on
estimates of the one-step error produced by Richardson extrapolation using
the solution on the current grid and on a coarsened grid.  If
`adjoint_flagging` then these estimates are applied to the inner product of
the error estimate with the adjoint solutions over the relevant time period.
In either case, the setrun parameter `flag_richardson_tol` is used as the
tolerance.



.. _refinement_geoclaw:

Flagging criteria in GeoClaw
-----------------------------

In GeoClaw, a special `flag2refine` subroutine is defined.
A standard approach for modeling tsunamis propagating across the ocean
is to refine anywhere that the surface elevation of the ocean :math:`\eta =
h+B` is greater in absolute value than some specified `wave_tolerance`, e.g.
0.1 meter as set, for example, in the `setrun.py` file of
`$CLAW/geoclaw/examples/tsunami/chile2010`.  
This `wave_tolerance` parameter can be set for any GeoClaw application.

Often this ends up refining the entire ocean when in fact only some waves
are of interest.  In this case one can use `regions` as described in
:ref:`flagregions` to limit refinement to certain space-time regions.

Alternatively, starting in Version 5.6.0 one can use adjoint flagging (see
:ref:`adjoint`) to better select the waves that will reach a particular
location over a specified time range, including those that might reflect off
distant shores.

Generally one must also use `regions` to allow (or force) much higher levels of
refinement over small regions along the coast if one is doing detailed
inundation modeling of a particular community.





