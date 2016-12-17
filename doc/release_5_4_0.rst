

.. comment: Change master to v5.4.0 in github links below once release is tagged

.. _release_5_4_0:

==========================
Release 5.4.0
==========================

Release candidate pending.

Clawpack 5.4.0 will be released on TBA.  See :ref:`installing`.

Changes relative to Clawpack 5.3.1 (November 9, 2015) are shown below.


Changes to classic
------------------


See `classic diffs
<https://github.com/clawpack/classic/compare/v5.3.1...master>`_

Changes to clawutil
-------------------

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.3.1...master>`_

Changes to visclaw
------------------

 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.3.1...master>`_

Changes to riemann
------------------

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.3.1...master>`_

Changes to amrclaw
------------------

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


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.3.1...master>`_

