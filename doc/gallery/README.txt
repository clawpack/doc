
To build the gallery (e.g. for amrclaw):

  export GIT_STATUS=True   # to save git info in each _output
  python make_plots.py $CLAW/amrclaw/examples
  python gallery.py
  cd ..
  make html

To make plots for all examples:
  python make_plots.py
This will prompt for each repository and will overwrite the files
make_plots_errors.txt   and  make_plots_output.txt
each time so you might want to open those files in a different window.
