:orphan:
  
.. _release_5_9_0:

===============================
v5.9.0 release notes
===============================

Clawpack 5.9.0 was released on August 26, 2022. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.7026045


Changes relative to Clawpack 5.8.2 (December 14, 2021) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.9.0) on August 26, 2022.

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
  For more info, see :ref:`output_styles`.

- Gauge output in amrclaw and geoclaw can also now be specified as
  'ascii', 'binary64', or 'binary32'; see :ref:`gauges` for instructions.

- Adding support for `'binary32'` required changes in the pyclaw, clawutil 
  and visclaw repositories as well.

- A new `fgout` capability was added to geoclaw (see below and :ref:`fgout`),
  which also required additional changes to other repositories.



Changes to classic
------------------

- Comments in some sample `setrun.py` files were changed to make it clear
  that only `output_format = 'ascii'` is supported so far in classic.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.8.2...v5.9.0>`_

Changes to clawutil
-------------------

- Support for `'binary32'` and `fgout` grids added.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.8.2...v5.9.0>`_

Changes to visclaw
------------------

- Support for `'binary32'` and `fgout` grids added.

- `pcolor` plots are now rasterized by default, which greatly reduces the
  file size in some cases.  When e.g. `savefig('filename.svg')` is used
  the labels are still vector graphics but the flow field is rasterized.
  Passing the option `pcolor_kwargs = {"rasterized":False}` in setplot
  turns this off. See `<https://github.com/clawpack/visclaw/pull/286>`_.

- The `JSAnimation` subdirectory was removed, since we now use
  `anim.to_jshtml` instead.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.8.2...v5.9.0>`_

Changes to riemann
------------------

- None.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.8.2...v5.9.0>`_

Changes to amrclaw
------------------

- Support for `output_format='binary32'` added for both output frames and
  gauges.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.8.2...v5.9.0>`_

Changes to geoclaw
------------------

- Support for `output_format='binary32'` added for both output frames and
  gauges.

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

- `$CLAW/geoclaw/examples/tsunami/chile2010_fgmax` has been replaced by
  `$CLAW/geoclaw/examples/tsunami/chile2010_fgmax-fgout`.  This example
  now also shows how to plot results on fgout grids either by 
  using a special `setplot` function or by reading them directly.
  It also shows how to make an animation from the fgout results.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.8.2...v5.9.0>`_


Changes to PyClaw
------------------

- Support for reading fgout frames added, by passing the parameter
  `file_prefix` more consistently (which can be e.g. `fgout` rather than
  `fort`, as used for output frames).

- Support for reading binary output files with format `'binary32'` or
  `'binary64'`.  Added for both output frames and gauges.  The old `'binary'`
  format is equivalent to `'binary64'`.

- Support reading `file_format` from the `fort.t` files, now one of `ascii`,
  `binary32`, or `binary64`.  See General Changes above for more details.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.8.2...v5.9.0>`_

For older changes in PyClaw, see also the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.8.2...v5.9.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.9.x...dev>`_
  shows changes in the `dev` branch not yet in the main version of the
  documentation.

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.8.2...v5.9.0>`_

