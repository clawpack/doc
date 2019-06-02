:orphan:

.. _release_5_6_0:

===============================
v5.6.0 release notes
===============================


Clawpack 5.6.0 was released on June 2, 2019.  See :ref:`installing`.

Changes relative to Clawpack 5.5.0 (Aug 28, 2018) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Changes that are not backward compatible
----------------------------------------

 - A new approach to flagging cells for AMR refinement was added in 1d and
   2d amrclaw and in geoclaw (see notes below).  This led to the addition
   of a new `adjoint.data` file created by running `setrun.py`.
   If adjoint error flagging is not being used then this file is still 
   expected by the Fortran code.  

 - Many Fortran routines changes for adjoint flagging and some new modules
   were added, resulting in changes to the Makefiles used in amrclaw and
   geoclaw (see below).

General changes
---------------

 - None so far.

Changes to classic
------------------

Nothing major.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.5.0...v5.6.0>`_

Changes to clawutil
-------------------

 - A new attribute `data.ClawRunData.adjointdata` was added, which points to
   an object of class `amrclaw.data.AdjointData` containing information
   about inputs needed for adjoint flagging.


See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.5.0...v5.6.0>`_

Changes to visclaw
------------------

 - Numerous minor improvements.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.5.0...v5.6.0>`_

Changes to riemann
------------------

 - HLLE solvers added for the Euler equations and 1d and 2d shallow water.

 - Riemann solvers added for the adjoint of the linearized shallow water
   equations in non-conservative form, as needed for adjoint flagging.

 - Note that other adjoint Riemann solvers for amrclaw examples had already
   been added in v5.5.0.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.5.0...v5.6.0>`_

Changes to amrclaw
------------------

 - A new approach to flagging cells for AMR refinement was added in 1d and
   2d (not yet in 3d), based on 
   first solving an adjoint equation and then taking inner products of the
   forward solution at each regridding time with snapshots of the adjoint
   solution.  This is described in `<http://www.clawpack.org/dev/adjoint.html>`_
   and `<http://www.clawpack.org/dev/refinement.html>`_.  This was developed 
   over the past several years, primarily by 
   `@BrisaDavis <https://github.com/BrisaDavis/>`_, and required 
   refactoring several routines.  Some of these changes were already
   included in version 5.5.0.

 - In `amrclaw/src/1d`, new the Fortran module `adjoint_module.f90`
   was to support adjoint flagging, and `Makefile.amr_1d` updated.

 - In `amrclaw/src/2d`, new Fortran modules `adjoint_module.f90` and 
   `adjointsup_module.f90` were added to support adjoint flagging, 
   and `Makefile.amr_2d` updated.

 - class `amrclaw.data.AdjointData` added, to contain information 
   about adjoint error flagging.

 - `moment.f` was refactored as `moment.f90`.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.5.0...v5.6.0>`_

Changes to geoclaw
------------------

 - The adjoint flagging option was also added to GeoClaw, resulting in 
   many changes to geoclaw routines.

 - In `geoclaw/src/2d/shallow`, new Fortran modules `adjoint_module.f90` and 
   `adjointsup_module.f90` were added to support adjoint flagging, 
   and `Makefile.geoclaw` updated.

 - These modules were also added to
   `src/2d/shallow/multilayer/Makefile.multilayer`, although adjoint
   flagging has not been implemented yet for the multilayer equations.

 - New capabilities were added to `src/python/geoclaw/surge/storm.py` for
   reading storm tracks.

 - `topotools.read_netcdf` was improved to more robustly handle `coarsen == 1`

 - The url was fixed in `examples/tsunami/chile2010/maketopo.py` that caused
   a webpage to be downloaded instead of the topofile needed for this
   example, caused by incorrect url resolution of `geoclaw.org`.

 - A typo was fixed in `dtopotools.SubFault.dynamic_slip` that caused
   failure.

 - Numerous other minor fixes and improvements.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.5.0...v5.6.0>`_


Changes to PyClaw
------------------


For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.5.0...v5.6.0>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.5.0...v5.6.0>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.5.0...v5.6.0>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.5.0...v5.6.0>`_

