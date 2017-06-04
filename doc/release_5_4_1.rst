:orphan:


.. comment: Change master to v5.4.1 in github links below once release is tagged

.. _release_5_4_1:

==========================
Release 5.4.1
==========================


Clawpack 5.4.1 was released on TBA.  See :ref:`installing`.

Changes relative to Clawpack 5.4.0 (February 17, 2017) are shown below.


Changes to classic
------------------

None.

See `classic diffs
<https://github.com/clawpack/classic/compare/v5.4.0...master>`_

Changes to clawutil
-------------------

Minor changes.

See `clawutil diffs
<https://github.com/clawpack/clawutil/compare/v5.4.0...master>`_

Changes to visclaw
------------------

- Fixes for Python3 compatibility.
- Improve KML functionality.
- Add `legend_tools` module to simplify adding a legend.
- Other minor fixes.
 
See `visclaw diffs
<https://github.com/clawpack/visclaw/compare/v5.4.0...master>`_

Changes to riemann
------------------

- Added several Riemann solvers for new problems.
- Improved several existing solvers.

See `riemann diffs
<https://github.com/clawpack/riemann/compare/v5.4.0...master>`_

Changes to amrclaw
------------------

The major new addition is 1d `amrclaw` code in the `src/1d` directory and 
some examples in the `examples` directory. (Also regression tests in `tests`).
This code was based on the `2d` code but reduced to a fully `1d` version that is better than the previous approach of using the `2d` code with only 1 cell in the `y` direction.  This code has not yet been extensively tested on challenging problems, so let us know if you run into problems with it.


- Cleanup some code related to timers.
- Fix a problem with integer overflows in some cases.
- Suppress printing Courant number every timestep to `fort.amr`
- Print more digits in gauge locations to output files `gauge*.txt`.
- Other minor fixes.

See `amrclaw diffs
<https://github.com/clawpack/amrclaw/compare/v5.4.0...master>`_

Changes to geoclaw
------------------


- Allow more flexibility in specification of `fgmax` grids when doing a restart.
- Print more digits in gauge locations to output files `gauge*.txt`.
- Other minor fixes.

See `geoclaw diffs
<https://github.com/clawpack/geoclaw/compare/v5.4.0...master>`_


Changes to PyClaw
------------------

For changes in PyClaw, see the `PyClaw changelog
<https://github.com/clawpack/pyclaw/blob/master/CHANGES.md>`_.

See `pyclaw diffs
<https://github.com/clawpack/pyclaw/compare/v5.4.0...master>`_

