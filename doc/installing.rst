.. _installing:

**************************************
Installation instructions
**************************************

See also: 

* :ref:`pyclaw`
* :ref:`installation`
* :ref:`setup_dev`


Prerequisites
-------------

**Operating systems.**
Clawpack should work fine on Unix/Linux or Mac OS X systems.  Much
of it will work under Windows using Cygwin, but this is not officially
supported.

On OS X you need to have the `Xcode developer tools
<http://developer.apple.com/technologies/tools/xcode.html>`_
installed in order to have "make" working.


**Fortran.**
The main Clawpack routines are written in Fortran (a mixture of
Fortran 77 and Fortran 90/95) and so compiling and running the code
requires a Fortran compiler, such as `gfortran
<http://gcc.gnu.org/wiki/GFortran>`_, which is part of the GNU gcc compiler
suite.
See :ref:`fortran_compilers` for more about which compilers work well with
Clawpack.

For Mac OSX, see `hpc.sourceforge.net <http://hpc.sourceforge.net/>`_ for
some installation options.

Makefiles are used in libraries and directories and you will need some
version of *make*.

**Python.**
We use Python for visualization of results
(see :ref:`plotting`) and also for user input (see :ref:`setrun`).
Older Matlab plotting scripts are still available but are no longer
being developed and the examples now included in Clawpack include
`setplot.py` files to facilitate use of the Python plotting tools
(see :ref:`setplot`).

You will need Python Version 2.5 or above (but **not** 3.0 or above,
which is not backwards compatible).  You will also need 
`NumPy <http://www.numpy.org/>`_ and
`matplotlib <http://matplotlib.org/>`_ for plotting.  

See :ref:`python` for information on
installing the required modules and to get started using Python if
you are not familiar with it.

**Virtual Machine.**
An alternative to installing the prerequisites and Clawpack itself is to use the
:ref:`vm`.

**Cloud Computing.**
Another alternative is to run Clawpack on the Cloud, see :ref:`aws`.


.. _install_pyclaw:

PyClaw only
-------------------

For users who only plan to use the Python interface of PyClaw, see the
instructions at

* :ref:`pyclaw`
* :ref:`installation`


.. _install_from_git:

Cloning from GitHub
---------------------

Clawpack 5.0 be obtained by cloning a number of repositories
from `<https://github.com/clawpack>`_.  This is advised
for those who want to help
develop Clawpack or to have the most recent bleeding edge version.
See :ref:`developers_gitclone` for instructions.


.. _downloading:

Downloading Clawpack
--------------------

Many users will want to install from a tar file.

Tar files will be provided containing all the code from various
repositories together for the convenience of users.
These releases will be found on the
`Github releases page <https://github.com/clawpack/clawpack/releases>`_.

After downloading a tar file, unzip and untar using a command like::

    tar -xf clawpack-5.0.0.tar.gz

This should create a directory with the corresponding name, e.g.
`clawpack-5.0.0`.  If you `cd` into this directory and use `pwd` to "print
working directory", you will find the full path to the top level of
Clawpack.  This path is needed in the next step to set environment variables::

    cd clawpack-5.0.0
    pwd

**Note:** The tar file contains only a subset of the Clawpack repositories,
those that contain the core code and examples.  Other repositories contain
things like additional applications, documentation, and webpages.
See :ref:`clawpack_components` for more details and information on
downloading other repositories.



.. _setenv:

Setting environment variables
-----------------------------


To use the Fortran version of the Clawpack you will need to set the
environment variable `CLAW` to point to the top level of clawpack tree.
You also need to prepend this directory to your `PYTHONPATH` so that the
Clawpack Python modules can be found when importing.  
In the bash shell these can be set via::

    export CLAW=/full/path/to/top/level
    export PYTHONPATH=$CLAW:$PYTHONPATH

Finally, you need to set `FC` to point to the desired Fortran compiler,
e.g.::

    export FC=gfortran   # or other preferred Fortran compiler

Consider putting the three commands above in a file that is executed every
time you open a new shell or terminal window.  On Linux machines
with the bash shell this is generally the file `.bashrc` in your home
directory.  On a Mac it may be called `.bash_profile`.

