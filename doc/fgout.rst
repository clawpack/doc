
.. _fgout:

==============================
Fixed grid output (fgout)
==============================

**New in v5.9.0, with a change to the API in v5.11.0:** 

See also:

 - :ref:`fgout_tools_module`
 - :ref:`setrun_fgout` - For adding fgout data to `setrun.py`
 - :ref:`fgout_examples` - Links to some examples

GeoClaw has the capability to output the results at specified output times
on a specified "fixed grid" by interpolating from the AMR grids active at each 
output time.

This complements the normal output frame capabilities of Clawpack,
and has several advantages for some applications, particularly when
making animations or when using the GeoClaw solution as input to
another process, such as particle tracking.

Advantages include:

    1. The solution is output on a fixed uniform grid at each fgout
    time, independent of the AMR structure.  This is useful in order
    to produce a set of frames for an animation that are all the same
    resolution with the same size array.

    2. It is possible to produce fgout outputs at times that do not
    coincide with the time steps of the computation, whereas standard
    frame output can only occur at the end of a time step on the coarsest
    level.  Hence fgout output does not require reducing the time step to hit
    the fgout times exactly, which would cause significant increase in
    computing time and possible degradation of the computed solution
    if the coarse grid time steps had to be greatly reduced to match
    frequent output times in a finely resolved region.

    3. When exploring the solution or making an animation over one
    small portion of the computational domain, it is possible to
    create an fgout grid that only covers this region at the desired
    resolution and does not require output of the entire AMR structure
    over the entire computational domain at each output time.
    This can *greatly* reduce the size of the output in some cases.

    4. If an fgout grid is output with sufficiently fine temporal resolution,
    then this set of data can be used to explore the solution in various ways
    using post-processing.  For example, it is possible to spatially
    interpolate to any desired location within the grid and produce a time
    series of the solution at this point.   This would be similar to the gauge
    output produced by GeoClaw, but would allow specifying the point of
    interest after the fact, whereas standard gauages must be specified in
    advance of the GeoClaw run (see :ref:`gauges`).  Similarly, the fluid
    velocities computed from GeoClaw can be used to track particles (as
    massless tracer particles for visualization purposes, or with more
    complex dynamics for debris tracking). The Python module
    :ref:`fgout_tools_module` provides some tools for interpolating
    from fgout frames to arbitrary points `(x,y,t)`.

The original version of this, capability, originally called `fixedgrid
output` in Clawpack 4.6 was carried over and existed through v5.8.x, but has
been removed as of Version 5.9.0.

An improved version for monitoring maximum values and arrival times was
added in v5.7.0, referred to as `fgmax grids`; see :ref:`fgmax`.

An improved version of the capability to output on a fixed grid at more
frequent times than the standard AMR output has been introduced in v5.9.0,
and these are now called `fgout grids` to complement the `fgmax grids`.
These `fgout grids` are described further below (with some changes
introduced in v5.11.0).

.. _fgout_input:

Input file specification
-------------------------

The GeoClaw Fortran code reads in one or more files that specify fgout grids 
grid(s) for writing out the solution on a fixed grid throughout
the computation.  

The desired fgout grid(s) are specified to GeoClaw in `setrun.py`,
by setting `rundata.fgout_data.fgout_grids` to be a list of objects
of class `fgout_tools.FGoutGrid`.  
After doing `make data` or `make .output`, these are written out
to `fgout_grids.data`, the file that is read by the Fortran code at runtime.

More than one fgout grid can be specified, and an integer label with at
most 4 digits can be assigned to each grid.  You can assign numbers
to each fgout grid using the `fgno` attribute, described below.
If you do not assign numbers, they will be numbered sequentially (1,2, etc.)
based on the order they are specified in the `setrun.py` file.


A simple example
-----------------

**Modified for v5.11.0**

Here's an example of how one grid can be set up::

    from clawpack.geoclaw import fgout_tools

    fgout_grids = rundata.fgout_data.fgout_grids  # empty list initially

    fgout = fgout_tools.FGoutGrid()
    fgout.fgno = 1
    fgout.output_format = 'binary32'
    fgout.nx = 200
    fgout.ny = 250
    fgout.x1 = -115.
    fgout.x2 = -70.
    fgout.y1 = -55.
    fgout.y2 = -10.
    fgout.output_style = 1  # new in v5.11.0
    fgout.tstart = 0.
    fgout.tend = 6.*3600
    fgout.nout = 37
    fgout.q_out_vars = [1,2,3,4]  # new in v5.11.0
    fgout_grids.append(fgout) 

