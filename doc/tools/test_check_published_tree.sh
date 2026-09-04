#!/usr/bin/env bash
#
# Tests for check_published_tree.sh.
#
# Usage: doc/tools/test_check_published_tree.sh
#
# The negative cases matter more than the positive one: this guard exists to
# stop a publish that would delete parts of www.clawpack.org that no build can
# regenerate, so the tests assert that it actually refuses.

set -uo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
GUARD=$HERE/check_published_tree.sh

VERSIONS="dev v5.14.x v5.13.x v5.12.x v5.11.x v5.10.x v5.9.x v5.8.x v5.7.x"

# Top-level paths the published site has but no build produces.  A subset of
# the real list is enough to exercise the logic.
UNMANAGED_DIRS="gallery doxygen notebooks pdf v5.1.x v5.6.x"
UNMANAGED_FILES="README.txt clawlogo.jpg index_redirect.html"

n_pass=0
n_fail=0

report() {
    if [ "$1" = "pass" ]; then
        n_pass=$((n_pass + 1)); echo "PASS  $2"
    else
        n_fail=$((n_fail + 1)); echo "FAIL  $2"
    fi
}

# expect_ok <name> -- guard must succeed
expect_ok() {
    local name=$1; shift
    if "$@" >/dev/null 2>&1; then report pass "$name"; else
        report fail "$name (guard rejected a safe tree)"
        "$@" 2>&1 | tail -5 | sed 's/^/        /'
    fi
}

# expect_fail <name> <expected substring> -- guard must refuse
expect_fail() {
    local name=$1 want=$2; shift 2
    local out
    if out=$("$@" 2>&1); then
        report fail "$name (guard ALLOWED an unsafe tree)"
    elif ! echo "$out" | grep -q "$want"; then
        report fail "$name (refused, but not for the expected reason)"
        echo "$out" | tail -5 | sed 's/^/        /'
    else
        report pass "$name"
    fi
}

# Build a fake promoted multiversion build.
make_build() {
    local build=$1
    mkdir -p "$build"
    for v in $VERSIONS; do
        mkdir -p "$build/$v"
        echo "<a href=\"../dev/index.html\">dev</a>" > "$build/$v/index.html"
    done
    # Promoted root: links already rewritten to ./
    echo "<a href=\"./dev/index.html\">dev</a>" > "$build/index.html"
    echo "www.clawpack.org" > "$build/CNAME"
    : > "$build/.nojekyll"
    mkdir -p "$build/_static"
    echo "body{}" > "$build/_static/style.css"
}

# Build a fake clawpack.github.com clone, committed.
make_site() {
    local site=$1
    mkdir -p "$site"
    git -C "$site" init --quiet
    git -C "$site" config user.email t@example.com
    git -C "$site" config user.name test

    for v in $VERSIONS; do
        mkdir -p "$site/$v"
        echo "<a href=\"../dev/index.html\">dev</a>" > "$site/$v/index.html"
    done
    for d in $UNMANAGED_DIRS; do
        mkdir -p "$site/$d"
        echo "hand-maintained content" > "$site/$d/index.html"
    done
    for f in $UNMANAGED_FILES; do
        echo "hand-maintained" > "$site/$f"
    done
    mkdir -p "$site/pyclaw/gallery"
    echo "pyclaw gallery" > "$site/pyclaw/gallery/gallery_all.html"

    echo "<a href=\"./dev/index.html\">dev</a>" > "$site/index.html"
    echo "www.clawpack.org" > "$site/CNAME"
    : > "$site/.nojekyll"

    git -C "$site" add -A
    git -C "$site" commit --quiet -m "initial site"
}

with_fixture() {
    ROOT=$(mktemp -d)
    BUILD=$ROOT/site-build
    SITE=$ROOT/site
    make_build "$BUILD"
    make_site "$SITE"
}

cleanup() { rm -rf "$ROOT"; }

# ---------------------------------------------------------------------------
echo "== the additive sync the workflow actually performs =="
with_fixture
rsync -a "$BUILD"/dev/ "$SITE"/dev/
rsync -a --exclude='/dev/' --exclude='/v*.*.x/' "$BUILD"/ "$SITE"/
expect_ok "additive sync is accepted" "$GUARD" "$SITE" "$BUILD"
cleanup

# ---------------------------------------------------------------------------
echo
echo "== the failure this guard exists to prevent =="
# A bare `rsync -a --delete` at the site root does not just remove published
# content -- it removes .git along with it, destroying the repository. The
# guard cannot even inspect the result, which is itself a refusal.
with_fixture
rsync -a --delete "$BUILD"/ "$SITE"/
expect_fail "root --delete (which also eats .git) is refused" \
    "not a git clone" "$GUARD" "$SITE" "$BUILD"
