:orphan:

.. _release_5_12_0:

===============================
v5.12.0 release notes
===============================

Clawpack 5.12.0 was released on May 5, 2025. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.15350682


Changes relative to Clawpack 5.11.0 (August 25, 2024) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

- In GeoClaw, several bugs were fixed in the implicit solvers for Boussinesq
  equations. A newer version of PETSc (>= 3.20) is now required and names
  of some variables in the `petscMPIoptions` file have changed, along with
  some of the environment variables expected in the `Makefile`.


General changes
---------------

Unit testing and continuous integration on Github continue to be broken, but
we are working on modifying tests to use `pytests` (rather than `nose`) and
Github CI (rather than travis).

Changes to classic
------------------

- None

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.11.0...v5.12.0>`_

Changes to clawutil
-------------------

- A `make check` option has been added to the general `Makefile.common`,
  which prints out the values of environment variables used in the `Makefile`.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.11.0...v5.12.0>`_

Changes to visclaw
------------------

- Several minor changes.

See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.11.0...v5.12.0>`_

Changes to riemann
------------------

- Several minor changes.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.11.0...v5.12.0>`_

Changes to amrclaw
------------------

- Fix gauges so value at initial gauge reporting time `t1` is alway output at
  start of gauge output file.  Previously if `min_time_increment > 0` was set
  for a gauge it wouldn't capture the gauge value until this long after the
  starting time value `t1` specified for the gauge.

- Allow an arbitrary number of flagregions (was limited to 99 previously).

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.11.0...v5.12.0>`_

Changes to geoclaw
------------------

- Some new capabilities added for storms.

  Support for reading in data files that specify wind and pressure
  fields on a grid is now supported. This currently specifically
  reads files in the Oceanweather Inc. formats NWS12 (ASCII) and
  NWS13 (NetCDF) with further support for more general NetCDF data
  included. This should be considered experimental at this time but
  is included to test this functionality out and start to plan out
  support for more file formats and nested grids.

- A new `speed_limit` was introduced that can be set in `setrun.py`, e.g. ::

    rundata.geo_data.speed_limit = 20.  # meters/sec

  This is used to reduce the fluid speed each time step in any cell where the
  speed exceeds this value.
  The default value is 50, which is larger than physically
  reasonable speeds for almost all problems. This fix seems to often eliminate
  problems where the code dies with `Too many dt reductions`.
  See https://www.clawpack.org/dev/speed_limit.html for details and more
  discussion.

- Several bugs were fixed in the 2D Boussinesq solver implementation described
  at https://www.clawpack.org/bouss2d.html, mostly concerning the way
  boundary conditions at patch edges are handled in the linear system solver
  when there are
  re-entrant corners on a fine level (e.g. the inside corner of an L-shaped
  union of patches).  Domain boundaries were not always handled properly in the
  case of solid wall or periodic boundary conditions.

- For efficiency, the sparse matrix needed for the dispersive terms is now
  built directly in CSR (compressed sparse row) format, as used by the
  PETSc linear solvers, instead of building the matrix in 
  COO (coordinate, or triplet format) and then converting.  
  This should not affect users' code (except to make it run faster).

- The 2D Boussinesq code should now be run with PETSc 23.0 (or later), which
  requires some changes to parameter names in the `petscMPIoptions` file
  and environment variables used in a Boussinesq application `Makefile`.
  See https://www.clawpack.org/bouss2d.html, and
  `$CLAW/geoclaw/examples/bouss/README.txt` for more information.

- The calling sequence of `cellgridintegrate` was changed to remove `topo_module`
  variables.

- Numerous other bug fixes and enhancements.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.11.0...v5.12.0>`_


Changes to PyClaw
------------------

- Some changes related to CI and pytests, still in progress.

- Several other minor changes.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.11.0...v5.12.0>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.11.0...v5.12.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.11.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.11.0...v5.12.0>`_
