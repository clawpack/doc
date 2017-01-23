
.. _trouble:

*************************************
Troubleshooting
*************************************


.. _trouble_installation:

Troubleshooting Installation
+++++++++++++++++++++++++++++

Don't forget to :ref:`setenv`, if necessary.

See :ref:`python_path` for problems with your Python path.

The utility function :ref:`whichclaw` may be useful for sorting out path issues.

Troubleshooting Fortran:
+++++++++++++++++++++++++++++

.. _trouble_f2py:

Setting the Fortran compiler to be used by f2py (pip)
-----------------------------------------------------

When trying to install with `pip` (see :ref:`installing_pip`)
or `python setup.py install`, if you get an error like::

    error: f90 not supported by GnuFCompiler

then f2py is trying to use your f77 compiler.  This may happen even if
you also have an f90 compiler like gfortran installed.  In this case,
``pip install`` will not work; you should download a tarball or clone
the code from Github.  Then, in order to see the compilers detected by f2py,
run::

    python setup.py config_fc --help-fcompiler

Then to install using a different compiler, do e.g.::

    python setup.py config_fc --fcompiler=gfortran install

You may replace ``gfortran`` with the compiler you wish to use.

.. _trouble_makeexe:

Trouble running "make .exe"
+++++++++++++++++++++++++++

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
++++++++++++++++++++++++++++


If there are errors in the `setrun` function (usually defined in
`setrun.py`) then the these may show up when you try to "make .data"
since this function must be executed.

See :ref:`setrun` for information about the setrun function.


.. _trouble_makeoutput:

Trouble running "make .output"
++++++++++++++++++++++++++++++

If you want to re-run the code and you get::

    $ make .output
    make: `.output' is up to date.

then you can force it to run again by removing the file `.output`::

    $ rm -f .output
    $ make .output

This happens for example if you changed something that you know
will affect the output but that isn't in the Makefile's set of
dependencies.

You can also do

    $ make output

(with no dot before ``output``) to run the code without checking dependencies.
See :ref:`makefiles` for more details and warnings.

.. _trouble_makeplots:

Trouble running "make .plots"
++++++++++++++++++++++++++++++
   
The Python plotting routines require `NumPy` and `matplotlib`.  See 
:ref:`python` for information on installing these.

If there are errors in the `setplot` function (usually defined in
`setplot.py`) then the these may show up when you try to "make .plots"
since this function must be executed.  See :ref:`setplot`.

You can also do

    $ make plots

(with no dot before ``plots``) to plot the output without checking dependencies.
This will never run the code, it will only attempt to plot the output files
found in `_output` directory (or wherever the `OUTDIR` variable in the
`Makefile` points).

See :ref:`makefiles` for more details and warnings.


