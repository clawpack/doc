
.. _clawpack_components:

===================
Clawpack components
===================


Clawpack is developed using the `git <http://git-scm.com/>`_ version control
system and all the source code is openly available via the
`Clawpack GitHub Organization <https://github.com/orgs/clawpack>`_.

The code is organized in several independent git repositories.  One of these
is the `clawpack/clawpack <https://github.com/clawpack/clawpack>`_
super-repository that is used to coordinate versions between other
repositories.  If you are interested in cloning the code directly from
GitHub and/or helping develop Clawpack, see :ref:`developers`.

If you download a tar file of Clawpack, as described in
:ref:`install_clawpack`, then you will obtain a top level directory that has the
following subdirectories:

* `classic`  (Classic single-grid Fortran code)
* `amrclaw` (:ref:`amrclaw`, AMR version of Fortran code)
* `riemann`  (Riemann solvers, in Fortran, also used by PyClaw)
* `geoclaw`  (GeoClaw for geophysical flows)
* `clawutil`  (Utility functions, Makefile.common used in multiple repositories)
* `pyclaw`  (Python version that includes SharpClaw and PETSc parallelization)
* `visclaw`  (Python graphics and visualization tools)

These correspond to individual GitHub repositories.  

.. _other_repos:

Other repositories
-----------------------

Other repositories in the
`Clawpack GitHub Organization <https://github.com/orgs/clawpack>`_
may be of interest to some users:

* `apps` contains additional applications, see :ref:`apps`.
* `doc` contains `sphinx <http://sphinx.pocoo.org/>`_ input files for the
  Clawpack documentation.
* `clawpack.github.com` contains the html files that appear on the web.
* `clawpack-4.x` contains the latest version of Clawpack 4.x, the legacy
  code.
