

.. _setrun_geoclaw:

*****************************************************************
Specifying GeoClaw parameters in `setrun.py`
*****************************************************************


Since :ref:`geoclaw` is a modified version of :ref:`amrclaw`, 
all of the parameters that
are required for AMRClaw are also needed by GeoClaw.  See
:ref:`setrun_amrclaw` for a discussion of these, and :ref:`setrun` for a
description of `setrun.py` input scripts more generally.

In addition, a number of other parameters should be set in the `setrun.py`
file in any :ref:`geoclaw` application.
See also the :ref:`geohints` for more about parameter choices.

It is best to look at a specific example while reading this section, for
example in one of the subdirectories of `$CLAW/geoclaw/examples/tsunami`.
  

The function `setrun` in this module is essentially the same as for AMRClaw,
except that it expects to be called with *claw_pkg = 'geoclaw'*.  This call
should be performed properly by the Makefile if you have *CLAW_PKG =
geoclaw* set properly there.

.. comment

  The section :ref:`setrun_geoclaw_sample_parameters` 

The new section :ref:`setrun_setgeo` 
in this module contains the new GeoClaw parameters.

A brief summary of these:

Additional AMR parameters
--------------------------

In addition to the standard AMRClaw parameters described in
:ref:`setrun_amrclaw`, some additional parameters governing how refinement
is done should be specified for GeoClaw applications:  

.. attribute:: rundata.refinement_data.variable_dt_refinement_ratios : bool

    The default is False, in which case refinement factors in time
    are specified by the user as usual in the array 
    `rundata.amrdata.refinement_ratios_t`.

    When True, this indicates that GeoClaw should automatically choose
    refinement factors in time on each level based on an estimate of the maximum
    wave speed on all grids at this level.  For most hyperbolic problems the CFL
    condition suggests that one should refine in time by the same factor as in
    space.  However, for GeoClaw applications where fine grids appear only in
    shallow coastal regions this may not be the case.  

.. attribute:: rundata.refinement_data.wave_tolerance : float

   Cells are flagged for refinement if the difference between the surface
   elevation and sea level is larger than this tolerance.  Note that whether
   refinement is actually done depends also on how various AMR regions have
   been set (see Section :ref:`regions`) and also on several other
   attributes described below that contain information on minimum and
   maximum refinement allowed in various regions.


.. attribute:: rundata.refinement_data.speed_tolerance : list

   Cells are flagged for refinement at a level if the magnitude of the 
   velocity is greater than the corresponding value in the list.  For 
   instance if `rundata.refinement_data.speed_tolerance = [1.0, 2.0, 3.0]`
   then cells with a speed of 1.0 would refine to level 2, cells with a 
   speed of 2.0 would refine to level 3, and cells with a speed of 3.0
   would refine to level 4.
    

.. _setrun_geo:

General geo parameters
----------------------

`rundata.geo_data` has the following additional attributes:

.. attribute:: rundata.geo_data.gravity : float

   gravitational constant in m/s**2, e.g.  *gravity = 9.81*.

.. attribute:: rundata.geo_data.coordinate_system : integer

   *coordinate_system = 1* for Cartesian x-y in meters, 
   
   *coordinate_system = 2* for latitude-longitude on the sphere.

.. attribute:: rundata.geo_data.earth_radius : float

   radius of the earth in meters, e.g.  *earth_radius = 6367.5e3*.

.. attribute:: rundata.geo_data.coriolis_forcing : bool

   *coriolis_forcing = True* to include Coriolis terms in momentum equations

   *coriolis_forcing = False* to omit Coriolis terms (usually fine for tsunami modeling)
   

.. attribute:: rundata.geo_data.sea_level : float

   sea level (often *sea_level = 0.*)  
   This is relative to the 0 vertical datum of the topography files used.
   It is important to set this properly for tsunami applications, see
   :ref:`sealevel`.


.. attribute:: rundata.geo_data.friction_forcing : bool

   Whether to apply friction source terms in momentum equations.
   See :ref:`manning` for more discussion of the next three parameters.

.. attribute:: rundata.geo_data.friction_depth : float

   Friction source terms are only applied in water shallower than this,
   i.e. if `h < friction_depth`, 
   assuming they have negligible effect in deeper water.

.. attribute:: rundata.geo_data.manning_coefficient : float or list of floats

   For friction source terms, the Manning coefficient.  If a single value
   is given, this value will be used where ever h < friction_depth.
   If a list of values is given, then the next parameter delineates the
   regions where each is used based on values of the topography B.

.. attribute:: rundata.geo_data.manning_break : list of floats

   If manning_coefficient is a list of length N, then this should be a 
   monotonically increasing list
   of length N-1 giving break points in the topo B used to determine where
   each Manning coefficient is used.

   For example, if ::

        manning_coefficient = [0.025, 0.06]
        manning_break = [0.0]

   then 0.025 will be used where B<0 and 0.06 used where B>0.  
   (Subject still to the restriction that no friction is applied 
   where h >= friction_depth.)


.. _setrun_topo:

Topography data file parameters
-------------------------------

