
.. _kmltools_module:

kmltools module of utility functions 
========================================

Use functions in this module to create kml files 
that can be opened in Google Earth or other GIS tools to display
lines (e.g. transects),
polygons of various sorts (e.g. outlines of topofiles, flagregions, fgmax
regions), or points (indicating gauge locations, for example).

Some functions instead create kmz files that contain png files (showing e.g.
topography values, maximum inundation depth in an fgmax region, contours of
the dtopo deformation, etc.) together with a kml wrapper that positions the
images properly.

If you include the following lines in the `__main__` program of `setrun.py`,
after `rundata` has been computed by calling `setrun`::

    from clawpack.geoclaw import kmltools
    kmltools.make_input_data_kmls(rundata)

then `make data`
will automatically generate a number of useful kml/kmz files from the data
provided, showing for example the extents of topofiles, dtopofiles,
flagregions for refinement, gauge locations, etc.
Clicking on one of these regions pops up additional information.

Documentation auto-generated from the module docstrings
--------------------------------------------------------

.. automodule:: clawpack.geoclaw.kmltools
   :members:

