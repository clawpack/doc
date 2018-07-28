
.. _okada:

=====================================================
Earthquake sources: Fault slip and the Okada model
=====================================================

To initiate a tsunami from an earthquake, it is necessary to generate a model of
how the seafloor moves, which is generally specified in a *dtopo* file as
described in :ref:`topo_dtopo`.  This is often done by starting with a
description of an earthquake fault, broken up into a collection of
subfaults, with various parameters defined on each subfault.  A seismic
modeling code would take these parameters and compute the elastic waves
generated in the earth as a result.  However, for tsunami modeling all we need
to know is the motion of the seafloor, which is one boundary of the seismic
domain.  Moreover the high-frequency ground motions during the earthquake
have little impact on the resulting tsunami.  For these reasons it is often
sufficient to use the "Okada model" described below, which gives the final
deformation of the sea floor due to specified slip on each subfault.

The Jupyter notebook `$CLAW/apps/notebooks/geoclaw/Okada.ipynb`
illustrates how the Okada model works and how to generate the seafloor
deformation needed in GeoClaw using this model.


The Python module `$CLAW/geoclaw/src/python/geoclaw/dtopotools.py` 
provides tools to convert a file specifying a collection of subfaults
into a *dtopofile* by applying the Okada model to each subfault and adding
the results together (valid by linear superposition of the solutions to the
linear elastic halfspace problems).
See :ref:`dtopotools_module` for more documentation and illustrations.

.. _okada_slip:

Fault slip on rectangular subfaults
-----------------------------------

For historic earthquakes, it is generally possible to find many different
models for the distribution of slip on one or more fault planes, 
see for example the pointers at :ref:`tsunamidata_sources`.  

An earthquake subfault model is typically given in the form of a set of
*rectangular patches* on the fault plane.  
Each patch has a set of parameters defining the relative slip of rock on one
side of the planar patch to slip on the other side.  The minimum set of
parameters required is:

* *length* and *width* of the fault plane (typically in m or km),
* *latitude* and *longitude* of some point on the fault plane, typically
  either the centroid or the center of the top (shallowest edge),
* *depth* of the specified point below the sea floor,
* *strike*, the orientation of the top edge, measured in degrees
  clockwise from North.  Between 0 and 360.  The fault plane dips downward
  to the right when moving along the top edge in the strike direction.
* *dip*, angle at which the plane dips downward from the top edge, a
  positive angle between 0 and 90 degrees.
* *rake*, the angle in the fault plane in which the slip occurs,
  measured in degrees counterclockwise from the strike direction.
  Between -180 and 180.
* *slip > 0*, the distance (typically in cm or m) the hanging block moves
  relative to the foot block, in the direction specified by the rake.
  The "hanging block" is the one above the dipping fault plane (or to the
  right if you move in the strike direction).  

Note that for a strike-slip earthquake, *rake* is near 0 or 180.  
For a subduction earthquake, the rake is usually closer to 90 degrees.

For kinematic (time-dependent) rupture, it is also necessary to specify the
`rupture_time` and `rise_time` of each subfault, as discussed below.

A fault can be specified in GeoClaw as an instance of the
`dtopotools.Fault` class, instatiated e.g. by::

    from clawpack.geoclaw import dtopotools
    fault = dtopotools.Fault()

Then set `fault.subfaults` to a list of subfaults as instances of the class
`dtopotools.SubFault`. Each subfault has attributes corresponding to the
parameters listed above.  In addition, `coordinate_specification` should be
set for each subfault to one of:


- "bottom center": (longitude,latitude) and depth at bottom center
- "top center": (longitude,latitude) and depth at top center
- "centroid": (longitude,latitude) and depth at centroid of plane
- "noaa sift": (longitude,latitude) at bottom center, depth at top,
  This mixed convention is used by the NOAA SIFT
  database and "unit sources", see:
  http://nctr.pmel.noaa.gov/propagation-database.html.
- "top upstrike corner": (longitude,latitude) and depth at
  corner of fault that is both updip and upstrike.

For example, a simple single-subfault model of the 2010 Chile event can be
specified by::


    subfault = dtopotools.SubFault()
    subfault.length = 450.e3             # meters
    subfault.width = 100.e3              # meters
    subfault.depth = 35.e3               # meters
    subfault.strike = 16.                # degrees
    subfault.slip = 15.                  # degrees
    subfault.rake = 104.                 # degrees
    subfault.dip = 14.                   # degrees
    subfault.longitude = -72.668         # degrees
    subfault.latitude = -35.826          # degrees
    subfault.coordinate_specification = "top center"

    fault = dtopotools.Fault()
    fault.subfaults = [subfault]


Starting in Version 5.5.0, it is also possible to specify a set of
*triangular* subfault patches rather than rectangles.  Doing so requires
a different set of parameters, as described below in
:ref:`okada_triangular`.

