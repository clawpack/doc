
.. _howto_doc:

Guide for updating this documentation
=============================================

Out of date -- see the README.md at https://github.com/clawpack/doc

The restructured text files are in the `clawpac/doc
<https://github.com/clawpack/doc>`_ repository in `$CLAW/doc/doc`.

Before proceeding, first make sure other repositories are checked out to
master, since some pages now have literalinclude's that bring in code 
(e.g. setaux_defaults.rst, etc).

To create html files::

    cd $CLAW/doc/doc
    make html

To view the files, point your browser to `$CLAW/doc/doc/_build/html/index.html`

If you like what you see, you can push back to your fork and then issue a
pull request to have these changes incorporated into the documentation.


Updating the webpages
---------------------

A few developers can push html files to the repository
`clawpack/clawpack.github.com
<https://github.com/clawpack/clawpack.github.com>`_ 
which causes them to show up on the web at
`http://clawpack.github.io
<http://clawpack.github.io>`_.  

To do so, first create the html files as described above in
`$CLAW/doc/doc/_build/html`.  Commit any changed source files and 
push to `clawpack/doc <https://github.com/clawpack/doc>`_.

Then do::

    cd $CLAW/clawpack.github.com
    git checkout master
    git pull origin  # make sure you are up to date before doing next steps!

    cd $CLAW/doc/doc
    source rsync_clawpack.github.sh     

This copies the contents of `$CLAW/doc/doc/_build/html/` to 
`$CLAW/clawpack.github.com/`

Then move to the latter repository and add and commit any new or changed files. 
All files are needed, so ::

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

Note that `<http://clawpack.org>`_ and `<http://www.clawpack.org>`_
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
