#!/usr/bin/env bash
#
# Validate a clawpack.github.com working tree after syncing a built site into
# it, and BEFORE committing.  This is the guard that makes an accidentally
# destructive publish impossible rather than merely unlikely.
#
# Usage: doc/tools/check_published_tree.sh <site_clone> <build_dir> [--prune]
#
#   site_clone  a clone of clawpack/clawpack.github.com with the sync applied
#   build_dir   the promoted build that was synced in (used to derive the set
#               of version directories the build actually produced)
#   --prune     allow deletions inside version directories only
#
# Why a hardcoded preserve list
# -----------------------------
# The published site is not a pure build artifact.  It accumulated 15 years of
# hand-maintained content that no current build produces: conference link
# pages, doxygen output, notebooks, PDFs, old doc trees.  A `rsync --delete`
# or a force-push would silently destroy all of it.  Keeping the list in a
# reviewed file, rather than in workflow YAML, means a change to it shows up
# in a pull request diff.

set -euo pipefail

SITE=${1:?usage: check_published_tree.sh <site_clone> <build_dir> [--prune]}
BUILD=${2:?usage: check_published_tree.sh <site_clone> <build_dir> [--prune]}
PRUNE=${3:-}

EXPECTED_CNAME=www.clawpack.org
# See check_built_site.sh: only 9 of the 15 whitelisted refs are buildable.
MIN_VERSIONS=9

# Top-level directories in the published site that no doc build produces.
# Verified against the master tree of clawpack/clawpack.github.com.
#
# v5.1.x-v5.6.x are here for a specific reason: they are version directories,
# so they look like build output, but sphinx-multiversion can no longer build
# them (their conf.py fails to load) and the HTML on the site is frozen output
# from an older toolchain.  Treating them as unmanaged is what keeps a
# --prune run from deleting documentation we can no longer regenerate.
PRESERVE_DIRS=(
    .doctrees
    .ipynb_checkpoints
    _plots_test
    v5.1.x
    v5.2.x
    v5.3.x
    v5.4.x
    v5.5.x
    v5.6.x
    amrclaw
    clawdev2016
    doc-5.1.0
    doxygen
    gallery
    geoclaw
    gitwash
    hpc3_2014
    junk
    list
    master
    notebooks
    old
    pdf
    sharpclaw
    sphinx-versioning
)

# Subdirectories of build-produced directories that are nonetheless
# hand-maintained.  pyclaw/ in particular is only partly build-owned.
PRESERVE_SUBDIRS=(
    pyclaw/gallery
    pyclaw/devel
)

# Root files no doc build produces.  (.nojekyll, CNAME, README.md,
# clawpack_logos.zip, objects.inv, searchindex.js and .buildinfo ARE produced,
# via doc/extra_files and the promoted version, so they are excluded here.)
PRESERVE_FILES=(
    README.txt
    clawicon.ico
    clawicon_new.ico
    clawlogo.jpg
    clawlogo_border.jpg
    clawlogo_new.jpg
    git-clone.py
    pyclaw.log
    index_old.html
    index_redirect.html
    index1.html
)

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "ok   $*"; }

[ -d "$SITE/.git" ] || fail "$SITE is not a git clone"
[ -d "$BUILD" ] || fail "$BUILD is not a directory"

git_site() { git -C "$SITE" "$@"; }

# The version directories this build actually produced.  Deletions are only
# ever permitted inside these -- deriving the list from the build (rather than
# from a pattern) is what stops a --prune run from touching a version the
# build can no longer regenerate, such as v5.1.x-v5.6.x.
built_versions=$(
    find "$BUILD" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; \
        | grep -E '^(dev|v[0-9]+\.[0-9]+\.x)$' | sort
)
[ -n "$built_versions" ] || fail "$BUILD contains no version directories"

# ---------------------------------------------------------------------------
# 1. Deletions
# ---------------------------------------------------------------------------
deleted=$(git_site diff --diff-filter=D --name-only HEAD)

