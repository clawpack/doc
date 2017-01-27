
.. _installing_conda:

Installing using conda
======================

.. warning:: This is currently under development and not extensively tested.

See https://github.com/clawpack/conda-recipes.

If you use the
`conda package manager <http://conda.pydata.org/docs/index.html>`_
for Python and you only want to use the PyClaw
portion of Clawpack, then you might want to try this.  

You might want to consider first creating a separate `conda environment
<http://conda.pydata.org/docs/using/envs.html>`_ if you want to separate
Clawpack and it's dependencies from other versions of Python code. 

Then you can install via::

    conda install -c clawpack -c conda-forge clawpack=5.4.0

