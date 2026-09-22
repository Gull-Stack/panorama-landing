"""One nav, one footer, for forty-five hand-written HTML files.

⛔ THE NAV WAS COPIED INTO EVERY PAGE. Forty of them carried a "Visit Us"
button; twenty-six said "Find Your Builder"; thirty linked a Floor Plans page.
Changing a nav label meant forty-five edits and the site had already drifted --
builder-*.html even shipped the comment "paste this EXACT block; it will be
normalized site-wide later". This module is that normalization. It is the only
place the nav exists, and tools/sweep-nav.py writes it into every page.

⛔ IT STAYS SERVER-RENDERED HTML, NOT A JS INCLUDE. Ranee's headline complaint
on 2026-09-21 was a page that paints blank white until script runs. Moving the
nav into JavaScript would make exactly that worse.

RANEE'S NAV, 2026-09-21, in her words:
  "that find your builder should be find your home. Up the top."
  "That should be the main place that we want people to go."
  "So maybe the find your builder has the outline around it. And, but it still
   has the drop down."  -> the CTA and the dropdown are ONE item, not two.
  "Instead of visit us, because we don't have any other contact information to
   give them."           -> Visit Us is REMOVED, not relabelled.
  "amenities will be its own thing... I just think it should be at top level
   instead of on a dropdown."
  "We're not gonna have any floor plans on the whole thing."
"""

# (label, href, [(sub-label, sub-href), ...] or None, css_class)
NAV = [
    # ⛔ ONE ITEM. Ranee asked for the outline AND the dropdown on the same
    # thing; rendering a "Find Your Home" button beside a "Find Your Home"
    # dropdown would be two doors to one room.
    ("Find Your Home", "find-a-home/", [
        ("Overview", "find-a-home/"),
        ("Panorama Builders", "find-a-home/builders.html"),
        ("Villages", "find-a-home/villages.html"),
        ("Townhomes For Rent", "find-a-home/rentals.html"),
        ("Bring Your Own Builder", "find-a-home/bring-your-own-builder.html"),
    ], "nav-cta nav-cta-drop"),
    # ⛔ TWO GROUPS, NOT ONE. Ranee, 2026-09-21: "Lifestyle, life at Panorama,
    # and amenities are one thing. So that's about our specific Panorama
    # community. The rest is about the area around it, so we need to
    # differentiate more between those two." The old "Lifestyle" dropdown mixed
    # Panorama's own trail system with Herriman's schools and shopping.
    # Community first, then the area. Nothing about Herriman goes in the
    # community group, and nothing Panorama owns goes in the area group.
    ("Life at Panorama", "life-culture/", [
        ("Overview", "life-culture/"),
        ("Panorama Trails", "things-to-do/parks-trails.html"),
        ("Our Story", "life-culture/history.html"),
    ], "nav-link"),
    # Promoted out of the Lifestyle dropdown on Ranee's instruction.
    ("Amenities", "life-culture/amenities.html", None, "nav-link"),
    ("Around Herriman", "things-to-do/", [
        ("Things To Do", "things-to-do/"),
        ("Dining", "things-to-do/dining.html"),
        ("Recreation", "things-to-do/recreation.html"),
        ("Shopping", "things-to-do/shopping.html"),
        ("Schools", "life-culture/schools.html"),
        ("Why Herriman", "life-culture/why-herriman.html"),
    ], "nav-link"),
    # Location stays top level: its page carries Panorama's own master plan
    # AND the nearby destinations, so it belongs to neither group alone.
    ("Location", "maps/", None, "nav-link"),
    ("Gallery", "gallery.html", None, "nav-link"),
]

# Pages that no longer exist. Any link to one is rewritten to its replacement,
# so a deleted page never leaves a 404 behind.
#   floorplans -- "no floor plans on the whole thing"
#   homesites  -- "no specific lots for each builder"
RETIRED = {
    "find-a-home/floorplans.html": "find-a-home/builders.html",
    "find-a-home/homesites.html": "find-a-home/villages.html",
}


def rel(depth: int, href: str) -> str:
    """A root-relative href, rewritten for a page `depth` folders down."""
    if href.startswith(("http", "#", "mailto:", "tel:")):
        return href
    return ("../" * depth) + href


def nav_html(depth: int, home_is_hash: bool = False) -> str:
    up = "../" * depth
    logo_href = "#" if home_is_hash else (up or "/")
    out = [
        '  <nav class="nav" id="nav">',
        f'    <a href="{logo_href}" class="logo">',
        f'      <img src="{up}assets/logo-white.png" alt="Panorama">',
        "    </a>",
        '    <div class="mobile-toggle" onclick="toggleMobileMenu()">',
        "      <span></span><span></span><span></span>",
        "    </div>",
        '    <div class="nav-links" id="navLinks">',
    ]
    for label, href, subs, cls in NAV:
        if subs:
            out.append('      <div class="nav-item">')
            out.append(
                f'        <a href="{rel(depth, href)}" class="{cls}">{label} <span class="arrow">▼</span></a>'
            )
            out.append('        <div class="nav-dropdown">')
            for sl, sh in subs:
                out.append(f'          <a href="{rel(depth, sh)}">{sl}</a>')
            out.append("        </div>")
            out.append("      </div>")
        else:
            out.append(f'      <a href="{rel(depth, href)}" class="{cls}">{label}</a>')
    out += ["    </div>", "  </nav>"]
    return "\n".join(out)


