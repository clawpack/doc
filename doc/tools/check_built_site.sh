#!/usr/bin/env bash
#
# Validate a promoted multiversion build before it is allowed anywhere near
# the published site.
#
# Usage: doc/tools/check_built_site.sh <html_dir> [min_versions]
#
# Checks, in order of what they protect against:
#
#   1. A site with no root.  `make versions` on its own produces only version
#      subdirectories -- see howto_doc.rst.  Publishing that would leave
#      www.clawpack.org/installing.html a 404.
#   2. An unpromoted or half-promoted tree, detected via the sidebar version
#      links: after promotion the root's links must be './dev/', not '../dev/'.
#   3. A missing .nojekyll, without which GitHub Pages refuses to serve the
#      _static and _sources directories (every page loses its CSS).
#   4. A missing or wrong CNAME, which would drop the www.clawpack.org custom
#      domain.
#   5. A version whitelist that silently dropped versions -- most importantly
#      the sphinx-multiversion remote-ref behaviour that makes v5.14.x vanish
#      in CI (see .github/workflows/docs-publish.yml).

set -euo pipefail

HTML=${1:?usage: check_built_site.sh <html_dir> [min_versions]}
# 9 buildable versions: dev, v5.14.x, and tags v5.7.x-v5.13.x.  Tags v5.1.x
# through v5.6.x match the whitelist but their conf.py no longer loads, so
# sphinx-multiversion skips them -- see KNOWN_UNBUILDABLE in check_versions.py.
MIN_VERSIONS=${2:-9}
EXPECTED_CNAME=www.clawpack.org

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "ok   $*"; }

[ -d "$HTML" ] || fail "$HTML is not a directory"

# 1. Site root exists and is not empty.
[ -s "$HTML/index.html" ] \
    || fail "$HTML/index.html missing or empty -- the promote step did not run"
pass "site root index.html present"

# 2. The promote step rewrote the version-switcher links.
if grep -q 'href="\.\./dev/' "$HTML/index.html"; then
    fail "$HTML/index.html still has '../dev/' links -- promote step incomplete"
fi
if ! grep -q 'href="\./dev/' "$HTML/index.html"; then
    fail "$HTML/index.html has no './dev/' link -- version switcher missing"
fi
pass "root version-switcher links rewritten to ./dev/"

# 3 and 4. Pages needs both of these at the root, and both come from
# doc/extra_files via html_extra_path.
[ -f "$HTML/.nojekyll" ] \
    || fail "$HTML/.nojekyll missing -- Pages would not serve _static/_sources"
pass ".nojekyll present"

[ -f "$HTML/CNAME" ] || fail "$HTML/CNAME missing -- custom domain would drop"
if [ "$(tr -d '[:space:]' < "$HTML/CNAME")" != "$EXPECTED_CNAME" ]; then
    fail "$HTML/CNAME is '$(cat "$HTML/CNAME")', expected $EXPECTED_CNAME"
fi
pass "CNAME is $EXPECTED_CNAME"

# 5. Every version directory is present and non-empty.  Version dirs are the
# immediate subdirectories named 'dev' or 'v<major>.<minor>.x'.
n_versions=0
missing=""
while IFS= read -r version; do
    n_versions=$((n_versions + 1))
    [ -s "$HTML/$version/index.html" ] || missing="$missing $version"
done < <(
    find "$HTML" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; \
        | grep -E '^(dev|v[0-9]+\.[0-9]+\.x)$' | sort
)

[ -z "$missing" ] || fail "version dir(s) with no index.html:$missing"

if [ "$n_versions" -lt "$MIN_VERSIONS" ]; then
    echo "versions found:" >&2
    find "$HTML" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; \
        | grep -E '^(dev|v[0-9]+\.[0-9]+\.x)$' | sort >&2
    fail "found $n_versions version dirs, expected at least $MIN_VERSIONS"
fi
pass "$n_versions version dirs, all with a non-empty index.html"

echo
echo "$HTML looks publishable."
