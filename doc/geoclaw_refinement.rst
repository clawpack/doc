

.. _geoclaw_refinement:

*******************
GeoClaw Refinement
*******************

This documentation is intended to provide an explanation as to how GeoClaw
currently allows refinement to take place.  The best place to look for details
not included here is the source itself, most notably ``flag2refine2.f90`` and
secondarily ``allowflag.f90``.

GeoClaw broadly has two different types of refinement, that which is forced due
to a region either specified via a topography file, a dtopo file, or a qinit
file, and refinement due to a criteria such as sea-level.  These criteria can be
controlled via data parameters usually found in the ``setrun.py`` file.  See
:ref:`setrun_geoclaw` for specific details on the parameters below.

Algorithm
---------

Since the order of the evaluation of the criteria and how they are evaluated is
important it is worthwhile to take some time to examine how this works:

#. Each region based criteria is checked for the minimum level in that region. 
   If the current location is not at or above this level and it is inside a
   region then it is flagged for needing refinement and the algorithm moves to
   the next cell location.

#. Each region based criteria is checked to see if it allows refinement to the
   next level at the point in question.  Note that if two regions overlap the
   maximum level is allowed.

#. If it was determined that refinement will be allowed then the physics based
   criteria are checked in order to see if the cell in question should be
   flagged.  Note that with the sea-level criteria a limit can be placed on the
   maximum level allowed to refine to based on the depth in the cell.

We now turn to a description of each refinement criteria

Region-Based Criteria
---------------------

Region based refinement generally is specified as a rectangular (quadralateral
on the sphere technically) region where refinement is limited or forced.  There
are four kinds of regions currently supported:

 * Topography Regions - When specifying a topography file the user can also
   specify minimum and maximum levels of refinement to be used with that
   topography file.  For instance, if we had the line::

    topo_data.topofiles.append([3, 2, 5, 0.0, 1e4, 'gulf_caribbean.tt3'])

   the region that the topography file 'gulf_caribbean.tt3' covers would force
   refinement to at least level 2 and allow all refinement up to level 5.  It
   also would only enforce this criteria while the topography file was being
   used, i.e. between time ``t=0.0`` and ``t=1e4``.

 * General Regions - These regions do not coincide with any specific element,
   such as topography, but allow the user to specify rectangular regions in
   space and intervals in time to allow and force refinement to a particular
   level.  Beyond the need to specify the corners of the regions these act in
   the same way as topography regions do.

 * DTopography Regions - Identically treated as the topography regions, just for
   the dtopo files.

 * QInit Regions - Again these behave the same as topography regions however the
   time interval that they are enforced on is only enforced at the starting time
   of the simulation.

Physics-Based Criteria
----------------------

Once it has been determined that the regions allow for refinement at the cell
being examined we then move onto using criteria based on the state vector ``q``.
These are only checked if the depth of the fluid is above the ``dry_tolerance``.

 * Wave Criteria - Check that the difference between the specified ``sea_level``
   parameter and the sea-surface :math:`\eta` is above the parameter
   ``wave_tolerance``.  If this is satisfied the cell's depth is then checked to
   see if it is in deep water via the parameter ``deep_depth``, if so then it
   checks to see if it is allowed to refine via the parameter
   ``max_level_deep``.  If this is all satisfied the cell is flagged.
 
 * Speed Criteria - Compute the speed of the fluid in this cell via::

    speed = sqrt(q(2, :, :)**2 + q(3, :, :)**2) / q(1, :, :)

   and checks to see if the given computed speed is greater than the tolerance
   for the current level.  The parameter ``speed_tolerance`` is an array equal
   in length to the number of allowed levels with each value corresponding to
   the tolerance for that level.  If the speed of the fluid in that cell is
   greater than the ``m``th element than refinement to the ``m``the level is
   forced.  As an example consider a cell on level 2 whose speed was computed to
   be 2 m/s.  If the parameter ``speed_tolerance = [0.5, 1.0, 3.0, 5.0]`` then
   the cell would be marked as needing refinement.  If instead the cell was
   already at level 3 then the cell would not be flagged as needing refinement.

 * Storm Criteria - If modeling storm surge there are two additional physical
   parameters that are checked.  The first is distance from the eye of the storm
   and the second is the wind speed.  An array for each criteria is allowed to
   specify the tolerances per-level for which refinement will be forced similar
   to the speed criteria.