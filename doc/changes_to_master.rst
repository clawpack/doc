:orphan:

.. _changes_to_master:

===============================
Changes to master since v5.4.1
===============================


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.4.1) on February 17, 2017.

These changes should appear in the next release.  If you need them now,
see :ref:`developers` for instructions on cloning and installing from the
master branch. 

Changes that are not backward compatible
----------------------------------------

- The format of checkpoint styles has changed for AMRClaw and GeoClaw, so old
  checkpoint files can not be used to restart with newer code.

- In GeoClaw, the way some topofiles are interpreted has been changed to conform with 
  the intended "grid registration".
  This is not backward compatable for files with headers that specify
  `xllower, yllower`.  See below for more details.


General changes
---------------

 - `LICENSE` file added to all repositories, with BSD license

Changes to classic
------------------

 - None other than addition of License.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.4.1...master>`_

Changes to clawutil
-------------------

 - Minor changes

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.4.1...master>`_

Changes to visclaw
------------------

 - The script `src/python/visclaw/plot_timing_stats.py` 
   can be used to plot timing data that is now printed out following
   AMRClaw and GeoClaw runs.  See the AMRClaw notes below for more details.
 - Minor changes to Matlab codes 
 - Minor changes to kml functionality, and printing of more digits
 - `ClawPlotItem.colorbar_kwargs` added for setting other colorbar keyword
   arguments
 - `ClawPlotAxes.beforeframe` added to allow e.g. plotting on a background
   image, see `PR #226 <https://github.com/clawpack/visclaw/pull/226>`_ for an
   example.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.4.1...master>`_

Changes to riemann
------------------

 - Add some vectorized Riemann solvers
 - Changes to layered shallow water solvers
 - Add some Riemann solvers for adjoint equations

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.4.1...master>`_

Changes to amrclaw
------------------

- The `valout.f` routine in `amrclaw/src/Nd` (for `N=1,2,3`)
  has been cleaned up as `valout.f90`, and now also prints out timing
  information to two files in the output directory: `timing.txt` contains a
  summary at the end of the run, while `timing.csv` contains cumulative timing
  information at each output time.  

- The boundary condition routines `amrclaw/src/Nd/bcNamr.f`  (for `N=1,2,3`)
  have been replaced with modernized versions `amrclaw/src/Nd/bcNamr.f90` 
  that should be easier to read and modify by users if necessary.
  
- The script `$CLAW/visclaw/src/python/visclaw/plot_timing_stats.py` 
  can be used to plot this data (or modify this script as desired).
  Information on both wall time and CPU time is
  included, particularly useful for multi-core simulations.

- Write more digits in `regions.data` file.

- Clean up some timing variables.

- The maximum number of allowable refined grids is now
  variable, and no longer static. If the current maximum
  is exceeded, all arrays dimension at `maxgr`, namely
  `rnode`, `node`, and `listOfGrids` (currently set
  to 10000) are resized by another 10K.
  `bndList` is also now resizable.

- The format of checkpoint files changed to include `maxgr`.
  **This is not backward compatible -- old checkpoint files can not be used
  to restart with the new code.**

- `Makefile.amr_2d` changed to include the new files to initialize,
  restart, and resize the nodal arrays and boundary lists.

- The gauges had one some variable that depended
  on `maxgr`. By changing the gauges algorithm, this was
  eliminated. The old algorithm did not scale well for
  `O(10^5)` grids and `O(100)` gauges. The new algorithm just
  has each grid patch sort the gauge list to see if it has any
  gauges to update. (The old algorithm sorted all grid owners and
  their owner gauges, (thus needing to save that mapping), and
  therefore was  an index lookup by grid number. But again, 10^5
  grids needing 2 arrays for only 100 gauges did not make sense.
  Also changed the algorithm for finding the best source grid for a
  gauge. By starting at the finest level, and rearranging the order
  of the loops, once a grid owner was found for a gauge there was no
  need to search the rest of the grids.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.4.1...master>`_

Changes to geoclaw
------------------
- Makefile.geoclaw changed to include the new files to initialize,
  restart, and resize the nodal arrays and boundary lists.

- The way some topofiles are interpreted has been changed to conform with 
  the intended "grid registration".  In particular, topofiles with a header 
  containing `xllower` and `yllower` contain data that should be viewed as
  cell-centered data on a uniform grid that starts at 
  `(xllower + dx/2, yllower + dy/2)` and not at `(xllower, yllower)`.
  See `PR #303 <https://github.com/clawpack/geoclaw/pull/303>`_ for more 
  discussion and :ref:`grid_registration` for documentation.
  **This is not backward compatable for files with these headers.**
  Change the header to specify `xlower` and `ylower` (or `xllcenter,
  yllcenter`) if you want the data to be interpreted in the old manner.
  
- The boundary condition routine `geoclaw/src/2d/shallow/bc2amr.f` 
  have been replaced with a modernized version `geoclaw/src/2d/shallow/bc2amr.f`
  that should be easier to read and modify by users if necessary.
  (Similar to changes made in amrclaw.)
    
- The format of checkpoint files changed to include `maxgr`.
  **This is not backward compatible -- old checkpoint files can not be used
  to restart with the new code.**

- The `valout.f` routine in `src/2d/shallow`
  has been cleaned up as `valout.f90`, and now also prints out timing
  information to two files in the output directory.  See the notes
  for amrclaw above for more details.

- Many updates have been made to the storm surge code.
  **@mandli should update this section.**
  
- Multi-layer shallow water solvers have been extended to work with AMR.
  (This is still under development and may have some bugs.)

- Makefile.geoclaw changed to include the new files to initialize,
  restart, and resize the nodal arrays and boundary lists.

- New capabilities have been added to read topofiles in netCDF, and also to
  download topo DEMs from `.nc` files at remote URLs.  This allows downloading
  only a subset of the DEM and at a coarsened resolution.
  See `topotools.read_netcdf` in :ref:`topotools_module`,
  and `tests/test_etopo1.py` for an example of usage.
  *More documentation needed.*

- The `etopotools.py` module has been deprecated in favor of the 
  `topotools.read_netcdf` function, which can be called with 
  `path = 'etopo1` to read from the online etopo1 database in netCDF format.
  This allows downloading only a subset of the DEM and at a coarsened resolution.
  The old way of doing this is not robust and sometimes gave incorrect results
  due to issues with the old etopo1 server (which is no longer maintained).
  See :ref:`topo_netcdf` and 
  `PR #308 <https://github.com/clawpack/geoclaw/pull/308>`_.
  An example can be found in `tests/test_etopo1.py`.

- More generally, topofiles can now be read in from netCDF files either
  locally or from the web.  See :ref:`topo_netcdf` for some documentation.

- New capabilities have been added to download NOAA tide gauge data, see
  `PR #287 <https://github.com/clawpack/geoclaw/pull/287>`_.

- Some plotting issues have been resolved.

- `dtopotools.SiftFault` now has the rigidity `mu` set properly, which
  changes the magnitude `Mw` that is reported for a fault created using
  the NOAA SIFT database.

- `dtopotools.SubFault` has been extended to allow triangular subfaults
  in addition to rectangular subfaults.  Some examples illustrating this
  should be added to the `apps` repository.

- `topotools.read` now allows `dx != dy` in a header for `topo_type in [2,3]`.

- Many other minor changes.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.4.1...master>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.4.1...master>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.4.1...master>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.4.1...master>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.4.1...master>`_