If your environment variable `CLAW` is properly set, the command ::

    ls $CLAW

should list the top level directory, and report for example::

    README.md       riemann/        pyclaw/
    amrclaw/        setup.py        clawutil/       
    geoclaw/        visclaw/        classic/        
    


.. _install_links:

Symbolic links for Python modules
---------------------------------

You will need to set up a subdirectory named $CLAW/clawpack that contains
symbolic links to various other directories.  This are used so that Python
import commands will work.

These links are created by::

    cd $CLAW
    python setup.py no-pyclaw

If you plan to use PyClaw, you can instead do::

    python setup.py install

This will create the links and will also compile some Fortran code using
`f2py` that is needed for the PyClaw codes to work.


Test that your links and `PYTHONPATH` are properly set by starting Python
(or IPython) and trying::

    >>> from clawpack import visclaw

This should not give an error message.


.. _first_test:

Testing your installation 
-------------------------

As a first test of the Fortran code, try the following::

    cd $CLAW/classic/tests
    make tests

This will run several tests and compare a few numbers from the solution with
archived results.  The tests should run in a few seconds.

There are similar `tests` subdirectories of `$CLAW/amrclaw` and
`$CLAW/geoclaw` to do quick tests of these codes.

.. _first_run:

Running an example
------------------

To do a more substantial run and plot the results, try one of the examples
illustrated in the :ref:`galleries`.

For example, a simple 1-dimensional acoustics equations can be solved
using the code in `$CLAW/classic/examples/acoustics_1d_example1`, as
illustrated in :ref:`gallery_classic_amrclaw`.

Move to this directory via::

    cd $CLAW/classic/examples/acoustics_1d_example1

You can try the following test in this directory, or you may want to first
make a copy of it (see the instructions in :ref:`copyex`).

The Makefiles are set up to do dependency checking so that in many
application directories you can simply type::

  $ make .plots

and the Fortran code will be compiled, data files created, the code
run, and the results plotted automatically, resulting in a set of webpages
showing the results.

However, if this is your first attempt to run a code, it is useful to go
through these steps one at a time, both to understand the steps and so that
any problems with your installation can be properly identified.

You might want to start by examining the Makefile.  This sets a number of
variables, which at some point you might need to modify for other examples,
see :ref:`makefiles` for more about this.  At the bottom of the Makefile is
an `include` statement that points to a common Makefile that is used by most
applications, and where all the details of the make process can be found.

To compile the code, type::

  $ make .exe    

If this gives an error, see :ref:`trouble_makeexe`.

This should compile the example code (after first compiling the required
library routines) and produce an executable named `xclaw` in this directory.

Before running the code, it is necessary to also create a set of data files
that are read in by the Fortran code.  This can be done via::
  
  $ make .data

If this gives an error, see :ref:`trouble_makedata`.

This uses the Python code in `setrun.py` to create data files that have the
form `*.data`.  

Once the executable and the data files all exist, we can run the code.  The
recommended way to do this is to type::

  $ make .output

If this gives an error, see :ref:`trouble_makeoutput`.

Before running the code a subdirectory `_output` is created
and the output of the code (often a large number of files) is directed to
this subdirectory.  This is convenient if you want to do several runs with
different parameter values and keep the results organized.  After the code
has run you can rename the subdirectory, or you can modify the variable
`OUTDIR` in the Makefile to direct results to a different directory.  See
:ref:`makefiles` for more details.  Copies of all the data files are also
placed in the output directory for future reference.



**Plotting the results.**  
Once the code has run and the files listed above have been created, there are several
options for plotting the results.  

To try the Python tools, type::

  $ make .plots

If this gives an error, see :ref:`trouble_makeplots`.

If this works, it will create a subdirectory named `_plots` that contains a number of
image files (the `*.png` files) and a set of html files that can be used to view the
results from a web browser.  See :ref:`plotting_makeplots` for more details.

An alternative is to view the plots from an interactive Python session, as described in
the section :ref:`plotting_Iplotclaw`.

If you wish to use Matlab instead, see :ref:`matlabplots`.

Other visualization packages could also be used to display the results, but you will need
to figure out how to read in the data.  See :ref:`fortfiles` for information about the
format of the files produced by Clawpack.


