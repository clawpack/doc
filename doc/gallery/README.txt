
To build the gallery (e.g. for amrclaw):

  python make_plots.py $CLAW/amrclaw/examples
  python gallery.py
  cd ..
  make html

To make plots for all examples:
  python make_plots.py
This will prompt for each repository and will overwrite the make_plots_errors.txt 
file each time so you might want to open that in a different window.