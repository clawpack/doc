.. _testing_refactor:

=========================
Clawpack Testing Refactor
=========================

.. seealso::
   - :ref:`testing`

Overview
--------

Clawpack is moving to a pytest-based testing model built around example-local regression tests and shared test infrastructure in clawutil.

This refactor is motivated by the need to:
 - simplify test authoring
 - reduce custom test scaffolding
 - better match pytest conventions
 - improve CI integration
 - support incremental migration from the legacy regression framework

Current reference implementations include:
 - https://github.com/clawpack/clawutil/issues/187
 - https://github.com/clawpack/classic/issues/96
 - https://github.com/clawpack/amrclaw/issues/310

Design decisions
----------------

1. **Pytest is the system-wide test runner** - All new tests should be written
   for pytest.
2. **Example-based regression tests are the primary solver test model** - For
   solver-heavy code, the canonical test is a small example that:
   - writes input data
   - builds using the example Makefile
   - runs in a temporary directory
   - compares output to saved regression data
3. **Shared testing infrastructure lives in clawutil** - Common runner logic and
   helpers should be centralized rather than duplicated across repositories.
4. **Tests should use the real build workflow** - Tests should exercise the same
   example Makefile workflow that users rely on.
5. **Fresh builds should be explicit** - Tests should request a fresh build
   through the runner or build target, rather than relying on import-time
   cleanup or hidden state mutation.
6. **Legacy test infrastructure is transitional** - Existing legacy tests may
   remain temporarily, but new tests should follow the pytest model and old
   tests should be migrated over time.

Test layout
-----------

A typical migrated example should contain::

    example_name/
        Makefile
        setrun.py
        test_example_name.py
        regression_data/
            frame0001.txt
            frame0002.txt

Typical test workflow
---------------------

A typical example test:
1.	creates or modifies rundata
2.	writes data files
3.	builds the executable
4.	runs in tmp_path
5.	compares selected frames or diagnostics

Regression data policy
----------------------

Regression data should be:
 - small
 - reviewable in a PR
 - deterministic
 - specific to the example

Use `--save` to regenerate baselines intentionally.

CI policy
---------

CI should:
 - run pytest directly
 - store test artifacts in a predictable directory
 - prefer fast, stable examples in PR checks
 - allow broader coverage in scheduled or extended workflows

Data Included in the Repository for CI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Example regression tests should avoid external downloads when possible. Small,
stable input files should be checked into the repository. Download and
conversion logic should be tested separately in focused utility tests.

Compiler Flags and Numerical Reproducibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regression tests are sensitive to floating-point roundoff and compiler
optimizations. To ensure stable and reproducible results across platforms,
CI uses conservative optimization flags (e.g., `-O1`).

Higher optimization levels may produce small numerical differences and are
not currently used for regression validation.

Migration guidance
------------------

When migrating an old test:
 - prefer example-local placement
 - move shared behavior into clawutil
 - remove hidden setup side effects
 - keep the test close to the user-facing workflow

Reference example
-----------------
`$CLAW/classic/examples/acoustics_1d_heterogeneous/test_acoustics_1d_heterogeneous.py`
is intended to serve as an example setup.
