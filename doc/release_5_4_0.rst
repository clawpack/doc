

.. comment: Change master to v5.4.0 in github links below once release is tagged

.. _release_5_4_0:

==========================
Release 5.4.0
==========================

Release candidate pending.

Clawpack 5.4.0 will be released on TBA.  See :ref:`installing`.

Changes relative to Clawpack 5.3.1 (November 9, 2015) are shown below.

.. _release_5_4_0_global:

Global changes
--------------

**Python 3 compatibility.** Python code in all repositories has been updated so
that it should work with either Python 2 or Python 3.  In particular the
statements::

    from __future__ import absolute_import
    from __future__ import print_function

have been added and print statements have been replaced by print functions.
Various other minor changes were also required.

**Makefile structure for Fortran codes.** 
The `Makefile` in all Fortran examples and tests has been
modified to rely on a common list of library source code files,
rather than listing all of these in every `Makefile`.  Capabilites include
the ability to specify whether a library file should be replaced
by one from the local directory.  This is cleaner and will make it
easier to update code in the future -- if a new library routine is
required only one master list needs updating rather than the
`Makefile` in every example and users' application directories.
See :ref:`makefiles_library` for more details on how to specify
local files in place of default library files.

**Improved Gauge Output Options**
:ref:`gauges` in `amrclaw` and `geoclaw` now support a number of additional 
output options including:

 - specification of output fields, i.e. you can now specify the q and aux
   fields that are output;
 - specification of output field format, i.e. you can now specify the number
   of digits to output;
 - a minimum length of time at which a gauge is allowed to output, i.e. if
   this was set to 10 time units then the gauge would only output every 10
   time units or longer;
 - support for future file format specifications (only ASCII is supported now);

Other improvements to gauge handling include:

 - a refactor of how the code stores gauge data has been done in the Fortran
   *gauges_module.f90* source file in each library.

 - Gauge output is accumulated in a buffer internally and written out
   intermitently, instead of writing to disk every time step.
   (The parameter `MAX_BUFFER` in the `amrclaw` library routines 
   `gauges_module.f90` controls the size of this buffer.)

 - The gauge output for the gauges is written to distinct files in the
   output directory, e.g. `gauge00001.txt` for gauge number 1.  In previous
   versions of Clawpack all gauges were written to a single file
   `fort.gauge`.  The new approach allows gauges to be written in parallel and
   also facilitates reading in a single gauge more quickly.

 - Some header info appears in each of these files to describe the gauge
   output.

 - When doing a restart (see :ref:`restart`), gauge output from the original run
   is no longer overwritten by the second run. Instead gauge
   output from the restart run will be appended to the end of each
   `gaugeXXXXX.txt` file.


**Updated regression testing framework for Fortran.**
The Fortran code uses an updated framework and so the regression data has
changed.

Changes to classic
------------------

**Makefile structure.** See discussion above, under
:ref:`release_5_4_0_global`.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.3.1...master>`_

Changes to clawutil
-------------------

**Makefile structure.** The `Makefile.common` was updated to support the
changes described in the discussion above, under
:ref:`release_5_4_0_global`.

**Better support for gauges.**  
New supporting code added.

**Updated regression testing framework for Fortran.**
New supporting code added.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.3.1...master>`_

Changes to visclaw
------------------

**Parallel Plotting in setplot.py.**
A new capability has been added to plot multiple frames at once  on
a multicore machine when doing `make plots` (i.e. not interactive).
The png files for different frames can be simultaneously generated.
To use this feature you need to:

 - Add the line `plotdata.parallel = True` (usually at the 
   bottom) to `setplot.py`.

and then *either*:

 - Add the line `plotdata.num_procs = 4` (or however many processes you
   wish to use), or

 - Alternatively you can set the shell environment variable 
   `OMP_NUM_THREADS` to the number of processes desired.  

The value specified by `OMP_NUM_THREADS` is used only if
`plotdata.num_procs` is not set.  If neither is set, the default
is to use only one process.

**Gauge plots.** 
Updates to go with improvements to how gauges are handled.

**KML files for GeoClaw output.**
Some improvements have been made to the capabilities for creating KML and
KMZ files for plotting on Google Earth or with other GIS tools.

See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.3.1...master>`_

Changes to riemann
------------------

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.3.1...master>`_

Changes to amrclaw
------------------

**Makefile structure.** See discussion above, under
:ref:`release_5_4_0_global`.

**Gauge output** See discussion above, under
:ref:`release_5_4_0_global`.

**Ghost Cell  (filpatch) Filling.**
A list of the neighboring grids at same the level of refinement 
that are used for filling ghost cells for each grid patch is saved between
regridding steps. This improves the speed of `filpatch`
operations. (Not yet implemented for neighboring grids at coarser level,
still have to search for neighbors.)

**Proper Nesting.**
Insidious but rare bug fixed, where occasionally a fine level grid had
cells with no underlying coarse grid cell from which to interpolate the
new values.  The fix can make regridding more expensive when more than 3
levels of refinement are used. (This will be addressed in future
revisions).  Also, there were several different ways of projecting a
cell to a coarser level. This was made consistent across all routines.
The refined grids that are generated are now somewhat different and may
cover a slightly larger area than in previous releases.

**3D filpatch bug fix.**
Fixed a bug in calculating indices used when interpolating from coarse to fine
grid ghost cells. (Fixed in 2D in previous release.) 

**Output Formats.**
Enlarged formats in many format statements used for ascii output
throughout.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.3.1...master>`_

Changes to geoclaw
------------------

**Makefile structure.** See discussion above, under
:ref:`release_5_4_0_global`.

**Gauge output** See discussion above, under
:ref:`release_5_4_0_global`.

The changes in amrclaw titled **Ghost Cell  (filpatch) Filling**,
**Proper Nesting** and **Output Formats**
also affect geoclaw. See notes above.

**fgmax Checkpoint/Restart Capability.**
If checkpoints have been requested, `fgmax` variables are 
added to the end of the checkpoint file. This enables a calculation to
restart for a longer simulation time and still compute valid `fgmax` 
amplitudes and arrival times,  instead of reinitializing the `fgmax` arrays.
See :ref:`fgmax`.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.3.1...master>`_


Changes to PyClaw
------------------

**Python 3 compatibility.** See discussion above, under
:ref:`release_5_4_0_global`.

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.3.1...master>`_

