:group: pyclaw

.. contents::

.. _output:

***********************
PyClaw output
***********************
In the documentation below, it is assumed that `claw` refers to a 
`pyclaw.controller.Controller` object, as is customary in the example
scripts.

Output frames
=============
The result of a PyClaw simulation is a set of snapshots, or *frames*
of the solution.  By default these are written to disk in a subdirectory
named `_outdir`.  Writing of output files can be turned off by setting
`claw.output_format = None`.

If `claw.keep_copy = True`, then output frames are also saved in memory
in the list `claw.frames`.  Each entry is a `pyclaw.solution.Solution`
object.  Thus the initial condition is available from `claw.frames[0].q`
and the final solution is in `claw.frames[-1].q`.
This can be convenient for working with
smaller simulations without reading from and writing to disk.


When output is saved/written
============================
PyClaw supports the same basic options as other Clawpack packages for
controlling output.  These are selected by setting `claw.output_style`:

    * `claw.output_style = 1`: Evenly spaced output, between the initial
      and final simulation times.  The number of outputs is the value of
      `claw.num_output_times`.
    * `claw.output_style = 2`: Manual specification of output times.
      Output will be written at the times specified in
      `claw.output_times`, which should be a list.
    * Write output after a certain number of steps have been taken;
      the number is specified in `claw.nstepout`.  For instance,
      if `claw.nstepout = 3`, then output is written after every 3
      steps.  This is most often useful for debugging.

Where and how output is written
===============================
The following options control the kind and location of output
files:

    * `claw.output_format`: A string specifying the format in which output data
      is written.  The default is `ascii`.  Other valid options are `binary`,
      `hdf5`, and `petsc`.  These formats can be useful for obtaining
      smaller output files or for loading output data into other software.
      Finally, this can be set to `None` to avoid writing any output to disk.
    * `claw.outdir`: Subdirectory in which to place output files.  Defaults
      to `_output`.
    * `claw.output_file_prefix`: Allows manual specification of the prefix
      for output files.
    * `claw.overwrite`: if True, allow existing files in the output
      directory to be overwritten by the current run.

What output is written
======================
PyClaw supports options to output more
than just the solution :math:`q`.  It can provide:

    * Snapshots of the values in the `aux` array at the initial time
      and/or output times.  This is turned on by setting
      `claw.write_aux_int = True` or `claw.write_aux_always = True`.
    * Output of derived quantities computed from :math:`q`; for instance,
      pressure (not a conserved quantity) could be computed from density
      and energy.
    * Output of scalar functionals, such as the total mass summed over the whole grid.
    * Output of gauge values, which are time traces of the solution at a
      single point.

Derived quantities and functionals are written out at the same times that the solution
:math:`q` is written.  While these could be computed in postprocessing, it is more efficient
to compute them at run-time for large parallel runs.  

Gauge output is written at every timestep.  In order to get this data without a
gauge, one would otherwise have to write the full solution out at every
timestep, which might be very slow.



Outputting derived quantities
===============================
It is sometimes desirable to output quantities other than those
in the vector q.  To do so, just add a function `p_function` to 
the controller that accepts the state and sets the derived quantities
in state.p

.. testsetup:: *

    from clawpack import pyclaw
    from clawpack import riemann
    import numpy as np
    solver = pyclaw.ClawSolver2D(riemann.acoustics_2D)
    domain = pyclaw.Domain([0.,0.],[1.,1.],[100,100])
    num_aux = 2 
    state = pyclaw.State(domain,solver.num_eqn,num_aux)
    solution = pyclaw.Solution(state,domain)
    grid = state.grid
    Y,X = np.meshgrid(grid.y.centers,grid.x.centers)
    r = np.sqrt(X**2 + Y**2)
    width = 0.2
    state.q[0,:,:] = (np.abs(r-0.5)<=width)*(1.+np.cos(np.pi*(r-0.5)/width))
    state.q[1,:,:] = 0.
    state.q[2,:,:] = 0.
    claw = pyclaw.Controller()

.. doctest::

    >>> def stress(state):
    ...    state.p[0,:,:] = np.exp(state.q[0,:,:]*state.aux[1,:,:]) - 1.

    >>> state.mp = 1
    >>> claw.p_function = stress

