#!/usr/bin/env python
# encoding: utf-8
r"""
One definition of "which Clawpack source tree are we documenting?".

``conf.py`` and every tool under ``tools/`` must agree on this, or the warning
baseline stops being comparable: ``check_doc_warnings.py`` rewrites warning
locations relative to this root, so a tool that picks a different root produces
different signatures for the same warning.

The default is the parent of this repository -- the ordinary ``$CLAW`` layout,
where ``doc`` sits next to ``geoclaw``, ``pyclaw`` and the rest, and
``clawpack/__init__.py`` maps ``clawpack.geoclaw`` onto
``geoclaw/src/python/geoclaw``.

Setting ``CLAW`` overrides it.  That is how the docs get built against the
pinned tree (``tools/clawpack-ref.txt``, ``make claw-pin``) without anyone
having to move their checkout around, and it is what CI uses.
"""

from __future__ import annotations

import os


TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(TOOLS_DIR)        # doc/doc -- the sphinx source dir

CLAW_ROOT_HELP = """\
The docs are built against a Clawpack source tree, selected by $CLAW and
defaulting to the parent of this repository.  To build against the pinned
tree instead:

    make claw-pin                 # clone tools/clawpack-ref.txt into ../.claw-pin
    CLAW=$(cd ../.claw-pin && pwd) make checkwarnings

Use a virtualenv with no clawpack installed: an editable or pip-installed
clawpack registers a meta-path finder that shadows the source tree no matter
what sys.path says."""


def claw_root() -> str:
    """Absolute path of the Clawpack source tree to document."""
    override = os.environ.get('CLAW')
    if override:
        return os.path.abspath(override)
    return os.path.abspath(os.path.join(SRC_DIR, os.pardir, os.pardir))
