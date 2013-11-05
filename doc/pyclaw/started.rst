:group: pyclaw

.. _pyclaw_installation:

==================
Installing PyClaw
==================
The fastest way to install the latest release of PyClaw is::

    pip install clawpack

To get the latest development version, do this instead::

    git clone git@github.com:clawpack/clawpack.git
    cd clawpack
    pip install -e .

If you encounter any difficulties in the installation
process, please `contact us <claw-users@googlegroups.com>`_ or
`raise an issue <http://github.com/clawpack/pyclaw/issues/>`_.

To run an example, launch an IPython session and then::

    from clawpack.pyclaw import examples
    claw = examples.shock_bubble_interaction.setup()
    claw.run()
    claw.plot()

This will run the code and then place you in an interactive plotting shell.
To view the simulation output frames in sequence, simply press 'enter'
repeatedly.  To exit the shell, type 'q'.  For help, type '?' or see
:ref:`pyclaw_plotting`.


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
    If you do not have one already, we recommend getting one via 
    `GCC Wiki GFortranBinaries <http://gcc.gnu.org/wiki/GFortranBinaries>`_.  

There are some additional dependencies for running in parallel; see
:ref:`parallel`.  


Obtaining Python, numpy, and matplotlib
+++++++++++++++++++++++++++++++++++++++++++++++
If you don't already have these on your system, we recommend 
`Anaconda CE <https://store.continuum.io/>`_ or 
`Enthought Canopy Express <https://www.enthought.com/products/epd/free/>`_
(both free).


Clawpack
-----------------------------------------------------------
PyClaw is part of Clawpack, which includes several other
packages; see :ref:`clawpack_components`.  Note that the 
installation instructions above will install PyClaw,
Riemann and VisClaw.  If you also wish to use AMRClaw or
GeoClaw, you should follow the more general Clawpack
:ref:`installing`.


Testing your installation with nose
-----------------------------------------------------------
If you've manually downloaded the source, or cloned from Github,
then you can easily test your installation.
First install nose: ::

   pip install nose

Then ::

    cd clawpack/pyclaw
    nosetests 

If you have followed the instructions for :ref:`parallel`, you can run the tests in parallel::

    mpirun -n 4 nosetests

.. note::

    PyClaw automatically enables tests that require PETSc if it detects a
    petsc4py installation.  Otherwise, tests that use PETSc are disabled.

Next steps
-----------------------------------------------------------
Now you're ready to set up your own PyClaw simulation.  Try the :ref:`pyclaw_tutorial`!
