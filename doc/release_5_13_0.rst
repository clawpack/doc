:orphan:

.. _release_5_13_0:

===============================
v5.13.0 release notes
===============================

Clawpack 5.13.0 was released on TBD. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.TBD


Changes relative to Clawpack 5.12.0 (May 5, 2025) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

- `src/geoclaw_riemann_utils.f90` was modified to improve the convergence rate
  on a smooth problem.  This does not seem to affect results in general, but may
  lead to slight differences in GeoClaw simulations since this affects the core
  Riemann solver used for shallow water equations.

- Several bugs were also fixed in the Boussinesq (dispersive) version of
  GeoClaw, which may continue to evolve.

General changes
---------------

Unit testing and continuous integration on Github continue to be broken, but
we are working on modifying tests to use `pytest` (rather than `nose`) and
Github CI (rather than travis).

As part of this, the `tests` subdirectories of several repositories (`classic`,
`amrclaw`, `geoclaw`) are being eliminated or reduced in scope, while many of
the examples in the `examples` subdirectories now have new python scripts
starting with `test_` that typically run a smaller version of the example and
then compare some output with values stored in a `regression_data` subdirectory.

The `NumFocus Code of Conduct <https://github.com/clawpack/clawpack/blob/master/CODE_OF_CONDUCT.md>`__ has been adopted by the Clawpack project and
a file describing this has been added to the top directory of many of the
repositories.

Changes to classic
------------------

- Some examples modified to incorporate quick tests for conversion to
  `pytest` framework, with corresponding directorys in `tests` removed.

- Minor changes to clean up  old files.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.12.0...v5.13.0>`_

Changes to clawutil
-------------------

- switch from `repr` to `str` in `data.py` so that arrays are properly
  converted to list of numbers in `.data` files (rather than e.g.,
  `0.3` showing up as `np.float64(0.3)`, as produced by recent numpy versions.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.12.0...v5.13.0>`_

Changes to visclaw
------------------

- Several minor changes.

See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.12.0...v5.13.0>`_

Changes to riemann
------------------

- `src/geoclaw_riemann_utils.f90` was modified to improve the convergence rate
  on a smooth problem.  Does not seem to affect results in general, but may
  lead to slight differences in GeoClaw simulations since this affects the core
  Riemann solver used for shallow water equations.

- `sw_aug_1d_solver.f90` was added.

- Several minor changes.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.12.0...v5.13.0>`_

Changes to amrclaw
------------------

- Fix ruled rectangle flagregions to be less sensitive to roundoff, so same
  refinement patches are more consistently computed with different compilers.

- Fix definition of `timing_line` in `valout.f90` that throws error with
  newer gfortran compilers (e.g. 15.1.0)

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.12.0...v5.13.0>`_

Changes to geoclaw
------------------

- See changes to `riemann/src/geoclaw_riemann_utils.f90` which affect the
  core Riemann solver for shallow water equations.

- Some bugs were fixed in the boussinesq version of the code.

- Fix definition of `timing_line` in `valout.f90` that throws error with
  newer gfortran compilers (e.g. 15.1.0)

- There is a new `setrun.py` parameter `rundata.topo_data.override_order`
  that is set to `False` by default to produce the default behavior in which
  cell-averaged topography values in GeoClaw are computed using the "best
  available" topofile at each point, assuming higher resolution (as defined
  by cell area `dx*dy` in the DEM) is better.  If this parameter is set to
  `True` then instead the order the topofiles are specified in `setrun.py`
  is instead used (with best listed last).  This is particulalry useful if two
  topofiles have essentially the same resolution but the cell areas differ
  slightly and it is important to be precise about which one has the better
  data.  See :ref:`topo_order` for more details.

- A new function `geoclaw.kmltools.dtopo_contours2kmz` was added to plot
  contour lines of a dtopo deformation and wrap the plot in kml for viewing
  on Google Earth.

- Deprecated `np.infty` replaced by `np.inf` several places.

- `geoclaw.dtopotools.create_dtopography` was refactored so that the surface
  deformation `dZ` does not have to be first computed (and saved) for each
  subfault and then combined into the final `dZ`, which caused memory issues
  when `dZ` is on a fine grid and there are several thousand subfaults.
  Now each subfault `dZ` is discarded after use in accumulating the global `dZ`,
  greatly reducing the memory footprint.

- Numerous other bug fixes and enhancements.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.12.0...v5.13.0>`_


Changes to PyClaw
------------------

- Several other minor changes.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.12.0...v5.13.0>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.12.0...v5.13.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.12.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.12.0...v5.13.0>`_
