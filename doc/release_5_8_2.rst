:orphan:

.. _release_5_8_2:

===============================
v5.8.2 release notes
===============================

Clawpack 5.8.2 was released on December 14, 2021. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.XX


Changes relative to Clawpack 5.8.1 (October 19, 2021) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

None.

General changes
---------------

None.



Changes to classic
------------------

None.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.8.1...v5.8.2>`_

Changes to clawutil
-------------------

Minor addition of a print statement.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.8.1...v5.8.2>`_

Changes to visclaw
------------------

None.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.8.1...v5.8.2>`_

Changes to riemann
------------------

None.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.8.1...v5.8.2>`_

Changes to amrclaw
------------------

- Bug fix that avoids some segmentation faults when running amrclaw or geoclaw
  jobs with many grids.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.8.1...v5.8.2>`_

Changes to geoclaw
------------------

None, although the bug fix in amrclaw is sometimes needed.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.6.1...master>`_


Changes to PyClaw
------------------

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.8.1...v5.8.2>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.8.1...v5.8.2>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.8.x...dev>`_
  shows changes in the `dev` branch not yet in the posted version of the
  documentation.

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.8.1...v5.8.2>`_

