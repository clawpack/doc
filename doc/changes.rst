.. _changes:

==========================
Recent changes
==========================

.. _planned_for_50:

Changes in Clawpack 5.0
================================

Clawpack 5.0 is a major reorganization of the Clawpack code base that has
been going on for several years.  We hope to release a version soon that ill
be easy to install and use for general users.  Currently it still in a state
of flux but developers and other brave souls can use it by following the
instructions found at :ref:`setup_dev`.
Note that in order to use Clawpack 5.0 currently you need to clone a number
of github repositories.

This documentation is also under construction and parts of it have not yet been
updated to Clawpack 5.0.

Substantial changes are planned for Clawpack 5.0.  See the 
`Clawpack wiki <https://github.com/clawpack/doc/wiki>`_ for
details.  **This is out of date**

Note that Clawpack is an *organization* on GitHub, meaning that it is
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
  `maux` (the number of auxiliary variables) as another paramter at the end.
  This is required because of the reordering of indices so that
  `aux(ma,i,j)` is now the `ma` element of the `aux` vector in the `(i,j)`
  cell.  The leading dimension of `aux` is assumed to be `maux` and is
  required in declaring this variable.  

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
  
* The single-grid Clawpack code (no AMR) is now in the 
  `classic repository <https://github.com/clawpack/classic>`_ 
  This is being rewritten in Fortran 90 (still in progress).

* The AMRClaw code is now in the 
  `amrclaw repository <https://github.com/clawpack/amrclaw>`_.
  Some new capabilities have been added:   
  
   * It is now possible to specify refinement *regions*, previously only
     supported in GeoClaw.  For a description, see :ref:`flag`.


.. _new_in_claw4x:

Clawpack 4.x
==========================

For documentation and recent changes to the Clawpack 4.x version, please see
`Clawpack 4.x documentation
<http://depts.washington.edu/clawpack/users-4.x/index.html>`_

