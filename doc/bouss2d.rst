.. _bouss2d:

*********************************************
Boussinesq solvers in Two Space Dimensions
*********************************************


As of Version 5.10.0, GeoClaw includes the option to solve a
dispersive Boussinesq-type equation known as Serre-Green-Naghdi (SGN)
instead of the usual shallow water equations (SWE).
This equation and related depth-averaged equations have been used
extensively in the literature
to better model wave propagation in situations where the wavelength is not
sufficiently long relative to the fluid depth for the SWE
approximation to be accurate.  Applications include the study
of tsunamis generated by landslides, asteroid impacts, or other localized
phenomena.  Including dispersive terms has also been found to give more
realistic results for earthquake-generated tsunamis in some situations.
See [BergerLeVeque2023]_ for references to some of this literature along
with more discussion of the GeoClaw implementation and test problems.

The one-dimensional version of these capabilities are
described in :ref:`bouss1d`.

The SGN equations are still depth-averaged equations, with the same
conserved quantities (fluid depth `h` and momenta `hu` and `hv` in 2D) as the
shallow water equations (SWE), but the
equations contain higher order derivative terms and so they are no longer
hyperbolic and require implicit methods for efficient solution with a
physically reasonable time step.  This adds considerable complexity to the
code since adaptive mesh refinement (AMR) is still supported.
The implementation proceeds by alternating time
steps on the shallow water equations (SWE) with the solution of elliptic
equations where the operator involves second order derivatives in `x` and `y`
of a new set of variables used to modify the momenta each time step.
The right hand side also involves third order derivatives of the topography.

In two space dimensions, solving this
elliptic equation requires setting up and solving a sparse
linear system of equations in each time step, at each refinement level when
AMR is being used. All grid cells from all patches at 
the same refinement level
are included in the linear system. Boundary conditions at the edge of
patches must be interpolated from coarser level solutions, in much the same
way that the boundary conditions for `h`, `hu`, and `hv` are interpolated
when solving the SWE with AMR. Because the solution of the elliptic system
yields correction terms to the momenta (denoted here by `huc` and `hvc`),
when solving the Boussinesq equations the array `q` of state variables
is expanded to include these correction terms as well, and so the number of
equations and variables is 5 instead of 3.  This change must be made in
`setrun.py`, along with other changes discussed below, in order to use
the Boussinesq solvers.

Currently the only linear system solver supported for solving the large
sparse elliptic systems is `PETSc <https://petsc.org/release/>`_,
which can use MPI to solve these these systems. Using the Boussinesq solvers
requires these prerequesites, as discussed further in :ref:`bouss2d_prereqs`.

See [BergerLeVeque2023]_ for more discussion of the equations solved and the
AMR algorithms developed for these equations.

.. _bouss2d_eqns:

Boussinesq-type dispersive equations
------------------------------------

The equations we solve are not the original depth-averaged dispersive
equations derived by Boussinesq, but for simplicity
in this documentation and the code, we often refer to the
equations simply as "Boussinesq equations", following common practice.
Many variants of these equations have been derived and fine-tuned to 
better match the dispersion relation of the linearized
`Airy wave theory <https://en.wikipedia.org/wiki/Airy_wave_theory>`__
and to incorporate variable bottom topography.

Two variants are currently implement in GeoClaw, described below.
In practice we recommend using only the SGN equations, which we have found
to be more stable.

.. _bouss2d_sgn:

The SGN equations
-----------------

The Serre-Green-Naghdi (SGN) equations implemented in GeoClaw
are generalized to include a parameter `alpha`
suggested by Bonneton et al.  Both the 1D and 2D versions of these equations
and their GeoClaw implementation are discussed in [BergerLeVeque2023]_.
The value `alpha = 1.153` is
recommended since it gives a better approximation to the linear dispersion
relation of the Airy solution to the full 3d problem.
This value is
hardwired into `$CLAW/geoclaw/src/2d/bouss/bouss_module.f90`.  To change
this value, you must modify this module.  (See :ref:`makefiles_library`
for tips on modifying a library routine.) 
Setting `alpha = 1` gives the original SGN equations.


.. _bouss2d_ms:

The Madsen-Sorensen (MS) equations
----------------------------------

