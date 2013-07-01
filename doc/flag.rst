
.. _flag:

**************************************
Flagging cells for adaptive refinement
**************************************

**Describe flagging  and clustering algorithms in more detail.**

See :ref:`setrun_amrclaw` for a description of the input parameters that define how
Richardson extrapolation and/or the `flag2refine` subroutine work.

.. _flag_regions:

Refinement regions
------------------

In AMRClaw and GeoClaw it is possible to specify space-time regions in which
refinement to a certain level is forced or a level beyond which refinement if
forbidden.  These are specified through the parameter `rundata.regiondata.regions` in
`setrun.py`.  
This is a list of lists, each of which specifies a region in the form 
`[minlevel,maxlevel,t1,t2,x1,x2,y1,y2]`.


For example, suppose that `amr_levels_max = 6` has been specified along
with these two regions::

    rundata.regiondata.regions = []
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
determined by the *error flagging criteria*, i.e. as 
specified by Richardson extrapolation and/or the default or user-supplied
routine `flag2refine`.  The parameters for these are described in
:ref:`setrun`.

Points that are not covered by either region are not constrained by the
regions.  They might
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

  * If `L >= maxlevel` for *any* such region, set `flag = False` for this
    cell and go on to the next cell.

  * If `L < minlevel` for *every* such region, set `flag = True` and
    go on to the next grid cell.

