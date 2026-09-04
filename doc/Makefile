# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =

# Two build directories, deliberately separate (see howto_doc.rst):
#   BUILDDIR     single-version scratch build (`make html`).  Fast, but it has
#                no site root and its sidebar version links are absent, so it
#                is NOT publishable -- it exists so a quick local build cannot
#                clobber the multiversion tree.
#   VERSIONSDIR  multiversion output (`make versions`).  This is what gets
#                published to clawpack.github.com by `make versions-publish`.
BUILDDIR      = _build1
VERSIONSDIR   = _build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

SPHINX_WEB ?= False
ifeq ($(SPHINX_WEB),True)
	LAYOUT = _themes/flask_web/layout.html
else
	LAYOUT = _themes/flask_local/layout.html
endif

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest checkwarnings checkwarnings-update checkwarnings-strict check-versions versions clean-versions versions-promote versions-publish

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  pickle     to make pickle files"
	@echo "  json       to make JSON files"
	@echo "  htmlhelp   to make HTML files and a HTML help project"
	@echo "  qthelp     to make HTML files and a qthelp project"
	@echo "  devhelp    to make HTML files and a Devhelp project"
	@echo "  epub       to make an epub"
	@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  text       to make text files"
	@echo "  man        to make manual pages"
	@echo "  changes    to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  doctest    to run all doctests embedded in the documentation (if enabled)"
	@echo "  versions          to build every whitelisted version into $(VERSIONSDIR)/html"
	@echo "  versions-promote  to copy the latest version to the site root and fix its links"
	@echo "  versions-publish  to do a clean versions build + promote (the publishable site)"
	@echo "  clean-versions    to remove $(VERSIONSDIR)"
	@echo "  checkwarnings        to fail on any NEW reST/docstring warning (vs the baseline)"
	@echo "  checkwarnings-update to regenerate the warning baseline (tools/doc_warnings_baseline.txt)"
	@echo "  checkwarnings-strict to fail on ANY reST/docstring warning, ignoring the baseline"

clean:
	-rm -rf $(BUILDDIR)/*

html:
	@echo Using LAYOUT = $(LAYOUT)
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
	@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/SharpClaw.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/SharpClaw.qhc"

devhelp:
	$(SPHINXBUILD) -b devhelp $(ALLSPHINXOPTS) $(BUILDDIR)/devhelp
	@echo
	@echo "Build finished."
	@echo "To view the help file:"
	@echo "# mkdir -p $$HOME/.local/share/devhelp/SharpClaw"
	@echo "# ln -s $(BUILDDIR)/devhelp $$HOME/.local/share/devhelp/SharpClaw"
	@echo "# devhelp"

epub:
	$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

latexpdf:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	make -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	@echo
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."

# Cheap pre-flight: sphinx-multiversion silently skips refs that are not local
# branches, and refs whose conf.py fails to load.  Catch that before spending
# a long time on the build.
check-versions:
	python tools/check_versions.py

versions: check-versions
	sphinx-multiversion . $(VERSIONSDIR)/html $(SPHINXOPTS)
	@echo
	@echo "Built one subdirectory per version in $(VERSIONSDIR)/html."
	@echo "NOTE: there is no site root yet -- run 'make versions-promote'"
	@echo "      (or use 'make versions-publish' to do both)."

clean-versions:
	-rm -rf $(VERSIONSDIR)

versions-promote:
	python tools/promote_latest.py $(VERSIONSDIR)/html

# The single entry point for publishing, used by humans and by CI alike.
# The clean matters: promoting into an already-promoted tree leaves the
# previous version's files stranded at the root.
#
# These are recursive $(MAKE) calls rather than prerequisites so the order
# holds even under `make -j`, where prerequisites could otherwise run
# concurrently and clean the tree out from under the build.
versions-publish:
	$(MAKE) clean-versions
	$(MAKE) versions
	$(MAKE) versions-promote
	@echo
	@echo "Publishable site is in $(VERSIONSDIR)/html."
	@echo "To publish by hand: cd .. && ./rsync_doc.sh"

checkwarnings:
	python tools/check_doc_warnings.py

checkwarnings-update:
	python tools/check_doc_warnings.py --update

checkwarnings-strict:
	python tools/check_doc_warnings.py --strict

