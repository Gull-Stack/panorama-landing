#!/usr/bin/env python3
"""Small copies of every photo, so a page never downloads a 600 KB file to
paint a 300 px tile.

    python3 tools/build-images.py [--check]

Ranee, 2026-10-29: the gallery and amenity tiles "are loading very slowly".
They were: the gallery painted 39 full-size aerials (about 20 MB) as
thumbnails. Every jpg under images/ now gets two copies under images/_r/:

    images/_r/<path>-800.jpg    tiles, cards, gallery thumbnails
    images/_r/<path>-1600.jpg   heroes, the lightbox, one-big-image slots

tools/build-site.py writes them into srcset, so the browser picks the small
one on a phone and the large one on a wide screen. The original stays put
and is never served by a generated page.

Uses macOS `sips`, which every machine that builds this site has.
"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "images"
OUT = SRC / "_r"
WIDTHS = (800, 1600)


def width_of(p):
    out = subprocess.run(["sips", "-g", "pixelWidth", str(p)], capture_output=True, text=True).stdout
    return int(out.strip().split()[-1])


def main():
    check = "--check" in sys.argv
    stale = []
    for src in sorted(SRC.rglob("*.jpg")):
        if OUT in src.parents:
            continue
        rel = src.relative_to(SRC).with_suffix("")
        for w in WIDTHS:
            dst = OUT / f"{rel}-{w}.jpg"
            # --check asks only "is every copy there": a fresh clone stamps
            # every file with checkout time, so mtimes mean nothing in CI.
            if dst.exists() and (check or dst.stat().st_mtime >= src.stat().st_mtime):
                continue
            if check:
                stale.append(str(dst.relative_to(ROOT)))
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            # Never upscale: a 1248 px original gets a 1248 px "1600" copy.
            target = min(w, width_of(src))
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "normal",
                            "--resampleWidth", str(target), str(src), "--out", str(dst)],
                           check=True, capture_output=True)
    if stale:
        print("STALE - run `python3 tools/build-images.py`:", *stale[:10], sep="\n  ")
        return 1
    print("image copies are current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
