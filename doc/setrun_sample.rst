

.. _setrun_sample:

*****************************************************************
Sample `setrun.py` module for classic Clawpack
*****************************************************************

.. warning :: Need to update link?  Add 2d example?

This sample `setrun.py` script is from the example in
`$CLAW/classic/tests/advection`.

::

    """ 
    Module to set up run time parameters for Clawpack.

    The values set in the function setrun are then written out to data files
    that will be read in by the Fortran code.
        
    """ 

    import clawpack.clawutil.clawdata


    #------------------------------
    def setrun(claw_pkg='Classic'):
    #------------------------------
        
        """ 
        Define the parameters used for running Clawpack.

        INPUT:
            claw_pkg expected to be "Classic4" for this setrun.

        OUTPUT:
            rundata - object of class ClawRunData 
        
        """ 
        
        assert claw_pkg.lower() == 'classic',  "Expected claw_pkg = 'classic'"

        rundata = clawpack.clawutil.clawdata.ClawRunData(pkg=claw_pkg, num_dim=1)

        #------------------------------------------------------------------
        # Problem-specific parameters to be written to setprob.data:
        #------------------------------------------------------------------

        probdata = rundata.new_UserData(name='probdata',fname='setprob.data')
        probdata.add_param('u',     1.0,  'advection velocity')
        probdata.add_param('beta', 200.,  'Gaussian width parameter')

        
        #------------------------------------------------------------------
        # Standard Clawpack parameters to be written to claw.data:
        #------------------------------------------------------------------

        clawdata = rundata.clawdata  # initialized when rundata instantiated

        # ---------------
        # Spatial domain:
        # ---------------

        # Number of space dimensions:
        clawdata.num_dim = 1
        
        # Lower and upper edge of computational domain:
        clawdata.lower[0] = 0.0
        clawdata.upper[0] = 1.0

        # Number of grid cells:
        clawdata.num_cells[0] = 100
        
        

        # ---------------
        # Size of system:
        # ---------------

        # Number of equations in the system:
        clawdata.num_eqn = 1

        # Number of auxiliary variables in the aux array (initialized in setaux)
        clawdata.num_aux = 0
        
        # Index of aux array corresponding to capacity function, if there is one:
        clawdata.capa_index = 0
        
        
        
        # -------------
        # Initial time:
        # -------------

        clawdata.t0 = 0.0


        # Restart from checkpoint file of a previous run?
        # Note: If restarting, you must also change the Makefile to set:
        #    RESTART = True
        # If restarting, t0 above should be from original run, and the
        # restart_file 'fort.chkNNNNN' specified below should be in 
        # the OUTDIR indicated in Makefile.

        clawdata.restart = False               # True to restart from prior results
        clawdata.restart_file = 'fort.chk00006'  # File to use for restart data
        
        
        # -------------
        # Output times:
        #--------------

        # Specify at what times the results should be written to fort.q files.
        # Note that the time integration stops after the final output time.
        # The solution at initial time t0 is always written in addition.

        clawdata.output_style = 1

        if clawdata.output_style == 1:
            # Output nout frames at equally spaced times up to tfinal:
            clawdata.num_output_times = 10
            clawdata.tfinal = 1.0
            clawdata.output_t0 = True  # output at initial (or restart) time?

        elif clawdata.output_style == 2:
            # Specify a list of output times.  
            clawdata.tout =  [0.5, 1.0]   # used if output_style == 2
            clawdata.num_output_times = len(clawdata.tout)

        elif clawdata.output_style == 3:
            # Output every iout timesteps with a total of ntot time steps:
            clawdata.output_step_interval = 1
            clawdata.total_steps = 5
            clawdata.output_t0 = True
            

        clawdata.output_format == 'ascii'      # 'ascii' or 'netcdf' 

        clawdata.output_q_components = 'all'   # could be list such as [True,True]
        clawdata.output_aux_components = 'none'  # could be list
        clawdata.output_aux_onlyonce = True    # output aux arrays only at t0
        


        # ---------------------------------------------------
        # Verbosity of messages to screen during integration:  
        # ---------------------------------------------------

        # The current t, dt, and cfl will be printed every time step
        # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
        #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
        clawdata.verbosity = 1
        
        

        # --------------
        # Time stepping:
        # --------------

        # if dt_variable==1: variable time steps used based on cfl_desired,
        # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
        clawdata.dt_variable = True
        
        # Initial time step for variable dt.  
        # If dt_variable==0 then dt=dt_initial for all steps:
        clawdata.dt_initial = 0.8 / float(clawdata.num_cells[0])
        
        # Max time step to be allowed if variable dt used:
        clawdata.dt_max = 1e+99
        
        # Desired Courant number if variable dt used, and max to allow without 
        # retaking step with a smaller dt:
        clawdata.cfl_desired = 0.9
        clawdata.cfl_max = 1.0
        
        # Maximum number of time steps to allow between output times:
        clawdata.steps_max = 500

        
        

        # ------------------
        # Method to be used:
        # ------------------

        # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
        clawdata.order = 2
        
        # Use dimensional splitting?
        clawdata.dimensional_split = 0
        
        # For unsplit method, transverse_waves can be 
        #  0 or 'none'      ==> donor cell (only normal solver used)
        #  1 or 'increment' ==> corner transport of waves
        #  2 or 'all'       ==> corner transport of 2nd order corrections too
        clawdata.transverse_waves = 0
        
        # Number of waves in the Riemann solution:
        clawdata.num_waves = 1
        
        # List of limiters to use for each wave family:  
        # Required:  len(limiter) == num_waves
        # Some options:
        #   0 or 'none'     ==> no limiter (Lax-Wendroff)
        #   1 or 'minmod'   ==> minmod
        #   2 or 'superbee' ==> superbee
        #   3 or 'mc'       ==> MC limiter
        #   4 or 'vanleer'  ==> van Leer
        clawdata.limiter = ['mc']

        clawdata.use_fwaves = False    # True ==> use f-wave version of algorithms
        
        # Source terms splitting:
        #   src_split == 0 or 'none'    ==> no source term (src routine never called)
        #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
        #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
        clawdata.source_split = 'none'
        

        # --------------------
        # Boundary conditions:
        # --------------------

        # Number of ghost cells (usually 2)
        clawdata.num_ghost = 2
        
        # Choice of BCs at xlower and xupper:
        #   0 => user specified (must modify bcN.f to use this option)
        #   1 => extrapolation (non-reflecting outflow)
        #   2 => periodic (must specify this at both boundaries)
        #   3 => solid wall for systems where q(2) is normal velocity
        
        clawdata.bc_lower[0] = 2
        clawdata.bc_upper[0] = 2
        
        return rundata
        # end of function setrun
        # ----------------------


    if __name__ == '__main__':
        # Set up run-time parameters and write all data files.
        import sys
        if len(sys.argv) == 2:
        rundata = setrun(sys.argv[1])
        else:
        rundata = setrun()

        rundata.write()
        