Primarily for historical reasons, GeoClaw also includes an implementation of
another Boussinesq-type dispersive system, the Madsen-Sorensen (MS) equations.
These equations also give a good approximation to the linear dispersion
relation of the Airy solution when the parameter `Bparam = 1/15` is used,
which is hardwired into `$CLAW/geoclaw/src/2d/bouss/bouss_module.f90`.
These equations were used in an earlier GeoClaw implementation 
by Jihwan Kim, known as BoussClaw  [KimEtAl2017]_.
This implementation was successfully used in a number of studies
(see [BergerLeVeque2023]_ for some citations).
However, extensive tests with these equations have revealed stability issues,
particularly with the use of AMR, which have also been reported by others.
Implementations of MS in both 1D and 2D  are included in GeoClaw,
but are generally not
recommended except for those interested in comparing different
formulations for small numbers of time steps, 
and perhaps further investigating the stability issues.

.. _bouss2d_usage:

Using the 2d Boussinesq code
----------------------------

Provided the :ref:`bouss2d_prereqs` have been installed, switching from the
SWE to a Boussinesq solver in GeoClaw requires only minor changes to
`setrun.py` and the `Makefile`.

See the files in `$CLAW/geoclaw/examples/bouss/radial_flat` for an example.


.. _bouss2d_setrun:

setrun.py
^^^^^^^^^

As mentioned above, it is necessary to set::

    clawdata.num_eqn = 5
    
instead of the usual value 3 used for SWE, since correction terms for the
momenta are also stored in the `q` arrays to facilitate interpolation to
ghost cells of finer level patches each time step.

It is also necessary to set some parameters that are specific to the
Boussinesq solvers.  Somewhere in the `setrun` function you must include ::

    from clawpack.geoclaw.data import BoussData
    rundata.add_data(BoussData(),'bouss_data')
    
and then the following parameters can be adjusted (the values shown here
are the default values that will be used if you do not specify a value 
directly)::

    rundata.bouss_data.bouss_equations = 2    # 0=SWE, 1=MS, 2=SGN
    rundata.bouss_data.bouss_min_level = 1    # coarsest level to apply bouss
    rundata.bouss_data.bouss_max_level = 10   # finest level to apply bouss
    rundata.bouss_data.bouss_min_depth = 10.  # depth (meters) to switch to SWE
    rundata.bouss_data.bouss_solver = 3       # 3=PETSc
    rundata.bouss_data.bouss_tstart = 0.      # time to switch from SWE

These parameters are described below:

- `bouss_equations`: The system of equations being solved.  Setting this to 2
  gives the recommended SGN equations, while 1 gives Madsen-Sorensen.
  
  Setting `bouss_equations = 0` causes the code to revert to the shallow
  water equations, useful for comparing dispersive and nondispersive results.
  (But if `bouss_data` is being set, it still requires `clawdata.num_eqn = 5`
  and the two new components in q are always 0 in this case, so this is
  slightly less efficient than using the standard GeoClaw.) 
  
- `bouss_min_level`: The minimum AMR level on which Boussinesq correction
  terms should be applied.  In some cases it may be desirable to use the SWE
  on the coarsest grids in the ocean while Boussinesq corrections are only
  applied on fine levels near shore, for example.

- `bouss_max_level`: The finest AMR level on which Boussinesq correction
  terms should be applied.  In some cases it may be desirable to use the SWE
  only on coarser grids if the finest level grid only exists in very shallow
  regions or onshore, where the the equations switch to SWE for inundation  
  modeling.  Since much of the computational work is often on the finest level,
  avoiding the Boussinesq terms altogether on these levels may be advantageous
  in some situations.
 
- `bouss_min_depth`: The criterion used for switching from Boussinesq to SWE
  in shallow water and onshore.  If the original water depth `h` at time `t0`
  is less than `bouss_min_depth` in a cell or any of its nearest
  neighbors in a 3-by-3 neighborhood,
  then this cell is omitted from set of unknowns in the elliptic equation
  solve and no dispersive correction terms are calculated for this cell.
  This is discussed further below in :ref:`bouss2d_switch`.

- `bouss_solver`: What linear system solver to use. Currently only the value
  3 for `PETSc`_ is recognized.

- `bouss_tstart`: The time `t` at which to start applying Boussinesq terms.
  Normally you will want this to be less than or equal to `t0`, the starting
  time of the calculation (which is not always 0). However,
  there are some cases in which the initial data results in extreme
  motion in the first few time steps and it is necessary to get things going
  with the SWE.  For most applications this is not necessary and you need
  only change this parameter if you are solving a problem for which `t0 < 0`.
 
