:orphan:

.. _python_path:

Python path
===========


When using PyClaw or other Python tools from Clawpack (e.g. the
visualization tools in VisClaw or :ref:`topotools` from GeoClaw), you need
to be able to import various modules.  

For a general discussion of importing Python modules, see the tutorial in the 
`Python3 documentation <https://docs.python.org/3/tutorial/modules.html>`_.

Below are some hints in case you run into problems with import statements
with modules not being found, or being imported from the wrong version of
Clawpack (if you have more than one on your computer).

.. _whichclaw:

whichclaw.py
------------

The script `$CLAW/clawutil/src/python/clawutil/whichclaw.py` may be useful in
debugging paths.  It prints out information on how various paths and environment
variables are set.  (Available starting in Version 5.4.0.)

Sample output::

    $ python $CLAW/clawutil/src/python/clawutil/whichclaw.py

    `import clawpack` imports from:
        /Users/rjl/clawpack_src/clawpack-v5.5.0

    The CLAW environment variable is set to: 
        /Users/rjl/D/clawpack-v5.5.0
    The PYTHONPATH environment variable is not set

    The following directories on sys.path might contain clawpack,
    and are searched in this order:
        /Users/rjl/clawpack_src/clawpack-v5.5.0

    The following easy-install.pth files list clawpack:
        /Users/rjl/Library/Python/2.7/lib/python/site-packages/easy-install.pth
            (points to /Users/rjl/clawpack_src/clawpack-v5.5.0)

Beware if there seems to be a conflict (e.g. between where the `CLAW` 
environment variable points and where Python imports from).
See below for more about `sys.path` and `easy-install.pth` files.

Which version was imported?
---------------------------

Try the following in a Python (or IPython) shell::

    >>> import clawpack
    >>> clawpack.__file__

This should print out something like::

    '/Users/rjl/clawpack_src/clawpack-v5.5.0/clawpack/__init__.py'

This shows where clawpack is being imported from.  In this case the
directory `/Users/rjl/clawpack_src/clawpack-v5.5.0` is the directory
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

.. warning :: Up to version 5.5.0, 
   the directory `$CLAW/clawpack` also contains symbolic links to other
   directories within the Clawpack repository hierarchy that contain
   other Python modules.  This allows you to do, for example::

    >>> from clawpack import pyclaw
    >>> pyclaw.__file__

    '/Users/rjl/clawpack_src/clawpack-v5.5.0/clawpack/pyclaw/__init__.py'

Starting in Version 5.6.0, symbolic links in `$CLAW/clawpack` 
have been eliminated.
Instead `$CLAW/clawpack/__init__.py` includes a dictionary of subpackages with 
the relative path indicated in this file::

    >>> import clawpack
    >>> clawpack._subpackages
    {'forestclaw': 'pyclaw/src', 'amrclaw': 'amrclaw/src/python', 'riemann': 'riemann', 
     'pyclaw': 'pyclaw/src', 'classic': 'classic/src/python', 'visclaw': 'visclaw/src/python', 
    'clawutil': 'clawutil/src/python', 'petclaw': 'pyclaw/src', 'geoclaw': 'geoclaw/src/python'}
  


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
or remove this line from `site-packages/easy-install.pth`, or execute
`pip uninstall clawpack`.

The :ref:`whichclaw` command is useful for determining where the 
`site-packages/easy-install.pth` is located.

More generally, to find `site-packages/easy-install.pth`, 
use this these commands in Python::

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

If you install Clawpack with pip, then you do not need to include it in
environment variable `PYTHONPATH`.

Setting the environment variable `PYTHONPATH` is often
considered bad practice in the Python community
and can lead to problems, see for example
`PYTHONPATH Considered Harmful <https://orbifold.xyz/pythonpath.html>`_.


In spite of the possible drawbacks, some Clawpack developers often
use `PYTHONPATH` to switch versions without difficulty, particularly
when using one of the :ref:`installing_fortcodes` rather than pip.

If you do wish to use it, you should set `PYTHONPATH` to point to the top
level of the clawpack directory for the code you wish to use.
Then use the :ref:`whichclaw` utility to check that this is where Clawpack
is imported from, and there is not an `easy-install.pth` file generated by
pip that points to a different location.

If you have an environment variable `PYTHONPATH` set, the paths specified
here may be searched before or after what is specified in the users'
`site-packages/easy-install.pth`, depending on how you set `PYTHONPATH`.  
See also 
https://docs.python.org/3/using/cmdline.html#environment-variables.
Hence trying to use `PYTHONPATH` if you have also used pip to install a
different version of Clawpack can lead to confusion.

To see if this environment variable is set, in the bash shell you can do::

     $ echo $PYTHONPATH

or use the :ref:`whichclaw` utility to report this, along with any other
possibly conflicting `easy-install.pth` files.

See :ref:`setenv` for information on setting environment variables.

