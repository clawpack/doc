"""
Convert Jupyter notebooks in $CLAW/apps/notebooks directory to html files after
executing the notebook.  

The notebooks are put in $CLAW/doc/gallery/notebooks with the same subdirectory
structure as in $CLAW/apps/notebooks.
"""

from __future__ import print_function

import subprocess
import os

try:
    CLAW = os.environ['CLAW']
    apps_notebooks = os.path.join(CLAW,'apps','notebooks')
    assert os.path.isdir(apps_notebooks), "*** apps repository missing?"
except:
    print("$CLAW/apps must point to the apps repository")

static_notebook_dir = os.path.join(CLAW,'doc','gallery','_static','notebooks')

cmd = 'mkdir -p %s' % static_notebook_dir
print('>>> %s' % cmd)
os.system(cmd)

notebooks = ['geoclaw/topotools_examples.ipynb',
             'geoclaw/dtopotools_examples.ipynb',
             'geoclaw/Okada.ipynb',
             'geoclaw/chile2010a/chile2010a.ipynb',
             'geoclaw/chile2010b/chile2010b.ipynb',
             'amrclaw/advection_2d_square/amrclaw_advection_2d_square.ipynb',
             'classic/advection_1d/advection_1d.ipynb',
             'classic/acoustics_1d_example1/acoustics_1d_example1.ipynb']

#notebooks = ['classic/acoustics_1d_example1/acoustics_1d_example1.ipynb']


for nb in notebooks:
    nbdir, nbname = os.path.split(nb)
    input_file = os.path.join(apps_notebooks, nb)
    output_file = os.path.join(static_notebook_dir, nb.replace('ipynb','html'))
    cmd = 'mkdir -p %s' % os.path.join(static_notebook_dir, nbdir)
    print('>>> %s' % cmd)
    os.system(cmd)

    args = ["jupyter", "nbconvert", 
            "--to", "html", 
            "--execute",
            "--output", output_file,
            "--ExecutePreprocessor.kernel_name=python2",
            "--ExecutePreprocessor.timeout=600", 
            input_file]

    cmd = ' '.join(args)
    print('>>> %s' % cmd)

    subprocess.check_call(args)

