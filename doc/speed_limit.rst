
.. _speed_limit:

*****************************************************************
Setting a Speed Limit to Avoid Instabilities
*****************************************************************

**To appear in v5.11.1.**  Not yet in the master branch...  

See https://github.com/clawpack/geoclaw/pull/637
for some more information on this modification.

A new paramter `rundata.geo_data.speed_limit` can now be set in `setrun.py`
to impose an upper limit on the water speed `s = sqrt(u**2 + v**2)`.  By
default this is set to 50 m/s (about 112 mph), which we believe is larger
than any physical water speed for most practical problems, and so using the
default value should not significantly affect agreement with
past simulation results.

In practice you may want to explicitly set a smaller value, e.g. ::

    rundata.geo_data.speed_limit = 20.

for better performance and less danger of instability in certain cases.

.. _speed_limit_dt:

Avoiding `too many dt reductions`
---------------------------------

The reason for introducing the `speed_limit` is to improve the stability of
GeoClaw in situations where flows are inundating relatively steep
topography.  Past versions of GeoClaw have sometimes died with a cryptic
error message such as ::

    **** Too many dt reductions ****
    **** Stopping calculation   ****
    **** ntogo =   172

This indicates that GeoClaw has repeatedly attempted to reduce the time step dt
to get the Courant number below the desired value `clf_desired`,
but has failed to do so with a physically reasonable set of reductions.  
(`ntogo` is the number of time steps still remaining to sync up this level
with the next coarser AMR level.)

The developers have determined that this usually happens in grid
cells that are on steep topography (e.g. on a cliff face)
in a case when the cell is at the edge of the inundation zone
with a fluid depth that is much smaller than the jump in topography between
this cell and an adjacent lower cell.  The Riemann solver for the shallow
water equations is not designed to handle the resulting flow of this small
amount of water down the vertical interface between these cells, since
depth-averaged equations are not appropriate to model this waterfall.  As a
result, the values of `h` and the momenta `hu, hv` that come out of the
approximate Riemann solution may be such that `h` is very small while `hu,
hv` are so large that `u = hu/h` and/or `v = hv/h` turn out to be much too
large to be physically meaningful (values in excess of 10000 m/s have been
observed in a single cell in simulations that behave well everywhere
else).  Since the Courant number is based on the wave speed `|s| +
sqrt(g*h)`, huge values of `s` require tiny values of `dt` to respect
the CFL condition.

The new `speed_limit` fixes things up in these isolated bad cells and allows
the calculation to proceed.

.. _speed_limit_imposed:

How is the speed limit imposed?
-------------------------------

The new `speed_limit` is used in the GeoClaw `b4step2.f90` subroutine to check
the speed `s` in every cell before taking the next step on the shallow water
equations.  In a cell where `s > speed_limit`, the velocities `u,v` are
scaled down so the direction of the velocity vector is preserved,
but with reduced speed `sqrt(u**2 + v**2) = speed_limit`.  This is also
done in `getmaxspeed.f90`, used for setting time steps.

The `speed_limit` is also imposed in the `src2.f90` subroutine, but only
in the case where the user sets

    rundata.geo_data.friction_forcing = False

so that no bottom friction is applied in this routine.  For
frictionless calculations, we have found that unphysical speeds can
arise in many cells in the inundation zone. These are typically cells
where the depth `h` is very small but `hu,hv` are large, and even a bit of
bottom friction typically damps the speed to something reasonable, if 
`friction_forcing` is being used.  This has
not been extensively tested, but in some experiments a Manning coefficient
of at least 0.05 avoids problems.  If you need to use a smaller value, you may
need to adjust `src2.f90` to also apply the `speed_limit` more generally.
(The Manning coefficient value 0.025 is often used for tsunami modeling.)

