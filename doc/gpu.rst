
.. _gpu:


*************************************
Using the GPU version of Clawpack
*************************************

GPU versions of the two-dimensional AmrClaw and GeoClaw codes have been
developed primarily by Xinsheng Qin, as described in the references below.

This is still under development and has not yet been fully merged
in Clawpack, but there is a `gpu` branch of most of the Clawpack
repositories and checking those out will give a working version of
the GPU code.

You can do this by checking out the gpu branch of the `clawpack/clawpack`
module and then doing `git module update`.

To create a new clone `clawpack_gpu` with the
proper branches checked out, you can use these commands::

    git clone https://github.com/clawpack/clawpack.git clawpack_gpu
    cd clawpack_gpu
    git checkout -b gpu origin/gpu
    git submodule init
    git submodule update

Note that this version of the GPU code is roughly based on version 5.5.0 of
Clawpack but had some other changes merged in as well (in particular adjoint
flagging, see :ref:`adjoint`), and so it is not exactly equivalent in
capabilities.

The GPU version has some new libraries of source code. In particular,
`$CLAW/amrclaw/src/2d/GPU` contains `.H`, `.cpp` and `.f90` files for the 
2d amrclaw code.  Many of the `.f90` files replace those normally used
from `$CLAW/amrclaw/src/2d` and those files are removed from this branch.
This means that the pure CPU version of amrclaw cannot be run from this
branch, instead check out a specific version such as `v5.5.0` to 
run the CPU code for comparisons.

Similarly, `$CLAW/geoclaw/src/2d/shallow/GPU` contains replacement `.f90`
files for many of the library routines in `$CLAW/geoclaw/src/2d/shallow`.

References
----------

- Efficient Tsunami Modeling on Adaptive Grids with Graphics Processing Units (GPUs)
  by X. Qin, R. J. LeVeque, and M. Motley, 
  Journal of Advances in Modeling Earth Systems, 2019, 
  `DOI:10.1029/2019MS001635 <https://doi.org/10.1029/2019MS001635>`_
  
- Accelerating wave-propagation algorithms with adaptive mesh refinement 
  using the Graphics Processing Unit (GPU),
  by X. Qin, R. J. LeVeque, and M. R. Motley,
  `<https://arxiv.org/abs/1808.02638>`_

- See also the older instructions and links to Xinsheng's original branches at
  `<https://github.com/xinshengqin/geoclaw/tree/geo_gpu_paper>`_
