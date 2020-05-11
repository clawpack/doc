"""
Convert Jupyter notebooks in $CLAW/apps/ directory to html files after
executing the notebook.  

The notebooks are put in $CLAW/doc/gallery/apps with the same subdirectory
structure as in $CLAW/apps.

As of v5.7.0:
No longer assume they are in apps/notebooks, and put apps/etc in _static/ path.
"""

from __future__ import print_function

import subprocess
import os

try:
    CLAW = os.environ['CLAW']
    apps_dir = os.path.join(CLAW,'apps')
    assert os.path.isdir(apps_dir), "*** apps repository missing?"
except:
    print("$CLAW/apps must point to the apps repository")

static_apps_dir = os.path.join(CLAW,'doc','gallery','_static','apps')

cmd = 'mkdir -p %s' % static_apps_dir
print('>>> %s' % cmd)
os.system(cmd)

notebooks = ['notebooks/geoclaw/topotools_examples.ipynb',
             'notebooks/geoclaw/dtopotools_examples.ipynb',
             'notebooks/geoclaw/Okada.ipynb',
             'notebooks/geoclaw/chile2010a/chile2010a.ipynb',
             'notebooks/geoclaw/chile2010b/chile2010b.ipynb',
             'notebooks/amrclaw/advection_2d_square/amrclaw_advection_2d_square.ipynb',
             'notebooks/classic/advection_1d/advection_1d.ipynb',
             'notebooks/classic/acoustics_1d_example1/acoustics_1d_example1.ipynb']

# for testing:
notebooks = ['notebooks/geoclaw/Okada.ipynb']


for nb in notebooks:
    nbdir, nbname = os.path.split(nb)
    input_file = os.path.join(apps_dir, nb)
    output_file = os.path.join(static_apps_dir, nb.replace('ipynb','html'))
    cmd = 'mkdir -p %s' % os.path.join(static_apps_dir, nbdir)
    print('>>> %s' % cmd)
    os.system(cmd)

    args = ["jupyter", "nbconvert", 
            "--to", "html", 
            "--execute",
            "--output", output_file,
            "--ExecutePreprocessor.kernel_name=python3",
            "--ExecutePreprocessor.timeout=1200", 
            input_file]

    cmd = ' '.join(args)
    print('>>> %s' % cmd)

    subprocess.check_call(args)

