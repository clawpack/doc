:orphan:

.. _sphere_source:

============================================
Source terms for shallow water on the sphere
============================================

The shallow water equations on the sphere involve some geometric
source terms that are currently missing from GeoClaw.  Experiments
during initial develpment of GeoClaw seemed to indicate that they were
not important, but more recently it has been found that at least the
source term in the mass equation can be quite important for properly
modeling waves moving between the tropics and polar regions due to the
variation in cell size with latitude.

As of v5.9.1, these source terms have been added to
`$CLAW/geoclaw/src/2d/shallow/src2.f90`.  
There is a `setrun.py` parameter `rundata.geo_data.sphere_source`
that can be set to 0 for no source terms, 1 to add the source term
only in the mass equation, or 2 to add source terms in the momentum equations
too.

**Change in default behavior:**

Starting in v5.10.0, the default value ::

    rundata.geo_data.sphere_source = 1

is used if this parameter is not
set otherwise in `setrun.py`, so that the source term in mass is included.
Adding the source terms in momentum seems to have almost no effect in
most practical problems, as illustrated in 
`this document
<https://faculty.washington.edu/rjl/misc/spherical_swe_2023-10-27.pdf>`__,
which presents more discussion of these source terms and includes some
examples to illustrate the effect they have in various circumstances.

