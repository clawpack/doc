
.. _python_path:

Python path
===========

When using PyClaw or other Python tools from Clawpack (e.g. the
visualization tools in VisClaw or :ref:`topotools` from GeoClaw), you need
to be able to import various modules.  

For a general discussion of importing Python modules, see the tutorial in
the Python documentation:  
`Python 2 <https://docs.python.org/2/tutorial/modules.html>`_,
`Python 3 <https://docs.python.org/3/tutorial/modules.html>`_.

Below are some hints in case you run into problems with import statements
with modules not being found, or being imported from the wrong version of
Clawpack (if you have more than one on your computer).

Try the following in a Python (or IPython) shell::

    >>> import clawpack
    >>> clawpack.__file__

This should print out something like::

    '/Users/rjl/clawpack_src/clawpack-v5.3.1/clawpack/__init__.py'

This shows where clawpack is being imported from.  In this case the
directory `/Users/rjl/clawpack_src/clawpack-v5.3.1` is the directory
normally referred to as `$CLAW` in this documentation.  Within this
directory, there is a subdirectory `$CLAW/clawpack` that contains a file
`__init__.py`, which is a standard Python way of indicating that the files
in the directory should be handled as a Python package.  

The directory `$CLAW` (top level of Clawpack code)  
must be in the Python search path in order for this import statement to work.
The Python command `import clawpack` searches through all directories in
this path looking for the first one that contains a subdirectory named
`clawpack` containing a file `__init__.py`, (or a file named `clawpack.py`,
but in this case it should find the `$CLAW/clawpack` directory).  

The directory `$CLAW/clawpack` also contains symbolic links to other
directories within the Clawpack repository hierarchy that contain
other Python modules.  This allows you to do, for example::

    >>> from clawpack import pyclaw
    >>> pyclaw.__file__

    '/Users/rjl/clawpack_src/clawpack-v5.3.1/clawpack/pyclaw/__init__.py'

If you examine this in bash, e.g. via::

    $ ls -l $CLAW/clawpack/pyclaw

you should find that this is a symbolic link to the directory
`$CLAW/pyclaw/src/pyclaw`, which is where you would find the actual source
code for things in the `pyclaw` package.

These symbolic links are set up when you install clawpack (using `pip
install` or more explicitly using e.g. `python setup.py symlink-only`).

**Example:** Suppose you want to examine the Python code for the `Iplotclaw`
module of VisClaw (see :ref:`plotting_Iplotclaw`).  You can figure out where
this code is via::

    >>> from clawpack.visclaw import Iplotclaw
    >>> Iplotclaw.__file__

Alternatively, in IPython you could examine this code directly via::

    In [1]: from clawpack.visclaw import Iplotclaw
    In [2]: Iplotclaw??


sys.path
--------

To examine the Python search path, you can do::

    >>> import sys
    >>> sys.path

This should print out a list of strings.  The first string in the list is
probably the empty string, indicating that the current working directory
should be searched first. The remaining strings are paths in your file
system.

You should see that the directory referred to as `$CLAW` in this
documentation is in the path.  

If you have multiple versions of Clawpack on your computer and Python seems 
to be importing from the wrong place, check the path.
Directories are searched in the order listed in `sys.path`.  


easy-install.pth
----------------

If you used `pip` to install Clawpack (following :ref:`installing_pip`),
then the path to the installed version will may be added to the file
`easy-install.pth` located in the `site-packages` directory.  If you want
to switch to a different version you may need to either use `pip` again,
or remove this line from `site-packages/easy-install.pth`.


To find `site-packages/easy-install.pth`, use this these commands in Python::

    >>> import site
    >>> site.getusersitepackages()

this will tell you where the users' `site-packages` directory is. If you
installed using the `--user` flag in the `pip install`, then it is the
`easy-install.pth` in this directory that contains the path.

If you installed without the `--user` flag, then then system-wide
`site-packages/easy-install.pth` file has been modified.  You can find the
path to this via::

    >>> import site
    >>> site.getsitepackages()



PYTHONPATH
----------

If you have an environment variable `PYTHONPATH` set, the paths specified
here may be searched before or after what is specified in the users'
`site-packages/easy-install.pth`, depending on how you set `PYTHONPATH`.  

To see if this is set, in the bash shell you can do::

     $ echo $PYTHONPATH

See :ref:`setenv` for information on setting environment variables.


