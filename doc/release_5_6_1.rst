:orphan:

.. _release_5_6_1:

===============================
v5.6.1 release notes
===============================

**DRAFT**

Clawpack 5.6.1 is **pending**.  See :ref:`installing`.

Changes *to master* relative to Clawpack 5.6.0 (June 2, 2019) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

`$CLAW/amrclaw/src/2d/amr_module.f90` has changed, so do a `make new` in 
any AMRClaw or GeoClaw application directories.

General changes
---------------


Changes to classic
------------------

None.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.6.0...master>`_

Changes to clawutil
-------------------

- The python package `subprocess` is now used in `runclaw.py`, improving ability
  to run multiple models.
- Improved handling of Fortran modules.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.6.0...master>`_

Changes to visclaw
------------------

- Improvements to `plot_timing_stats.py` to create plots of CPU time and wall
  time used in a simulation, and number of cells updated.
  For some examples of the output, see http://staff.washington.edu/rjl/misc/timing_plots/
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.6.0...master>`_

Changes to riemann
------------------

None.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.6.0...master>`_

Changes to amrclaw
------------------

- Improvements in how timing of code is done, in particular using `integer(kind=8)`
  variables for better computation of wall time.
- Improve handling of `AdjointData` file references.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.6.0...master>`_

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
  
See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.6.0...master>`_


Changes to PyClaw
------------------

None.

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.6.0...master>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.6.0...master>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.6.0...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.6.0...master>`_

