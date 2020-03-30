
.. _flagregions:

Specifying flagregions for adaptive refinement
==============================================

**New in Version 5.7.0.**

AMRClaw and GeoClaw version 5.6.1 (and earlier) allow specifying
rectangular refinement regions (see :ref:`refinement_regions`) 
in `setrun.py`, in the form of a list that is appended to
`rundata.regiondata.regions`::

   rundata.regiondata.regions.append([minlevel,maxlevel,t1,t2,x1,x2,y1,y2])

This is a region that is active from time `t1` to `t2` over the
spatial extent `[x1,x2,y1,y2]`.

Starting in v5.7.0 of AMRClaw/GeoClaw we now support a new approach to
specifying regions that are now called `flagregions` for more clarity
regarding what they are used for.  The new data structure
also supports simple rectangles and so should ultimately replace
`regions` in both AMRClaw and GeoClaw, but currently you can mix and match. 


The new way of specifying a flag region in `setrun.py` is to first
define an object `flagregion` of class `clawpack.amrclaw.data.FlagRegion`, 
set various
attributes of this object (including `minlevel`, `maxlevel`, `t1`,
`t2`, and a spatial extent), and then append this object to the list
`rundata.flagregiondata.flagregions`. 

Here is how you would specify a simple rectangle as above in the new
style, chosen to cover the entire spatial domain and to allow only 1 level
everywhere (which might be supplemented by other regions where more levels
are allowed)::

    x1,x2,y1,y2 = [rundatat.clawdata.lower[0], rundatat.clawdata.upper[0],
                   rundatat.clawdata.lower[1], rundatat.clawdata.upper[1]]

    from clawpack.amrclaw.data import FlagRegion
    flagregion = FlagRegion(num_dim=2)  # so far only 2D supported
    flagregion.name = 'Region_domain'
    flagregion.minlevel = 1
    flagregion.maxlevel = 1
    flagregion.t1 = 0.
    flagregion.t2 = 1e9
    flagregion.spatial_region_type = 1  # Rectangle
    flagregion.spatial_region = [x1,x2,y1,y2]
    rundata.flagregiondata.flagregions.append(flagregion)

Note that `flagregion.spatial_region_type == 1` indicates that the
flagregion is a rectangle.

.. _flagregions-rr:

Using ruled rectangles as flagregions
-------------------------------------

In addition to simple rectangles, more general ruled rectangles can also be
used as flagregions.  These are a restricted set of polygons for which it is
easy to test if a point is inside or outside, as described in more detail in
:ref:`ruled_rectangles`.

To specify a ruled rectangle, use `flagregion.spatial_region_type == 2`
and provide a path to a data file that describes the ruled rectangle.
For simple ruled rectangles the code to create the data file can also be
included in `setrun.py`.

Here is an example where a simple ruled rectangle is defined and used as a
flagregion.  In this case the flagregion is a trapezoid with vertices
:math:`(1,3),~ (1,6),~ (2,4),~ (2,7)`::

   from clawpack.amrclaw.data import FlagRegion
   flagregion = FlagRegion(num_dim=2)
   flagregion.name = 'Region_Trapezoid'
   flagregion.minlevel = 2
   flagregion.maxlevel = 3
   flagregion.t1 = 0.
   flagregion.t2 = 1e9
   flagregion.spatial_region_type = 2  # Ruled Rectangle
   flagregion.spatial_region_file = \
       os.path.abspath('RuledRectangle_Trapezoid.data')
   rundata.flagregiondata.flagregions.append(flagregion)

   # code to make RuledRectangle_Trapezoid.data:
   from clawpack.amrclaw import region_tools
   rr = region_tools.RuledRectangle()
   rr.method = 1 # piecewiselinear edges between s values
   rr.ixy = 'x'  # so s refers to x, lower & upper are limits in y
   rr.s = np.array([1,2])
   rr.lower = np.array([3,6])
   rr.upper = np.array([4,7])
   rr.write('RuledRectangle_Trapezoid.data')  # creates data file


See the `setrun.py` file in
`$CLAW/amrclaw/examples/advection_2d_flagregions` for additional examples.

See :ref:`mf-amr-flag` for a more complex example where a ruled rectangle is
defined that covers a set of fgmax points (see :ref:`fgmax`) defined with the 
:ref:`marching_front`.
