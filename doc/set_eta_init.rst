
.. _set_eta_init:

Set Eta Init – spatially varying initial surface elevation
==========================================================

Prior to Version 5.7.0,
GeoClaw had a single scalar parameter `sea_level` and the water
surface is initialized to this value in every cell where the GeoClaw
cell-averaged topography value `B` is smaller, i.e., the water depth
in each cell is initialized to:

`h[i,j] = max(0, sea_level - B[i,j])`.

In some cases it is desirable to initialize the depth so that the
surface is spatially varying.

Starting in v5.7.0, the library routine
`$CLAW/geoclaw/src/2d/shallow/set_eta_init.f90` can be used to set
the desired initial water surface `eta = B + h` in a spacially varying
manner.  In order to invoke this routine, in `setrun.py` you should set::

    rundata.qinit_data.variable_eta_init = True

Default behavior, adjusting sea level by seismic deformation
------------------------------------------------------------

The default library routine 
`$CLAW/geoclaw/src/2d/shallow/set_eta_init.f90`
is set up for the use case in which a region subsides or is uplifted by a
local earthquake.  
In tsunami modeling of a nearfield event, the seafloor
deformation due to the earthquake often extends onto shore in the region
being modeled. If the coastal region subsides, for example, then the
land drops near the shore and the water adjacent drops as well. If a
grid patch was initialized before the deformation specified in the dtopo
file by the formula above, then the depth `h[i,j]` does not decrease
during the subsidence, which is the correct behavior. 

However, in some
cases the tsunami does not arrive at the shore quickly and so it is
desirable to use coarser grids in early stages of the computation,
introducing highly refined grids only after some specified time. When
new levels of refinement are first introduced into a simulation then the
formula given above is used to initialize cells near the coast. But if the 
coast subsided (or is uplifted), the the formula above should be replaced by:

`h[i,j] = max(0, sea_level + dz[i,j] - B[i,j])`

where `dz[i,j]` is obtained by interpolating the co-seismic
deformation specified in the dtopo file to the cell center. Failure to
do this can sometimes result in large areas being flooded by the
initialization that should not be flooded by the tsunami.


The default version of `$CLAW/geoclaw/src/2d/shallow/set_eta_init.f90`
loops over all (possibly time-dependent)
dtopo files and interpolates from these
files to the points on the grid patch, at the specified time, to adjust the
initial constant `sea_level` value at each point on the patch.

Note that this `set_eta_init` function is only called when a grid cell is
first initialized at a given AMR level. It is called from `qinit.f90` to
initialize any patches that exist at the initial time (which may be before
the earthquake starts, in which case no adjustment to `sea_level` would be
made).  

It is also called if a region is refined to a higher level than
previously, but the resulting value is used only in cells where the
the water surface level `h+B` cannot be interpolated from coarser levels, due
to the fact that one or more neighboring cells was dry (in which case
`h+B=B` may be huge if the land rises steeply, and using this value in an
interpolation of the sea surface would lead to artificially high surface
elevation, and hence incorrect depth `h` when this is computed as `eta - B`.
So such cells near the coast must be filled with water up to the value
specified by `set_eta_init`.  In previous versions they were always filled
to the level specified by `sea_level`, but this was incorrect 
in regions where the water level subsided (or was uplifted) along with the
land.

As noted above,
this is particularly important in coastal regions where there is seismic
deformation but it takes some time for the tsunami to arrive and so the fine
grids needed to resolve the region are not introduced until some time after the
seismic deformation.

Other use cases
---------------

For other uses one can copy the library routine
`$CLAW/geoclaw/src/2d/shallow/set_eta_init.f90`
to the application directory and modify it as desired (and change the
`Makefile` to point to the modified version).

For example, there may be **onshore lakes** whose initial surface elevation
should be different than `sea_level`.  This could be added to the existing
routine, so that siesmic displacement of both the offshore water and onshore
lakes is also handled, or the dtopo adjustments can be removed if not needed.

When modeling **dam break problems,** there may one or more lakes
of interest at different initial elevations.
As an example, to develop a custom routine in the case
where a lake behind a dam is desired to be set to one elevation while
everywhere else there should be no water, this routine could check the
`(x,y)` location of each cell and set `eta_init` either to the lake
elevation, if in a specified region,
or to a very negative value lower than any topography (to force `h = 0`),
when outside the region covered by the lake.


