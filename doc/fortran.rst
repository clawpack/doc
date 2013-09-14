
.. _fortran:

***************
Fortran version
***************


Input parameters are generally specified in a Python script :file:`setrun.py`
and then::

   $ make .data

creates the :file:`*.data` files that the Fortran code requires.  


Makefiles
---------

Most example directories contain a :file:`Makefile` that offers several
options.  Type::

  $ make help

for a list.
Often::

  $ make .plots

is all you need to type to create the data files,
compile the code, run it, and produce plots as png and html files.

Or, if you just want to run the code and produce output without making
all the plots (and then do the plotting interactively, for example)::

  $ make .output

Note: There is a dot before ``plots`` and ``output`` in the above
commands.  

The directory where output and plots are stored is specified in the Makefile.

The Makefile in most directories includes a common Makefile found at
`$CLAW/clawutil/src/Makefile.common` that does most of the work.  
If you get the error message::

        Makefile:  /clawutil/src/Makefile.common: No such file or directory

then the environment variable `CLAW` is not set properly.  
See :ref:`setenv`.

More tips
---------

* The "make .output"
  command runs the code and stores the name of the output directory in the
  file ``.output`` and it is the modification time of this file that is checked
  relative to the dependencies. (Note: the unix command ls generally does
  not display files that start with a dot so this file may be invisible
  unless you use "ls -a".)

  If you want to re-run the code and encounter::

    $ make .output
    $ make: `.output' is up to date.

  you can remove the file ``.output`` to force the code to be run again.  

* Similarly, remove the file ``.plots`` to force the plots to be recreated.
  

* If you change the compiler flags FFLAGS in the Makefile or as an
  environment variable, then you should
  make sure that all files used are recompiled with the new flags.  The
  Makefiles as written do not catch this dependency and will not recompile
  all the .o files when the Makefile changes.  To force recompilation,
  use::

     $ make new

  See :ref:`fortran_compilers` for more about compiler flags.
