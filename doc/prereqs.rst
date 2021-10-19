:orphan:

.. _prereqs:

Installation Prerequisites
===========================

Installing and using Clawpack requires the following:

.. _prereqs_os:

Operating system
------------------

- Linux
- Mac OS X: For the Fortran packages, you need to have the `Xcode developer tools
  <http://developer.apple.com/technologies/tools/xcode.html>`_ installed in
  order to have `make` working.  PyClaw does not require `make`.


.. _prereqs_fortran:

Fortran
-------

To use the Fortran versions of the PDE solvers (:ref:`contents_fortcodes`), 
you will need 
`gfortran <http://gcc.gnu.org/wiki/GFortran>`_ or another F90 compiler.

See :ref:`fortran_compilers` for more about which compilers work well with
Clawpack.

.. _prereqs_python:

Python
------

- Python Version 3.0 or above (much of the code works in Python2, but this
  is no longer officially supported; see :ref:`python-three`).
- `NumPy <http://www.numpy.org/>`_  (for PyClaw/VisClaw)
- `matplotlib <http://matplotlib.org/>`_ (for PyClaw/VisClaw)

There are many ways to install the Python scientific stack, e.g. via
`apt-get` or `brew`.  On MacOS, you might check out 
`ScipySuperpack for Homebrew <http://stronginference.com/ScipySuperpack/>`__.

.. _prereqs_pip:

pip
---

If you are installing via `pip install` then you need `pip`.
If you need to install it, see 
`<https://pip.pypa.io/en/stable/installation/>`_

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

