
.. _surgedata:

==================================
Sources for Storm Surge Data
==================================

For storm surge computations the input data is very similar to tsunamis save
for the specification of the forcing storm (as opposed to an earthquake).  There
are multiple ways to specify a storm forcing in GeoClaw which include

1. Storms described by a set of observerd parameters for which the wind and pressure
   fields are constructed by a parametric model such as the Holland 1980 model.  These
   generally require:
   - the maximum wind speed,
   - the radius at which the maximum winds occurs,
   - the central pressure of the storm,
   - the location of the center of the storm (the eye),
   - and sometimes the maximum radius of the storm is also included.

2. Storm described by a grided set of data.  This includes output from a 
   modeled storm such as from HWRF, or observed values if dense enough.  Here GeoClaw
   will interpolate this data to the grid cells as needed rather than assume a particular
   profile for the wind and pressure.

For the parameterized storm data there are a number of sources supported for this data and
there is a listing in :ref:`_storm_module` of available input formats.  Valid input files
for this type of input are made available by the particular agency involved:

 - `ATCF <http://ftp.nhc.noaa.gov/atcf/archive/>`_
 - `HURDAT <http://www.aoml.noaa.gov/hrd/hurdat/Data_Storm.html>`_
 - `JMA <http://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/besttrack.html>`_
 - `IMD <http://www.rsmcnewdelhi.imd.gov.in/index.php?option=com_content&view=article&id=48&Itemid=194&lang=en>`_
 - `TCVITALS <http://hurricanes.ral.ucar.edu/repository/>`_

Note that not all these formats are currently fully supported and may require some work
to be readable.