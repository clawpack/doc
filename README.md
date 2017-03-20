
# clawpack/doc

This repository hosts contains documentation for Clawpack. By pushing `html` files created here to the `clawpack.github.com` repository, they show up automatically at http://www.clawpack.com.


The GitHub page for this repository also hosts the main wiki pages for Clawpack:
    https://github.com/clawpack/doc/wiki

Instructions to make Sphinx docs for local viewing::

```
    cd $CLAW/doc/doc              # assumes this repo is at $CLAW/doc
    export SPHINX_WEB=False       # or ok to leave unset
    make html                     # requires Sphinx
    open _build/html/index.html
```

To make version for clawpack.org webpages, assuming you have cloned 
`$CLAW/clawpack.github.com` from 
`git@github.com:clawpack/clawpack.github.com.git` and have push permission:

```
    cd $CLAW/doc/doc              # assumes this repo is at $CLAW/doc
    export SPHINX_WEB=True
    make html                     # requires Sphinx
    
    cd ..
    source rsync_doc.sh   # copies html files to $CLAW/clawpack.github.com
    
    cd $CLAW/clawpack.github.com
    git add .
    git commit
    git push       # assumes push permission to
```
    

To make gallery for local viewing / webpages, do the steps above but with
`doc/doc` replaced by `doc/gallery` and `rsync_doc.sh` replaced by
`rsync_gallery.sh`.   Note that to do this you first have to build the
gallery by running all the examples and producing plots.  See documention in
the directories below.  (Which needs to be updated.)

