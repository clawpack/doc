

.. _quick_surge:

*****************************************************************
Quick start guide for storm surge modeling
*****************************************************************

To get started with a storm surge computation it is best to refer to a previous
working example.  For example, you might start with 
`$CLAW/geoclaw/examples/storm-surge/ike`.  There are also a number of additional 
examples in the `$CLAW/geoclaw/examples/storm-surge` directory as well as some
in the `$CLAW/apps/surge-examples` directory (this is actually a repository of 
examples that is actively updated).  The primary input that one needs to provide
for a new example usually involves two data source

 - Topography data:  Data that specifies the topography and bathymetry of the
   region around the area of interest.  For storm surge computations it is 
   generally good practice to include entire oceanic basins so that you can
   ensure that flow into and out of the basin is resolved by the computation
   and is sufficiently distant from the computational domain's boundaries.
 - Storm data:  Of course we need to specify the particular storm that you
   are interested in.  There are a number of ways to specify a storm which
   are described in :ref:`setrun_surge`.  Sources for parameterized storms
   can also be found in :ref:`surgedata` and a description of how to include
   them in :ref:`_surge_module`.

.. warning:: This is a work in progress and only partially has been filled out.
   If you are interested in the rest of the steps or wish to contribute your
   own workflow please let us know!

Here we will concentrate on changing the Hurricane Ike example into one for
Hurricane Katrina.

1. First copy the files located in the Hurricane Ike directorty located at
   `$CLAW/geoclaw/examples/storm-surge/ike`.

2. Next let's find some better topography for the New Orleans area...

3. Now let's find a storm specification for Hurricane Katrina.  In this 
   example we will use the ATCF database.  For Katrina this ends up being
   the file located `here <>`_.

4. We now need to modify the `setrun.py` to use our new storm format and
   topography we now added...

5. Finally we need to also modify the plotting so that we have an

6. Gauges...

7. Running the simulation...
