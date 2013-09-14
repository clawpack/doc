

.. _openmp:

**************************************
Using OpenMP
**************************************

Most of the Clawpack Classic, AMRClaw and GeoClaw Fortran codes include
OpenMP directives for making use of multicore shared memory machines.  

**Note:** Versions of gfortran before 4.6 are known to have OpenMP bugs.
You should use a recent version or a different compiler if you want to use
OpenMP.

To invoke OpenMP you need to compile the entire code with appropriate
compiler flags (see :ref:`fortran_compilers`).  For example, with gfortran
and the bash shell you could do::

    export FFLAGS='-O2 -fopenmp'  # or hardwire FFLAGS in the Makefile
    make new

in an application directory, which should recompile all of the library
routines as well.

Then you may want to specify how many threads OpenMP should split the work
between, e.g. ::

    export OMP_NUM_THREADS=2

If you do not set this environment variable some default for your system
will be used.  

You may also need to increase the stack size if the code bombs for no
apparent reason (and no useful error message)::

    export OMP_STACKSIZE=16M

and also::

    ulimit -s unlimited

On a Mac this isn't allowed and the best you can do is ::

    ulimit -s hard


To stop using OpenMP you could do::

    export FFLAGS=-O2   # or hardwire FFLAGS in the Makefile
    make new

.. _openmp_amr:

Using OpenMP with AMR 
---------------------

The code in AMRClaw and GeoClaw is parallelized by splitting the list of
patches that must be advanced in time between threads, and then each grid
patch is handled by a single thread.  For this reason good performance will
be seen only when there are a sufficiently large number of patches at each
level relative to the number of threads.  For this reason it is recommended
that the parameter `max1d` be set to 60 in the modules

* `$CLAW/amrclaw/src/2d/amr_module.f90`
* `$CLAW/amrclaw/src/3d/amr_module.f90`

when OpenMP is used.  This limits the size of any patch to have at most
`max1d` grid cells in each direction.  If OpenMP is not used, a larger value
of `max1d` might give somewhat better performance since there is less
overhead associated with passing boundary values in ghost cells and other
per-patch work.  However, this is generally negligible and `max1d=60` is the
default value set in the code.   If you do change this value, remember to
recompile everything via::

    make new


.. _openmp_fixedgrids:

Fixed grid output in GeoClaw
----------------------------

The original fixed grid output routines are not thread safe and so OpenMP
should not be used if you want to produce output on fixed grids.

The newer fgmax routines that keep track of maxima on fixed grids should be
thread safe.

