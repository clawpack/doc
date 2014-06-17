
.. _release_5_2_0:

==========================
Release 5.2.0 (TO APPEAR)
==========================


Clawpack 5.2.0 was released on ??? (To appear).  See :ref:`installing`.


Changes to classic
------------------

* Change max number of values printed on each line of `fort.q` files to 50.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.1.0...master>`_

Changes to clawutil
-------------------

* Add `nohup` and `nice` options to `runclaw.py`

* Some minor corrections.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.1.0...master>`_

Changes to visclaw
------------------

* Several minor improvements.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.1.0...master>`_

Changes to riemann
------------------

* Some minor corrections.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.1.0...master>`_

Changes to amrclaw
------------------

* Refactoring of code handling `aux` arrays when regridding.  
  Now allows `setaux` to check `aux(1,i,j)` to determine if the
  values `aux(:,i,j)` need to be set or if this cell has already been set by
  copying from `aux` arrays at the same level that existed before
  regridding.  It should always be ok to just set them, so this should be
  backward compatible.  But this allows avoiding recalculating `aux` values
  unnecessarily in cases where this computation is very expensive.  In
  particular, this was done so that `geoclaw` does not need to recompute
  cell averages of topography (see geoclaw changes below for more details).

* Fixed (?) sphere boundary conditions for clamshell grids.

* Change max number of values printed on each line of `fort.q` files to 50.

* Several other minor fixes.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.1.0...master>`_

Changes to geoclaw
------------------

* Refactoring of code handling `aux` arrays when regridding.  
  Now allows `setaux` to check `aux(1,i,j)` to determine if the
  values `aux(:,i,j)` need to be set or if this cell has already been set by
  copying from `aux` arrays at the same level that existed before
  regridding.  This is used in geoclaw to avoid recomputing cell averages of
  topography, which requires integrating a piecewise bilinear function
  formed from all the topography grids that overlap the grid cell.  This
  can be expensive particularly when a grid cell is covered by a finer
  topography grid.

* One change to the `Makefile` for a GeoClaw run is required because
  of refactoring of this code.  You must:


    * Replace the line ::

          $(GEOLIB)/fgmax_interpolate.f90 \

      by ::

          $(GEOLIB)/fgmax_interpolate0.f90 \

      or ::

          $(GEOLIB)/fgmax_interpolate1.f90 \

      The latter choice will preserve the original behavior, with 
      bilinear interpolation used to interpolate from the finite volume
      grid centers to the fixed grid.  However, the choice 
      `fgmax_interpolate0.f90` is now recommended.  This simply uses the
      value in the finite volume grid cell that contains the fixed grid
      point (0 order extrapolation) and avoids problems sometimes seen when
      doing linear interpolation near the margins of the flow.

  As always, you should do `make new` in your application directory
  after updating the version.

* Change to the way fixed grids are specified.... Describe!

* Major refactoring of some of the `topotools` and `dtopotools`....Describe!

* Change max number of values printed on each line of `fort.q` files to 50.

* Multilayer shallow water equations functionality and test problem added.

* Several other corrections and minor improvements.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.1.0...master>`_

Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.1.0...master>`_

