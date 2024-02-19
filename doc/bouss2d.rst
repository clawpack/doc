.. _bouss2d:

*********************************************
Boussinesq solvers in Two Space Dimensions
*********************************************

.. warning :: Not yet incorporated in clawpack master branch or releases.

As of Version 5.10.0 (?), GeoClaw supports two different sets of
dispersive Boussinesq-type equations that have been used in the literature
to better model wave propagation in situations where the wavelength is not
sufficiently long relative to the fluid depth for the shallow water
equation approximation to be accurate.  The one-dimensional version of these
capabilities are described in :ref:`bouss1d`.

These Boussinesq equations are still depth-averaged equations, with the same
conserved quantities (fluid depth `h` and momenta `hu` and `hv` in 2D) as the
shallow water equations (SWE), but the
equations contain higher order derivative terms and so they are no longer
hyperbolic and require implicit methods for efficient solution with a
physically reasonable time step.  This adds considerable complexity to the
code since adaptive mesh refinement (AMR) is still supported.

The equations implemented include third-order derivatives
with respect to `txx`, `tyy`, and `txy`.
However, the implementations proceed by alternating
steps with the shallow water equations (SWE) and the solution of elliptic
equations that involve second order derivatives in `x` and `y` but no 
time derivatives.

In two space dimensions, solving this
elliptic equation requires solving a sparse
linear system of equations in each time step, at each refinement level when
AMR is being used. The structure of this system is complicated by the need
to include all grid cells from all patches at the same refinement level
in the linear system that is solved. Boundary conditions at the edge of
patches must be interpolated from coarser level solutions, in much the same
way that the boundaary conditions for `h`, `hu`, and `hv` are interpolated
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
AMR strategy used, along with simulation results from several test problems.

.. _bouss2d_eqns:

Boussinesq-type dispersive equations
------------------------------------

The equations we solve are not the original depth-averaged dispersive
equations derived by Boussinesq, but for simplicity
in this documentation and the code, we refer to the
equations simply as "Boussinesq equations", following common practice.
Many variants of these equations have been derived and fine-tuned to 
better match the dispersion relation of the linearized
`Airy wave theory <https://en.wikipedia.org/wiki/Airy_wave_theory>`__
and to incorporate variable bottom topography.

Two variants are currently implement in GeoClaw, described below.

.. _bouss2d_sgn:

The SGN equations
-----------------

The recommended set of equations to use are a modification of the
Serre-Green-Naghdi (SGN) equations with the addition of a parameter `alpha`
suggested by Bonneton et al.  Both the 1D and 2D versions of these equations
and their GeoClaw implementation are discussed in [BergerLeVeque2023]_.
Setting `alpha = 1` gives the original SGN equations, but `alpha = 1.153` is
recommended since it gives a better approximation to the linear dispersion
relation of the Airy solution to the full 3d problem.

.. _bouss2d_ms:

The Madsen-Sorensen (MS) equations
----------------------------------

These equations also give a good approximation to the linear dispersion
relation of the Airy solution when the parameter `beta = 1/15` is used.
These equations were used in an earlier GeoClaw implementation known as
BoussClaw [KimEtAl2017]_.
These have been reimplemented in GeoClaw more recently,
including a 2d implementation that allows the use of AMR.  However,
extensive tests with these equations have revealed some stability issues,
particularly in the case of AMR, which have also been reported by others.
The 1D MS implementation is included in GeoClaw but it is generally not
recommended except for those interested in comparing different formulations
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
    rundata.bouss_data.bouss_solver = 3       # 1=GMRES, 2=Pardiso, 3=PETSc
    rundata.bouss_data.bouss_tstart = 0.      # time to switch from SWE

These parameters control:

- `bouss_equations`: The system of equations being solved.  Setting this to 2
  gives the recommended SGN equations.
  
  The value `alpha = 1.153` recommended for SGN is
  hardwired into `$CLAW/geoclaw/src/2d/bouss/bouss_module.f90`.  To change
  this value, you must modify this module.  (See :ref:`makefiles_library`
  for tips on modifying a library routine.)  Similarly, if you set
  `bouss_equations = 1` for the Madsen-Sorensen equations, the recommended 
  parameter value `B = 1/15` is set in `bouss_module.f90`.
  
  Setting `bouss_equations = 0` causes the code to revert to the shallow
  water equations, useful for comparing dispersive and nondispersive results.
  
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
  is less than `bouss_min_depth` in a cell or any of its nearest neighbors,
  then this cell is omitted from set of unknowns in the elliptic equation
  solve and no dispersive correction terms are calculated for this cell.
  This is discussed further below in :ref:`bouss2d_switch`.

- `bouss_solver`: What linear system solver to use. Currently only the value
  3 for `PETSc`_ is recognized.

- `bouss_tstart`: The time `t` at which to start applying Boussinesq terms.
  Normally you will want this to be less than or equal to `t0`, the starting
  time of the calculation (which is usually but not always 0). However,
  there are some cases in which the initial data results in extreme
  motion in the first few time steps and it is necessary to get things going
  with the SWE.  For most applications this is not necessary and you need
  only change this parameter if you have set `t0 < 0`.
 
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
environment variables in the shell from which `make` is invoked). Together
these specify the path to the installation of PETSc that you wish to use, see
`Maintaining Your PETSc Installation(s) <https://petsc.org/release/install/multibuild/>`_ in the PETSc documentation.

The `Makefile` should also include a line of the form::

    PETSC_OPTIONS=-options_file $(CLAW)/geoclaw/examples/bouss/petscMPIoptions

with a pointer to the file that sets various `PETSc` options. The file
`$CLAW/geoclaw/examples/bouss/petscMPIoptions` gives the options used in
the examples, which may be adequate for other problems too.

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

See also the PETSc documentation page
`Environmental Variables $PETSC_DIR And $PETSC_ARCH <https://petsc.org/release/install/multibuild/#environmental-variables-petsc-dir-and-petsc-arch>`__

.. _bouss2d_switch:

Wave breaking and switching to SWE
----------------------------------

The `bouss_min_depth` parameter is needed because in very shallow water, and for
modeling onshore inundation, the Boussinesq equations are not suitable.
So some criterion is needed to drop these correction terms and revert to
solving SWE near shore.  Many different approaches have been used in the
literature.  So far we have only implemented the simplest common approach,
which is to revert to SWE in any grid cell where the initial water depth (at
the initial time) is less than `bouss_min_depth`.

Examples
--------

In addition to the example application included in GeoClaw, found in the
directory `$CLAW/geoclaw/examples/bouss/radial_flat`, several other examples
of usage can be found in the code repository
https://github.com/rjleveque/ImplicitAMR-paper
developed to accompany the paper [BergerLeVeque2023]_.