.. _bouss2d_makefile:

Makefile
^^^^^^^^

You can copy the `Makefile` from 
`$CLAW/geoclaw/examples/bouss/radial_flat/Makefile` and make any adjustments
needed.

This `Makefile` reads in the standard Boussinesq solver file
`$CLAW/geoclaw/src/2d/bouss/Makefile.bouss`, which lists the Fortran modules
and source code files that are used by default from the library
`$CLAW/geoclaw/src/2d/bouss`, or from `$CLAW/amrclaw/src/2d` or
`$CLAW/geoclaw/src/2d/shallow` in the case of files that did not need to
be modified for the Boussinesq code.

Two `Makefile` variables `PETSC_DIR` and `PETSC_ARCH` must be set (perhaps as
environment variables in the shell from which `make` is invoked). These are
described further below in :ref:`bouss2d_prereqs`.

The `FFLAGS` specified in the `Makefile` should include `-DHAVE_PETSC`
to indicate that `PETSc` is being used, necessary when compiling the
source code for Boussinesq solvers.

The `Makefile` should also include a line of the form::

    PETSC_OPTIONS=-options_file $(CLAW)/geoclaw/examples/bouss/petscMPIoptions

with a pointer to the file that sets various `PETSc` options. The file
`$CLAW/geoclaw/examples/bouss/petscMPIoptions` gives the options used in
the examples, which may be adequate for other problems too.
This file includes some comments briefly explaining the options set. 
We use a GMRES Krylov space method as the main solver
and algebraic multigrid as the preconditioner.
For more about the options for these methods, see:

   - https://petsc.org/release/manualpages/KSP/KSPSetFromOptions
   - https://petsc.org/release/manualpages/PC/PCSetFromOptions/


In addition to a line of the form ::

    EXE = xgeoclaw

that specifies the name and location of the executable to be generated, the
`Makefile` should also contain a line of the form::

    RUNEXE="${PETSC_DIR}/${PETSC_ARCH}/bin/mpiexec -n 6"

This is the command that should be used in order to run the executable.
In other words, if you set `PETSC_DIR` and `PETSC_ARCH` as environment
variables, and the executable is named `xgeoclaw` as usual, then the command ::

    $PETSC_DIR/$PETSC_ARCH/bin/mpiexec -n 6 xgeoclaw
    
given in the shell should run the executable (invoking MPI with 6 processes in
this example).  If this does not work then one of the environment variables
may be set incorrectly to find the `mpiexec` command.


.. _bouss2d_prereqs:

Prerequisites for the 2d Boussinesq code
----------------------------------------

Currently the only linear solver supported is `PETSc`, so this must be
installed, see `<https://petsc.org/release/install/>`__ for instructions
and also note the `PETSc prerequisites 
<https://petsc.org/release/install/install_tutorial/#prerequisites>`__.
Note that MPI, LAPACK, and the BLAS are required and will be installed as
part of installing PETSc.  If you already have some of the prerequisites
installed, be sure to read `Configuring PETSc 
<https://petsc.org/release/install/install/#configuring-petsc>`__
before installing.

The environment variables `$PETSC_DIR` and `$PETSC_ARCH` must be set
appropriately based on your PETSc installation, either as environment
variables or directly in the `Makefile`. 
See the PETSc documentation page
`Environmental Variables $PETSC_DIR And $PETSC_ARCH <https://petsc.org/release/install/multibuild/#environmental-variables-petsc-dir-and-petsc-arch>`__.

.. _bouss2d_switch:

Wave breaking and switching to SWE
----------------------------------

The `bouss_min_depth` parameter is needed because in very shallow water, and for
modeling onshore inundation, the Boussinesq equations are not suitable.
So some criterion is needed to drop these correction terms and revert to
solving SWE near shore.  Many different approaches have been used in the
literature.  So far we have only implemented the simplest commonly used approach,
which is to revert to SWE in any grid cell where the initial water depth (at
the initial time) is less than `bouss_min_depth`.


Examples
--------

In addition to one example application included in GeoClaw, found in the
directory `$CLAW/geoclaw/examples/bouss/radial_flat`, several other examples
of usage can be found in the code repository
https://github.com/rjleveque/ImplicitAMR-paper, which was
developed to accompany the paper [BergerLeVeque2023]_.
