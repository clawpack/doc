

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

**Add more**

Changes to AMR parameters
-------------------------

* The `rundata` object generally defined in `setrun.py` now has an 
  attribute `rundata.amrdata` and AMR parameters are attributes of this
  object. 

* Setting `mxnest` negative to indicate that anisotropic refinement
  in different directions might be used has been eliminated.
  Now this is always assumed and one must always specify 
  refinement ratios in each direction and in time.

**Add more**
