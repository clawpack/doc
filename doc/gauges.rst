

.. _gauges:

***************
Gauges
***************


With AMRClaw in two space dimensions and GeoClaw
it is possible to specify gauge locations as points (x,y) where the values of all
components of q should be output every time step during the computation over some
time range (t1,t2).  

Gauges are useful in several ways, e.g.:

 1. To compare computational results to measurements from 
    physical gauges such as a pressure gauge or tide gauge that
    record data as a function of time at a single point,

 2. To better visualize how the solution behaves at a single point,

 3. To better compare results obtained with different methods or grid resolutions.
    Comparing two-dimensional pcolor or contour plots can be difficult whereas
    comparing to curves that give the solution as a function of time often reveals
    more clearly differences in accuracy or nonphysical oscillations.

.. _setrun_guages:

Gauge parameters in setrun
--------------------------

See also :ref:`setrun_amrclaw`.

Gauges are specified in `setrun` by adding lists of gauge data for each
desired gauge to the `ClawRunData`
object `rundata.gaugedata.gauges`.  This is initialized as an empty list and 
new gauges can be specified by::

    rundata.gaugedata.gauges.append([gaugeno, x, y, t1, t2])

with values

* *gaugeno* : integer

  the number of this gauge

* *x, y* : floats

  the location of this gauge

* *t1, t2* : floats

  the time interval over which gauge data should be output.


During the computation the value of all components of q at all gauge locations will
be output to a single file `fort.gauge` in the output directory.  Lines of this
file have the form::

   gaugeno  level  t  q[0]  q[1] ...  q[meqn-1]

where level is the AMR level used to determine the q values at this time.
Internally the finest level available at each gauge is used, with bilinear
interpolation to the gauge locations from the 4 nearest cell centers.

**New in 5.4.0.**
The output that is in the gauge files can be controlled by a variety of
parameters.  These can be specified on a per gauge basis or set for all gauges
specified.  The output parameters are

- *file_format* : Specifies the file format of the gauge data.  Currently
  *"ascii"* is the only value accepted.
- *display_format* : Specifies the format of the numbers written to the gauge
  file for each field.  These are Fortran format strings defaulting to
  *"e15.7"*.
- *q_out_fields* : Specifies which fields of the q array to output. Specify as
  a list the indices that should be output.  Defaults to *"all"*.
- *aux_out_fields* : Specifies which fields of the aux array to output.
  Specify as a list the indices that should be output. Defaults to *"none"*
- *min_time_increment* : Specify a minimum amount of time that should pass
  before recording the values at a gauge.  This can be useful for decreasing
  the amount of output at a gauge location that is currently being 
  time-stepped at small increments.  The default is *0* which effectively 
  turns off this constraint.

Setting these values can be done in multiple ways for convenience.  The most
direct way is via a dictionary with the keys as the gauge ids and the
corresponding parameter as the value.  For example, if we had 3 gauges with
ids 3, 7, 13 we could specify that they all use the display format *e26.16* by
setting::

    gaugedata.display_format = "e26.16"

or::

    gaugedata.display_format = {3:"e26.16", 13:"e8.6"}

to set gauge 3's display format to "e26.16", leave gauge 7 set to the default
and  set 13's to "e8.6".  For the parameters *q_out_fields* and
*aux_out_fields* one can also specify *"all"* to output all fields or *"none"*
to specify none of them (equivalent to an empty list of indices).  Both of
these arrays use Python indexing, i.e. they start at 0.

**Note:** For GeoClaw, the sea-surface value :math:`\eta = h + B` (sum of
water depth and topography) is also output as another column after the q fields.
In the case of the multilayer code the eta for each surface follows the q
fields for that layer.

