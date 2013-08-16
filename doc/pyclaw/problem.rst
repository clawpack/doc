:group: pyclaw

.. _problem_setup:

=============================
Setting up your own problem
=============================
The best way to set up a new problem is to find an existing problem setup that
is similar.  The main steps are:

    * Write the initialization script
    * Write routines for source terms, custom boundary conditions, or other customizations
    * Write a Riemann solver (if solving a new system of equations)
    * Write a Makefile if using any custom Fortran code
    * Write a setplot.py file for visualization

If needed for your problem, custom Riemann solvers, boundary condition routines,
source term routines, and other functions can all be written in Python but you may
prefer to write some of them in Fortran for performance reasons.
The latter approach requires direct use of 
`f2py <http://www.scipy.org/F2py>`_.  See :ref:`port_Example` for 
more details.


Writing the initialization script
===================================
This script should:

    * Import the appropriate package (pyclaw or petclaw)
    * Instantiate a :class:`~pyclaw.solver.Solver` and specify the Riemann solver to use
    * Set the boundary conditions
    * Define the domain through a :class:`~pyclaw.geometry.Domain` object
    * Define a :class:`~pyclaw.solution.Solution` object
    * Set the initial condition

Usually the script then instantiates a :class:`~pyclaw.controller.Controller`, sets the
initial solution and solver, and calls :meth:`~pyclaw.controller.Controller.run`.

Setting initial conditions
----------------------------
Once you have initialized a Solution object, it contains a member state.q
whose first dimension is num_eqn and whose remaining dimensions are those
of the grid.  Now you must set the initial condition.  For instance

.. testsetup:: *

    from clawpack import pyclaw
    from clawpack import riemann
    x = pyclaw.Dimension('x',-1.0,1.0,100)
    y = pyclaw.Dimension('y',-1.0,1.0,100)
    domain = pyclaw.Domain([x,y])
    solver = pyclaw.ClawSolver2D(riemann.acoustics_2D)
    state = pyclaw.State(domain,solver.num_eqn,num_aux)

.. doctest::

    >>> import numpy as np
    >>> Y,X = np.meshgrid(state.grid.y.centers,state.grid.x.centers)
    >>> r = np.sqrt(X**2 + Y**2)
    >>> width = 0.2
    >>> state.q[0,:,:] = (np.abs(r-0.5)<=width)*(1.+np.cos(np.pi*(r-0.5)/width))
    >>> state.q[1,:,:] = 0.
    >>> state.q[2,:,:] = 0.

Note that in a parallel run we only wish to set the local values of the state
so the appropriate geometry object to use here is the 
:class:`~pyclaw.geometry.Grid` class.

Setting auxiliary variables
----------------------------
If the problem involves coefficients that vary in space or a mapped grid,
the required fields are stored in state.aux.  In order to use such fields,
you must pass the num_aux argument to the State initialization

.. testsetup::

    num_aux = 2

.. doctest::

    >>> state = pyclaw.State(domain,solver.num_eqn,num_aux)

The number of fields in state.aux (i.e., the length of its first dimension)
is set equal to num_aux.  The values of state.aux are set in the same way
as those of state.q.

Setting boundary conditions
----------------------------
The boundary conditions are specified through solver.bc_lower and 
solver.bc_upper, each of which is a list of length ``solver.num_dim``. The 
ordering of the boundary conditions in each list is the same as the ordering of 
the Dimensions in the Grid; typically :math:`(x,y)`. Thus 
``solver.bc_lower[0]`` specifies the boundary condition at the left boundary 
and ``solver.bc_upper[0]`` specifies the condition at the right boundary. 
Similarly, ``solver.bc_lower[1]`` and ``solver.bc_upper[1]`` specify the 
boundary conditions at the top and bottom of the domain.

PyClaw includes the following built-in boundary condition implementations:

    * ``pyclaw.BC.periodic`` - periodic
    * ``pyclaw.BC.extrap`` - zero-order extrapolation
    * ``pyclaw.BC.wall`` - solid wall conditions, assuming that the 2nd/3rd    
      component of q is the normal velocity in x/y.

Other boundary conditions can be implemented by using ``pyclaw.BC.custom``, and
providing a custom BC function.  The attribute solver.user_bc_lower/upper must
be set to the corresponding function handle.  For instance


.. doctest::

    >>> def custom_bc(state,dim,t,qbc,num_ghost):
    ...    for i in xrange(num_ghost):
    ...       qbc[0,i,:] = q0

    >>> solver.bc_lower[0] = pyclaw.BC.custom
    >>> solver.user_bc_lower = custom_bc

If the ``state.aux`` array is used, boundary conditions must be set for it
in a similar way, using ``solver.aux_bc_lower`` and ``solver.aux_bc_upper``.
Note that although state is passed to the BC routines, they should
NEVER modify state.  Rather, they should modify qbc/auxbc.

Setting solver options
----------------------------

Using your own Riemann solver
=============================
The Riemann package has solvers for many hyperbolic systems.  If your problem
involves a new system, you will need to write your own Riemann solver.  
A nice example of how to compile and import your own Riemann solver can be seen
`here https://github.com/damiansra/empyclaw/tree/master/maxwell_1d_homogeneous`_.
You will need to:

    * Put the Riemann solver in the same directory as your Python script
    * Write a short makefile calling f2py
    * import the Riemann solver module in your Python script

Here are some tips if you are converting an old Clawpack 4.5 or earlier Riemann solver:

    * Rename the file from .f to .f90 and switch to free-format Fortran
    * Move the spatial index (i) to the last place in all array indexing

Please do contribute your solver to the package by sending a pull request on Github
or e-mailing one of the developers.  To add your Riemann solver to the Clawpack
Riemann package, you will need to:

    * Place the .f90 file(s) in clawpack/riemann/src.
    * Add the solver to the list in clawpack/riemann/setup.py
    * Add the solver to the list in clawpack/riemann/src/python/riemann/setup.py 
    * Add the solver to the list in clawpack/riemann/src/python/riemann/Makefile
    * Add the solver to the list in clawpack/riemann/src/python/riemann/__init__.py


For very simple problems in one dimension, it may be worthwhile to write the
Riemann solver in Python, especially if you are more comfortable with Python
than with Fortran.  For two-dimensional problems, or one-dimensional problems
requiring fine grids (or if you are impatient) the solver should be written
in Fortran.  The best approach is generally to find a similar solver in the
Riemann package and modify it to solve your system.

Adding source terms
==============================
Non-hyperbolic terms (representing, e.g., reaction or diffusion) can be included
in a PyClaw simulation by providing an appropriate function handle to 

    * solver.step_source if using Classic Clawpack.  In this case, the function
      specified should modify q by taking a step on the equation :math:`q_t = \psi(q)`.

    * solver.dq_src if using SharpClaw.  In this case, the function should
      return :math:`\Delta t \cdot \psi(q)`.

For an example, see pyclaw/examples/euler_2d/shockbubble.py.

Setting up the Makefile
===============================
Generally you can just copy the Makefile from an example in pyclaw/examples and
replace the value of `RP_SOURCES`.  Make sure the example you choose has the
same dimensionality.  Also be sure to use the f-wave targets if your Riemann
solver is an f-wave solver.


