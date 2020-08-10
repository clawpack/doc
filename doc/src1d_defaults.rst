:orphan:

.. _src1d_defaults:

========================
src1d default routines
========================

See also :ref:`user_src1d`.

Below are links to the default `src1d` library routines for AMRClaw.  
The same form is used in both 2d and 3d.
By default these do nothing.  If you wish to specify source terms, you
need to copy one of these files to your application directory and modify it
as needed.  Remember to change to `Makefile` to point to the proper version.

- `$CLAW/amrclaw/src/2d/src1d.f90
  <https://github.com/clawpack/amrclaw/blob/master/src/2d/src1d.f90>`__

- `$CLAW/amrclaw/src/3d/src1d.f90
  <https://github.com/clawpack/amrclaw/blob/master/src/3d/src1d.f90>`__

(Note: these links are for the version checked in to the master branch.
You can select a different branch or tag from the GitHub page.)


.. _src1d_geoclaw:

src1d routine in GeoClaw
--------------------------

In GeoClaw, there is a library routine to impose source terms for bottom
friction (via a Manning term) and Coriolis terms.  The topography source term
is built into the Riemann solver in a manner that achieves well balancing
(an ocean at rest remains at rest).

- `$CLAW/geoclaw/src/2d/shallow/src1d.f90
  <https://github.com/clawpack/geoclaw/blob/master/src/2d/shallow/src1d.f90>`__

