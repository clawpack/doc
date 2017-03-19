
.. _amrclaw:


*************************************
AMRClaw
*************************************

The AMRClaw version of Clawpack provides Adaptive Mesh Refinement (AMR)
capabilities in 2 and 3 space dimensions.  (The two-dimensional code can
also be used for 1-dimensional problems, see :ref:`amrclaw_1d`.)

**See also:**

* :ref:`amr_algorithm`
* :ref:`refinement`
* :ref:`amrclaw_doxygen`

Block-structured AMR is implemented, in which rectangular patches of the
grid at level `L` are refined to level `L+1`.  
See :ref:`setrun_amrclaw` for a list of the input parameters that can be
specified to help control how refinement is done.
The general algorithms are described in [BergerLeVeque98]_.

See :ref:`ClawPlotItem` for a list of 2d plot types that can be used to
create a `setplot` function to control plotting of two-dimensional results.
Some of the attribute names start with the string `amr_`, indicating that a
list of different values can be specified for each AMR level.
See  :ref:`plotting` and :ref:`setplot` for more about plotting.

Python plotting tools for 3d are still under development.  For now, the
Matlab tools from Clawpack 4.3 can still be used, see
:ref:`matlabplots`.

.. toctree::
   :maxdepth: 2

   amrclaw1d
   setrun_amrclaw
   setrun_amrclaw_sample
   amr_algorithm
   refinement
   gauges


