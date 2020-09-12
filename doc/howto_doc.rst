
.. _howto_doc:

Guide for updating this documentation
=============================================

See also the README.md at https://github.com/clawpack/doc.

The `clawpack/doc <https://github.com/clawpack/doc>`_ repository is not
included in the Clawpack distribution and must be cloned separately if you
want to work with these files.

After cloning into the `$CLAW` directory, the restructured text
files for the main documentation are in `$CLAW/doc/doc`.  All files
related to the gallery are in `$CLAW/doc/gallery`.  As of Version
5.4.1, these two subdirectories are separate Sphinx projects 

They used to be connected using 
`intersphinx <http://www.sphinx-doc.org/en/stable/ext/intersphinx.html>`_.  
but this was dropped in v5.7.x.

Git branches and tags
---------------------

Older versions of the documentation used to be tagged for each minor
release, e.g. `v5.6.1`.  Starting with v5.7.0, these are now only tagged
with the major release, e.g. `v5.7.x`.  

The side menu on the Sphinx pages now lists only these major tags. The
assumption is that any changes within e.g. the 5.7 version are minor enough
that the documentation should not change substantially.

There are two active **branches** at any time, one for the current major
release, e.g. `v5.7.x`, and one named `dev` for the development of documenation
for features not yet released.  When a new major release is done the
`v5.7.x` branch will be retired, creating a `v5.7.x` tag instead along with
a new `v5.8.x` branch.

As documents are improved, continue to update the current release branch,
e.g. `v5.7.x`, and also merge these changes in to the `dev` branch.  In
general `dev` should be up to date with the current release branch along
with perhaps some new documentation for features not in the current
release.

Note that the file `conf.py` contains the version number.  Please insure
that the `dev` branch and current release branch each have the correct
thing. This can easily get messed up when merging from one branch to the
other.  One way to help avoid this is to always merge via, e.g.::

    git checkout dev
    git merge v5.7.x --no-ff --no-commit 

and then check before doing the merge commit to make sure `conf.py` hasn't
been improperly changed.  If it has, and that's the only change to this
file, you can do::

    git reset HEAD conf.py
    git checkout conf.py

and check that it's correct before committing via e.g.::

    git commit -m "merged recent v5.7.x changes into dev"
    

Configuration and style files
-----------------------------

The general look of the documentation and various things that appear on each
page are controlled by the following files:

 - `conf.py` includes the version number, sets the `html_theme`, as well as
   setting paths to extensions and various other sphinx settings.
 - `_themes/flask_local/layout.html` determines the menus at the top
 - `_static/clawlogo.jpg` is the Clawpack logo put on each page
 - `_static/clawicon.ico` is the icon that appears on browser tabs
 - `_templates/index.html` contains the main landing page
 
.. _howto_doc_release:

Updating the docs for a new release
-----------------------------------

When updating the documentation for a new release, see also
:ref:`howto_release_doc` for a list of necessary changes.


Before proceeding, first make sure other repositories are checked out to
master, since some pages now have literalinclude's that bring in code 
(e.g. setaux_defaults.rst, etc).
**Note: This is no longer true.**

To create html files from the dev branch only, for example::

    cd $CLAW/doc/doc
    git checkout dev
    make html

The `Makefile` has been modified so that `make html` does this::

    sphinx-build -b html . _build1/html

To view the files, point your browser to `$CLAW/doc/doc/_build1/html/index.html`

Note that we suggest using `_build1` when building a single version so this
can be quickly rebuilt when writing and editing documentation.


To generate docs including previous versions
--------------------------------------------

This should be done when you are close to pushing changes to the website,
otherwise the above approach works fine and shows the current state of the
documentation based on files in your working directory.

This can take much longer since it rebuilds pages for all
versions.

The instructions below make webpages that list v5.4.0, etc. and allow
viewing docs that may be more relevant to a previous version of Clawpack.

As of v5.7.x, we are now using 
`sphinx-multiversion <https://holzhaus.github.io/sphinx-multiversion/master/index.html>`__
instead of 
`sphinxcontrib-versioning <https://github.com/sphinx-contrib/sphinxcontrib-versioning>`__.


