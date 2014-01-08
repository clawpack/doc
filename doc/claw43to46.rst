
.. _claw43to46:

##########################################
Converting from Clawpack 4.3 to 4.6
##########################################

For users who want to migrate code from 4.3 to 5.0, this may be a useful
intermediate step, followed by migration from 4.6 to 5.0 using the script
described at :ref:`claw46to50`.

The Python interface (using `setrun.py` and `setplot.py`) was first
introduced in 4.4, so the main step needed to convert from 4.3 is to create
these files, and to make a number of changes to the `Makefile`.  

If you are doing this by hand, you should convert directly to 5.0 form.

In some cases it will be easiest to do the bulk of the work using scripts.
A first pass of conversion to 4.6 form can be done by executing::

    $ python $CLAW/clawutil/src/python/clawutil/conversion/convert43to46.py

in your application directory.  You should then inspect the files generated
and fix any broken links, etc.

After this, see :ref:`claw46to50`.

.. warning:: This migration script from 4.3 to 4.6 only works for classic
   (single grid) codes in 1d and 2d, not AMRClaw codes.

