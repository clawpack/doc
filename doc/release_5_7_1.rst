:orphan:

.. _release_5_7_1:

===============================
v5.7.1 release notes
===============================

Clawpack 5.7.1 was released on September 11, 2020. See :ref:`installing`.

Permanent DOI:
`[DOI 10.5281/zenodo.4025432] <https://doi.org/10.5281/zenodo.4025432>`__.

Changes relative to Clawpack 5.7.0 (April 23, 2020) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

- None

General changes
---------------

- None

Changes to classic
------------------

- None

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.7.0...v5.7.1>`_

Changes to clawutil
-------------------

- New `b4run.py` capability added -- script run before `runclaw` from `make
  .output` that can be used to copy files to `_output`, for example.

- `claw_git_status.py` improved.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.7.0...v5.7.1>`_

Changes to visclaw
------------------

- Fix some things that weren't backward compatible with older versions of 
  `matplotlib`

- Improve animation plot quality, and other changes to `animation_tools.py`

- New Matlab tools

- Other misc. changes
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.7.0...v5.7.1>`_

Changes to riemann
------------------

- None

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.7.0...v5.7.1>`_

Changes to amrclaw
------------------

- fix `verbosity_regrid`
- fix use of `kmltools` in `region_tools`

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.7.0...v5.7.1>`_

Changes to geoclaw
------------------

- Some fixes to fgmax examples
- Improve some kml and netcdf tools
- Additional storm models
- Other misc. fixes and improvements

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.7.0...v5.7.1>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/v5.7.1/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.7.0...v5.7.1>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.6.0...v5.7.1>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.6.1...v5.7.x>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.7.0...v5.7.1>`_

