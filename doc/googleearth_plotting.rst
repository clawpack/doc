
.. _googleearth:

*******************************************
Creating plots for the Google Earth browser
*******************************************

.. _Google Earth: http://www.google.com/earth

The Google Earth browser is a powerful visualization tool
for viewing the output of geophysical simulations.  The VisClaw
visualization suite includes tools that will produce plots and
associated .kmz files needed for easy browsing of your data
in Google Earth.

Below is a guide for how to create Google Earth visualizations
of simulations produced by GeoClaw.  Of course, VisClaw will
allow you to visualize results of others types of simulations, but
the GeoClaw tsunami simulations are particularly appropriate for the
Google Earth platform in that both water and topography features
are important.

The Google Earth browser is not a fully functional GIS tool, and
so while the simulations may look very realistic, one
should not base critical decisions on conclusions drawn from the Google Earth
visualization alone.  Nevertheless, these realistic visualizations can be used
to communicate to non-experts important scientific information.

.. _google_earth_example:

An Example
----------

To see what you can do, first you will need to download the
`Google Earth`_ browser and download this example.

.. _google_earth_requirements:

Basic Requirements
------------------
To get started you will need to have the Python packages `lxml`_,
`pykml`_ and, optionally, `gdal`_.  The lxml package can be
easily installed through a Python package manager.  For example,
using the pip install package manager, you can use the commands::

  % pip install lxml
  % pip install pykml
  % pip install gdal

Other installation procedures, including those specific to Anaconda ("conda install") or
specific operating systems (OSX, Linux, Windows) should work as well.

You will also need to set the GDAL_DATA environment variable to the location
of the data files needed by the GDAL library.  Here are some examples of typical
library locations.  If you are unsure as to where the support files are located,
look for `gdal/gcs.cvs`.  This most likely is the proper location, so set GDAL_DATA
to the complete path to this directory.

* OSX


* Testing your GDAL installation

To make sure your GDAL installation is working properly, first download `this script`_
along with `this plot`_ (or just download the tar-ball `here`_) and run the
script from the command line::

  test_gdal % test_gdal.sh



.. _google_earth_basic_plotting:

Basic Plotting
--------------
To get started right away with a simple example, go to the Chile 2010
example in GeoClaw.


  plotfigure.kml_tile_images=False

in setplot.py.   This will generate the .kmz file that you can load

.. _google_earth_features:

Plotting Features
-----------------
Right away, you may have noticed that if you load the .kmz file created above
into Google Earth, the plots are very slow to load.  This is due in part to
limitations in Google Earth for visualizating large files over large regions.
Fortunately, we can easily break up the figures by tiling them in a hierarchy
of files that Google Earth will use to dynamically adjust the resolution of the
image depending on your zoom level.

Improving your visualization
----------------------------
There are several things you can adjust to improve your visualization.


**Increasing image resolution**

You may want to adjust the resolution of the PNG files that are produced.  This is especially true if you anticipate having several zoom levels.  To do this, set the plotfigure attribute `kml_dpi` (dots-per-inch) to a  suitable high resolution::

  plotfigure.kml_dpi = 1600

Be aware that setting the resolution to higher values can slow down both the creation of the PNG
file as well as the tiling of the image.  High resolution untiled images will most likely not load
in Google Earth.

**Setting the time slider start time**

The time values in the time slider can be set to reflect the timing of a particular event (a
tsunami, for example).  Again, in `setplot.py`, you can set the start time of an event (in
UTC time coordinates) and an time zone offset to reflect the local time of the event.  For
example, the Tohoku tsunami took place March 11, 2010, at 5:46 UTC::

  plotfigure.kml_starttime = [2011,3,11,5,46,0]  # [year, month, day, hours, minutes,seconds]
  plotfigure.kml_tz_offset = 9    # 9 hours again of UTC

**Choosing colormaps**

There are several choices of colormaps, some which may be better suited to the
geographical location of your visualization than others. For example, to visualize tsunami flow
across the ocean, you may want to have the undisturbed portion of your simulated results match
the ocean color in Google Earth as closely as possible.  In this case, set::

  plotitem.pcolor_cmap = geoplot.googleearth_darkblue

If you would like the undisturbed sea surface to be transparent, set::

  plotitem.pcolor_cmap = geoplot.googleearth_transparent


Gallery
-------

.. image:: images/googleearth_tohoku.pdf

Trouble Shooting
----------------
