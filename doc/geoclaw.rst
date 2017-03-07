.. _geoclaw:

***************
GeoClaw
***************

See `www.geoclaw.org <http://www.geoclaw.org>`_ for more overview of the
GeoClaw software and links to references and uses.

.. warning:: As with all of Clawpack, this code is provided as a research
   and teaching tool with no guarantee of suitability for any particular
   purpose, and no liability on the part of the authors.  See the
   :ref:`license` for more details and :ref:`geohints` for tips on
   exercising appropriate care in using the code.

The `$CLAW/geoclaw` directory contains a specialized version of some Clawpack
and AMRClaw routines that have been modified to work well for certain
geophysical flow problems.  

Currently the focus is on 2d depth-averaged
shallow water equations for flow over varying topography.  The term
*bathymetry* is often used for underwater topography (sea floor or lake
bottom), but in this documentation and in the code the term *topography* is
often used to refer to either.

A primary concern with such flows is handling the margins of the flow where
the depth goes to 0, for example at the shore line.  In GeoClaw this is
handled by letting the depth variable *h* in the shallow water equations be
0 in some cells.  Robust Riemann solvers are used that allow for dry cells
adjacent to wet cells and that allow wetting and drying, for example as a
tsunami inundates dry land.

Some sample calculations can be viewed in the :ref:`gallery_geoclaw`.
More will eventually appear in the :ref:`apps`.

.. toctree::
   :maxdepth: 2

   geoclaw_started
   geohints
   topo
   topotools
   setrun_geoclaw
   plotting_geoclaw
   googleearth_plotting
   quick_tsunami
   okada
   sealevel
   manning
   fgout
   fgmax
   tsunamidata

* `Links <http://depts.washington.edu/clawpack/geoclaw/>`_
  to relevant papers and sample codes (some are based on the Clawpack 4.x
  version of GeoClaw).
