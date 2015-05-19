
.. _fgout:

=====================
Fixed grid output
=====================

GeoClaw has the capability to output the results at specified output times
on a specified "fixed grid" by interpolating from the AMR grids active at each 
output time.  The original version of this from Clawpack 4.6 still exists,
see :ref:`setrun_fixedgrids`,
but it has been deprecated and its use is not advised.

An improved version for monitoring maximum values and arrival times has been
added, see :ref:`fgmax`.

