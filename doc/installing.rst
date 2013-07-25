.. _installing:

**************************************
Installation instructions
**************************************



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
which is not backwards compatible).  You will also need *NumPy* and
*matplotlib* for plotting.  

See :ref:`python` for information on
installing the required modules and to get started using Python if
you are not familiar with it.

**Virtual Machine.**
An alternative to installing the prerequisites and Clawpack itself is to use the
:ref:`vm`.

**Cloud Computing.**
Another alternative is to run Clawpack on the Cloud, see :ref:`aws`.

.. _downloading:

Downloading Clawpack
--------------------

Eventually tar files will be provided containing all the code from various
repositories together for the convenience of users.

Eventually `pip install clawpack` might work in general for all of Clawpack.
Currently this only installs PyClaw, see
`Installing PyClaw <http://numerics.kaust.edu.sa/pyclaw/started.html>`_

Currently Clawpack 5.0 can be obtained by cloning a number of repositories
from `<https://github.com/clawpack>`_.

See the :ref:`setup_dev` below and follow these, except
that you can just clone directly from  `<https://github.com/clawpack>`_
rather than first forking them if you do not plan to make changes and issue
pull requests.

.. _setup_dev:

Temporary installation instructions for developers
---------------------------------------------------

**This should be simplified eventually and moved elsewhere**

Read the sections :ref:`git_and_github` and :ref:`using-git`.

To get started you will need to fork and then clone at least the following
set of repositories:

* `<https://github.com/clawpack/pyclaw>`_  (Python code, some of which is
  needed also for Fortran version)
* `<https://github.com/clawpack/clawutil>`_ (Utility functions,
  Makefile.common used in multiple repositories)
* `<https://github.com/clawpack/amrclaw>`_ (AMR version of Fortran code)
* `<https://github.com/clawpack/riemann>`_  (Riemann solvers)
* `<https://github.com/clawpack/visclaw>`_  (Python graphics and visualization tools)

You might also want:

* `<https://github.com/clawpack/doc>`_  (documentation)
* `<https://github.com/clawpack/geoclaw>`_  (GeoClaw)
* `<https://github.com/clawpack/classic>`_  (Classic single-grid code)
* `<https://github.com/clawpack/apps>`_  (To collect applications)
* `<https://github.com/clawpack/clawpack-4.x>`_  (Previous versions, 4.6)

You should set your environment variable `$CLAW` to point to the top
level directory that contains all of these clones.

Then you should be able to do::

    $ cd $CLAW
    $ rm -ri python/clawpack  # only needed if you already had this directory
    $ bash clawutil/src/make_clawtop.sh

This will create a directory `$CLAW/python/clawpack` that contains 
symbolic links to all the python directories from which you might
want to import things.

Set your `PYTHONPATH` environment variable to include `$CLAW/python`, e.g.  ::

    $ export PYTHONPATH=$CLAW/python:$PYTHONPATH

and then you should be able to do things like... ::

    >>> from clawpack.visclaw.Iplotclaw import Iplotclaw


.. _setenv:

Setting environment variables
-----------------------------

In addition to setting the environment variables `$CLAW` and `$PYTHONPATH`
as described above, you should also set::

    CLAWUTIL=$CLAW/clawutil
    AMRCLAW=$CLAW/amrclaw
    GEOCLAW=$CLAW/geoclaw
    VISCLAW=$CLAW/visclaw
    RIEMANN=$CLAW/riemann
    FC=gfortran   # or other preferred Fortran compiler

Consider putting the appropriate commands  in your .cshrc or .bashrc
file (which is executed automatically in each new shell you create).   

.. _first_test:

Testing your installation and running an example
------------------------------------------------


As a first test, go to the directory
`$CLAW/amrclaw/tests/example1`.
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

One could run the code by typing "./xamr", but using the make option has
several advantages.  For one thing,
this checks dependencies to make sure the executable and data files are up
to date, so you could have typed "make .output" without the first two steps
above.

Also, before running the code a subdirectory `_output` is created
and the output of the code (often a large number of files) is directed to
this subdirectory.  This is convenient if you want to do several runs with
different parameter values and keep the results organized.  After the code
has run you can rename the subdirectory, or you can modify the variable
`OUTDIR` in the Makefile to direct results to a different directory.  See
:ref:`makefiles` for more details.  Copies of all the data files are also
placed in the output directory for future reference.

If the code runs successfully, you should see output like the following::

.. warning:: Out of date!  Needs updating.



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


**Creating html versions of source files.***


To best view the results, and the source code and README files,
type::

  $ make .htmls

and view the resulting README.html file with a web browser.  

.. _startserver:

Starting a Python web server
-----------------------------

.. warning:: Out of date!  Needs updating.


This part is not required, but 
to best view README.html and other Clawpack generated html files,
it is convenient to start a local webserver via::

  $ cd $CLAW
  $ python python/startserver.py

Note that this will take over the window, so do this in a new window, or
else do::

  $ xterm -e python python/startserver.py &

to execute it in a new xterm (if available).
The setenv commands described above will define an alias so that this last
command can be simplified to::

  $ clawserver

The main $CLAW directory will then be available at http://localhost:50005
and jsMath should work properly to display latex on the webpages (once you've
downloaded the required fonts, see
`<http://www.math.union.edu/locate/jsMath/users/fonts.html>`_).  
