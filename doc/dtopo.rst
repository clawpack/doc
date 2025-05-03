

.. _dtopo:

*****************************************************************
Moving topography displacement files
*****************************************************************

.. seealso::
   - :ref:`dtopotools_module`
   - :ref:`topo`
   - :ref:`tsunamidata`


For tsunami generation a *dtopo file* is often used to specify the
displacement of the topography relative to that specified in the topo files,
which are described in :ref:`topo`.  The dtopo file specifies the change in
topography over some region (by specifying the displacement on a grid of
points) either at a single time or at a sequence of times. Various file
formats are allowed, see :ref:`dtopo_formats` below.

This displacement might arise from various sources, including:

- An earthquake creating motion of the seafloor, specified as either a
  time history of the displacement might be available, or simply as the
  final static displacement at the end of the shaking (for an
  "instantaneous" event).

- A submarine landslide, slump, or mass flow, or
  a subareal landslide along the coast that strikes and enters the water.

In the latter case it is generally challenging to model the landslide motion
accurately and it is often necessary to use a fully coupled model that
includes the effect of the fluid motion on the landslide during its
evolution.  Such cases cannot be modeled simply by providing a dtopo file as
described here.  But in some cases it may be possible to run a separate
landslide model first and use the evolution of the surface to generate a
dtopo file that can then be used to generate a tsunami.  See
:ref:`landslides` for more details and an example.

The `D-Claw <https://dlgeorge.github.io/project/dclaw-project>`__ code
is an extension of GeoClaw that can model dense debris flows and some kinds
of landslides, including subareal landslides striking water and generating
a tsunami.  See :ref:`dclaw` for more details.

.. _dtopo_seismic:

dtopo files for earthquakes
---------------------------

Genearating a tsunami in GeoClaw often proceeds by specifying the vertical
motion of the seafloor at one or more times.  The entire water column in each
grid cell is then moved vertically by the same amount (or some filtering
may be applied, see below).  This creates a disturbance of the sea surface,
which in turn results in tsunami waves that propagate away from the source
region.

Calculating the seafloor deformation due to an earthquake usually starts by
specifying some amount of slip on a fault plane interior to the earth,
or more likely on a finite set of subfaults, each of
which is a planar rectangle or triangle, and which together better approximate
the fault surface for a complex fault.

There are three distinct ways of approximating seafloor deformation resulting
from an earthquake that are commonly used in GeoClaw:

 1. The **Okada model** is a simple approach in which the earth is assumed to be
    a homogeneous halfspace, with the earth's surface (and seafloor) at the
    top free surface.  The slip on a single subfault then results in a
    static deformation of the surface at some time after all the seismic waves
    have propagated away.  The Okada model can be applied to either a single
    rectangle or triangle, and then for a more complex fault the deformation due
    to each subfault is simply summed up, assuming linearity.  This approach
    does not model the shaking of the earthquake but the final static deformation
    is often sufficient to model the resulting tsunami.  This is often called
    a "static displacement" or "instantaneous displacement" model,
    since the earthquake is assumed to
    act at the same time on all subfaults and the final static deformation
    from each subfault is used immediately at the earthquake time (usually
    either at the time `t0` where the GeoClaw simulation starts or perhaps
    1 second later so that the initial flat ocean surface is also captured in
    the output).

 2. A **"kinematic" earthquake model** assigns slips to each subfault and also
    assigns a "rupture time" and a "rise time" for each subfault, with the
    latter determining how long it takes the slip to build up on the subfault.
    A quasi-static approach can then be used in which the Okada model is used
    at each time from `t0` to the final time of any subfault motion, with
    the cumulative slip up to that time used as the seafloor deformation at that
    time. Alternatively, a full 3D seismic simulation could be performed to
    model the generation and propagation of seismic waves spreading out from
    the fault.  The motion of the free surface in the seismic simulation is
    then used as the seafloor deformation, and is evolving in time from the
    initial time `t0` of the earthquake to a later time when all the seismic
    waves have decayed. At this time, the final seafloor deformation may be
    similar to what the Okada model would predict, particularly if the seismic
    simulation is done in a homogeneous half-space.  However, the seismic
    simulation can instead be done using a model of the structure of the earth
    in which the elastic parameters (and seismic wave speeds) vary in space.
    Some seismic codes also allow the free surface to model the topography and
    bathymetry of the sea floor as well, and may even model the ocean as a
    separate acoustic layer on top of the earth.

 3. A **"dynamic" rupture model** is even more complex, in that the initial fault
    geometry and stresses are prescribed but the slip on each subfault is
    then determined dynamically by using a rupture model for the rock mechanics,
    coupled with the 3D elastic wave equations.

