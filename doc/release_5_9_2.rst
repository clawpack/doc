:orphan:
  
.. _release_5_9_2:

===============================
v5.9.2 release notes
===============================

Clawpack 5.9.2 was released on November 4, 2023. See :ref:`installing`.

Permanent DOI: http://doi.org/10.5281/zenodo.XXX


Changes relative to Clawpack 5.9.2 (October 2, 2023) are shown below.

To see more recent changes that are in the the master branch but not yet
released, see :ref:`changes_to_master`.


Follow the links to see changes that have been made to the master branch of
each repository since the last release (v5.9.2) on November 4, 2023.

These changes should appear in the next release.  If you need them now,
see :ref:`developers` for instructions on cloning and installing from the
master branch. 

To see documentation that has already been developed to accompany any new
features listed below, click on the "dev" branch of the documentation, in
the menu on the left hand side of this page.


General changes
---------------

The build process for the Python modules has been completely redone using
`meson <https://mesonbuild.com/>`__ in place of `distutils`, which is being
deprecated.  We chose `meson` since this is now being used by many of the core
scientific python projects that we use, e.g. `numpy` and `scipy`.  This should
not affect most users, except for some changes to the recommended installation
options, see :ref:`installing`.

Many Python modules were cleaned up by removing transition code that was useful
for Python2 users but is no longer needed since we now require Python3 in
general.

Otherwise, mostly minor changes and bug fixes.

Changes to classic
------------------


See `classic diffs
<https://github.com/clawpack/classic/compare/v5.9.2...master>`_

Changes to clawutil
-------------------

Some new data objects were added to `clawpack.clawutil.data` for GeoClaw 1d
and Boussinesq solvers, but these will not be used until the next major release.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.9.2...master>`_

Changes to visclaw
------------------

 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.9.2...master>`_

Changes to riemann
------------------


See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.9.2...master>`_

Changes to amrclaw
------------------


See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.9.2...master>`_

Changes to geoclaw
------------------

The `setrun` parameter `runclaw.geo_data.sphere_source` was added to allow
experimenting with the spherical source term that is currently missing from
the default GeoClaw code, see :ref:`sphere_source`, which now includes a
link to a document with more description of the problem and computational
examples.

See `geoclaw diffs <https://github.com/clawpack/geoclaw/compare/v5.9.2...master>`_


Changes to PyClaw
------------------


See `pyclaw diffs <https://github.com/clawpack/pyclaw/compare/v5.9.2...master>`_

===========================
Other Clawpack Repositories
===========================

The repositories below are not included in the Clawpack tarfile or pip
install, but changes to these repositories may also be of interest.

- `apps diffs
  <https://github.com/clawpack/apps/compare/v5.9.2...master>`_

- `doc diffs
  <https://github.com/clawpack/doc/compare/v5.9.x...dev>`_

- `docker-files diffs
  <https://github.com/clawpack/docker-files/compare/v5.9.2...master>`_
