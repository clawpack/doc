
.. _output_styles:

******************************
Output data sytles and formats
******************************

Output style
------------

In :ref:`setrun`, the style of specifying output times can be
specified by setting the parameter `output_style`.  This can be illustrated
by a typical example from a `setrun.py` file::


    clawdata.output_style = 1

    if clawdata.output_style==1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.num_output_times = 2
        clawdata.tfinal = 2*3600.
        clawdata.output_t0 = True  # output at initial (or restart) time?

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = [0, 1800, 7200]

    elif clawdata.output_style == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 3
        clawdata.output_t0 = False

In this case setting `clawdata.output_style==1` results in outputs at times
`clawdata.t0`, 1800, and 3600 (equally spaced in time). 
Setting `clawdata.output_style==2` results in outputs at times
0, 1800, and 7200 (not necessarily equally spaced).
Setting `clawdata.output_style==3` results in outputs after 1, 2, and 3
time steps on the coarsest grid (used primarily for debugging, or in cases
where you do not want the time steps to be adjusted to hit specific output
times).

.. _output_formats:

Output data formats
-------------------

In AMRClaw and GeoClaw, the format for the output data (solutions) can be
specified by setting the parameter `output_format` to `'ascii'`,
`'binary64'`, or `'binary32'`.  (The single-grid
`classic` code only supports ASCII output at this time.)

To read the solution stored in these files into Python for plotting or other
postprocessing purposes, utilities are provided that are described in
:ref:`pyclaw_io`.

Setting `output_format = 'ascii'` gives ASCII text output.  The data files
can then be viewed with any standard text editor, which is particularly
useful for debugging.  However, ASCII files are generally much larger than
is necessary to store the original data in binary form, and so when grid
have many grid cells or when many output frames are saved it is often better
to use some form of binary output, see :ref:`output_binary`.

In AMRClaw and GeoClaw, ASCII and binary output are both written
by the library routine `valout.f90`.  The aux arrays are also dumped
if requested, see :ref:`output_aux`.

.. _output_ascii:

ASCII output data format
------------------------

Two output files are created at each output time (each frame).  The frames
are generally numbered 0, 1, 2, etc.  The two files, at frame 2, for
example, are called `fort.t0002` and `fort.q0002`.  

`fort.t0002`
************

This file has the typical form::

    0.40000000E+00    time
    1                 meqn
   36                 ngrids
    0                 naux
    2                 ndim
    2                 nghost
 ascii                format


This file contains only 7 lines with information about the current time and the
number of AMR patches at this time, along with other metadata needed for
reading the AMR data properly. 

In the above example, Frame 2 contains 36 patches.  
If you are using the classic code
or PyClaw with only a single patch, then `ngrids` would be 1.

The data for all 36 patches is contained in `fort.q0002`.  The data from each
patch is preceeded by a header that tells where the patch is located in the
domain, how many grid cells it contains, and what the cell size is, e.g. 

`fort.q0002`
************

This header has the typical form::

    1                 grid_number
    1                 AMR_level
    40                mx
    40                my
    0.00000000E+00    xlow
    0.00000000E+00    ylow
    0.25000000E-01    dx
    0.25000000E-01    dy

This would be followed by 40*40 = 1600 lines with the data from cells (i,j).
The order they are written is (in Fortran style)::

    do j = 1,my
        do i = 1,mx
            write (q(i,j,m), m=1,meqn)

Each line has `meqn` (change to `num_eqn`?) values, for the components of
the system in this grid cell.

After the data for this patch, there would be another header for the next
patch, followed by its data, etc.

In the header, `xlow` and `ylow` are the coordinates of the lower left
corner of the patch, `dx` and `dy` are the cell width in `x` and `y`, and 
`AMR_level` is the level of refinement, where 1 is the coarsest level.  
Each patch has a unique `grid_number` that usually isn't needed for
visualization purposes.




.. _output_binary:

Raw binary output data formats
------------------------------

**New in v5.9.0:** Previously the user could specify `output_format='binary'`
for binary format. Starting in v5.9.0, the user can specify either
`output_format='binary64'` or `output_format='binary32'`.  For backward
compatibility, the former is equivalent to specifying `output_format='binary'`
and dumps full 8-byte precision values.  The new `'binary32'` option
truncates the solution values to 4-bytes before writing, cutting the file
size in half.  For *most* applications, this should still give sufficient
precision for plotting purposes.

The files for each frame are numbered as for the ASCII file and the
`fort.t0002` file, for example, is still an ASCII file with 7 lines of
metadata.  There are also ASCII files such as `fort.q0002`, but these now
contain only the headers for each grid patch and not the solution on each
patch.  In addition there are files such as
`fort.b0002` that contain a raw binary dump of the data from all of the 
grid patches at this time, one after another.  In order to decompose this
data into patches for plotting, the `fort.q0002` file must be used.

Unlike the ASCII data files, the binary output
files contain ghost cells as well as the interior cells (since a contiguous
block of memory is dumped for each patch with a single `write` statement).


.. _output_netcdf:

NetCDF output data format
------------------------------

NetCDF output is not currently supported in Clawpack. This is not a suitable
format for AMR style data.

.. _output_aux:

Output of aux arrays
---------------------

The contents of `aux` arrays can also be output along with each time frame.
Which components are output is controlled by the setrun variable 
`clawdata.output_aux_components`, which can be `'none'` (default) or `'all'`
currently.  The values, if desired, will go into files `fort.aXXXX` that
have the same format as the `q` data, as
specifed by `output_format`. Set `output_aux_onlyonce` to
`True` if the `aux` arrays do not change with time and you only want to
output these arrays once.


