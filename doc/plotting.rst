
.. _plotting:

***************************************
Plotting options 
***************************************

.. _plotting_postproc:

Plotting as post-processing
---------------------------

Running a Fortran version of Clawpack produces output files that can then be
read in to a graphics package as a post-processing step.  If you understand
the format of the output files, you can write custom graphics routines using
your favorite visualization tools.  The output formats are described in the
section :ref:`output_styles`.

Clawpack  includes utilities for plotting using Python, and most of the
documention assumes you will use these tools.  See
:ref:`plotting_python` for a description of these.
The Python package `matplotlib <matplotlib?>`_ 
is used under the hood for 1d and 2d plots, but the tools provided with
Clawpack simplify some common tasks since they handle looping over all grid
patches as is generally required when plotting AMR data.

Early versions of Clawpack used Matlab for plotting.
See :ref:`matlabplots` for pointers if you wish to use these tools.
**Matlab tools deprecated?**

The advantages of using the Python options are:

 * Python and the graphics modules used in Clawpack are open source.  Since
   Clawpack itself is open source we find it desirable to also have an open
   source plotting open for viewing the results.

 * The Python tools developed so far (mostly for 1d and 2d data sets) are
   more powerful than the Matlab versions they replace, and can be used for
   example to automatically generate html versions of multiple plots each
   frame over all frames of a computation, to generate latex versions of the
   output, as well as to step through the frames one by one as with the
   Matlab tools.  It is easier to specify a set of multiple plots to be
   produced for each frame.

 * Matlab graphics are somewhat limited for 3d data sets, whereas several
   open source visualization tools such as `VisIt
   <https://wci.llnl.gov/codes/visit>`_ (developed at Lawrence Livermore
   National Laboratory) are much better for dealing
   with large data sets, AMR meshes, etc.  VisIt has Python bindings and 
   we are currently extending our tools to work with VisIt.  If you are
   already a VisIt user, note that VisIt has a Claw reader that can be used to
   import data from Clawpack, see `Application Toolkit Formats
   <http://www.visitusers.org/index.php?title=Detailed_list_of_file_formats_VisIt_supports#Application_Toolkit_Formats>`_.

   We are also considering developing tools for use with
   `Mayavi <http://code.enthought.com/projects/mayavi>`_.

 * Python is a powerful language that can be scripted to perform multiple
   runs, such as in a convergence test, and collect the results in tables or
   plots.  We are developing tools to simplify this process.


.. _plotting_onfly:

Plotting on the fly
---------------------------

**Describe options.**

