
.. _matlabplots:


***************************************
Plotting using Matlab
***************************************

Up through Version 4.3, Matlab was always used for plotting and an
extensive set of plotting tools were developed.  These are still
available in `$CLAW/visclaw/src/matlab`
The user interface for these routines is essentially unchanged from the
previous versions, although several new features have been added.

.. _setting_up_matlab:

Setting up Matlab environment variables
---------------------------------------
To use the Matlab plotting tools with Clawpack, you will need to first
be sure that the necessary Malab routines are on the Matlab search
path.  This can be done by explicitly setting the MATLABPATH.  In bash,
this is done via

  $ export MATLABPATH ${CLAW}/visclaw/src/matlab

Alternatively, one can add this directory to the Matlab search path
using the Matlab "pathtool" command.


.. _create_output_for_matlab:

Running the code for visualizing in Matlab
------------------------------------------
To visualize output using Matlab plots, first run the example using::

  $ make .output

This will build the executable 'xclaw', run the Python script
'setrun.py' to create necessary input files for the executable, and
finally run the executable to create output files.  These output files
will be stored by default in the directory '_output'.

Once we have output files, e.g. 'fort.q0000', 'fort.q0001', and corresponding
fort.t0000' or 'fort.t0001' files, we plot them in Matlab by entering
at the Matlab prompt one of the following::

  >> plotclaw2

or::

  >> plotclaw3

depending on whether you are plotting two dimensional or three dimensional output.

Initially, you will be prompted as whether you want to run a file ''setplot''::

  >> plotclaw2

  plotclaw2  plots 2d results from clawpack or amrclaw
  Execute setplot2 (default = yes)?

The :ref:'setplot', normally located in the working directory,
contains initial settings for the plot.  The file is run by default.

Successivly hitting [enter] steps through and plots data from each of the fort files in order.  In
one and two dimensions, this plotting prompt is::

  Frame 2 at time t = 0.2
  Hit <return> for next plot, or type k, r, rr, j, i, q, or ?

The explanations for each prompt option are giving by entering '?'::

  Frame 2 at time t = 0.2
  Hit <return> for next plot, or type k, r, rr, j, i, q, or ?  ?

  Hit <return> for next plot, or type k, r, rr, j, i, q, or ?  ?
    k  -- keyboard input.  Type any commands and then "return"
    r  -- redraw current frame, without re-reading data
    rr -- re-read current file,and redraw frame
    j  -- jump to a particular frame
    i  -- info about parameters and solution
    q  -- quit



These are largely unchanged from 4.3.
See the `README` file in that directory for some tips.
Some documentation can also be found at
`http://math.boisestate.edu/~calhoun/visclaw/matlab_gallery/test_graphics/index.html`.


.. warning:: There is one change to the form of the output files `fort.000N` starting in
   Clawpack 4.4:  The parameter `ndim` has been added.
