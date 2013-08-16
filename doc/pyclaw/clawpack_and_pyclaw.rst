:group: pyclaw

.. _clawpack_and_pyclaw:

.. _port_Example:

Porting a problem from Clawpack 4.6.x to PyClaw 
======================================================
The script `pyclaw/development/clawdata2pyclaw.py` is intended to aid
in converting a Clawpack 4.6 problem setup to PyClaw.  However,
some manual conversion is necessary, especially if the problem
includes custom fortran routines.

In PyClaw, the high-level portions of the Fortran routines are reorganized in 
an object-oriented Python framework, while the low-level ones are bound through
the Fortran to Python interface generator `f2py <http://www.scipy.org/F2py>`_.
Therefore, for simple problems you won't need to call f2py directly. However, if 
you want to reutilize some problem-specific fortran routines that were set up and 
tested in a Clawpack problem, you can easily do it. Indeed, if those routines 
are complicated and/or computationally intensive, 
you should consider directly using the f2py 
interface in the initialization script (see :ref:`problem_setup`).
The example in `clawpack/pyclaw/examples/shallow_sphere`, which
solves the shallow water equations on the surface of a sphere, is a
complete example that relies heavily on the use of problem-specific Fortran routines.
In that problem setup, a few Fortran routines have been used to provide the 
following functionality:

    * Initialize the solution ``state.q[:,:,:]``

    * Provide the mapping from a uniform Cartesian domain to the desired 
      physical domain, i.e. the mapc2p function

    * Setup the auxiliary variables ``state.aux[:,:,:]``

    * Compute the (non-hyperbolic) contribution of a source term

    * Impose custom boundary conditions to both solution and auxiliary 
      variables

The first step to succesfully interface the Fortran functions with PyClaw 
is to automate the extension module generation of these routines through f2py.
You can use `clawpack/pyclaw/examples/shallow_sphere/Makefile` as a template::

    # Problem's source Fortran files
    INITIALIZE_SOURCE = mapc2p.f setaux.f qinit.f src2.f
    problem.so: $(INITIALIZE_SOURCE)
        $(F2PY) -m problem -c $^

The code above, calls f2py to compile a set of Fortran routines 
and build a module 
(``problem.so``) which can then be imported as a function in Python.
The argument following the ''-m'' flag is the name the python module should have (i.e.
the name of the target). f2py uses the ``numpy.distutils`` module from NumPy 
that supports a number of major Fortran compilers. For more information 
see `<http://www.scipy.org/F2py>`_.

After compilation, it is useful to check the signature of each 
function contained in ``problem.so``, which may be different than
that of the original Fortran function, since f2py eliminates dummy variables.
One can easily achieve that by using the following commands::

    $ ipython
    >>> import problem
    >>> problem?

The last command queries the content of the module and outputs the functions' 
signature that must be used in the initialization script to correctly call the 
fortran functions. In the shallow water equations on a sphere example, we get 
the following output::

    >>> Type:		module
    >>> Base Class:	<type 'module'>
    >>> String Form:	<module 'problem' from 'problem.so'>
    >>> Namespace:	Interactive
    >>> File:		/Users/../../../clawpack/pyclaw/examples/shallow-sphere/problem.so
    >>> Docstring:
        This module 'problem' is auto-generated with f2py (version:1).
        Functions:
        mapc2p(x1,y1,xp,yp,zp,rsphere)
        aux = setaux(maxmx,maxmy,num_ghost,mx,my,xlower,ylower,dxc,dyc,aux,rsphere,num_aux=shape(aux,0))
        q = qinit(maxmx,maxmy,num_ghost,mx,my,xlower,ylower,dx,dy,q,aux,rsphere,num_eqn=shape(q,0),num_aux=shape(aux,0))
        q = src2(maxmx,maxmy,num_ghost,xlower,ylower,dx,dy,q,aux,t,dt,rsphere,num_eqn=shape(q,0),mx=shape(q,1),my=shape(q,2),num_aux=shape(aux,0))

For instance, the function ``src2``, which computes the contribution of the 
(non-hyperbolic) source term, has the following intent variables::

    >>> cf2py integer intent(in) maxmx
    >>> cf2py integer intent(in) maxmy
    >>> cf2py integer optional, intent(in) num_eqn
    >>> cf2py integer intent(in) num_ghost
    >>> cf2py integer intent(in) mx
    >>> cf2py integer intent(in) my
    >>> cf2py double precision intent(in) xlower
    >>> cf2py double precision intent(in) ylower
    >>> cf2py double precision intent(in) dx
    >>> cf2py double precision intent(in) dy
    >>> cf2py intent(in,out) q
    >>> cf2py integer optional, intent(in)  num_aux
    >>> cf2py intent(in) aux
    >>> cf2py double precision intent(in) t
    >>> cf2py double precision intent(in) dt
    >>> cf2py double precision intent(in) Rsphere

Note that ``num_eqn``, ``mx``, ``my`` ``num_aux`` are identified by f2py as optional
arguments since their values can be retrieved by looking at the dimensions of
other multidimensional arrays, i.e. ``q`` and ``aux``.

We are now ready to call and use the Fortran functions in the initialization
script. For instance, the ``src2`` function is called in the 
`script <http://numerics.kaust.edu.sa/pyclaw/examples/shallow-sphere/shallow_4_Rossby_Haurwitz_wave.py>`_ by using a fortran_src_wrapper function whose main part reads::

    >>> # Call src2 function
    >>> import problem
    >>> state.q = problem.src2(mx,my,num_ghost,xlowerg,ylowerg,dx,dy,q,aux,t,dt,Rsphere)

A similar approach is used to call other wrapped Fortran functions like 
``qinit``, ``setaux``, etc.

An important feature that makes PyClaw more flexible is the 
capability to replace the standard low-level Fortran routines whith some 
problem-specific routines. Binding new low-level functions and replacing the 
standard ones is very easy; the user just needs to modify the problem-specific 
Makefile. The shallow water equations on a sphere is again a 
typical example that uses this nice feature. Indeed, to run correctly the problem an 
ad-hoc ``step2`` function (i.e. the ``step2qcor``) is required. For that problem
the interesting part of the `Makefile
<http://numerics.kaust.edu.sa/pyclaw/examples/shallow-sphere/shallow_4_Rossby_Haurwitz_wave.py>`_
reads::

    # Override step2.f with a new function that contains a call to an additional
    # function, i.e. qcor.f
    # ==========================================================================
    override TWO_D_CLASSIC_SOURCES = step2qcor.f qcor.o flux2.o limiter.o philim.o

    qcor.o: qcor.f
        $(FC) $(FFLAGS) -o qcor.o -c qcor.f

The user has just to override ``step2.f`` with the new function ``step2qcor.f`` 
and provide new::

    output_filenames : input_filenames
    	actions

rules to create the targets required by the new Fortran routine. 
Similar changes to the problem-specific Makefile can be used to replace other 
low-level Fortran routines.

