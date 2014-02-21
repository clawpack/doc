
.. _release_5_0_1:

==========================
Release 5.0.1
==========================

Clawpack 5.0.1 was released on ??.  See :ref:`installing`.


Changes to classic
------------------

* None

See `classic diffs
<https://github.com/clawpack/classic/compare/aac8471ce97...master>`_

Changes to clawutil
-------------------

* Minor change for replacing a rundata object.  

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/55f81e395...master>`_

Changes to visclaw
------------------

* Replaced JSAnimation.IPython_display.py by improved version.

* Added an attribute to `data.py`.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/6669145d5bdf...master>`_

Changes to riemann
------------------

* Changes to multi-layer code -- do not attempt to compile  by default
  since LAPACK is required.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/7ef4a50f84c...master>`_

Changes to amrclaw
------------------

* Fixed the calling sequence where setaux is called two places in the
  regridding routines.  

* Several other minor fixes.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/0ad5e60a38d...master>`_

Changes to geoclaw
------------------

* Change gauge output to avoid underflow in printing.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/eefc8e4ff...master>`_

Changes to PyClaw
------------------


* Added 3d capabilities to SharpClaw.

* Many other minor fixes.

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/875a98eea...master>`_

