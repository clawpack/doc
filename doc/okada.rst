
.. _okada:

=====================================================
Earthquake sources: Fault slip and the Okada model
=====================================================

To initiate a tsunami from an earthquake, it is necessary to generate a model of
how the seafloor moves, which is generally specified in a *dtopo* file as
described in :ref:`topo_dtopo`.

.. _okada_slip:

Fault slip
----------

For historic earthquakes, it is generally possible to find many different
models for the distribution of slip on one or more fault planes, 
see for example the pointers at :ref:`tsunamidata_sources`.  

An earthquake subfault model is typically given in the form of a set of
rectangular patches on the fault plane.  
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


.. _okada_model:

Okada model
-----------

The slip on the fault plane(s) must be translated into seafloor deformation.
This is often done using the "Okada model", which is derived from
a Green's function sollution to the elastic half space problem.  Uniform
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

The GeoClaw routine `$CLAW/python/pyclaw/geotools/okada2.py` available
starting in Version 4.6.3, is an improved version of
`$CLAW/python/pyclaw/geotools/okada.py` that allows specifying whether the
latitude and longitude provided corresponds to the centroid, bottom center,
or the top center of the fault plane (the original assumed top center).  
The specification of other parameters has also been modified, see the
documentation in that file.

The Python module `$CLAW/python/pyclaw/geotools/dtopotools.py` (new in
4.6.3) provides tools to convert a file specifying a collection of subfaults
into a *dtopofile* by applying the Okada model to each subfault and adding
the results together (valid by linear superposition of the solutions to the
linear elastic halfspace problems).
These still need to be cleaned up and better documented, but an example of
the usage can be found in the new application example
`$CLAW/apps/tsunami/chile2010b`.


