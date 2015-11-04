
.. comment: Change version numbers and DATE.

.. _release_5_3_1:

==========================
Release 5.3.1
==========================

Clawpack 5.3.1 was released on DATE.  See :ref:`installing`.

Changes relative to Clawpack 5.3.0 (May 21, 2015) are shown below.

Changes to classic
------------------

Minor fixes and new testing framework.

See `classic diffs <https://github.com/clawpack/classic/compare/v5.3.0...v5.3.1>`_

Changes to clawutil
-------------------

Allow `checkpt_style < 0` in `setrun.py`, see Changes to amrclaw below.

New testing framework.

See `clawutil diffs <https://github.com/clawpack/clawutil/compare/v5.3.0...v5.3.1>`_

Changes to visclaw
------------------

Added `amr_data_show` attribute to `ClawPlotItem` to suppress certain amr levels in plotting.
 
Read gauge locations from `setgauge.data` file in `plotdata.outdir` rather
than in `datadir`.  This works better if gauges are changed for new runs but
you want to plot old output.

Fix `colormaps.add_colormap` function to work better for combining two
different colormaps for different ranges of a variable in certain cases.

See `visclaw diffs <https://github.com/clawpack/visclaw/compare/v5.3.0...v5.3.1>`_

Changes to riemann
------------------

Added `src/riemann_interactive.py` for making interactive plots of the phase
plane in Jupyter notebooks.  For an example, see 
http://nbviewer.ipython.org/github/maojrs/ipynotebooks/blob/master/interactive_test.ipynb.


See `riemann diffs <https://github.com/clawpack/riemann/compare/v5.3.0...v5.3.1>`_

Changes to amrclaw
------------------

Bug in 3d dimensional splitting fixed --- the CFL was computed incorrectly,
causing the code to use timesteps that are too large and go 
unstable in some cases.

Improved the checkpoint and restart capabilities, adding the option to set
`checkpt_style < 0` in `setrun.py` if you want the checkpoint to alternate
between two files rather than creating a unique new file each time a
checkpoint is done.  This reduces storage needed if you want to checkpoint
frequently but only need the most recent one, e.g. to guard against crashes
in a long run.  Two files are used in case the code crashes in the middle of
doing a checkpoint, the previous one is still intact.  You can set
`checkpt_style = -2`, for example, to give the same behavior as
`checkpt_style = 2` but with only two files.

Also improved checkpointing so that the output files `fort.amr` and `fort.gauge`
have buffers flushed whenever checkpointing, to avoid possibly losing some
gauge output if the code crashes.  Now `fort.gauge` will have data at least
up to the last checkpoint time.

Fixed so that `advanc` is not called initially if `flag_richardson` is
`False`, avoiding some unneeded work in this case.

Better reporting of statistics regarding run time and number of cells
integrated is now provided to the screen at the end of a run, and to the
file `_output/fort.amr`.  In particular, better reports wall time vs. CPU
time when OpenMP is used, and breaks this down into several groups to help
determine where the code is spending the most time.

New testing framework and several changes in the `tests` directory.

See `amrclaw diffs <https://github.com/clawpack/amrclaw/compare/v5.3.0...v5.3.1>`_

Changes to geoclaw
------------------

Binary output option added for multi-layer code.

Bug fixes in `topotools` and `dtopotools`.

Better reporting of statistics regarding run time and number of cells
integrated is now provided to the screen at the end of a run, and to the
file `_output/fort.amr`.  In particular, better reports wall time vs. CPU
time when OpenMP is used, and breaks this down into several groups to help
determine where the code is spending the most time.

Restart option changed so that `fort.gauge` is appended to rather than
clobbering the previous version.  This may be modified in future releases,
it is currently inconsistent with what's done in amrclaw.  See
https://github.com/clawpack/clawutil/issues/93.

New testing framework.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.3.0...v5.3.1>`_

Changes to PyClaw
------------------

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/v5.3.1/CHANGES.md>`_.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.3.0...v5.3.1>`_

