#!/usr/bin/env bash
# Every generator and every gate, in the order they depend on each other.
#
#   ./tools/build.sh          regenerate and rewrite
#   ./tools/build.sh --check  fail if anything committed is stale (CI)
#
# ⛔ ORDER MATTERS. Images first (pages read their sizes), brands next (they
# write into src/pages/things-to-do.html), then the pages, then the sitemap
# (it lists the pages that exist).
set -euo pipefail
cd "$(dirname "$0")/.."
A="${1:-}"

python3 tools/build-images.py   $A
python3 tools/build-brands.py   $A
python3 tools/build-site.py     $A
python3 tools/build-sitemap.py  $A
python3 tools/check-links.py
python3 tools/check-css.py
python3 tools/check-icons.py

# External images live on somebody else's CDN, so this one needs the network.
python3 tools/check-external-images.py || true
