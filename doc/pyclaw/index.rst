:group: pyclaw

.. _pyclaw:


Pyclaw 
======

Installation::

    pip install clawpack

To run an example, launch an IPython session and then::

    from clawpack.pyclaw import examples
    claw = examples.shock_bubble_interaction.setup()
    claw.run()
    claw.plot()

**Features:**

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

.. toctree::
   :maxdepth: 2

   ../first_run_pyclaw
   basics
   going_further
   classes
   ../developers
   troubleshooting
   about
   ../gallery/pyclaw/gallery/gallery_all


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


Citing
=======================
If you use PyClaw in work that will be published, please cite the Clawpack software::

    @misc{clawpack,
        title={Clawpack software}, 
        author={Clawpack Development Team}, 
        url={http://www.clawpack.org}, 
        note={Version x.y},
        year={2014}}

and the paper::

    @article{pyclaw-sisc,
            Author = {Ketcheson, David I. and Mandli, Kyle T. and Ahmadia, Aron J. and Alghamdi, Amal and {Quezada de Luna}, Manuel and Parsani, Matteo and Knepley, Matthew G. and Emmett, Matthew},
            Journal = {SIAM Journal on Scientific Computing},
            Month = nov,
            Number = {4},
            Pages = {C210--C231},
            Title = {{PyClaw: Accessible, Extensible, Scalable Tools for Wave Propagation Problems}},
            Volume = {34},
            Year = {2012}}

Please fill in the version number that you used.

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

