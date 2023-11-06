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
`$CLAW/geoclaw/src/2d/shallow/src2.f90`.  In v5.9.1 these terms are turned
off by default for backward compatibility but to allow for further testing
by turning them on and recompiling.  
As of v5.9.2, there is a `setrun.py` parameter `rundata.geo_data.sphere_source`
that can be set to 0 (default) for no source terms, 1 to add the source term
only in the mass equation, or 2 to add source terms in the momentum equations
too.
In the future the default value will probably be 1, to add the source term
in mass. 

A document is in preparation to describe these source terms and show some
examples of the impact they have. A draft can be viewed at
`<https://faculty.washington.edu/rjl/misc/spherical_swe_2023-10-27.pdf>`__


