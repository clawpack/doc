#!/usr/bin/env python
"""
Pre-flight check: report which versions sphinx-multiversion will actually
build, and fail *before* a long build if the set is wrong.

Run from the Sphinx source directory (doc/)::

    python tools/check_versions.py

This exists because sphinx-multiversion can silently build fewer versions than
you expect, and the failure is expensive and easy to miss.

The trap
--------
``sphinx_multiversion.git.get_refs`` only considers ``refs/heads/*`` and
``refs/tags/*``.  Remote-tracking refs are skipped entirely unless
``smv_remote_whitelist`` is set (its default is ``None``, and the relevant
branch reads ``elif ref.is_remote and remote_whitelist is not None``).

``git clone`` and ``actions/checkout`` create a *local* branch only for the
ref they check out.  Everything else is a remote-tracking ref.  So on a fresh
CI checkout -- and on any local clone where you have never checked the branch
out -- ``refs/heads/v5.14.x`` does not exist, and v5.14.x is dropped from the
build without any error.  Since ``smv_latest_version`` is v5.14.x, and that is
the version promoted to the site root, the result is a published site with no
root at all.

Rather than set ``smv_remote_whitelist`` (which makes CI and local builds
resolve refs differently and creates duplicate local/remote entries for the
same branch), we require the branches to exist locally and print the exact
command to create any that are missing.

The second trap
---------------
sphinx-multiversion also drops any ref whose ``conf.py`` fails to load, with
only a ``Failed load config for ...`` line on stderr and a zero exit status.
The tags v5.1.x through v5.6.x hit this: their ``conf.py`` lists a
``plot_directive`` extension that no longer resolves, and they predate
``sphinx_multiversion`` being added to ``extensions`` (v5.7.x is the first tag
that has it).  Their HTML on www.clawpack.org is frozen output from an older
toolchain, and the publish sync is additive, so it survives untouched.

Those six are therefore recorded in KNOWN_UNBUILDABLE below.  The point of
listing them explicitly rather than lowering a threshold is that any *new*
version dropping out still fails this check.
"""

import argparse
import json
import os
import re
import subprocess
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.dirname(TOOLS_DIR)

# Refs that match the whitelists but whose conf.py cannot be loaded by a
# supported Sphinx.  See "The second trap" above.  Their content is already
# published and the sync never deletes it, so dropping them is not data loss --
# but the set must not grow silently.
KNOWN_UNBUILDABLE = {
    "v5.1.x",
    "v5.2.x",
    "v5.3.x",
    "v5.4.x",
    "v5.5.x",
    "v5.6.x",
}


def conf_value(source, name):
    match = re.search(
        r"""^%s\s*=\s*r?['"]([^'"]*)['"]""" % re.escape(name),
        source,
        re.MULTILINE,
    )
    return match.group(1) if match else None


def local_refs():
    """Return (branches, tags) that exist as local refs."""
    out = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname)", "refs/heads", "refs/tags"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    branches, tags = [], []
    for line in out.splitlines():
        if line.startswith("refs/heads/"):
            branches.append(line[len("refs/heads/") :])
        elif line.startswith("refs/tags/"):
            tags.append(line[len("refs/tags/") :])
    return branches, tags


def remote_branches():
    """Return remote-tracking branch names as {short_name: full_ref}."""
    out = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname)", "refs/remotes"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    found = {}
    for line in out.splitlines():
        parts = line.split("/", 4)  # refs/remotes/<remote>/<name...>
        if len(parts) < 4:
            continue
        name = parts[3] if len(parts) == 4 else "/".join(parts[3:])
        if name != "HEAD":
            found.setdefault(name, line)
    return found


