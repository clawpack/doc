
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

Gallery
-------

.. image:: images/googleearth_tohoku.pdf

Trouble Shooting
----------------
