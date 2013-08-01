
.. _bc:

===================
Boundary conditions
===================

Boundary conditions are imposed each time step by filling ghost cells
adjacent to the edge of each grid patch.  See Chapter 4 of [LeVeque-FVMHP]_
for more details.

Boundary conditions are set by the library routines:

* `$CLAW/classic/src/Nd/bcN.f` for the classic code (N = 1, 2, 3).
* `$CLAW/amrclaw/src/Nd/bcNamr.f` for the amrclaw code (N = 2, 3).

Several standard choices of boundary condition procedures are provided in
these routines, and can be 
selected at each boundary by setting the input paramters `bc_lower` and
`bc_upper` in each dimension (see :ref:`setrun`) to one of the following:

*   1 or 'extrap'   : extrapolation (non-reflecting outflow)

    In this case values from the grid cell adjacent to the boundary
    are copied into all ghost cells moving in the direction normal to
    the boundary.  This gives a fairly good approximation to a
    non-reflecting or outgoing boundary condition that lets waves pass
    out of the boundary without reflection, particularly in one space
    dimension.  In more than one direction this is not perfect for waves 
    that hit the boundary at an oblique angle.

*   2 or 'periodic' : periodic boundary conditions

    In this case ghost cell values are set by copying from interior
    cells at the opposite boundary so that periodic boundary conditions
    are perfectly imposed.  Normally periodic boundary conditions would
    be imposed by setting this value for both `bc_lower` and `bc_upper`
    in some dimension, but this is not required.

*   3 or 'wall'     : solid wall boundary conditions are imposed 
    for systems where the second component of `q`  is the `x` velocity
    or momentum in one dimension (and where the third component
    of `q` is also the `y` velocity/momentum in more dimensions,
    etc.)  This is true, for example, if the acoustics equations
    are solved with components `q = (p, u, v)` or shallow water
    equations with `q = (h, hu, hv)`.

    In this case the normal velocity/momentum at a wall is
    reflected about the boundary (copied to a ghost cell from
    the cell equally far from the boundary on the interior side)
    while all other components are extrapolated.

    Reflecting boundary conditions can also often be used on a line of
    symmetry of a solution in order to reduce the computational domain 
    to be only half of the physical domain.

    Note that this option does not work on a mapped grid... 
    **Add pointer to modified version**


If none of the above boundary conditions are desired, the user can modify
the subroutine `bcN` so that setting the appropriate component of `bc_lower`
or `bc_upper` to 0 will execute code added by the user.  In this case it is
best to put the modified version of `bcN.f` in the application directory and
modify the `Makefile` to point to the modified version.

For an example, see ??  **Add pointer**



.. _bc_amr:

Boundary conditions for adaptive refinement
-------------------------------------------

When AMR is used, any interior patch edges (not at a domain boundary) are
filled automatically each time step, either by copying from adjacent
patches at the same level or by interpolating (in both space and
time) from coarser levels if needed.

The user must still specify boundary conditions at the edges of the
computational domain.  The same set of choices for standard boundary
conditions as described above are implemented in the library routine
`bcNamr.f`, and so specifying these boundary conditions requires no change
to `setrun.py` when going from Classic Clawpack to AMRClaw.  However, if
special boundary conditions have been implemented in a custom version of
`bcN.f` then the same procedure for setting ghost cells will have to be
implemented in a custom version of `bcNamr.f`.  This routine is slightly
more complicated than the single-grid Classic version, since one must always
check whether each ghost cell lies outside the computational domain (in
which case the custom boundary condition procedure must be applied) or lies
within the domain (in which case ghost cell values are automatically set by
the AMR code and the user   `bcNamr` routine should leave these values
alone.


.. _bc_geoclaw:

Boundary conditions for GeoClaw
--------------------------------

For tsunami modeling or other geophysical flows over topography the
computational domain has artificial boundaries that are placed sufficiently
far from the region of interest that any flow or waves leaving the domain
can be ignored and there should be no incoming waves.  Extrapolation
boundary conditions are then appropriate.  If the ocean is truncated at some
point then these generally have been found to give very small spurious
reflection of outgoing tsunami waves.  Extroplation boundary conditions can
also be used on dry land (where the depth `h` is zero).  

In some cases reflecting boundary conditions might be more appropriate,
e.g. along the walls of a wave tank.  

The library routine `$CLAW/geoclaw/src/2d/shallow/bc2amr.f` is modified from
the  `amrclaw` version only by extrapolating the depth at the boundaries
into ghost cells.

.. _bc_sphere:

Boundary conditions for clamshell grids on the sphere
------------------------------------------------------

In 2D AMRClaw and  GeoClaw, an additional option is available for `bc_lower`
and `bc_upper` that is implemented in the library routines:

*   4 or 'sphere'   : sphere boundary conditions

    Must set `bc_lower[0:2] = bc_upper[0:2] = 4` (i.e. at all 4 boundaries)

    These boundary conditions are similar to periodic boundary conditions,
    but for the clamshell grid introduced in [CalhounHelzelLeVeque]_
    for solving problems on the sphere using a single logically rectangular
    grid.  This is best envisioned by folding a rectangular piece of paper
    in half, gluing the edges together, and inflating to a sphere.  See the
    animations on the `website for the original paper <?>`_
    See also [BergerCalhounHelzelLeVeque]_ for further examples.
    

