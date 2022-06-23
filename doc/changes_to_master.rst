:orphan:

.. _changes_to_master:

===============================
Changes to master since v5.8.2
===============================


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.8.2) on December 14, 2021.

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

- `'binary32`' added as an `output_format` option in both amrclaw and
  geoclaw. (So far classic only supports `'ascii'` output.) The old
  `'binary'` option now defaults to `'binary64'`, which dumps the raw 
  binary of the full float64 (kind=8) Fortran variables.  The new
  `'binary32'` option trucates to float32 (kind=4) before dumping, and
  results in binary output files that are only half as large.  Since
  float32 values have about 8 significant figures, this is generally
  sufficient for most plotting and post-processing needs.  These files
  are also much smaller than the files created with the `'ascii'`
  option, which is generally recommended only for debugging if you need to 
  examine the output files directly.

- Adding support for `'binary32'` required changes in the pyclaw, clawutil 
  and visclaw repositories as well.

- A new `fgout` capability was added to geoclaw (see below and :ref:`fgout`),
  which also required additional changes to other repositories.



Changes to classic
------------------

- Comments in some sample `setrun.py` files were changed to make it clear
  that only `output_format = 'ascii'` is supported so far in classic.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.8.2...master>`_

Changes to clawutil
-------------------

- Support for `'binary32'` and `fgout` grids added.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.8.2...master>`_

Changes to visclaw
------------------

- Support for `'binary32'` and `fgout` grids added.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.8.2...master>`_

Changes to riemann
------------------


See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.8.2...master>`_

Changes to amrclaw
------------------

- Support for `output_format='binary32'` added.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.8.2...master>`_

Changes to geoclaw
------------------

- Support for `output_format='binary32'` added.

- New `fgout` grid capabilities added, as described at :ref:`fgout`.
  This allows specifying one or more fixed resolution rectangular grids on
  which the AMR solution will be interpolated (in both space and time)
  at each time in a specified set of times.  This does not affect the
  time steps used in the computation and allows frequent output on a
  fixed portion of the domain for making animations or doing
  post-processing, such as particle tracking based on the velocity field.

- The new `fgout` capability (together with :ref:`fgmax`)
  replaces the very old `fixedgrid` capability,
  which has now been further deprecated.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.8.2...master>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.8.2...master>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.8.2...master>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.8.x...dev>`_
  shows changes in the `dev` branch not yet in the posted version of the
  documentation.

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.8.2...master>`_

