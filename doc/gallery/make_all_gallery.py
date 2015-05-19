"""
Create plots for all examples that go in the galleries
"""

from clawpack.clawutil import make_all
import os

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("Need to set CLAW environment variable")

os.environ['GIT_STATUS'] = 'True'
os.environ['CLAW_TOPO_DOWNLOAD'] = 'True'

# to test:
#examples_dir = CLAW + '/amrclaw/ex2'
#make_all.make_all(examples_dir)

if 1:
    examples_dir = CLAW + '/classic/examples'
    make_all.make_all(examples_dir)

if 0:
    examples_dir = CLAW + '/amrclaw/examples'
    make_all.make_all(examples_dir)

if 0:
    examples_dir = CLAW + '/geoclaw/examples'
    make_all.make_all(examples_dir)

if 0:
    examples_dir = CLAW + '/apps/fvmbook'
    make_all.make_all(examples_dir)

