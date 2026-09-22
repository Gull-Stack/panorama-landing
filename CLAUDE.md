# Panorama landing (DAI)

Static site for Panorama, DAI's master-planned community in Herriman. Live at
panorama-landing-chi.vercel.app. See README.md for the builder data flow.

Run `./tools/build.sh --check` before every push. It regenerates nothing and
fails if anything is stale or broken.

## Session Log

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
