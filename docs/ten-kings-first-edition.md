# Ten Kings — first edition, 2026-11-17

Published route: `/museum-notes/ten-kings/`.

The user explicitly authorized the first edition to be committed, pushed and deployed,
overriding the handoff's default local-only instruction. The handoff's restrictions on
publishing raw archives and uploading photographs to external services remain respected:
no R2 uploads were made for this topic. Only selected local WebP derivatives are published.

## Sources of truth

- `museum-notes/ten-kings/data/works.json`: 18 paintings plus six supporting object groups;
  stable IDs, separate ownership and the shared CMA viewing record, label/photo mappings,
  edited reading sections, references and uncertainties.
- `data/photos.json`: 81 unique source photographs, explicit captions in work sections,
  source filenames/hashes, selected derivative provenance, dimensions, rotations and srcsets.
  Responsive hero crop shares source photograph 002 and is not a new photograph or object.
- `data/editorial.json`: personal preface derived from the user's supplied draft, home
  sequence, overview, collection timeline and the attribution discussion.
- `data/sources.json`: actual reading status for 13 online references. Unread books are
  explicitly separate. No third-party pictures or infrared images were imported.
- `data/visits.json`: November 13–14, 2026, as explicitly supplied by the user, not inferred
  from filenames. Individual photographs are not assigned guessed visit days.

All 458 JPEG originals have been verified against the supplied SHA256 manifest. They,
the full CSV, thumbnails and contact sheets remain in the private extracted package:
`/home/qingxi/museum/ten-kings-handoff/十王与救赎_Codex完整素材包`.
Do not copy that directory into the public site.

## Build and check

```
python3 scripts/build_museum.py
python3 scripts/check_ten_kings.py
python3 scripts/check_sama_batch.py
```

The full site build calls `build_ten_kings.py` last. It regenerates 16 topic pages,
the home entrance, and small related links from Japanese Zen and Xuzhou. Normal builds
need no private package, network access or credentials. Image regeneration is optional:

```
python3 scripts/prepare_ten_kings_images.py /path/to/extracted/package
```

Add a new reading or photograph in structured data first. Keep painting identity separate
from details and repeat visits. Prefer short published sections over handoff instructions.
No new work is inferred from a close-up, a label, or an exhibition installation photo.

## First-edition verification

- Full site generator passed. Its final diff is limited to the new topic and intended entrances.
- Topic check passed: all 16 page paths/anchors, 24 records, full/label mappings, selected
  image dimensions and actual filename widths, no raw JPEG/CSV/contact-sheet publication.
- Existing SAMA check passed (30 works / 87 photographs / 239 pages and related links).
- Actual Chromium preview at 1440, 768 and 360 px: all 16 pages loaded without JS errors,
  missing resources or horizontal overflow. Full figures retain their aspect ratio.
- Figure/caption edges and spacing checked. Fifth/eighth/tenth king and central Ksitigarbha
  close readings inspected; zoom, arrows, Escape, label expansion, detail deep links,
  gallery navigation and no-JS links tested. Screenshots remain outside the repository in
  `/tmp/ten-kings-review/`.
- Hero `sizes` explicitly describes its 1200 px desktop width; mobile uses uncropped
  installation image. Responsive artwork images are lazy-loaded except the page's main image.

## Editorial corrections and remaining questions

- King 3's label omits gold in its material; retained ink/color rather than applying one
  generic materials field to all ten. Group origin/date follows the photographed CMA labels.
- The dispute note distinguishes CMA's Goryeo attribution, the NMK response and records
  reported as undecided, and Jeong Woo-taek's objections as reported in the press. Neither
  the disputed monograph nor technical reports have been read; no final verdict is claimed.
- The Princeton page now records Korean/Goryeo without a precise date. The 14th-century
  dating and IR repair hypothesis are specifically attributed to the exhibition label.
- Met 30.76.298: ca. 13th century online versus late 14th century on the CMA label; both kept.
- S1992.11 is credited to the National Museum of Asian Art, not loosely called Freer.
- Three Leeum paintings and the urn have no accession number on their photographed labels.
- CMA 2025.141, CMA 2019.224 and NMAA S1992.11 remain distinct records. The CMA–Met possible
  workshop relationship is not the same as a historical relationship to the Ten Kings group.
- No original temple, confirmed original hanging scheme, or identity for “青龍公” is invented.
- Six supporting entries were manually checked against labels (292, 314, 326, 367, 393, 417).
  The two paired entries are groups, not a claim that the site contains only six physical objects.
- Current CMA photography policy was read. It does not supply a blanket CC0 license for
  loan works. This personal noncommercial notebook uses only the user's own photographs,
  and does not represent them as official open-access museum images.

For the next revision, prioritize the user's prose and photo choices, the other seven
paintings' depth, and direct access to the attribution/technical literature. The remaining
original photographs stay available for later study without becoming unreviewed public records.

## Follow-up completed: Leeum National Treasure 218

Added a comparison within the central Ksitigarbha reading, with a home entry and
stable anchor `ksitigarbha/#leeum-amitabha-national-treasure-218`.
`data/comparisons.json` keeps this Washington-original / Cleveland-digital record
separate from the 24 CMA exhibition records. The date of the Washington visit is
unknown; the exhibition's dates are not used as a visit date.

The user clarified that the attached red-robed Buddha painting is the lower label's
Buddha Amitabha Triad (National Treasure 218), not the upper label's Kshitigarbha
with Entourage. It is also different from the existing CMA Leeum triad (photo 231).

Two supplemental photographs are now imported from the user-provided local files:
- `ab5e5460014a3bf195f463aabb6a06ab.jpg`: complete work, 960 × 1280.
- `d1a298cd407a40c0cc7ebcb89fa37f39.jpg`: complete double label, 1280 × 1707;
  only the lower label refers to this work, explicitly stated in the caption.

Their hashes and responsive derivative provenance are recorded in `data/photos.json`.
Originals stay in `/home/qingxi/museum/`; no crop, color changes or reflection removal.
There are now 83 selected source photographs. For optional regeneration, pass
`--supplement-directory /home/qingxi/museum` to the image preparation script.

Read the Korean national heritage object's full record, including its dynamically
loaded Korean, English and Chinese descriptions. The entry distinguishes coming
in welcome from the alternative interpretation of predicting future Buddhahood.
The Washington exhibition page confirms the Sackler galleries within NMAA. The
account of digital re-encounter and the work not traveling to CMA is the user's
viewing evidence, not a newly claimed museum provenance record.

Follow-up validation: full site build, topic validation and existing SAMA cross-topic
check passed. Actual Chromium at 1440, 768 and 390 px passed homepage-to-comparison
navigation, image/caption alignment, artwork and double-label zoom, Escape, source
anchors and automatic opening of the evidence details. No horizontal overflow,
JavaScript error or failed image request. Preview screenshots are outside the repo
in `/tmp/ten-kings-review/leeum-*.png`.
