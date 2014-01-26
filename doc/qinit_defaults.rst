
.. _qinit_defaults:

======================
qinit default routines
======================

For GeoClaw, see :ref:`qinit_geoclaw`.

Below are the default `qinit` library routines for Classic and AMRClaw.  

These should never be used
as is, but rather copied to your application directory and modified to set
the initial conditions as desired.

`$CLAW/classic/src/1d/qinit.f90`:

.. literalinclude:: ../../classic/src/1d/qinit.f90
   :language: fortran
   :linenos:

`$CLAW/classic/src/2d/qinit.f90`:

.. literalinclude:: ../../classic/src/2d/qinit.f90
   :language: fortran
   :linenos:

`$CLAW/classic/src/3d/qinit.f90`:

.. literalinclude:: ../../classic/src/3d/qinit.f90
   :language: fortran
   :linenos:


.. _qinit_geoclaw:

qinit routine in GeoClaw
------------------------

In GeoClaw, there is a library routine that 
sets the surface elevation to sea level by default, and also has the option
of adding a perturbation as specified in the setrun file, see
:ref:`setrun_qinit`.

`$CLAW/geoclaw/src/2d/shallow/qinit.f90`:

.. literalinclude:: ../../geoclaw/src/2d/shallow/qinit.f90
   :language: fortran
   :linenos:
