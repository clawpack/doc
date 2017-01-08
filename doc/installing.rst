.. _installing:

**************************************
Installation options
**************************************

Please `register <http://depts.washington.edu/clawpack/register/index.html>`_
if you have not already done so.  This is very useful in helping
us track the extent of usage, and important to the :ref:`funding` agencies
who support this work.

**Prerequisites:** Before installing, check that you have the :ref:`prereqs`.

Install using pip
=====================================

This is the simplest approach, see :ref:`installing_pip`.


Install from a tarfile
=====================================

Download a tar file of the latest release:

* `https://github.com/clawpack/clawpack/releases/download/v5.4.0rc-alpha/clawpack-v5.4.0rc-alpha.tar.gz
  <https://github.com/clawpack/clawpack/releases/download/v5.4.0rc-alpha/clawpack-v5.4.0rc-alpha.tar.gz>`_
* :ref:`previous`
* :ref:`changes`


See :ref:`clawpack_components` for a list of what's included in this tar file.

Save this tar file in the directory where you want the top level of the
clawpack tree to reside.  Then untar using the command::   

    tar -xzvf clawpack-v5.4.0rc-alpha.tar.gz

Then move into the top level directory::

    cd clawpack-v5.4.0

Next install the Python components of Clawpack::

    python setup.py install

This will compile a lot of Fortran code using `f2py` and will produce a lot of 
output, so you might want to redirect the output, e.g. ::

    python setup.py install > install_output.txt

If you get compilation errors in this step, you can still use the
Classic, AMRClaw, and GeoClaw; see :ref:`install_no-pyclaw`.

If you only plan to use PyClaw, jump to :ref:`first_run`.  If you
plan to use Classic, AMRClaw, or GeoClaw continue with :ref:`setenv`.


.. _install_no-pyclaw:

Install other packages without compiling PyClaw
================================================
If you get errors in the compilation step when using `pip install` or
`python setup.py install`, check :ref:`trouble_installation`. 
If your problem is not addressed there, please `let us know <claw-users@googlegroups.com>`_
or `raise an issue <https://github.com/clawpack/clawpack/issues>`_.
You can still use the Fortran codes (AMRClaw, GeoClaw, and Classic) by doing
the following.  

First, download a tarfile of the latest release as described in
:ref:`install_clawpack`.  

Next :ref:`setenv`.  You must then also set your PYTHONPATH manually::

    export PYTHONPATH=$CLAW:$PYTHONPATH

Then you should be able to do::

    cd $CLAW   # assuming this environment variable was properly set
    python setup.py symlink-only

This will create some symbolic links in the `$CLAW/clawpack` 
subdirectory of your top level Clawpack directory, but does not compile code
or put anything in your site-packages.
In Python you should now be able to do the following, for example::

    >>> from clawpack import visclaw

If not then either your `$PYTHONPATH` environment variable is not set
properly or the required symbolic links were not created.

Next go to :ref:`first_run`.

.. _install_pyclaw_parallel:

Install only PyClaw (for running in parallel)
================================================
First, install PyClaw as explained above.  Then see the install instructions
for :ref:`parallel`.

Alternatively, you may use the following shell scripts (assembled by Damian San Roman)
to install everything:

* Linux machine or Beowulf Cluster: https://gist.github.com/sanromd/9112666
* Mac OS X: https://gist.github.com/sanromd/10374134


.. _install_dev:

Install the latest development version
================================================

The development version of Clawpack can be obtained by cloning 
`<https://github.com/clawpack>`_.  This is advised for those who want to help
develop Clawpack or to have the most recent bleeding edge version.
See :ref:`setup_dev` for instructions.


.. _install_alternatives:

Running Clawpack on a VM or in the Cloud
========================================

.. warning:: The information on the pages listed below is out of date.

**Virtual Machine.**
An alternative to installing the :ref:`install_prerequisites` 
and Clawpack itself is to use the :ref:`vm`.


**Cloud Computing.**

* :ref:`pyclaw` can be installed and run in the cloud for free on 
  http://wakari.io or http://cloud.sagemath.com; see :ref:`cloud`.
* All of Clawpack can be run on AWS using the :ref:`aws`.

Next steps:
===========

Once Clawpack is installed, you can go to one of the following pages to get
started:

- :ref:`first_run_pyclaw`
- :ref:`first_run_fortran`

