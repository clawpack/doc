:group: pyclaw

.. _pyclaw_tutorial:
  
***********************************************
PyClaw tutorial: Solve the acoustics equations
***********************************************
PyClaw is designed to solve general systems of hyperbolic PDEs of the form

.. math::
   \begin{equation}
        \kappa(x) q_t + A(q,x) q_x = 0.
    \end{equation}

As an example, in this tutorial we'll set up a simulation that solves 
the acoustics equations in one dimension:

.. math::
   \begin{eqnarray}
        &p_t + K u_x = 0\\
        &u_t + \frac{1}{\rho} p_x = 0
    \end{eqnarray}

The key to solving a particular system of equations with PyClaw or other similar 
codes is a Riemann solver.  Riemann solvers for many systems are available as part 
of the clawpack/riemann package. 

We'll assume that you've already followed the :ref:`pyclaw_installation` instructions.

The following instructions show how to set up a problem step-by-step in an
interactive shell.  See :ref:`acoustics_1d` for the full source on which this is based.
   
The commands below should be typed at the Python prompt; we recommend using
IPython.

.. doctest::

    >>> from clawpack import pyclaw
    >>> from clawpack import riemann

The Solver
===========
PyClaw includes various algorithms for solving hyperbolic PDEs; each is implemented
in a :class:`~pyclaw.solver.Solver` object.  So the first step is to create a solver

.. doctest::

    >>> solver = pyclaw.ClawSolver1D(riemann.acoustics_1D)

Next we set the boundary conditions.  We'll use a wall (wall)
condition at the left boundary and a non-wall (zero-order extrapolation)
condition at the right boundary

.. doctest::

    >>> solver.bc_lower[0] = pyclaw.BC.wall
    >>> solver.bc_upper[0] = pyclaw.BC.extrap

The domain
==============
Next we need to set up the grid.  We do so by defining the
physical domain and the computational resolution.  We'll
use the interval :math:`(-1,1)` and 200 grid cells:

.. doctest::

    >>> domain = pyclaw.Domain([-1.0], [1.0], [200])
    
Notice that the calling sequence is similar to numpy's ``linspace`` command.

Finally, we set up a :class:`~pyclaw.Solution`
object, which will hold the solution values:

.. doctest::

    >>> solution = pyclaw.Solution(solver.num_eqn, domain)

Initial condition
=================
Now we will set the initial value of the solution

.. doctest::

    >>> state = solution.state
    >>> xc = state.grid.p_centers[0]      # Array containing the cell center coordinates
    >>> from numpy import exp
    >>> state.q[0,:] = exp(-100 * (xc-0.75)**2) # Pressure: Gaussian centered at x=0.75.
    >>> state.q[1,:] = 0.                       # Velocity: zero.


Problem-specific parameters
===========================
The acoustics equations above have some coefficients -- namely, the
bulk modulus :math:`K` and density :math:`\rho` -- that must be defined.
Furthermore, checking the code for the Riemann solver we've chosen
reveals that it expects us to provide values for the impedance :math:`Z`
and sound speed :math:`c`.  These values are stored in a Python dictionary
called problem_data that is a member of the :class:`~pyclaw.state.State`

.. doctest::

    >>> from math import sqrt
    >>> rho = 1.0
    >>> bulk = 1.0
    >>> state.problem_data['rho'] = rho
    >>> state.problem_data['bulk'] = bulk
    >>> state.problem_data['zz'] = sqrt(rho*bulk)
    >>> state.problem_data['cc'] = sqrt(bulk/rho)

The controller
===================
The most convenient way to run a PyClaw simulation is by using a
:class:`~pyclaw.controller.Controller` object.  The controller
directs the solver in advancing the solution and handles output.

.. doctest::

    >>> controller = pyclaw.Controller()
    >>> controller.solution = solution
    >>> controller.solver = solver
    >>> controller.tfinal = 1.0

At last everything is set up!  Now run the simulation

.. doctest::

    >>> status = controller.run()

This should print out a few lines indicating the output times. It also prints
the minimum and maximum tipe-step used, the number of steps required for the
computation and the maximum CFL number. The simplest way to plot the solution
is

.. doctest::

    >>> from clawpack.pyclaw import plot
    >>> plot.interactive_plot() # doctest: +SKIP
    

That's it!  Your first PyClaw simulation.  Of course, we've only
scratched the surface of what PyClaw can do, and there are many
important options that haven't been discussed here.  To get an
idea, take a look through the pyclaw/examples directory and try running
some other examples.  It's also a good idea to get more deeply
acquainted with the main :ref:`pyclaw_classes`.
