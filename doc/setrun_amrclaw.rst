
.. _setrun_amrclaw:

*****************************************************************
Specifying AMRClaw run-time parameters in `setrun.py`
*****************************************************************


It may be useful to look at a specific example, e.g. 
:ref:`setrun_amrclaw_sample`.

**Note:** Many parameters have changed name since Version 4.X and some new
ones have been added.  See :ref:`setrun_changes` for a summary.

To convert a Version 4.x `setrun.py` file to Version 5.0, see :ref:`claw46to50`.


Input
-----

`setrun` takes a single argument `claw_pkg` that should be set to `amrclaw`.

Output
------

`rundata`, an object of class `ClawRunData`, created in the
setrun file with the commands::

       from clawpack.clawutil import clawdata 
       rundata = clawdata.ClawRunData(claw_pkg, num_dim)

The `rundata` object has an attribute `rundata.clawdata` whose
attributes are described in :ref:`setrun`.

In addition, for AMRClaw `rundata` has an attribute `rundata.amrdata`
whose attributes are described below.


Run-time parameters
-------------------

The parameters needed in 2 space dimensions (*ndim=2*) are described.  In 3d
there are analogous parameters in z required, as mentioned below.

In addition to the parameters in `rundata.clawdata` (see :ref:`setrun`),
the AMR parameters that can be set are the following attributes of
`rundata.amrdata`: 


Special AMR parameters
----------------------

.. attribute:: amr_levels_max : int

   Maximum levels of refinement to use.  

.. attribute:: refinement_ratios_x : list of int 

   Refinement ratios to use in the `x` direction.  

   *Example:*  If `num_cells[0] = 10` and `refinement_ratios_x = [2,4]`
   then the Level 1 grid will have 10 cells in the x-direction, 
   Level 2 patches will be refined by a factor of 2, 
   and Level 3 will be refined by 4 relative to Level 2 
   (by 8 relative to Level 1).  

.. attribute:: refinement_ratios_y : list of int 

   Refinement ratios to use in the `y` direction.  
  
.. attribute:: refinement_ratios_t : list of int 

   Refinement ratios to use in time.  For an explicit method, maintaining
   the Courant number usually requires refining in time by the same factor as
   in space (or the maximum of the refinement ratio in the different space
   directions).  

   **Note:** Rather than specifying this list, in GeoClaw it is possible to set 
   to set `variable_dt_refinement_ratios = True` so refinement ratios in
   time are chosen automatically.  This might be ported to AMRClaw?
  
.. attribute:: aux_type : list of str, of length num_aux

   Specifies the type of variable stored in each aux variable.  
   These are used when coarsening aux arrays.  Each 
   element can be one of the following (but at most one can be 'capacity'):

    * 'center' for cell-centered values (e.g. density)
    * 'capacity' for a cell-centered capacity function (e.g. cell volume)
    * 'xleft' for a value centered on the left edge in x (e.g. normal velocity u)
    * 'yleft' for a value centered on the left edge in y (e.g. normal velocity v)

.. attribute:: flag_richardson : boolean

   Determines whether Richardson extrapolation will be used as an error
   estimator.  If `True`, patches will be coarsened by a factor of 2 each
   time regridding is done and  the result from a single step on the 
   coarsened patch with double the time step will be compared to the
   solution after 2 steps on the original patch in order to estimate the error.

.. attribute:: flag_richardson_tol : float

   When `flag_richardson == True`, cells will be flagged for refinement
   if the absolute value of the estimated error exceeds this value.

   When `flag_richardson == False`, this value is not used.

.. attribute:: flag2refine : boolean

   Determines whether the subroutine `flag2refine` is used to flag cells 
   for refinement.  
   
.. attribute:: flag2refine_tol : float

   When `flag2refine == True`, the default library version `flag2refine.f`
   checks the maximum absolute value of the difference between any component
   of q in this cell with the corresponding component in any of the
   neighboring cells.  The cell is flagged for refinement if the maximum 
   value is greater than this tolerance.

.. attribute:: regrid_interval : int

   The number of time steps to take on each level between regridding to the
   next finer level.

.. attribute:: regrid_buffer_width : int
 
   The number of points to flag for refining around any point flagged by
   error estimation or `flag2refine`.  This buffer zone is to insure that
   waves do not leave the refined region before the next regridding and so
   is generally chosen based on the value of `regrid_interval`, typically to
   be the same value since waves can travel at most one grid cell per time
   step.

.. attribute:: clustering_cutoff  : float between 0 and 1

   Cut-off used in clustering flagged points into rectangular patches for
   refinement.  Clusters are chosen to minimize the number of patches
   subject to the constraint::

      (# flagged pts) / (total # of cells refined) < clustering_cutoff

   If `clustering_cutoff` is close to 1, only flagged cells will be refined,
   which could lead to many `1 x 1` patches.  

   The default value 0.7 usually works well.
   
.. attribute:: verbosity_regrid : int

   Additional information is printed to the terminal each time regridding is
   done at this level or coarser.  Set to 0 to suppress regridding output.

.. attribute:: regions : list

   List of lists of the form
   `[minlevel,maxlevel,t1,t2,x1,x2,y1,y2]`.
   See :ref:`refinement_regions`.  
   This attribute may be phased out in the future in favor of `flagregions`,
   but currently both are supported.

.. attribute:: flagregions : list

   (Introduced in v5.7.0)
   List of objects of class `clawpack.amrclaw.data.FlagRegion` that specify
   regions where further adaptive refinement is either forced or forbiddne.
   These objects are more flexible than the
   older `regions` lists and are now preferred.  See :ref:`flagregions`.

.. attribute:: max1d : int

   The maximum size (in each spatial dimension) of any grid patch.  If
   a larger region must be refined then it it split into multiple patches.
   This can be tuned if desired based on cache size and OMP efficiency
   (recall that multiple patches can be advanced in time in parallel).
   For debugging it may also be useful to vary this parameter.
   For most cases the default values work fine: 500 in 1D, 60 in 2D, 32 in 3D.

.. attribute:: memsize : int

   The initial length of the `alloc` array used internally in AMRClaw for
   dynamic allocation of grid patch data.  The default values depend on
   the number of space dimensions and may be large enough.  If the
   `alloc` array is not long enough, then Fortran's dynamic memory
   allocation will be used to double the size of this array and copy over
   all previous data, so it is not necessary to specify a value unless you
   are running a large problem and are concerned about the time spent
   repeatedly doubling and copying.  The default values are::

       2**20 - 1 = 1048575 in 1D, 
       2**22 - 1 = 4194303 in 2D, 
       2**23 - 1 = 8388607 in 3D.  

   These are chosen so that repeated doubling can get as close to `2**30 - 1` as
   possible, the limit of `int*4` array indices.  The code will crash if 
   more memory is needed, in which case you may have to recompile with
   `int*8` index variables.

   



Debugging flags for additional printing
---------------------------------------

Setting one or more of these to `True` will cause additional information to
be written to the file `fort.amr` in the output directory.
    
.. attribute:: dprint : boolean

   Print domain flags

.. attribute:: eprint : boolean

   Print error estimation flags

.. attribute:: edebug : boolean

   Print even more error estimation flags

.. attribute:: gprint : boolean

   Print grid bisection and clustering information

.. attribute:: nprint : boolean

   Print proper nesting output

.. attribute:: pprint : boolean

   Print projection of tagged points

.. attribute:: rprint : boolean

   Print regridding summary

.. attribute:: sprint : boolean

   Print space/memory output

.. attribute:: tprint : boolean

   Print time step info on each level

.. attribute:: uprint : boolean

   Print update/upbnd information


