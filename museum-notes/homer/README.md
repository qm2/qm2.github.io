# 光与空气之间｜温斯洛·霍默的水彩世界

`/museum-notes/homer/` is a personal, photograph-led exhibition notebook. It is linked directly from the Museum Notes home as American painting, not added to European painting counts.

## Source and build

- Input: `/home/qingxi/museum/homer-handoff/Winslow_Homer_Codex_Package/`, from the user's supplied ZIP.
- `data/works.json`: 67 canonical work/group records, bilingual titles, verified label metadata, authorship, captions, 33 selections, chapter introductions and separate detail-page paragraphs. One record contains two separately attributed paper works in one frame; 67 is a record count, not an assertion of 67 autograph Homer works.
- `data/photos.json`: all 215 inputs, original filename, retained path and SHA-256. `data/originals/` retains each supplied JPEG unchanged, including alternate views, labels and exhibition context. Only selected photographs appear in the reading experience.
- `data/editorial.json`: editable first-person introduction, comparisons, gallery/material selection and sources. The introduction only uses the user's stated interests and repeated visits; it adds no specific travel or first-visit date.
- `data/sections.json`: seven editorial chapters; these are not presented as the museum's official seven sections.
- `data/editorial_shortlist.json`, `locations.json`, and the three Chinese handoff documents preserve the selection/geographic plan. The canonical reviewed fields are in `works.json`.
- `data/map.json`: nine regional groups, associated works and chapter destinations. No hypothetical exact artwork coordinates. `ne_110m_land.geojson`: Natural Earth public-domain land, downloaded from https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson on 2026-11-01. The two local SVG views have no online tile/runtime dependency.
- `images/`: 480/960/1600-width WebP derivatives, capped at native image width, never cropped or upscaled. Most supplied photos are about 1700 pixels; the site does not claim larger original resolution. `data/derivatives.json` records actual dimensions.

Run from the website root:

```sh
python3 scripts/build_museum.py
python3 scripts/check_homer.py
python3 scripts/check_xiangtangshan.py
```

The main builder calls `build_homer.py`. A focused rebuild is `python3 scripts/build_homer.py`. Pillow is already used by the project; there is no new browser library. Shared `museum.css`, Caravaggio's existing lightbox CSS/JS and the notebook header/footer are reused; `homer.css` and `homer.js` scope the new reading layout, offline map and archive filter to this unit.

## Label review, 2026-11-01

All 67 paired label photographs were visually read, and all 215 photos inspected through numbered contact sheets. The 30 selected complete views were also checked against the supplied preview. Preferred full-work close photographs are used without cropping; `detail_206.jpg` replaces the more distant framed `Driftwood` view as display photo. Numbered images 179, 181–183, 185, 187, 189, 191, 193, 195, 197, 199, 202, 204, 207, 209, 211, 213, 215 are explicitly captioned as details where used. Each work displays at most three detail views.

Corrections from photographed labels, preserved in each record's `review_note`:

- 136 / label137, *Clamming*: **1887**, not 1879.
- 151 / label152, *Fisherwomen*: **1881–82**, not 1882–83.
- 154 / label155, *Fox Hill, Bahamas*: **1885**, not 1899. The woman stands by a gate; the second head appears behind the wall. No invented infant/walking scene.
- 157 / label158, *Hunter in the Everglades*: **c.1886**, not 1904.
- 171 / label172, *Bridlington Quay*: **1883**, not 1881.
- 97 / label98: left, Homer, *Preparatory Drawing for Oil Painting “On Guard”*, c.1864, 97.886; right, **John Parker Davis after Homer**, *Watching the Crows*, 1868, 38.843. The supplied slug with `cows` is retained as a stable intake identifier only; the published title says **Crows**.
- 99 / label100 and 107 / label108: **unidentified artists after Homer**, not autograph Homer drawings.
- 173 / label174: *Customs House*, not *Custom House*.

