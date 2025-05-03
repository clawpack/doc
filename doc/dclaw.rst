.. _dclaw:

*****************************************************************
D-Claw for debris flows and landslides
*****************************************************************

The D-Claw code has been under development at the USGS for more than 10 years.
Originally it was branched off of Clawpack 4.x and evolved somewhat independently
of GeoClaw.  However, recently it has been substantially rewritten to be
compatible with recent versions of Clawpack 5.x and many of the new capabilities
introduced in GeoClaw such as :ref:`fgmax` and :ref:`fgout` are now available
in D-Claw as well.

Like GeoClaw, D-Claw solves 2-dimensional depth-averaged equations with the
fluid depth `h` and two depth-averaged momenta `hu,hv` as primary variables,
along with new
variables for the solid mass fraction and pore pressure.  It is based on
a model for dense granular flows described in detail in [IversonGeorge2014]_
and [GeorgeIverson2014]_.

For more information or to download the D-Claw code, see:

- `Documentation <https://claw.code-pages.usgs.gov/dclaw/>`_
- `USGS repository <https://code.usgs.gov/claw/dclaw>`_
- `Github mirror <https://github.com/geoflows/dclaw>`_
- `Some D-Claw research applications <https://dlgeorge.github.io/projects/>`_