This specifies output on a 200 by 250 grid of equally spaced points on the
rectangle `[-115, -70] x [-55, -10]`.  (Note that these values are cell
edges, the actual fgout points will be at cell centers, 
displaced from these edges.  See :ref:`fgout_registration` below.)

The output times are equally spaced
from `tstart = 0` to `tend = 6*3600` (6 hours).  
There will be 37 total outputs, so one every 10 minutes.

The parameter `fgout.output_format` can be set to `'ascii'`, `'binary32'`,
or `'binary' == 'binary64'`; the same options as supported for the
standard output in geoclaw as of v5.9.0.  
Usually`'binary32'` is best, which truncates the float64 (kind=8)
computated values in the fortran code to float32 (kind=4) before dumping the
raw binary.  This is almost always sufficient precision for plotting or
post-processing needs, and results in smaller files than either of the other
options.  This may be particularly important if hundreds of fgout frames 
are saved for making an animation or doing particle tracking.

**New in v5.11.0:** `fgout.output_style == 1` corresponds to specifying
`tstart`, `tend`, and `nout` as previously.  But now it is possible
to instead set fgout.output_style == 2`, in which case a list of output
times can be specified that need not be equally spaced, e.g. ::

    fgout.output_style = 2  # new in v5.11.0
    fgout.output_times = [0.] + list(linspace(1,2,13)*3600)
    
to output a frame at time 0 and then every 5 minutes from 1 hour to 2 hours.

You can also now specify which components of `q` to save for each frame,
see below and :ref:`fgout_q_out_vars`.

.. _fgout_format:

Format of fgout output
-----------------------

After GeoClaw has run, the output directory should contain 
files of this form for each fgout grid:

 - `fgout0001.t0000`  # containing info about this output time
 - `fgout0001.q0000`  # header (and also data if `output_format=='ascii'`)
 - `fgout0001.b0000`  # data in binary format (only if `output_format` is a binary type`)

These would be for fgout grid number `fgno = 1` at the first output time.

These files have exactly the same format as the output files produced at
each output time for standard GeoClaw output (and more generally for any
Clawpack output), as described at :ref:`output_styles`.  The style allows
specifying AMR output in which there are many grids at each output time,
possibly at various refinement levels. 
In the case of fgout grids there will always be only a single grid at each
output time, with `AMR_level` set to 0 in the header files to indicate
that these grids are not part of the general AMR hierarchy.

.. _fgout_setplot:

Using `setplot.py` to produce plots
-----------------------------------

Since the files have the same format as the usual `fort.t`, `fort.q`, and 
`fort.b` files for Clawpack output, it is possible to use a `setplot.py`
file to set up plotting this sequence of fgout frames in exactly the same
manner as for standard output.  The only difference is that it is necessary
to specify that the file names start with `fgout...` rather than `fort.`.
This can be done in `setplot.py` via::

    plotdata.file_prefix = 'fgout0001'  # for fgout grid fgno==1
    plotdata.format = 'binary32'    # set to match fgout.output_format

An example is provided in 
`$CLAW/geoclaw/examples/tsunami/chile2010_fgmax-fgout`.


.. _fgout_plotting:

Reading and plotting fgout arrays directly
------------------------------------------

Alternatively, since every output frame consists of only a single uniform
grid of data, it is much easier to manipulate or plot this data directly than
for general AMR data.  The `fgout_tools.py` module described at
:ref:`fgout_tools_module` provides tools for reading frames and producing
arrays that can then be worked with directly. It also contains tools for
interpolating within these grids in both space and time.

For example, here's how to read a frame 5 of an fgout grid set up as above::

    fgno = 1
    outdir = '_output'
    fgout_grid = fgout_tools.FGoutGrid(fgno, outdir)
    fgout_grid.read_fgout_grids_data() # required as of v5.11.0

    fgframe = 5
    fgout = fgout_grid.read_frame(fgframe)
    
