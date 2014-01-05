.. _build-gallery:

Building the PyClaw gallery locally
===================================

You can build a local copy of the PyClaw gallery as follows: first, you should clone
the clawpack documentation repository::

    git clone git://github.com/clawpack/doc

Then run all the examples::

    cd doc/doc/pyclaw/gallery
    python gallery.py

Next generate the gallery itself::

    python gallery.py

Finally, you need to call sphinx to convert all the .rst files to .html::

    cd ../..
    make html
