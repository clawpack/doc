
.. _claw46to50:

##########################################
Converting from Clawpack 4.6 to 5.0
##########################################


Python conversion tool
----------------------

A first pass at the conversion of *setrun.py*, *setplot.py* and the
*Makefile* can often be achieved by typing::

    $ python $CLAW/clawutil/src/python/clawutil/conversion/convert.py

in your application directory.  You should then inspect the files generated
and fix any broken links, etc.

Currently this sort of works for 2d *amrclaw* applications only.
