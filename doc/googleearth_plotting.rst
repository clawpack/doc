
.. _googleearth:

*******************************************
Creating plots for the Google Earth browser
*******************************************

.. _Google Earth: http://www.google.com/earth

The Google Earth browser is a powerful visualization tool for viewing
the output of geophysical simulations.  The VisClaw visualization
suite includes tools that will produce plots and associated .kmz files
needed for easy browsing of your data in Google Earth.

Below is a guide for how to create Google Earth visualizations of
simulations produced by GeoClaw.  Of course, the VisClaw visualization
tools for Google Earth will allow you to visualize results of others
types of simulations, but the GeoClaw tsunami simulations are
particularly appropriate for the Google Earth platform in that land
topography, ocean bathymetry and wave disturbances created by tsunamis
or other innundation events can all be viewed simultaneously.

The Google Earth browser is not a fully functional GIS tool, and so
while the simulations may look very realistic, one should not base
critical decisions on conclusions drawn from the Google Earth
visualization alone.  Nevertheless, these realistic visualizations are
useful for setting up simulations, getting simulation can be used to
communicate to non-experts important scientific information.

.. _google_earth_requirements:

Basic requirements
==================

.. _lxml: http://pypi.python.org/pypi/lxml/3.4.0
.. _GDAL: http://www.gdal.org
.. _pykml: http://pythonhosted.org/pykml/

To get started,  you will need the required Python packages `lxml`_ and
`pykml`_.  These libraries can be easily installed through Python
package managers *PIP* and *conda*::

  % conda install lxml   # PIP may also work
  % pip install pykml    # Not available through conda

.. _Optional library:

Optional GDAL library
---------------------
To create a pyramid of images that will load faster in Google Earth, you may also want to install
the Geospatial Data Abstraction Library (`GDAL`_).    This can be most easily installed with *conda*::

  % conda install gdal

For OSX, the GDAL library can also be installed through MacPorts or Homebrew.

You will also need to set an environment
variable 'GDAL_DATA' to point to the directory containing the projection files.
For example, in Anaconda Python, these are installed under the `share/gdal` directory,
and so you can set (in bash) the environment variable as::

    export GDAL_DATA=$ANACONDA/share/gdal

Routines from this library are called if you indicate that you'd like to tile your images.  See
`Tiling images for faster loading`_.

.. _google_earth_example:

An example : The Chile 2010 tsunami event
=========================================

.. _Chile_2010.kml: http://math.boisestate.edu/~calhoun/visclaw/GoogleEarth/kml/Chile_2010.kml

Simulations of the Chile 2010 earthquake and tsunami are included as
an example in the GeoClaw module of Clawpack.  Once you have run this
simulation and created output files in an *_output* directory, you can create a
Google Earth KMZ file with the command::

  % make plots "SETPLOT_FILE=setplot_kml.py"

This runs the commands in *setplot_kml.py*. The resulting archive file
*Chile_2010.kmz* (created in your plots directory) can be opened in
Google Earth.

An on-line version of results from this example can be viewed by
opening the file `Chile_2010.kml`_ in Google Earth.

.. figure::  images/GE_Chile.png
   :scale: 50%
   :align: center

   Simulation of the Chile 2010 tsunami (see geoclaw/examples/tsunami/chile2010).

.. _google_earth_basic_plotting:

Plotting attributes needed for Google Earth
-------------------------------------------

The plotting parameters needed to instruct VisClaw to create plots
suitable for visualization in Google Earth are all set through VisClaw
*plotfigure* and *plotdata* plotting objects.

To describe these attributes, we will go through each setting in the
Chile 2010 example.  These attributes can all be found in the
**setplot_kml.py** file for that example.

plotdata attributes
-------------------

The following *plotdata* attributes apply to all VisClaw figures to be
visualized in Google Earth.  These attributes are all *optional* and
have reasonable default values.

