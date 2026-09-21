#!/usr/bin/env python3
"""Every internal href on the site resolves to a file that exists.

⛔ THIS PASS DELETED TWO PAGES (floor plans, homesites) that thirty and
thirty-six links pointed at. A dead nav item on a community site that people
reach by reading a SIGN ON THE PROPERTY -- Ranee, 2026-09-21, on how anyone
finds this site at all: "Sign on the property. Okay, that's my point. And
that's it." -- is not recoverable by a search result. So the links get a gate.
"""
import pathlib, re, sys
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "node_modules", "tools", "data"}
HREF = re.compile(r'(?:href|src)="([^"]+)"')

def main():
    pages = [p for p in ROOT.rglob("*.html") if not (SKIP & set(p.relative_to(ROOT).parts))]
    bad = []
    for p in pages:
        base = p.parent
        for raw in HREF.findall(p.read_text()):
            u = urlparse(raw)
            # `src="${imageBasePath}${num}.jpg"` in gallery.html is a JS
            # template literal filled at runtime, not an href.
            if u.scheme or "${" in raw or raw.startswith(("#", "//", "mailto:", "tel:", "data:")):
                continue
            path = unquote(u.path)
            if not path:
                continue
            target = (base / path).resolve()
            if path.endswith("/") or not pathlib.PurePath(path).suffix:
                ok = (target / "index.html").exists() or target.exists()
            else:
                ok = target.exists()
            if not ok:
                bad.append(f"{p.relative_to(ROOT)} -> {raw}")

    print(f"{len(pages)} pages, {len(bad)} broken internal links")
    for b in sorted(set(bad)):
        print("  ", b)
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
