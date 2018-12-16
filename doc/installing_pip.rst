.. _installing_pip:

**************************************
Installation instructions (pip)
**************************************

For other installation options, see :ref:`installing`.

See also:

* :ref:`clawpack_packages`
* :ref:`changes`
* :ref:`previous`
* :ref:`trouble_installation`

**Register:** Please `register <http://depts.washington.edu/clawpack/register/index.html>`_
if you have not already done so.  This is very useful in helping
us track the extent of usage, and important to the :ref:`funding` agencies
who support this work.


**Prerequisites:** Before installing, check that you have the :ref:`prereqs`.

*Installing* Clawpack requires downloading some version and then setting
paths so that Python import statements (and possibly Fortran Makefiles) find
the desired version.  `pip` can be used to reset Python paths as well as to
download a new version of Clawpack and set the path appropriately.  See
:ref:`python_path` for more information.

Installing with `pip` also compiles Riemann solvers written in Fortran for
use in PyClaw.  If you get a Fortran error message when installing, see
:ref:`trouble_f2py`.


.. _install_quick_all:

Quick Installation of all packages
=====================================

The recommended way to install the latest release of Clawpack, for
using PyClaw and/or the Fortran packages, is to give the following pip
install command (you might want to first read the notes below to see if you
want to change anything in this command)::  

    pip install --src=$HOME/clawpack_src --user -e \
        git+https://github.com/clawpack/clawpack.git@v5.5.0#egg=clawpack-v5.5.0

This will install Clawpack into the directory
`$HOME/clawpack_src/clawpack-v5.5.0`, or the top 
installation directory can be changed by modifying the `--src` target.

See :ref:`clawpack_components` for a list of what's included in this top level.

The `--user` flag is necessary if you are installing on a shared computer
where you do not have root access.  If you do have root access and want it
to be available to all users, you can omit this flag.  See notes below for
more information.

In order to use the Fortran codes within Clawpack (`classic`,
`amrclaw`, or `geoclaw`), you should then set the environment
variable `CLAW` to point to the `clawpack-v5.5.0` directory within
the installation directory `$HOME/clawpack_src`, and `FC` to point
to the desired Fortran compiler, e.g. in the bash shell::

    export CLAW=$HOME/clawpack_src/clawpack-v5.5.0
    export FC=gfortran

**Note:** 
You may want to set `CLAW` even if you are only using PyClaw, since `$CLAW` is
sometimes used in this documentation to indicate the top level of the
Clawpack source directory structure.

See :ref:`setenv` for more information, and :ref:`python_path` if you are
having problems with importing Python modules.

.. _install_quick_pyclaw:

Quick Installation of only PyClaw
=====================================


If you only want to use PyClaw (and associated Python
tools, e.g. VisClaw for visualization), they you could do::

    pip install --user clawpack

or, more specifically, ::

    pip install --user clawpack==v5.5.0

However, if you think you might want to use the Fortran packages as well
(Classic, AMRClaw, GeoClaw) and/or want easier access to the Python source
code, it is recommended that you follow the instructions above for 
:ref:`install_quick_all` (or see other :ref:`installing`).


Next steps:
-----------

Once Clawpack is installed, you can go to one of the following pages to get
started:

- :ref:`first_run_pyclaw`
- :ref:`first_run_fortran`

Using pip to install a different version
-----------------------------------------

Using `pip` to download and install actually clones Git repositories from
https://github.com/clawpack/clawpack.  If you are comfortable with
Git you can use the same top repository to update Clawpack or switch
to other versions.  However, if you have made any changes to files
that are tracked by Git in this set of directories and then try to
update or check out other branches, you may run into merge conflicts.

Instead, you can always install another branch by doing a new
`pip install` into a different subdirectory of `clawpack_src`, e.g. ::

    export CLAW_VERSION=v5.3.1  # used several places in next commands
    pip install --src=$HOME/clawpack_src --user -e \
        git+https://github.com/clawpack/clawpack.git@$CLAW_VERSION#egg=clawpack-$CLAW_VERSION
    export CLAW=$HOME/clawpack_src/clawpack-$CLAW_VERSION

If this version doesn't already exist on your computer then it will clone
the necessary repositories.

If you already have a different version of Clawpack in some directory 
obtained by any means (e.g. from a tarfile), then you can set the paths
properly via::

    export CLAW=/full/path/to/desired/version/of/clawpack
    cd $CLAW
    pip install --user -e .   # note trailing dot indicating "this directory"


Experimenting with code in the examples directories
---------------------------------------------------

We suggest that if you want to experiment extensively with examples or
modify an example to solve your own problem, you first copy a directory out
of the source code tree to a different location, in order to minimize
confusion if you later want to update to a different version of clawpack.  See
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

- When the `--user` flag is omitted, the `pip install` will modify a
  system-wide file `easy-install.pth` to add the path. This requires
  root permission.  When the `--user` flag is used, this path will
  instead be added to an `easy-install.pth` file that is within
  your user directory structure. See :ref:`python_path` for information on
  finding these files.

- If you use `pip` to install or switch versions then you should **not** set
  the environment variable `PYTHONPATH`.  See :ref:`python_path` for more
  information.

- If you wish to point to a different version of the Clawpack Python tools, 
  you need to rerun `pip install`.

- If you get a Fortran error message when installing, see
  :ref:`trouble_f2py`.

If you cannot get this to work, consider other :ref:`installing` and 
`raise an issue <https://github.com/clawpack/doc/issues>`_ to let us know
what went wrong.

