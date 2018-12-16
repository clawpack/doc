
.. _setenv:

=========================
Set environment variables
=========================

CLAW
----

To use the Fortran versions of Clawpack you will need to set the
environment variable `CLAW` to point to the top level of clawpack tree
(there is no need to perform this step if you will only use PyClaw).
In the bash shell these can be set via::

    export CLAW=/full/path/to/clawpack  # to top level clawpack directory


FC
--

You also need to set `FC` to point to the desired Fortran compiler,
e.g.::

    export FC=gfortran   # or other preferred Fortran compiler

Consider putting the two commands above in a file that is executed every
time you open a new shell or terminal window.  On Linux machines
with the bash shell this is generally the file `.bashrc` in your home
directory.  On a Mac it may be called `.bash_profile`.

If your environment variable `CLAW` is properly set, the command ::

    ls $CLAW

should list the top level directory, and report for example::

    README.md       riemann/        pyclaw/
    amrclaw/        setup.py        clawutil/       
    geoclaw/        visclaw/        classic/        

PYTHONPATH
----------

We do not recommend setting this environment variable.  See
:ref:`python_path` for more information.  Instead we recommend using `pip
install` to set the Python path appropriately, see :ref:`installing_pip`.