Once the subfaults have been specified, the function 
`fault.create_dtopography` can be used to create a
`dtopotools.DTopography` object, and then written out as a dtopofile for use
in GeoClaw, e.g.::

    x,y = fault.create_dtopo_xy(dx=1/60., buffer_size=2.0)
    fault.create_dtopography(x,y,times=[1.])
    dtopo = fault.dtopo
    fault.rupture_type = 'static'
    dtopo.write('chile_dtopo.tt3', dtopo_type=3)

This will create a file `chile_dtopo.tt3` that can be used as a
dtopofile in GeoClaw.  It will cover a region `buffer_size = 2.0`
degrees larger on each side than the surface projection of the
rectangular fault, with a resolution of one arcminute (`dx = 1/60.` degree).

In addition to `dtopotools.Fault`, the `dtopotools` has several other
derived classes that simplify setting up a fault from a specified set of
subfaults:

- `CSVFault`: reads in subfaults from a csv file with header,
- `SiftFault`: sets up a fault based on the NOAA SIFT unit sources, see
  http://nctr.pmel.noaa.gov/propagation-database.html,
- `UCSBFault`: reads in subfaults in UCSB format,
- `SegmentedPlaneFault`: Take a single fault plane and subdivides it into
  recangles, to allow specifying different subfault parameters on each.

See :ref:`dtopotools_module` for more details, and the Jupyter notebook
`$CLAW/apps/notebooks/geoclaw/dtopotools_examples.ipynb` for more examples.

.. _okada_model:

Okada model
-----------

The slip on the fault plane(s) must be translated into seafloor deformation.
This is often done using the "Okada model", which is derived from
a Green's function solution to the elastic half space problem, following 
[Okada85]_.  Uniform
displacement of the solid over a finite rectangular patch specified
using the parameters described above, when inserted in a homogeneous
elastic half space a distance *depth* below the free surface, leads
to a steady state solution in which the free surface is deformed.  This
deformation is used as the seafloor deformation.  Of course this is only an
approximation since the actual seafloor in rarely flat, and the actual earth
is not a homogeneous isotropic elastic material as assumed in this model.
However, it is often assumed to be a reasonable approximation for tsunami
modeling, particularly since the fault slip parameters are generally not
known very well even for historical earthquakes and so a more accurate
modeling of the resulting seafloor deformation may not be justified.

In addition to the parameters above, the Okada model also requires an elastic
parameter, the Poisson ratio, which is usually taken to be 0.25.


Kinematic rupture
-----------------

It is also possible to set a `rupture_time` and a `rise_time` for each
subfault in order to model a time-dependent rupture process.  This is called
a "kinematic rupture" since the these values are specified. 

To specify a kinematic rupture, create a `dtopotools.Fault` object `fault`
with `fault.rupture_type = 'kinematic'`. 
(For backward compatibility, you can also specify this as `'dynamic'`.
However, the term "dynamic rupture" often refers to modeling the
rupture process itself.)

A kinematic rupture is **not** modeled by via modeling the seismic
waves that would be generated by the specified subfault motions.
There are seismic codes that do this, based on the same set of fault
parameters, but this is not supported directly in GeoClaw. If
desired, output from such a code could be converted by the user
into a dtopo file for use in GeoClaw.

Once a `dtopotools.Fault` object has been created with the desired
subfaults, a `dtopotools.DTopography` object can be computed using
the `dtopotools.Fault.create_dtopography` function in GeoClaw (and
written out as a dtopo file using its `write` function.) The moving
dtopo generated in this manner is the sum of the Okada solutions
generated by each subfault, sampled at a set of specified times
`t`.  For subfaults with `subfault.rupture_time > t`, no displacement
is included, while if `subfault.rupture_time + subfault.rise_time
<= t` the entire deformation due to this subfault is included, with
linear interpolation between these at intermediate times.


.. warning:: Starting in Version 5.5.0, the subfault parameter `rise_time`
   now refers to the total rise time of a subfault, while `rise_time_starting`
   is the rise time up to the break in the piecewise quadratic
   function defining the rise. By default `rise_time_ending` is set equal to
   `rise_time_starting`.  
   (In earlier versions, `rise_time` read in from csv
   files, for example, was erroneously interpreted as `rise_time_starting` 
   is now.) See the module function `rise_fraction` in
   :ref:`dtopotools_module` for more details.

.. _okada_triangular:

Fault slip on triangular subfaults
----------------------------------

Starting in Version 5.5.0, it is also possible to specify a set of
*triangular* subfault patches rather than rectangles.

Specifying a subfault as a triangular patch rather than as a rectangle can
be done by setting `subfault.coordinate_specification = 'triangular'` and
specifying `subfault.corners` as a list of three `(x,y,depth)` tuples, along
with the `slip` and `rake`. In this case you do not set the attributes
`length`, `width`, `depth`, `strike`, or `dip`, since the corners of the
triangle are sufficient to determine this geometry.  
Internally a strike direction is calculated by intersecting the plane
defined by the triangle with the ground surface, and choosing the direction
so that the plane of the triangle dips at an angle between 0 and 90 degrees
relative to the strike direction.  The specified `rake` is again
interpreted as degrees counterclockwise from this strike direction.

For an example see [need to add a notebook].