.. code-block:: python

  #-----------------------------------------
  # plotdata attributes for KML
  #-----------------------------------------
  plotdata.kml_name = "Chile 2010"
  plotdata.kml_starttime = [2010,2,27,6,34,0]  # Time of event in UTC [None]
  plotdata.kml_tz_offset = 3    # Time zone offset (in hours) of event. [None]

  plotdata.kml_index_fname = "Chile_2010"  # name for .kmz and .kml files ["_GoogleEarth"]

  # Set to a URL where KMZ file will be published.
  # plotdata.kml_publish = None

.. attribute:: kml_name : string

  Name used in the Google Earth sidebar to identify the simulation. Default : "GeoClaw"

.. attribute:: kml_starttime : [Y,M,D,H,M,S]

  Start time and date, in UTC,  of the event.  The format is *[year,month,day,hour, minute, second]*.
  By default, local time will be used.

.. attribute:: kml_timezone : integer

  Time zone offset, in hours, from UTC.  For example, the offset for Chile is +3 hours,
  whereas the offset for Japan is -9 hours.   Default : no time zone offset.

.. attribute:: kml_index_fname : string

  The name given to the KMZ file created in the plot directory.  Default : "_GoogleEarth"

.. attribute:: kml_publish : string

  A URL address for the server hosting a KMZ file you wish to make available on-line.   See
  `Publishing your results`_.


plotfigure attributes
---------------------

The following attributes apply to an individual figure created for visualization in Google Earth.
The first three attributes are **required**.  The rest are optional.

.. code-block:: python

  #-----------------------------------------------------------
  # Figure - Sea Surface
  #----------------------------------------------------------
  plotfigure = plotdata.new_plotfigure(name='Sea Surface',figno=1)
  plotfigure.show = True

  # Required KML attributes for visualization in Google Earth
  plotfigure.use_for_kml = True
  plotfigure.kml_xlimits = [-120,-60]    # Longitude
  plotfigure.kml_ylimits = [-60, 0.0]    # Latitude

  # Optional attributes
  plotfigure.kml_use_for_initial_view = True
  plotfigure.kml_figsize = [30.0,30.0]
  plotfigure.kml_dpi = 12         # Resolve all three levels
  plotfigure.kml_tile_images = False    # Tile images for faster loading.  Requires GDAL [False]

.. attribute:: use_for_kml : boolean

  Indicates to VisClaw that the PNG file created for this figure should be suitable for
  visualization in Google Earth. With this set to `True`, all titles, axes labels, colorbars
  and tick marks will be suppressed.  Default : `False`.

.. attribute:: kml_xlimits : [longitude_min, longitude_max]

  Longitude range used to place PNG figure on Google Earth. *This setting will override
  any limits set as `plotaxes` attributes*.  **Required**

.. attribute:: kml_ylimits : [latitude_min, latitude_max]

  Latitude range used to place the PNG figure on Google Earth.
  *This setting will override any limits set as `plotaxes` attributes*.  **Required**

.. attribute:: kml_use_for_initial_view : boolean

  Set to `True` if this figure should be used to determine the initial
  camera position in Google Earth.  The initial camera position will
  be centered over this figure, and at an elevation equal to
  approximately twice the width of the figure, in meters.  By default, the first figure
  created will be used to set the initial view.

.. attribute:: kml_figsize :  [size_x_inches,size_y_inches]

   Set the figure size, in inches, for the PNG file.  See `Removing aliasing artifacts`_ for
   tips on how to set the figure size and dpi for best results.  Default : chosen by Matplotlib.

.. attribute:: kml_dpi : integer

  dots-per-inch used in rendering PNG figures.  This should be consistent with the `figsize`
  set above, and the refinement factors.
  See `Removing aliasing artifacts`_ below for more details on how to improve the PNG rendering
  figures.  Default : 200.

.. attribute:: kml_tile_images : boolean

  Set to `True` if you want to create a *pyramid* of images for faster loading in Google Earth.
  *This require the GDAL library*.   Default : False.

Creating the figures
--------------------

All figures created for Google Earth are rendered as PNG files using
the Matplotlib backend.  So in this sense, the resulting PNG files are
created in a manner that is no different from other VisClaw output
formats.  Furthermore, there are no special plotaxes or plotitems
attributes to set for KML figures.  But several attriubutes will either
be ignored by the KML output or should  be suppressed for best results
in Google Earth.

