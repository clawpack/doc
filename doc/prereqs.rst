
.. _prereqs:

Installation Prerequisites
===========================

Installing and using Clawpack requires the following:

.. _prereqs_os:

Operating system
------------------

- Linux
- Mac OS X (you need to have the `Xcode developer tools
  <http://developer.apple.com/technologies/tools/xcode.html>`_ installed in
  order to have "make" working)


.. _prereqs_fortran:

Fortran
-------

- `gfortran <http://gcc.gnu.org/wiki/GFortran>`_ or another F90 compiler

See :ref:`fortran_compilers` for more about which compilers work well with
Clawpack.

Note that Fortran is required even if you only plan to use the "pure Python"
finite volume methods in PyClaw, since the Riemann solvers are mostly 
written in Fortran and compiled for use in PyClaw using 
`f2py <https://docs.scipy.org/doc/numpy-dev/f2py/>`_.

.. _prereqs_python:

Python
------

- Python Version 2.7 or above, or (**new in 5.4.0**) Python 3
- `NumPy <http://www.numpy.org/>`_  (for PyClaw/VisClaw)
- `matplotlib <http://matplotlib.org/>`_ (for PyClaw/VisClaw)

The `Anaconda Python Distribution <https://docs.continuum.io/anaconda/index>`_
is an easy way to get all of these. 
See :ref:`python` for more information on
installing the required modules and to get started using Python if
you are not familiar with it.

.. _prereqs_pip:

pip
---

If you are installing via `pip install` then you need `pip`.
You may already have it; in particular the Anaconda Python distribution
contains pip. If you need to install it, see 
`<https://pip.pypa.io/en/stable/installing/>`_

The version of `pip install` suggested for :ref:`install_quick_all` requires
a recent version of `pip`, so you may need to upgrade if you run into
problems.

.. _prereqs_git:

Git
----

If you are installing via `pip` using the command in
:ref:`install_quick_all`, or via `git clone`, then you need Git.
You may already have it; in particular the Xcode tools on 
Mac OSX contains Git.  If you need to install it, see `the Git book
<https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_.

