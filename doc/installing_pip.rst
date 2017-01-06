.. _installing_pip:

**************************************
Installation instructions (pip)
**************************************

These instructions are a work in progress.  Suggestions welcome 
(`raise an issue <https://github.com/clawpack/doc/issues>`_).

For other installation options, see :ref:`installing`.

See also:

* :ref:`clawpack_packages`
* :ref:`changes`
* :ref:`previous`
* :ref:`trouble_installation`


.. _install_quick:

Quick Installation of all packages
=====================================

Please `register
<http://depts.washington.edu/clawpack/register/index.html>`_ if you have not
already done so.  This is purely optional, but is useful in helping us track
the extent of usage.

Check that you have the :ref:`prereqs`.

The recommended way to install the latest release of Clawpack, for
using PyClaw and/or the Fortran packages, is to give the following pip
install command::  

    pip install --src=$HOME/clawpack_v5.4.0 -e git+https://github.com/clawpack/clawpack.git@v5.4.0#egg=clawpack

This will install Clawpack into the directory
`$HOME/clawpack_v5.4.0/clawpack`, or the installation directory can
be changed by modifying the `--src` target in this command.  
We recommend naming the top level source directory (e.g.
`$HOME/clawpack_v5.4.0`) with a version number that agrees with the
version you are installing to avoid confusion in the future.  (See
below for installing other versions.)

In order to use the Fortran codes within Clawpack (`classic`,
`amrclaw`, or `geoclaw`), you should then set the environment
variable `CLAW` to point to the `clawpack` directory within
`$HOME/clawpack_v5.4.0`, and `FC` to point to the desired Fortran
compiler, e.g. ::

    export CLAW=$HOME/clawpack_v5.4.0/clawpack
    export FC=gfortran

**Note:** 
You may want to set `CLAW` even if you are only using PyClaw, since `$CLAW` is
sometimes used in this documentation to indicate the top level of the
Clawpack source directory structure.

See :ref:`setenv` for more information.

Next steps:
-----------

Once Clawpack is installed, you can go to one of the following pages to get
started:

- :ref:`first_run_pyclaw`
- :ref:`first_run_fortran`

Notes on using pip to install
-----------------------------

This approach clones Git repositories from
https://github.com/clawpack/clawpack.  If you are comfortable with
Git you can use the same top repository to update Clawpack or switch
to other versions.  However, if you have made any changes to files
that are tracked by Git in this set of directories and then try to
update or check out other branches, you may run into merge conflicts.

Instead, you can always install another branch by doing a new
`pip install` into a different place, e.g. ::

    export CLAW_VERSION=v5.3.1  # used several places in next commands
    pip install --src=$HOME/clawpack_$CLAW_VERSION -e git+https://github.com/clawpack/clawpack.git@$CLAW_VERSION#egg=clawpack
    export CLAW=$HOME/clawpack_$CLAW_VERSION/clawpack

We also suggest that if you want to experiment extensively with examples or
modify an example to solve your own problem, you first copy a directory out
of the source code tree to a different location, in order to minimize
confusion if you later want to update to a newer version of clawpack.  See
:ref:`newapp` for more details.

If you want to check out the `master` branch of the clawpack repositories or
work with other development versions, see :ref:`setup_dev`.

.. _trouble_pip:

Troubleshooting pip install
---------------------------

In case you run into problems with `pip install` or with changing version,
here are some tips:

- The `-e` flag ("editable") results in the the source code
  remaining in the directory `$CLAW`, which includes all the Fortran packages as
  well as Python source.

- Earlier versions of the installation instructions required setting the
  environment variable `PYTHONPATH`.  This is not necessary or desirable if
  you use the `pip install` option, which instead
  creates or modifies a file `easy_install.pth` that is
  found in the Python `site-packages` directory.
  The path to the clawpack source is added to this file and hence to the
  search path for Python.  This allows importing Clawpack modules, but note
  that directories specified here are searched before those specified by
  the environment variable `PYTHONPATH`.  

- If you wish to point to a different version of the Clawpack Python tools, 
  you need to rerun `pip install`, or else remove the path from the
  `easy_install.pth` file if you need to use `PYTHONPATH`.

- If you get a Fortran error message when installing, see
  :ref:`trouble_f2py`.

If you cannot get this to work, consider other :ref:`installing` and 
`raise an issue <https://github.com/clawpack/doc/issues>`_ to let us know
what went wrong.

