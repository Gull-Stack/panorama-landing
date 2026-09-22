#!/usr/bin/env python3
"""Every externally hosted image still resolves.

    python3 tools/check-external-images.py

⛔ tools/check-links.py DELIBERATELY SKIPS THESE. It resolves internal hrefs
against files on disk; an image on somebody else's CDN cannot be checked that
way, so it was excluded and nobody looked again. On 2026-09-21 a render of all
41 pages found `images.unsplash.com/photo-1468186503690` returning 404 on the
live site -- a grey broken-image box on a client page, for an unknown length of
time, that every gate in this repo reported as fine.

⛔ THE REAL FINDING IS THE OTHER 32. This site hotlinks 33 stock photos across
8 pages -- skiing, golf, reservoirs, restaurants. None of them is Panorama, none
is under DAI's control, and any of them can 404 or be swapped by a third party
without warning. One already did. That is a decision for Ranee, not a cleanup to
do quietly: see the note in README.md.
"""
import pathlib, re, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "node_modules", "tools", "data"}
EXT = re.compile(r'<img[^>]+src="(https?://[^"]+)"')


def main():
    used = {}
    for p in ROOT.rglob("*.html"):
        if SKIP & set(p.relative_to(ROOT).parts):
            continue
        for url in EXT.findall(p.read_text()):
            used.setdefault(url, []).append(str(p.relative_to(ROOT)))

    print(f"{len(used)} externally hosted images across "
          f"{len({f for v in used.values() for f in v})} pages")
    dead = []
    for url, files in sorted(used.items()):
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "panorama-linkcheck"})
        try:
            code = urllib.request.urlopen(req, timeout=15).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = str(e)[:40]
        if code != 200:
            dead.append((code, url, files))

    for code, url, files in dead:
        print(f"  DEAD {code}  {url[:78]}")
        for f in files:
            print(f"          on {f}")
    print(f"{len(dead)} dead")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
