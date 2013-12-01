
.. _riemann:

Riemann solvers
===============

The Riemann solver defines the hyperbolic equation that is being solved and
does the bulk of the computational work -- it is called at every cell
interface every time step and returns the information about waves and speeds
that is needed to update the solution.  

The directory `$CLAW/riemann/src` contains Riemann solvers for many
applications, including advection, acoustics, shallow water equations, Euler
equations, traffic flow, Burgers' equation, etc.

.. _rp1:

One-dimensional Riemann solver
------------------------------

Understanding the 1-dimensional solver is a critical first step since in 2
or 3 dimensions the bulk of the work is done by a "normal solver" that
solves a 1-dimensional Riemann problem normal to each cell edge.  (These are
then augmented by transverse solvers as described below.)

See :ref:`wp_algorithms` and [LeVeque-FVMHP]_ for more details about how the
algorithms in Clawpack use the Riemann solution.

The calling sequence for the 1-dimensional Riemann solver subroutine `rp1`
is::

    subroutine rp1(maxm,meqn,mwaves,maux,mbc,mx,ql,qr,auxl,auxr,wave,s,amdq,apdq)

    ! Input arguments
    integer, intent(in) :: maxmx,meqn,mwaves,mbc,mx,maux
    double precision, intent(in), dimension(meqn, 1-mbc:maxmx+mbc) :: ql,qr
    double precision, intent(in), dimension(maux, 1-mbc:maxmx+mbc) :: auxl,auxr

    ! Output arguments
    double precision, intent(out) :: s(mwaves, 1-mbc:maxmx+mbc)
    double precision, intent(out) :: fwave(meqn, mwaves, 1-mbc:maxmx+mbc)
    double precision, intent(out), dimension(meqn, 1-mbc:maxmx+mbc) :: amdq,apdq

Note that the integer parameters used in this calling sequence have
different names than are now being used in `setrun.py`.  The correspondence
is:

* `meqn = num_eqn`, the number of equations in the system,
* `mwaves = num_waves`, the number of waves in each Riemann solution,
* `mx = num_cells`, the number of grid cells,
* `maux = num_aux`, the number of auxiliary variables,

The input data consists of two arrays `ql` and `qr`. The value
ql(:,i) is the value :math:`Q_i^L` at the left edge of the i’th
cell, while qr(:,i) is the value :math:`Q_i^R` at the right edge
of the i’th cell, as indicated in this figure:

.. image :: images/qlqr.png
   :width: 10cm

Normally `ql = qr` and both values agree with :math:`Q_i^n` , the cell
average at time :math:`t_n`. 
More flexibility is allowed because in some applications, or in
adapting clawpack to implement different algorithms, it is useful to allow
different values at each edge. For example, we might want to define a
piecewise linear function within the grid cell as illustrated in the figure
and then solve the Riemann problems between these values. This approach to
high-resolution methods is discussed in Chapter 6 of [LeVeque-FVMHP]_.

Note that the Riemann problem at the interface :math:`x_{i−1/2}`
between cells :math:`i − 1` and :math:`i` has data:

* Left state: :math:`Q_{i-1}^R` =  `qr(:,i-1)`,
* Right state: :math:`Q_{i}^L =` `ql(:,i)`.

This notation is rather confusing since normally we use :math:`q_\ell`
to denote the left state and :math:`q_r`  to denote the right state
in specifying Riemann data.

The Riemann solver `rp1` also has input parameters `auxl` and `auxr`
that contain values of the auxiliary variables if these are being used (see
:ref:`user_setaux`). 
Normally `auxl = auxr = aux` when the Riemann solver is called from the
standard Clawpack routines.

The routine `rp1` must solve the Riemann problem for each value of `i`,
and return the following (for `i=1-mbc` to `mx+mbc`):

* `amdq(1:meqn,i)`  = the vector :math:`{\cal A}^-\Delta Q_{i-1/2}`,

* `apdq(1:meqn,i)`  = the vector :math:`{\cal A}^+\Delta Q_{i-1/2}`,

* `wave(1:meqn,i,p)`  = the vector :math:`{\cal W}^p_{i-1/2}`,

* `s(i,p)`  = the wave speed :math:`s^p_{i-1/2}` for each wave.

This uses the notation of :ref:`wp_algorithms` and [LeVeque-FVMHP]_.

.. _riemann_fwave:

f-wave Riemann solvers
----------------------

As described in :ref:`wp_fwave`, for spatially-varying flux functions it is
often best to use the f-wave formulation of the wave-propagation algorithms.
This can be implemented in Clawpack by providing a
suitable Riemann solver that returns f-waves instead of ordinary waves,
obtained by decomposing 
the flux difference :math:`f(Q_i,x_i) - f(Q_{i-1},x_{i-1})` into
f-waves using appropriate eigenvectors of the Jacobian matrices to either
side of the interface.  The Riemann solver has the same form and calling
sequence as described above, the only difference is that the output
argument `wave` should return an array of f-waves.  while `amdq`
and `apdq` have the same meaning as before.

In order to indicate that the Riemann solver returns f-waves, the parameter
`runclaw.use_fwaves` in `setrun` should be set to `True`, see :ref:`setrun`.

TODO: Continue description -- 2d and 3d, transverse solvers.