All collection institutions were read from labels. *Watching the Harbor* and *Customs House* remain private collection; *The Shepherdess* belongs to Tina and Joe Pyne; *Sheep and Cattle* to the Sarofim Foundation; *Eight Bells* and *The Guide* to MFAH. Remaining records list MFA Boston. No owner is inferred from the exhibition's title.

MFAH's current exhibition page and July 2026 announcement confirm November 1, 2026–February 7, 2027. The current MFA Boston exhibition page was read for context, not used for Houston dates or as an image source. Published analysis paraphrases photographed labels and describes visible details; it does not claim access to the exhibition catalogue. Innu is used for the community, while the historical English work title is retained. *Driftwood*'s possible autobiographical reading remains attributed to the exhibition interpretation. No claim of precise painting locations, prices or rarity ranking is added.

## Checks and further additions

`check_homer.py` checks original hashes, photo/work/label folders, 33=12+21 selection counts and seven featured plates, text lengths, documented date/authorship corrections, all 68 generated pages, local links/fragments, absence of remote artwork images and non-upscaled derivatives. Browser checks at 1440 and 390 pixels (light/dark) cover layout, captions, both geographic views, keyboard links/disclosures, search/media/decade filters, lightbox next/zoom/close/Escape and no-JavaScript fallback. Browser screenshots stay outside the repository.

For a future photo, retain its bytes under the corresponding `data/originals/works/<slug>/`, append a new unused number and checksum in `photos.json`, and update `display_photo` or `detail_photos` in the existing work record. For a new work, add a new canonical record and its label, keeping uncertain attribution explicit. Review selection and count assertions when the deliberate 67/33 scope changes; regenerate rather than hand-editing HTML. First-person paragraphs can be revised in `editorial.json` without changing factual records.

Remaining limits: unspecified artists of two wood engravings remain unidentified by the label; exact creation locations of broadly regional works are not established; Chinese titles are reading translations alongside original English, not a claimed standardized Chinese catalogue. Historical materials are photographed exhibits, not evidence that the displayed paint box was Homer's own.

## Editorial refinement, 2026-11-01

- The first 30 selections remain; added photo95 (1862 reconnaissance drawing), photo78 (Santiago street corner) and photo159 (Bermuda rocky shore). Chapter order is explicit in `sections.json`; *Watching the Harbor* closes the prologue in 1873, and *Eight Bells* joins the final marine chapter. Existing work/region/section fragments remain valid.
- Hero: untrimmed photo179, labelled as a detail. *The Blue Boat* in its chapter, detail page and comparisons uses photo11 (`main.jpg`), keeping the complete photographed composition. Neither original is edited.
- Seven featured plates have larger figures; supporting works have concise `home_note` copy. Existing `paragraphs` retain close reading on detail pages. First-person interests remain in the introduction, not repeated in the woods chapter.
- Compact map buttons select a single region; existing region IDs, links and native details fallback remain. English place names appear with the selected region. All artwork thumbnails use the author's photographs.
- Four technique examples use photo215 and three explicitly labelled crops: photo46 (flowers), photo180 (mayfly and lower-left scraped area), photo190 (lower right sail). `editorial.json` stores normalized crop boxes; `derivatives.json` stores pixel boxes and source paths. The crop masters are lossless WebP at native resolution, with no colour changes, retouching or enlargement. Every original JPEG and label retains its original checksum. Crops illustrate the explanations in photographed labels10,47,4,77 respectively, reread for this revision.
- Material-case photographs and gallery views remain in optional disclosures. Captions and sources are preserved while repeated authorship/metadata wording is reduced on the chapter page.
- Targeted build only: `python3 scripts/build_homer.py`. Museum-home count changed to 33 in its generator and generated file; no other topic is rebuilt or redesigned. Browser validation covers 1440px and 390px, light/dark, nine map choices and bookmarked fragments, filters, all four technique figures, original/full-view distinction and lightbox controls.

The cover is intentionally a photographed detail; the full composition is one click away in its work page. *Watching the Harbor* and the sail crop have the resolution of the existing photographs, not newly supplied macro photographs. Their use and the first-person introduction remain natural points for the author to review.
