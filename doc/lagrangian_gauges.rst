
.. _lagrangian_gauges:


Lagrangian gauges for particle tracking
=======================================

Specifying Lagrangian Gauges
----------------------------

Gauges are normally added in `setrun.py` via lines of the form:

::

    rundata.gaugedata.gauges.append([gaugeno, xg, yg, t1, t2])

where `(xg,yg)` is the gauge location and the gauge is to be tracked
for `t1 <= t <= t2`. Several properties can already be set for gauges,
for example `rundata.gaugedata.display_format` can be used to specify
how many digits to print out. This can be either a single format string
or a dictionary with an entry for each gauge, as described at
http://www.clawpack.org/gauges.html.

A new property has now been defined that specifies whether each gauge is
"stationary" or "lagrangian". In the past all gauges were stationary,
i.e. `(xg,yg)` is a fixed location. If a gauge is set to be lagrangian
then `(xg,yg)` specifies the initial location for `t <= t1` but
after this time the gauge location is updated using the fluid velocity
at each time that the gauge values are recorded (until time `t2` if
this is less than the final time of the computation, but often it is set
to a huge value like `1e9`).

The frequency of updating is controlled by
`rundata.gaugedata.min_time_increment` -- if this is 0 (the default)
then the gauge values are updated every time step.

Currently lagrangian gauges are implemented only in GeoClaw, for which
the fluid velocity `(ug,vg)` at a gauge location `(xg,yg)` is
computed from the momentum in the appropriate manner based on
`rundata.geo_data.coordinate_system`. This could be implemented more
generally in amrclaw in the same manner, but of course would only make
sense when solving equations for velocities are part of the solution.

The velocities are used to move each gauge location from the current
`(xg, yg)` to `(xg + dt*ug, yg + dt*vg)`, i.e. Forward Euler is used
to integrate :math:`dx/dt = u, dy/dt = v`.

The default if nothing is added to `setrun.py` is equivalent to
setting

::

    rundata.gaugedata.gtype = 'stationary'

so that all gauges are stationary. Alternatively this can be set to
`'lagrangian'` to make all gauges lagrangian, or
`rundata.gaugedata.gtype` can be a dictionary with
`rundata.gaugedata.gtype[gaugeno]` set to one of these values as
desired for each gauge. These values are written out to `gauges.data`
(as 1 for stationary, 2 for lagrangian), from which they are read into
GeoClaw.

When a gauge is lagrangian, the values written out (e.g. to the file
`_output/gauge00001.txt` for gauge 1) are modified so that the columns
that normally contain momenta `hu` and `hv` are replaced by the
current location `xg` and `yg`.

Visclaw tools for plotting
--------------------------

A new module `clawpack.visclaw.particle_tools` has been added to
facilitate plotting particle locations and particle paths.
