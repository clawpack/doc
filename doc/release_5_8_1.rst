:orphan:

.. _release_5_8_1:

===============================
v5.8.1 release notes
===============================

Clawpack 5.8.1 was released on October 19, 2021. See :ref:`installing`.

**The installation instructions have been reorganized (once again)
in an attempt to make the different options clearer.**

Permanent DOI: http://doi.org/10.5281/zenodo.??


Changes relative to Clawpack 5.8.0 (February 4, 2021) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------


General changes
---------------


Changes to classic
------------------

No changes.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.8.0...v5.8.1>`_

Changes to clawutil
-------------------

No changes.


See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.8.0...v5.8.1>`_

Changes to visclaw
------------------

No major changes.

See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.8.0...v5.8.1>`_

Changes to riemann
------------------

- Fix `rp1_shallow_hlle.f90` to work better near dry states.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.8.0...v5.8.1>`_

Changes to amrclaw
------------------

No changes.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.8.0...v5.8.1>`_

Changes to geoclaw
------------------

- Some improvements to storm tracks
- Reading (some) geotiff files now supported in `topotools`
- Added `kmltools.topo2kmz` to make Google Earth overlays showing topography
- Some other bug fixes.
  
See `geoclaw diffs 
<https://github.com/clawpack/geoclaw/compare/v5.8.0...v5.8.1>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.8.0...v5.8.1>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.8.0...v5.8.1>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.8.x...dev>`_
  shows changes in the `dev` branch not yet in the posted version of the
  documentation.

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.8.0...v5.8.1>`_

