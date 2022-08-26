.. _installing_pip:

**************************************
pip install instructions
**************************************


**Note:** If you only plan to use the Fortran versions of the solvers 
(rather than :ref:`pyclaw`), and you run into problems with pip,
then you might want to try :ref:`installing_fortcodes`.



.. _install_quick_pyclaw:

Quick Installation of PyClaw with pip
=====================================

Please see :ref:`clawpack_packages` before installing, particularly
if you are not sure whether you will
be using the Fortran versions of the PDE solvers 
(:ref:`contents_fortcodes`) or the :ref:`pyclaw` version of the PDE solvers.
See :ref:`installing` for other installation options.

**Prerequisites:** Before installing, check that you have the :ref:`prereqs`.

If you only want to use PyClaw (and associated Python
tools, e.g. VisClaw for visualization), then the simplest way to install
Clawpack is via::

    pip install --user clawpack

or, more specifically, ::

    pip install --user clawpack==v5.9.0

or you can choose a previous version from the `PyPi history <https://pypi.org/project/clawpack/#history>`__.

However, note that this does not download the Fortran codes in a way that they
can be used for :ref:`contents_fortcodes`.

If you think you might want to use the Fortran packages as well
(Classic, AMRClaw, GeoClaw) and/or want easier access to the Python source
code, it is recommended that you follow the pip instructions below. 


.. _install_quick_all:

Quick Installation of all packages with pip
============================================

The recommended way to install the latest release of Clawpack, for
using both PyClaw and the Fortran packages, is to use pip, e.g. with the
following command 
**(you might want to first read the notes below to see if you
want to change anything in this command)**::  

    pip install --src=$HOME/clawpack_src --user -e \
        git+https://github.com/clawpack/clawpack.git@v5.9.0#egg=clawpack-v5.9.0 \
        --use-deprecated=legacy-resolver
        
        
**Notes:** 

- With older versions of `pip`, the flag 
  `--use-deprecated=legacy-resolver`
  may not be recognized and is not needed.
  
- Using pip to install will also check some python
  :ref:`prereqs` and may update these on your system, and will use f2py to
  convert Fortran Riemann solvers to Python versions.  See 
  :ref:`installing_options` if you want more control.

- This will download Clawpack (via a git clone) into the directory
  `$HOME/clawpack_src/clawpack-v5.9.0`.  The top 
  installation directory can be changed by modifying the ``--src`` target 
  (or omit this part to put it in your current working directory).
  If you have already downloaded Clawpack via a different mechanism then
  see :ref:`pip_switch_version` rather than using the above command.
    
- See :ref:`clawpack_components` for a list of what's included in this top
  level directory.
  
- The ``--user`` flag is necessary if you are installing on a shared computer
  where you do not have root access.  If you do have root access and want it
  to be available to all users, you can omit this flag.  See notes below for
  more information.
  
- The ``-e`` flag makes it an "editable" install, leaving the source code in
  place and allowing you to modify it if desired.
  (Otherwise, by default, pip would move the python code to some
  `site-packages` directory and delete everything else.)
  
- In order to use the Fortran codes within Clawpack (`classic`,
  `amrclaw`, or `geoclaw`), you should then set the environment
  variable `CLAW` to point to the `clawpack-v5.9.0` directory within
  the installation directory `$HOME/clawpack_src`, and `FC` to point
  to the desired Fortran compiler, e.g. in the bash shell::
  
        export CLAW=$HOME/clawpack_src/clawpack-v5.9.0
        export FC=gfortran


- You may want to set `CLAW` even if you are only using PyClaw, since `$CLAW` is
  sometimes used in this documentation to indicate the top level of the
  Clawpack source directory structure.

Installing with `pip` also compiles Riemann solvers written in Fortran for
use in PyClaw.  If you get a Fortran error message when installing, see
:ref:`trouble_f2py`.

See :ref:`setenv` for more information, and :ref:`python_path` if you are
having problems with importing Python modules.


Next steps:
-----------

Once Clawpack is installed, you can go to one of the following pages to get
started:

- :ref:`first_run_pyclaw`
- :ref:`first_run_fortran`
- :ref:`trouble_installation`


.. _pip_switch_version:

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

See :ref:`python_path` if you are having problems with the wrong version
being imported.


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
  you need to rerun `pip install` (or use `pip uninstall clawpack` to
  remove clawpack from the search path controlled by pip).

- If you get a Fortran error message when installing, see
  :ref:`trouble_f2py`.

If you cannot get this to work, consider other :ref:`installing` and 
`raise an issue <https://github.com/clawpack/doc/issues>`_ to let us know
what went wrong.

