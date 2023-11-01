
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


.. _fortran_LFLAGS:

`LFLAGS` environment variable
------------------------------

The `LFLAGS` environment variable is used to provide flags that are needed when
linking the final binary.  The most likely use for this flag would be to link a
particular library with the binary (such as a NetCDF library) or provide a path
to a compiled module. If this variable is not set in the environment then
`LFLAGS` defaults to the relevant flags in `FFLAGS`.


.. _fortran_PPFLAGS:

Pre-Processor and the `PPFLAGS` environment variable
----------------------------------------------------

Compilers often provide a pre-processor that can scan source code before
compilation providing some ability to define variables at compile time or
transform the code.  Currently the pre-processor is always called before
Clawpack compilation to support optional dependencies, such as NetCDF support,
and some testing abilities.  The `PPFLAGS` environment variable is meant to
provide further control of the pre-processor.  


.. _fortran_gfortran:

gfortran compiler
---------------------


*Some useful flags:*

* For debugging::

    FFLAGS = -g -Wall -pedantic -fbounds-check -ffpe-trap=invalid,overflow,zero

* For optimizing::

    FFLAGS = -O2

* For using OpenMP::

    FFLAGS = -O2 -fopenmp

  In this case you should also set some  environment variables.  See
  :ref:`openmp` for details.   

  **Note:** Versions of gfortran before 4.6 are known to have OpenMP bugs.

* For using NetCDF::

    FFLAGS = -DNETCDF -lnetcdf -I$(NETCDF4_DIR)/include
    LFLAGS = -lnetcdf

  The `FFLAGS` can also be put into `PPFLAGS`.  Note that the variable
  `NETCDF4_DIR` should be defined in the environment.


.. _fortran_intel:

Intel fortran compiler
----------------------

Set the `FC` environment variable to `ifort`.

*Some useful flags:*

* For debugging::

    FFLAGS = -g -C -CB -CU -fpe0 -ftrapuv -fp-model precise

* For optimizing::

    FFLAGS = -O2

* For using OpenMP::

    FFLAGS = -O2 -qopenmp

  In this case you should also set the environment variable `OMP_NUM_THREADS`
  to indicate how many threads to use.

  For older versions of the ifort compiler, you may instead need::
  
    FFLAGS = -O2 -openmp

* For using NetCDF::

    FFLAGS = -DNETCDF -lnetcdf -I$(NETCDF4_DIR)/include
    LFLAGS = -lnetcdf

  Same as for gfortran above.
