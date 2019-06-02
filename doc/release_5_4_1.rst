:orphan:


.. _release_5_4_1:

==========================
v5.4.1 release notes
==========================


Clawpack 5.4.1 was released on June 28, 2017.  See :ref:`installing`.

Changes relative to Clawpack 5.4.0 (February 17, 2017) are shown below.

Changes to documentation
------------------------

The documentation repository https://github.com/clawpack/doc has been refactored so that versioning is now supported.  On the menu to the left of the Clawpack documentation pages, at the bottom you should see links to select previous versions of the documentation, in particular `v5.4.0` and some earlier versions.  The `master` version points to the current master branch of the doc repository used to build the documentation.

If you switch to different version of a page, use the back button to return to the version for the current release, or click on the Clawpack logo to get back to this version.  If you click on the `master` version most things will work but links to gallery pages will not (due to the way relative paths are specified since inter-sphinx is now used for different projects in the main docs and the gallery).  Old versions of the gallery are not available.

Instructions for building the documentation have been updated in :ref:`howto_doc`.


Changes to classic
------------------

The Woodward-Collela blast wave problem for 1-dimensional Euler was added to the examples.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.4.0...v5.4.1>`_

Changes to clawutil
-------------------

Minor changes.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.4.0...v5.4.1>`_

Changes to visclaw
------------------

- Fixes for Python3 compatibility.  
- **There are still some known issues when making plots using Python3 that are being worked on.**  See e.g. https://github.com/clawpack/visclaw/pull/219.
- Improve KML functionality.
- Add `legend_tools` module to simplify adding a legend.
- Other minor fixes.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.4.0...v5.4.1>`_

Changes to riemann
------------------

- Added several Riemann solvers for new problems.
- Improved several existing solvers.
- The GeoClaw Riemann solver `riemann_aug_JCP` in `geoclaw_riemann_utils.f`
  has been modified to incorporate pressure source terms for storm surge
  simulations.  The calling sequence has changed.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.4.0...v5.4.1>`_

Changes to amrclaw
------------------

The major new addition is 1d `amrclaw` code in the `src/1d` directory and 
some examples in the `examples` directory. (Also regression tests in `tests`).
These examples have also been added to the gallery at `www.clawpack.org <http://www.clawpack.org>`_. 
This code was based on the `2d` code but reduced to a fully `1d` version that is better than the previous approach of using the `2d` code with only 1 cell in the `y` direction.  This code has not yet been extensively tested on challenging problems, so let us know if you run into problems with it.


- Cleanup some code related to timers.
- Fix a problem with integer overflows in some cases.
- Suppress printing Courant number every timestep to `fort.amr`
- Print more digits in gauge locations to output files `gauge*.txt`.
- The code in `$CLAW/amrclaw/src/2d` has had comments improved and added so that doxygen can be used, see :ref:`amrclaw_doxygen`.
- Other minor fixes.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.4.0...v5.4.1>`_

Changes to geoclaw
------------------


- Allow more flexibility in specification of `fgmax` grids when doing a restart.
- Print more digits in gauge locations to output files `gauge*.txt`.
- For storm surge, the pressure gradient source term has been moved to the 
  Riemann solver for well-balancing.  This may cause slightly different 
  results on these applications but should not affect others.
- The output and plotting functions for surge and multilayer versions been refactored.
- Other minor fixes and improvements of Python tools.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.4.0...v5.4.1>`_


Changes to PyClaw
------------------

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.4.0...v5.4.1>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.4.0...v5.4.1>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.4.0...v5.4.1>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.4.0...v5.4.1>`_

