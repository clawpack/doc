
.. _trouble:


*************************************
Troubleshooting
*************************************

Installation
++++++++++++

.. _trouble_makeexe:

Trouble running "make .exe"
---------------------------

If the code does not compile, check the following:

 * Make sure your environment variable `CLAW` is set properly::

    $ printenv CLAW

   to print the value.  
   The Makefiles use this variable to find the common Makefile and
   library routines.

   If you get the error message::

        Makefile:154: /clawutil/src/Makefile.common: No such file or directory

   then `CLAW` is not set properly.  It is looking for the file
   `$CLAW/clawutil/src/Makefile.common` and if `CLAW` is not set, the path
   will be missing.

 * Make sure your environment variable `FC` is set properly.  This
   should be set to
   the command used to invoke the Fortran compiler, e.g. *gfortran*.  

   If you get an error like::

    make[1]: gfortran: No such file or directory

   then the gfortran compiler is not being found.



.. _trouble_makedata:

Trouble running "make .data"
------------------------------

If you get the Python error::

    ImportError: No module named pyclaw

it's possible that your environment variable `PYTHONPATH` does not
include $CLAW/python in the path.  If you followed the instructions
at :ref:`setenv` then this variable should be set properly.   Recall
that this has to be set in any new shell you use for Clawpack.

If there are errors in the `setrun` function (usually defined in
`setrun.py`) then the these may show up when you try to "make .data"
since this function must be executed.


.. _trouble_makeoutput:

Trouble running "make .output"
------------------------------

If you want to re-run the code and you get::

    $ make .output
    make: `.output' is up to date.

then you can force it to run again by removing the file `.output`::

    $ rm -f .output
    $ make .output

This happens for example if you changed something that you know
will affect the output but that isn't in the Makefile's set of
dependencies.

Starting in 4.5.1, you can also do

    $ make output

(with no dot before ``output``) to run the code without checking dependencies.
See :ref:`makefiles` for more details and warnings.

.. _trouble_makeplots:

Trouble running "make .plots"
------------------------------
   
The Python plotting routines require `NumPy` and `matplotlib`.  See 
:ref:`python` for information on installing this.

If there are errors in the `setplot` function (usually defined in
`setplot.py`) then the these may show up when you try to "make .output"
since this function must be executed.

Starting in 4.5.1, you can also do

    $ make plots

(with no dot before ``plots``) to plot the output without checking dependencies.
See :ref:`makefiles` for more details and warnings.


