
.. _clawpack_packages:

************************************
Which Clawpack solver should I use?
************************************

Clawpack includes a number of related hyperbolic PDE solvers:

 - Classic
 - :ref:`amrclaw`
 - :ref:`geoclaw`
 - :ref:`pyclaw`

All of them are built on common algorithmic
ideas, make use of the same set of Riemann solvers, and can be used with VisClaw
for visualization.  If you're not sure which solver to use, here you will find
the main differences between them.


Installation and user interface
===============================
The AMRClaw, GeoClaw, and Classic solvers are traditional Fortran-based
packages and rely on Makefiles and environment variables.  Problems are
specified partially through parameter input files (`clawez.data`) and partially
through custom Fortran code (to set initial conditions, for instance).

With PyClaw, problems are specified through Python script files, or
interactively (e.g., in IPython).  Typically, the user does not need to
write any Fortran code (though custom routines can be written in Fortran
when necessary for performance reasons).
PyClaw uses much of the same library of Fortran code, but that code is
compiled during installation so that it can be imported dynamically within
Python programs.


Algorithmic differences
===============================
All of the Clawpack solvers include the *classic* algorithms described in 
[LeVeque-FVMHP]_; if you only require those, it's easiest to use Classic or
PyClaw.  Most of the packages contain additional algorithms:

 - **AMRClaw** includes block-structured adaptive mesh refinement that allows one
   to use a non-uniform grid that changes in time and uses smaller grid cells 
   in regions with fine structure or where high accuracy is required.
 - **GeoClaw** Includes the AMR capabilities of AMRClaw and also has a number
   of special routines and algorithms for handling geophysical problems, including
   special well-balanced, positivity-preserving shallow water solvers.
 - **PyClaw** includes the high-order WENO-RK algorithms of SharpClaw, described in
   [KetParLev13]_.


Parallel computing
==================
- **AMRClaw**, **GeoClaw**, and **Classic** can be run in parallel using shared memory
  via OpenMP.
- **PyClaw** can be run in parallel on distributed-memory machines using MPI (through 
  PETSc) and has been shown to scale to tens of thousands of cores.
