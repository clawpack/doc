
.. _wp_algorithms:

Wave-propagation algorithms
===========================

.. _wp_1d:

One space dimension
-------------------

Clawpack can be used to solve a system of equations of the form

.. math::
   \kappa(x)q_t+f(q)_x = \psi(q,x,t),

where :math:`q=q(x,t)\in{\cal R}^m`.  The standard case of a homogeneous
conservation law has :math:`\kappa\equiv 1` and :math:`\psi\equiv 0`,

.. math::
   q_t+f(q)_x=0.
   :label: cons1d

The flux function :math:`f(q)` can also depend explicitly on :math:`x` and
:math:`t` as well as on :math:`q`.
Hyperbolic systems that are not in conservation form, e.g.,

.. math::
   q_t+A(x,t)q_x=0,

can also be solved. See [LeVeque-FVMHP]_ for more details about the
wave-propagation algorithms that are briefly described here.

The basic requirement on the homogeneous system is that it be hyperbolic in
the sense that a Riemann solver can be specified that, for any two states
:math:`q_{i-1}` and :math:`Q_i`, returns a set of :math:`M_w` waves
:math:`{\cal W}^p_{i-1/2}` and speeds
:math:`s^p_{i-1/2}`
satisfying

.. math::
   \sum_{p=1}^{M_w} {\cal W}^p_{i-1/2} = Q_i-Q_{i-1} \equiv \Delta Q_{i-1/2}.


The Riemann solver must also return a left-going fluctuation 
:math:`{\cal A}^-\Delta Q_{i-1/2}` and
a right-going fluctuation :math:`{\cal A}^+\Delta Q_{i-1/2}`. In
the standard conservative case :eq:`cons1d` these should satisfy

.. math::
   {\cal A}^-\Delta Q_{i-1/2}+{\cal A}^+\Delta Q_{i-1/2} = f(Q_i)-f(Q_{i-1})
   :label: asum

and the fluctuations then define a "flux-difference splitting".

.. math::
   {\cal A}^-\Delta Q_{i-1/2} = \sum_p (s^p_{i-1/2})^- {\cal W}^p_{i-1/2},
   \qquad {\cal A}^+\Delta Q_{i-1/2} = \sum_p (s^p_{i-1/2})^+ {\cal W}^p_{i-1/2},
    
where :math:`s^- = \min(s,0)` and :math:`s^+ = \max(s,0)`.  In the
nonconservative case \eqn{claw_1dnoncon}, there is no "flux function"
:math:`f(q)`,
and the constraint :eq:`asum` need not be satisfied.

Godunov's method
----------------

Only the fluctuations are used for the first-order Godunov method, which is
implemented in the form

.. math::
   Q_i^{n+1} = Q_i^n - \frac{\Delta t}{\Delta x}\left[{\cal A}^+\Delta Q_{i-1/2}
   + {\cal A}^-\Delta Q_{i+1/2}\right],

assuming :math:`\kappa \equiv 1`.

The Riemann solver must be supplied by the user in the form of a subroutine
`rp1`, as described in :ref:`user_riemann`.


Typically the Riemann solver first computes waves and speeds and then uses
these to compute :math:`{\cal A}^+Q_{i-1/2}` and :math:`{\cal A}^-Q_{i-1/2}`
internally in the Riemann solver.  

High-resolution methods
-----------------------

The waves and speeds must also
be returned by the Riemann solver in order to use the high-resolution
methods described in [LeVeque-FVMHP]_, which reduce to a second-order
accurate Lax-Wendroff type method when limiters are not used.  
By introducing wave limiters, non-physical oscillations near discontinuities
or steep gradients in the solution can be avoided.  The limiters are based
on the theory of TVD methods for nonlinear scalar equations and extended in
a natural way to systems of equations.

These methods take the form

.. math::

   Q_i^{n+1} = Q_i^n - \frac{\Delta t}{\Delta x}\left[{\cal A}^+Q_{i-1/2} 
   + {\cal A}^-Q_{i+1/2}\right]
   - \frac{\Delta t}{\Delta x}(\tilde F_{i+1/2} - \tilde F_{i-1/2})

where

.. math::

   \tilde F_{i-1/2} = \frac 1 2 \sum_{p=1}^{M_w} |s^p_{i-1/2}|
   \left( 1-\frac{\Delta t}{\Delta x} |s^p_{i-1/2}|\right)
   \tilde{\cal W}_{i-1/2}^p.

Here :math:`\tilde{\cal W}_{i-1/2}^p` represents a limited version of the wave
:math:`{\cal W}_{i-1/2}^p`, obtained by comparing :math:`{\cal W}_{i-1/2}^p` to
:math:`{\cal W}_{i-3/2}^p` if :math:`s^p>0` or to :math:`{\cal W}_{i+1/2}^p`
if :math:`s^p<0`.

.. _wp_fwave:

f-wave formulation
-------------------

For equations with spatially-varying flux functions, such as

.. math::
   q_t+f(q,x)_x=0.
   :label: cons1dvf

it is often convenient to use the f-wave formulation of the algorithm, as
proposed in [BaleLevMitRoss02]_. Rather than decomposing the jump
:math:`Q_i-Q_{i-1}` into waves, the idea of the f-wave approach is to
decompose the flux difference :math:`f(Q_i,x_i) - f(Q_{i-1},x_{i-1})` into
f-waves using appropriate eigenvectors of the Jacobian matrices to either
side of the interface.  See :ref:`riemann_fwave` for more details.



Capacity functions
------------------

When a capacity function :math:`\kappa(x)` is present, the Godunov method becomes

.. math::

   Q_i^{n+1} = Q_i^n - \frac{\Delta t}{\kappa_i \Delta x}
   \left[{\cal A}^+Q_{i-1/2} + {\cal A}^-Q_{i+1/2}\right],

See [LeVeque-FVMHP]_ for discussion of this algorithm and its extension to
the high-resolution method.
Capacity functions are useful in particular for solving equations on a
mapped grid. 

Source terms
------------

If the equation has a source term,
a routine `src1` must also be supplied that
solves the  source term equation :math:`q_t=\psi` over a time step.
A fractional step method  is used to couple this with the homogeneous
solution, as described in :ref:`user_src`.

Boundary conditions
-------------------

Boundary conditions are imposed by setting values in ghost cells each time
step, as described in :ref:`bc`.



TODO: Continue description -- 2d and 3d, transverse solvers.