# ⛔ THE FOOTER NEEDED NORMALIZING FOR THE SAME REASON THE NAV DID, and the
# 2026-09-21 CTA sweep proved it: footers already carried a "Find Your Builder"
# link, the sweep added a "Find Your Home" one pointing at the same page, and
# several pages ended up listing both. A footer pasted into forty files cannot
# be rewritten by hand without that happening.
FOOTER_LINKS = [
    ("Find Your Home", "find-a-home/"),
    ("Panorama Builders", "find-a-home/builders.html"),
    ("Life at Panorama", "life-culture/"),
    ("Amenities", "life-culture/amenities.html"),
    ("Around Herriman", "things-to-do/"),
    ("Location", "maps/"),
    ("Gallery", "gallery.html"),
]

# Pages about the AREA, not the community. Each carries the eyebrow below
# above its <h1>, so a visitor who lands from search on "Dining" knows it is
# about Herriman before reading a word of it. tools/sweep-site.py writes it
# and --check fails if one drifts. Same pages as the "Around Herriman" group.
AREA_EYEBROW = "Around Herriman"
AREA_PAGES = [
    "things-to-do/index.html",
    "things-to-do/dining.html",
    "things-to-do/recreation.html",
    "things-to-do/shopping.html",
    "life-culture/schools.html",
    "life-culture/why-herriman.html",
]


def footer_html(depth: int) -> str:
    up = "../" * depth
    links = "\n      ".join(
        f'<a href="{rel(depth, h)}">{l}</a>' for l, h in FOOTER_LINKS
    )
    return f"""  <footer>
    <div class="footer-logo"><img src="{up}assets/logo-white.png" alt="Panorama"></div>
    <p class="footer-tagline">The View Is Better From Here</p>
    <div class="footer-links">
      {links}
    </div>
    <p class="footer-legal">&copy; 2026 Panorama. A DAI Development. All rights reserved.<br>Builder participation, plans, and availability subject to change without notice.</p>
  </footer>"""


GUARD_CSS = "css/reveal-guard.css"

# ⛔ THE `.js` CLASS ALONE DOES NOT FIX WHAT RANEE SAW. It rescues a visitor
# with no JavaScript; she has JavaScript. Her blank white slab came from WHEN
# the observer runs -- at the bottom of a 1,653-line document, so everything
# above the fold sits at opacity 0 through the whole parse. This script runs in
# <head> and starts observing each element AS IT IS PARSED, via a
# MutationObserver, so an element already on screen activates in the next frame
# instead of after the entire page has been read.
#
# ⛔ It also fails open twice over: no IntersectionObserver, no MutationObserver,
# or a throw anywhere in here, and `.js` comes back off -- which, per
# css/reveal-guard.css, means nothing is hidden at all. An animation is never
# allowed to be the reason a word is missing.
#
# ⛔ It is INLINE on purpose. An external <script src> in <head> is a blocking
# round-trip before first paint, and a deferred one runs too late to help --
# which is the entire defect.
JS_GUARD = """<script>/* reveal guard - see css/reveal-guard.css */
(function(){var h=document.documentElement;h.classList.add('js');
try{if(!window.IntersectionObserver||!window.MutationObserver){h.classList.remove('js');return;}
var sel='.reveal,.reveal-left,.reveal-right,.scale-in,.reveal-stagger';
var io=new IntersectionObserver(function(es){for(var i=0;i<es.length;i++){if(es[i].isIntersecting){es[i].target.classList.add('active');io.unobserve(es[i].target);}}},{threshold:0.15,rootMargin:'0px 0px -50px 0px'});
var scan=function(){var n=document.querySelectorAll(sel);for(var i=0;i<n.length;i++){if(!n[i].hasAttribute('data-rv')){n[i].setAttribute('data-rv','');io.observe(n[i]);}}};
var mo=new MutationObserver(scan);mo.observe(h,{childList:true,subtree:true});
document.addEventListener('DOMContentLoaded',function(){scan();mo.disconnect();});
}catch(e){h.classList.remove('js');}})();</script>"""


def head_guard(depth: int) -> str:
    """The stylesheet link + the head script, for a page `depth` folders down."""
    up = "../" * depth
    return f'  <link rel="stylesheet" href="{up}{GUARD_CSS}">\n  {JS_GUARD}'
