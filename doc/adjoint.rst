:orphan:

.. _adjoint:

**************************************
Guiding AMR with adjoint flagging
**************************************

A new approach to flagging cells for refinement was introduced in Clawpack
5.6.0 -- using the solution to an adjoint problem to determine what cells in
the forward solution should be refined because these cells may have an impact
on the some specified functional of interest.  This approach currently only
works for autonomous linear problems, in which case the adjoint problem needs
to be solved only once, and shifted versions of the adjoint solution can be
used at any time that flagging is performed.  The adjoint problem is solved
first and snapshots of the adjoint are saved.  These are read in at the start
of the forward solution, and space-time interpolation used as needed at each
regridding time.

The general approach is described in:

- [DavisLeVeque2018]_
- [Davis2018]_

See :ref:`adjoint_geoclaw` for discussion of the GeoClaw version.

Adjoint flagging is appropriate when you are not interested in computing an
accurate solution over the entire space-time domain, but rather are
interested only in some linear functional applied to the solution at each
time (or at a single time, or range of times).  
In one space dimension this functional has  the form

.. math::
   J(t) = \int_a^b \phi(x)^T q(x,t)\,dx

where :math:`a\leq x \leq b` is the full computational domain and
:math:`\phi(x)` is specified by the user as initial data for the
adjoint problem that is solved backward in time.  For example, if the
solution is of interest only over a small range of :math:`x` values, say
:math:`x_1 \leq x \leq x_2`,  then :math:`\phi(x)`
might be a box function with value 1 in this interval and 0 elsewhere, or
:math:`\phi(x)` could be a sharply peaked Gaussian about one location of
interest.  

In order to calculate an accurate solution near the location of interest at
the final time :math:`T` it may be necessary to refine the solution at other
places at earlier times.  The adjoint helps to identify where refinement is
needed.  The adjoint equation is first solved backward in time from the final
time :math:`T` with initial data :math:`\hat q(x,T) = \phi(x)` given by the
functional.  The waves propagating backward from time :math:`T` to some
regridding time :math:`t_r` in the adjoint solution identify which
waves in the forward solution at time :math:`t_r` will reach the location of
interest at time :math:`T`.  

Some examples for AMRClaw are available in 

- `$CLAW/amrclaw/examples/acoustics_1d_adjoint`
- `$CLAW/amrclaw/examples/acoustics_2d_adjoint`

In each case the main directory has a subdirectory named `adjoint`
that contains the code that must be run first in order to compute and save
snapshots of the adjoint solution.

The `adjoint/Makefile` must point to an appropriate Riemann solver for the adjoint
problem, which is a linear hyperbolic PDE with coefficient matrices that are
transposes of the coefficient matrices appearing in the forward problem. 

For variable-coefficient problems it is important to note that if the forward
problem is in conservation form then the adjoint is not, and vice versa.  For
example, in one space dimension, if the forward problem is
:math:`q_t + A(x)q_x = 0`, then the adjoint is 
:math:`\hat q_t + (A(x)^T \hat q)_x = 0`.  On the other hand if the
forward problem is 
:math:`q_t + (A(x)q)_x = 0`, then the adjoint is 
:math:`\hat q_t + A(x)^T \hat q_x = 0`.  

Note that the eigenvalues of :math:`A` are unchanged upon transforming but
the left eigenvectors of :math:`A` are now the right eigenvectors of
:math:`A^T`, and these must be used in the adjoint Riemann solver.
See for example `$CLAW/riemann/src/rp1_acoustics_variable_adjoint.f90`, used
for the example in `$CLAW/amrclaw/examples/acoustics_1d_adjoint/adjoint`.

Boundary conditions conditions may also need to be adjusted in going from the
forward to adjoint equation.  The guiding principle is that boundary
conditions must vanish during the integration by parts that is used to define
the adjoint PDE, as described in more detail in the references.

