

.. _restart:


*************************************
Checkpointing and restarting
*************************************

.. warning ::  These instructions currently only apply to `amrclaw` and 
   `geoclaw` codes.

.. _restart_checkpt:

Checkpointing a computation
---------------------------

In this section `clawdata` refers to the `rundata.clawdata` attribute
of an object of class `ClawRunData`, as is generally set at the top
of a `setrun.py` file.

The `rundata.clawdata.checkpt_style` parameter specified in `setrun.py` (see
:ref:`setrun`) determines how often checkpointing is done, if at all.
The checkpoint files are saved in the same output directory as the solution

If `clawdata.checkpt_style` is a **positive integer** then a new checkpoint file
will be created at each checkpoint time with a file name that includes the
number of coarse grid time steps taken so far, in the form `fort.chkNNNNN`.
This is a (possibly very large) binary file that contains all the information
needed to restart the calculation at this point.
There will also be a 2-line ASCII file `fort.tchkNNNNN` that contains the
time of this checkpoint and the number of coarse steps taken so far.

If `clawdata.checkpt_style` is a **negative integer** then the checkpoint files
will alternate between `fort.chkaaaaa` and `fort.chkbbbbb`, overwriting
any previous version.  This insures that there is always at least one full
checkpoint file available but never more than two, in order to save disk space
since these files can be huge.  Negative styles are generally appropriate if
you simply want to make sure there's a recent checkpoint file available in
case the code dies due to a time limit or disk space quota being exceeded, for
example.

The available checkpoint styles are:

* If `clawdata.checkpt_style==0`, then no checkpoints are saved.

* If `abs(clawdata.checkpt_style)==1`, then a checkpoint will be saved only
  at the final time (useful if you might need to restart and run out longer).

* If `abs(clawdata.checkpt_style)==2`, then a checkpoint will be done at the
  times specified by the list `clawdata.checkpt_times`.

* If `abs(clawdata.checkpt_style)==3`, then a checkpoint will be done every 
  `clawdata.checkpt_interval` steps on the coarsest grid.

* If `abs(clawdata.checkpt_style)==4`, then a checkpoint will be done
  at each output time (as specified in various ways depending on the value
  of `clawdata.output_style`.

Note that if `abs(clawdata.checkpt_style)` is 1 or 2 then specific
checkpoint times are specified.  If these do not agree with output times on the
coarsest level then the time step may need to be adjusted to hit these
times exactly on all levels.  For this reason we generally recommend using
styles 1, 3 or 4.

See the comments in :ref:`setrun_sample` for examples.

.. _restart_stop:

Aborting a computation with a STOP file
---------------------------------------

As of v5.10.0, it is possible to abort a running computation and have it
save a checkpoint file before quitting.  Simply create a (possibly empty)
file named `STOP` in the directory from which the (amrclaw or geoclaw)
code is running. The code will continue to run until the current coarse
level time step has been completed (which may require many time steps on
finer levels). At this point all levels are at the same time and it is
possible to write a checkpoint file that can be used for restarting. The
checkpoint file will be named `fort.chkNNNNN` based on the number of coarse
time steps taken so far (if `abs(checkpt_style) >= 0`) or the next available
`fort.chkaaaaa` or `fort.chkbbbbb` if a negative `checkpt_style` was specified.

Note that an the usual AMR output may not be written out at the time
the calculation quits, unless this time had been specified as an output
time.  If you want to output the solution at this time without taking any
additional time steps, you could do a restart that reads in the final
checkpoint file and that has `tfinal` adjusted in `setrun.py` to be earlier 
than the time of this checkpoint.

.. _restart_restart:

Restarting a computation
-------------------------

To restart a computation from any point where checkpoint files have been saved,
modify `setrun.py` to set::

    clawdata.restart = True
    clawdata.restart_file = 'fort.chkNNNNN' 

where `NNNNN` is the time step number from which the restart should
commence,  or replace by `aaaaa` or `bbbbb` if a negative
`checkpt_style` was used in the original run, as discussed above.

You should also modify the output time parameters to specify that the
computation should go to a later time than the time of the restart file
(which can be found in the file `fort.tchkNNNNN`).

Note the following in setting the new output times:

* The value `clawdata.t0` should generally be left to the original starting
  time of the computation.

* If `clawdata.output_style==1`, then `clawdata.t0` and `clawdata.tfinal`
  along with `clawdata.num_output_times` are used to determine equally
  spaced output times.  Only those times greater than the restart time will
  be used as output times.

  If `clawdata.output_t0==True` then a time frame will be output at the
  restart time (not t0 in general).  This may duplicate the final frame that was
  output from the original computation.  Set `clawdata.output_t0 = False`
  to avoid this.

* If `clawdata.output_style==2`, then `clawdata.output_times` is a list of
  output times and only those times greater than or equal to 
  the restart time will be used as output times.


**No need to modify the Makefile for a restart:**  
As of v5.4.0 it is not necessary
to make any changes in the `Makefile` when doing a restart run.
Values set in the `setrun.py`
file will be used to determine if this is a restart run (in which case
the previous output directory should be added to, rather than replaced).

.. _restart_output:

Output files after a restart
----------------------------

After running the restarted computation,
the original set of output files should still be in the output directory
along with a new set from the second run.  Note that one output time may
be repeated in two frames if `clawdata.output_t0 == True` in the restarted run.

**New in 5.4.0.**
Gauge output from the original run 
is no longer overwritten by the second run. Instead gauge
output from the restart run will be appended to the end of each
`gaugeXXXXX.txt` file (or `gaugeXXXXX.bin` in the case of binary gauge
output, introduced in v5.9.0).  

Note that if you have to restart a computation from a checkpoint
file that is at an earlier time than the original computation
reached, then intermediate gauge outputs will be repeated twice,
and data from these output files may have to be adjusted to account
for this.  If multiple restarts are performed from the same checkpoint
file then gauge data will accumulate in an undesirable fashion, but
for most purposes this does the right thing.

