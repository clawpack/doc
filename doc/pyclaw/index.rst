:group: pyclaw

.. _pyclaw:


PyClaw 
======

In this section of the documentation, PyClaw refers 
a Python version of the hyperbolic PDE solvers that allows solving the
problem in Python (e.g. in a Jupyter notebook) without explicitly using
any Fortran code.  Versions of the solvers are written in Python.
However, they use Riemann solvers that are converted from the Fortran
versions into Python-callable versions using 
`f2py <https://numpy.org/doc/stable/f2py/>`__,  
to facilitate using the same large set of solvers from either Fortran
or Python.  Note that
in order for this to work the solvers must be precompiled, as is done
when using `pip install`, for example (see :ref:`installing_pip`).

See :ref:`clawpack_packages` for more information about the different
capabilities of PyClaw relative to :ref:`contents_fortcodes`.

**Note:** The `clawpack/pyclaw` directory also contains some 
Python tools that are used many places in
Clawpack, e.g. when plotting with :ref:`visclaw` or when compiling and
running Fortran code using a `Makefile` and `setrun.py` file
(when using :ref:`contents_fortcodes`).
These modules are mostly used "under the hood".  
Other Python tools of use in the Fortran versions
are described elsewhere; see e.g. :ref:`plotting` or :ref:`geoclaw`.
All of these modules are pure Python and should work fine as long
as the top level of Clawpack is on your :ref:`python_path`.


.. _pyclaw_install:

PyClaw installation
-------------------

Using `pip install` is the recommended approach, see
:ref:`installing_pip`.


Examples
--------

Next, try running an example `Jupyter notebook <http://www.clawpack.org/gallery/notebooks.html#notebooks>`_.

Alternatively, to run an example from the **IPython prompt**::

    from clawpack.pyclaw import examples
    claw = examples.shock_bubble_interaction.setup()
    claw.run()
    claw.plot()

To run an example and plot the results directly from the command line,
go to the directory where Clawpack is installed and then::

    cd pyclaw/examples/euler_2d
    python shock_bubble_interaction.py iplot=1


Features
--------

    * A **hyperbolic PDE solver** in 1D, 2D, and 3D, including mapped grids and surfaces, built on Clawpack;
    * **Massively parallel** -- the same simple script that runs on your laptop will
      scale efficiently on the world's biggest supercomputers (see :ref:`parallel`);
    * **High order accurate**, with WENO reconstruction and Runge-Kutta time integration
      (see :ref:`solvers`);
    * Simple and intuitive thanks to its Python interface.

PyClaw makes use of the additional Clawpack packages, 
`Riemann <http://github.com/clawpack/riemann>`_ and
`VisClaw <http://github.com/clawpack/visclaw>`_ for Riemann solvers and visualization, 
respectively.

If you have any issues or need help using PyClaw, `contact us <claw-users@googlegroups.com>`_.

PyClaw Documentation
====================

See also the 
`Gallery of PyClaw Applications <http://www.clawpack.org/gallery/pyclaw/gallery/gallery_all.html>`_ 
for some examples of how PyClaw can be used.

.. toctree::
   :maxdepth: 2

   ../first_run_pyclaw
   basics
   going_further
   classes
   ../developers
   troubleshooting
   about



.. _pyclaw_reference:

PyClaw Modules reference documentation
======================================
.. toctree::
   :maxdepth: 1
   
   controller
   solvers
   evolve/limiters
   io
   solution
   state
   geometry
   util

.. _riemann_reference:

Riemann Solvers reference documentation
========================================
The Riemann solvers now comprise a separate package.  For convenience,
documentation of the available pure python Riemann solvers is included
here.  Many other Fortran-based Riemann solvers are available.

.. toctree::
   :maxdepth: 3
   
   rp

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Citing PyClaw
=======================
If you use PyClaw in work that will be published, please cite the Clawpack software
(see :ref:`citing`) and also mention specifically that you used PyClaw, and cite the paper::

    @article{pyclaw-sisc,
            Author = {Ketcheson, David I. and Mandli, Kyle T. and Ahmadia, Aron J. and Alghamdi, Amal and {Quezada de Luna}, Manuel and Parsani, Matteo and Knepley, Matthew G. and Emmett, Matthew},
            Journal = {SIAM Journal on Scientific Computing},
            Month = nov,
            Number = {4},
            Pages = {C210--C231},
            Title = {{PyClaw: Accessible, Extensible, Scalable Tools for Wave Propagation Problems}},
            Volume = {34},
            Year = {2012}}

If you use the Classic (2nd-order) solver, you may also wish to cite::

    @article{leveque1997,
            Author = {LeVeque, Randall J.},
            Journal = {Journal of Computational Physics},
            Pages = {327--353},
            Title = {{Wave Propagation Algorithms for Multidimensional Hyperbolic Systems}},
            Volume = {131},
            Year = {1997}}

If you use the SharpClaw (high order WENO) solver, you may also wish to cite::

    @article{KetParLev13,
            Author = {Ketcheson, David I. and Parsani, Matteo and LeVeque,
            Randall J.},
            Journal = {SIAM Journal on Scientific Computing},
            Number = {1},
            Pages = {A351--A377},
            Title = {{High-order Wave Propagation Algorithms for Hyperbolic Systems}},
            Volume = {35},
            Year = {2013}}