See :ref:`topo` for more information about specifying topography (and
bathymetry) data files in GeoClaw.


.. attribute:: rundata.topo_data.topofiles : list of lists

   *topofiles* should be a list of the form *[file1info, file2info, etc.]*
   where each element is itself a list of the form 

     [topotype, fname]

   with values

     *topotype* : integer

       1,2 or 3 depending on the format of the file (see :ref:`topo`).

     *fname* : string

       the name of the topo file.

    **Note:** Starting in v5.8.0 implicitly specifying a flag region for
    AMR is no longer supported in the specification of a topo file.
    For more about controlling AMR in various regions, see :ref:`flagregions`.

.. attribute:: rundata.dtopo_data.dtopofiles : list of lists

   Information about topography displacement files, giving perturbations to
   topography generated by an earthquake, for example.

   *dtopofiles* should be a list of the form *[]* or *[file1info]*
   where each element (currently at most 1 is allowed!)
   is itself a list of the form 

     [dtopotype, fname]

   with values

     *dtopotype* : integer

       1 or 3 depending on the format of the file (see :ref:`topo_dtopo`).

     *fname* : string

       the name of the dtopo file.  See :ref:`topo_dtopo` for information about
       the format of data in this file.

    **Note:** Starting in v5.8.0 implicitly specifying a flag region for
    AMR is no longer supported in the specification of a dtopo file.
    For more about controlling AMR in various regions, see :ref:`flagregions`.


.. attribute:: rundata.dtopo_data.dt_max_dtopo : float

   the maximum time step allowed during the time interval over which the 
   topography is moving.  This is assumed to start at time `t0` and to
   extend to the maximum time that any of the dtopo files specified is
   active.  This avoids issues where the time step selected by the CFL
   condition is much larger than the time scale over which the topography
   changes.  You must also set `rundata.clawdata.dt_initial` to the same
   value (or smaller) to insure that the first time step is sufficiently small.

.. _setrun_qinit:

qinit data file parameters
-------------------------------

A modification to the initial data specified by default can be made as
described at :ref:`qinit_file`.

.. attribute:: rundata.qinit_data.qinit_type : integer

   Specifies what type of perturbation is stored in the *qinitfile*, 
   see :ref:`qinit_file` for more information.  Valid values for *qinit_type*
   are
   
    - 0 = No perturbation specified
    - 1 = Perturbation to depth *h*
    - 2 = Perturbation to x-momentum *hu*
    - 3 = Perturbation to y-momentum *hv*
    - 4 = Perturbation to surface level


.. attribute:: rundata.qinit_data.qinitfiles : list of lists

   *qinitfiles* should be a list of the form *[]* or *[file1info]*
   where each element (currently at most 1 is allowed!)
   is itself a list of the form 

     [fname]

   with values

     *fname* : string

       the name of the qinitdata file.  See :ref:`topo` for information about
       the format of data in this file.

    **Note:** Starting in v5.8.0 implicitly specifying a flag region for
    AMR is no longer supported in the specification of a dtopo file.
    For more about controlling AMR in various regions, see :ref:`flagregions`.


See :ref:`qinit_file` for more details about the format.

Force some cells to be initially dry
-------------------------------------

.. attribute:: rundata.qinit_data.force_dry_list: list of `clawpack.geoclaw.data.ForceDry` objects

Normally the finite volume cells with topography values below sea level (as
specified by `rundata.geo_data.sea_level`) are initialized as wet, with the
depth of water `h` needed to bring the surface eta to sea level.  If the
computational domain includes regions where there is dry land below sea level
(e.g. behind a dike or levy), then these regions can be specified via this
attribute. See :ref:`force_dry`.

Adjust sea level in some regions
--------------------------------

.. attribute:: rundata.qinit_data.variable_eta_init: logical

Normally a single constant value of sea level 
(specified by `rundata.geo_data.sea_level`) is used to initialize the
depth of water required to bring the surface eta to sea level.
Sometimes sea level should have different values in different locations,
e.g. for an inland lake with surface level above the ocean level, or in
regions where coseismic uplift or subsidence moves the original water
vertically.  If so, set this attribute to `True` and see :ref:`set_eta_init`
for more discussion on how to proceed.
    

.. _setrun_regions:

AMR refinement region parameters
--------------------------------


    As in AMRClaw (see :ref:`setrun_amrclaw`),
    one can specify `regions` and/or `flagregions` to control flagging cells
    for refinement to the next level.  
    See :ref:`refinement_regions` and :ref:`flagregions` for more details.

.. attribute:: rundata.regiondata.regions: list of regions

    An old style `region` is a list of the form

        `[minlevel,maxlevel,t1,t2,x1,x2,y1,y2]`

    See :ref:`refinement_regions` for more details.

.. attribute:: rundata.regiondata.flagregions: list of flagregions

    A new style `flagregion` is an object of class 
    `clawpack.amrclaw.data.FlagRegion`. 
    See :ref:`flagregions` for more details.


.. _setrun_fixedgrids:

Deprecated Fixedgrid output parameters
---------------------------------------

