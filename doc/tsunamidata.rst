
.. _tsunamidata:

==================================
Some sources of tsunami data
==================================

.. seealso :: :ref:`topo`

Topography / bathymetry
------------------------

Note that it is important to know what elevation :math:`B=0` 
corresponds to for each
topography dataset you might use (i.e. the 
`vertical datum <http://tidesandcurrents.noaa.gov/datum_options.html>`_)
Global ETOPO1 bathymetry is relative to MSL (Mean Sea Level), 
while tsunami inundation relief is often relative to MHW (Mean High Water).
These can often be combined since the difference is small relative to the
resolution of the global bathymetry and the result assumed to be relative to
MHW.  This is important if comparing to tide gauge observation or when
modeling inundation.

The NOAA Design-a-Grid tool no longer exists but you can download data sets
from:

* `NCEI's WCS Grid Extraction Tool <http://maps.ngdc.noaa.gov/viewers/wcs-client/>`_
* `NOAA NCEI inundataion relief
  <http://www.ngdc.noaa.gov/mgg/coastal/coastal.html>`_:
  High resolution data near US coastlines.
* `More recent catalog
  <https://data.noaa.gov/waf/NOAA/NESDIS/NGDC/MGG/DEM/iso/>`_

It is also possible to open a remote NetCDF file on the
`NOAA THREDDS server <https://www.ncei.noaa.gov/thredds/remoteCatalogService?catalog=https://www.ngdc.noaa.gov/thredds/demCatalog.xml>`_
to download data, which allows downloading only a
subsampled subset of a large DEM.  See :ref:`topo_netcdf` for more
details.

.. _tsunamidata_sources:

Earthquake source models
------------------------

An earthquake source is typically specified by giving the slip along the
fault on a set of fault planes or on subfaults making up a single plane.
This data must then be converted into seafloor deformation to create the
*dtopo* file needed for GeoClaw (see :ref:`topo_dtopo`).  This conversion
is often done using the Okada model as described at
:ref:`okada`.

* `USGS archive <https://earthquake.usgs.gov/earthquakes/browse/>`_
* `Chen Ji's archive, UCSB
  <http://www.geol.ucsb.edu/faculty/ji/big_earthquakes/home.html>`_


DART buoy data
--------------

* `Information page <http://www.ngdc.noaa.gov/hazard/DARTData.shtml>`_
* `Real-time and archived data <http://www.ndbc.noaa.gov/dart.shtml>`_

Tide gauges
-----------

Tide gauge data is often recorded relative to MLLW (Mean Lower-Low Water), so be
sure to check the 
`vertical datum <http://tidesandcurrents.noaa.gov/datum_options.html>`_.

For example, if you go to a station page such as 
`Hilo Bay
<http://tidesandcurrents.noaa.gov/data_menu.shtml?stn=1617760%20Hilo,%20Hilo%20Bay,%20Kuhio%20Bay,%20HI&type=Historic%20Tide%20Data>`_,
you will see a *Datums* link on the left menu that gives the difference
between MLLW and other water levels such as MHW, which might be the
reference level for the bathymetry.  (Be sure to switch from feet to
meters!)  Sometimes you can also select the Datum to use when retrieving
data.

* `NCEI <http://www.ngdc.noaa.gov/hazard/tide.shtml>`_
* NOAA Tides & Currents: `Historic verified data
  <http://tidesandcurrents.noaa.gov/station_retrieve.shtml?type=Historic+Tide+Data>`_
  ...  `Preliminary data
  <http://tidesandcurrents.noaa.gov/station_retrieve.shtml?type=Tide+Data>`_

* `NOAA 1-minute water level data
  <http://tidesandcurrents.noaa.gov/1mindata.shtml>`_
  at tsunami-capable stations.

* `GLOSS / SONEL <http://www.sonel.org/-Tide-gauges,29-.html?lang=en>`_
