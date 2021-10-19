:orphan:

.. _changes_to_master:

===============================
Changes to master since v5.8.0
===============================


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.8.0) on February 4, 2021.

These changes should appear in the next release.  If you need them now,
see :ref:`developers` for instructions on cloning and installing from the
master branch. 

To see documentation that has already been developed to accompany any new
features listed below, click on the "dev" branch of the documentation, in
the menu on the left hand side of this page.

Changes that are not backward compatible
----------------------------------------


General changes
---------------


Changes to classic
------------------

No changes.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.8.0...master>`_

Changes to clawutil
-------------------

No changes.


See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.8.0...master>`_

Changes to visclaw
------------------

No major changes.

See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.8.0...master>`_

Changes to riemann
------------------

- Fix `rp1_shallow_hlle.f90` to work better near dry states.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.8.0...master>`_

Changes to amrclaw
------------------

No changes.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.8.0...master>`_

Changes to geoclaw
------------------

- Some improvements to storm tracks
- Reading (some) geotiff files now supported in `topotools`
- Added `kmltools.topo2kmz` to make Google Earth overlays showing topography
- Some other bug fixes.
  
See `geoclaw diffs 
<https://github.com/clawpack/geoclaw/compare/v5.8.0...master>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.8.0...master>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.8.0...master>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.8.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.8.0...master>`_