For a working example, see `the PyClaw P-system example <https://github.com/clawpack/pyclaw/blob/master/examples/psystem_2d/psystem_2d.py>`_.


Outputting functionals
===============================
In PyClaw a functional is a scalar quantity computed from :math:`q` that is written
to file at each output time.  For now, only functionals of the form

.. math::
   \begin{equation}
	F(q) = \int |f(q)| dx dy
   \end{equation}	

are supported.  In other words, the functional must be the absolute
integral of some function of :math:`q`.  To enable writing functionals, simply
set `state.mF` to the number of functionals::

    >>> state.mf = 1

and point the controller to a function that computes :math:`f(q)` elementwise
and stores it in the array
`state.F`.  For instance, if your first two conserved quantities are density
and momentum, you might write:

.. doctest::

    >>> def energy(state):
    ...    state.F[0,:,:] = 0.5 * state.q[0,:,:]*state.q[1,:,:]
    >>> claw.compute_F = energy
    >>> claw.F_file_name = 'total_energy'

The total energy (summed over the grid) would then be written to
`_output/total_energy.txt`.  The output file has two columns; the
first is time and the second is the functional value.  Output is
written at the same times that `q` is written to file.

For a working example, see `the PyClaw P-system example <https://github.com/clawpack/pyclaw/blob/master/examples/psystem_2d/psystem_2d.py>`_.

Using gauges
===================
A gauge in PyClaw is a single grid location for which output is written at
every time step.  This can be very useful in some applications, like comparing
with data from tidal gauges (from whence the name is derived) in tsunami modeling.
The gauges are managed by the grid object, and a grid at location :math:`(x,y)` 
may be added simply by calling `grid.add_gauges((x,y))`.  Multiple gauges
can be set at once by providing a list of coordinate tuples

.. testsetup::

    x1 = 0; x2 = 1; x3 = 2
    y1 = 1; y2 = 2; y3 = 0

.. doctest::

    >>> state.grid.add_gauges([(x1,y1),(x2,y2),(x3,y3)])

By default, the solution values are written out at each gauge location.
To write some other quantity, simply provide a function 
:math:`f(q,aux)` and point the solver to it

.. doctest::

    >>> def f(q,aux):
    ...    return q[1,:,:]/q[0,:,:]

    >>> solver.compute_gauge_values = f

For a working example, see `the PyClaw P-system example <https://github.com/clawpack/pyclaw/blob/master/examples/psystem_2d/psystem_2d.py>`_.


*******
Logging
*******
By default, PyClaw prints a message to the screen each time it writes
an output file.  This message is also writing to the file `pyclaw.log`
in the working directory.  There are additional warning or error messages
that may be sent to the screen or to file.  You can adjust the logger levels
in order to turn these messages off or to get more detailed debugging
information.

The controller provides one means to managing the logging with the
:py:attr:`~pyclaw.controller.verbosity` parameter and is provided as an easy
interace to control the console output (that which is shown on screen).  Valid
values for :py:attr:`~clawpack.pyclaw.controller.verbosity` are:

===========  ================
Verbosity     Message Level    
-----------  ----------------
0             Critical - This effectively silences the logger, since there are 
              no logging messages in PyClaw that correspond to this level.  May 
              be useful in an IPython notebook for instance if you want the 
              plots to appear immediately below your code.
1             Error - These are logged by the IO system to indicate that 
              something has gone wrong with either reading or writing a file.
2             Warning - There are no warning level logger messages.
3             Info - Additional IO messages are printed and some minor messages 
              dealing with hitting the end time requested.
4             Debug - If this level is set all logger output is displayed.  This
              includes the above and detailed time step information for every 
              time step (includes CFL, current dt and whether a time step is 
              rejected).
===========  ================

When running on a supercomputer, logging to file can be problematic because
the associated I/O can slow down the entire computation (this is true on 
Shaheen). To turn off all logging (both to screen and to file), you need to 
change the level of the root logger::

    import logging
    logger = logging.getLogger('pyclaw')
    logger.setLevel(logging.CRITICAL)

Again since we don't use `CRITICAL` logger messages in PyClaw, this has the 
effect of turning the loggers off. 