.. code-block:: python

  # Create the figure
  plotaxes = plotfigure.new_plotaxes('kml')

  plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
  plotitem.plot_var = geoplot.surface_or_depth
  plotitem.cmin = -0.2
  plotitem.cmap = 0.2
  plotitem.pcolor_cmap = googleearth_transparent

  def kml_colorbar(filename):
    cmin = -0.2
    cmax = 0.2
    cmap = geoplot.googleearth_transparent
    geoplot.kml_build_colorbar(filename,cmap,cmin,cmax)

  plotfigure.kml_colorbar = kml_colorbar


plotaxes attributes
^^^^^^^^^^^^^^^^^^^

The plotaxes attributes
`colorbar`, `xlimits`, `ylimits` and `title` will all be ignored by the KML plotting.
For best results, the attribute `scaled` should be set to its default value `False`.  The
only plotaxes attribute that might be useful in some limited contexts is the `afteraxes`
setting, and only if the `afteraxes` function does not add plot features that cause
Matplotlib to alter the space occupied by the figure.   In most cases, the `afteraxes`
commands should not be needed or should not be used.

plotitem attributes
^^^^^^^^^^^^^^^^^^^

The most useful `plotitem` type will probably be the `2d_pcolor` type, although other
types including the filled contour `contourf` can also be used to good effect.
The transparent
colormap is particularly appealing visually when overlaid onto the Google Earth ocean
bathymetry.  This colormap is the `geoplot.googleearth_transparent` colormap, available
in the geoplot module.   Other colormaps that are designed to work well with the Google Earth
browser backdrop are the `googleearth_lightblue` and `googleearth_darkblue` colormaps. These
are solid colormaps, with the zero sea surface level set to colors which match those of the
ocean bathymetry.

Adding a colorbar overlay
^^^^^^^^^^^^^^^^^^^^^^^^^

A colorbar can be associated with each figure in the Google Earth
browser by setting the figure attribute `colorbar`. The color axis
range `[cmin, cmax]` and the colormap `cmap` should be consistent with
those set as plotitem attributes.

Gauges and miscellaneous settings
---------------------------------

There are no particular attributes for gauge plots and so they
can be created in the usual way.  In the Google Earth browser, gauge locations
will be displayed as Placemarks.  Clicking on gauge Placemarks will bring
up the individual gauge plots.  The screenshot below shows the gauge plot
that appears when either the gauge Placemark or the gauge label in the sidebar is
clicked.


.. figure::  images/GE_screenshot.png
   :scale: 20%
   :align: center

   Screenshot illustrating gauge plots.

Additional plotdata attributes
------------------------------

VisClaw has additional plotdata attributes indicating which figures and frames
to plot, and which output style to create.  When plotting for Google
Earth, one additional output parameter is necessary.


.. code-block:: python

  #-----------------------------------------
  plotdata.print_format = 'png'      # file format
  plotdata.print_framenos = 'all'    # list of frames to print
  plotdata.print_fignos = 'all'      # list of figures to print
  plotdata.html = False              # create html files of plots?
  plotdata.latex = False             # create latex file of plots?
  # ....
  plotdata.kml = True                # Create a KML/KMZ file


.. attribute:: kml : boolean

   Set to `True` to indicate that a KML/KMZ file should be created. Default : False.

Plotting tips
=============
Below are tips for creating zoomed images,  improving the quality of your images and publishing your
results.

Creating multiple figures at different resolutions
--------------------------------------------------
You can create several figures for visualization in Google Earth.  Each figure you create will show
up in a separate folder in the Google Earth sidebar.  For at least one figure, you will probably want
to set the `kml_xlimits` and `kml_ylimits` to match the computational domain.

To get higher resolution zoomed in figures, you will want to restrict
the x- and y-limits to a smaller region.  For best results, these zoom
regions should be consistent with the resolution of your simulation.
For example, to create a zoomed in figure that contains only
refinement levels 3 and 4, set x- and y-limits that contain an integer
number of grids cells at level 3.  See `Removing aliasing artifacts`_
for more details on how to set the zoom levels.


