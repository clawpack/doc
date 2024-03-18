.. _geoclaw1d:

*********************************************
GeoClaw in One Space Dimension
*********************************************

As of Version 5.10.0, the geoclaw repository contains some code for solving
problems in one space dimension.  This can be used for solving plane wave
problems on planar topography (including onshore inundation), as well as
radially symmetric problems on the plane 
or axisymmetric problems on the sphere (see :ref:`geoclaw1d_coord`).

Some general notes:

- The standard 2d version of GeoClaw can be used to solve 1d problem by
  simply specifying a domain that is only a few cells wide in the
  y-direction, and insuring that the topography, initial data, and any dtopo
  files varies only in x as well.  By setting the AMR refinement ratios to be
  1 in the y-direction, it is possible to still use adaptive mesh refinement
  in x.  For some 1d problems this may be the best approach.

- By contrast, the newly introduced 1d code does not support AMR at this
  time.  Instead, a fixed grid is used.  

  However, the grid spacing may be
  variable and some tools are provided to compute a mapped grid that has the
  property that the Courant number (based on the linearized
  shallow water wave speed `sqrt(g*h)`)is roughly constant, so that cells in
  deep water are larger than cells in shallow water (transitioning to a
  uniform grid in very shallow water and onshore).  For some problems a fine
  1d grid of this nature can be used to compute a very accurate solution and
  is sometimes preferable to using AMR.

- In addition to shallow water equations, the 1d code also supports two
  different forms of Boussinesq equations, which include dispersive terms
  and better model waves whose wavelength is short compared to the fluid
  depth.  For more information, see :ref:`bouss1d`.
  (Two-dimensional Boussinesq solvers have also recently been implemented,
  with AMR, and will appear in a future release; see :ref:`bouss2d`.)

- Topography data (topo files) and moving topography (dtopo files) can be
  specified much as in 2d GeoClaw; see :ref:`topo1d` below.

The 1d library routines are found in `$CLAW/geoclaw/src/1d_classic/shallow`,
with some additional routines needed for the Boussinesq solvers in 
`$CLAW/geoclaw/src/1d_classic/bouss`.  

Some examples illustrating usage can be found in
`$CLAW/geoclaw/examples/1d`, and some plots and animations can be viewed in
the `GeoClaw Gallery
<https://www.clawpack.org/gallery/gallery/gallery_geoclaw.html>`__

.. _geoclaw1d_coord:

Coordinate systems
-------------------

In `setrun.py`, the parameter `rundata.geo_data.coordinate_system`
can be used to specify the coordinate system to be used.

- `rundata.geo_data.coordinate_system == 1`: `x` is measured in meters. This
  is the most natural coordinate system for many 1d problems, e.g. modeling
  waves in a wave tank, or plane waves in the ocean (provided the topography
  only varies in the direction of propagation).

- `rundata.geo_data.coordinate_system == -1`: `x >= 0` is measured in meters
  and represents radial distance. 
  In this case, the solution is assumed to a 1d cross section of
  a rotationally symmetric 2d solution.  The 2d shallow water (or
  Boussinesq) equations can then be reduced to 1d equations that have a
  similar form to the plane wave equations, with the addition also of a
  geometric source term [BergerLeVeque2023]_.
  This source term is built in to the solution procedure in this case.

- `rundata.geo_data.coordinate_system == 2`: `x` is measured in degrees
  for a problem that is rotationally symmetric on the sphere about some axis
  of rotation, e.g. waves
  spreading out from a radially symmetric crater on topography that is also
  rotationally symmetric about the same axis. In this case `-90 <= x <=90`
  with the endpoints corresponding to the two points where the axis intersects
  the sphere, so it represents latitude with respect to this axis.  
  (If the axis passes through the poles then `x` is the ordinary
  latitude with `x = -90` at the south pole and `x = +90` at the north pole.)

  As in the case of radial symmetry, the spherical case requires some
  changes in the equations and the addition of a geometric source term.
  Near each pole the solution behaves much as in the radial symmetric case,
  but note that waves from a disturbance at one pole will initially
  decay as they spread out but after passing the equator they will start to
  refocus at the other pole.


.. geoclaw1d_grids:

Uniform and mapped grids
------------------------

In `setrun.py`, the parameter `rundata.grid_data.grid_type`
can be used to specify the computational grid to be used.

