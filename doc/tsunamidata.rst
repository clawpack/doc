
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
Global ETOPO bathymetry is relative to MSL (Mean Sea Level), 
while tsunami inundation relief is often relative to MHW (Mean High Water).
These can often be combined since the difference is small relative to the
resolution of the global bathymetry and the result assumed to be relative to
MHW.  This is important if comparing to tide gauge observation or when
modeling inundation.


- `ETOPO Global Relief Model
  <https://www.ncei.noaa.gov/products/etopo-global-relief-model>` provides 
  global bathymetry data at 15, 30 or 60 arc-second resolution.
  Note that ETOPO 2022 is the current version and ETOPO1 (often used in the
  past for GeoClaw modeling is obsolete). 
  Subsets of the 30 or 60 arc-second versions can be downloaded using
  the `geoclaw.topotools.read_netcdf` function, see
  :ref:`topo_netcdf`.  For the 15 arcsecond data it is necessary
  to download one or more tiles from the `15 Arc-second Resolution Bedrock
  elevation netCDF catalog
  <https://www.ngdc.noaa.gov/thredds/catalog/global/ETOPO2022/15s/15s_bed_elev_netcdf/catalog.html>`__

- `NCEI's Bathymetric Data Viewer <https://www.ncei.noaa.gov/maps/bathymetry/>`_
  (Unselect Multibeam Survey Tracklines and Hydrographic Survey Outlines and
  select DEM Footprings to see what is available.)

- `NOAA NCEI inundataion relief
  <http://www.ngdc.noaa.gov/mgg/coastal/coastal.html>`_:
  High resolution data near US coastlines. Includes a link to the
  `THREDDS Data Server <https://www.ngdc.noaa.gov/thredds/demCatalog.html>`_
  for direct access, and `Metadata <https://data.noaa.gov/waf/NOAA/NESDIS/NGDC/MGG/DEM/iso/>`_

- It is also possible to open a remote NetCDF file on the
  `NOAA THREDDS server <https://www.ngdc.noaa.gov/thredds/demCatalog.html>`_
  to download data, which allows downloading only a
  subsampled subset of a large DEM.  See :ref:`topo_netcdf` for more details.

- `GEBCO Gridded Bathymetry Data
  <https://www.gebco.net/data_and_products/gridded_bathymetry_data/>`_


.. _tsunamidata_sources:

Earthquake source models
------------------------

An earthquake source is typically specified by giving the slip along the
fault on a set of fault planes or on subfaults making up a single plane.
This data must then be converted into seafloor deformation to create the
*dtopo* file needed for GeoClaw (see :ref:`topo_dtopo`).  This conversion
is often done using the Okada model as described at
:ref:`okada`.

* `USGS archive <https://earthquake.usgs.gov/earthquakes/search/>`_
* `Chen Ji's archive, UCSB
  <https://ji.faculty.geol.ucsb.edu/big_earthquakes/home.html>`_


DART buoy data
--------------

*Deep-ocean Assessment and Reporting of Tsunamis (DART®)*

- `Information and links <http://www.ngdc.noaa.gov/hazard/DARTData.shtml>`_

Tide gauges
-----------

Tide gauge data is often recorded relative to MLLW (Mean Lower-Low Water), so be
sure to check the 
`vertical datum <http://tidesandcurrents.noaa.gov/datum_options.html>`_.

For example, if you go to a station page such as 
`Hilo Bay
<https://tidesandcurrents.noaa.gov/stationhome.html?id=1617760>`_,
you will see a *Datums* link at the bottom that gives the difference
between MLLW and other water levels such as MHW, which might be the
reference level for the bathymetry.  (Be sure to switch from feet to
meters!)  Sometimes you can also select the Datum to use when retrieving
data.

- `NOAA NCEI Water Level Data in Support of Tsunami Research <http://www.ngdc.noaa.gov/hazard/tide.shtml>`_
- `NOAA Tides & Currents site map
  <https://tidesandcurrents.noaa.gov/sitemap.html>`_
- `GLOSS / SONEL <http://www.sonel.org/-Tide-gauges,29-.html?lang=en>`_
