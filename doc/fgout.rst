
.. _fgout:

=====================
Fixed grid output
=====================

**To appear in v5.9.0:** 

See also:

 - :ref:`fgout_tools_module`
 - :ref:`setrun_fgout` - For adding fgout data to `setrun.py`

GeoClaw has the capability to output the results at specified output times
on a specified "fixed grid" by interpolating from the AMR grids active at each 
output time.

This complements the normal output frame capabilities of Clawpack,
and has several advantages for some applications, particularly when
making animations or when using the GeoClaw solution as input to
another process, such as particle tracking:

    1. The solution is output on a fixed uniform grid at each fgout
    time, independent of the AMR structure.  This is useful in order
    to produce a set of frames for an animation that are all the same
    resolution with the same size array.

    2. It is possible to produce fgout outputs at times that do not
    coincide with the time steps of the computation, whereas standard
    frame output can only occur at the end of a time step on coarsest
    level.  Thus it does not require reducing the time step to hit
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

An improved version of of the capability to output on a fixed grid at more
frequent times than the standard AMR output is being introduced in v5.9.0,
and these are now called `fgout grids` to complement the `fgmax grids`.

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
to each fgout grid using the `fgno` attribute, described below, or
if you do not then they will be numbered sequentially (1,2, etc.)
based on the order they are specified in the `setrun.py` file.


A simple example
-----------------

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
    fgout.tstart = 0.
    fgout.tend = 6.*3600
    fgout.nout = 37
    fgout_grids.append(fgout) 

This specifies output on a 200 by 250 grid of equally spaced points on the
rectangle `[-115, -70] x [-55, -10]`.  (Note that these values are cell
edges, the actual fgout points will be at cell centers, 
displaced from these edges.  See :ref:`fgout_registration` below.)

The output times are equally spaced
from `tstart = 0` to `tend = 6*3600` (6 hours).  
There will be 37 total outputs, so one every 10 minutes.  

The parameter `fgout.output_format` can be set to `'ascii'`, `'binary32'`,
or `'binary64'`, the same options as supported for the standard output in
geoclaw as of v5.9.0.  
Usually`'binary32'` is best, which truncates the float64 (kind=8)
computated values in the fortran code to float32 (kind=4) before dumping the
raw binary.  This is almost always sufficient precision for plotting or
post-processing needs, and results in smaller files than either of the other
options.  This may be particularly important if hundreds of fgout frames 
are saved for making an animation or doing particle tracking.

.. _fgout_format:

Format of fgout output
-----------------------

After GeoClaw has run, the output directory should contain 
files of this form for each fgout grid:

 - `fgout0001.t0000`  # containing info about this output time
 - `fgout0001.q0000`  # header (and also data if `output_format=='ascii'`)
 - `fgout0001.b0000`  # data in binary format (only if 
   `output_format=='binary32'` or `'binary64'`)

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

.. _fgout_plotting:

Reading and plotting fgout arrays directly
------------------------------------------

Alternatively, since every output frame consists of only a single uniform
grid of data, it is much easier to manipulate or plot this data directly than
for general AMR data.  The `fgout_tools.py` module described at
:ref:`fgout_tools_module` provides tools for reading frames and producing
arrays that can then be worked with directly.

For example, here's how to read a frame 5 of an fgout grid set up as above::


    fgno = 1
    outdir = '_output'
    output_format = 'binary32'  # format of fgout grid output
    fgout_grid = fgout_tools.FGoutGrid(fgno, outdir, output_format)

    fgframe = 5
    fgout = fgout_grid.read_frame(fgframe)

Then `fgout.X` and `fgout.Y` are 2-dimensional arrays defining the grid
and `fgout.q` defines the standard GeoClaw `q` array, with `q[0:4,:,:]` 
corresponding to `h, hu, hv, eta`, where `eta = h+B` and `B` is the topography.
For convenience, additional attributes are defined using lazy
evaluation only if requested by the user, including 
`h, hu, hv, eta, u, v, s, hss`, where `s` is the speed and 
`hss` is the momentum flux.

For some examples, see `$CLAW/geoclaw/examples/tsunami/chile2010_fgmax-fgout`.

.. _fgout_registration:

fgout grid registration
-----------------------

Note above that fgout points are specified by setting e.g. `fgout.x1,
fgout.x2` and `fgout.nx` in `setrun.py`.  For consistency with the way the
finite volume computational grid is set (and written to the output files),
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
finite volume cell and simply evaluate this value in the cell that includes
the fgout point.  This is controlled by the parameter `method = 0` in
subroutine `fgout_interp` in `$CLAW/geoclaw/src/2d/shallow/fgout_module.f90`.
This is generally recommended rather than setting `method = 1`, which gives
linear interpolation between finite volume cell centers, because interpolating
`h`, `B`, and `eta` separately near the shore can lead to unphysically large
values of `h` and/or `eta`.

Similarly, the temporal intepolation between the two neighboring time steps is
done by simply using the value at the later time step, as controlled by the
parameter `method = 0` in the 
subroutine `fgout_write` in `$CLAW/geoclaw/src/2d/shallow/fgout_module.f90`.
This is generally recommended rather than setting `method = 1`, which gives
linear interpolation between the times, because interpolating
`h`, `B`, and `eta` separately near the shore can lead to unphysically large
values of `h` and/or `eta`.

If you want to change one of these methods, you can make your own version of
`fgout_module.f90` and point to this in the `Makefile` under `MODULES=`
(see :ref:`makefiles_replace`).
