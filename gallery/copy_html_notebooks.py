"""
Copy html versions of Jupyter notebooks in $CLAW/apps directory to 
    $CLAW/doc/gallery/_static/apps
with the same subdirectory structure as in $CLAW/apps.

Confirms copy for out of date html files.

If the html file for some notebook NB.ipynb is out of date or doesn't exist,
create it via:

    cd $CLAW/apps/...
    make NB.html -f $CLAW/apps/notebooks/Makefile

You can make html files from all .ipynb files in a directory via:
    cd $CLAW/apps/...
    make notebook_htmls -f $CLAW/apps/notebooks/Makefile

"""

from __future__ import print_function

import os

try:
    CLAW = os.environ['CLAW']
    apps_dir = os.path.join(CLAW,'apps')
    assert os.path.isdir(apps_dir), "*** apps repository missing?"
except:
    print("$CLAW/apps must point to the apps repository")

static_apps_dir = os.path.join(CLAW,'doc','gallery','_static','apps')


all_notebooks = [ \
    'notebooks/geoclaw/topotools_examples.ipynb',
    'notebooks/geoclaw/dtopotools_examples.ipynb',
    'notebooks/geoclaw/Okada.ipynb',
    'notebooks/geoclaw/MarchingFront.ipynb',
    'notebooks/geoclaw/ForceDry.ipynb',
    'notebooks/geoclaw/chile2010a/chile2010a.ipynb',
    'notebooks/geoclaw/chile2010b/chile2010b.ipynb',
    'notebooks/amrclaw/advection_2d_square/amrclaw_advection_2d_square.ipynb',
    'notebooks/amrclaw/RuledRectangles.ipynb',
    'notebooks/classic/advection_1d/advection_1d.ipynb',
    'notebooks/classic/acoustics_1d_example1/acoustics_1d_example1.ipynb',
    'notebooks/visclaw/animation_tools_demo.ipynb',
    'notebooks/visclaw/pcolorcells.ipynb',
    'notebooks/visclaw/gridtools.ipynb'
    ]

notebooks = all_notebooks

# only select notebooks:
#notebooks = [nb for nb in all_notebooks if 'geoclaw' in nb]
#notebooks = [nb for nb in all_notebooks if 'visclaw' in nb]

# or explicitly list:
notebooks = ['notebooks/geoclaw/MarchingFront.ipynb']

skipped = []

for nb in notebooks:
    nbdir, nbname = os.path.split(nb)
    nb_file = os.path.join(apps_dir, nb)
    html_file = nb_file.replace('ipynb','html')
    print('\n==> Notebook: %s' % nb_file)

    try:
        nb_mod_time = os.path.getmtime(nb_file)
    except:
        print('*** Jupyter notebook not found')
        print('    Skipping')
        skipped.append(nb)
        continue
    try:
        html_mod_time = os.path.getmtime(html_file)
    except:
        print('*** html version not found for notebook:')
        print('    Skipping')
        skipped.append(nb)
        continue

    if html_mod_time < nb_mod_time:
        print('*** html file might be out of date')
        ans = input('    Copy anyway? ')
    else:
        ans = 'y'

    if ans.lower() not in ['y','yes']:
        print('    Skipping')
        skipped.append(nb)
        continue # to next notebook
        
    gallery_html_file = os.path.join(static_apps_dir, nb.replace('ipynb','html'))
    cmd = 'mkdir -p %s' % os.path.join(static_apps_dir, nbdir)
    print('>>> %s' % cmd)
    os.system(cmd)

    cmd = 'cp %s %s' % (html_file, gallery_html_file)
    print('>>> %s' % cmd)
    os.system(cmd)

if len(skipped) > 0:
    print('\n*** Warning, the following were skipped:')
    for nb in skipped:
        print('    ',nb)