Regardless of how complex the model is that determines the seafloor motion,
in GeoClaw we simply read in the resulting vertical seafloor displacement
on a uniform grid at a sequence of one or more times.

.. _dtopo_formats:

dtopo file formats
------------------

Currently two formats are supported for this file:

    **dtopotype=1:**

    Similar to
    topo files with *topotype=1* as described above, except that each line
    starts with a *t* value for the time, so each line contains t,x,y,dz

    The x,y,dz values give the displacement dz at x,y at time t.  It is assumed
    that the grid is uniform and that the file contains mx*my*mt lines if mt
    different times are specified for an mx*my grid.

    **dtopotype=3:**

    This is the recommended `dtopo_type`.  Similar to
    topo files with *topotype=3* as described above, but the header is
    different, and contains lines specifying *mx, my, mt, xlower, ylower, t0,
    dx, dy*, and *dt*.  These are followed by *mt* sets of *my* lines,
    each line containing *mx* values of *dz*.

Here is an example header for a dtopofile::

        721       mx
       1201       my
         56       mt
    -1.28500000000000e+02   xlower
    4.00000000000000e+01   ylower
    0.00000000000000e+00   t0
    8.33333333332575e-03   dx
    8.33333333333286e-03   dy
    1.00000000000000e+01   dt


The time increment is `dt=10` seconds and `mt=56` snapshots of the
vertical deformation are stored in this file;
this header is followed by 1201 x 56 lines, each having 721 values
giving the vertical displacement on one line of constant latitude.

Note that while the topography is moving, it is important to insure that the
time step is small enough to capture the motion.  The `setrun.py`
parameter `rundata.dtopo_data.dt_max_dtopo` can be set to the  maximum timestep
to be used between time `t0 = 0` and `t0 + (mt-1)*dt = 550` seconds, in the
example above.  See :ref:`setrun_topo`.

GeoClaw does not include any capabilities for 3D seismic modeling, but
the Okada model on both rectangles and triangles is implemented, along with
tools for reading the fault parameters in
various formats, applying the Okada model, and generating a dtopo file
with the resulting displacements.
See :ref:`okada` and :ref:`dtopotools_module` for more details.

.. _qinit_file:

qinit data file
---------------

Instead of (or in addition to) specifying a displacement of the topography
it is possible to specify a perturbation to the depth, momentum, or surface
elevation of the initial data.  This is generally useful only for tsunami
modeling where the initial data specified in the default *qinit.f90* function
is the stationary water with surface elevation equal to *sea_level* as set in
`setrun.py` (see :ref:`setrun_geoclaw`).

Of course it is possible to copy the *qinit.f90* function to your
directory and modify it, but for some applications the initial elevation may
be given on grid of the same type as described above.  In this case file can
be provided as described at :ref:`setrun_qinit` containing this
perturbation.

The file format is similar to what is described above for *topotype=1*, but
now each line contains *x,y,dq* where *dq* is a perturbation to one of the
components of *q* as specified by the value of *qinit_type* specified (see
:ref:`setrun_qinit`).  If *qinit_type = 4*, the value *dq* is instead the
surface elevation desired for the initial data and the depth *h* (first
component of *q*) is set accordingly.
