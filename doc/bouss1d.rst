.. _bouss1d:

*********************************************
Boussinesq solvers in One Space Dimension
*********************************************

As of Version 5.10.0, the geoclaw repository contains some code for solving
problems in one space dimension, as described more generally in
:ref:`geoclaw1d`.  This 1d code also supports two different sets of
dispersive Boussinesq equations that have been used in the literature
to better model wave propagation in situations where the wavelength is not
sufficiently long relative to the fluid depth for the shallow water
equation (SWE) approximation to be accurate.

These Boussinesq equations are still depth-averaged equation with the same
conserved quantities (fluid depth `h` and momentum `hu` in 1d), but the
equations contain higher order derivative terms and so they are no longer
hyperbolic. The equations implemented include third-order derivatives
with respect to `txx`.  However, the implementations proceed by alternating
steps with the shallow water equations and the solution of elliptic
equations that involve second-order derivatives in `xx` but no time derivatives.
In one space dimension, solving this equation requires solving a tridiagonal
linear system of equations in each time step.

See :ref:`bouss2d` and [BergerLeVeque2023]_ for more discussion
of the Boussinesq-type equations SGN and MS that are implemented in GeoClaw.
We recommend using the Serre-Green-Naghdi (SGN) equations rather than
Madsen-Sorensen (MS), which has similar dispersive properties but
is less stable.

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

The `Makefile` and `setrun.py` files must be modified from those used
for SWE as described below.
See the examples with names like `$CLAW/geoclaw/examples/1d/bouss_*` 
for sample files to use as a template.

.. _bouss1d_makefile:

Makefile
^^^^^^^^

A different `Makefile` is required for applications to use code from both
the `$CLAW/geoclaw/src/1d/shallow` and `$CLAW/geoclaw/src/1d/bouss`
libraries.  

Solving the Boussinesq equations requires solving an elliptic equation each
time step, which in one space dimension yields a tridiagonal linear system of
equations.  LAPACK is used for this, and the `Makefile` requires `FFLAGS` to
include `-llapack -lblas` or explicit pointers to these libraries on your
computer.  Alternatively, the file
`$CLAW/geoclaw/src/1d/bouss/lapack_tridiag.f`
contains the necessary soubroutines from lapack and the blas and so you can
add this to the list of `SOURCES` in the `Makefile`.  See
`$CLAW/geoclaw/src/1d/examples/bouss_wavetank_matsuyama/Makefile`
for an example.

OpenMP is not used in the 1d codes, so there is no need to compile with
these flags.  For more about `FFLAGS` and suggested settings for debugging,
see :ref:`fortran_fflags`.

.. _bouss1d_setrun:

setrun.py
^^^^^^^^^


To use the Boussinesq solvers, somewhere in the `setrun` function you
must include ::

    from clawpack.geoclaw.data import BoussData1D
    rundata.add_data(BoussData1D(),'bouss_data')
    
and then the following parameters can be adjusted (the values shown here
are the default values that will be used if you do not specify a value 
directly)::
    
    rundata.bouss_data.equations = 2   # 0=SWE, 1=MS, 2=SGN
    rundata.bouss_data.deepBouss = 5.  # depth (meters) to switch to SWE

The `rundata.bouss_data` object has attributes:

- `bouss_equations`: The system of equations being solved.  Setting this to 2
  gives the recommended SGN equations.
  
  The value `alpha = 1.153` recommended for SGN is
  hardwired into `$CLAW/geoclaw/src/2d/bouss/bouss_module.f90`.  To change
  this value, you must modify this module.  (See :ref:`makefiles_library`
  for tips on modifying a library routine.)  Similarly, if you set
  `bouss_equations = 1` for the Madsen-Sorensen equations, the recommended 
  parameter value `Bparam = 1/15` is set in `bouss_module.f90`.
  
  Setting `bouss_equations = 0` causes the code to revert to the shallow
  water equations, useful for comparing dispersive and nondispersive results.
   
- `bouss_min_depth`: The criterion used for switching from Boussinesq to SWE
  in shallow water and onshore.  If the original water depth `h` at time `t0`
  is less than `bouss_min_depth` in a cell or any of its nearest neighbors,
  then this cell is omitted from set of unknowns in the elliptic equation
  solve and no dispersive correction terms are calculated for this cell.   

The latter parameter is needed because in very shallow water, and for
modeling onshore inundation, the Boussinesq equations are not suitable.
So some criterion is needed to drop these correction terms and revert to
solving SWE near shore.  Many different approaches have been used in the
literature.  So far we have only implemented the simplest common approach,
which is to revert to SWE in any grid cell where the initial water depth (at
the initial time) is less than `bouss_min_depth`.
See :ref:`bouss2d_switch` for more discussion.
