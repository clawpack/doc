

.. _quick_surge:

*****************************************************************
Quick start guide for storm surge modeling
*****************************************************************

See also this `youtube video <https://www.youtube.com/watch?v=YurKRmYgGfk&t=10s>`__
and the related materials from the `2020 GeoClaw Developers Workshop
<http://www.clawpack.org/geoclawdev-2020/>`__, the :ref:`met_forcing` overview,
and the :ref:`setrun_surge` reference.

The quickest way to get started is to run a working example and then adapt it.
A good starting point is ``$CLAW/geoclaw/examples/storm-surge/ike`` (Hurricane
Ike, parametric Holland 1980 forcing).  There are further examples in
``$CLAW/geoclaw/examples/storm-surge`` and in the actively maintained
``$CLAW/apps/surge-examples`` repository.

Running the Ike example
=======================

From ``$CLAW/geoclaw/examples/storm-surge/ike``::

    make all

This downloads the topography, writes the storm forcing file, compiles
``xgeoclaw``, runs the simulation, and produces plots in ``_plots``.  The
individual steps are also available as separate targets::

    make .exe       # compile xgeoclaw
    make data       # write the *.data files from setrun.py
    make .output    # run the simulation
    make .plots     # generate plots with setplot.py

The two inputs a surge computation needs
========================================

- **Topography / bathymetry** for the region of interest.  For surge it is good
  practice to include entire oceanic basins so that flow into and out of the
  basin is resolved and the domain boundaries are far from the area of interest.
  See :ref:`topo` for supported formats.
- **Storm forcing** describing the wind and pressure.  There are two families
  (parametric and gridded); see :ref:`met_forcing` for the overview and
  :ref:`surgedata` for data sources.

Configuring the forcing in ``setrun.py``
========================================

Storm forcing is configured through ``rundata.met_data`` (full reference in
:ref:`setrun_surge`).  The Ike example enables the wind and pressure source
terms and selects a parametric Holland 1980 storm::

    data = rundata.met_data
    data.wind_forcing = True
    data.pressure_forcing = True
    data.drag_law = 1                      # Garratt wind drag

    # Preferred, explicit forcing selection:
    data.storm_family = "parametric"
    data.storm_subtype = "holland80"
    data.storm_file = "ike.storm"          # GeoClaw-format storm file

    # AMR refinement on wind speed (m/s) and distance to the eye (m):
    data.wind_refine = [20.0, 40.0, 60.0]
    data.R_refine = [60.0e3, 40.0e3, 20.0e3]

The legacy selector ``data.storm_specification_type = 'holland80'`` is
equivalent and still supported.

Building the storm file
=======================

The GeoClaw-format storm file (``ike.storm`` above) is produced from a track in
one of the ingest formats (ATCF, HURDAT, IBTrACS, JMA, TCVITALS).  Using the
Python API (see :ref:`storm_module`)::

    from clawpack.geoclaw.met.storm import Storm
    import numpy as np

    storm = Storm(path="track.dat", file_format="ATCF")
    storm.time_offset = np.datetime64("2008-09-13T07:00")   # e.g. landfall
    storm.write("ike.storm", file_format="geoclaw")

Plotting and gauges
===================

The example ``setplot.py`` uses the ``clawpack.geoclaw.met.plot`` helpers
(imported as ``met_plot``) to plot the surface elevation, wind speed, and
pressure fields, overlay the storm track, and plot gauge time series.  Gauges
record the wind and pressure aux fields when ``rundata.gaugedata.aux_out_fields``
includes the wind/pressure aux indices.

Using gridded (OWI / NetCDF) forcing
====================================

To force GeoClaw with gridded fields instead of a parametric model, set the
family to ``"gridded"`` and provide the field files.  For NetCDF this is a
CF-compliant file of wind (``u10``, ``v10``) and mean-sea-level pressure
(``msl``); GeoClaw discovers the variables and coordinates automatically.  See
:ref:`netcdf_input` for the full workflow and the
``$CLAW/geoclaw/examples/storm-surge/isaac`` example, which drives both
parametric and gridded forcing from the same ATCF track.

Adapting to a different storm
=============================

To model a different event, copy the Ike example directory and then:

1. Obtain topography covering the affected basin (see :ref:`topo` and the data
   sources linked from :ref:`surgedata`).
2. Obtain the storm track (e.g. an ATCF best-track file; see :ref:`surgedata`)
   and build the storm file as shown above, or point ``storm_file`` at a
   gridded descriptor for gridded forcing.
3. Update ``setrun.py`` -- the domain extent, refinement regions, ``met_data``
   selection, gauges, and run time -- for the new event.
4. Update ``setplot.py`` for the new domain and gauges.
