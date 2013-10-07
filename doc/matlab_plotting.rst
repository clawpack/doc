
.. _matlabplots:


***************************************
Plotting using Matlab
***************************************

Up through Version 4.3, Matlab was always used for plotting and an
extensive set of plotting tools have been developed.  These are still
available in `$CLAW/visclaw/src/matlab`
The user interface for these routines is essentially unchanged from the
previous versions, although several new features have been added.

To visualize output using



These are largely unchanged from 4.3.
See the `README` file in that directory for some tips.
Some documentation can also be found at
`http://math.boisestate.edu/~calhoun/visclaw/matlab_gallery/test_graphics/index.html`.


Starting in 4.4, we have also introduced a set of Python plotting tools, see
:ref:`plotting` for some of the advantages of switching to these tools.


.. warning:: There is one change to the form of the output files `fort.000N` starting in
   Clawpack 4.4:  The parameter `ndim` has been added.
