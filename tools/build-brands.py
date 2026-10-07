#!/usr/bin/env python3
"""The brand lists on Around Herriman, ordered by Google rating.

    python3 tools/build-brands.py           # write the lists from data/brands.json
    python3 tools/build-brands.py --check   # fail if the page is stale (CI)
    GOOGLE_PLACES_KEY=... python3 tools/build-brands.py --fetch   # refresh ratings, then write

Ranee, 2026-10-06 call: "We should sort in the Mountain View Village the brand
names that are organized by those that have the highest Google rating first
so that they're actually suggesting popular names, not mediumly interesting
restaurants."

⛔ THE RATING IS NEVER TYPED BY HAND. Every number in data/brands.json came
from Google Places (searchText, one result, the brand name plus the center),
and the file records the day it was fetched. The page shows the ORDER and the
fetch month; it does not print the numbers, so nothing on the page can go
stale as a figure.

⛔ A WRONG MATCH SORTS LAST, NOT FIRST. Places answered "Salt & Straw,
Mountain View Village" with the shopping center itself (4.6, 1,569 reviews).
A match whose returned name shares no word with the brand is retried with the
city alone; if that fails too it keeps rating null and goes to the end. A
place with under MIN_REVIEWS reviews also goes to the end: a 4.5 from four
reviews is not "popular".

The key is NOT in the repo. It is the GOOGLE_PLACES_KEY environment variable
(macOS Keychain item `panorama-places-key` on Josh's machine).
"""
import json, os, pathlib, re, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "brands.json"
PAGE = ROOT / "things-to-do" / "index.html"
MIN_REVIEWS = 25
STOP = {"the", "and", "&", "of", "at", "grill", "restaurant", "cafe", "co", "company", "inc"}


def tokens(s):
    return {t for t in re.findall(r"[a-z0-9']+", (s or "").lower()) if t not in STOP}


def good_match(brand, matched):
    return bool(tokens(brand) & tokens(matched))


def places(key, q):
    req = urllib.request.Request(
        "https://places.googleapis.com/v1/places:searchText",
        data=json.dumps({"textQuery": q, "maxResultCount": 1}).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": key,
            "X-Goog-FieldMask": "places.displayName,places.rating,places.userRatingCount,places.formattedAddress",
        },
    )
    r = json.load(urllib.request.urlopen(req, timeout=20))
    p = (r.get("places") or [{}])[0]
    return {
        "matched": (p.get("displayName") or {}).get("text"),
        "address": p.get("formattedAddress"),
        "rating": p.get("rating"),
        "count": p.get("userRatingCount"),
    }


def fetch(d):
    key = os.environ.get("GOOGLE_PLACES_KEY")
    if not key:
        raise SystemExit("--fetch needs GOOGLE_PLACES_KEY in the environment")
    for c in d["centers"].values():
        for rows in c["lists"].values():
            for row in rows:
                b = row["brand"]
                hit = places(key, f"{b}, {c['name']}, {c['city']}")
                if not good_match(b, hit["matched"]):
                    hit = places(key, f"{b}, {c['city']}")
                    hit["fallbackQuery"] = True
                if not good_match(b, hit["matched"]):
                    hit = {"matched": hit["matched"], "address": hit["address"], "rating": None, "count": None, "unmatched": True}
                row.update(hit)
                time.sleep(0.15)
    d["fetchedAt"] = time.strftime("%Y-%m-%d", time.gmtime())
    DATA.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def order(rows):
    def key(r):
        rating, count = r.get("rating"), r.get("count") or 0
        trusted = rating is not None and count >= MIN_REVIEWS
        return (0 if trusted else 1, -(rating or 0), -count, r["brand"])
    return sorted(rows, key=key)


def esc(s):
    return s.replace("&", "&amp;").replace("'", "&rsquo;")


def render(rows, fetched):
    month = time.strftime("%B %Y", time.strptime(fetched, "%Y-%m-%d"))
    lis = "\n".join(f"            <li>{esc(r['brand'])}</li>" for r in order(rows))
    return f'<ul class="brand-list">\n{lis}\n          </ul>\n          <p class="brand-note">Ordered by Google rating, {month}.</p>'


def main():
    check = "--check" in sys.argv
    d = json.loads(DATA.read_text())
    if "--fetch" in sys.argv:
        fetch(d)
    t = PAGE.read_text()
    new = t
    for cid, c in d["centers"].items():
        for cat, rows in c["lists"].items():
            a, z = f"<!-- BRANDS:{cid}:{cat}:START -->", f"<!-- BRANDS:{cid}:{cat}:END -->"
            if a not in new or z not in new:
                raise SystemExit(f"things-to-do/index.html has no {a} .. {z} markers")
            head, rest = new.split(a, 1)
            _, tail = rest.split(z, 1)
            new = head + a + "\n          " + render(rows, d["fetchedAt"]) + "\n          " + z + tail
    if new != t:
        if check:
            print("STALE - run `python3 tools/build-brands.py`: things-to-do/index.html")
            return 1
        PAGE.write_text(new)
        print("wrote brand lists into things-to-do/index.html")
    else:
        print(f"brand lists are current (ratings fetched {d['fetchedAt']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
