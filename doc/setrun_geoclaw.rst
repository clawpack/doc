

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
example  :ref:`setrun_geoclaw_sample`.

See also the sample codes in the directory `$CLAW/geoclaw/examples/tsunami`.
  

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
    
.. attribute:: rundata.refinement_data.max_level_deep : int

   For simulations over the ocean, it is often useful to specify
   a *maximum refinement level* allowed in deep parts of the ocean.  This is
   useful if a high level of refinement is specified on some rectangular
   region but only the parts of this region near the shore actually need to
   be refined.

.. attribute:: rundata.refinement_data.max_level_deep : float

   The deepness that triggers the refinement limitation imposed by
   `max_level_deep` above.


General geo parameters
----------------------

`rundata.geo_data` has the following additional attributes:

.. attribute:: gravity : float

   gravitational constant in m/s**2, e.g.  *gravity = 9.81*.

.. attribute:: coordinate_system : integer

   *coordinate_system = 1* for Cartesian x-y in meters, 
   
   *coordinate_system = 2* for latitude-longitude on the sphere.

.. attribute:: earth_radius : float

   radius of the earth in meters, e.g.  *earth_radius = 6367.5e3*.

.. attribute:: coriolis_forcing : bool

   *coriolis_forcing = True* to include Coriolis terms in momentum equations

   *coriolis_forcing = False* to omit Coriolis terms (usually fine for tsunami modeling)
   

.. attribute:: sea_level : float

   sea level (often *sea_level = 0.*)  
   This is relative to the 0 vertical datum of the topography files used.
   It is important to set this properly for tsunami applications, see
   :ref:`sealevel`.


.. attribute:: friction_forcing : bool

   Whether to apply friction source terms in momentum equations.
   See :ref:`manning` for more discussion of the next four parameters.

.. attribute:: manning_coefficient : float

   For friction source terms, the Manning coefficient.  By default this
   value will be used everywhere unless `manning_coefficient_onshore` is
   set to a different value, in which case this value will be used only
   where the topo satisfies `B < friction_shore_level`.

.. attribute:: manning_coefficient_onshore : float

   Optional second Manning coefficient to use "onshore", 
   where the topo satisfies `B >= friction_shore_level`.
   If not set, it will default to the same value as `manning_coefficient`.

.. attribute:: friction_shore_level : float

   For friction source terms, the value used to determine whether a cell
   is "onshore" or "offshore", in cases where different Manning coefficients
   are desired in the two cases.  The default value is 0.

.. attribute:: friction_depth : float

   Friction source terms are only applied in water shallower than this,
   i.e. if `h < friction_depth`, 
   since they have negligible effect in deeper water.

.. _setrun_topo:

Topography data file parameters
-------------------------------

See :ref:`topo` for more information about specifying topography (and
bathymetry) data files in GeoClaw.


.. attribute:: rundata.topo_data.topofiles : list of lists

   *topofiles* should be a list of the form *[file1info, file2info, etc.]*
   where each element is itself a list of the form 

     [topotype, minlevel, maxlevel, t1, t2, fname]

   with values

     *topotype* : integer

       1,2 or 3 depending on the format of the file (see :ref:`topo`).

     *minlevel* : integer

       the minimum refinement level that should be enforced in the region
       covered by this grid (for times between *t1* and *t2*).

     *maxlevel* : integer

       the maximum refinement level that should be allowed in the region
       covered by this grid (for times between *t1* and *t2*).
     
     *t1, t2* : floats

       the time interval over which refinement should be controlled.

     *fname* : string

       the name of the topo file.

    For more about controlling AMR in various regions, see :ref:`regions`.

.. attribute:: dtopofiles : list of lists

   Information about topography displacement files, giving perturbations to
   topography generated by an earthquake, for example.

   *dtopofiles* should be a list of the form *[]* or *[file1info]*
   where each element (currently at most 1 is allowed!)
   is itself a list of the form 

     [dtopotype, minlevel, maxlevel, fname]

   with values

     *dtopotype* : integer

       1 or 3 depending on the format of the file (see :ref:`topo_dtopo`).

     *minlevel* : integer

       the minimum refinement level that should be enforced in the region
       covered by this grid.

     *maxlevel* : integer

       the maximum refinement level that should be allowed in the region
       covered by this grid.
     
     *fname* : string

       the name of the dtopo file.  See :ref:`topo_dtopo` for information about
       the format of data in this file.


