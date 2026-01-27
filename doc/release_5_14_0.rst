:orphan:

.. _release_5_14_0:

===============================
v5.14.0 release notes
===============================

Clawpack 5.14.0 was released on January 26, 2026. See :ref:`installing`.

Permanent DOI: https://doi.org/10.5281/zenodo.18382457


Changes relative to Clawpack 5.13.1 (Sept. 12, 2025) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

- A couple bugs were discovered in the GeoClaw code from v5.13.0 and v5.13.1,
  so GeoClaw users should be careful using results obtained with those.

  The most serious bug fix is a change to the main GeoClaw Riemann solver,
  discussed further in the `riemann` section below.  The pre-v5.13.0 version
  has been restored.

  The ranking algorithm for ordering the topofiles provided by the user
  has also changed slightly, and some changes might be observed if the user
  specifies two topofiles with essentially the same resolution but that
  differ slightly due to rounding errors in the `dx` and/or `dy` values.
  See `geoclaw` section below for more details.  Also, the new feature
  introduced in v5.13.0 to allow more control over topo file ordering did
  not work properly at all and has now been fixed.

General changes
---------------

- None


Changes to classic
------------------

- None

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.13.1...v5.14.0>`_

Changes to clawutil
-------------------

- `Makefile.common` was updated to include compiler flags for the intel ifx
  compiler.

- minor bug fixes and other changes.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.13.1...v5.14.0>`_

Changes to visclaw
------------------

- A few enhancements.

See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.13.1...v5.14.0>`_

Changes to riemann
------------------

- The Riemann solver in `geoclaw_riemann_utils.f` was modified to revert
  one change back to the version from v5.12.0 and earlier.
  This change was made in commit 4340757 and released in v5.13.0 to improve
  the order of accuracy on some test problems, but then it was found to give
  streaks in velocity on some practical problems. Reviewing the git history,
  this was seen earlier, and the code that we are reverting to in this commit
  was added in 2016 (in commit 9c02ede) to fix this problem.

  See
   - https://github.com/clawpack/riemann/pull/187
   - https://github.com/clawpack/riemann/issues/188

- Other minor changes.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.13.1...v5.14.0>`_

Changes to amrclaw
------------------

- Fix example `$CLAW/amrclaw/examples/advection_2d_inflow`.

- Introduce binary output option for gauges in 1D.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.13.1...v5.14.0>`_

Changes to geoclaw
------------------

- The modification of the Riemann solver discussed above in the `riemann`
  repository section may give different results.

- The new feature introduced in v5.13.0 to allow more control over
  topo file ordering, described at :ref:`topo_order`,
  which is used by setting the new `setrun.py` parameter to:

      rundata.topo_data.override_order = True

  did not work as advertised and would have ordered topo files in the
  opposite order than what is indicated in the documentation.
  Moreover, if one or more dtopo file is specified, a more serious
  problem arose, since special `topo_for_dtopo`
  topography arrays are introduced at the resolution of each dtopo file.
  These were not necessarily being properly ordered with
  `topo_data.override_order = True`.

  A refactoring of the ordering algorithms has addressed this problem.
  The `topo_data.override_order` now only controls the ordering of the
  original topo files specified in `setrun.py`, and then the `topo_for_dtopo`
  files are inserted in the ordered list.  For more discussion see

    - https://github.com/clawpack/geoclaw/issues/689
    - :ref:`topo_order`

- As part of the refactor mentioned above, the ordering of topofiles may
  also change in the case where `topo_data.override_order = False` but
  two files at essentially the resolution are specified.  If the resolutions
  are exactly equal then the one listed last in `setrun.py` is given
  preference, but if their resolutions (as judged by `dx*dy`) is slightly
  different due to rounding errors in `dx` and/or `dy`, then the one listed
  first might have been used if it had slightly smaller `dx*dy`.  The new
  code introduces a fudge factor so that the resolution is considered better
  only if the area if the difference in `dx*dy` is greater than some
  relative tolerance (set to `0.001`) times the smaller area.

  This change could lead to different results from GeoClaw than past versions
  (even when not using the `topo_data.override_order` option), if it means a
  different topo file at a nearly equal resolution is now given priority.
  This should only happen if the user has nearly-equal resolution topo files
  that cover an overlapping region and would only be a problem if their
  topo values `Z` differ signficiantly in this region.

- As part of the refactor, the information about the ordering of topo
  and `topo_for_dtopo` files that is written to `_output/fort.geo` has been
  clarified, and users are encouraged to check this file to insure that
  topo files are being given the desired order of priority.

- The module `center_points.py` was improved and a new utility
  `$CLAW/geoclaw/src/python/geoclaw/center_gauges.py` was added, to center
  gauges or other specific points in grids cells at a specified resolution.

- Arguments `buffer` and `align` were added to the `topotools` functions `crop`
  and `read_netcdf`, to allow user to insure a buffer of points surrounds the
  desired extent, and to subsample (when `coarsen > 1`) with the starting
  index chosen so the resulting points are aligned with specified values if
  possible.  This is useful if the original DEM has points aligned with integer
  longitudes and latitudes, for example, and this properly should be preserved
  for the coarser grid (i.e. the distance between points and an integer
  longitude or latitude is an integer number of grid cells on the coarser grid).

- `kmltools.make_input_data_kmls` improved so it doesn't die if a topofile
  or dtopofile is not found (it just does not make a kml file showing the
  extent), useful if doing `make data` on a laptop for a problem where large
  topofiles only exist on a supercomputer, for example.

- Add `make_function` methods to both `topotools.Topography` and
  `dtopotools.DTopography` to easily compute an interpolating function that
  can be used to evaluate along a transect, for example.

- Several other more minor bug fixes and enhancements.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.13.1...v5.14.0>`_


Changes to PyClaw
------------------

- Better command line interface for gauge comparisons.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.13.1...v5.14.0>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.13.1...v5.14.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.12.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.13.1...v5.14.0>`_
