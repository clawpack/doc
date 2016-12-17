
.. _makefiles_library:


=====================================
Library routines in Makefiles
=====================================

See :ref:`makefiles` for general information on using the `Makefile` found
in application directories for the Fortran codes.

**New in 5.4.0.** The `Makefile` also typically refers to a common list of
library routines needed for this particular example or application code,
rather than listing all the files individually in every `Makefile`.  


For example, the directory `$CLAW/classic/examples/advection_1d_example1`
contains the lines::

    
    # ---------------------------------
    # package sources for this program:
    # ---------------------------------
    
    include $(CLAW)/classic/src/1d/Makefile.classic_1d
    
    # ---------------------------------------
    # package sources specifically to exclude
    # (i.e. if a custom replacement source 
    #  under a different name is provided)
    # ---------------------------------------
    
    EXCLUDE_MODULES = \
    
    EXCLUDE_SOURCES = \
    
    # ----------------------------------------
    # List of custom sources for this program:
    # ----------------------------------------
    
    MODULES = \
    
    SOURCES = \
      qinit.f90 \
      setprob.f90 \
      $(CLAW)/riemann/src/rp1_advection.f90
    

This indicates that the file `$CLAW/classic/src/1d/Makefile.classic_1d`
is used to specify the default list of files to be used.  These are
separated into `MODULES` and `SOURCES` since Fortran modules need to be
compiled before files that contain only subroutines or functions.

In the example shown above, we are
including three source code routines specific to this example: `qinit.f90`
and `setprob.f90` from this example directory, and the Riemann solver
`rp1_advection.f90` from the `riemann` repository.

The file `$CLAW/classic/src/1d/Makefile.classic_1d` contains::

    #get the directory of this makefile
    LIB:=$(CLAW)/classic/src/1d

    #list of common sources for classic 1d codes
    COMMON_SOURCES += \
      $(LIB)/qinit.f90 \
      $(LIB)/setprob.f90 \
      $(LIB)/setaux.f90 \
      $(LIB)/bc1.f \
      $(LIB)/b4step1.f90 \
      $(LIB)/driver.f90 \
      $(LIB)/claw1ez.f \
      $(LIB)/claw1.f \
      $(LIB)/copyq1.f \
      $(LIB)/inlinelimiter.f90 \
      $(LIB)/opendatafile.f \
      $(LIB)/out1.f \
      $(LIB)/src1.f90 \
      $(LIB)/step1.f90

For the `classic` 1d code there are no modules, only subroutines.

Replacing files with the same name as library files
---------------------------------------------------

Note that the list of default library routines above contains both
`qinit.f90` and `setprob.f90`.  The default versions of these files contain
subroutines that have the correct calling sequence but return without doing
anything.  Every application directory will generally contain a local
version of `qinit.f90` that sets the initial conditions.  Many applications
also have a custom version of `setprob.f90` that sets parameters, reads
custom input files, etc.  

Since the local `Makefile` contains `qinit.f90` and `setprob.f90` in its
list of `SOURCES`, the new make system (as of v5.4.0) will use these in
place of the library source files since they have identical names.  Hence we
do not need to list these routines explicitly in the list `EXCLUDE_SOURCES`
(although it wouldn't hurt to do so).

Note that if the local version were called `qinit.f` rather than
`qinit.f90`, the local version would also still be used in spite of the
different extension, since the base of the file name is the same.
(See :ref:`f77_vs_f90` for an important cautionary note on what
might go wrong if you have both a `.f` file and a `.f90` file with
the same base name in the same directory.)

Using a modified library routine with a different name
------------------------------------------------------

Suppose we want to use a local version of `bc1.f` in order to
implement some new boundary condition not included in the default version.
If we call the local file `bc1.f` then we can simply add it to the list
`SOURCES` in the local `Makefile` and it will be used in place of the
default library version as described in the previous section.

However, suppose our new boundary condition routine is called
`bc1_inflow.f` instead of `bc1.f`.  Then we would add this routine
to the list `SOURCES` in the local `Makefile` and in this case we
must also add `bc1.f` to `EXCLUDE_SOURCES` list.  After these changes
the local `Makefile` would contain these lines::


    EXCLUDE_MODULES = \

    EXCLUDE_SOURCES = \
      bc1.f \

    # ----------------------------------------
    # List of custom sources for this program:
    # ----------------------------------------

    MODULES = \

    SOURCES = \
      qinit.f90 \
      setprob.f90 \
      bc1_inflow.f \
      $(CLAW)/riemann/src/rp1_advection.f90

(It doesn't matter what order the files are listed in each section.)

