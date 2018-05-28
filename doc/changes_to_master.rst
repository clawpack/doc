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

 - Minor changes to Matlab codes 
 - Minor changes to kml functionality
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.4.1...master>`_

Changes to riemann
------------------

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.4.1...master>`_

Changes to amrclaw
------------------
- The maximum number of allowable refined grids is now
  variable, and no longer static. If the current maximum
  is exceeded, all arrays dimension at maxgr, namely
  rnode, node, and listOfGrids (currently set
  to 10000) are resized by another 10K.
  bndList is also now resizable.

- Makefile.amr_2d changed to include the new files to initialize,
  restart, and resize the nodal arrays and boundary lists.

- The gauges had one some variable that depended
  on maxgr. By changing the gauges algorithm, this was
  eliminated. The old algorithm did not scale well for
  O(10^5) grids and O(100) gauges. The new algorithm just
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

- The geoclaw versions for checkpointing and restarting also had
to change to write out maxgr, and call the allocate routines for
the arrays that depend on maxgr. (see amrclaw changes)

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

