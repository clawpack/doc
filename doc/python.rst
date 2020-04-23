

.. _python:

***************
Python Hints
***************

.. contents::

.. _python-three:

Dropping support for Python 2.7
--------------------------------

As of Clawpack v5.7.0 we are no longer supporting Python 2.7, and
Python 3.x is expected, see :ref:`release_5_7_0`.  At this point we
believe v5.7.0 still works with Python 2.7, but we are phasing out
testing this in the future.

This is consistent with the fact that Python 2.7 itself will not be
maintained beyond January, 2020, and most package we rely on (e.g.
numpy, matplotlib, jupyter) are also ceasing support for Python 2.7,
see https://python3statement.org/

Hence we view Clawpack version 5.6.x as the end of the line for Python
2 support  (probably 5.6.1 unless there's a strong need to update this
further).  Clawpack 5.6.x will continue to be available, of course,
but in order to take advantage of future improvements to Clawpack (and
most other Python packages) we strongly suggest that you start
converting all of your codes to work in Python 3 if you haven't
already.  Often this only requires changing print statements to print
functions, but there are a few other changes.  See e.g.,
https://docs.python.org/3/howto/pyporting.html
and other online resources discussing the differences between Python 2 and 3.

.. _python-intro:

What is Python?
---------------

Python is a powerful object-oriented interpreted scripting/programming
language. Some version of Python is almost certainly on your computer
already (on unix, linux, OSX type::

    $ python --version 

to find out which version, or just::
    
    $ python

to start a python shell with a prompt that looks like::

    >>>

You may prefer to use `IPython
<http://ipython.scipy.org/moin/>`_, which is a nicer shell
than the pure python shell, with things like command completion and history.
See the `Quick IPython Tutorial
<http://ipython.scipy.org/doc/manual/html/interactive/tutorial.html>`_.

.. _python-install:

Installation of required modules
--------------------------------

To effectively use the pyclaw and Clawpack plotting routines that are
written in Python, you will need version 2.7 or greater
(but **not** 3.0 or above, which is not backwards compatible).  
some modules that are not included in the standard Python distribution. 
Python modules are loaded with the *import* statement in Python and a wide
variety of specialized modules exist for various purposes since people use
Python for many different purposes.

An alternative to installing the packages discussed below, you could also use the
:ref:`VM`, which has all the required Python modules pre-installed.

For use with Clawpack, you will need the `Numpy
<http://www.numpy.org/>`_ module (*Numerical Python*)
that allows working with arrays in much the same way as in Matlab.  
This is distributed as part of 
`SciPy <http://docs.scipy.org/doc/>`_ (*Scientific Python*).
See the `Installing SciPy <http://www.scipy.org/Installing_SciPy>`_
page for tips installing SciPy and NumPy on various platforms.

For plotting you will also need the `matplotlib
<http://matplotlib.org/>`_ module which provides Matlab-like
plotting commands for 1d and 2d plots (e.g. contour and pcolor plots).
This is generally the hardest thing to get going properly.  See the 
`matplotlib Installation FAQ
<http://matplotlib.sourceforge.net/faq/installing_faq.html>`_.

Often the easiest way to get all the modules you need is to install the

`Anaconda Python Distribution <http://docs.continuum.io/anaconda/>`_
or the 
`Enthought Python Distribution
<http://www.enthought.com/products/epd.php>`_, which is free for academic
users.  Versions are available for Windows, Mac OS X, and Redhat linux.  

With some versions of Linux (e.g. debian and Ubuntu), you can easily install
what's needed using ``apt-get``::

    $ apt-get install python-numpy
    $ apt-get install python-scipy
    $ apt-get install python-matplotlib

For OS X, you might also try the `Scipy Superpack
<http://stronginference.com/scipy-superpack/>`_.
See also these `tips on installing matplotlib on OS X
<http://matplotlib.sourceforge.net/faq/installing_faq.html#os-x-questions>`_.


References and tutorials
------------------------

Some useful links to get started learning Python:

   * `Dive Into Python <http://www.diveintopython.net/>`_

   * `Python tutorial <http://www.python.org/doc/tut/>`_
   * `NumPy User Guide <http://docs.scipy.org/doc/numpy/user/>`_
   * `NumPy for Matlab users <http://www.scipy.org/NumPy_for_Matlab_Users>`_
   * `SciPy Reference Guide <http://docs.scipy.org/doc/scipy/reference/>`_
   * `Matplotlib gallery <http://matplotlib.sourceforge.net/gallery.html>`_
   * `LeVeque's class notes
     <http://faculty.washington.edu/rjl/classes/am583s2014/notes/python.html>`_ 
   * `Langtangen's book <http://folk.uio.no/hpl/scripting/>`_ and
     `Introductory slides <http://heim.ifi.uio.no/~hpl/scripting/all-nosplit/>`_


Notebooks
---------

See :ref:`notebooks`.

