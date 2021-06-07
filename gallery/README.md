# To create galleries:

## For the Fortran examples:

#### Step 1: Run all examples

Run the script `$CLAW/classic/examples/run_examples.py` and examine the files
  `make_all_errors.txt` and
  `make_all_output.txt`
for any errors.

Do the same in `$CLAW/amrclaw/examples` and `$CLAW/geoclaw/examples`, and also in `$CLAW/apps/fvmbook` for the book examples.

Alternatively, the script `$CLAW/doc/gallery/gallery/make_plots.py` can be used to run all examples.

#### Step 2: Copy files from other repos into doc repo for viewing in gallery

Edit `$CLAW/doc/gallery/gallery/gallery.py` if desired to modify the set of examples to include in the gallery, and specify which plots from each example to use as thumbnails.

Run this code to create thumbnails and copy all the plots and html files from the specified example directories into the directory `$CLAW/doc/gallery/_static`.  Subdirectories are created that parallel the repositories `amrclaw`, etc.

    
## For PyClaw:

#### Step 1: Run all examples

    cd $CLAW/doc/gallery/pyclaw/gallery
    python make_plots.py
    
#### Step 2: Copy files and make thumbnails

Run the script `gallery.py` in this same directory.

*[@ketch should update this if necessary]*

# Make the Sphinx pages

After creating the thumbnails and copying files as described above for the Fortran and/or PyClaw repositories, you can create a new set of Sphinx pages displaying these via:

    cd $CLAW/doc/gallery
    make html
    
If this worked then the file `$CLAW/doc/gallery/_build/html/index.html` should display the index and clicking on an example should show the thumbnails. Clicking on a thumbnail or the `Plots` link should take you to all plots for the example.

# Update version on website

To make gallery pages that are properly linked to the other Docs when posted
on the website, you must do::

    cd $CLAW/doc/gallery
    export SPHINX_WEB=True
    make html

The html files created must be moved to the `$CLAW/clawpack.github.com` repository and pushed to Github in order to show up on the webpages at http://www.clawpack.org/gallery/.

The shell script `$CLAW/doc/rsync_gallery.sh` can be used to `rsync` these files.

