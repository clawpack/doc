.. _manning:

==========================
Manning friction term
==========================

When using GeoClaw to model inundation, it is important to include an
appropriate bottom friction term in the equations.  This takes the form of a
source term added to the right hand side of 
the momentum equations:

    :math:`(hu)_t + \cdots = -\gamma (hu),`
    
    :math:`(hv)_t + \cdots = -\gamma (hv),`

The form built into GeoClaw is the Manning formulation, in which
:math:`\gamma` is a function of the depth and momentum:

    :math:`\gamma = \frac{gn^2\sqrt{(hu)^2 + (hv)^2}}{h^{7/3}}.`

with :math:`g` the gravitational constant and :math:`n` the "Manning
coefficient".  This is an empirical formula and the proper value of
:math:`n` to use depends on the roughness of the terrain or seabed, as shown
for example in 
`this table <http://www.engineeringtoolbox.com/mannings-roughness-d_799.html>`_.
Often for generic tsunami modeling, the constant value :math:`n=0.025` is used.
An enhancement of GeoClaw planned for the future is to allow
spatially-varying Manning coefficient.

The friction term is only applied in regions where the depth is below a
threshold specified by *frictiondepth* (see :ref:`setrun_geoclaw`).

.. warning:: Changing the Manning coefficient can have a significant effect
   on the extent of inundation and runup.  If GeoClaw (or any other code) is
   used for estimating real-world hazards, users should think carefully
   about chosing an appropriate value, and may want to run sensitivity
   studies.  A smaller value of :math:`n` (less friction) will generally 
   lead to greater inundation.

.. warning:: A bug was recently discovered in GeoClaw that was corrected 
   in Version 4.6.3:  The exponent (7/3) was used in the Fortran code, which
   evaluates as 2 in integer arithmetic rather than 2.3333.  This has now
   been corrected by writing it as (7.d0/3.d0).  This can make a difference in
   the extent of inundation and runup.  Given the uncertainty in the proper
   value of :math:`n` to use and the inadequacy of using the same value
   everywhere, the effect of this bug on the resulting accuracy was probably 
   small, but users may want to test this.

