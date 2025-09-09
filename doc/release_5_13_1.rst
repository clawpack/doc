:orphan:

.. _release_5_13_1:

===============================
v5.13.1 release notes
===============================

Clawpack 5.13.1 was released on Sept. TBD, 2025. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.TBD


Changes relative to Clawpack 5.13.0 (August 23, 2025) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

- None

General changes
---------------

A couple bugs prevented most GeoClaw code from running and these have
now been fixed.

Unit testing and continuous integration on Github is now working for
`amrclaw`, still a work in progress for other repositories.
We are working on modifying tests to use `pytest` (rather than `nose`) and
Github CI (rather than travis).


Changes to classic
------------------

- None

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.13.0...v5.13.1>`_

Changes to clawutil
-------------------

- minor bug fixes

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.13.0...v5.13.1>`_

Changes to visclaw
------------------

- None.

See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.13.0...v5.13.1>`_

Changes to riemann
------------------

- None

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.13.0...v5.13.1>`_

Changes to amrclaw
------------------

- Several changes needed to get pytest working.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.13.0...v5.13.1>`_

Changes to geoclaw
------------------

- The 1D code was failing because the new `override_topo_order` parameter
  introduced in v5.13.0 in 2D was also written to the `topo.data` files in
  1D, but was not being read in by the Fortran.  This was fixed in
  [#669](https://github.com/clawpack/geoclaw/pull/669).
  (Only one topofile is currently allowed in 1D, so the value of this
  flag is moot.)

- A bug introduced in the 2D code resulted in a call to `b4step2` having
  the wrong number of parameters. This was fixed in
  [#670](https://github.com/clawpack/geoclaw/pull/670).

- Several other more minor bug fixes and enhancements.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.13.0...v5.13.1>`_


Changes to PyClaw
------------------

- Better command line interface for gauge comparisons.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.13.0...v5.13.1>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.13.0...v5.13.1>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.12.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.13.0...v5.13.1>`_
