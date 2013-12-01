
.. _user_routines:

User files required for the Fortran code
========================================

The `Makefile` in an application directory shows the set of Fortran source
code files that are being used.  Most of these files are typically in one of
the libraries, but a few subroutines must be provided by the user in order to
specify the hyperbolic problem to be solved and the initial conditions.
Other subroutines may also be provided that are application-specific.
This page summarizes some of the most common user-modified routines.

The calling sequence for each subroutine differs with the number of space
dimensions.  The sample calling sequences shown below are for one space
dimension.  

See the examples in the following directories for additional samples:

* `$CLAW/classic/examples`
* `$CLAW/amrclaw/examples`
* `$CLAW/geoclaw/examples`


.. _user_qinit:

Specifying the initial conditions
----------------------------------

Calling sequence in 1d::

      subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)

Typically every application directory contains a file `qinit.f` or
`qinit.f90` that sets the initial conditions, typically in a loop such as::

    do i=1,mx
        xi = xlower + (i-0.5d0)*dx
        q(1,i) = xi**2
        enddo

This loop would set the value of :math:`q^1` in the i'th cell to
:math:`x_i^2` where :math:`x_i` is the cell center.  
For the finite volume methods used in Clawpack, the initial data should
really be set to be the cell average of the data over each grid cell,
determined by integrating the data for the PDE.
If the initial data is given by a smooth function, then evaluating the 
function at the center of the grid cell generally agrees with the cell
average to :math:`{\cal O}(\Delta x^2)` and is consistent with the
second-order accurate high-resolution methods being used in Clawpack.  

For a system of more than 1 equation, you must set `q(m,i)` for `m =
1, 2, ..., num_eqn`.

For adaptive mesh refinement codes, the `qinit` subroutine will be called
for each grid patch at the initial time, so it is always necessary to
compute the cell centers based on the information passed in.

.. _user_riemann:

Specifying the Riemann solver
-----------------------------

The Riemann solver defines the hyperbolic equation that is being solved and
does the bulk of the computational work -- it is called at every cell
interface every time step and returns the information about waves and speeds
that is needed to update the solution.  

See :ref:`riemann` for more details about the Riemann solvers.

All of the examples that come with Clawpack use Riemann solvers that are
provided in the directory `$CLAW/riemann/src`, see the `Makefile` in one of
the examples to determine what Riemann solver file(s) are being used (in two
and three space dimensions, transverse Riemann solvers are also required).

The directory `$CLAW/riemann/src` contains Riemann solvers for many
applications, including advection, acoustics, shallow water equations, Euler
equations, traffic flow, Burgers' equation, etc.

.. _user_bc:

Specifying boundary conditions
--------------------------------------------------------

Boundary conditions are set by the library routines:

* `$CLAW/classic/src/Nd/bcN.f` for the classic code (N = 1, 2, 3).
* `$CLAW/amrclaw/src/Nd/bcNamr.f` for the amrclaw code (N = 2, 3).

Several standard choices of boundary condition procedures are provided in
these routines -- see :ref:`bc` for details.

For user-supplied boundary conditions that are not implemented in the
library routines, the library routine can be copied to the application
directory and changes made as described at :ref:`bc_user`.
The `Makefile` should then be modified to point to the local version.


.. _user_setprob:

Specifying problem-specific data
---------------------------------

Often an application problem has data or parameters that is most
conveniently specified in a user-supplied routine named `setprob`.  There is
a library version that does nothing in case one is not specified in the
application directory.  As usual, the `Makefile` indicates what file is
used.

The `setprob` subroutine takes no arguments.  Data set in `setprob` is often
passed in common blocks to other routines, such as `qinit` or the Riemann
solver.  This is appropriate only for data that does not change with time
and does not vary in space (e.g. the gravitational constant `g` in the
shallow water equations, or the density and bulk modulus for acoustics in
a homogenous medium).

Note that named common blocks must have the same name in each routine where
they are used.  Check any Riemann solvers you use (including those from
`$CLAW/riemann/src`) to see if they require some parameters to be passed in
via a common block.  If so, `setprob` is the place to set them.

For spatially-varying data, see :ref:`user_setaux` below.

Often `setprob` is written so that it reads in data values from a file,
often called `setprob.data`.  This makes it easier to modify parameter
values without recompiling the code.  It is also possible to set these
values in `setrun.py` so that this input data is specified in the same file
as other input parameters.  For a sample, see
`$CLAW/classic/examples/acoustics_1d_heterogeneous`, for example.

.. _user_setaux:

Specifying spatially-varying data using `setaux`
-------------------------------------------------

Some problems require specifying spatially varying data, for example the
density and bulk modulus for acoustics in a heterogenous medium might vary
in space and in principle could be different in each grid cell.  The best
way to specify such data is by use of *auxiliary arrays* that are created
whenever a grid patch for the solution is created and have the same number
of cells with `num_aux` components in each cell.  The value `num_aux` is
specified in `setrun.py`, and the contents of the `aux` arrays are filled by
a subroutine named `setaux`, which in one dimension has the calling
sequence::

    subroutine setaux(mbc,mx,xlower,dx,maux,aux)

If adaptive refinement is being used, then every time a new grid patch is
created at any refinement level this subroutine will be called to fill in
the corresponding `aux` arrays.  For a sample, see
`$CLAW/classic/examples/acoustics_1d_heterogeneous`, for example.

If the `aux` arrays need to be time-dependent, the easiest way to adjust
them each time step is in the routine `b4step` described below.

.. _user_b4step:

Using `b4step` for work to be done before each time step
--------------------------------------------------------

Describe.

.. _user_src:

Using `src` for source terms
--------------------------------------------------------

Problems of the form 
:math:`q_t(x,t) + f(q(x,t))_x = \psi(q,x,t)`
can be solved using a fractional step approach, as described in Chapter 17
of [LeVeque-FVMHP]_.  The user can provide a subroutine named `srcN` in `N`
space dimensions that takes a single time step on the equation
:math:`q_t = \psi`.  In one dimension the calling sequence is::

      subroutine src1(meqn,mbc,mx,xlower,dx,q,maux,aux,t,dt)

On output the `q` array should have been updated by using the input values
as initial data for a single step of length `dt` starting at time `t`.

The library version of `srcN` does nothing.  If you copy this to an
application directory and modify for your equation, you must modify the
`Makefile` to point to the local version.  You must also set the
`source_split` parameter in `setrun.py` (see :ref:`setrun`) to either
`godunov` or `"strang"`.  In the former case, the 1st order Godunov
splitting is used (after each time step on the homogenous 
hyperbolic equation, a time step of the same length is taken on the source
terms).  In the latter case the 2nd order Strang splitting is used: the time
step on the hyperbolic part is both preceeded and followed by
a time step of half the length on the source terms.