def dump_metadata(confdir):
    """Return the version names sphinx-multiversion would build, or None."""
    result = subprocess.run(
        [
            "sphinx-multiversion",
            "--dump-metadata",
            confdir,
            os.path.join(confdir, "_build", "html"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return None

    # conf.py prints to stdout (e.g. "clawpack_root = ..."), once per ref, so
    # the JSON document does not start at byte 0.  Find where it does.
    start = result.stdout.find("{")
    if start < 0:
        sys.stderr.write(result.stdout)
        return None
    try:
        return sorted(json.loads(result.stdout[start:]))
    except json.JSONDecodeError:
        sys.stderr.write(result.stdout)
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "--conf", default=os.path.join(DOC_DIR, "conf.py"), help="path to conf.py"
    )
    parser.add_argument(
        "--no-dump",
        action="store_true",
        help="skip running sphinx-multiversion; check local refs only",
    )
    parser.add_argument(
        "--create-local-branches",
        action="store_true",
        help="create local branches for whitelisted remote branches that are "
        "missing (for CI, where actions/checkout leaves only one local "
        "branch); without this the command is printed for you to run",
    )
    args = parser.parse_args(argv)

    with open(args.conf) as f:
        source = f.read()

    latest = conf_value(source, "smv_latest_version")
    branch_pat = conf_value(source, "smv_branch_whitelist")
    tag_pat = conf_value(source, "smv_tag_whitelist")

    if not latest:
        sys.exit("conf.py does not define smv_latest_version")

    branches, tags = local_refs()

    # Materialise whitelisted branches that exist only as remote-tracking
    # refs.  Opt-in, because it mutates the repository: CI passes the flag,
    # humans get the command printed instead (see below).
    if args.create_local_branches:
        remotes = remote_branches()
        for name, ref in sorted(remotes.items()):
            if name in branches or not re.match(branch_pat, name):
                continue
            print("creating local branch %s from %s" % (name, ref))
            subprocess.run(["git", "branch", name, ref], check=True)
        branches, tags = local_refs()

    wanted_branches = [b for b in branches if re.match(branch_pat, b)]
    wanted_tags = [t for t in tags if re.match(tag_pat, t)]
    expected = sorted(wanted_branches + wanted_tags)

    print("smv_branch_whitelist = %r -> local branches: %s"
          % (branch_pat, ", ".join(sorted(wanted_branches)) or "(none)"))
    print("smv_tag_whitelist    = %r -> %d local tag(s)"
          % (tag_pat, len(wanted_tags)))
    print("smv_latest_version   = %r" % latest)
    print("expected versions (%d): %s" % (len(expected), ", ".join(expected)))

    # The critical check: is the version that becomes the site root present?
    if latest not in expected:
        remotes = remote_branches()
        print()
        if latest in remotes:
            sys.exit(
                "ERROR: %s matches the branch whitelist but exists only as a "
                "remote-tracking ref (%s), which sphinx-multiversion ignores.\n"
                "It is smv_latest_version, so the build would have no site "
                "root.\n\nCreate the local branch first:\n\n"
                "    git branch %s %s\n"
                % (latest, remotes[latest], latest, remotes[latest])
            )
        sys.exit(
            "ERROR: smv_latest_version (%s) is not among the refs that would "
            "be built.\nEither create it locally or update conf.py." % latest
        )

    if args.no_dump:
        print("\nLocal refs look right (skipped sphinx-multiversion).")
        return 0

    built = dump_metadata(DOC_DIR)
    if built is None:
        sys.exit("sphinx-multiversion --dump-metadata failed; see above")

    print("\nsphinx-multiversion will build (%d): %s"
          % (len(built), ", ".join(built)))

    dropped = set(expected) - set(built)
    unexpected = sorted(set(built) - set(expected))
    new_drops = sorted(dropped - KNOWN_UNBUILDABLE)
    recovered = sorted(KNOWN_UNBUILDABLE & set(built))

    if sorted(dropped & KNOWN_UNBUILDABLE):
        print("\nknown-unbuildable, skipped as expected (%d): %s"
              % (len(dropped & KNOWN_UNBUILDABLE),
                 ", ".join(sorted(dropped & KNOWN_UNBUILDABLE))))

    if latest not in built:
        sys.exit(
            "ERROR: smv_latest_version (%s) is not in the build; the site "
            "would have no root." % latest
        )

    if new_drops:
        sys.exit(
            "ERROR: version(s) dropped out of the build that used to be "
            "there: %s\nsphinx-multiversion skips any ref whose conf.py "
            "fails to load, and only says so on stderr. Check the "
            "'Failed load config' lines above." % ", ".join(new_drops)
        )

    if unexpected:
        sys.exit(
            "ERROR: unexpected version(s) in the build: %s"
            % ", ".join(unexpected)
        )

    if recovered:
        print(
            "\nNOTE: %s now build(s) successfully; remove from "
            "KNOWN_UNBUILDABLE in %s."
            % (", ".join(recovered), os.path.basename(__file__))
        )

    print("\nVersion set is consistent (%d buildable)." % len(built))
    return 0


if __name__ == "__main__":
    sys.exit(main())
