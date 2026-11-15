# Panorama: client notes

Durable facts. Newest first within each section.

## Who

- Toll Brothers contact: Alex Marks, Marketing Director, amarks@tollbrothers.com.
  Sales: Panorama@tollbrothers.com, 385-238-1805. Photo collection (public):
  tb-p-001-public.stylelabs.cloud/collections/6581e039a71e4db685d8d4786d88e7.
- Ranee, 11/12: amenities "will not be built for a year or more". Use "Coming
  2028!" (Dog Park, Panorama Frames, Trail System: "Coming 2027"). The date
  will change and amenities open at different times.
- Ranee, 11/12: the site shows no pricing, floor plans or leasing and move-in
  details for Panorama Townhomes.
- Ranee, 11/12: builders are Fieldstone, McArthur, Toll Brothers, Sego, Jcraft
  and Elevation. 11/13 she sent a Candlelight logo for "the Candlelight Homes
  page", with page information to follow.
- **Ranee Stam**, DAI Director of Marketing, ranee@daiutah.com, direct
  801.495.3416, main 801.495.3414. Asks for and approves everything here.
- McArthur Homes contact: Paige Giles, Online Sales Counselor,
  osc@mcarthurhomes.com, (801) 760-5760. Assets live in their Drive folder
  `1j9dn5H6sbO2qINTU_sbyCHAGbVL8Uzg6` ("McArthur Panorama Assets"): Logo/,
  Photos/, Model Home Info, Builder Marketing Copy (added 10/14).

## Decisions (Ranee, 10/30 email)

- Live domain: **panoramautah.com**. DNS is at GoDaddy (DAI's); records
  `A @ 76.76.21.21`, `CNAME www cname.vercel-dns.com`. Already added to Vercel.
- BYOB contact: **info@panoramautah.com** only. "Take off the phone number."
- Design guidelines go on the site as a download marked "Subject to change".
  She will make a cover image for it. The PDF itself says "Village 8".
- Sego is a confirmed builder (sent assets; zip never arrived). Other builders
  besides McArthur and Sego are still unconfirmed.
- Ranee attaches files that don't arrive (10/29 site plan, 10/30 site plan +
  Sego zip). Check attachments every time; ask for a Drive link.

## Decisions (Ranee, 10/29 review call)

- No builder villages and no "who builds where" anywhere. Builders may buy
  more lots and should describe themselves.
- No contact on the site except Bring Your Own Builder ("email or call").
  Everywhere else the action is "visit their website".
- Builder pages: 50-word intro, one big image, a couple of paragraphs, bullets,
  model homes, their link (the link they send, UTM if any). No floor plans.
- Townhomes for rent are **Panorama Townhomes**, not DAI. Everything about them
  says "coming soon" until leasing opens; then link to the real site.
- Design guidelines: builders in BYOB must follow them (upgraded landscaping,
  fencing, decking). Ranee is fine with a page, a download, or email-gated;
  "we just want them to be able to have access to the raw file."
- Playground equipment colors are changing; current renderings are interim.
- Josh, on the call: they want pickleball courts at Panorama eventually (PPA
  sponsorship joke). Not on the site.

## Gotchas

- The 10/29 call transcript is garbled: "Siego" is probably Sego Homes;
  "PanoramaHerman.com" is panoramaherriman.com (her leasing reference).
- The canonical host is still panorama-landing-chi.vercel.app (`SITE` in
  `tools/build-site.py`, `BASE` in `tools/build-sitemap.py`). Change both at
  the domain cutover.