cleanup

# The more realistic careless case: --delete with .git spared, so the repo
# survives and the damage shows up as staged deletions.
with_fixture
rsync -a --delete --exclude='/.git/' "$BUILD"/ "$SITE"/
expect_fail "root --delete is refused" "would be deleted" \
    "$GUARD" "$SITE" "$BUILD"
cleanup

with_fixture
rsync -a --delete --exclude='/.git/' "$BUILD"/ "$SITE"/
# ...and --prune must not rescue it: the deletions are outside version dirs.
expect_fail "root --delete is refused even with --prune" \
    "only inside the version dirs" \
    "$GUARD" "$SITE" "$BUILD" --prune
cleanup

# ---------------------------------------------------------------------------
echo
echo "== unmanaged content must not be modified =="
with_fixture
rsync -a "$BUILD"/dev/ "$SITE"/dev/
echo "clobbered" > "$SITE/gallery/index.html"
expect_fail "modified unmanaged dir is refused" "was modified by the sync" \
    "$GUARD" "$SITE" "$BUILD"
cleanup

with_fixture
rsync -a "$BUILD"/dev/ "$SITE"/dev/
echo "clobbered" > "$SITE/README.txt"
expect_fail "modified unmanaged root file is refused" \
    "was modified by the sync" "$GUARD" "$SITE" "$BUILD"
cleanup

with_fixture
rsync -a "$BUILD"/dev/ "$SITE"/dev/
echo "clobbered" > "$SITE/pyclaw/gallery/gallery_all.html"
expect_fail "modified pyclaw/gallery is refused" "was modified by the sync" \
    "$GUARD" "$SITE" "$BUILD"
cleanup

# A version directory the build can no longer regenerate is unmanaged too.
with_fixture
rm -rf "$SITE/v5.1.x"
expect_fail "deleting a frozen version dir is refused" "would be deleted" \
    "$GUARD" "$SITE" "$BUILD"
cleanup

# ---------------------------------------------------------------------------
echo
echo "== site invariants =="
with_fixture
echo "example.com" > "$SITE/CNAME"
expect_fail "wrong CNAME is refused" "CNAME is" "$GUARD" "$SITE" "$BUILD"
cleanup

# .nojekyll is tracked in the site repo, so losing it trips the deletion
# check first.  Either way the publish is refused, which is what matters --
# without it Pages stops serving _static and every page loses its CSS.
with_fixture
rm "$SITE/.nojekyll"
expect_fail "missing .nojekyll is refused" "would be deleted" \
    "$GUARD" "$SITE" "$BUILD"
cleanup

# The invariant check itself, reached when the file was never tracked.
with_fixture
git -C "$SITE" rm --quiet --cached .nojekyll
git -C "$SITE" commit --quiet -m "untrack .nojekyll"
rm "$SITE/.nojekyll"
expect_fail "absent untracked .nojekyll is refused" ".nojekyll missing" \
    "$GUARD" "$SITE" "$BUILD"
cleanup

# ---------------------------------------------------------------------------
echo
echo "== an unpromoted build must not reach the site =="
with_fixture
# `make versions` without the promote step: root links keep the extra ../
echo "<a href=\"../dev/index.html\">dev</a>" > "$SITE/index.html"
expect_fail "unpromoted root is refused" "unpromoted build" \
    "$GUARD" "$SITE" "$BUILD"
cleanup

# ---------------------------------------------------------------------------
echo
echo "== a partial build must not reach the site =="
with_fixture
rm -rf "$BUILD"/v5.7.x "$BUILD"/v5.8.x "$BUILD"/v5.9.x
rsync -a "$BUILD"/dev/ "$SITE"/dev/
expect_fail "too few versions is refused" "expected >=" \
    "$GUARD" "$SITE" "$BUILD"
cleanup

# ---------------------------------------------------------------------------
echo
echo "== --prune inside a rebuilt version dir is allowed =="
with_fixture
echo "stale page" > "$SITE/dev/removed_page.html"
git -C "$SITE" add -A
git -C "$SITE" commit --quiet -m "add a stale page"
rsync -a --delete "$BUILD"/dev/ "$SITE"/dev/
expect_ok "prune inside dev/ is accepted" \
    "$GUARD" "$SITE" "$BUILD" --prune
cleanup

echo
echo "$n_pass passed, $n_fail failed"
[ "$n_fail" -eq 0 ]
