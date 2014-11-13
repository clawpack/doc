:group: pyclaw

.. _cloud:

============================
Running PyClaw in the cloud
============================

PyClaw can be quickly installed and run for free using either SageMathCloud or Wakari.
After you've followed the instructions below, you may want to try some of the :ref:`notebooks`.

Sage Math Cloud
===============
To run on Sage Math Cloud, simply create an account and a project at http://cloud.sagemath.org/.
Clawpack is pre-installed, so you can use it immediately from a terminal or IPython notebook.
Since matplotlib plots generated from the terminal will not work in the cloud, we
recommend using an IPython notebook.

You can also install the latest release of Clawpack in your Sage Math Cloud project.
Open a new terminal in your project, and type::

    pip install --user clawpack


Wakari
======
Create an account at https://www.wakari.io/ and open a new terminal shell.
Then type::

    pip install -U numpy
    pip install clawpack


That's it -- you should now be able to import Clawpack in your IPython notebooks.
