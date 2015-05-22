
.. comment: Change version numbers and DATE.

.. _release_5_3_0:

==========================
Release 5.3.0
==========================

Clawpack 5.3.0 was released on May 21, 2015.  See :ref:`installing`.

Changes relative to Clawpack 5.2.2 (October 28, 2014) are shown below.

Changes to classic
------------------

* One example added with a pointwise Riemann solver.

See `classic diffs <https://github.com/clawpack/classic/compare/v5.2.2...v5.3.0>`_

Changes to clawutil
-------------------

* Added `nbtools.py` module for working with Jupyter (formerly IPython)
  notebooks (still work in progress).

* Added ability to correctly call alternative Makefiles, e.g. ::

    make .plots -f Makefile_kml

* Added support for preprocessing variables and flags

* Added support for storm surge code

See `clawutil diffs <https://github.com/clawpack/clawutil/compare/v5.2.2...v5.3.0>`_

Changes to visclaw
------------------

* Added support for creating `kml` files that can be viewed on Google Earth
  (for GeoClaw applications).  See :ref:`googleearth_plotting`.

* Added some support for JSAnimation in notebooks and other improvements, in
  particular to insure that filenames do not have extraneous spaces and fail
  to show up in animation.

* Added support for ForestClaw

* Added function `gaugetools.compare_gauges` and support for gauges in 3d.

* Deprecate `plot_topo_file` and `TopoPlotData` in favor of
  `topotools.Topography` methods.

* Some refactoring and cleaning up of code, and minor bug fixes.

 
See `visclaw diffs <https://github.com/clawpack/visclaw/compare/v5.2.2...v5.3.0>`_

Changes to riemann
------------------

* Added 3d Euler equations in general geometries using f-waves.

* Added 2d acoustics solvers for mapped grids.

* Added some pointwise Riemann solvers for several problems in 1d and 2d.

* Added `riemann_tools.py` and other code to facilitate showing Riemann
  solutions in notebooks.   Still work in progress.

See `riemann diffs <https://github.com/clawpack/riemann/compare/v5.2.2...v5.3.0>`_

Changes to amrclaw
------------------

* Substantial refactoring of code, much of which should be invisible to 
  users.  

* Some changes are required in any application `Makefile` to 
  update from 5.2.2 to 5.3.0.

  - In 2d, remove::

        $(AMRLIB)/dumpgauge.f \

  - In 2d, add the files::

          $(AMRLIB)/stepgrid_dimSplit.f \
          $(AMRLIB)/step2x.f90 \
          $(AMRLIB)/step2y.f90 \
          $(AMRLIB)/flux2_dimSplit.f \

  - In 3d, add the MODULE::

          $(AMRLIB)/gauges_module.f90

    somewhere **after** `$(AMRLIB)/amr_module.f90` in the list of modules.

  - In 3d, add the files::

          $(AMRLIB)/stepgrid_dimSplit.f \
          $(AMRLIB)/step3x.f \
          $(AMRLIB)/step3y.f \
          $(AMRLIB)/step3z.f \
          $(AMRLIB)/flux3_dimSplit.f \

  Here `AMRLIB = $(CLAW)/amrclaw/src/2d` in 2d, for example

* Gauge output refactored.

* Gauge output option added to 3d code. For an example, see
  `$CLAW/amrclaw/examples/advection_3d_swirl/setrun.py`

* Dimensional splitting option added to both 2d and 3d code. To use, in 
  `setrun.py` set `clawdata.dimensional_split` to `"split"` or `1`.

* New approach to handling boundary conditions to fix bug where 
  boundary conditions varying spatially along a boundary could not be specified.
  Illustrated in new `examples/advection_2d_inflow`.

* `alloc` changed from pointer to allocatable, `igetsp` stack-based, 

* Several bug fixes, particularly in 3d code.

See `amrclaw diffs <https://github.com/clawpack/amrclaw/compare/v5.2.2...v5.3.0>`_

Changes to geoclaw
------------------

* Some changes are required in any application `Makefile` to 
  update from 5.2.2 to 5.3.0.

  - add the MODULEs::

         $(GEOLIB)/gauges_module.f90 \
         $(GEOLIB)/surge/holland_storm_module.f90 \
         $(GEOLIB)/surge/stommel_storm_module.f90 \
         $(GEOLIB)/surge/constant_storm_module.f90 \
         $(GEOLIB)/surge/storm_module.f90 \
         $(GEOLIB)/friction_module.f90

  - remove the MODULE::

         $(AMRLIB)/gauges_module.f90 \

  - remove the file::

         $(GEOLIB)/dumpgauge.f \

  Here `GEOLIB = $(CLAW)/geoclaw/src/2d/shallow`.

  Note that `$(GEOLIB)/gauges_module.f90` must come **after** both
  ` $(AMRLIB)/amr_module.f90` and
  `$(GEOLIB)/geoclaw_module.f90` in the list of modules.

* Gauge output refactored as in `amrclaw`.  Note it is now necessary to use
  the version of `gauges_module.f90` in `geoclaw` rather than the version from 
  `amrclaw` since the subroutine for printing the gauges is now in this module
  rather than in `dumpgauge.f`.  In `geoclaw`, an additional column is 
  printed for `eta = B + h`, the sea surface, in addition to the 
  components of `q`.

* Multilayer code merged in and several routines refactored or consolidated.

* New support added for creating `kml` files for plotting results on Google
  Earth.

* Topography `topo_type` 2 and 3 are now more flexible: 

  - The header lines can have either the number or the text first, e.g. ::

        NCOLS 200

    or ::

        200 NCOLS

    (In either case the label is ignored, the order of lines is all that
    matters).   Both Python and Fortran codes now support this.

  - The header line for the cellsize `dx` can now have a single value
    or two values `dx` and `dy` for different resolutions in longitude and
    latitude.  Previously a single value was allowed and `dx == dy` assumed.

* Added support for creating `kml` files that can be viewed on Google Earth
  (for GeoClaw applications).  See :ref:`googleearth_plotting`.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.2.2...v5.3.0>`_

Changes to PyClaw
------------------

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/v5.3.0/CHANGES.md>`_.

See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.2.2...v5.3.0>`_

