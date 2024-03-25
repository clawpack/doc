# -*- coding: utf-8 -*-
#
# Clawpack documentation build configuration file, created by
# sphinx-quickstart on Wed Mar 25 12:07:14 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# If your extensions are in another directory, add it here. If the directory
# is relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('./ext'))

clawpack_root = os.path.abspath('../..')
print("clawpack_root = %s" % clawpack_root)
sys.path.append(os.path.join(clawpack_root,'amrclaw/doc'))
sys.path.append(os.path.join(clawpack_root,'visclaw/doc'))
sys.path.append(os.path.join(clawpack_root,'geoclaw/doc'))
sys.path.append(os.path.join(clawpack_root,'pyclaw/src'))
sys.path.append(os.path.join(clawpack_root,'riemann/src/python/riemann'))


# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
# extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.coverage','sphinx.ext.viewcode','sphinx.ext.inheritance_diagram']

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'only_directives',
              'sphinx.ext.inheritance_diagram',
              'sphinx_multiversion',
              'sphinx.ext.mathjax',
              'srclinks']


mathjax_path = 'https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


# The suffix of source filenames.
source_suffix = '.rst'

# removed edit_on_github extension since it seemed to be broken
edit_on_github_project = 'clawpack/doc'
edit_on_github_branch = 'dev'

# srclink settings
srclink_project = 'https://github.com/clawpack/doc'
srclink_src_path = 'doc/'
srclink_branch = 'dev'
edit_srclink_url = True

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'contents'

# General information about the project.
project = u'Clawpack'
copyright = u'CC-BY 2024, The Clawpack Development Team'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
#version = '5.10'
version = 'dev'
# The full version, including alpha/beta/rc tags.
#release = '5.10.x'
release = 'dev'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['users']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = 'math'

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


sys.path.append(os.path.abspath('_themes'))
html_theme_path = ['_themes']
html_extra_path = ['extra_files']
html_theme = 'flask_local'

github_fork = 'clawpack'
html_additional_pages = {'index': 'index.html'}


# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    'index':    ['localtoc.html', 'srclinks.html', 'searchbox.html',
                 'versioning.html'],
    '**':       ['localtoc.html', 'relations.html',
                 'srclinks.html', 'searchbox.html', 'versioning.html']
}

# Whitelist pattern for tags (set to None to ignore all tags)
# Will show up in list of Older releases,  see _templates/versioning.html
#smv_tag_whitelist = r'^.*$'  # all tags 
smv_tag_whitelist = r'^v\d+\.\d+\.x$'  # all tags of form v*.*.x

# Whitelist pattern for branches (set to None to ignore all branches)
# Will show up in list of Latest releases,  see _templates/versioning.html
smv_branch_whitelist = r'v5.10.x|dev'

# For possible use in adding version banners?
# see https://holzhaus.github.io/sphinx-multiversion/master/templates.html#version-banners
smv_released_pattern = r'v.*'
smv_latest_version = 'v5.10.x'

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
#html_theme = 'default'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {"linkcolor": "#000000", "textcolor":"#ff0000"}
#html_theme_options = {"rightsidebar": False, "stickysidebar":True, "relbarbgcolor":"#000000"}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = ['_static']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = '_static/clawlogo.jpg'
html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/clawicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'Clawpackdoc'


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = [
  ('index', 'Clawpack.tex', r'Clawpack Documentation', r'RJL', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True


keep_warnings = True

inheritance_graph_attrs = dict(rankdir="TB",
                               fontsize=12,splines='"true"',penwidth=100)

inheritance_node_attrs = dict(fontsize=12, shape='box3d',
                              color='black', style='filled', fillcolor='gray')
