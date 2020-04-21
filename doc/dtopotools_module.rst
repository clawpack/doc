
.. _dtopotools_module:

dtopotools module for moving topography
=======================================

See also :ref:`okada` for a discussion of the subfault parameters required
for the Okada model of seafloor deformation resulting from slip on a
specified fault plane.

.. warning:: Starting in Version 5.5.0, the subfault parameter `rise_time`
   now refers to the total rise time of a subfault, while `rise_time_starting`
   is the rise time up to the break in the piecewise quadratic
   function defining the rise. By default `rise_time_ending` is set equal to
   `rise_time_starting`.  See the module function `rise_fraction` below
   for more description. (In earlier versions, `rise_time` read in from csv
   files, for example, was erroneously interpreted as `rise_time_starting` 
   is now.)


The notebook `dtopotools_examples.ipynb
<http://www.clawpack.org/gallery/_static/notebooks/geoclaw/dtopotools_examples.html>`_
illustrates how to use some of the tools.

The notebook `Okada.ipynb
<http://www.clawpack.org/gallery/_static/notebooks/geoclaw/Okada.html>`_
illustrates the Okada model using some of these tools.

The file `$CLAW/geoclaw/tests/test_dtopotools.py` contains some tests of these
tools.  Looking at these test routines may also give some ideas on 
how to use them.

Documentation auto-generated from the module docstrings
--------------------------------------------------------

.. automodule:: clawpack.geoclaw.dtopotools
   :members:

