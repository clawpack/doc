.. _first_run_pyclaw:

Testing a PyClaw installation and running an example
=====================================================

If you downloaded Clawpack manually, you can test your :ref:`pyclaw`
installation as follows (starting from your `clawpack` directory)::

    cd pyclaw
    nosetests

This should return 'OK'.


Running an example
------------------

Many examples of Clawpack simulations can be seen in the :ref:`galleries`.

To run an example and plot the results using PyClaw, simply do the following
(starting from your `clawpack` directory)::

    cd pyclaw/examples/euler_2d
    python shock_bubble_interaction.py iplot=1

That's it.  For next steps with PyClaw, see :ref:`basics`.

More examples
-------------

You might also want to download the :ref:`apps`, which contains additional
examples.

