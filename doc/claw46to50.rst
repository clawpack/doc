
.. _claw46to50:

##########################################
Converting from Clawpack 4.6 to 5.0
##########################################

Many input parameters have been renamed and some new options have been
added.  See :ref:`setrun_changes`.



Python conversion tool
----------------------

A first pass at the conversion of *setrun.py*, *setplot.py* and the
*Makefile* can often be achieved by typing::

    $ python $CLAW/clawutil/src/python/clawutil/conversion/convert.py

in your application directory.  You should then inspect the files generated
and fix any broken links, etc.


**Note:**

This does not yet work for all variants of the code.

Old AMRClaw codes are often in a subdirectory *amr* of an application
directory, and the directory above may contain Fortran files or other files
used by the AMR code.  Typically you will want to combine these in one
directory.

The `Makefile` is currently not converted properly -- a generic `Makefile`
is added to the directory but must be customized to point to any local
Fortran codes, for example.
