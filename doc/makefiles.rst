
.. _makefiles:


=====================================
Clawpack Makefiles
=====================================

Makefiles for the Fortran code in many repositories 
use the common Makefile found in `$CLAW/clawutil/src/Makefile.common`,
so you must have the `clawutil` repository.

**New in 5.4.0.** The `Makefile` also typically refers to a common list of
library routines needed for this particular example or application code,
rather than listing all the files individually in every `Makefile`.  See
:ref:`makefiles_library` for more details on how to specify local files in
place of library files if you need to replace a default file.

In most directories with a `Makefile` you can type::

    $ make help

to find out what options are available.

Applications directory Makefiles
--------------------------------

.. _makefiles_output:

output
++++++

In applications directories, compiling and running the code can usually be
accomplished via::

    $ make .output

This checks dependencies using the data of the hidden file `.output` that is
created after the code has successfully run.  If any Fortran codes have been
modified since this date, the code is first recompiled.  If the `setrun.py`
script has been changed more recently, then the data files are first
recreated.

If you want to re-run the code and you get::

    $ make .output
    make: `.output' is up to date.

then you can force it to run again by removing the file `.output`::

    $ rm -f .output
    $ make .output

This happens for example if you changed something that you know
will affect the output but that isn't in the Makefile's set of
dependencies, or if the code bombed or was aborted before completion.

The hidden file ``.output`` contains a single line, which is the path to the
directory where the output resides (as specified by the ``CLAW_outdir`` variable
in the ``Makefile``).  This file is used by the interactive plotting routines, as
described in :ref:`plotting`.

You can also do::

    $ make output

(with no dot before ``output``) to run the code without checking dependencies.
This is sometimes handy but note that
if you modify the ``setrun`` function
and then do ``make output``, it will not use the new parameter values.
You must do ``make .data`` to regenerate the data files used by Clawpack.
This would be done automatically by ``make .output``, for which ``.data`` is a
dependency.

.. _makefiles_plots:

plots
++++++

In applications directories, plotting results computed by Clawpack can generally
be accomplished via::

    $ make .plots

This checks dependencies using the date of the hidden file `.plots`.

This creates a set of webpages that show the plots, as described further in
:ref:`plotting`.  There are other interactive plotting options also described
there.

Starting in 4.5.1, you can also do

    $ make plots

(with no dot before ``plots``) to plot the output without checking dependencies.
This insures that the code will not be run again and is sometime safer than
``make .plots``, which may attempt to run the code if something appears out of
date. 


Variables
+++++++++

A number of variables are defined in the Makefiles of application
directories.  For example, output is directed to the subdirectory specified
by the variable `OUTDIR`.  To change this, simply modify the Makefile before
typing "make .output".  Alternatively, you can modify the variable from the
command line, e.g.::

    $ make .output OUTDIR=run1

to direct output to a subdirectory named `run1`.

Compiler flags
++++++++++++++

Compiler flags can be changed by modifying the `FFLAGS` variable in the
Makefile.  If you change compiler flags you will generally need to recompile
all the Fortran files and the Makefile dependencies will not detect this.
To force recompilation of all files, use the "make new" option, e.g. to
recompile with the `-g` flag for debugging::

    $ make new FFLAGS=-g

See :ref:`fortran_compilers` for more about compiler flags.

Duplicate Base Source Name
++++++++++++++++++++++++++

Fortran source files with the same base name but different suffixes can cause
unexpected source files to be compiled.  This occurs as the Makefiles are
structured to use the free-format Fortran source files **.f90* before the
fixed-format source files with *.f*.  For example, if someone specified
*qinit.f* in the Makefile but there was *qinit.f90* file that had already been
compiled then the compiler would assume that object file is up to date.  The
simple fix for this is to make sure to run *make new* to ignore all the old
object files and recompile all the source in the Makefile.