- `rundata.grid_data.grid_type == 0`: A uniform grid is used, with
  spacing determined by the domain length and the number of grid cells
  specified.

- `rundata.grid_data.grid_type == 1`: A mapped grid is used. 
  In this case a function `mapc2p.f90` must be provided to map 
  the computational grid specified in `setrun.py` to physical cells.
  See :ref:`mapc2p`.  In this case `0 <= x <= 1` is used in the examples,
  but any computational grid interval can be used as long as `mapc2p`
  maps equally spaced points on this interval to te desired physical grid.

- `rundata.grid_data.grid_type == 2`: A nonuniform grid is used with a
  user-specified set of grid cell edges.  In this case
  `rundata.grid_data.fname_celledges` should be set to a string
  giving the name of the file that contains the cell edges (one per line).
  Also, the computational grid should be in the domain `0 <= x <= 1`, i.e.::

    clawdata.lower[0] = 0.           # xlower
    clawdata.upper[0] = 1.           # xupper
    clawdata.num_cells[0] = mx       # number of grid cells

  In this case the number of celledges in the data file should be `mx+1`.
  A `mapc2p` function that maps the unit interval to the physical grid
  must then be specified in `setplot.py`, and can be generated using the
  function `clawpack.geoclaw.nonuniform_grid_tools.make_mapc2p()`.

  The module  `clawpack.geoclaw.nonuniform_grid_tools.py`
  also includes tools to create a nonuniform grid with the property that
  a specified uniform grid width is used onshore an in very shallow
  water, but are much larger in deeper water, with the physical grid widths
  chosen so that the CFL number is roughly uniform (based on the propagation
  speed `sqrt(g*h)`).
  Most of the examples in `$CLAW/geoclaw/examples/1d_classic/`
  illustrate this.

Note that when using `grid_type` 1 or 2, any gauges specified in `setrun.py`
must be specified in computational coordinates, not physical coordinates.
See, e.g. `$CLAW/geoclaw/examples/1d_classic/ocean_shelf_beach/setrun.py`
for an example.

.. geoclaw1d_topo:

Topograpy data
-------------------

Topography data is specified in a file that has two columns, with values
`x, B` specifying the topo value `B` at spatial locations `x`.
The topography is viewed as being piecewise linear connecting these points.
As in 2d GeoClaw, the finite volume cells used for the computation have a
single cell-averaged `B` value that is obtained by cell-averaging this
piecewise linear function.

Note that if a mapped grid is used and if the topography values are 
specified at the cell edges, then the cell-averaged finite volume values are
simply the average of the `B` values from each edge of the cell.  In this
case, the same file that is used to specify the topography can also be used
to specify the grid. (The second column is ignored when it is read in as a
grid specification.)

In `setrun.py`, the parameter `rundata.topo_data.topofiles`
is set to a list of topofiles, each of which is specified by a list
containing the `topo_type` and `topofile_path`, the path to the file, as
in 2d.  Currently only one topofile is supported, and
so this should have the form:

    rundata.topo_data.topofiles = [[topo_type, topofile_path]]

Currently only `topo_type == 1` is supported, which has the form described
above.


.. geoclaw1d_dtopo:

Moving topograpy (dtopo) data
-----------------------------

In `setrun.py`, the parameter `rundata.dtopo_data.dtopofiles`
is set to a list of dtopofiles, each of which is specified by a list
containing the `dtopo_type` and `dtopofile_path`, the path to the file, as
in 2d.  Currently only one dtopofile is supported, and
so this should have the form:

    rundata.dtopo_data.dtopofiles = [[dtopo_type, dtopofile_path]]

Currently only `dtopo_type == 1` is supported, and the dtopofile should have
a form similar to what was described for topofiles above,
except that each line
starts with a *t* value for the time, so each line contains t,x,dz

The `x,dz` values give the displacement `dz` at `x` at time `t`.  It is assumed
that the grid is uniform and that the file contains `mx*mt` lines if mt
different times are specified on a grid with mx points.  

One way to specify a dtopo file is to use the Okada model (see :ref:`okada`)
in a situation where the fault is dipping in the x-direction and the fault
geometry and slip are assumed
to be constant in the y-direction over a long enough distance that a 1d
slice in x is a reasonable model.
Tools are provided create such a dtopo file, see the example in
`$CLAW/geoclaw/examples/1d/okada_dtopo`.