if [ -n "$deleted" ]; then
    if [ "$PRUNE" != "--prune" ]; then
        echo "$deleted" | head -50 >&2
        fail "$(echo "$deleted" | wc -l | tr -d ' ') file(s) would be deleted; \
pass --prune only if that is intended"
    fi
    # Even when pruning, deletions are confined to rebuilt version dirs.
    allowed=$(echo "$built_versions" | sed 's|$|/|' | paste -sd'|' -)
    outside=$(echo "$deleted" | grep -Ev "^($allowed)" || true)
    if [ -n "$outside" ]; then
        echo "$outside" | head -50 >&2
        fail "--prune allows deletions only inside the version dirs this \
build regenerated ($(echo "$built_versions" | paste -sd',' -))"
    fi
    pass "$(echo "$deleted" | wc -l | tr -d ' ') deletion(s), all inside rebuilt version dirs (--prune)"
else
    pass "no deletions"
fi

# ---------------------------------------------------------------------------
# 2. Unmanaged paths are byte-identical
# ---------------------------------------------------------------------------
for path in "${PRESERVE_DIRS[@]}" "${PRESERVE_SUBDIRS[@]}" "${PRESERVE_FILES[@]}"; do
    # Absent is fine (the path may not exist on every branch); changed is not.
    if [ -e "$SITE/$path" ] || git_site cat-file -e "HEAD:$path" 2>/dev/null; then
        if ! git_site diff --quiet HEAD -- "$path"; then
            git_site diff --stat HEAD -- "$path" >&2
            fail "unmanaged path '$path' was modified by the sync"
        fi
    fi
done
pass "${#PRESERVE_DIRS[@]} unmanaged dirs, ${#PRESERVE_SUBDIRS[@]} subdirs and \
${#PRESERVE_FILES[@]} root files untouched"

# ---------------------------------------------------------------------------
# 3. Site invariants
# ---------------------------------------------------------------------------
[ -f "$SITE/.nojekyll" ] || fail ".nojekyll missing from $SITE"
[ -f "$SITE/CNAME" ] || fail "CNAME missing from $SITE"
if [ "$(tr -d '[:space:]' < "$SITE/CNAME")" != "$EXPECTED_CNAME" ]; then
    fail "CNAME is '$(cat "$SITE/CNAME")', expected $EXPECTED_CNAME"
fi
pass ".nojekyll present and CNAME is $EXPECTED_CNAME"

# ---------------------------------------------------------------------------
# 4. The site root came from a promoted build
# ---------------------------------------------------------------------------
[ -s "$SITE/index.html" ] || fail "$SITE/index.html missing or empty"
if grep -q 'href="\.\./dev/' "$SITE/index.html"; then
    fail "$SITE/index.html has '../dev/' links -- an unpromoted build was synced"
fi
if ! grep -q 'href="\./dev/' "$SITE/index.html"; then
    fail "$SITE/index.html has no './dev/' link -- version switcher missing"
fi
pass "site root is a promoted build"

# ---------------------------------------------------------------------------
# 5. Every version the build produced landed in the site
# ---------------------------------------------------------------------------
n_versions=0
missing=""
while IFS= read -r version; do
    n_versions=$((n_versions + 1))
    [ -s "$SITE/$version/index.html" ] || missing="$missing $version"
done <<< "$built_versions"

[ -z "$missing" ] || fail "version(s) missing from the site:$missing"
if [ "$n_versions" -lt "$MIN_VERSIONS" ]; then
    fail "build had only $n_versions version dirs, expected >= $MIN_VERSIONS"
fi
pass "$n_versions version dirs present in the site"

# ---------------------------------------------------------------------------
# 6. Change budget, for the human reading the run summary
# ---------------------------------------------------------------------------
echo
echo "Change summary:"
git_site diff --stat HEAD | tail -5
untracked=$(git_site ls-files --others --exclude-standard | wc -l | tr -d ' ')
echo "new (untracked) files: $untracked"
echo
echo "$SITE is safe to commit."
