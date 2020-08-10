:orphan:

.. _setaux_defaults:

========================
setaux default routines
========================

Below are links to the default `setaux` library routines for Classic and AMRClaw.  
By default these do nothing.  If you wish to specify `aux` arrays you will
need to copy one of these files to your application directory and modify it
as needed.  Remember to change to `Makefile` to point to the proper version.


- `$CLAW/classic/src/1d/setaux.f90
  <https://github.com/clawpack/classic/blob/master/src/1d/setaux.f90>`__

- `$CLAW/classic/src/2d/setaux.f90
  <https://github.com/clawpack/classic/blob/master/src/2d/setaux.f90>`__

- `$CLAW/classic/src/3d/setaux.f90
  <https://github.com/clawpack/classic/blob/master/src/3d/setaux.f90>`__

(Note: these links are for the version checked in to the master branch.
You can select a different branch or tag from the GitHub page.)




.. _setaux_geoclaw:

setaux routine in GeoClaw
--------------------------

In GeoClaw, there is a library routine that sets `aux(1,i,j)` to the cell
average of the bathymetry, `aux(2,i,j)` to the ratio of the true cell area
to `dx*dy` (the capacity function), and `aux(3,i,j)` to the length ratio of 
the bottom edge to `dx` (The latter two quantities vary  
with latitude when `coordinate_system == 2`).

- `$CLAW/geoclaw/src/2d/shallow/b4step2.f90
  <https://github.com/clawpack/geoclaw/blob/master/src/2d/shallow/b4step2.f90>`__

