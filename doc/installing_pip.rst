.. _installing_pip:

**************************************
Installation instructions (new)
**************************************

These instructions are a work in progress.  Suggestions welcome.

For older installation instructions that contains more options, see
:ref:`installing`.

See also:

* :ref:`clawpack_packages`
* :ref:`changes`
* :ref:`previous`
* :ref:`trouble_installation`

.. _install_prerequisites_pip:

Installation Prerequisites
================================================

**Operating system:**

- Linux
- Mac OS X (you need to have the `Xcode developer tools
  <http://developer.apple.com/technologies/tools/xcode.html>`_ installed in
  order to have "make" working)


**Fortran:**

- `gfortran <http://gcc.gnu.org/wiki/GFortran>`_ or another F90 compiler

See :ref:`fortran_compilers` for more about which compilers work well with
Clawpack.

**Python:**

- Python Version 2.7 or above (but **not** 3.0 or above, which is not backwards compatible)
- `NumPy <http://www.numpy.org/>`_  (for PyClaw/VisClaw)
- `matplotlib <http://matplotlib.org/>`_ (for PyClaw/VisClaw)

The `Anaconda Python Distribution <https://docs.continuum.io/anaconda/index>`_
is an easy way to get all of these. 
See :ref:`python` for more information on
installing the required modules and to get started using Python if
you are not familiar with it.

**pip:**

You may already have pip, in particular the Anaconda Python distribution
contains pip. If you need to install it, see 
`<https://pip.pypa.io/en/stable/installing/>`_


**Git:**

You may already have Git, in particular the Xcode tools on 
Mac OSX contains Git.  If you need to install it, see `the Git book
<https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_.

.. _install_quick:

Quick Installation of all packages
=====================================

Please `register
<http://depts.washington.edu/clawpack/register/index.html>`_ if you have not
already done so.  This is purely optional, but is useful in helping us track
the extent of usage.

The recommended way to install the latest release of Clawpack, for
using PyClaw and/or the Fortran packages, is to give the following pip
install command::  

    pip install --src=$HOME/clawpack_src -e git+https://github.com/clawpack/clawpack.git@v5.3.1#egg=clawpack

This will install Clawpack into the directory `$HOME/clawpack_src/clawpack`, or the
installation directory can be changed by modifying the `--src` target
in this command.

In order to use the Fortran versions, you should then set the environment
variable `CLAW` to point to this directory, and `FC` to point to the desired
Fortran compiler, e.g. ::

    export CLAW=$HOME/clawpack_src/clawpack
    export FC=gfortran

You may want to set `CLAW` even if you are only using PyClaw, since `$CLAW` is
sometimes used in this documentation to indicate the top level of the
Clawpack source directory structure.

**Notes about pip install:**

- The `-e` flag ("editable") results in the the source code
  remaining in the directory `$CLAW`, which includes all the Fortran packages as
  well as Python source.

- Other released versions can be obtained by changing `v5.3.1` to a
  different tag in the `pip install` command.
  You can switch between versions or upgrade to a newer version by
  repeating the above command with a different version number.
  The directory `$HOME/clawpack_src/clawpack` is a git clone of the top level
  `clawpack` repository and "installing" a different version checks out
  different tagged versions.

- Earlier versions of the installation instructions required setting the
  environment variable `PYTHONPATH`.  This is not necessary or desirable if
  you use the `pip install` option, which instead
  creates or modifies a file `easy_install.pth` that is
  found in the Python `site-packages` directory.
  The path to the clawpack source is added to this file and hence to the
  search path for Python.  This allows importing Clawpack modules, but note
  that directories specified here are searched before those specified by
  the environment variable `PYTHONPATH`.  So if you wish to point to
  a different version of the Clawpack Python tools, you need to rerun `pip
  install`, or else remove the path from the `easy_install.pth` file if 
  you need to use `PYTHONPATH`.


Once Clawpack is installed, you can go to one of the following pages to get
started:

- :ref:`first_run_pyclaw`
- :ref:`first_run_fortran`