.. _Creating an image pyramid:

Tiling images for faster loading
--------------------------------

If you create several frames with relatively high dpi, you many find that the resulting
KMZ file is slow to load in Google Earth.  In extreme cases, large PNG files will not load
at all.  You can improve Google Earth performance by creating an image hierarchy which
loads only a low resolution sampling of the data at low zoom levels and  higher resolution
images close-up views.  In VisClaw, this image pyramid can be set by
setting the plotfigure attribute `kml_tile_images` to `True`.

.. code-block:: python

   plotfigure.kml_tile_images = True

**Note:** This requires the GDAL library, which can be installed following the
`Optional GDAL library`_ instructions, above.

.. _Enhancing the resolution:

Removing aliasing artifacts
---------------------------

You may find that the transparent colormap leads to unappealing visual
artifacts.  This can happen when the resolution of the plot does not
match the resolution of the data used to create the plot.  For
example, in the Chile example, the number of grid cells on the
coarsest level is 30 in each direction.  The default settings for the
figure size (`kml_figsize`) and dpi (`kml_dpi`), however, result in a
figure with a noticable plaid pattern.

.. figure::  images/GE_aliased.png
   :scale: 50%
   :align: center

   Aliasing effects resulting from default `kml_dpi` and `kml_figsize` settings

This can be corrected by matching the resolution to the resolution of
the AMR grid hierarchy.  The coarsest level grid in the Chile example
is 30x30.  The refinement factors for the two finer levels are 2
and 6.  To avoid aliasing affects, the resolution of the resulting PNG
file should be a multiple of 30*2*6 = 360.  This can be done by
setting the figure size and DPI properly::

  # Set dpi and figure size to resolve the 30x30 coarse grid, and two levels of refinement with
  # refinement factors of 2 and 6.
  plotfigure.kml_figsize = [30,30]
  plotfigure.kml_dpi = 12


The resulting image is free of the aliasing artifacts.

.. figure::  images/GE_nonaliased.png
   :scale: 200%
   :align: center

   Aliasing effects removed by properly setting `kml_dpi` and `kml_figsize`

While the above removes aliasing artifacts, you may still find that
the resolution is unacceptable, especially when viewing close-up
views of shorelines, for example.  In this case, you can increase
the resolution of the figure in integer factors that remain consistent with
the coarse grid and refinement factors.

It might not be possible to fully resolve all levels of a large
simulation with many refinement levels because the resulting image
resolution exceeds the Matplotlib limit of 32768 pixels along each
edge of the PNG file.  In this case, one can limit the number of
levels that are resolved by a particular figure, and create zoomed in
figures that resolve finer levels.  Alternatively, one can break the
computational domain into several figures, each covering a portion of
the entire domain.

The Chile example shows a zoomed in figure near the shoreline with increased resolution at all levels.

.. _Publishing your results:

Publishing your results
-----------------------

You can easily share your KMZ file with collaborators
by providing links to your archive KMZ file in HTML webpages.  Collaborators can
download the KMZ file and open it in a Google Earth browser.

However, you may find that the KMZ file is too large to make
downloading convenient.  In this case, you can provide a light-weight
KML file that provides a single link to a KMZ file that you store on a
host server.  Collaborators interested in your results can then open
this KML file in Google Earth and browse your results via an internet connection.

To create this KML file, you should set the `plotdata` attribute
`kml_publish` to the url address of your host server where the KMZ
files will be stored.  For example, the Chile file above is stored at::

  plotdata.kml_publish = "http://math.boisestate.edu/~calhoun/visclaw/GoogleEarth/kmz"

VisClaw will detect that this `plotdata` attribute has been set and
automatically create a KML file that refers to the linked file
"Chile_2010.kmz", stored at the above address.  This KML file (see
`Chile_2010.kml`_) can be easily shared or posted on webpages to allow
collaborators to view your results via links to your remotely stored
KMZ file.  The KML file is set to automatically load an updated KMZ
file every 5 minutes.  You can easily change this setting by editing
the KML file.

By default,  `plotdata.kml_publish` is set to `None`, in which case, no KML file will be created.
