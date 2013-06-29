
.. _git_versions:

==============================
Keeping track of git versions
==============================

The command::

    $ $CLAW/clawutil/src/python/clawutil/claw_git_status.py

will report on the status of all Clawpack repositories found, e.g. what
branch is checked out, the hash of the most recent commit, and any tracked 
files with uncommitted changes.  This information will be saved to a file
`claw_git_status.txt` and any diffs found for uncommitted changes will be
saved to a file `claw_git_diffs.txt`.  

An optional command line argument allows you to save these files in a
different directory, e.g. ::

    $ $CLAW/clawutil/src/python/clawutil/claw_git_status.py _output

This is often useful to do when running a code if you want to later
determine exactly what version of the code was used, particularly when doing
regression testing.

The function `$CLAW/clawutil/src/python/clawutil/runclaw.py`
now has an argument `print_git_status` (with default value `False`).
Calling `runclaw` with `print_git_status == True` will write these files to
the output directory specified by the `outdir` argument.
(Need to modify `Makefile.common` to take advantage of this.)


