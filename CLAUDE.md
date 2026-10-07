# Panorama landing (DAI)

Static site for Panorama, DAI's master-planned community in Herriman. Live at
panorama-landing-chi.vercel.app. See README.md for the builder data flow.

Run `./tools/build.sh --check` before every push. It regenerates nothing and
fails if anything is stale or broken.

## Session Log

### 2026-10-06 — Ranee's weekly call: every tile is its subject, the map has pins, her videos are the heroes

- Ranee's asks from the 10/6 call (Josh's transcript) and her 10/6 emails:
  tile images must depict their subject and never repeat; "Close to a Lot"
  becomes an actual map with dropped pins for dining, recreation, shopping,
  schools, parks and trails; Mountain View Village and The District as equal
  tiles, brands in two columns, bigger type; Golf stops floating; stronger
  hover contrast on every tile; her new header video replaces the home
  images; her amenity video is the Life at Panorama hero; her REV master plan.
- **Home hero** is `videos/home-hero.mp4` (her Panorama-Development_2.mp4,
  54 s, encoded 720p/1000k, 4.8 MB) with a poster from its first frame. The
  six rotating aerials are gone from the markup.
- **Life at Panorama hero** is `videos/life-hero.mp4` (her Playgrounds video,
  69 s, 6.9 MB). `flyover1.mp4` and `fun.mp4` (stock, 25 MB) are deleted.
- **Amenity tiles** (`grid-4`, two rows of four): Tot Lot, Gathering
  Pavilions, Pocket Parks and the Panorama Park section image are stills from
  her park video (`images/amenities/*.jpg`). Skate, Zip, Dog Park keep their
  photos. Panorama Frames and Trail System have NO render and show a navy
  `.render-pending` tile that says so. The couple-on-red-rocks photo that sat
  on two tiles is off the page. No image appears twice on the page.
- **Nearby map** (`js/near-map.js`, Leaflet 1.9.4 from unpkg, OSM tiles,
  no key): 23 pins, every one a place already named in the page copy, with
  coordinates from OSM's geocoder on 10/6 and the page's own drive times.
  Legend chips toggle a category; each popup links to Google Maps. Used on
  Around Herriman ("Close to a Lot") and Life at Panorama ("The
  Neighborhood"). ⛔ CARTO's free tiles stamp "API KEY REQUIRED" now.
  ⛔ Ranee said "an actual Google map"; that needs a Maps Platform key on the
  GullStack GCP project (`gcloud auth login` had expired this session). One
  `L.tileLayer` line to swap.
- **Brand cards** (`.brand-card`, `.brand-list` in two columns, Cormorant):
  dining and shopping each show Mountain View Village and The District at
  the same size. Names come from mountainviewvillage.com's directory and the
  District listing on mallsinamerica.com, October 2026, and the card says so.
  ⛔ Ranee asked for brands sorted by Google rating. That is a Places API
  call (same key as above); today they are ordered by national recognition,
  which is a judgement, not a rating. Nothing claims a rating.
- **Golf** is a `grid-2` block with its own photo; **Skiing** has a ski photo
  instead of a repeat of the home aerial; **Why Herriman** shows Butterfield
  Canyon (CC BY 2.0, credited in a `.photo-credit`). Golf and skiing photos
  are CC0 from Wikimedia Commons. Around Herriman's hero is `aerial-16`,
  which no other page used.
- **Hover** on `.card`, `.card-light`, `.feature-box`, `.builder-logo-link`:
  lift, gold border, deeper shadow.
- **Builder tiles on Find Your Home sit on a light section**; the rules
  assumed navy glass, so names painted white on white and the product line
  fell to browser blue. `.section-light .builder-logo-link` fixes it.
- **McArthur Homes is builder #8** (`data/builders.json`), from the Drive
  folder Ranee forwarded 10/6: navy SVG logo for white tiles, white stacked
  PNG for the navy hero (new `logoOnDark` field, `build-builders.py`),
  3 exterior + 5 interior photos, two model homes on Panorama Park Dr with
  2027 opening estimates. Intro, homes copy and differentiators are still
  null and render as Pending. Their "open for sale December or January"
  line has no field and is not on the page.
- **Master plan** is her 10/6 `_REV` PNG, rendered on white; caption says
  revised 10/6/2026. The empty "Five Distinctive Villages" heading on Find
  Your Home is gone.
- Not done, on purpose: the password gate and the panoramautah.com cutover
  Josh described on the call. Gating the vercel.app host now would lock out
  the builders Ranee already sent it to; it goes on the new host at cutover.
- `./tools/build.sh --check` green: 8 builders, 33 pages, 0 broken links,
  0 unreachable classes, 0 emoji. Rendered home, Life, Around Herriman, Find
  Your Home and the McArthur page at 1280 and 390 before the PR.

### 2026-09-22 (b) — Nav splits the community from the area; /tools/ no longer public

- Ranee, 21 Sept: "Lifestyle, life at Panorama, and amenities are one thing
  ... The rest is about the area around it, so we need to differentiate more."
- The "Lifestyle" dropdown is gone. Two groups now: **Life at Panorama**
  (Overview, Panorama Trails, Our Story) and **Around Herriman** (Things To
  Do, Dining, Recreation, Shopping, Schools, Why Herriman). Amenities, Location
  and Gallery stay top level. Location stays out of both groups because its
  page carries Panorama's master plan AND nearby destinations.
- The six area pages carry an "Around Herriman" eyebrow above the h1.
  `AREA_PAGES` in `tools/panorama_site.py`; `sweep-site.py` writes it and
  `--check` fails on a missing one or a stray one. Both planted, both red.
- Footer follows the same split.
- `.vercelignore` keeps `tools/` out of the deploy (it served the Python
  scripts, 200). No build runs on Vercel, so nothing there needs them.
- `./tools/build.sh --check` green. Rendered 6 pages at 1440 and 390, no
  sideways scroll, dropdown and mobile menu checked.
- Not touched: README.md, STORYBRAND.md and this file are still served too.

### 2026-09-22 — Every emoji icon is now a gold outline SVG

- Ranee on the 21 Sept call: "make them all gold and just an outline. I don't
  want any of those types of icons anywhere." We make the icons; she does not.
- 116 emoji and check-mark glyphs across 21 pages are now inline
  `<svg class="pi">`. Four CSS `content: "✓"` bullets are a masked gold check.
  One family: 24 viewBox, stroke 1.5, no fill.
- `svg.pi` lives in `css/interior.css` and `css/chrome.css`. Stroke is
  `var(--gold)`.
- Gold-filled icon frames (`.lifestyle-icon`, `.feature-icon`,
  `.luxury-feature-icon`) are outlines now. A gold fill hid a gold stroke.
- Removed the "Custom icons pending, coming from Ranee" line on Amenities.
- New gate `tools/check-icons.py` in `build.sh`. It scans page markup and CSS
  `content:` rules, including numeric entities like `&#127969;`. Comments,
  `<style>` and `<script>` bodies are skipped, so the ⛔ notes stay.
- Rendered 22 pages at 1440 and 390. Every icon is gold, stroked, no sideways
  scroll.
- Open: `check-external-images.py` runs with `|| true` in `build.sh`, so a dead
  hotlink never fails the build. 32 Unsplash images still wait on Ranee.
