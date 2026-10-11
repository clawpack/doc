#!/usr/bin/env bash
#
# Publish the main documentation to a local clone of clawpack.github.com.
#
# Build it first with:
#
#     cd doc && make versions-publish
#
# NOTE: `make html` writes doc/_build1/html, which is a single-version scratch
# build with no site root -- it is NOT publishable.  The guard below exists to
# catch that mistake, and to catch a `make versions` that was never promoted.
#
# Set DRYRUN=1 to see what would be copied without writing anything.
#
# This is additive on purpose: no --delete.  The published site holds many
# directories this build does not produce (gallery/, amrclaw/, geoclaw/,
# doxygen/, notebooks/, pdf/, ...), and deleting them would take down large
# parts of www.clawpack.org.

set -euo pipefail

SRC=doc/_build/html
DEST=../clawpack.github.com

if [ ! -f "$SRC/index.html" ]; then
    echo "error: no promoted build found at $SRC/index.html" >&2
    echo "       run 'cd doc && make versions-publish' first" >&2
    exit 1
fi

if [ ! -d "$DEST" ]; then
    echo "error: $DEST does not exist" >&2
    echo "       clone clawpack/clawpack.github.com next to this repo" >&2
    exit 1
fi

rsync -av ${DRYRUN:+--dry-run} "$SRC"/ "$DEST"/
