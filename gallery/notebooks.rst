
.. _notebooks:

Clawpack Gallery of Jupyter Notebooks
=====================================

The `Jupyter notebook <http://jupyter.org/>`_
(formerly known as IPython notebook)
is a very nice platform for illustrating Clawpack examples.

The links below will take you to static view of several notebooks
as html files.  You can also play animations in them and interact
with some plots, but to actually run the code yourself you should clone the 
apps repository.

**Version:** Most of these notebooks now work with Clawpack 5.7.0.

**Finding the notebooks:**  The links below are to html rendered versions of the
notebooks.  See the beginning of each notebook for information on where to find
the original `.ipynb` file.  Many of them are in the 
`apps repository <http://github.com/clawpack/apps>`__,
in some subdirectory of `$CLAW/apps/notebooks`.

If you have used Clawpack with the Jupyter notebook and would like to submit
your notebook for inclusion, please send us a link
or submit a 
`pull request to the apps repository <http://github.com/clawpack/apps/pulls>`__.


.. _notebooks_pyclaw:

Examples using PyClaw
------------------------------------

* :ref:`pyclaw/intro_notebook.ipynb`
* `A 2D fluid dynamics example <https://github.com/clawpack/apps/blob/master/notebooks/pyclaw/Quadrants.ipynb>`_
* `Stegotons: solitary waves arising in non-dispersive periodic media <https://github.com/clawpack/apps/blob/master/notebooks/pyclaw/Stegotons.ipynb>`_
* `Demonstration of different limiters for advection <http://nbviewer.ipython.org/gist/ketch/9508222>`_
* `PyClaw's Geometry tools <https://gist.github.com/ketch/1a7888d1fcc37209b260>`_
* `Solitary waves formed by diffraction of shallow water waves over a corrugated bottom <http://nbviewer.jupyter.org/gist/ketch/9250942>`_

.. _notebooks_classic:

Examples using Fortran Classic
------------------------------------


* `advection_1d <_static/apps/notebooks/classic/advection_1d/advection_1d.html>`_
  illustrating upwind, Lax-Wendroff, and limiter methods.
  From `$CLAW/apps/notebooks/classic/advection_1d.ipynb`.
  
* `acoustics_1d_example1 <_static/apps/notebooks/classic/acoustics_1d_example1/acoustics_1d_example1.html>`_.
  From `$CLAW/apps/notebooks/classic/acoustics_1d_example1.ipynb`.

.. _notebooks_amrclaw:

Examples using AMRClaw
------------------------------------


* `advection_2d <_static/apps/notebooks/amrclaw/advection_2d_square/amrclaw_advection_2d_square.html>`_

* `RuledRectangles <_static/apps/notebooks/amrclaw/RuledRectangles.html>`_
  Illustration of Ruled Rectangles from `clawpack.amrclaw.region_tools`. 

.. _notebooks_geoclaw:

Examples using GeoClaw
------------------------------------

* `topotools_examples <_static/apps/notebooks/geoclaw/topotools_examples.html>`_
  illustrates some of the tools from :ref:`topotools_module`.

* `dtopotools_examples <_static/apps/notebooks/geoclaw/dtopotools_examples.html>`_
  illustrates some of the tools from :ref:`dtopotools_module`.

* `Okada <_static/apps/notebooks/geoclaw/Okada.html>`_
  illustrates use of the Okada model for generating sea floor deformation.

* `CSZ_example <_static/apps/notebooks/geoclaw/dtopo_triangular/CSZ_example.html>`_
  illustrates use of the Okada model on triangles rather than
  rectangles, creating a dtopo file for a "random" Cascadia Subduction Zone event.

* `MarchingFront <_static/apps/notebooks/geoclaw/MarchingFront.html>`_
  illustrates a marching front algorithm that can be used to identify land
  behind dikes, and also useful for creating Ruled Rectangles for use as
  flagregions, or to select fgmax points below some fixed elevation.

* `ForceDry <_static/apps/notebooks/geoclaw/ForceDry.html>`_
  illustrates how to force some regions to be initialized as dry land even
  if they are below sea level (but protected by dikes).

* `MakeFlagregionsCoast <_static/apps/notebooks/geoclaw/MakeFlagregionsCoast.html>`_
  illustrates making a ruled rectangle for use as a flagregion using the
  marching front algorithm.

* `IslandBuffering <_static/apps/notebooks/geoclaw/IslandBuffering.html>`_
  illustrates how to make a ruled rectangle surrounding an island with
  a buffer zone that extends out some distance that is independent 
  of water depth.

.. _notebooks_tsunami-examples:

Tsunami modeling examples
-------------------------

Radial Ocean
^^^^^^^^^^^^

These notebooks are part of
`$CLAW/geoclaw/examples/tsunami/radial_ocean_island_fgmax
<_static/geoclaw/examples/tsunami/radial-ocean-island-fgmax/README.html>`__.

* `make_input_files <_static/geoclaw/examples/tsunami/radial-ocean-island-fgmax/make_input_files.html>`__
  creates input files.

* `process_fgmax <_static/geoclaw/examples/tsunami/radial-ocean-island-fgmax/process_fgmax.html>`__
  makes plots of fgmax results.


Chile 2010
^^^^^^^^^^^

* `chile2010a <_static/apps/notebooks/geoclaw/chile2010a/chile2010a.html>`_
  illustrates how to set up a basic GeoClaw run with adaptive refinement.

* `chile2010b <_static/apps/notebooks/geoclaw/chile2010b/chile2010b.html>`_
  illustrates setting regions and gauges.
  
Tohoku 2011
^^^^^^^^^^^^

* `compare_results <_static/apps/tsunami-examples/tohoku2011_hawaii_currents/compare_results.html>`_ 
  compares GeoClaw results to observations at a tide gauge and 
  ADCP current profiler in Hawaii.


.. _notebooks_tools:

Tools for running clawpack and visualizing results in notebooks
-----------------------------------------------------------------

Several of the notebooks above use the `clawpack.clawutil.nbtools
<https://github.com/clawpack/clawutil/blob/master/src/python/clawutil/nbtools.py>`__ module
of notebook tools to compile and run Fortran versions of Clawpack Classic,
AMRClaw, or GeoClaw, and display the plots and/or animations of the results
in the notebook.  For example, see 
  
* `amrclaw/advection_2d <_static/apps/notebooks/amrclaw/advection_2d_square/amrclaw_advection_2d_square.html>`__
* `chile2010a <_static/apps/notebooks/geoclaw/chile2010a/chile2010a.html>`__

The animations are presented with the aid of the 
  
* `clawpack.visclaw.animation_tools <https://github.com/clawpack/visclaw/blob/master/src/python/visclaw/animation_tools.py>`__ module. 

The notebook

* `animation tools demo <_static/apps/notebooks/visclaw/animation_tools_demo.html>`__

shows some other related animation tools.


.. _notebooks_vis:

Plotting and visualization
---------------------------

In addition to the notebooks referenced above, the following notebooks also
show how to use various plotting and visualization tools available in Clawpack:

* `pcolorcells <_static/apps/notebooks/visclaw/pcolorcells.html>`__
  A version of `pcolormesh` that works better for finite volume cell averaged
  data, also with an illustration of use in making kml overlays for Google Earth.
  
* `gridtools <_static/apps/notebooks/visclaw/gridtools.html>`__
  Tools to extract data from (so far only 2D) AMRClaw output, e.g. to 
  extract a uniform grid or a 1D transect that uses the finest available
  grid info at each point.

* `animation tools demo <_static/apps/notebooks/visclaw/animation_tools_demo.html>`__
  illustrates animation tools, including ways to create interactive
  animations using Jupyter widgets or as embedded or stand-alone javascript
  or mp4 files. (These tools may be useful for plots created outside of
  Clawpack as well.)

.. _notebooks_riemann:

Riemann solvers
------------------------------------

A collection of notebooks illustrating exact and approximate Riemann solvers
is available in the repository

- `<https://github.com/clawpack/riemann_book>`__

and visible as rendered html files at 

- `<http://www.clawpack.org/riemann_book/html/Index.html>`__

These were developed for the book `Riemann Problems and Jupyter Solutions
<https://bookstore.siam.org/fa16/bonus>`__ 
by D. I. Ketcheson, R. J. LeVeque, and M. J. del Razo.  
A paperback version was published by SIAM in 2020.


.. _notebooks_methods:

Illustration of numerical methods
------------------------------------

* `Advection Equation and the REA algorithm <http://nbviewer.ipython.org/github/maojrs/ipynotebooks/blob/master/advection_REA.ipynb>`_

