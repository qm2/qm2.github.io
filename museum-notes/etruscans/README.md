# 伊特鲁里亚文明：亲见作品录

First batch: SAMA, *The Etruscans: From the Heart of Ancient Italy*, October 31, 2026–March 14, 2027. Visit month November 2026; no confirmed visit day. Owner/loan institution is distinct from the viewing venue.

## Build and checks

```sh
python3 scripts/build_etruscans.py
python3 scripts/check_etruscans.py
# With the repository served at http://127.0.0.1:8765:
python3 scripts/check_etruscans_browser.py
# Whole notebook build includes this builder last:
python3 scripts/build_museum.py
```

The builder reuses the shared Roman-sarcophagus layout and gallery and Caravaggio lightbox. CSS and additional JS are scoped to this topic. It idempotently reconnects the museum home, Greek/Roman bronzes, Roman sarcophagi and their stories page. Do not edit generated HTML directly.

## Canonical data

- `data/objects.json`: 131 stable records, each potentially a single object, component or group; not a reconstruction of the museum's approximately 130 exhibition objects. Collection, geographical relationship, visit events and exhibition membership are separate. No visit date is inferred from filenames.
- `data/photos.json`: all 377 originals, hashes, dimensions, original filenames, roles and inverse object links. 202 object, 129 label, 20 detail, 16 panel, 10 context photographs. Shared images are stored once. Panels and context remain accessible even when they do not belong to one object.
- `data/deep_readings.json`: 53 edited readings; the other 78 have independent compact data/photo pages. These are not additional objects.
- `data/chapters.json`, `comparisons.json`, `places.json`, `timeline.json`, `collections.json`, `function_taxonomy.json`: nine editorial chapters, eight comparisons and reusable facets. 29 place entries, 18 approximate coordinates, ten shown initially. Modern discoveries are separate from ancient object dates.
- `data/personal-favorites.json`: five user-selected favorites and supplied personal foreword; full-photo choices are distinct from homepage detail crops.
- `data/captions.json`, `detail-crops.json`, `object-notes.json`: photographic descriptions, explicit crop bounds and evidence discrepancies.
- `content/civilization-guide.md`, `data/deities.json`, `glossary.json`, `sources.json`: background, lookup and traceable research scope. Unread catalogue/partial web records are not represented as full-text research.
- `data/naming-review.json`: ordinary nouns and descriptive artwork titles are translated into readable Chinese while `title_en` keeps the original label. Proper names use documented Chinese usage where available (e.g. Vulci / 武尔奇); uncertain names keep their source spelling. Chinese descriptive titles are not asserted to be official Chinese museum titles.
- `data/photo-editing.json`: source-pixel crop recipes, separate cover/detail choices, paragraph-level details and an audit of all 53 reading covers. `image-derivatives.json` records generated dimensions and versioned filenames; `detail-crops.json` exposes the five favorite details. These never add records to the 377-photo index.

## Photos live on Cloudflare R2

All image bytes are **outside Git**. `museum-notes/image-hosts.json` maps this topic to `https://images.mertonmuseum.com`. HTML uses `scripts/museum_image_urls.py`; preview and live site load the same public assets. No credentials are needed to build or view.

Original ZIP and extracted package remain under `/home/qingxi/museum/`. The 377 original JPEGs retain their supplied bytes. WebP derivatives never exceed original resolution (long edge approximately 1700 px); no color/reflectance repair or AI alteration. Editorial crops have explicit source-photo bounds. Originals and older derivatives remain intact; new content-versioned URLs avoid stale CDN images.

```sh
python3 scripts/prepare_etruscans_images.py \
  /home/qingxi/museum/etruscans-codex-pack \
  /home/qingxi/museum/etruscans-assets/images
```

The external asset directory contains an upload manifest and verification report, not API keys. Initial upload: **1,843 objects, approximately 189.2 MB**; the November 11 composition pass adds 64 versioned derivatives (about 6.9 MB). Every object was fetched from the public custom domain and SHA-256/Content-Type checked. Files use `museum-notes/etruscans/images/`; originals are in its `originals/` subtree. Do not upload the ZIP, research pages or credentials.

## Future additions

Reuse an object ID for a return visit; append a visit event and new photo links, not a duplicate object. Give a new object its own ID and actual exhibition membership; keep the original SAMA group distinct. Add a place only when supported: no-coordinate records still work in text filters. Add its owner to collections and connect it to a suitable chapter. The grid, facets, map member counts and dated rows derive from the same records. Keep future exhibition and venue-specific introductions accurate when adding a new batch.

Start a basic record with `new_object_template.json`; fill `visits`, the label source and reciprocal photo links, then add a reading only when research supports it. Test the new original/derivative paths publicly before publishing HTML. The preparer currently processes the first supplied package; for later batches merge the canonical photo index rather than overwriting it with the original first-batch output.

## Identity and evidence safeguards

- e111 is Louvre **Cp5193.1-2**, a cinerary urn, not the larger Cp5194 sarcophagus.
- e129 is Hinthial from Torraccia di Chiusi near San Gimignano, not Chiusi city or Volterra's *Ombra della Sera*. The official conservation page records discovery during 2010–2011.
- e122 retains AD 1–100.
- e069–e076 share p215 and numbered label p216; no separate object photo is fabricated. e064–e068 use p209; p214 is animal-head necklace no.4, p213 human-head necklace no.5.
- e035: impasto in label material field versus bucchero in explanatory text/SAMA; material remains 陶.
- e083: label inventory 13636 versus SAMA 51846. e105: label ca.500–475 BC versus SAMA 500–480 BC. e085 retains its wide 600–200 BC label date.
- e101/e110/e112/e127/e130/e131 lack a confidently transcribed inventory number; e072's number also needs checking. No incomplete code is silently completed.
- Modern display support, copied tomb-painting backgrounds and the ancient votive temple model are distinguished in captions/reading. A shared display never proves a shared original ensemble.

The complete editorial research and photo-matching handoff stays outside Git. Only supported, reader-facing text is rendered. Research notes in `content/` record remaining issues but are not copied into public body text.

## Rebuild the photographic edit only

```sh
python3 scripts/prepare_etruscans_editorial.py /home/qingxi/museum/etruscans-assets/images
python3 scripts/build_etruscans.py
```

The crop source is always an original JPEG, never an earlier thumbnail. Widths in filenames and srcset must equal decoded pixel widths. The browser's density-corrected `naturalWidth` is not the file's encoded width. Match `sizes` to the rendered width and validate decoded files separately. Local before/after screenshots live outside Git in `/home/qingxi/museum/etruscans-assets/review/`.
