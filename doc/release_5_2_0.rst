:orphan:

.. _release_5_2_0:

==========================
v5.2.0 release notes
==========================

Clawpack 5.2.0 was released on July 18, 2014.  See :ref:`installing`.

Changes relative to Clawpack 5.1.0 (March 2, 2014) are shown below.

Changes to classic
------------------

* Change max number of values printed on each line of `fort.q` files to 50.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.1.0...v5.2.0>`_

Changes to clawutil
-------------------

* Add `nohup` and `nice` options to `runclaw.py`

* Some minor corrections.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.1.0...v5.2.0>`_

Changes to visclaw
------------------

* Several minor improvements.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.1.0...v5.2.0>`_

Changes to riemann
------------------

* Some minor corrections.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.1.0...v5.2.0>`_

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
<https://github.com/clawpack/amrclaw/compare/v5.1.0...v5.2.0>`_

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

* Several changes have been made to the `fgmax` routines that are used to
  keep a running maximum of values over the entire calculation.  
  See :ref:`fgmax` for documentation on the latest version.


* Major refactoring of the module
  `$CLAW/geoclaw/src/python/geoclaw/topotools.py`.  
  The file `$CLAW/geoclaw/tests/test_topotools.py` contains some tests of these
  tools.  Looking at these test routines will give some ideas on how to use them.
  More documentation is needed.

* Change max number of values printed on each line of `fort.q` files to 50.

* Multilayer shallow water equations functionality and test problem added.

* Several other corrections and minor improvements.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.1.0...v5.2.0>`_

Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/v5.2.0/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.1.0...v5.2.0>`_

