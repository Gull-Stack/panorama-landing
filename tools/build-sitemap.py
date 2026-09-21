#!/usr/bin/env python3
"""Regenerate sitemap.xml from the pages that actually exist.

    python3 tools/build-sitemap.py [--check]

⛔ IT LISTED TWO DELETED PAGES. find-a-home/homesites.html and
find-a-home/floorplans.html were retired on 2026-09-21 and the sitemap still
submitted both -- a hand-maintained list of URLs drifts the first time a page
is added or removed, and nobody sees it because nobody reads a sitemap.
"""
import pathlib, re, sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://panoramahomes.com"
SKIP = {".git", "node_modules", "tools", "data"}

# Highest first. Ranee, 2026-09-21: Find Your Home is "the main place that we
# want people to go", and Amenities became a top-level destination the same day.
PRIORITY = [
    (re.compile(r"^index\.html$"), "1.0", "weekly"),
    (re.compile(r"^find-a-home/index\.html$"), "0.9", "weekly"),
    (re.compile(r"^find-a-home/builders\.html$"), "0.9", "weekly"),
    (re.compile(r"^find-a-home/builder-.*\.html$"), "0.8", "monthly"),
    (re.compile(r"^life-culture/amenities\.html$"), "0.8", "monthly"),
    (re.compile(r"^(find-a-home|life-culture|things-to-do|maps|villages)/"), "0.7", "monthly"),
    (re.compile(r"^(blog|areas)/"), "0.5", "monthly"),
]


def meta(rel):
    for pat, pri, freq in PRIORITY:
        if pat.search(rel):
            return pri, freq
    return "0.6", "monthly"


def url_for(rel):
    return BASE + "/" + ("" if rel == "index.html" else rel.replace("index.html", ""))


def build():
    pages = sorted(
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*.html")
        if not (SKIP & set(p.relative_to(ROOT).parts))
    )
    today = date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in sorted(pages, key=lambda r: (float(meta(r)[0]) * -1, r)):
        pri, freq = meta(rel)
        out += ["  <url>",
                f"    <loc>{url_for(rel)}</loc>",
                f"    <lastmod>{today}</lastmod>",
                f"    <changefreq>{freq}</changefreq>",
                f"    <priority>{pri}</priority>",
                "  </url>"]
    out.append("</urlset>")
    return "\n".join(out) + "\n", len(pages)


def main():
    want, n = build()
    p = ROOT / "sitemap.xml"
    have = p.read_text() if p.exists() else ""
    # lastmod moves every day; compare everything else.
    strip = lambda t: re.sub(r"<lastmod>[^<]*</lastmod>", "", t)
    if "--check" in sys.argv:
        if strip(have) != strip(want):
            print("sitemap is stale - run `python3 tools/build-sitemap.py`")
            return 1
        print(f"sitemap lists all {n} pages")
        return 0
    p.write_text(want)
    print(f"sitemap.xml: {n} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
