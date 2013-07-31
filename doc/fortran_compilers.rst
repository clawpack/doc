
.. _fortran_compilers:

**************************************
Fortran Compilers
**************************************

This section is relevant to users who want to compile the fortran code in
the classic, amrclaw, or geoclaw branches.

.. _fortran_FC:

`FC` environment variable
-------------------------

Users should set the environment variable `FC` to point to the correct
compiler, e.g. in bash via::

    $ export FC=gfortran

Note that some versions of `make` will set `FC=f77` by default if no value
is specified, and adding a line to the Makefile such as::

    FC ?= gfortran

will not override this.  The common Makefile in
`$CLAW/clawutil/src/Makefile.common` now tests to see if `FC` is set to
`f77` and if so resets it to `gfortran` since much of Clawpack is not `f77`
compliant.  However, it is best to set the `FC` environment variable
yourself, e.g. in your `.bashrc` file.

.. _fortran_FFLAGS:

`FFLAGS` environment variable
-----------------------------

Compiler flags can be specified using the `FFLAGS` variable that can be set
in an application Makefile.  By default sample Makefiles now specify::

    FFLAGS ?= 

so that no flags are used unless the
environment variable `FFLAGS` is set already.  This line can be changed in
the Makefile, but it is often easiest to set an environment variable for the
flags you generally want to use.  

**Note:** If you change the flags you generally have to recompile *all* the
code, and this dependency is not handled automatically.  So always do::

    $ make new

before rerunning an example with `make .output` or `make .plots`.

.. _fortran_gfortran:

gfortran compiler
---------------------


*Some useful flags:*

* For debugging::

    FFLAGS = -g -Wall -fbounds-check -ffpe-trap=invalid,overflow,zero

* For optimizing::

    FFLAGS = -O2

* For using OpenMP::

    FFLAGS = -O2 -fopenmp

  In this case you should also set the environment variable `OMP_NUM_THREADS`
  to indicate how many threads to use.

  **Note:** Versions of gfortran before ?? are known to have OpenMP bugs.

.. _fortran_intel:

Intel fortran compiler
----------------------

Set the `FC` environment variable to `ifort`.

*Some useful flags:*

* For debugging::

    FFLAGS = -g -C -CB -CU -fpe0 -ftrapuv

* For optimizing::

    FFLAGS = -O2

* For using OpenMP::

    FFLAGS = -O2 -fopenmp

  In this case you should also set the environment variable `OMP_NUM_THREADS`
  to indicate how many threads to use.

