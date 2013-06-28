.. _sealevel:

==========================
Setting sealevel
==========================

GeoClaw has a parameter *sealevel* (see :ref:`setrun_geoclaw`) that can be
used to specify the initialization of the fluid depth relative to the
specified topography (see :ref:`topo`).  Unless a different set of initial
conditions is specified (see :ref:`setrun_qinit`), the default is to
initialize with zero velocity and depth *h* chosen so that *h+B = sealevel*
at any point where *B < sealevel*, where *B* is the topography or bathymetry
in the grid cell (as determined by interpolation from the specified
*topo* files as described in :ref:`topo`).

It is important to know what 
`vertical datum <http://tidesandcurrents.noaa.gov/datum_options.html>`_
the topography is relative to.  Coastal bathymetry developed for tsunami
modeling (e.g. from
`NOAA NGDC inundataion relief
<http://www.ngdc.noaa.gov/mgg/coastal/coastal.html>`_)
is often relative to Mean High Water (MHW), in
which case setting *sealevel = 0.* corresponds to assuming the water level
is initially at MHW.  To adjust to use a different tide level, the value of
*sealevel* must be set appropriately.  The relation between MHW and other
tide levels such as Mean Sea Level (MSL) can often be found from the NGDC
webpages for a nearby tide gauge. 
For example, if you go to a station page such as 
`Hilo Bay
<http://tidesandcurrents.noaa.gov/data_menu.shtml?stn=1617760%20Hilo,%20Hilo%20Bay,%20Kuhio%20Bay,%20HI&type=Historic%20Tide%20Data>`_,
you will see a *Datums* link on the left menu.
(Be sure to switch from feet to meters!) 

Note that the difference between MHW and MSL can vary greatly between
different locations.  
Global bathymetry data such as the ETOPO1 data (available from
`GEODAS Grid Translator - Design-a-Grid
<http://www.ngdc.noaa.gov/mgg/gdas/gd_designagrid.html>`_)
is generally relative to MSL.  
However, this data has a resolution of 1 arc-minute, more than 1.5 km, and
is not suitable as coastal bathymetry, so this data will presumably only be
used in grid cells away from the region where coastal bathymetry is
available.  Since the difference between MSL and
MHW is at most a few meters, the use of different vertical datums for
regions of vastly different resolution will generally have little effect.

If GeoClaw is used to compare inundation or tide gauge values to
observations from past tsunamis, it may be important to know the tide stage
when the largest tsunami waves arrived.  Ideally it would be possible to
model the actual rise and fall of the tides during the duration 
of the event, but this is not currently possible.
Tidal currents may also have a significant effect on observed inundation
patterns, but these are also ignored in GeoClaw since the water is assumed
to be at rest before the tsunami arrives.

If GeoClaw is used for hazard assessment based on potential tsunami
scenarios, then thought should be given to the appropriate value of
*sealevel* to assume.  The NGDC coastal bathymetry data is referenced to MHW
because this is often the level assumed for tsunami hazard assessment, but
higher tide levels such as Mean Higher High Water (MHHW) or the Astronomical
High Tide (AHT) are sometimes used for worst-case scenarios.  

See :ref:`tsunamidata` for some other sources of data.

