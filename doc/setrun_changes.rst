

.. _setrun_changes:

*****************************************************************
Changes to input parameters in setrun.py from 4.x to 5.0
*****************************************************************

Changes to general parameters 
-----------------------------

* Many names have been changed, e.g.

  * `ndim` to `num_dim`
  * `xlower`, `ylower`, `zlower` are now `lower[0], lower[1], lower[2]`.
  * `xupper`, `yupper`, `zupper` are now `upper[0], upper[1], upper[2]`.
  * `mx, my, mz` are now `num_cells[0:3]`.

  There are many other such changes.  It is best to take a look at the 
  `setrun.py` for an example in `$CLAW/classic/examples`.  

See also:
  
 * :ref:`setrun`
 * :ref:`claw46to50`

Changes to AMR parameters
-------------------------

* The `rundata` object generally defined in `setrun.py` now has an 
  attribute `rundata.amrdata` and AMR parameters are attributes of this
  object.   Most names of attributes have changed from those used in 4.x.

* Setting `mxnest` negative to indicate that anisotropic refinement
  in different directions might be used has been eliminated.
  Now this is always assumed and one must always specify 
  refinement ratios in each direction and in time.

* New attributes have been added to indicate whether Richardson
  extrapolation and/or the routine ins `flag2refine` should be used
  to flag cells for refinement.  See :ref:`refinement`.

* The capability of using "regions" to specify areas where refinement is
  forced or prohibited has been extended from GeoClaw to AMRClaw.
  See :ref:`refinement_regions`.

See also:
  
 * :ref:`setrun_amrclaw`
 * :ref:`claw46to50`


Changes to GeoClaw parameters
------------------------------

A number of changes have been made to parameter names and also functionality
in some cases.

See also:
  
 * :ref:`setrun_geoclaw`
 * :ref:`claw46to50`


