
Main Clawpack documentation (Sphinx project).

Everything about building, checking and publishing it -- including a
step-by-step for each common task and what CI does for you -- is in
howto_doc.rst.  The release procedure is in howto_release.rst.

Quick local preview (in a virtualenv without clawpack installed;
see howto_doc.rst, "Setting up a build environment"):

    $ pip install -r tools/requirements-docs.txt
    $ make html          # -> _build1/html/index.html

To change the layout of pages, adjust
    _themes/flask_local/layout.html
    _themes/flask_local/static/flasky.css_t

To change the main landing page, edit
    _templates/index.html

The gallery is a separate project; see ../gallery/README.md.
