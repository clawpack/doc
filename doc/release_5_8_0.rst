:orphan:

.. _release_5_8_0:

===============================
v5.8.0 release notes
===============================

Clawpack 5.8.0 was released on TBA. See :ref:`installing`.

Permanent DOI: TBA


Changes relative to Clawpack 5.7.1 (Sept. 11, 2020) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

- For AMRClaw and GeoClaw, the data file `amr.data` now created from
  `setrun.py` now includes an additional line with the parameter `memsize`
  specifying the initial length of the `alloc` array used for allocating
  memory to patches when adaptive refinement is used.  This can be specified
  in `setrun.py` by setting `amrdata.memsize`.  If it is not set, then 
  default values are used that are similar to past default values;
  see :ref:`setrun_amrclaw`.
  So this is backward compatible in the sense that no changes to `setrun.py`
  are required, but the old `amr.data` files will not work so you may need 
  to do `make data` to create a new version.

- In GeoClaw, refinement "regions" can no longer be specified implicitly
  when listing a topo dtopo or qinit file.  See the `geoclaw` section below.
  **Note:** You may need to explicitly declare new `regions` or
  `flagregions` to produce the same behavior as in past versions of GeoClaw.

- The GeoClaw transverse Riemann solver `rpt2_geoclaw.f` has been improved
  and results in slightly different computated results in some cases. For
  more details see the `riemann` and `geoclaw` sections below.

- For AMRClaw and GeoClaw,
  an additional short array is saved in a checkpoint file for use in a 
  restart.  Due to this change, a checkpoint file created using a previous
  version of Clawpack cannot be used for a restart with the new version.

General changes
---------------

The travis tests that automatically run on pull requests no longer test using
Python2, only Python3.  See :ref:`python-three`.

Changes to classic
------------------


See `classic diffs
<https://github.com/clawpack/classic/compare/v5.7.1...v5.8.0>`_

Changes to clawutil
-------------------


See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.7.1...v5.8.0>`_

Changes to visclaw
------------------

- `ClawPlotAxes.skip_patches_outside_xylimits` does not work properly if there
  is a `mapc2p` function defining a grid mapping, so it is now ignored in 
  this case.

 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.7.1...v5.8.0>`_

Changes to riemann
------------------

- The GeoClaw transverse solver `rpt2_geoclaw.f` was modified to fix some
  long-standing bugs and change some of the logic.  
  
  The new version gives
  slightly different results on most problems, but extensive testing indicates
  the new results are at least as good as the old.  The new version has also
  been refactored to make the logic clearer and to avoid some unnecessary work,
  and generally runs faster.  In some cases where instabilities had been
  observed in long-duration runs (particularly for storm surge), the new 
  version appears to provide better stability.
  
  In particular, the left- and right-going waves are now split up transversely
  using states in the cell to the left (resp. right) in which the splitting is
  performed, rather than using Roe averages based on the cell from which the
  wave originates.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.7.1...v5.8.0>`_

Changes to amrclaw
------------------

- An additional short array is saved in a checkpoint file for use in a 
  restart.  Due to this change, a checkpoint file created using a previous
  version of Clawpack cannot be used for a restart with the new version.
  
- A `memsize` parameter can now be set in `setrun.py`, see above
  and :ref:`setrun_amrclaw`.
  
- `src/2d/prepc.f` was improved to use less storage from the
  work array `alloc` that is used for memory allocation for AMR patches.
  For large-scale problems this can be a substantial savings and allow
  running larger problems.
  


See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.7.1...v5.8.0>`_

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

- Changes to `riemann/src/rpt2_geoclaw.f90`.  These cause some change in 
  results but tests have shown the new results appear to be at least as 
  good as previous results and the code may be more stable in some
  situations.  For more detail see the "Changes to riemann" above.

- The new `flagregions` introduced in v5.7.0 (see :ref:`flagregions`)
  were not implemented properly in GeoClaw, and in some situations
  refinement to a `maxlevel` that was indicated only in `flagregion` was
  not allowed as expected. This is now fixed.

- In previous versions of GeoClaw one could implicitly define AMR flag
  regions that are aligned with the spatial extent of topo, dtopo, or qinit 
  files by specifying `minlevel, maxlevel` (and in the case of topo files, 
  a time interval `t1, t2`) when the file name is given.  This feature
  did not always work as advertised and was often confusing.   If these
  values are specified then they are now ignored, as explained in
  more detail in the following items.   Not that you may have to explicitly
  declare new flag regions now in order to have the expected refinement regions.

- When specifying topo files in `setrun.py` using the format::
    
    [topotype, minlevel, maxlevel, t1, t2, fname]

  the values `minlevel, maxlevel, t1, t2` will now be ignored.  
  To avoid warning messages, instead specify::

    [topotype, fname]

- When specifying dtopo files in `setrun.py` using the format::
    
    [topotype, minlevel, maxlevel, fname]

  the values `minlevel, maxlevel` will now be ignored.  
  To avoid warning messages, instead specify::

    [topotype, fname]

- When specifying qinit files in `setrun.py` using the format::
    
    [minlevel, maxlevel, fname]

  the values `minlevel, maxlevel` will now be ignored.  
  To avoid warning messages, instead specify::

    [fname]

- A `memsize` parameter can now be set in `setrun.py`, see above
  and :ref:`setrun_amrclaw`.

- An additional short array is saved in a checkpoint file for use in a 
  restart.  Due to this change, a checkpoint file created using a previous
  version of Clawpack cannot be used for a restart with the new version.
  
See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.7.1...v5.8.0>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.7.1...v5.8.0>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.7.1...v5.8.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.7.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.7.1...v5.8.0>`_

