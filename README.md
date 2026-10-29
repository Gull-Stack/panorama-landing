# Panorama — panoramaherriman.com

The Panorama community site. Static HTML, no framework, no build step to deploy
— Vercel serves these files as they sit.

> ⛔ The README that was here described a **plastic surgery practice template**.
> It was the scaffold this site was started from and had never been replaced,
> so the only written instructions in the repo were for a different product.

---

## What this site is for

Ranee, 2026-09-21:

> "We're not gonna take tours. We're not gonna schedule tours. We're not gonna
> do any kind of lead generation or anything on this. Because we just don't
> have a budget to spend any time as a marketing department. We're just gonna
> build the landing site, basically, is how I'm viewing it."

> "The whole thing is find your home. And that is not about filling out a
> contact form. It's about clicking on the builder links."

So: **the job of this site is to hand a visitor to a builder.** Everything else
is context. There are no forms, no tour scheduling and no lead capture, and
adding any of them is a decision for Ranee, not a feature.

Three rules that came out of the same call and are enforced in code:

| Rule | Where it is enforced |
|---|---|
| No floor plans, anywhere | `data/builders.json` has no field for them; the pages that listed them are deleted |
| No lot or village assigned to a builder | the village hotspot map is gone; lots appear only on the master plan image at the bottom of Find Your Home |
| No invented copy | every builder field is null until Ranee supplies it, and renders as a visible "Pending" marker naming what is missing |

**How people find it:** a sign on the property. Ranee, asked directly: *"Sign on
the property. Okay, that's my point. And that's it."* A Google Business listing
is blocked — the community has no office, and Google will not verify it. Treat
direct and QR traffic as the whole audience; nothing here should depend on
search.

---

## Changing something

```bash
./tools/build.sh           # regenerate everything, rewrite the files
./tools/build.sh --check   # fail if anything committed is out of date
```

Run it after any edit and commit whatever it changes. Then preview with
`npx serve -l 8765 .` (the Maps key allows localhost:8765).

**Since 2026-10-29 every page is generated.** The served `.html` files start
with a `GENERATED` comment naming their source. Never edit one; the next build
erases it.

| To change | Edit |
|---|---|
| A page's words or photos | `src/pages/<page>.html` (body only, JSON header on line 1) |
| A builder page or tile | `data/builders.json` |
| The header, mega menu, footer, `<head>` | `tools/build-site.py` (`MENU`, `FOOTER`, `page()`) |
| Any style | `css/site.css` (the only stylesheet) |
| Menu, reveal, lightbox | `js/site.js` |
| The nearby map's pins | `js/near-map.js` (name the place in the page copy first) |

### Adding a builder's photos, logo or copy

The fields follow Ranee's builder asset guide one for one:

| Asset guide | Field |
|---|---|
| Intro, 50 words or less | `intro` |
| 2–4 paragraphs on the homes they build here | `homes` (a list of paragraphs) |
| 4–8 differentiators | `differentiators` ("Title – text" splits into bold title + text) |
| Exterior images | `exteriorImages` (the FIRST one is the page's one big image) |
| Their URL + UTM | `url` + `utm` |
| Model homes | `modelHomes` |
| Logo | `logo` (light backgrounds), `logoOnDark` (the navy page header) |

Ranee's builder page spec, 10/29: *"a 50-word intro, a big image, a couple
paragraphs about the homes ... a couple bullet points ... their model homes,
and that's it. And then their link."* No contact block, no carousel, no floor
plans. A builder with no copy gets one "Home details coming soon" note, not a
row of Pending chips.

**⛔ Open question, 2026-09-21.** Every builder except McArthur carries
`"verified": false`. Ranee: *"I don't know if all those other ones are
builders, to be honest."*

### Images

Put the original under `images/`. `tools/build-images.py` writes an 800 px and
a 1600 px copy to `images/_r/`, and every generated `<img>` uses them through
`srcset` with `loading="lazy"`. Ranee, 10/29, on the gallery: "loading very
slowly". It was painting 39 full-size aerials as thumbnails.

### ⛔ Why the page used to flash blank white

Ranee, 9/21: *"The white looks like an error out here because it loads late."*
Hiding for the fade-in is opt-in under `html.js`, and `js/site.js` marks
everything already on screen as revealed before it turns hiding on. Never add
a `.reveal` rule outside `.js`.

---

## Hotlinked stock photos: gone

As of 2026-10-29 no page loads an image from another server
(`tools/check-external-images.py` reports 0). The pages that hotlinked
Unsplash were retired or rebuilt on local files.
