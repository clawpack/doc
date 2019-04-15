.. _first_run_pyclaw:

Testing a PyClaw installation and running an example
=====================================================

If you downloaded Clawpack manually, you can test your :ref:`pyclaw`
installation as follows (starting from your `clawpack` directory)::

    cd pyclaw/examples
    nosetests

This should return 'OK'.  
(You may need to install `nose <https://nose.readthedocs.io/en/latest/>`_
if `nosetests` is not on your system.)


Running an example
------------------

Many examples of PyClaw simulations can be seen in the 
`PyClaw gallery <http://www.clawpack.org/gallery/pyclaw/gallery/gallery_all.html>`_
and `Jupyter notebook examples <http://www.clawpack.org/gallery/notebooks.html#notebooks>`_.

You might also want to download the :ref:`apps`, which contains additional
examples in `apps/notebooks/pyclaw`.

From the Jupyter notebook
*************************

Try any of the notebooks listed under PyClaw in the :ref:`notebooks`.

From the IPython interpreter
****************************
Launch an IPython session and then::

    from clawpack.pyclaw import examples
    claw = examples.shock_bubble_interaction.setup()
    claw.run()
    claw.plot()

From the command line
*********************

To run an example and plot the results using PyClaw, simply do the following
(starting from your `clawpack` directory)::

    cd pyclaw/examples/euler_2d
    python shock_bubble_interaction.py iplot=1


That's it.  For next steps with PyClaw, see :ref:`basics`.
