
.. _geoplot:

========================================================
GeoClaw plotting tools
========================================================

**Needs updating**

The module `$CLAW/visclaw/geoplot.py` contains some useful tools for
plotting GeoClaw output.

To be continued.  See comments in the module.


Plotting water depth or surface elevation
-----------------------------------------

For information on using masked arrays, see:
 
 * `Masked array operations <http://docs.scipy.org/doc/numpy/reference/routines.ma.html>`_

Tips on latitude-longitude coordinate axes
-------------------------------------------

With the  default style, matplotlib axis labels are often hard to read when
plotting in latitude and longitude.  It may help to disable offset labeling
and to rotate the longitude labels::

    ticklabel_format(format='plain',useOffset=False)
    xticks(rotation=20)

To set the aspect ratio so that latitude and longitude are scaled
appropriately, set `mean_latitude` to some average latitude value in the
region of interest and then::

    gca().set_aspect(1./cos(mean_latitude*pi/180.))

