
.. _howto_doc:

Guide for updating this documentation
=============================================

See also the README.md at https://github.com/clawpack/doc

The `clawpack/doc <https://github.com/clawpack/doc>`_ repository is not
included in the Clawpack distribution and must be cloned separately if you
want to work with these files.

After cloning into the `$CLAW` directory, the restructured text
files for the main documentation are in `$CLAW/doc/doc`.  All files
related to the gallery are in `$CLAW/doc/gallery`.  As of Version
5.4.1, these two subdirectories are separate Sphinx projects connected using 
`intersphinx <http://www.sphinx-doc.org/en/stable/ext/intersphinx.html>`_.  
This is so that past versions of the main documentation pages can
be supported without past versions of the galleries.

Before proceeding, first make sure other repositories are checked out to
master, since some pages now have literalinclude's that bring in code 
(e.g. setaux_defaults.rst, etc).

To create html files::

    cd $CLAW/doc/doc
    make html

To view the files, point your browser to `$CLAW/doc/doc/_build/html/index.html`

To generate pages with old Clawpack versions
=============================================

This should be done when you are close to pushing changes to the website,
otherwise the above approach works fine and shows the current state of the
documentation based on files in your working directory.

This takes much longer than `make html` since it rebuilds pages for all
versions.

The instructions below make webpages that list v5.4.0, etc. and allow
viewing docs that may be more relevant to a previous version of Clawpack.

But note that the `.rst` files used to build these pages come form what is
checked into the `master` branch on Github (and the commits corresponding to
tags such as `v5.4.0`).  So if you have changed `.rst` files but these have
not yet been merged into `master` on Github, you will not see the changes
reflected in the html files you build.

To make pages that show previous Clawpack versions, first install the
sphinx extension via::

    pip install -U sphinx
    pip install sphinxcontrib-versioning

and then do this::

    cd $CLAW/doc/doc
    export SPHINX_WEB=False # to build for local viewing
    sphinx-versioning build -i -r master doc ./_build/html

Note that `-i` causes versions to be listed in reverse order at the bottom,
`-r master` uses the master branch for the main landing page, and `doc` is
the directory containing the `.rst` files relative to the top directory
of the Git repository. Only `.rst` files that are checked into Git on some
branch at `origin` are seen.

To view the files, point your browser to `$CLAW/doc/doc/_build/html/master/index.html`

If you like what you see, you can push back to your fork and then issue a
pull request to have these changes incorporated into the documentation.

**Note:** To make versions where the links to the gallery work properly after the
pages are pushed to the Clawpack website (but not locally), set
the environment variable `SPHINX_WEB` to True in the above steps.
This variable is used in `conf.py` to adjust the links used in
`intersphinx_mapping` since two sphinx projects are linked together.

Updating the gallery
--------------------

The gallery webpages are now decoupled from the main sphinx pages, and reside
in `$CLAW/doc/gallery` rather than `$CLAW/doc/doc`.  

To remake the galleries, you need to first run all the examples that produce
results shown in the galleries.  

For detailed instructions, see `CLAW/doc/gallery/README.md
<https://github.com/clawpack/doc/blob/master/gallery/README.md>`_.

Then do the following::

    cd $CLAW/doc/gallery
    export SPHINX_WEB=False # to build for local viewing
    sphinx-versioning build -i -r master doc ./_build/html

If the environment variable `SPHINX_WEB` is set to False (or not set) then
this makes files in which the links work to jump to the main doc files, when
viewed locally.

Set the environment variable `SPHINX_WEB` to True to make files where the
links work properly when pushed to the Clawpack webpages.
This variable is used in `conf.py` to adjust the links used in
`intersphinx_mapping` since two sphinx projects are linked together.


Updating the webpages
---------------------

A few developers can push html files to the repository
`clawpack/clawpack.github.com
<https://github.com/clawpack/clawpack.github.com>`_ 
which causes them to show up on the web at
`http://clawpack.github.io
<http://clawpack.github.io>`_.  

To do so, first create the html files as described above, with
`SPHINX_WEB=True` in both the `doc` and `gallery` directories.

Commit any changed source files and 
push to `clawpack/doc <https://github.com/clawpack/doc>`_.

Then do::

    cd $CLAW/clawpack.github.com
    git checkout master
    git pull origin  # make sure you are up to date before doing next steps!

    cd $CLAW/doc/doc
    rsync -azv _build/html/ ../../clawpack.github.com/
    
If you have updated the gallery, also do::

    rsync -azv ../gallery/_build/html/ ../../clawpack.github.com/gallery/


Then move to the `clawpack.github.com` repository and 
add and commit any new or changed files. 
All files are needed, so ::

    cd $CLAW/clawpack.github.com
    git add . 

should work.  For the commit message you might want to add the commit
hash of the most recent commit in $CLAW/doc/doc::

    cd $CLAW/clawpack.github.com
    git add . 
    git commit -m "changes from doc/doc commit <hash>"

And finally push to the web::

    git push origin

which assumes that `origin` is
`git@github.com:clawpack/clawpack.github.com.git`.

It may take a few minutes for the updated webpages to appear at 
`<http://clawpack.github.io/>`_.

Note that `<http://clawpack.org>`_ and `<http://www.clawpack.com>`_
should also resolve properly to `<http://clawpack.github.io/>`_.
and that `www.clawpack.org` should appear in the browser address bar.  The
file `extra_files/CNAME` combined with settings on the domain server
`godaddy.com` determine this behavior.

.. _extra_files:

Extra files for webpages not built by Sphinx
---------------------------------------------

Any files placed in `$CLAW/doc/doc/extra_files` will be copied verbatim
(recursively for subdirectories) to the directory
`$CLAW/doc/doc/_build/html` when Sphinx is used to build the documentation.
These will be copied to `$CLAW/clawpack.github.com/` when the 
`rsync_clawpack.github.sh` script is run and hence will appear on the
webpages.   

For example, the file `$CLAW/doc/doc/extra_files/clawdev2013/index.html`
should appear at `<http://www.clawpack.org/clawdev2013/index.html>`_.

The files in `$CLAW/doc/doc/extra_files/links` provide redirects so that
links like `<http://www.clawpack.org/links/an11>`_ resolve properly to
webpages on the University of Washington server.  Links of this nature have
been provided in published paper and some contain large amounts of data that
have not been copied to Github.
