:orphan:
  
.. _release_5_10_0:

===============================
v5.10.0 release notes
===============================

Clawpack 5.10.0 was released on XX. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.XX


Changes relative to Clawpack 5.9.2 (November 4, 2023) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.10.0) on XX.

These changes should appear in the next release.  If you need them now,
see :ref:`developers` for instructions on cloning and installing from the
master branch. 

To see documentation that has already been developed to accompany any new
features listed below, click on the "dev" branch of the documentation, in
the menu on the left hand side of this page.

Changes that are not backward compatible
----------------------------------------

- The switch to meson made in v5.9.2 requires the installation of some
  additional packages for developers or others who choose to clone the
  repositories from Github.  The instructions in :ref:`setup_dev` 
  now include instructions to::

    pip install -r requirements-dev.txt

  as part of the installation.



Changes to classic
------------------

None.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.9.2...v5.10.0>`_

Changes to clawutil
-------------------

- `$CLAW/clawutil/src/Makefile.common`, the main Makefile imported by all
  application Makefiles in the Fortran versions, has been improved:

  - When using `make new` to recompile all routines, after the modules are
    compiled all other fortran source codes are compiled in parallel,
    speeding up the process.

  - RUNEXE was added to provide a string to be inserted before the name
    of the executable `EXE` in order to run it. This is necessary in
    particular to run the new 2D Boussinesq code using MPI, see
    :ref:`bouss2d` for instructions. 
    
    (Support for this also added to
    `$CLAW/clawutil/src/python/clawutil/runclaw.py`).

  - If `FC` is any variant of `gfortran` then use the same flags as
    `gfortran`.

- Support added to 
  `$CLAW/clawutil/src/python/clawutil/data.py` for `checkpt_style==4`
  in AMRClaw and GeoClaw (see below), and also for the 
  `D-Claw code <https://dlgeorge.github.io/project/dclaw-project>`_
  for granular-fluid flows,
  which is being updated to work with the latest version of Clawpack.
  This is still work in progress.

- Other minor changes.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.9.2...v5.10.0>`_

Changes to visclaw
------------------

- Change the default `plotfigure.facecolor` to white for plots made by `frametools.py` (rather than `clawpack_tan`).

- Add hillshade option to `frametools.py` for better visualization of topography.

- Add `imshow_norm` and `imshow_alpha` as ClawPlotItem attributes for imshow plots.

- Remove deprecated `faceted` kwarg in calls to pcolor from `frametools.py`.

- Updates to matlab plotting routines.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.9.2...v5.10.0>`_

Changes to riemann
------------------

- New Riemann solver for the p-system.

- Clean up some other things.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.9.2...v5.10.0>`_

Changes to amrclaw
------------------

- Bug fix for case when the domain is periodic only in x and not in y.

- STOP feature added: If you create a (possibly empty) file named STOP in the
  run directory then the code will stop at the end of the current coarse grid
  time step, after writing a checkpoint file. Useful to kill a computation with
  the ability to restart after fixing something.
  
  
  
- Most routines in `$CLAW/amr/src/2d` were cleaned up to replace do loop labels
  and closing continue statements with more modern `enddo`, avoiding
  many warning messages when compiling the code.
  (Still need to clean up 1d and 3d, and classic code, but this cleans up
  GeoClaw compilation a lot.)

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.9.2...v5.10.0>`_

Changes to geoclaw
------------------

- 1D GeoClaw code added, as described at :ref:`geoclaw1d`. In particular there
  are new directories `$CLAW/geoclaw/src/1d_classic` and
  `$CLAW/geoclaw/examples/1d_classic`.
  
- 1D Boussinesq code added in `$CLAW/geoclaw/src/1d_classic/bouss` and some of
  the examples, as described in :ref:`bouss1d`.
  
- 2D Boussinesq code added, as described in :ref:`bouss2d`.  In particular there
  are new directories `$CLAW/geoclaw/src/2d/bouss` and 
  `$CLAW/geoclaw/examples/2d/bouss`.

- `checkpt_style == 4` is now supported, meaning to create a checkpoint file
  at every output time.  (As with other options, setting it to -4 means to
  checkpoint at the same times but to alternate between two checkpoint files
  rather than creating a unique file for each checkpoint, greatly reducing
  storage if you only need the latest one.)
  
- Introduce `integer(kind=8)` variables for some `topo_module` variables to
  handle very large topo files for which the index was overflowing.
  
- Introduce STOP feature as described in above for amrclaw.

- Improve calculation of number of steps to take (`ntogo`) when CFL number is
  too large in one step.  (Still have issues sometimes where code dies with
  too many dt reductions....)
  
- Fix bug in python function `clawpack.geoclaw.util.bearing` and introduce new
  `clawpack.geoclaw.util.gctransect` to compute points along a great circle
  transect connecting two points on the sphere. (Transects obtained by
  linear interpolation in x,y are fine over small regions but not for
  global-scale transects.)
 
- Other minor bug fixes, improvements, and cleanup.
 
See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.9.2...v5.10.0>`_


Changes to PyClaw
------------------

None.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.9.2...v5.10.0>`_

For older changes in PyClaw, see also the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.9.2...v5.10.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.9.x...dev>`_
  shows changes in the `dev` branch not yet in the main version of the
  documentation.

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.9.2...v5.10.0>`_
