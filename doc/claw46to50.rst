
.. _claw46to50:

##########################################
Converting from Clawpack 4.6 to 5.0
##########################################

(If you are converting code from Clawpack 4.3, see :ref:`claw43to46`.)

Many input parameters have been renamed and some new options have been
added in Clawpack 5.0.  See :ref:`setrun_changes`.

Python conversion tool
----------------------

A first pass at the conversion of *setrun.py*, *setplot.py* and the
*Makefile* can often be achieved by typing::

    $ python $CLAW/clawutil/src/python/clawutil/conversion/convert46to50.py

in your application directory.  You should then inspect the files generated
and fix any broken links, etc.

The original versions of various files will have `_4.x` appended to the file
name for reference.  When conversion is complete, these files can be
deleted.


**Notes:**

This does not yet work for all variants of the code.

Old AMRClaw codes are often in a subdirectory *amr* of an application
directory, and the directory above may contain Fortran files or other files
used by the AMR code.  Typically you will want to combine these in one
directory.

The `Makefile` is currently not converted properly -- a generic `Makefile`
is added to the directory but must be customized to point to any local
Fortran codes, for example.  In particular, make sure the Makefile points to
the correct Riemann solver(s), either a local file or a library routine from
the `$CLAW/riemann/src` directory.

The indices in `q` and `aux` arrays were permuted in Clawpack 5.0 relative
to early versions, e.g. the `m`th component of `q` in grid cell `(i,j)` is
now `q(m,i,j)` rather than `q(i,j,m)`.  The conversion script attempts to do
this reordering if it sees a pattern of a suitable form, but you should
carefully check your own local routines such as `qinit` or `setaux` to make
sure this has been done properly.

Calling sequences of several routines have also been changed and will need
to be adjusted by hand for any Fortran routines in your application directory. 
See :ref:`user_routines` for calling sequences of the routines that
most frequently are provided by users.  If you specify your own
Riemann solver, see also :ref:`riemann`, and if you have custom
boundary conditions, see :ref:`bc`.

Note in particular that parameter `maxmx` (and `maxmy`, `maxmz` in more
dimensions) is no longer in the calling sequence.  In earlier versions of
Clawpack this indicated the declared dimension of the `q` and `aux` arrays.
It is now assumed the arrays are dimensioned properly since dynamic memory
allocation is generally used at run time based on `mx` (resp. `my`, `mz`).
You should remove these from the calling sequence and also modify the
declaration of input parameters to use `mx` in place of `maxmx`, etc.

The classic code no longer requires a driver routine `driver.f`.  In earlier
versions of Clawpack this was used to declare the `q` and `aux` arrays to be
sufficiently large for the size of the problem to be solved.  (And
specifying a larger value for `mx` led to a run-time error.)  In Clawpack-5,
a library routine `driver.f90` is provided that calls the Clawpack routines,
which now use dynamic memory allocation to allocate the required arrays at
run time.


