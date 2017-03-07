:orphan:

.. _src_defaults:

========================
src default routines
========================

See also :ref:`user_src`.

For GeoClaw, see :ref:`src_geoclaw`.

Below are the default `src` library routines for Classic and AMRClaw.  
By default these do nothing.  If you wish to specify source terms, you
need to copy one of these files to your application directory and modify it
as needed.  Remember to change to `Makefile` to point to the proper version.

If you are using AMRClaw, you will also need to provide a routine `src1d`,
see :ref:`user_src1d`.


`$CLAW/classic/src/1d/src1.f90`:

.. literalinclude:: ../../classic/src/1d/src1.f90
   :language: fortran
   :linenos:

`$CLAW/classic/src/2d/src2.f90`:

.. literalinclude:: ../../classic/src/2d/src2.f90
   :language: fortran
   :linenos:

`$CLAW/classic/src/3d/src3.f90`:

.. literalinclude:: ../../classic/src/3d/src3.f90
   :language: fortran
   :linenos:


.. _src_geoclaw:

src routine in GeoClaw
--------------------------

In GeoClaw, there is a library routine to impose source terms for bottom
friction (via a Manning term) and Coriolis terms.  The topography source term
is built into the Riemann solver in a manner that achieves well balancing
(an ocean at rest remains at rest).

`$CLAW/geoclaw/src/2d/shallow/src2.f90`:

.. literalinclude:: ../../geoclaw/src/2d/shallow/src2.f90
   :language: fortran
   :linenos:
