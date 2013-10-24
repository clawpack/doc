

.. _setrun:

*****************************************************************
Specifying classic run-time parameters in `setrun.py`
*****************************************************************



It may be useful to look at a specific example, e.g. 
:ref:`setrun_sample`.

**Note:** Many parameters have changed name since Version 4.X and some new
ones have been added.  See :ref:`setrun_changes` for a summary.

To convert a Version 4.x `setrun.py` file to Version 5.0, see :ref:`claw46to50`.


Input
-----

`setrun` takes a single argument `claw_pkg` that should be set to `classic`.

Output
------

`rundata`, an object of class `ClawRunData`, created in the
setrun file with the commands::

       from clawpack.clawutil import clawdata 
       rundata = clawdata.ClawRunData(claw_pkg, num_dim)

The `rundata` object has an attribute `rundata.clawdata` whose
attributes are described below.


This section explains the parameters needed for the classic single-grid
Clawpack code.  Additional parameters are needed by extensions of the code.
For these, see:

 * AMRClaw (adaptive mesh refinement): :ref:`setrun_amrclaw`

 * GeoClaw (geophysical flows): :ref:`setrun_geoclaw`


Run-time parameters
-------------------

The parameters needed in 1 space dimension (*ndim=1*) are described.  In 2d
and 3d there are analogous parameters in y and z required, as mentioned
below.

.. attribute:: num_dim : integer from [1,2,3]

   number of space dimensions.  


.. attribute:: lower : list of floats

   lower limits in the x, [y,z]  directions.   

.. attribute:: upper : list of floats

   upper limits in the x, [y ,z]  directions.   


.. attribute:: num_cells : list of integers

   The number of grid cells in the x, [y, ,z]  directions.

   Note that when AMR is used, `num_cells` determines the number of cells in 
   each dimension on the coarsest Level 1 grid.  Additional parameters
   described below determine refinement ratios to finer levels.

.. attribute:: num_eqn : integer

   Number of equations in the system (e.g. *num_eqn=1* for a scalar problem).

.. attribute:: num_aux : integer

   Number of auxiliary variables in the aux array (initialized in `setaux.f`)

.. attribute:: capa_index : integer

   Index of aux array corresponding to capacity function, if there is one.

.. attribute:: t0 : float

   Initial time, often *t0 = 0.*

.. attribute:: restart : boolean

   **Currently only available in amrclaw and geoclaw.**

   Set True to restart a previous computation.  To use this option, 
   see :ref:`restart`.  Note that a change in the `Makefile` is also
   required.

.. attribute:: restart_file : str

   If `restart == True` then this should be the name of the checkpoint 
   file containing all the information needed to do a restart.  This will
   generally be of the form `fort.chkNNNNN` where `NNNNN` is the (coarse
   grid) timestep from the previous computation to restart from. 
   This file is assumed to be in the directory specified for output from
   this run.
   See :ref:`restart` for more details.

   
.. attribute:: output_style: integer

   There are three possible ways to specify the output
   times.   This parameter selects the desired manner to specify the times,
   and affects what other attributes are required.

     * *output_style = 1* : Output at fixed time intervals.

       Requires additional parameters:

       * `num_output_times` : integer, number of output times
       * `tfinal` : float, final time
       * `output_t0` : boolean, whether to also output at initial time `t0`.

       The time steps will be adjusted to hit these times exactly. (Provided
       *dt_variable = True*.  Otherwise *dt_initial* must divide
       *tfinal/num_output_times* an integer number of times.)

     * *output_style = 2*  : Output at specified times.

       Requires the additional parameter:

       * `output_times` : list of floats,
         times to output (include `t0` explicitly if desired)

     * *output_style = 3*  : Output every so many steps.
       Most often used for debugging, e.g to output every time step.

       Requires additional parameters:

       * `output_step_interval` : integer, number of steps between outputs
       * `total_steps` : integer, total number of steps to take
       * `output_t0` : boolean, whether to also output at initial time `t0`.


.. attribute:: output_format: str

   Format of output.  Currently the following are supported:

   * `'ascii'` : the files `fort.q0000` etc. are ASCII files.
   * `'binary'` : Raw binary dump.  Working??
   * `'netcdf'` : NetCDF format.  Working??

.. attribute:: output_q_components: list of booleans or str

   * A list such as `[1,0,1]` would indicate to output `q[0]` and `q[2]` only.
     *This might not be working yet.*

   * The string `'all'` indicates that all components should be output
   * The string `'none'` indicates that no components should be output

.. attribute:: output_aux_components: list of booleans or str

   * A list such as `[1,0,1]` would indicate to output `aux[0]` and `aux[2]` only.
     *This might not be working yet.*

   * The string `'all'` indicates that all components should be output
   * The string `'none'` indicates that no components should be output

.. attribute:: output_aux_onlyonce: boolean

   If `output_aux_components` is not `'none'` or an empty list, this
   indicates whether `aux` arrays should be only output at time `t0` or at
   every output time.  The latter is generally necessary for AMR
   applications unless the grids never change (and the component of `aux`
   are never modified except in `setaux`).

.. attribute:: verbosity: integer >= 0 

   A line of output (reporting t, dt and CFL number) is written to the
   terminal every time step, but only at Level `verbosity` or coarser.

   Set to 0 to suppress all such output.


.. attribute:: dt_initial: float >= 0. 

   Initial time step to try in first step.  If using `dt_variable == True`
   and are unsure of an appropriate
   timestep, set to a very small value (e.g. `1.e-10`).  After the first
   step the wave speeds observed in all Riemann solutions will be used to
   set the time step appropriately for the next step.
   

.. attribute:: dt_variable: boolean

   If True, time steps are adjusted automatically based on the desired
   Courant number *cfl_desired*.  

   If False, fixed time steps of lenght *dt_initial* are used.

.. attribute:: dt_max: float >= 0.

   If *dt_variable = True* then this is an upper bound on the allowable time
   step regardless of the Courant number.  Useful if there are other reasons
   to limit the time step (e.g. stiff source terms).

.. attribute:: cfl_desired: float >= 0.

   If *dt_variable = True* then this is the desired Courant number.  Time
   steps will be adjusted based on the maximum wave speed seen in the *last*
   time step taken.  For a nonlinear problem this may not result in the
   Courant number being exactly the desired value in the next step.

   Usually *cfl_desired = 0.9* or less.

.. attribute:: cfl_max: float

   If *dt_variable = True* then this is the maximum Courant number that can
   be allowed.  If a time step results in a Courant number that is greater
   than *cfl_desired* but less than or equal to *cfl_max*, the step is
   accepted.  If the Courant number is greater than *cfl_max* then the step
   is rejected and a smaller step is taken.  (At this point the maximum wave
   speed from Riemann solutions is known, so the step can be adjusted to
   exactly hit the desired value *cfl_desired*.)

   **Note:** With AMRClaw it is impossible to retake a step and so if
   `cfl > cfl_max` then a warning message is printed and the computation 
   continues.  *Note that results may be contaminated if the Courant number
   is much above 1.*
   This means that with AMR it is important to choose an appropriate time
   step  `dt_initial` for the first time step, or use a very small value.

   Usually *cfl_max = 1.0* is fine, e.g. 500000.
   
.. attribute:: steps_max: int

   Maximum number of time steps allowed between output times.  This is just
   to avoid infinite loops and generally a large value is fine.

.. attribute:: order : int

   `order == 1` : Use Godunov's method

   `order == 2` : Use second order corrections with limiters in normal
   direction.

.. attribute:: dimensional_split : str

   `dimensional_split == 'unsplit'`  is the only option currently allowed 
   for AMRClaw.

