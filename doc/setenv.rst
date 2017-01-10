
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

    export CLAW=/full/path/to/top/level


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

In earlier versions of Clawpack it was recommended to set the environment
variable `PYTHONPATH` when using the Fortran codes in Clawpack.  We now
recommend avoiding this by using these :ref:`installing_pip`.

See :ref:`python_path` for more about Python paths and this environment
variable.

If you want to set this environment variable to point to a different version
of Clawpack (useful in particular if you are using different version in
different shells, e.g. when dual-debugging or for different projects), you
can set (in bash)::

    export PYTHONPATH=/path/to/clawpack:$PYTHONPATH

to make sure this version is used instead of one specified in a
`site-packages/easy-install.pth` file.


