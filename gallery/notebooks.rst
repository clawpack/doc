
.. _notebooks:

Clawpack Gallery of Jupyter Notebooks
=====================================

The `Jupyter notebook <http://jupyter.org/>`_
(formerly known as IPython notebook)
is a very nice platform for illustrating Clawpack examples.

If you have used Clawpack with the Jupyter notebook, please send us a link
or submit a pull request to the `apps repository <http://github.com/clawpack/apps>`_.
The links below will take you to static view of several notebooks
as html files.  You can also play animations in them and interact
with some plots, but to actually run the code yourself you should clone the 
apps repository.

**Warning:** The notebooks and tools to support them are being actively
developed, so these may change in the near future and the versions posted
here may not work with the current Clawpack.

**Examples using PyClaw:**

* :ref:`pyclaw/intro_notebook.ipynb`
* `A 2D fluid dynamics example <https://github.com/clawpack/apps/blob/master/notebooks/pyclaw/Quadrants.ipynb>`_
* `Stegotons: solitary waves arising in non-dispersive periodic media <https://github.com/clawpack/apps/blob/master/notebooks/pyclaw/Stegotons.ipynb>`_
* `Demonstration of different limiters for advection <http://nbviewer.ipython.org/gist/ketch/9508222>`_

**Examples using Fortran Classic:**

* `advection_1d <_static/notebooks/classic/advection_1d/advection_1d.html>`_
  illustrating upwind, Lax-Wendroff, and limiter methods.
* `acoustics_1d_example1 <_static/notebooks/classic/acoustics_1d_example1/acoustics_1d_example1.html>`_

**Examples using AMRClaw:**

* `advection_2d <_static/notebooks/amrclaw/advection_2d_square/amrclaw_advection_2d_square.html>`_

**Examples using GeoClaw:**

* `chile2010a <_static/notebooks/geoclaw/chile2010a/chile2010a.html>`_
  illustrates how to set up a basic GeoClaw run with adaptive refinement.
* `chile2010b <_static/notebooks/geoclaw/chile2010b/chile2010b.html>`_
  illustrates setting regions and gauges.
* `topotools_examples <_static/notebooks/geoclaw/topotools_examples.html>`_
  illustrates some of the tools from :ref:`topotools_module`.
* `dtopotools_examples <_static/notebooks/geoclaw/dtopotools_examples.html>`_
  illustrates some of the tools from :ref:`dtopotools_module`.
* `Okada <_static/notebooks/geoclaw/Okada.html>`_
  illustrates use of the Okada model for generating sea floor deformation.

**Examples for VisClaw:**

* `Animation tools demo
  <https://nbviewer.jupyter.org/url/www.clawpack.org/_static/notebooks/animation_tools_demo.ipynb>`_

**Riemann solvers:**

A set of notebooks is under development to illustrate Riemann solvers.  See
http://www.clawpack.org/riemann_book/index.html.

.. _notebooks_old:

Old notebooks --- many need updating
------------------------------------

**Examples illustrating Riemann solvers:**

* `The Riemann problem for the Euler equations <http://nbviewer.ipython.org/gist/ketch/08ce0845da0c8f3fa9ff>`_
* `Euler shock tube  <http://nbviewer.ipython.org/gist/ketch/d31fd8d2d7739e59b6c6>`_
* `Riemann solutions of the shallow water equations <http://nbviewer.ipython.org/gist/rjleveque/8994740>`_ 
* `Shallow water equations -- Riemann solver tests <http://nbviewer.ipython.org/url/faculty.washington.edu/rjl/notebooks/shallow/SW_riemann_tester.ipynb>`_
* `Acoustics equations and their Riemann solver in 1D and 2D
  <http://nbviewer.ipython.org/github/maojrs/ipynotebooks/blob/master/acoustics_riemann.ipynb>`_
* `Elasticity equations and their Riemann solver in 2D and 3D <http://nbviewer.ipython.org/github/maojrs/ipynotebooks/blob/master/elasticity_riemann.ipynb>`_


**Examples illustrating methods:**

* `Advection Equation and the REA algorithm <http://nbviewer.ipython.org/github/maojrs/ipynotebooks/blob/master/advection_REA.ipynb>`_

