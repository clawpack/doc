
.. _setaux_defaults:

========================
setaux default routines
========================

For GeoClaw, see :ref:`setaux_geoclaw`.

Below are the default `setaux` library routines for Classic and AMRClaw.  
By default these do nothing.  If you wish to specify `aux` arrays you will
need to copy one of these files to your application directory and modify it
as needed.  Remember to change to `Makefile` to point to the proper version.


`$CLAW/classic/src/1d/setaux.f90`:

.. literalinclude:: ../../classic/src/1d/setaux.f90
   :language: fortran
   :linenos:

`$CLAW/classic/src/2d/setaux.f90`:

.. literalinclude:: ../../classic/src/2d/setaux.f90
   :language: fortran
   :linenos:

`$CLAW/classic/src/3d/setaux.f90`:

.. literalinclude:: ../../classic/src/3d/setaux.f90
   :language: fortran
   :linenos:


.. _setaux_geoclaw:

setaux routine in GeoClaw
--------------------------

In GeoClaw, there is a library routine that sets `aux(1,i,j)` to the cell
average of the bathymetry, `aux(2,i,j)` to the ratio of the true cell area
to `dx*dy` (the capacity function), and `aux(3,i,j)` to the length ratio of 
the bottom edge to `dx` (The latter two quantities vary  
with latitude when `coordinate_system == 2`).

`$CLAW/geoclaw/src/2d/shallow/setaux.f90`:

.. literalinclude:: ../../geoclaw/src/2d/shallow/setaux.f90
   :language: fortran
   :linenos:
