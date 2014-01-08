
.. _b4step_defaults:

========================
b4step default routines
========================

For GeoClaw, see :ref:`b4step_geoclaw`.

Below are the default `b4step` library routines for Classic and AMRClaw.  
By default these do nothing.  If you wish to specify `aux` arrays you will
need to copy one of these files to your application directory and modify it
as needed.  Remember to change to `Makefile` to point to the proper version.


`$CLAW/classic/src/1d/b4step1.f90`:

.. literalinclude:: ../../classic/src/1d/b4step1.f90
   :language: fortran
   :linenos:

`$CLAW/classic/src/2d/b4step2.f90`:

.. literalinclude:: ../../classic/src/2d/b4step2.f90
   :language: fortran
   :linenos:

`$CLAW/classic/src/3d/b4step3.f90`:

.. literalinclude:: ../../classic/src/3d/b4step3.f90
   :language: fortran
   :linenos:


.. _b4step_geoclaw:

b4step routine in GeoClaw
--------------------------

In GeoClaw, there is a library routine that sets `aux(1,i,j)` to the cell
average of the bathymetry, `aux(2,i,j)` to the ratio of the true cell area
to `dx*dy` (the capacity function), and `aux(3,i,j)` to the length ratio of 
the bottom edge to `dx` (The latter two quantities vary  
with latitude when `coordinate_system == 2`).

`$CLAW/geoclaw/src/2d/shallow/b4step2.f90`:

.. literalinclude:: ../../geoclaw/src/2d/shallow/b4step2.f90
   :language: fortran
   :linenos:
