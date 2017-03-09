.. _geoclaw_started:

Getting started with GeoClaw
============================

.. _geoclaw_run:

Running a GeoClaw code
----------------------

Setting up, running, and plotting a GeoClaw application follows the same pattern
as other AMRClaw applications, which in turn use many of the same
conventions as the classic single grid Clawpack code, in particular:

 * Setting parameters is done in `setrun.py`, as for other versions
   of Clawpack, as described in :ref:`setrun`.  However, there are several
   new parameters that may or must be set for GeoClaw.  See
   :ref:`setrun_geoclaw` for more details on these.

 * The program can be compiled and run using *make* and *make .output* as
   for other versions, see :ref:`fortran`.

 * Plots of results can be created either as a set of webpages via
   *make .plots* or interactively using *Iplotclaw*.  See
   :ref:`plotting` for more details.  Some additional Python plotting tools 
   that are useful for GeoClaw output (e.g. plotting land and water with
   different colormaps) are described in the section
   :ref:`plotting_geoclaw`.


.. _topo_intro:

Topography
----------

To simulate  flow over topography it is of course necessary to specify 
the topography.  This is usually done by providing one or more files of
surface elevation (relative to some reference, e.g. sea level) at a set of
points on a rectangular grid (with x-y locations in Cartesian units or in
latitude-longitude, depending on the application).

Several file formats are recognized by GeoClaw.  See :ref:`topo` for more
information on how to specify topography and some on-line resources for
obtaining topography.

.. _geoclaw_plotting:

Plotting GeoClaw results
------------------------

GeoClaw results can be plotted with the usual Python plotting tools (see
:ref:`plotting`).  

Some special tools and colormaps are available, see :ref:`geoplot`.

Setting up a new example
------------------------

 * :ref:`quick_tsunami`

