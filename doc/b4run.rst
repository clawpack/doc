
.. _b4run:

*****************************************************************
b4run function
*****************************************************************

When using the Fortran code, the command::

    make output

invokes the `runclaw` function from 
`$CLAW/clawutil/src/python/clawutil/runclaw.py 
<https://github.com/clawpack/clawutil/blob/master/src/python/clawutil/runclaw.py>`__
to run the Fortran executable.

Starting in v5.7.1, this function has been modified to look for a Python `b4run`
function to be executed before running the Fortran code.  This can be used,
for example, to:

 - automate copying certain files into the `_output` directory 
   (e.g. you might want to keep the `Makefile` and `setrun.py` 
   that were used for the run along with the output),

 - generate a log file with more information about the run, e.g. 
   what time the run was started and what directory the input files came 
   from (the `rundir`).

The file `$CLAW/clawutil/src/python/clawutil/b4run.py 
<https://github.com/rjleveque/clawutil/blob/b4run/src/python/clawutil/b4run.py>`__
is a sample file showing the format it should have, and implements
the sample actions described above.

To search for a `b4run.py` file, the current `rundir` directory is
first checked and if there is no such file in this directory then
the environment variable `B4RUN` is checked, which can be set to
the full path of a `b4run.py` file that you wish to use globally, for example.