**New in 5.4.0:**

 - Gauge output is accumulated in a buffer internally and written out
   intermitently, instead of writing to disk every time step.
   (The parameter `MAX_BUFFER` in the `amrclaw` library routines 
   `gauges_module.f90` controls the size of this buffer.)

 - The gauge output for the gauges is written to distinct files in the
   output directory, e.g. `gauge00001.txt` for gauge number 1.  In previous
   versions of Clawpack all gauges were written to a single file
   `fort.gauge`.  The new approach allows gauges to be written in parallel and
   also facilitates reading in a single gauge more quickly.

 - Some header info appears in each of these files to describe the gauge
   output.

 - When doing a restart (see :ref:`restart`), gauge output from the original run
   is no longer overwritten by the second run. Instead gauge
   output from the restart run will be appended to the end of each
   `gaugeXXXXX.txt` file.


Plotting tools
--------------

Several Python plotting tools are available to plot the gauge data, so you do not
have to parse the file `fort.gauge` yourself.  

If you want to read in the data for a particular gauge to manipulate it
yourself, you can do, for example::

    from clawpack.pyclaw.gauges import GaugeSolution
    g = GaugeSolution(gauge_id=1, path='_output')

to examine gauge number 1, for example.

Then:

* `g.t` is the array of times,
* `g.q` is the array of values recorded at the gauges (`g.q[m,n]` is the `m`th
  variable at time `t[n]`)


Alternatively, you can use the `getgauge` method of a `ClawPlotData` object,
e.g.::

    from clawpack.visclaw.data import ClawPlotData
    plotdata = ClawPlotData()
    plotdata.outdir = '_output'   # set to the proper output directory
    gaugeno = 1                   # gauge number to examine
    g = plotdata.getgauge(gaugeno)


In the `setplot` Python script you
can specify plots that are to be done for each gauge, similar to the manner in
which you can specify plots that are to be done for each time frame.  For example,
to plot the component q[0] at each gauge, include in `setplot` lines of this form::

    plotfigure = plotdata.new_plotfigure(name='q[0] at gauges', figno=300, \
                    type='each_gauge')

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = [-1.5, 1.5]
    plotaxes.title = 'q[0]'

    # Plot q[0] as blue line:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'b-'

Note that `plotdata.new_plotfigure` is called with `type='each_gauge'` which
denotes that this plot is to be produced for each gauge found in `setgauges.data`.
(When type is not specified, the default is `type='each_frame'` for time frame data).

If you type::

    $ make .plots

then html files will be created for the gauge plots along with the time frame plots
and will all show up in the index (usually in `_plots/_PlotIndex.html`).

When using Iplotclaw to interactively view plots, try::

    PLOTCLAW> plotgauge 1

to produce the plot for gauge 1, or simply::

    PLOTCLAW> plotgauge 

to loop through all gauges.  If you rerun the code without re-executing
`Iplotclaw`, you can refresh the gauge data via::

    PLOTCLAW> cleargauges

You can of course specify more than one plotitem on each plotaxes if you want.  For
example to plot the each gauge from the current run as a blue line and the same
gauge from some previous run (perhaps with a different grid resolution)
as a red line, you could add the following lines to the above example::

    # Plot q[0] from previous run as red line:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'r-'
    plotitem.outdir = '_output_from_previous_run'


Plotting gauge locations
------------------------

It is often convenient to plot the locations of the gauges on pcolor or contour
plots each time frame.  You can do this as follows, for example::

    plotfigure = plotdata.new_plotfigure(name='pcolor', figno=0)
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    # set other attributes as desired

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos='all', format_string='ko', add_labels=True)

    plotaxes.afteraxes = addgauges

You can replace `gaugenos='all'` by `gaugenos=[1,2]` or other list of specific
gauges to plot.  The `format_string` above specifies a black dot at each gauge
location and `add_labels=True` means that the gauge number will appear next to each
gauge.

If you want more control over this plotting you can of course copy the function
`plot_gauge_locations` from `clawpack.visclaw.gaugetools.py` 
to your setplot.py file and modify at will.

Examples
--------

Several of the examples found in `$CLAW/amrclaw/examples/`
and `$CLAW/geoclaw/examples/` contain the specification of gauges.


