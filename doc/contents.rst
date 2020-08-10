.. _contents:

`The Clawpack Homepage <index.html>`__ contains a general introduction to
the Clawpack open source software project.

.. contents::
   :depth: 3

====================================================
Full Table of Contents
====================================================

This is the documentation for **Clawpack Version 5.6.0.** 
For documentation corresponding to older versions see the list of
past releases in the menu to the left.  The *future* version refers
to new documentation for features that have been merged into the
master branch of a Clawpack repository, but have not yet been
released.  To use one of these features, see :ref:`setup_dev`.

**What's New??** For release notes, summaries of changes between releases, 
and links to all the Github commit logs, see :ref:`releases`.

Overview and Getting Started
============================

.. toctree::
   :maxdepth: 2

   about

.. toctree::
   :maxdepth: 1
   
   releases
   packages
   installing
   installing_pip
   installing_more_options
   setenv
   first_run
   clawpack_components
   wp_algorithms
   trouble

.. toctree::
   :maxdepth: 1
   
   docker_image
   vm
   aws


Examples and Applications
============================


.. toctree::
   :maxdepth: 1
   
   apps
   fvmbook
   contribute_apps
   testing
   sphinxdoc

Classic, AMRClaw, and GeoClaw
==============================

Using the Fortran codes
-------------------------
General information that applies to Classic, AMRClaw, and GeoClaw.

.. toctree::
   :maxdepth: 1

   first_run_fortran
   fortran
   fortran_compilers
   f77_vs_f90
   user_routines
   openmp
   timing
   python
   makefiles
   makefiles_library
   b4run
   application_documentation
   setrun
   setrun_sample
   bc
   output_styles
   mapc2p
   restart
   newapp
   sharing
   gpu

AMRClaw: adaptive mesh refinement
---------------------------------

.. toctree::
   :maxdepth: 2

   amrclaw

GeoClaw: geophysical flows
--------------------------

.. toctree::
   :maxdepth: 2

   geoclaw

PyClaw
======

.. toctree::
   :maxdepth: 2

   pyclaw/index


Riemann
=======

All Clawpack packages make use of the same collection of Riemann solvers.

See also the new book `Riemann Problems and Jupyter Solutions
<https://bookstore.siam.org/fa16/bonus>`_ (SIAM, 2020),
which consists of a set of Jupyter notebooks illustrating
the basic concepts of Riemann problems and approximate solvers.

.. toctree::
   :maxdepth: 2

   riemann
   riemann/Shallow_water_Riemann_solvers

VisClaw: Plotting and Visualization Tools
=========================================

.. toctree::
   :maxdepth: 2
   
   plotting


Migrating applications from older versions of Clawpack
======================================================
If you are looking to run an application that was written
for Clawpack 4.x, this may be helpful.

.. toctree::
   :maxdepth: 2

   claw43to46
   claw46to50

.. _contents-developers-resources:

Developers' resources
=====================

.. toctree::
   :maxdepth: 1

   community
   developers
   howto_doc
   howto_release
   regression
   git_versions
   photos

See also :ref:`setup_dev`

References
==========

.. toctree::
   :maxdepth: 1

   fvmbook
   biblio