The functional of interest is defined in the `adjoint/qinit.f` file that 
specifies "initial" conditions for the adjoint problem.

The `adjoint/setrun.py` file specifies the final time :math:`T` (as
`clawdata.tfinal`) and the output interval via `clawdata.num_output_times`,
as usual.  You should specify :math:`T` at least as large as the final time
of interest in the forward problem, and frequent enough snapshots that
interpolation between them is reasonable.

You should set ::

     clawdata.output_format = 'binary'

so that output is in binary format, since the code that reads in these
snapshots in solving the forward problem assumes this format.


After solving the adjoint equation by running the code in the `adjoint`
subdirectory in the usual manner (e.g. `make .output`), the code in the main
directory can now be used to solve the forward problem, with the adjoint
snapshots used to guide AMR.

Starting in v5.6.0 a new attribute of `clawutil.data.ClawRunData` 
is available named `adjointdata`. This ia an object of class
`amrclaw.data.AdjointData` and has several attribures that should be set.
For example, in `$CLAW/amrclaw/examples/acoustics_1d_adjoint` they are set
as follows::

    #------------------------------------------------------------------
    # Adjoint specific data:
    #------------------------------------------------------------------
    # Also need to set flagging method and appropriate tolerances above

    adjointdata = rundata.adjointdata
    adjointdata.use_adjoint = True

    # location of adjoint solution, must first be created:
    adjointdata.adjoint_outdir = os.path.abspath('adjoint/_output')

    # time period of interest:
    adjointdata.t1 = rundata.clawdata.t0
    adjointdata.t2 = rundata.clawdata.tfinal

    if adjointdata.use_adjoint:
        # need an additional aux variable for inner product:
        rundata.amrdata.aux_type.append('center')
        rundata.clawdata.num_aux = len(rundata.amrdata.aux_type)
        adjointdata.innerprod_index = len(rundata.amrdata.aux_type)

The times `adjointdata.t1` and `adjointdata.t2` determine the time interval
over which the functional is of interest, and `adjointdata.adjoint_outdir`
specifies where the adjoint snapshots are found.

The flagging method and tolerances are set using, e.g.::

    # set tolerances appropriate for adjoint flagging:

    # Flag for refinement based on Richardson error estimater:
    amrdata.flag_richardson = False
    amrdata.flag_richardson_tol = 1e-5

    # Flag for refinement using routine flag2refine:
    amrdata.flag2refine = True
    amrdata.flag2refine_tol = 0.01

If `amrdata.flag_richardson` is `True` then we attempt to use estimates of
the one-step error generated by Richardson extrapolation together with the
adjoint to perform flagging.  This is still experimental.  *(Describe in more
detail).*

Otherwise it is
simply inner products of the forward and adjoint solutions that are computed
and a cell is flagged for refinement in cells where the magnitude of the
inner project is greater than `amrdata.flag2refine_tol`.


.. _adjoint_geoclaw:

Using adjoint flagging in GeoClaw
---------------------------------

The references above contain tsunami modeling examples, as does the paper

- [DavisLeVeque2016]_

An example can be found in

- `$CLAW/geoclaw/examples/tsunami/chile2010_adjoint`

Note that GeoClaw solves the nonlinear shallow water equations while the
adjoint as implemented in GeoClaw is only suitable for linear problems.  To
date the adjoint has only been used to guide refinement for waves propagating
across the ocean as a way to identify which waves will reach a target
location of interest (possibly after multiple reflections).  In the deep
ocean the tsunami amplitude is very small compared to the water depth and so
GeoClaw is essentially solving the linear shallow water equations, 
linearized about the ocean at rest.  Hence the adjoint problem is also solved
about the ocean at rest and the adjoint equations take essentially the same
form as the forward equations.  The adjoint Riemann solver can be found in

- `$CLAW/riemann/src/rpn2_geoclaw_adjoint.f`
- `$CLAW/riemann/src/rpt2_geoclaw_adjoint.f`