The call to `read_fgout_grids_data()` reads `_output/fgout_grids.data`
and sets the `output_format` along with other fgout grid parameters set there.
It also sets `fgout.X`, `fgout.Y` as 2D arrays that are the same for
all fgout frames.

**Incompatibility with previous versions:**  If you have fgout output created
with a version of Clawpack prior to v5.11.0 and you wish to process it using
a newer version, calling ::

    fgout_grid.read_fgout_grids_data()
    
should throw an error because the contents and ordering of information in
`fgout_grids.data` has changed.  To read this data in the old style,
instead use::

    fgout_grid.read_fgout_grids_data_pre511()
    
The format of fgout frames has *not* changed, so once the basic grid information
has been set, loading each frame should still work fine.

**Reading each frame:**
The call to `read_frame()` above loads `fgout.q` for a frame number `fgframe`.
This defines the `q` array, with `q[0:mq,:,:]` 
corresponding to the requested `q_out_vars`.

**New in v5.11.0:** Previously `mq=4` and the `q` array always contained
`h, hu, hv, eta`, where `eta = h+B` and `B` is the topography.
This is still the default is `q_out_vars` is not specified in setting up the
fgout grid, but fewer components of `q` can now be output, along with additional
variables (see :ref:`fgout_q_out_vars`).

For convenience, additional attributes are defined using lazy
evaluation only if requested by the user, e.g.,
`h, hu, hv, eta, B, u, v, s, hss`, where `s` is the speed and 
`hss` is the momentum flux, provided enough components of q have been saved
to compute these.

The values in `fgout.X` and `fgout.Y` are the cell centers of the fgout
grid, and if you want to plot the `q` values on this grid you should use
`clawpack.visclaw.plottools.pcolorcells`, as described at
:ref:`pcolorcells`.  For example, here's a minimalist example of plotting
the water surface eta on top of topography for a single frame of fgout data
as read above::

    from clawpack.visclaw import plottools, geoplot
    from numpy import ma

    plottools.pcolorcells(fgout.X,fgout.Y,fgout.B, cmap=geoplot.land_colors)
    eta = ma.masked_where(fgout.h<0.001, fgout.eta)
    eta_plot = plottools.pcolorcells(fgout.X,fgout.Y,eta, cmap=geoplot.tsunami_colormap)

For more detailed examples of plotting, including making animations,
see `$CLAW/geoclaw/examples/tsunami/chile2010_fgmax-fgout`.


.. _fgout_q_out_vars:

Specifying `q_out_vars`
-----------------------

**New in v5.11.0:**

Previously, each fgout frame contained columns for `h, hu, hv, eta` at each
fgout time, where `eta = h + B` based on the current topography `B` at the
fgout point.

Starting in v5.11.0 the user can specify `q_out_vars` as an array containing
the indices of the Fortran `q` array that should be output, and/or additional
integers that specify `eta` or `B`.  The previous default corresponds to
setting::

    fgout.q_out_vars = [1,2,3,4]

since in the standard GeoClaw Fortran code has 3 variables in `q` (h, hu, hv)
and index 4 indicates that `eta = h+B` should also be written out for each
frame.

The integer 5 can be used to indicate that `B` should be written out.
For example, to only write out `h` and `B`, the user would set::

    fgout.q_out_vars = [1,5]

Note that if any two of `h,eta,B` are saved then the third can be computed
since `eta = h+B`.  The lazy evaluation routines will compute any of these
from the others if that is possible (or raise an exception if not).

Note that if know that the underlying AMR grids will never change in the fgout
region then it would be possible to do a short run with::

    fgout.q_out_vars = [5]

to capture the `B` values and then the full run with::

    fgout.q_out_vars = [1]

to capture only `h` for each frame and still be able to calculate `eta` for
each frame if needed for plotting, reducing the file size (possibly useful
if hundreds of frames on a fine resolution will be saved over some
region where the AMR resolution is fixed).

**Additional variables for Boussinesq solvers:**

