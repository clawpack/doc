
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

If you installed from a tarfile or using a `git clone` without using `pip`, then
you will need to set the `PYTHONPATH` variable in order for the Python codes to be
found.  This is not necessary if you used `pip` to install (see
:ref:`installing_pip`).  

See :ref:`python_path` for more about Python paths and this environment
variable.

In the `bash` shell, for example, this path can be set via::

    export PYTHONPATH=/path/to/clawpack:$PYTHONPATH

Note that this places this new path at the front of any existing path, and will be
searched before other directories where you might have a different version of
Clawpack, e.g. if you have used `pip` to install a different version and there is
a path in a `site-packages/easy-install.pth` file.  

Using `PYTHONPATH` can also be useful if you want to use
different versions of Clawpack in different shells, 
e.g. when dual-debugging or for different projects.


