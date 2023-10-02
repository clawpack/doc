:orphan:
  
.. _release_5_9_1:

===============================
v5.9.1 release notes
===============================

Clawpack 5.9.1 was released on TBD, 2023. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.XXX


Changes relative to Clawpack 5.9.0 (August 26, 2022) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.9.1) on TBD, 2023.

These changes should appear in the next release.  If you need them now,
see :ref:`developers` for instructions on cloning and installing from the
master branch. 

To see documentation that has already been developed to accompany any new
features listed below, click on the "dev" branch of the documentation, in
the menu on the left hand side of this page.


Changes to classic
------------------

- None. 

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.9.0...v5.9.1>`_

Changes to clawutil
-------------------

- Consistently use `CLAW_PYTHON` in `Makefile.common`, which should point to
  the version of Python the user wants to use for Clawpack.

- Make some changes to ease the transition from `nose` (which is no longer
  supported) to `pytest` in the future.

- Other minor changes.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.9.0...v5.9.1>`_

Changes to visclaw
------------------

- The `ClawPlotAxes.title` string is used by default to make a title for the
  plot for each time frame with the time in the units used in the problem.
  A new capability was added so that if `title` includes the string 
  `d:h:m:s` then the time is assumed to be in seconds and is converted to
  days:hours:minutes:seconds in the title. Otherwise, if the `title` includes
  `h:m:s` then the time is converted to hours:minutes:seconds in the title. 
  This is particularly useful in GeoClaw.

- Some more attributes have been added to `ClawPlotFigure`, `ClawPlotAxes`,
  and `ClawPlotItem`
  to facilitate making nicer looking plots without so much need to use
  `kwargs` attributes or define an `afteraxes function`, for example.

  The lines below are extracted from
  `$CLAW/visclaw/src/python/visclaw/data.py`.
  For more information about these attributes (and others), see
  `<https://www.clawpack.org/dev/setplot.html>`__.

  - Added to `ClawPlotFigure`::
  
        self.add_attribute('figsize',None)
        self.add_attribute('facecolor',None)

      
  - Added to `ClawPlotAxes`::

        self.add_attribute('time_label_kwargs', {})  # kwargs for xlabel cmd
        self.add_attribute('kwargs', {})
        self.add_attribute('grid', None) # True to add grid() command
        self.add_attribute('grid_kwargs', {}) # argument to grid() command
        self.add_attribute('title_fontsize', None)
        self.add_attribute('title_kwargs', {}) # e.g. to set color
        self.add_attribute('title_t_format', None) # format for t in title
        self.add_attribute('xticks_fontsize', None) 
        self.add_attribute('xticks_kwargs', {}) # e.g. to set ticks,rotation
        self.add_attribute('yticks_fontsize', None) 
        self.add_attribute('yticks_kwargs', {}) # e.g. to set ticks
        self.add_attribute('xlabel', None) # label for x-axis
        self.add_attribute('ylabel', None) # label for y-axis
        self.add_attribute('xlabel_fontsize', None)
        self.add_attribute('ylabel_fontsize', None)
        self.add_attribute('xlabel_kwargs', {})
        self.add_attribute('ylabel_kwargs', {})
        self.add_attribute('aspect', None)
        self.add_attribute('aspect_latitude', None)
        self.add_attribute('useOffset', None)

  - Added to `ClawPlotItem`::

        self.add_attribute('colorbar_extend',None)
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.9.0...v5.9.1>`_

Changes to riemann
------------------

- None.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.9.0...v5.9.1>`_

Changes to amrclaw
------------------

- In 2d and 3d, `valout.f90` now calls `bound` before dumping arrays when doing
  binary output (since the ghost cells are also dumped in this case).
  
- On restart, do not advance the frame number if `output_t0 == True`, so that
  there is not a duplicated frame at the same time.
  
- Other minor fixes.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.9.0...v5.9.1>`_

Changes to geoclaw
------------------

- Fixed `fgmax_finalize.90` so that if a grid number `fgno` is specified
  for the fgmax grid then it uses this in constructing the filename for 
  output (rather than 1,2,3 based on order specified in `setrun.py`)
  
- Facilitate reading a topo file when at `topotools.Topography` object
  is first instantiated: the `__init__` function now calls `read()` if
  `path` is provided as an argument.

- `fgmax_tools.FGmaxGrid.read_output` function now takes an argument 
  `indexing` that is `'ij'` by default for backward compatibility, but setting
  to `'xy'` results in the fgmax grid having the same layout as topo
  grids generated by `topotools.Topography`, which is often useful.
  
- Added `geoclaw.data.FGmaxData.read()` function to read in the data from a
  `fgmax_grids.data` file.
  
- Added `sphere_source` as local variable in `src/2d/shallow/src2.f90`, set to
  0 for now for backward compability.  This allows testing the addition of
  source terms that should be included on the sphere but were always missing.
  After further testing, the plan is to change the default in the next major
  release v5.10.0 and also allow this to be adjusted in `setrun.py`.
  See `<https://www.clawpack.org/dev/sphere_source.html>`__
  for more information.
  
- Other minor fixes.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.9.0...v5.9.1>`_


Changes to PyClaw
------------------

- Some fixes in ASCII  output for compatibility with Fortran versions.

- Other minor fixes.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.9.0...v5.9.1>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.9.0...v5.9.1>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.9.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.9.0...v5.9.1>`_
