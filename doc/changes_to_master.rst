
.. _changes_to_master:

===============================
Changes to master since v5.1.0
===============================


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.1.0). 

These changes should appear in the next release.  If you need them now,
see :ref:`developers` for instructions on cloning and installing from the
master branch. 


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

