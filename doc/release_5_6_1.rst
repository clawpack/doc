:orphan:

.. _release_5_6_1:

===============================
v5.6.1 release notes
===============================

Clawpack 5.6.1 is should be released on October 29, 2019. See :ref:`installing`.

Changes relative to Clawpack 5.6.0 (June 2, 2019) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

`$CLAW/amrclaw/src/2d/amr_module.f90` has changed, so do a `make new` in 
any AMRClaw or GeoClaw application directories.

General changes
---------------

A `gpu` branch has been added to many git repositories, and checking this out
gives a GPU version of two-dimensional AmrClaw and GeoClaw, as described at
:ref:`gpu`.  This version does not have equivalent capabilities to v5.6.1,
however, and is not included as part of the tar file for this release.


Changes to classic
------------------

None.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.6.0...v5.6.1>`_

Changes to clawutil
-------------------

- The python package `subprocess` is now used in `runclaw.py`, improving ability
  to run multiple models.
- Improved handling of Fortran modules.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.6.0...v5.6.1>`_

Changes to visclaw
------------------

- Improvements to `plot_timing_stats.py` to create plots of CPU time and wall
  time used in a simulation, and number of cells updated.
  For some examples of the output, see http://staff.washington.edu/rjl/misc/timing_plots/
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.6.0...v5.6.1>`_

Changes to riemann
------------------

- 1D MHD solver added.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.6.0...v5.6.1>`_

Changes to amrclaw
------------------

- Improvements in how timing of code is done, in particular using `integer(kind=8)`
  variables for better computation of wall time.
- Improve handling of `AdjointData` file references.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.6.0...v5.6.1>`_

Changes to geoclaw
------------------

- Some fixes to checkpoint and restart files
- Several changes to storm surge codes, including handling more forms of storm
  input data.
- Improvements in how timing of code is done, in particular using `integer(kind=8)`
  variables for better computation of wall time.
- Faster version of `filpatch` improves regridding performance substantially
  for some applications by re-using topo values rather than recomputing them.
- If some topo values are missing replace by value that makes this clearer
  by default, or allow the user to set an appropriate `topo_missing` value.
- New `geoclaw/examples/tsunami/bowl-slosh-netcdf` added to illustrate
  using netCDF topofiles.
  
See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.6.0...v5.6.1>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.6.0...v5.6.1>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.6.0...v5.6.1>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.6.0...v5.6.1>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.6.0...v5.6.1>`_