.. attribute:: rundata.fixedgrids : list of lists

   **Removed from GeoClaw as of v5.9.0.**  
   Use :ref:`setrun_fgmax` and/or :ref:`setrun_fgout` instead, 
   see below.


.. _setrun_fgmax:

Fixed grid maximum monitoring / arrival times
---------------------------------------------

.. attribute:: rundata.fgmax_grids : list of clawpack.geoclaw.fgmax_tools.FGoutGrid
   objects.


   This can be used to specify a set of grids on which to monitor the
   maximum flow depth (or other quantities) observed over the course of
   the computation, and/or the arrival time of the flow or wave.


   The "grids" also do not have to be rectangular grids aligned with the
   coordinate directions, but can consist of an arbitrary list of points
   that could also be points along a one-dimensional transect or points
   following a coastline, for example.

   You can set these via e.g.::
    
        from clawpack.geoclaw import fgmax_tools
        fgmax_grids = rundata.fgmax_data.fgmax_grids  # empty list initially

        fgmax = fgmax_tools.FGmaxGrid()
        # set fgmax attributes
        fgmax_grids.append(fgmax)    # written to fgmax_grids.data

        # repeat for additional fgout grids if desired

   See :ref:`fgmax` for more details.

.. attribute:: rundata.fgmax_data.num_fgmax_val : int

   Should take the value 1, 2, or 5 and indicates how many values to monitor.
   See :ref:`fgmax` for more details.

.. _setrun_fgout:

Fixed grid output
-----------------

.. attribute:: rundata.fgout_grids : list of clawpack.geoclaw.fgout_tools.FGoutGrid
   objects.

   You can set these via e.g.::
    
        from clawpack.geoclaw import fgout_tools
        fgout_grids = rundata.fgout_data.fgout_grids  # empty list initially

        fgout = fgout_tools.FGoutGrid()
        # set fgout attributes
        fgout_grids.append(fgout)    # written to fgout_grids.data

        # repeat for additional fgout grids if desired

   See :ref:`fgout` for more details.

.. _setrun_surge:

Storm Specification Data
------------------------

.. attribute:: rundata.surge_data.wind_forcing : bool

   Includes the wind forcing term if `True`.  The drag coefficient is specified
   by `rundata.surge_data.drag_law`.

.. attribute:: rundata.surge_data.drag_law : integer

   This specifies how to deterimine the wind drag coefficient.  Valid options
   include include `0` implying use no wind drag (effectively eliminates the
   wind source term but still computes the wind), `1` uses the Garret wind
   drag law, and `2` uses the Powell (2006) wind drag law.

.. attribute:: rundata.surge_data.pressure_forcing : bool

   Includes the pressure forcing term if `True`.

.. attribute:: rundata.surge_data.wind_index : int

   Specifies at what index into the `aux` array the wind velocities are stored.
   Note that this is Python indexed in the setrun but will be corrected in the
   FORTRAN code (1 is added to the index).

.. attribute:: rundata.surge_data.pressure_index : int

   Specifies at what index into the `aux` array the wind velocities are stored.
   Note that this is Python indexed in the setrun but will be corrected in the
   FORTRAN code (1 is added to the index).

.. attribute:: rundata.surge_data.display_landfall_time : bool

   Sets whether the console output displays time relative to land fall in days.
   In GeoClaw versions past 5.5 this only deterimines whether the time is 
   displayed in seconds or days.

.. attribute:: rundata.surge_data.wind_refine : list

   Similar to the `speed_tolerance` data, cells are flagged for refinement at 
   a level if the magnitude of the wind velocity in m/s is greater than the 
   corresponding value in the list.  For 
   instance if `wind_refine = [20.0, 30.0, 40.0]`
   then cells with a wind speed of 20.0 would refine to level 2, cells with a 
   wind speed of 30.0 would refine to level 3, and cells with a wind speed of 
   40.0 would refine to level 4.  This can also be set to a boolean which if
   `False` disables wind based refinement.

.. attribute:: rundata.surge_data.R_refine : list

   Similar to the `wind_refine` data, cells are flagged based on the radial
   distance to the storm's center.  This can also be set to a boolean which if
   `False` disables storm radial based refinement.

.. attribute:: rundata.surge_data.storm_specification_type : int

   Specifies the type of storm being used.  Positive options refer to a 
   parameterized storm model where as negative integers refer to fully 
   specified storms, for instance from HWRF, to be specified.

   Valid options 

    - `-1`: The input data is specified in the HWRF format.
    - `0`: No storm specified
    - `1`: Parameterized storm requested using the Holland 1980 modeled storm.
    - `2`: Parameterized storm requested using the Holland 2010 modeled storm.
    - `3`: Parameterized storm requested using the Chava, Lin, Emmanuel modeled 
      storm.

.. attribute:: rundata.surge_data.storm_file : string

   Specifies the path to the storm data.  IF `storm_specification_type > 0` then
   this should point to a GeoClaw formatted storm file (see :ref:`storm_module` for 
   details).  If `storm_specification < 0` then this should either specify a path
   to files specifying the storm or a single file depending on the type of input
   data.
