:orphan:
.. _release_5_2_2:

===============================
Release 5.2.2
===============================

Clawpack 5.2.2 was released on October 28, 2014.  
See :ref:`installing` and https://github.com/clawpack/clawpack/releases/.

Changes relative to Clawpack 5.2.1 (October 2, 2014) are shown below.


Changes to classic
------------------


See `classic diffs
<https://github.com/clawpack/classic/compare/v5.2.1...v5.2.2>`_

Changes to clawutil
-------------------

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.2.1...v5.2.2>`_

Changes to visclaw
------------------

 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.2.1...v5.2.2>`_

Changes to riemann
------------------

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.2.1...v5.2.2>`_

Changes to amrclaw
------------------


See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.2.1...v5.2.2>`_

Changes to geoclaw
------------------

* Fixed problem when a single time is specified in dtopo file and dtdtopo(m) = 0.
  The example in `$CLAW/geoclaw/apps/tsunami/chile2010` was modified in 5.2.1 
  to use this feature but it was not implemented properly. 
  See https://github.com/clawpack/geoclaw/pull/116.

* Removed duplicate definition of RefinementData in `data.py`

* Improved handling of ticklabels in topotools and dtopotools plotting.
  See https://github.com/clawpack/geoclaw/pull/114.

* Fixed a number of bugs in `fgmax_tools.py` that didn't work properly
  for `point_style` taking values other than 2.  Some new examples have 
  been added to `$CLAW/apps/tsunami` to illustrate the use of fgmax
  monitoring.  See:

   * :ref:`fgmax`
   * :ref:`apps`
   * :ref:`galleries`

* Fixed other minor glitches.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.2.1...v5.2.2>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.2.1...v5.2.2>`_

