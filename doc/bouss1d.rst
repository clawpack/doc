.. _bouss1d:

*********************************************
Boussinesq solvers in One Space Dimension
*********************************************

.. warning :: Not yet incorporated in clawpack master branch or releases.

As of Version 5.10.0, the geoclaw repository contains some code for solving
problems in one space dimension, as described more generally in
:ref:`geoclaw1d`.  This code also supports two different sets of
dispersive Boussinesq equations that have been used in the literature
to better model wave propagation in situations where the wavelength is not
sufficiently long relative to the fluid depth for the shallow water
equation approximation to be accurate.

These Boussinesq equations are still depth-averaged equation with the same
conserved quantities (fluid depth `h` and momentum `hu` in 1d), but the
equations contain higher order derivative terms and so they are no longer
hyperbolic. The equations implemented include third-order derivatives
with respect to `txx`.  However, the implementations proceed by alternating
steps with the shallow water equations and the solution of elliptic
equations that involve only second-order derivatives in `xx`.

.. _bouss1d_sgn:

The SGN equations
-----------------

The recommended set of equations to use are a modification of the
Serre-Green-Naghdi (SGN) equations with the addition of a parameter `alpha`
suggested by Bonneton et al.  Both the 1d and 2d versions of these equations
and their GeoClaw implementation are discussed in [BergerLeVeque2023]_.
Setting `alpha = 1` gives the original SGN equations, but `alpha = 1.153` is
recommended since it gives a better approximation to the linear dispersion
relation of the Airy solution to the full 3d problem.

.. _bouss1d_ms:

The Madsen-Sorensen (MS) equations
----------------------------------

These equations also give a good approximation to the linear dispersion
relation of the Airy solution when the parameter `beta = 1/15` is used.
These equations were used in an earlier GeoClaw implementation known as
BoussClaw.  These have been reimplemented in GeoClaw more recently,
including a 2d implementation that allows the use of AMR.  However,
extensive tests with these equations have revealed some stability issues,
particularly in the case of AMR, which have also been reported by others.
The 1d MS implementation is included in GeoClaw but it is generally not
recommended except for those interested in comparing different formulations
and perhaps further investigating the stability issues.

.. _bouss1d_usage:

Using the 1d Boussinesq code
----------------------------

As in the 1d shallow water implementation, general mapped grids can be used,
but AMR is not supported in 1d.  The  plane wave (`coordinate_system == 1`)
and planar radial (`coordinate_system == -1`) versions of the Boussinesq
equations are both implemented.  The axisymmetric version on the sphere
(`coordinate_system == 2`) is not yet implemented.

Specifying topo and dtopo files is identical to what is described for 
:ref:`geoclaw1d`.

**Some things that must change:**

See the examples with names like `$CLAW/geoclaw/examples/1d/bouss_*` 
for some sample code that can be modified for other problems.

.. _bouss1d_makefile:

Makefile
^^^^^^^^

A different `Makefile` is required for applications to use code from both
the `$CLAW/geoclaw/src/1d/shallow` and `$CLAW/geoclaw/src/1d/bouss`
libraries.  

Solving the Boussinesq equations requires solving an elliptic equation each
time step, by setting up and solving a tridiagonal linear system of
equations.  LAPACK is used for this, and the `Makefile` requires `FFLAGS` to
include `-llapack -lblas` or explicit pointers to these librarires on your
computer.  Alternatively, the file
`$CLAW/geoclaw/src/1d/bouss/lapack_tridiag.f`
contains the necessary soubroutines from lapack and the blas and so you can
add this to the list of `SOURCES` in the `Makefile`.  See e.g. 
`$CLAW/geoclaw/src/1d/examples/bouss_wavetank_matsuyama/Makefile`
for an example.

OpenMP is not used in the 1d codes, so there is no need to compile with
these flags.  For more about `FFLAGS` and suggested settings for debugging,
see :ref:`fortran_fflags`.

.. _bouss1d_setrun:

setrun.py
^^^^^^^^^


Some additional parameters must be added to `setrun.py`, typically set as 
follows::

    #rundata.add_data(BoussData1D(),'bouss_data')  # FIX!
    rundata.bouss_data.bouss = True
    rundata.bouss_data.equations = 2  # for SGN (recommended, or 1 for MS)
    rundata.bouss_data.deepBouss = 5.  # depth (meters) to switch to SWE

The `rundata.bouss_data` object has attributes:

- `bouss` (logical). Set to `True` to use Boussinesq corrections,
  set to `False` to revert to shallow water equations
- `equations` (int): Which equation set to use (1 for MS, 2 for SGN).
- `deepBouss` (float): water depth at which to switch from Boussinesq
  to SWE.

The latter parameter is needed because in very shallow water, and for
modeling onshore inundation, the Boussinesq equations are not suitable.
So some criterion is needed to drop these correction terms and revert to
solving SWE near shore.  Many different approaches have been used in the
literature.  So far we have only implemented the simplest common approach,
which is to revert to SWE in any grid cell where the initial water depth (at
the initial time) is less than `deepBouss`.