If the dispersive Boussinesq equations are solved (as introduced in v5.10.0,
see :ref:`bouss2d`), then the Fortran `q` array has two additional components
`q[4] = huc` and `q[5] = hvc`.  These are used to store corrections to the 
momenta `hu` and `hv` at each time step, which are computed by solving an
elliptic equation with an implicit solver.  It is convenient to store these
in `q` computationally, but the user rarely wants to see these values, and
so the `q_out_vars` can be used to suppress plotting these components and
only save `h, hu, hv, eta` as in the standard GeoClaw case by setting::

    fgout.q_out_vars = [1,2,3,6]
    
where now 6 represents `eta` (and 7 would indicate that `B` should be saved).

**qmap dictionary:**

To identify which component of the `q` array read in corresponds to what
variable name, a dictionary `fgout_grid.qmap` is used, with the standard
GeoClaw default being::

    {'h': 1, 'hu': 2, 'hv': 3, 'eta': 4, 'B': 5}
    
This dictionary can be specified when instantiating a new `FGoutGrid` object,
e.g.::

    fgout_grid = fgout_tools.FGoutGrid(fgno=1, outdir='_output', qmap='geoclaw')

to use the default GeoClaw dictionary. This is also the default if `qmap`
is not specified.  Alternatively you can instantiate this with
`qmap='geoclaw-bouss'`, which would be equivalent to instantiating with::

    qmap = {'h':1, 'hu':2, 'hv':3, 'huc':4, 'hvc':5, 'eta':6, 'B':7}
    
    
.. _fgout_registration:

fgout grid registration
-----------------------

Note above that fgout points are specified by setting e.g. `fgout.x1,
fgout.x2` and `fgout.nx` in `setrun.py`.  For consistency with the way the
finite volume computational grid is specified in `setrun.py`
(and written to the output files),
the values `x1, x2` are viewed as cell edges and `nx` is the desired number
of cells (in the `x` direction).  The actual fgout points will be at the
cell centers.  So the cell width (= distance between points)
is `dx = (x2-x1)/nx`, and the first fgout point (cell center)
will have `x` coordinate `x1 + dx/2`.

Solution values at these points are interpolated from the finite volume 
GeoClaw solution as described in the next section. 


.. _fgout_interp:

Choice of interpolation procedure
---------------------------------

The fgout grid need not be aligned with any computational grid, and in general
it may overlap several grids at different AMR resolutions. At each fgout time
requested, the solution is interpolated from the finest available AMR grid
covering each fgout point, at both the last time step before the fgout time
and the first time step after the fgout time. 

The default spatial interpolation method used to assign values to fgout points
at each time step is to assume the computational solution is constant in each
finite volume cell and simply evaluate this value in the finest AMR level
grid cell that includes
the fgout point.  This is controlled by the parameter `method = 0` in
subroutine `fgout_interp` in `$CLAW/geoclaw/src/2d/shallow/fgout_module.f90`.
This is generally recommended rather than setting `method = 1`, which gives
linear interpolation between finite volume cell centers, because interpolating
`h`, `B`, and `eta` separately near the shore can lead to unphysically large
values of `h` and/or `eta` (see :ref:`nearshore_interp`).

Similarly, the temporal intepolation between the two neighboring time steps is
done by simply using the value at the later time step, as controlled by the
parameter `method = 0` in the 
subroutine `fgout_write` in `$CLAW/geoclaw/src/2d/shallow/fgout_module.f90`.
This is generally recommended rather than setting `method = 1`, which gives
linear interpolation between the times, because interpolating
`h`, `B`, and `eta` separately near the shore can lead to unphysically large
values of `h` and/or `eta` (see :ref:`nearshore_interp`).

If you want to change one of these methods, you can make your own version of
`fgout_module.f90` and point to this in the `Makefile` under `MODULES=`
(see :ref:`makefiles_replace`).

.. _fgout_examples:

fgout examples
---------------

For some examples, see
`$CLAW/geoclaw/examples/tsunami/chile2010_fgmax-fgout`.
Sample results appear in the `GeoClaw Gallery
<https://www.clawpack.org/gallery/gallery/gallery_geoclaw.html>`__;
see the 
`README <https://www.clawpack.org/gallery/_static/geoclaw/examples/tsunami/chile2010_fgmax-fgout/README.html>`__
for a description and links to the plots and a script for making an animation.
