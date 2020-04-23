:orphan:

.. _release_5_7_0:

===============================
v5.7.0 release notes
===============================

Clawpack 5.7.0 was released on April 23, 2020. See :ref:`installing`.

Permanent DOI:
`[DOI 10.5281/zenodo.3764201] <https://doi.org/10.5281/zenodo.3764201>`__.

Changes relative to Clawpack 5.6.1 (October 28, 2019) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Python support
---------------

As of v5.7.0 we are no longer supporting Python 2.7, and Python 3.x is
expected.  At this point we believe v5.7.0 still works with Python 2.7, but
we are phasing out testing this in the future.

See :ref:`python-three` for more information about this.


Changes that are not backward compatible
----------------------------------------

Some of the `.data` files generated from `setrun.py` have been changed in both
amrclaw and geoclaw, so if using these packages it is important to do::

    make new
    
to recompile all the code and::

    make data
    
to recreate `.data` files in the new form (the latter should happen 
automatically if you `make .output`, for example).

General changes
---------------

- Support for particle tracking via "Lagrangian gauges" has been added to
  `amrclaw`, but this capability itself has so far only been added to `geoclaw`,
  see below.  This has changed the format of `gauges.data` files generated 
  from `setrun.py`.
  
- A new way of specifying `flagregions` for guiding adaptive mesh refinement
  has been introduced in both `amrclaw` and `geoclaw`, and `RuledRectangles`
  have been introduced to assist in specifying non-rectangular `flagregions`.
  This has added a new `flagregions.data` file generated from `setrun.py`.

Changes to classic
------------------

None.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.6.1...v5.7.0>`_

Changes to clawutil
-------------------

- Support added for `flagregions` and `FlagRegionData`, see 
  `flagregions.html <http://depts.washington.edu/clawpack/sampledocs/sphinx-multiversion/dev/flagregions.html>`_.

- Support added for gzip/bzip2 unpacking in `get_remote_file`.

- Changes to `Makefile.common` to add `make notebook_htmls` target to turn
  Jupyter notebooks into html files using nbconvert, 
  and `make readme` to better handle converting `README.rst` into `README.html`.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.6.1...v5.7.0>`_

Changes to visclaw
------------------

- Several updates to Matlab tools.

- Added `particle_tools.py` for plotting particle paths when using Lagrangian gauges.

- Added `plottools.pcolorcells` to better plot data on finite volume grid cells.

- Improvements to how animations are made on html pages and other updates to 
  `animation_tools.py`.
  
- Improve colorbar options and better colorbars when using `colormaps.add_colormaps`.
 
- Change default behavior in `frametools.py` when looping over all patches: 
  skip those that lie outside of rectangle specified by `xlimits` and `ylimits`
  to improve speed.  Can over-ride this by setting 
  `plotaxes.skip_patches_outside_xylimits = False`.
  
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.6.1...v5.7.0>`_

Changes to riemann
------------------

- Updates to a few Riemann solvers 

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.6.1...v5.7.0>`_

Changes to amrclaw
------------------

- Allow setting `max1d` in `setrun.py`.

- Close output files properly in `valout.f90`

- Some support for Lagrangian gauges but not yet fully implemented
  except in geoclaw.
  
- Introduce new `flagregions` to replace `regions` eventually, see
  `flagregions.html <http://depts.washington.edu/clawpack/sampledocs/sphinx-multiversion/dev/flagregions.html>`_.
  
- New `region_tools.py` module with class `RuledRectangle` in particular,
  useful in specifying `flagregions`.  See
  `ruled_rectangles <http://depts.washington.edu/clawpack/sampledocs/sphinx-multiversion/dev/ruled_rectangles.html>`_.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.6.1...v5.7.0>`_

Changes to geoclaw
------------------

- Support for "Lagrangian gauges" that can be used for particle tracking
  to help visualize the flow.  See
  `lagrangian_gauges.html <http://depts.washington.edu/clawpack/sampledocs/sphinx-multiversion/dev/lagrangian_gauges.html>`_.
  
- Many changes to how fgmax grids are specified and handled.  The new code is
  much faster if there are lots of fgmax points (tested up to around 7 million).
  You can now specify points near the coastline up to some elevation much
  more easily for problems where you know higher ground will never be
  inundated.  Points can also be specifed using file specified with the same
  format as a topofile (with `topo_type==3`) with 0/1 values indicating which
  points are to be used as fgmax points. For more about all these changes, see
  `fgmax.html <http://depts.washington.edu/clawpack/sampledocs/sphinx-multiversion/dev/fgmax.html>`_.  Note that now a file `fgmax_grids.data` is generated from
  information in `setrun.py` rather than `fgmax.data`, with a different format.

- Improvements to `fgmax_tools.py` module.

- New routine `set_eta_init.f90` added that can be used to specify a spatially
  varying initial elevation `eta = B + h`.  The default version handles 
  subsidence or uplift specified in `dtopo` files.   See
  `set_eta_init <http://depts.washington.edu/clawpack/sampledocs/sphinx-multiversion/dev/set_eta_init.html>`_.
  
- Improvements to `kmltools.py` to facilitate making kml versions of plots,
  including `pcolorcells_for_kml` to make png files that align better,
  `fgmax2kml` for plotting fgmax results, and better support to plot
  polygonal outlines of flagregions that are RuledRectangles.
  
- New option added to allow specifying a `force_dry_init` array that indicates
  cells that should be forced to be dry (`h = 0`) when initialized, even if
  the topography elevation is below `sea_level`.  This allows better modeling
  of coastal regions where there is dry land below sea level but protected by
  dikes or levies.  See
  `force_dry.html <http://depts.washington.edu/clawpack/sampledocs/sphinx-multiversion/dev/force_dry.html>`_.
  
- New `marching_front.py` module with tools to identify dry land protected by
  dikes or to select fgmax points connected to the shore by land below some
  specified elevation.  See
  `marching_front.html <http://depts.washington.edu/clawpack/sampledocs/sphinx-multiversion/dev/marching_front.html>`_.
 
- Many other minor fixes and improvements.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.6.1...v5.7.0>`_


Changes to PyClaw
------------------

Mostly minor changes.

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.6.1...v5.7.0>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.6.1...v5.7.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.6.1...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.6.1...v5.7.0>`_

