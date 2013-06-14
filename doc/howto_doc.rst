
.. _howto_doc:

Guide for updating this documentation
=============================================

The restructured text files are in the `clawpac/doc
<https://github.com/clawpack/doc>`_ repository in `$CLAW/doc/doc`.

To create html files::

    $ cd $CLAW/doc/doc
    $ make html

To view the files, point your browser to `$CLAW/doc/doc/_build/html/index.html`

If you like what you see, you can push back to your fork and then issue a
pull request to have these changes incorporated into the documentation.


Updating the webpages
---------------------

A few developers can push html files to the repository
`clawpack/clawpack.github.com
<https://github.com/clawpack/clawpack.github.com>`_ 
which causes them to show up on the web at
`http://clawpack.github.io/doc/index.html
<http://clawpack.github.io/doc/index.html>`_.  

To do so, first create the html files as described above in
`$CLAW/doc/doc/_build/html`.  Commit any changed source files and 
push to `clawpack/doc <https://github.com/clawpack/doc>`_.

Then do::

    $ cd $CLAW/doc/doc
    $ source rsync_clawpack.github.sh     

This copies the contents of `$CLAW/doc/doc/_build/html` to 
`$CLAW/clawpack.github.org/doc`

Then add and commit any new or changed files in this repository::

    $ cd $CLAW/clawpack.github.org/doc
    $ git add ...  # and commit

And finally push to the web::

    $ git push origin

which assumes that `origin` is
`git@github.com:clawpack/clawpack.github.com.git`.
