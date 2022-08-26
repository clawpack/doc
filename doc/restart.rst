

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

See the comments in :ref:`setrun_sample` for examples.

The checkpoint files are saved in the same output directory as the solution
output, with file names of the form `fort.tchkNNNNN` (a small ASCII file) and
`fort.chkNNNNN` (a large binary file)  where `NNNNN` is the
step number on the coarsest level.  These files containt all the information
needed to restart the computation at this point.

.. _restart_restart:

Restarting a computation
-------------------------

To restart a computation from any point where checkpoint files have been saved,
modify `setrun.py` to set::

    clawdata.restart = True
    clawdata.restart_file = 'fort.chkNNNNN' 

where `NNNNN` is the time step number from which the restart should
commence.  

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

.. _restart_makefile:

Modifying the Makefile for a restart
------------------------------------

**New in 5.4.0.** It is no longer necessary to set the `Makefile` variable
`RESTART` to `True` or `False`.  Instead you can set it to `None` (or omit
setting it at all, since this is the default), in which case the `setrun.py`
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