.. _setrun_qinit:

qinit data file parameters
-------------------------------

A modification to the initial data specified by default can be made as
described at :ref:`qinit_file`.

.. attribute:: iqinit : integer

   Specifies what type of perturbation is stored in the *qinitfile*, 
   see :ref:`qinit_file` for more information.  Valid values for *iqinit*
   are
   
    - 0 = No perturbation specified
    - 1 = Perturbation to depth *h*
    - 2 = Perturbation to x-momentum *hu*
    - 3 = Perturbation to y-momentum *hv*
    - 4 = Perturbation to surface level


.. attribute:: qinitfiles : list of lists

   *qinitfiles* should be a list of the form *[]* or *[file1info]*
   where each element (currently at most 1 is allowed!)
   is itself a list of the form 

     [minlevel, maxlevel, fname]

   with values

     *minlevel* : integer

       the minimum refinement level that should be enforced in the region
       covered by this grid.

     *maxlevel* : integer

       the maximum refinement level that should be allowed in the region
       covered by this grid.
     
     *fname* : string

       the name of the qinitdata file.  See :ref:`topo` for information about
       the format of data in this file.

See :ref:`qinit_file` for more details about the format.


.. _setrun_regions:

AMR refinement region parameters
--------------------------------

.. attribute:: regions : list of lists

   **Note:** this should become a more general AMR parameter.

   *regions* should be a list of the form *[region1info, region2info, etc.]*
   where each element is itself a list of the form 

     [minlevel, maxlevel, t1, t2, x1, x2, y1, y2]

   with values

     *minlevel* : integer

       the minimum refinement level that should be enforced in the region
       covered by this grid (for times between *t1* and *t2*).

     *maxlevel* : integer

       the maximum refinement level that should be allowed in the region
       covered by this grid (for times between *t1* and *t2*).
     
     *t1, t2* : floats

       the time interval over which refinement should be controlled.

     *x1, x2, y1, y2* : floats
       
       the spacial extent of this region.

    For more about controlling AMR in various regions, see :ref:`regions`.

.. _setrun_guages:

Gauge parameters
----------------

.. warning :: Needs updating

.. attribute:: gauges : list of lists

   **Note:** this should become a more general AMR parameter.

   *gauges* should be a list of the form *[gauge1info, gauge2info, etc.]*
   where each element is itself a list of the form 

     [gaugeno, x, y, t1, t2]

   with values

     *gaugeno* : integer

       the number of this gauge

     *x, y* : floats

       the location of this gauge

     *t1, t2* : floats

       the time interval over which gauge data should be output.

   For more about gauges, see :ref:`gauges`.

.. _setrun_fixedgrids:

Fixed grid output parameters
----------------------------

.. attribute:: fixedgrids : list of lists

   **Note:** this might become a more general AMR parameter.

   This can be used to specify a set of grids where output should be
   produced at the specified resolution regardless of how the AMR grids look
   at each time.  Interpolation from the best available grid near each point
   is used.  This is useful for comparing AMR output to results obtained
   with other codes that use a fixed grid.  


   *fixedgrids* should be a list of the form *[grid1info, grid2info, etc.]*
   where each element is itself a list of the form 

     [t1, t2, x1, x2, y1, y2, xpoints, ypoints]

   with values
     
     *t1, t2* : floats

       the time interval over which output should be written for this grid.

     *x1, x2, y1, y2* : floats
       
       the spacial extent of this grid.

     *xpoints, ypoints* : floats

       the number of grid points in the x and y directions (the grid will
       include *x1*, *x2* and *xpoints-2* points in between, for example).


.. _setrun_fixedgrids2:

Fixed grid (version 2) output parameters
-----------------------------------------

.. warning :: Needs updating
