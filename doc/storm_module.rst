
.. _storm_module:

Meteorological Forcing Python API
=================================

.. seealso::
   - :ref:`met_forcing` -- overview of met forcing and the object model
   - :ref:`setrun_surge` -- the ``rundata.met_data`` attribute reference
   - :ref:`netcdf_input` -- gridded NetCDF met forcing

This is the Python API for building and writing GeoClaw meteorological forcing.
The object model separates the evolving feature (a :class:`Track` /
:class:`StormTrack`) from the forcing generated from it
(:class:`ParametricMetForcing`, :class:`GriddedMetForcing`).  The historical
:class:`Storm` class is retained as a backwards-compatible wrapper.

Readers ingest many track/data formats; writers emit only the two files
GeoClaw consumes -- a parametric storm file (``write_geoclaw``) and a gridded
descriptor (``write_data``).

Storm (compatibility wrapper)
-----------------------------

.. automodule:: clawpack.geoclaw.met.storm
   :members:
   :undoc-members:
   :show-inheritance:

Track and StormTrack
--------------------

.. automodule:: clawpack.geoclaw.met.track
   :members:
   :undoc-members:
   :show-inheritance:

Parametric met forcing
----------------------

.. automodule:: clawpack.geoclaw.met.parametric
   :members:
   :undoc-members:
   :show-inheritance:

Gridded met forcing
-------------------

.. automodule:: clawpack.geoclaw.met.gridded
   :members:
   :undoc-members:
   :show-inheritance:

Workflow tools
--------------

.. automodule:: clawpack.geoclaw.met.tools
   :members:
   :undoc-members:
   :show-inheritance:

Met forcing data object
-----------------------

The ``surge.data`` file written by ``setrun.py`` is described by
:class:`~clawpack.geoclaw.data.SurgeData` (also available under the alias
``MetData``); it is set in ``setrun.py`` as ``rundata.met_data`` (the former
``rundata.surge_data`` remains an accepted alias).  See :ref:`setrun_surge` for
the per-attribute reference.

.. autoclass:: clawpack.geoclaw.data.SurgeData
   :members:
   :undoc-members:
   :show-inheritance:
