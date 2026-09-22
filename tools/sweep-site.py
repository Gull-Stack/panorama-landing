#!/usr/bin/env python3
"""Normalize the nav, the dead lead-gen links, and the no-JS guard, sitewide.

    python3 tools/sweep-site.py           # write, print a census
    python3 tools/sweep-site.py --check   # fail if any page has drifted

⛔ THE NAV IS PASTED INTO FORTY-FIVE FILES and had already drifted; the builder
pages literally shipped the comment "paste this EXACT block; it will be
normalized site-wide later". This is that. tools/panorama_site.py holds the one
copy.

⛔ EVERY LEAD-GEN LINK ON THE SITE POINTED AT #visit -- 110 of them, reading
"Visit Us" (53), "Contact" (32), "Schedule Your Tour" (13), plus private
showings, consultations and lot tours. Ranee, 2026-09-21: "We're not gonna take
tours. We're not gonna schedule tours. We're not gonna do any kind of lead
generation or anything on this... that is not about filling out a contact form.
It's about clicking on the builder links." And on the button specifically:
"Instead of visit us, because we don't have any other contact information to
give them." So #visit is deleted and all 110 become Find Your Home.

⛔ AND THE PAGE PAINTED BLANK WHITE ON REFRESH. Ranee: "Watch when they refresh.
This is just all white. So it looks kind of broken. Then you scroll, now you
see it." Cause: `.reveal { opacity: 0 }` is applied by the stylesheet at parse
time and only removed by an IntersectionObserver in a script at the BOTTOM of a
1,653-line document. Everything below the hero is invisible until that script
runs -- and permanently invisible if it never does. The fix is a one-line head
script that marks the document as scripted, plus `.js`-scoped reveal rules
(css/reveal-guard.css): no script, nothing is ever hidden.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import panorama_site as S

SKIP_DIRS = {".git", "node_modules", "tools", "data"}

GUARD_CSS = S.GUARD_CSS
JS_GUARD = S.JS_GUARD

# ⛔ THE BUTTONS WERE REPOINTED BUT THE SENTENCES STILL ASKED FOR A TOUR.
# Rewriting 110 hrefs left prose that contradicts the button above it -- "
# Schedule a private showing to explore available estate homesites" over a
# button that now reads Find Your Home. Each line below is a deliberate,
# reviewable edit; a regex broad enough to catch these would maul the rest of
# the copy.
#
# ⛔ NOT ON THIS LIST, ON PURPOSE: find-a-home/rentals.html. Its leasing email
# and "tour a townhome" are for DAI's OWN townhomes, not a builder hand-off,
# and Ranee's "we don't have any other contact information to give them" was
# said about the nav button. Deleting a real leasing contact on an inference is
# worse than asking. QUESTION FOR RANEE: does the no-tours rule reach rentals?
PROSE = [
    # villages/*
    ("Village 5 lots are selling quickly. Contact us today to schedule a private lot tour and explore your options.",
     "Village 5 sits at the top of the community, where the lots open onto the widest views Panorama has."),
    ("Village 3 lots are limited and in high demand. Schedule a private showing to explore available estate homesites and meet with our luxury builder partners.",
     "Village 3 is Panorama&rsquo;s estate enclave. See which builders are working here, then go to them directly."),
    ("Photos can&#39;t capture the full majesty of Village 4&#39;s Wasatch views. Schedule a visit to experience them for yourself.",
     "Photos can&rsquo;t capture the full majesty of Village 4&rsquo;s Wasatch views. Come up and stand in them."),
    ("Photos can't capture the full majesty of Village 4's Wasatch views. Schedule a visit to experience them for yourself.",
     "Photos can&rsquo;t capture the full majesty of Village 4&rsquo;s Wasatch views. Come up and stand in them."),
    # areas/*
    ("Love the master-planned concept? See how Panorama elevates it with mountain views and more space. Schedule your tour today.",
     "Love the master-planned concept? See how Panorama elevates it with mountain views and more space."),
    # find-a-home/bring-your-own-builder.html -- lots are no longer ours to sell
    # on this site, and "place a reservation" is the lead capture Ranee cut.
    ("Reserve your lot, then build with the custom builder of your choice.",
     "Bring the custom builder of your choice."),
    ("Tour the available lots, pick the village and view that speaks to you, and place a reservation to hold your homesite while you plan.",
     "Pick the village and the view that speaks to you, then work with DAI on the homesite."),
    ("1. Reserve Your Homesite", "1. Choose Your Homesite"),
    ("The homesites shown above are representative. The live lot list, exact acreages, and current pricing will be confirmed directly with DAI &mdash; contact us for the most up-to-date availability.",
     "The homesites shown above are representative. The live lot list, exact acreages and current pricing are confirmed directly with DAI."),
    ("Explore available lots and reserve yours today.", "Explore the homesites."),
    # ⛔ The section is called Find Your Home now. Breadcrumbs, <title>s and
    # back-links that still say "Find Your Builder" send a visitor looking for
    # a nav item that no longer exists.
    ("Find Your Builder | Panorama Herriman", "Find Your Home | Panorama Herriman"),
    ("Back to Find Your Builder", "Back to Find Your Home"),
    ("/ Find Your Builder</p>", "/ Find Your Home</p>"),
    (">Find Your Builder</a> /", ">Find Your Home</a> /"),
    ("See who&#39;s building in each village over on Find Your Builder.",
     "See every builder at Panorama over on Find Your Home."),
    ("See who's building in each village over on Find Your Builder.",
     "See every builder at Panorama over on Find Your Home."),
    ("<a href=\"../find-a-home/\">Find Your Builder</a> / Toll Brothers",
     "<a href=\"../find-a-home/\">Find Your Home</a> / Toll Brothers"),
    # Amenities is a top-level destination now, not a page inside Lifestyle.
    ("<a href=\"../\">Home</a> / <a href=\"./\">Lifestyle</a> / Amenities",
     "<a href=\"../\">Home</a> / Amenities"),
    # ⛔ "Instead of visit us, because we don't have any other contact
    # information to give them." The words go wherever they appear, not just on
    # the button.
    ("Visit us to see Panorama Park and explore our trail system firsthand.",
     "Panorama Park and the trail system are open &mdash; come up and walk them."),
    ("Schedule a private tour of available homesites in Village 1 and discover why Panorama Herriman is Utah&#39;s most sought-after new community.",
     "Village 1 is where Panorama meets Rosecrest &mdash; the closest homesites to the way in and out."),
    ("Schedule a private tour of available homesites in Village 1 and discover why Panorama Herriman is Utah's most sought-after new community.",
     "Village 1 is where Panorama meets Rosecrest &mdash; the closest homesites to the way in and out."),
    # ⛔ "We're not gonna have any floor plans on the whole thing" reaches the
    # rentals copy too, even though the leasing contact itself is left alone.
    ("Ask about current availability, floor plans, and move-in timing. Our leasing team will help you find the right fit.",
     "Ask about current availability and move-in timing. Our leasing team will help you find the right fit."),
]

NAV_RE = re.compile(r'[ \t]*<nav class="nav"[^>]*>.*?</nav>', re.S)
FOOT_RE = re.compile(r'[ \t]*<footer>.*?</footer>', re.S)
HEAD_RE = re.compile(r"</head>", re.I)
CRUMB_RE = re.compile(r'[ \t]*<p class="breadcrumb">.*?</p>')
EYEBROW_RE = re.compile(r'\n[ \t]*<p class="hero-eyebrow">[^<]*</p>')

# Link text on anything that used to point at the retired #visit anchor.
CTA_TEXT = "Find Your Home"


def depth_of(p: pathlib.Path) -> int:
    return len(p.relative_to(ROOT).parts) - 1


def sweep(p: pathlib.Path):
    t0 = t = p.read_text()
    d = depth_of(p)
    up = "../" * d
    notes = []

    # 1. One nav.
    if NAV_RE.search(t):
        home_hash = p.name == "index.html" and d == 0
        t2 = NAV_RE.sub(lambda _: S.nav_html(d, home_is_hash=home_hash), t, count=1)
        if t2 != t:
            notes.append("nav")
        t = t2

    # 1b. One footer. See FOOTER_LINKS for why this is swept and not hand-fixed.
    if FOOT_RE.search(t):
        t2 = FOOT_RE.sub(lambda _: S.footer_html(d), t, count=1)
        if t2 != t:
            notes.append("footer")
        t = t2

    # 1c. Area pages say they are about the area. See S.AREA_PAGES.
    rp = str(p.relative_to(ROOT))
    eyebrow = f'      <p class="hero-eyebrow">{S.AREA_EYEBROW}</p>\n'
    has = EYEBROW_RE.search(t)
    if rp in S.AREA_PAGES:
        if not has:
            t2 = CRUMB_RE.sub(lambda m: m.group(0) + "\n" + eyebrow.rstrip("\n"), t, count=1)
            if t2 != t:
                notes.append("area-eyebrow")
            t = t2
    elif has:
        # A page that left the area group must not keep the label.
        t = EYEBROW_RE.sub("", t, count=1)
        notes.append("area-eyebrow")

    # 2. Retired pages -> their replacement, so a deleted page leaves no 404.
    # ⛔ A page in the SAME FOLDER links to a sibling with no folder prefix at
    # all ("floorplans.html"), which the folder-qualified keys miss entirely.
    # find-a-home/index.html was the one survivor of the first run, and
    # tools/check-links.py is what caught it.
    for old, new in S.RETIRED.items():
        bare, folder = old.rsplit("/", 1)[-1], old.rsplit("/", 1)[0]
        cands = [up + old, "/" + old, old]
        if str(p.parent.relative_to(ROOT)) == folder:
            cands.append(bare)
        for href in cands:
            if href and f'href="{href}"' in t:
                t = t.replace(f'href="{href}"', f'href="{up + new}"')
                notes.append(f"retired:{bare}")

    # 3. The 110 lead-gen dead-ends. Href AND the words on the button.
    def fix_cta(m):
        inner = m.group(2)
        # Keep a nested <span> ornament out of it -- these are plain labels.
        return f'{m.group(1)}href="{up}find-a-home/"{m.group(3)}>{CTA_TEXT}</a>'

    n_before = t.count("#visit")
    t = re.sub(
        r'(<a\s[^>]*?)href="[^"]*#visit"([^>]*)>(.*?)</a>',
        lambda m: f'{m.group(1)}href="{up}find-a-home/"{m.group(2)}>{CTA_TEXT}</a>',
        t,
        flags=re.S,
    )
    # Any survivor (e.g. a bare href in JS or a form action).
    t = t.replace('action="../#visit"', f'action="{up}find-a-home/"')
    t = t.replace('href="#visit"', f'href="{up}find-a-home/"')
    t = t.replace('href="../#visit"', f'href="{up}find-a-home/"')
    t = t.replace('href="../index.html#visit"', f'href="{up}find-a-home/"')
    n_after = t.count("#visit")
    if n_before != n_after:
        notes.append(f"cta:{n_before - n_after}")

    # 3b. `href="#"` is a link that goes nowhere and looks like one that does.
    # The trail-map PDFs and the run app on the amenities page were all of
    # them. A pending asset is a marker, not an anchor.
    def dead_anchor(m):
        return f'<span class="{m.group(1)}asset-pending-line"><span class="pending-tag">Pending</span> {m.group(2)}</span>'

    t3 = re.sub(r'<a href="#" class="(asset-pending|app-link)"[^>]*>(.*?)</a>',
                lambda m: f'<span class="asset-pending-line"><span class="pending-tag">Pending</span> {m.group(2)}</span>',
                t, flags=re.S)
    if t3 != t:
        notes.append("dead-anchor")
    t = t3

    # 3c. The chrome's stylesheet, on the pages that have no other copy of it.
    # ⛔ ONLY where css/interior.css is absent -- both files define the nav and
    # the footer, and loading both is the duplication this whole pass exists to
    # remove. index.html styles its own nav inline and is excluded for the same
    # reason. See the header of css/chrome.css.
    needs_chrome = (
        "css/interior.css" not in t
        and not (d == 0 and p.name == "index.html")
        and ".nav-item {" not in t
    )
    if needs_chrome and "css/chrome.css" not in t:
        t = t.replace(
            f'<link rel="stylesheet" href="{up}{GUARD_CSS}">',
            f'<link rel="stylesheet" href="{up}css/chrome.css">\n  <link rel="stylesheet" href="{up}{GUARD_CSS}">',
            1,
        )
        notes.append("chrome-css")

    # 4. Prose that still asks for a tour the site no longer offers.
    n = 0
    for a, b in PROSE:
        if a in t:
            t = t.replace(a, b)
            n += 1
    if n:
        notes.append(f"prose:{n}")

    # 5. The no-JS guard, and the stylesheet that makes it mean something.
    if "</head>" in t.lower() and JS_GUARD not in t:
        if GUARD_CSS not in t:
            t = HEAD_RE.sub(
                f'  <link rel="stylesheet" href="{up}{GUARD_CSS}">\n  {JS_GUARD}\n</head>',
                t,
                count=1,
            )
        else:
            t = HEAD_RE.sub(f"  {JS_GUARD}\n</head>", t, count=1)
        notes.append("js-guard")

    return (t != t0), t, notes


def main():
    check = "--check" in sys.argv
    pages = sorted(
        p
        for p in ROOT.rglob("*.html")
        if not (SKIP_DIRS & set(p.relative_to(ROOT).parts))
    )
    changed, census = [], {}
    for p in pages:
        did, new, notes = sweep(p)
        if did:
            changed.append(str(p.relative_to(ROOT)))
            for n in notes:
                census[n.split(":")[0]] = census.get(n.split(":")[0], 0) + 1
            if not check:
                p.write_text(new)

    print(f"{len(pages)} pages scanned")
    for k, v in sorted(census.items()):
        print(f"  {k:12} {v} pages")
    if check:
        if changed:
            print("DRIFTED - run `python3 tools/sweep-site.py`:")
            for c in changed:
                print("   ", c)
            return 1
        print("nav + links are current on every page")
        return 0
    print(f"rewrote {len(changed)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
