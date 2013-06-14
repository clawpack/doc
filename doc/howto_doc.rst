
.. _howto_doc:

How-to guide for updating this documentation
=============================================

The restructured text files are in the `clawpac/doc
<https://github.com/clawpack/doc>`_ repository in `$CLAW/doc/doc`.

To create html files::

    $ cd $CLAW/doc/doc
    $ make html

To view the files, point your browser to `$CLAW/doc/doc/_build/html/index.html`

To post these on the web::

    $ source rsync_clawpack.github.sh     

This copies the contents of `$CLAW/doc/doc/_build/html/` to 
`$CLAW/clawpack.github.org/doc`


Then add and commit any new or changed files in this repository::

    $ cd $CLAW/clawpack.github.org/doc
    $ git add ...  # and commit

Pushing to the repository
`clawpack/clawpack.github.com
<https://github.com/clawpack/clawpack.github.com>`_ 
causes them to show up on the web at
`http://clawpack.github.io/doc/index.html
<http://clawpack.github.io/doc/index.html>`_.  If you do this, make sure you
also push the related commits of source files to `clawpack/doc
<https://github.com/clawpack/doc>`_.

(To do so you need permission to push to this clawpack repository. Or you
can push to your fork and issue a pull request, but it is better to issue
the pull request on the source file repository `clawpack/doc` instead.)
    




