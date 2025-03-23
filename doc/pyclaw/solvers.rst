:group: pyclaw

.. contents::

.. _solvers:

**********************************************
Using PyClaw's solvers: Classic and SharpClaw
**********************************************

At present, PyClaw includes two types of solvers:

    * Classic: the original 2nd-order Clawpack algorithms, in 1/2/3D
    * SharpClaw: higher-order wave propagation using WENO reconstruction and
      Runge-Kutta integration, in 1/2D


Solver initialization takes one argument: a Riemann solver, usually
from the Riemann repository.
Typically, all that is needed to select a different solver is to specify
it in the problem script, e.g.

.. doctest::

    >>> from clawpack import pyclaw
    >>> from clawpack import riemann
    >>> solver = pyclaw.ClawSolver2D(riemann.acoustics_2D)   

for the 2D acoustics equations and the Classic Clawpack solver or

.. doctest::

    >>> solver = pyclaw.SharpClawSolver2D(riemann.acoustics_2D) 

for the SharpClaw solver.  Most of the applications distributed with PyClaw
are set up to use either solver, depending on the value of the command line option
`solver_type`, which should be set to `classic` or `sharpclaw`.

Typically, for a given grid resolution, the SharpClaw solvers are more accurate
but also more computationally expensive.
For typical problems involving shocks, the Classic solvers are recommended.
For problems involving high-frequency waves, turbulence, or smooth solutions,
the SharpClaw solvers may give more accurate solutions at less cost.  This
is an active area of research and you may wish to experiment with both solvers.
Finally, note that the high-order WENO reconstruction in SharpClaw is
implemented only for uniform Cartesian grids.  For mapped grids, it is recommended
to use the Classic solvers or to use SharpClaw with TVD 2nd-order reconstruction.

Key differences between the Classic and SharpClaw solvers are:

    * The source term routine for the Classic solver should return the integral of
      the source term over a step, while the source term routine for SharpClaw
      should return the instantaneous value of the source term.  For Classic,
      the source term function is set using `solver.step_source`, while for
      SharpClaw it is set using `solver.dq_src`.  The `shock-bubble interaction
      example <https://www.clawpack.org/gallery/pyclaw/gallery/shock_bubble_interaction.html>`_
      shows how to use each of these.

    * The solvers have different options.  For a list of options and possible
      values, see the documentation of the :class:`~pyclaw.classic.solver.ClawSolver` and 
      :class:`~pyclaw.sharpclaw.solver.SharpClawSolver` classes.

For details of the solvers and their options, see :ref:`solvers_reference`.

.. _sharpclaw_solvers:

===============================
PyClaw's SharpClaw Solvers
===============================

The SharpClaw solvers are a collection of solvers that contain the
functionality of the Fortran code SharpClaw, developed in David Ketcheson's
thesis.  Solvers are available for 1D and 2D problems.
The SharpClaw solvers provide an interface similar to that
of the classic Clawpack solvers, but with a few different options.
The class `clawpack.pyclaw.SharpClawSolver` is a pure virtual class
not meant to be instantiated; you should use
`clawpack.pyclaw.SharpClawSolver1D` or `clawpack.pyclaw.SharpClawSolver2D`.
Most of the examples in `clawpack/pyclaw/examples` show how to use either
Classic or SharpClaw.


.. _pyclaw_clawpack_solvers:

==================================
Pyclaw's Classic Clawpack Solvers
==================================

The pyclaw classic clawpack solvers are a collection of solvers that represent
the functionality of the older versions of clawpack.  It comes in two forms, a
pure python version and a python wrapping of the fortran libraries.  All of the
solvers available provide the same basic interface and provide the same 
options as the old versions of clawpack.  
The class `clawpack.pyclaw.ClawSolver` is a pure virtual class
not meant to be instantiated; you should use
`clawpack.pyclaw.ClawSolver1D`, `clawpack.pyclaw.ClawSolver2D`, or `clawpack.pyclaw.ClawSolver3D`.


.. _pyclaw_clawpack_solvers_custom_BC_change:

=======================================
Change to Custom BC Function Signatures
=======================================

To allow better access to aux array data in the boundary condition functions 
both the `qbc` and `auxbc` arrays are now passed to the custom boundary
condition functions.  The new signature is

    def my_custom_BC(state, dim, t, qbc, auxbc, num_ghost):
        ...

and should be adopted as soon as possible.  The old signature

    def my_custom_BC(state, dim, t, bc_array, num_ghost):
        ...

can still be used but a warning will be issued and the old signature will not be
supported when version 6.0 is released.  This addition is available in versions > 5.2.0.
