:orphan:

.. _qinit_defaults:

======================
qinit default routines
======================

Below are links to the default `qinit` library routines for Classic and AMRClaw.  

These should never be used
as is, but rather copied to your application directory and modified to set
the initial conditions as desired.


- `$CLAW/classic/src/1d/qinit.f90
  <https://github.com/clawpack/classic/blob/master/src/1d/qinit.f90>`__

- `$CLAW/classic/src/2d/qinit.f90
  <https://github.com/clawpack/classic/blob/master/src/2d/qinit.f90>`__

- `$CLAW/classic/src/3d/qinit.f90
  <https://github.com/clawpack/classic/blob/master/src/3d/qinit.f90>`__

(Note: these links are for the version checked in to the master branch.
You can select a different branch or tag from the GitHub page.)


.. _qinit_geoclaw:

qinit routine in GeoClaw
------------------------

In GeoClaw, there is a library routine that 
sets the surface elevation to sea level by default, and also has the option
of adding a perturbation as specified in the setrun file, see
:ref:`setrun_qinit`.

- `$CLAW/geoclaw/src/2d/shallow/qinit.f90
  <https://github.com/clawpack/geoclaw/blob/master/src/2d/shallow/qinit.f90>`__

