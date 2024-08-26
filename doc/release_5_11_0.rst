:orphan:

.. _release_5_11_0:

===============================
v5.11.0 release notes
===============================

Clawpack 5.11.0 was released on August 25, 2024. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.13376470


Changes relative to Clawpack 5.10.0 (March 29, 2024) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

- In GeoClaw, some new options have been added to the specification of
  fgout grids. The format and contents of the `fgout_grids.data` file created
  by `make data` has changed.  Old-style files can still be read
  (see below and :ref:`fgout`).
  
- In GeoClaw, the transverse Riemann solver used for the SWE step when solving
  Boussinesq equations was changed to the standard GeoClaw solver, which should
  cause no noticeable changes.


General changes
---------------

Unit testing and continuous integration on Github continue to be broken, but
we are working on modifying tests to use `pytests` (rather than `nose`) and
Github CI (rather than travis). 

Changes to classic
------------------

- Some changes to `tests`.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.10.0...v5.11.0>`_

Changes to clawutil
-------------------

- Fixes to `imagediff.py`

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.10.0...v5.11.0>`_

Changes to visclaw
------------------

- Fixes to `kml_maxlevels`.

- Add `celledges_linewidth` attribute for plotting grid cells.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.10.0...v5.11.0>`_

Changes to riemann
------------------

- update `rpn2_geoclaw` and `geoclaw_riemann_utils` to initialize wave
  components `4:5` to 0 for Boussinesq code.  Has no effect on SWE solver.

- Update to `rpt2_layered_shallow_water.f90` 

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.10.0...v5.11.0>`_

Changes to amrclaw
------------------

- Some changes to `tests`.

- Allow more than 5 digits in gauge numbers.

- Fix `euler_3d_radial` initial condition bug.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.10.0...v5.11.0>`_

Changes to geoclaw
------------------

- Some changes to `tests`.

- Some new options have been added to the specification of
  fgout grids. The format and contents of the `fgout_grids.data` file created
  by `make data` has changed.  Old-style files can still be read using::

    fgout_grid.read_fgout_grids_data_pre511()
    
  New options include specifying output times for fgout grids that are not
  uniformly spaced in time, and specifying which components of the `q` array
  and/or the `eta` and `B` variables to write out at each fgout time.
  For more details see :ref:`fgout`.
  
- The `fgout_tools.py` module was also substantially refactored and improved
  to support use with the Boussinesq solvers and also with D-Claw.
  
- For Boussinesq option, switch to using Riemann solvers from the riemann
  repository to be consistent with SWE version.

- Change `nodata_value` in `topotools` from -9999 to -99999.

- Fix bug related to tracking pressure at gauges.

- In `examples/tsunami//chile2010_fgmax-fgout`,
  simplify `make_fgout_animation.py` and add new 
  `make_fgout_animation_with_transect.py`, and update these for new
  `fgout` formatting.
  
- Add `dZ_format` paramegter to `DTopography.write` function to allow writing
  fewer digits (making smaller dtopo files).
  
- Fix wind issues near `r = 0` in center of storms.

- Allow more than 5 digits in gauge numbers.

- Fix some gauge plotting issues for storm surge.

- Numerous other bug fixes and enhancements.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.10.0...v5.11.0>`_


Changes to PyClaw
------------------

- Some changes related to CI and pytests, still in progress.


See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.10.0...v5.11.0>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.10.0...v5.11.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.10.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.10.0...v5.11.0>`_
