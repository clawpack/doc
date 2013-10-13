
.. _amrclaw_1d:

---------------------------
AMRClaw for 1d problems
---------------------------


The two-dimensional code can also be used for 1-dimensional problems, by
setting `num_cells[1] = 1` so there is only one cell in the `y` direction.
Also set `refinement_ratios_y = [1,1,1, ...]` so that refinement is not done
in this direction.

In this case the code will automatically do sweeps only in the x-direction
and not attempt to solve any Riemann problems in the y-direction, or
transverse Riemann problems.  

The output in the *fort.q000N* files will be suitable for plotting with the
one-dimensional Python plotting tools, e.g. these files will list the number
of cells in *x* but not in *y*.  

**This appears to still have bugs and is being worked on.**

