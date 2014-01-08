
Instead of the first set of instructions below invoking make_plots.py, 
can use:
  python make_all_gallery.py


To build the gallery:

  export GIT_STATUS=True   # to save git info in each _output
  python make_plots.py $CLAW/classic/examples
  python make_plots.py $CLAW/amrclaw/examples
  export CLAW_TOPO_DOWNLOAD=True
  python make_plots.py $CLAW/geoclaw/examples
  python make_plots.py $CLAW/apps/fvmbook

  python gallery.py
  cd ..
  make html

To make plots for all examples:
  python make_plots.py
This will prompt for each repository and will overwrite the files
make_plots_errors.txt   and  make_plots_output.txt
each time so you might want to open those files in a different window.

Before running rsync_clawpack.github.sh, make sure there are no extraneous
frames left from earlier tests:
rm -rf $CLAW/clawpack.github.com/_static/classic
rm -rf $CLAW/clawpack.github.com/_static/amrclaw
rm -rf $CLAW/clawpack.github.com/_static/geoclaw
rm -rf $CLAW/clawpack.github.com/_static/apps/fvmbook

