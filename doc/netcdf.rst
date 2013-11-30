.. _netcdf:

==========================
Using NetCDF output
==========================

The AMRClaw and GeoClaw codes have the option to output results in
binary using NetCDF instead of the usual :ref:`ascii_output_format`.

To install netcdf
-------------------

The hardest part may be installing netcdf on your computer.
See `<http://www.unidata.ucar.edu/software/netcdf/>`_ for downloads and
instructions.

To compile with netcdf
----------------------

In the Makefile for your application directory, add the appropriate links to
the `FFLAGS` line to tell the compiler what netcdf libraries are used and
where to find them.  For example, if the libraries were installed in
`/usr/include` then this line should look like this, along with whatever other
flags you need::

    FFLAGS = -I/usr/include  -lnetcdf -lnetcdff

Also change the `Makefile` to remove the line that points to the routine
`valout.f` in AMRClaw or to `valout_geo.f` in GeoClaw to the appropriate one
of the following::

      $(CLAW_LIB)/valout_nc.f \

or ::

      $(GEOLIB)/valout_nc_geo.f \

After running the code, the output directory will contain files with names
like `fort.t0001.nc` and `fort.q0001.nc` (for time frame 1, for example).  

To plot the results
-------------------

You can use the same `setplot.py` to plot the results as usual, but you need
to add the line ::

    plotdata.format = 'netcdf'

somewhere in the `setplot` function.  

