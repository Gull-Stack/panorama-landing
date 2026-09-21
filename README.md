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

Run it after any edit and commit whatever it changes.

### Adding a builder's photos, logo or copy

**Edit `data/builders.json`. Never edit `find-a-home/builder-*.html`** — those
files are generated and your edit is erased on the next build.

The fields are Ranee's builder asset guide, one for one:

| Asset guide | Field |
|---|---|
| 1–5 exterior images, horizontal | `exteriorImages` |
| 1–5 interior images | `interiorImages` |
| Intro, 50 words or less | `intro` |
| 2–4 paragraphs, ~150 words, on the homes they build here | `homes` (a list of paragraphs) |
| 4–8 builder differentiators | `differentiators` |
| Their URL, with whatever UTM they want | `url` + `utm` |
| Model home addresses | `modelHomes` |
| The whole logo | `logo` |

Anything left `null` or `[]` renders as a **Pending** marker that names what is
missing. That is deliberate: the pages this replaced carried three floor plans
per builder — *"The Vista, 4 Beds, 3.5 Baths, Up to 3,600 sq ft"* — that no
builder ever supplied. A gap has to look like a gap.

```bash
# put the files in images/builders/<slug>/, then:
$EDITOR data/builders.json
./tools/build.sh
```

### Adding or removing a builder

Add an object to `builders` in the same file and run the build. It appears on
the home page, on Panorama Builders, on Find Your Home, in the sitemap, and gets
its own page. Removing one is deleting the object — but delete its generated
`find-a-home/builder-<slug>.html` too.

**⛔ Open question, 2026-09-21.** Ranee: *"I don't know if all those other ones
are builders, to be honest."* Every builder except Candlelight was already live
before that call and none is confirmed against an agreement. They are all
carrying `"verified": false`. Flip each to `true` as it is confirmed, and delete
the ones that turn out not to be builders.

### Changing the nav, the footer, or a link everywhere

`tools/panorama_site.py` holds the **one** copy of the nav and the footer.
Change it there and run the build; all 41 pages are rewritten. Do not edit a
`<nav>` or `<footer>` in a page — the next build overwrites it.

### Swapping the master plan or a map

Replace the image file and delete the `pending-note` next to it in the same
commit. A pending note that outlives its gap is worse than no note.

---

## The tools

| | |
|---|---|
| `tools/build.sh` | runs all of the below, in dependency order |
| `tools/build-builders.py` | `data/builders.json` → builder pages + every builder grid |
| `tools/sweep-site.py` | one nav, one footer, no dead links, the no-JS guard, on every page |
| `tools/build-sitemap.py` | `sitemap.xml` from the pages that exist |
| `tools/check-links.py` | every internal href resolves to a real file |
| `tools/panorama_site.py` | the nav, the footer, the retired-page redirects, the head guard |

`--check` on any of them fails instead of writing, which is what CI should run.

---

## ⛔ Why the page used to flash blank white

Ranee, watching it reload: *"The white looks like an error out here because it
loads late. Watch when they refresh. This is just all white. So it looks kind of
broken. Then you scroll, now you see it."*

`.reveal { opacity: 0 }` was applied by the stylesheet the moment the markup
parsed, and only lifted by an IntersectionObserver in a `<script>` at the
**bottom** of a 1,653-line document. Everything below the hero was invisible
until that script ran — and invisible **forever** if it never did.

Two fixes, both in `css/reveal-guard.css` and the head script that
`tools/sweep-site.py` writes into every page:

1. **Hiding is opt-in.** A one-line head script adds `.js` to `<html>`; the
   hidden state only applies under `.js`. No script, no hiding — the words are
   simply there.
2. **The observer starts during parse, not after it.** A `MutationObserver`
   hands each element to the `IntersectionObserver` as it is parsed, so anything
   already on screen reveals in the next frame instead of after the whole page
   has been read.

⛔ Never add a `.reveal` rule that is not scoped under `.js`, and never move
that script out of `<head>` or behind `defer`. Either one brings the white page
back.
