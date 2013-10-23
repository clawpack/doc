.. _clawpack5:


================================
Changes in Clawpack 5.0
================================

Clawpack 5.0 is a major reorganization of the Clawpack code base that has
been going on for several years.  
There is no complete list of changes since it has evolved to be very
different from the 4.x version of Clawpack in organization, but some of
major changes that affect users are listed below.

Some tools are available to assist users in converting code from earlier
versions.  To go from Clawpack 4.6 to 5.0, see
:ref:`claw46to50`.   Some older Clawpack 4.3 code can be first converted 
to 4.6 form using :ref:`claw43to44`.

If you wish to view recent changes on GitHub,
note that Clawpack is an *organization*, meaning that it is
comprised of several repositories.  Go to the 
`Clawpack GitHub <https://github.com/organizations/clawpack>`_ 
webpage to view all the repositories.

You might also view the 
`issues <https://github.com/organizations/clawpack/dashboard/issues>`_
associated with each Clawpack repository on
GitHub to see what bugs and features we are working on.

**Some of the major changes:**

* In all of the Clawpack codes, indices of the primary arrays `q` (for
  the solution) and `aux` (for auxiliary variables) have been reordered for
  better cache performance and to interface better with the PETSc code (used
  in as an option in PyClaw).  For example, in the two-dimensional Clawpack
  4.x code, `q(i,j,m)` denoted the m'th component of the solution vector in
  the `(i,j)` grid cell.  With this convention the various components of the
  solution in a single grid cell are scattered in memory with a stride of
  `mx*my`.  
  In Clawpack 5.0, the indexing for the same value is `q(m,i,j)` so that
  the components of `q` in a single grid cell are continguous in memory.

  Note that this means user routines such as `qinit.f`, `setaux.f`,
  and Riemann solvers must be modified.

* The calling sequence of Riemann solvers has been modified by adding
  `maux` (the number of auxiliary variables) as another paramter.
  This is required because of the reordering of indices so that
  `aux(ma,i,j)` is now the `ma` element of the `aux` vector in the `(i,j)`
  cell.  The leading dimension of `aux` is assumed to be `maux` and is
  required in declaring this variable.  

* Calling sequences of many subroutines have changed, so users converting
  code from Clawpack 4.x should carefully compare the calling sequences in 
  any custom Fortran code to those in relevant examples, or to the default
  versions in the libraries.

* Many Riemann solvers for different applications are now found in the 
  `riemann repository <https://github.com/clawpack/riemann>`_.
  In the future major changes may be made to the form of the Riemann solvers
  to allow more flexibility.

* The names of many input variables in `setrun.py` have been changed to
  clean things up and be more systematic.  Several options that used to be
  specified by obscure means have clarified, and some new options have been
  added.  For details and documentation on the new parameters, see:
  
   * :ref:`setrun_changes` 
   * :ref:`setrun`
   * :ref:`setrun_amrclaw`
   * :ref:`setrun_geoclaw`
  
* The classic single-grid Clawpack code (without AMR) is now in the 
  `classic repository <https://github.com/clawpack/classic>`_ 

* The AMRClaw code is now in the 
  `amrclaw repository <https://github.com/clawpack/amrclaw>`_.
  Some new capabilities have been added, e.g.:   
  
   * It is now possible to specify refinement *regions*, previously only
     supported in GeoClaw.  For a description, see :ref:`refinement`.

