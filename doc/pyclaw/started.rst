:group: pyclaw

.. _installation:

==================
Installing PyClaw
==================
The fastest way to install the latest release of PyClaw is::

    pip install clawpack

To get the latest development version, do this instead::

    git clone git@github.com:clawpack/clawpack.git
    cd clawpack
    pip install -e .

This assumes that you already have a Fortran 90 compiler; if not,
we recommend getting one via 
`GCC Wiki GFortranBinaries <http://gcc.gnu.org/wiki/GFortranBinaries>`_.  

There are some additional dependencies for running in parallel; see
:ref:`parallel`.  If you encounter any difficulties in the installation
process, please `contact us <claw-users@googlegroups.com>`_ or
`raise an issue <http://github.com/clawpack/pyclaw/issues/>`_.

Dependencies: Python, gfortran, numpy, and matplotlib
--------------------------------------------------------
PyClaw requires Python 2.5 or greater and a modern Fortran 95
compiler.  PyClaw is known to work with GNU gfortran 4.2 and higher and the IBM
XLF compiler.  

  * `Python <http://python.org>`_ version >= 2.5.
  * `numpy <http://numpy.scipy.org/>`_ version >= 1.6.
  * `matplotlib <http://matplotlib.sourceforge.net/>`_ version >= 1.0.1
    (optional -- only for plotting).
  * `pip <http://www.pip-installer.org/en/latest/installing.html>`_ 
  * A Fortran 90 compiler, such as gfortran version >= 4.2.
    You will need to use a Fortran compiler compatible with
    your Python installation.

Obtaining Python and its dependencies
+++++++++++++++++++++++++++++++++++++++++++++++
If you don't already have Python on your system, we recommend 
`Anaconda CE <https://store.continuum.io/>`_ or 
`Enthought Canopy Express <https://www.enthought.com/products/epd/free/>`_
(both free).


Clawpack
-----------------------------------------------------------
PyClaw is part of Clawpack, which also includes

*Clawutil*
    A package containing important utilities for working with Clawpack projects
    
*Riemann*
    A package containing a collection of Riemann solvers for PyClaw and 
    Clawpack.
    
*VisClaw*
    A set of visualization tools built on top of Matplotlib    


Testing your installation with nose
-----------------------------------------------------------
Install nose if you haven't already: ::

   pip install nose

Then test your installation: ::

    cd clawpack/pyclaw
    nosetests 

If you have followed the instructions for :ref:`parallel`, you can run the tests in parallel::

    mpirun -n 4 nosetests

.. note::

    PyClaw automatically enables tests that require PETSc if it detects a
    petsc4py installation.  Otherwise, tests that use PETSc are disabled.

Running and plotting an example
-----------------------------------------------------------
::

    cd clawpack/pyclaw/examples/euler_2d
    python shockbubble_bubble_interaction.py iplot=1

This will run the code and then place you in an interactive plotting shell.
To view the simulation output frames in sequence, simply press 'enter'
repeatedly.  To exit the shell, type 'q'.  For help, type '?' or see
:ref:`pyclaw_plotting`.

Next steps
-----------------------------------------------------------
Now you're ready to set up your own PyClaw simulation.  Try the :ref:`pyclaw_tutorial`!
