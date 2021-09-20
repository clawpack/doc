

.. _python:

***************
Python Hints
***************

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


References and tutorials
------------------------

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

Some useful links to get started learning Python:

   * `NumPy User Guide <https://numpy.org/doc/stable/>`_
   * `NumPy for Matlab users <https://numpy.org/doc/stable/user/numpy-for-matlab-users.html>`_
   * `SciPy Reference Guide <http://docs.scipy.org/doc/scipy/reference/>`_
   * `Matplotlib gallery <https://matplotlib.org/stable/gallery/index.html>`_
   * `LeVeque's class notes
     <http://faculty.washington.edu/rjl/classes/am583s2014/notes/python.html>`_ 
   


Notebooks
---------

The `Clawpack Gallery of Jupyter 
Notebooks <http://www.clawpack.org/gallery/notebooks.html>`__
contains a number of notebooks with other examples of using Python for
Clawpack.
