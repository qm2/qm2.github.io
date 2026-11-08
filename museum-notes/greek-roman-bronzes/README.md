# Greek and Roman bronzes / 希腊与罗马世界的青铜

A small, photographic notebook beside the Roman sarcophagi topic. Four reading themes, 18 stable viewing-group pages, a short history guide, four comparisons and a museum/date atlas. Built with the existing paper/type styles and shared image viewer; no new dependencies.

## Canonical content

- `data/works.json`: stable b01–b18 records. Collection/viewing museum, museum city, null visit dates, photographed labels, date alternatives and physical components are separate fields. A group is not necessarily one complete statue or one accession.
- `data/photos.json`: 44 original photos, SHA-256, orientation, responsive derivatives, role and linked works. Shared 1973/1974 labels are stored once. 1997 was unrelated and excluded at intake.
- `data/editorial.json`: public reading text, observation lists, memory cues, documentation and related objects. Edit here; generated HTML is not the source of truth.
- `data/sections.json`, `comparisons.json`, `history.json`: reading arrangement and contextual content.
- `data/museums.json`: eight viewing institutions; map and filters derive from the same records. Coordinates identify modern museum sites, not ancient workshops or itineraries. Rome labels have callout offsets; geographic anchors remain explicit.
- `data/sources.json`: supplied research references, source scope/limits, plus independently checked Constantine record S33. Only relevant references appear on each page. See `docs/greek-roman-bronzes/RESEARCH_UPDATE.md` for this round's reading status.
- `images/originals/`: the user's JPEGs, unchanged filenames and bytes. Derivatives are upright WebP; labels 1966 and 1992 are rotated 90° counterclockwise, photo 1993 90° clockwise. All transformations are recorded and reversible. No third-party artwork images or contact sheets are published.

## Dates and groups

- b03: head MC1072, left hand MC1070, globe MC1065; three components, one viewing group, original association not assumed.
- b14: two Nemi hand/forearm fittings; two photographs are views of those fittings, not three objects.
- b16: Apollo statue and detached fragments form one research group.
- b06: wolf shown separately from the 17 ancient timeline records, with traditional ancient and medieval scientific dating.
- b09: separate candidate points 176 and 180, not a fabricated intermediate year.
- b15: timeline endpoints 80–225 are display bounds for “late 1st–early 3rd century,” expressly not known years; original prose is authoritative.
- b17: current online 1st century CE and photographed 1st century BCE both retained, separate timeline bands.
- b02: online 475–450 BCE vs photographed 490–450 BCE retained.
- b07, b08, b13, b14 have no confirmed accession number. Archive photograph IDs must not populate accession fields.

## Build and check

From repository root:

```sh
python3 scripts/build_greek_roman_bronzes.py
python3 scripts/check_greek_roman_bronzes.py
python3 scripts/check_roman_sarcophagi.py
python3 scripts/build_museum.py
```

The full museum build invokes this generator last, following the Roman generator. Homepage entrance placement is idempotent. Roman home has a reciprocal link maintained in its own generator.

Serve the repository locally, then run:

```sh
python3 -m http.server 8791 --bind 127.0.0.1
python3 scripts/check_greek_roman_bronzes_browser.py
```

Browser checks cover 1440/390/320 px, every generated page and image, original links, rotated label, gallery all/previous/next, zoom/Escape, map/filters, URL state and back/forward, date alternatives, exact caption alignment and natural image proportions. Reports/screenshots remain under `/tmp`, outside published resources.

To regenerate images from the original handoff, use `scripts/prepare_greek_roman_bronzes.py [extracted-package-directory]`. Ordinary content builds do not require the source package. For later visits, retain the work ID and append photos with real visit dates only when supplied; add museum records only for new viewing institutions. Counts, maps and navigation regenerate from canonical data.
