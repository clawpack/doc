
.. _met_forcing:

**********************************************
Meteorological (Storm) Forcing
**********************************************

GeoClaw can force the shallow water equations with wind and atmospheric
pressure fields.  This *meteorological forcing* ("met forcing") drives storm
surge, and also supports non-tropical applications (extratropical cyclones,
meteo-tsunamis, and other atmospheric forcing).  A storm is one important
subtype of met forcing rather than the whole story.

This page gives an overview and points to the quick start, the ``setrun``
reference, and the Python API.  For a hands-on walkthrough see
:ref:`quick_surge`; for data sources see :ref:`surgedata`.

Forcing families
================

Met forcing comes in two families, selected in ``setrun.py`` through
``rundata.met_data`` (see :ref:`setrun_surge`):

**Parametric forcing**
   Wind and pressure fields are generated from a compact, evolving description
   of a storm (its track plus intensity parameters) using an analytic model
   such as Holland 1980.  A parametric storm has an analytic center/eye, so it
   can drive distance-to-center AMR refinement.  Supported models include
   ``holland80``, ``holland2008``, ``holland2010``, ``cle``, ``slosh``,
   ``rankine``, ``modified_rankine``, ``demaria``, and ``willoughby``.

**Gridded forcing**
   Wind and pressure are read from external field datasets and interpolated to
   the grid, rather than assuming a profile.  Two formats are supported:
   OWI/ASCII (NWS12) and NetCDF (NWS13).  Gridded forcing has no analytic
   center, so refinement is driven by the wind-speed thresholds only.  See
   :ref:`netcdf_input` for the NetCDF conventions, automatic variable
   discovery, and unit/time handling.

Selecting a forcing
===================

The explicit, preferred way to select forcing is a **family** plus a
**subtype**::

    rundata.met_data.storm_family  = "parametric"   # or "gridded" / "none"
    rundata.met_data.storm_subtype = "holland80"    # model, or "gridded"
    rundata.met_data.storm_file    = "path/to/storm"

See :ref:`setrun_surge` for the full attribute reference.

Python object model
===================

The Python side is organized around met forcing rather than only storms
(:ref:`storm_module` is the API reference):

- :class:`~clawpack.geoclaw.met.track.Track` -- a generic evolving feature
  with a center over time, and
  :class:`~clawpack.geoclaw.met.track.StormTrack`, which adds storm metadata
  (max wind speed, radius of maximum winds, central pressure, ...).
- :class:`~clawpack.geoclaw.met.parametric.ParametricMetForcing` -- forcing
  from a parameterized model referencing a track.
- :class:`~clawpack.geoclaw.met.gridded.GriddedMetForcing` -- forcing from
  external field datasets (OWI/ASCII, NetCDF).
- :class:`~clawpack.geoclaw.met.storm.Storm` -- a backwards-compatible
  wrapper retaining the historical ``read``/``write`` interface; new code can
  use the objects above directly.

Track readers ingest many formats (ATCF, HURDAT, IBTrACS, JMA, TCVITALS);
GeoClaw writes only the two forcing files it consumes: a parametric storm file
(``write_geoclaw``) and a gridded descriptor (``write_data``).

.. _met_forcing_migration:

What's new / migrating
======================

Existing ``setrun.py`` scripts continue to work.  The changes are additive:

- **Explicit family/subtype selection.** ``storm_family`` + ``storm_subtype``
  replace the overloaded integer ``storm_specification_type`` at the API level.
  The legacy selector -- either a model-name string (``'holland80'``,
  ``'data'``) or the signed integer code -- is still fully supported and maps
  to the same forcing.
- **Gridded NetCDF forcing.** Full gridded wind/pressure forcing from
  CF-compliant NetCDF files, with automatic variable/coordinate discovery and
  unit handling (:ref:`netcdf_input`).
- **Temporal ramps.** ``t_ramp_on`` / ``t_ramp_off`` ramp the forcing on and
  off over a specified number of seconds.
- **Object model.** The ``Track`` / ``StormTrack`` / ``ParametricMetForcing`` /
  ``GriddedMetForcing`` classes above, with ``Storm`` retained as a
  compatibility wrapper.
- **Python package renamed** ``clawpack.geoclaw.surge`` →
  ``clawpack.geoclaw.met`` (the meteorological-forcing name).  Import from
  ``clawpack.geoclaw.met`` (e.g. ``clawpack.geoclaw.met.storm``); the old
  ``clawpack.geoclaw.surge`` still works but emits a ``DeprecationWarning``.  In
  ``setrun.py`` use ``rundata.met_data`` (the former ``rundata.surge_data``
  remains an accepted alias), and :class:`~clawpack.geoclaw.data.SurgeData` is
  also exposed as ``MetData``.  The on-disk ``surge.data`` file and its format
  are unchanged.

.. note::

   The Fortran modules were renamed to the met-forcing vocabulary
   (``storm_module`` → ``met_forcing_module``,
   ``model_storm_module`` → ``parametric_met_forcing_module``,
   ``data_storm_module`` → ``gridded_met_forcing_module``).  This only affects
   custom Fortran source that ``use``\ s those modules; ``setrun.py`` workflows
   are unaffected.
