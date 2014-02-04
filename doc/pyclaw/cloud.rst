:group: pyclaw

.. _cloud:

============================
Running PyClaw in the cloud
============================

PyClaw can be quickly installed and run for free using either SageMathCloud or Wakari.
After you've followed the instructions below, you may want to try some of the :ref:`notebooks`.

Sage Math Cloud
===============
To install on Sage Math Cloud, create an account and a project at http://cloud.sagemath.org/.
Then open a new terminal in your project, and type::

    pip install --user clawpack

That's it -- you should now be able to import Clawpack in your IPython
notebooks within that project.  

Wakari
======
Create an account at https://www.wakari.io/ and open a new terminal shell.
Then type::

    pip install -U numpy
    pip install clawpack


That's it -- you should now be able to import Clawpack in your IPython notebooks.