To make pages that show previous Clawpack versions, first install
`sphinx-multiversion <https://holzhaus.github.io/sphinx-multiversion/master/index.html>`__.

Insure that any changes you want to show up in multiversion docs has been
committed to some branch (normally `dev` if you have been adding something new).

And then do this::

    cd $CLAW/doc/doc
    rm -rf _build   # recommended to make sure new versions are clean
    make versions

The `Makefile` has been modified so that `make versions` does this::

    sphinx-multiversion . _build/html

To view the files, point your browser to `_build/html/dev/index.html`  
and from there you should be able to navigate to other versions.
    
Unlike `sphinxcontrib-versioning`, this now uses your local branches and tags
rather than the versions on Github.  It lists only two branches under "Latest
Versions" and all tags as "Older Versions".  
The two branches are set to `dev` and the most
recent version, by this line of `conf.py`::

    smv_branch_whitelist = r'v5.7.x|dev' 
    
This should be updated for a new version.

Note that `_build/html` contains a subdirectory for each version, but there
are no `.html` files in the top level of `_build/html`.  For the Clawpack
webpage we need to:

- Copy the files from the current version to the top level so that
  navigating to http://www.clawpack.org/installing.html, 
  for example, goes to the current version of this document.
  
- Fix the links in the sidebars of each of these `.html` files so that clicking
  on `dev`, for example, takes you to http://www.clawpack.org/dev/installing.html
  
This can be done as follows::

    cd $CLAW/doc/doc/_build/html
    cp -r v5.7.x/* .   # replacing v5.7.x with the current version
    python ../../fix_links_top_level.py
    
If you like what you see, you can push back to your fork and then issue a
pull request to have these changes incorporated into the documentation.

**Note:** We are no longer using `intersphinx` to link the gallery and the 
main doc pages together.   Instead there are hard links to `www.clawpack.org`
to go from one to the other.  So the old use of 
the environment variable `SPHINX_WEB` is now deprecated.

Updating the gallery
--------------------

The gallery webpages are now decoupled from the main sphinx pages, and reside
in `$CLAW/doc/gallery` rather than `$CLAW/doc/doc`.  

To remake the galleries, you need to first run all the examples that produce
results shown in the galleries.  

For detailed instructions, see `CLAW/doc/gallery/README.md
<https://github.com/clawpack/doc/blob/dev/gallery/README.md>`_.

Then do the following::

    cd $CLAW/doc/gallery    make html

Note that we don't track past versions in the gallery.


Note that `doc/gallery/notebooks.rst` contains pointers to html versions of many
notebooks, stored in `doc/gallery/_static/notebooks`.  If any notebooks were
updated for this release, the corresponding html files should be too.
*(We should automate this).*

Updating the webpages
---------------------

A few developers can push html files to the repository
`clawpack/clawpack.github.com
<https://github.com/clawpack/clawpack.github.com>`_ 
which causes them to show up on the web at
`http://clawpack.github.io
<http://clawpack.github.io>`_.  

To do so, first create the html files as described above, which should appear
in `doc/doc/_build/html` and `doc/gallery/_build/html`.

Commit any changed source files and 
push to `clawpack/doc <https://github.com/clawpack/doc>`_.

Then do::

    cd $CLAW/clawpack.github.com
    git checkout v5.x.x
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

Pages from other clawpack repositories
--------------------------------------

Some webpages are created within other clawpack repositories. 
For example, the page http://www.clawpack.org/geoclawdev-2020/
is modified by pushing changes to the master branch of the repository
`geoclawdev-2020 <https://github.com/clawpack/geoclawdev-2020>`__.
This is configured in that repository, in the `GitHub Pages` section found 
under `Settings`.

Other repositories that create webpages include:

- `geoclawdev-2018 <https://github.com/clawpack/geoclawdev-2018>`__
- `clawdev-2016 <https://github.com/clawpack/clawdev-2016>`__
    
