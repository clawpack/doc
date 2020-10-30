:orphan:

.. _changes_to_master:

===============================
Changes to master since v5.7.1
===============================


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.7.1) on September 11, 2020.

These changes should appear in the next release.  If you need them now,
see :ref:`developers` for instructions on cloning and installing from the
master branch. 

To see documentation that has already been developed to accompany any new
features listed below, click on the "dev" branch of the documentation, in
the menu on the left hand side of this page.

Changes that are not backward compatible
----------------------------------------


General changes
---------------


Changes to classic
------------------


See `classic diffs
<https://github.com/clawpack/classic/compare/v5.7.1...master>`_

Changes to clawutil
-------------------


See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.7.1...master>`_

Changes to visclaw
------------------

 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.7.1...master>`_

Changes to riemann
------------------


See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.7.1...master>`_

Changes to amrclaw
------------------


See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.7.1...master>`_

Changes to geoclaw
------------------

Several changes were made to fix long-standing bugs.  These fixes lead to
slightly different results than those obtained with previous versions of
GeoClaw.  In all the tests performed so far the changes are minor and it is
thought that the new version is at least as accurate as the old version. 
Please let the developers know if you run into problems that may be related
to these changes.

- In `filpatch.f90`: The slope chosen for interpolating from a
  coarse grid to the ghost cells
  of a fine-grid patch had an index error that could affect the
  sign of the slope used in momentum components.  Also slopes were
  not always initialized to zero properly at the start of a loop

- Some index errors were fixed in `fgmax_interp.f90`.

- WIP: Changes to `riemann/src/rpt2_geoclaw.f90`.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.7.1...master>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.7.1...master>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.7.1...master>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.7.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.7.1...master>`_

