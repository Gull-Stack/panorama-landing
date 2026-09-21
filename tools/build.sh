#!/usr/bin/env bash
# Every generator and every gate, in the order they depend on each other.
#
#   ./tools/build.sh          regenerate and rewrite
#   ./tools/build.sh --check  fail if anything committed is stale (CI)
#
# ⛔ ORDER MATTERS. build-builders writes whole pages (including their nav);
# sweep-site normalizes the nav across every page including those. Run the
# sweep first and the freshly generated builder pages miss the pass.
set -euo pipefail
cd "$(dirname "$0")/.."
A="${1:-}"

python3 tools/build-builders.py $A
python3 tools/sweep-site.py     $A
python3 tools/build-sitemap.py  $A
python3 tools/check-links.py
python3 tools/check-css.py
