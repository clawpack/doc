
"""
Script to use with this code for making multi-version docs:
    https://holzhaus.github.io/sphinx-multiversion/master/index.html

Using sphinx-multiversion creates a _build/html directory that has a
subdirectory for each version.  But the current version .html files are not
in _build/html so you can only reach them if you point to a specific version.

We copy _build/html/* to $CLAW/clawpack.github.org/ for hosting on the web.

We want e.g. www.clawpack.org/installing.html to point to the current release
(without having to specify e.g.  www.clawpack.org/v5.6.1/installing.html).
This can be accomplished by copying the v5.6.1/* files up a level, but then the
links in the sidebar don't work properly for reaching other versions.

This script fixes those links.

First do:

    sphinx-multiversion . _build/html

This creates _build/html/dev and _build_html/v5.* for each branch/tag

Then copy the files from the current release up a level and fix the links
from these files to other versions:

    cd _build/html
    cp -r v5.6.1/* .   # Note: replace v5.6.1 with current version
    python ../../fix_links_top_level.py

This changes the links in the sidebar that point to other versions, replacing
../dev with ./dev, for example.

"""

import os,sys,glob

files = glob.glob('*.html')
for file in files:
    lines = open(file,'r').readlines()
    with open(file,'w') as f:
        for line in lines:
            line = line.replace('../v5','./v5')
            line = line.replace('../dev','./dev')
            f.write(line)

    print('Done with %s' % file)
    

