
# clawpack/doc

This repository contains the documentation for Clawpack, published at
http://www.clawpack.org via the `clawpack/clawpack.github.com` repository.

- `doc/`: the main Sphinx documentation (all versions)
- `gallery/`: the gallery, a separate Sphinx project

## Maintainer guides

Start here.  Each guide opens with a step-by-step checklist and says which
steps are automated.

| Task | Source | On the web |
| --- | --- | --- |
| Build, check and publish the docs | [`doc/howto_doc.rst`](doc/howto_doc.rst) | [howto_doc](http://www.clawpack.org/dev/howto_doc.html) |
| Do a Clawpack release | [`doc/howto_release.rst`](doc/howto_release.rst) | [howto_release](http://www.clawpack.org/dev/howto_release.html) |
| Update the gallery | [`gallery/README.md`](gallery/README.md) | |

Short version: merging to `dev` republishes www.clawpack.org/dev/
automatically.  The top-level site and the release versions are published
from **Actions → docs-publish → Run workflow** (`full-site`), which needs a
reviewer's approval.  The gallery is always built and published by hand.

The GitHub page for this repository also hosts the main wiki pages for
Clawpack: https://github.com/clawpack/doc/wiki