.. attribute:: transverse_waves : int or str

   `transverse_waves == 0 or 'none'` : No transverse correction terms
   (Donor cell upwind if also `order == 1`).

   `transverse_waves == 1 or 'increment'` : Only the increment waves are
   transmitted transversely.
   (Corner transport upwind if also `order == 1`,  should be second order
   accurate if `order == 2`).

   `transverse_waves == 2 or 'all'` : Corner tranpsort of second order
   corrections as well.  (Somewhat improved stability.)

.. attribute:: num_waves : int

   Number of waves the Riemann solver returns.

.. attribute:: limiter : list of int or str, of length num_waves

   Each element of the list can take the values:

    *   0 or 'none'     : no limiter (Lax-Wendroff)
    *   1 or 'minmod'   : minmod
    *   2 or 'superbee' : superbee
    *   3 or 'mc'       : monotonized central (MC) limiter
    *   4 or 'vanleer'  : van Leer

   See Chapter 6 of [LeVeque-FVMHP]_ for details.

.. attribute:: use_fwaves : boolean

   If True, the Riemann solvers should return f-waves (a decomposition of
   the the flux difference) rather than the usual waves (which give
   a decomposition of the jump in Q between adjacent states).
   See Section ?? of [LeVeque-FVMHP]_ 
   or [BaleLevMitRoss]_ for details.

.. attribute:: source_split : list of int or str, of length num_waves

   Determines form of fractional step algorithm used to apply source terms
   (if any).  Source terms must be implemented by providing a subroutine
   `srcN.f` (in `N` space dimensions) that is called each time step
   and should advance the solution by solving the source term equations
   (the PDE after dropping the hyperolic terms).

    *   src_split == 0 or 'none'    : no source term (`srcN` routine never called)
    *   src_split == 1 or 'godunov' : Godunov (1st order) splitting used, 
    *   src_split == 2 or 'strang'  : Strang (2nd order) splitting used.

   The Strang splitting requires calling the source term routine twice each
   time step (before and after the hyperbolic step, with half the time step)
   and is generally not recommended.  It is often no more accurate thn the
   Godunov splitting, requires more work, and can make it harder to properly 
   set ghost cells for boundary conditions.

.. attribute:: num_ghost : int

   number of ghost cells at each boundary.  Should be at least 1 if 
   `order == 1` and at least 2 if `order == 2`.

.. attribute:: bc_lower : list of int or str, of length num_ghost

   Choice of boundary conditions at the lower boundary in each dimension.
   Each element can take the following values:

    *   0 or 'user'     : user specified (must modify `bcNamr.f` to use this option)
    *   1 or 'extrap'   : extrapolation (non-reflecting outflow)
    *   2 or 'periodic' : periodic (must specify this at both boundaries)
    *   3 or 'wall'     : solid wall for systems where q(2) is normal velocity
    
    If the value is 0 or 'user', then the user must modify the boundary
    condition routine `bcNamr.f` to fill ghost cells in the desired manner.
    See :ref:`bc` for more details.

.. attribute:: bc_upper : list of int or str, of length num_ghost

   Choice of boundary conditions at the upper boundary in each dimension.
   The same choices are available as for `bc_lower`.

   Note that if periodic boundary conditions are specified at the lower
   boundary in some dimension then the same should be specified at the upper.

.. attribute:: checkpt_style :: int

   **Currently only available in amrclaw and geoclaw.**

   Specify how often checkpoint files should be created that can be used to
   restart a computation.
   See :ref:`restart` for more details.

     * *checkpt_style = 0* : Do not checkpoint at all
    
     * *checkpt_style = 1* : Checkpoint only at the final time.
    
     * *checkpt_style = 2* : Specify a list of checkpoint times. 

       This is generally **not** recommended because time steps will be 
       adjusted to hit the checkpoint times, but may be useful in order to
       create a checkpoint file just before some event of interest (e.g.
       when debugging a code that is known to crash at a certain time).

       Requires additional parameter:

       * checkpt_times : list of floats
    
     * *checkpt_style = 3* : Specify an interval for checkpointing.

       Requires additional parameter:

       * checkpt_interval : int

         Checkpoint every `checkpt_interval` time steps on Level 1 (coarsest
         level).

