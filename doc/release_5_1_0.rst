
.. _release_5_1_0:

==========================
Release 5.1.0
==========================


Clawpack 5.1.0 was released on March 2, 2014.  See :ref:`installing`.


Changes to classic
------------------

* None

See `classic diffs
<https://github.com/clawpack/classic/compare/aac8471ce97...master>`_

Changes to clawutil
-------------------

* Minor change for replacing a rundata object.  

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/55f81e395...master>`_

Changes to visclaw
------------------

* Replaced JSAnimation.IPython_display.py by improved version.

* Added an attribute to `data.py`.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/6669145d5bdf...master>`_

Changes to riemann
------------------

* Changes to multi-layer code -- do not attempt to compile  by default
  since LAPACK is required.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/7ef4a50f84c...master>`_

Changes to amrclaw
------------------

* Fixed the calling sequence where setaux is called two places in the
  regridding routines.  

* Several other minor fixes.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/0ad5e60a38d...master>`_

Changes to geoclaw
------------------

* Changed gauge output to avoid underflow in printing.

* Major change to the way moving topography (dtopo) is handled to correct
  problems observed with earlier versions of GeoClaw in which the moving
  topography was not always tracked properly.  A number of other
  improvements were also made to the way topography more generally is
  handled.  Some improvements:

    * Multiple dtopo files can be specified with overlapping time ranges and
      spatial extent.
    * Each dtopo file now results in the automatic creation of a topo array
      at the same resolution as the dtopo array that is updated before each
      time step so that it contains the proper topography plus dtopo.  
      These arrays remain after the dtopo stops moving and contain the final
      topography at the final time.  This avoids issues where dtopo might
      have been specified at much finer resolution than the topo files. (In
      earlier versions, the topo arrays were updated to incorporate the
      final topo+dtopo but only stored at the resolution of the original
      topo files.)
    * The routine for integrating the bilinear function defined by all
      topo arrays over a grid cell to compute `aux(1,i,j)`  has been improved 
      by making it a recursive function that can handle an arbitrary number
      of nested topo grids (including those created automatically from dtopo
      grids).  Previous versions died if there were more than 4 nested topo
      grids.

* Several changes to the `Makefile` for a GeoClaw run are required because
  of refactoring of this code.  You must:

    * Remove the line ::

         $(GEOLIB)/dtopo_module.f90 \

    * Replace the lines ::

          $(GEOLIB)/movetopo.f \
          $(GEOLIB)/cellgridintegrate.f \

      by ::

          $(GEOLIB)/topo_update.f90 \
          $(GEOLIB)/cellgridintegrate2.f \

      For an example, see the changes made to
      `$CLAW/geoclaw/examples/tsunami/chile2010/Makefile`,

  As always, you should do `make new` in your application directory
  after updating the version.

* A new parameter has been added that can be set in `setrun.py`::

    rundata.dtopo_data.dt_max_dtopo = 0.2

  for example will specify that the maximum time step allowed on the
  coarsest level is 0.2 seconds during the time when the topography is
  moving.  This avoids issues where the time step selected by the CFL
  condition is much larger than the time scale over which the topography
  changes.  You must also set `rundata.clawdata.dt_initial` to the same
  value (or smaller) to insure that the first time step is sufficiently small.


    

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/eefc8e4ff...master>`_

Changes to PyClaw
------------------


* Added 3d capabilities to SharpClaw.

* Many other minor fixes.

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/875a98eea...master>`_

