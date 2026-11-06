# 造像与发愿

15 independent readings of 12 core and 3 visual-feature stone sculptures, with 57 associated personal artwork/detail/label photographs (59 archived originals). Route `/museum-notes/images-and-vows/`.

## Sources of truth

- `data/works.json`: stable object identities, museum/owner/display distinction, chronology, material/dimensions, original essays, related works, inscription evidence and publication status. `mfah-526-faxing` uses slug `faxing-526` and shares identity with `/xuzhou/x24/`; the new reading is not a second physical artwork or a redirect.
- `data/photos.json`: object association, exact original filename/SHA-256, view-specific caption, responsive variants and display rotation. Labels 1832 and 1839 rotate 90° counterclockwise in derivatives; originals remain unchanged.
- `data/sources.json`: references, evidence type and research scope. Only cited references render on each page.
- `data/editorial.json`: five narrative chapters, selections/comparisons and documented collection nodes. Counts/catalogue are computed from works, not hand-maintained elsewhere.
- `../../docs/images-and-vows/`: intake audit, full original 111-image manifest, research and outstanding issues. Original archive remains `/home/qingxi/museum/南北朝石像.zip`; all 111 extracted originals remain in that sibling folder's `photos/originals/`. Do not delete unselected photographs.

## Inscription policy

No OCR or visual decipherment of carved text. Eight records contain published full inscriptions or complete published text passages: 490, 494, 511, 526, 528, 530, 533–543 and 545. Each has a source ID and explanation of textual status. Preserve lacunae, difficult words and variant forms; modern paraphrase is explicitly 本站意译. 528 retains the later 743 addition with a separate note. For the remaining works, museum summaries/iconographic studies are not back-translated into invented ancient inscriptions.

The 500-year Cleveland stele has a potential older transcription with a 499 date, but its identity/date correspondence remains unverified: not published as established text. The 526 `二區` is not a count of figures in the triad and does not establish another object's whereabouts. 511 王州子/王叔子 remain source-specific distinctions. For 543, CBETA and the 2009 study now distinguish 寺主赫连子悦 from 都邑主李道赞; competing claims of primacy remain attributed.

## Build and check

From repository root:

```sh
python3 scripts/build_museum.py
python3 scripts/check_images_and_vows.py
python3 scripts/check_images_and_vows_browser.py
```

Browser check requires local socket and Chromium access. It opens desktop/mobile viewports, checks all detail pages, photo/caption alignment, gallery views, show-all, labels, full-text disclosures, lightbox zoom/Escape/focus, filters, deep links and parent entrances. Screenshots are local `/tmp/vows-*.png`, never public resources.

`build_images_and_vows.py` builds only this topic and idempotently inserts the two parent entries. Main build invokes it after the existing topics. `build_xuzhou.py` renders optional `context_links`; only x24 uses the new backlink. No unrelated styles are changed; CSS/JS use the `iv-` scope and reuse the existing image dialog.

The first edition was published with user authorization. The research revision and atlas were initially local only. On 2026-11-06 the user authorized committing the completed topic changes; this does not authorize pushing or deploying this revision.

## Add later photographs or objects

Use an existing work ID for another view of the same sculpture, append its photo record and caption, and regenerate derivatives without overwriting originals. New independent objects require their own verified identity/source record before adding to the public works array; candidates remain in the research audit. Never infer visits from upload filenames. Keep temporary scans, third-party images and unpublished book pages out of public assets.

## First-edition validation

Full museum rebuild succeeded. Static checks verified 15 identities, 59 original hashes, 8 sourced transcriptions, all generated links and anchors, and parent/back links. Existing Xuzhou, Japanese Zen and Yongle–Xuande checks also passed. Chromium was exercised at 1440, 390 and 320px: every view in the five extended galleries, every published image and label across all fifteen pages, show-all, keyboard activation, lightbox zoom/Escape/focus, full-text anchors, filters and no-JavaScript reading. Photo/caption widths and left edges match within 2px, with close spacing and natural image aspect ratios. Screenshots were inspected for cover, inscriptions, detail image and north/south comparison. No third-party artwork photography is introduced.

## Research revision (2026-11-06, local only)

Five core pages use `inscription_data.passages` (original/translation/source), `terms`, `wish` and `variants`. `inscription_after` places readings after the first visual section. Full transcripts remain unchanged apart from paragraph whitespace. `photo_links` connect analysis to existing gallery views; `publications` keeps unread bibliographies distinct from directly consulted research. Homepage chapter `background` contains the Chengdu discovery audit.

Photos 1891/1892 were incorrectly associated with C429 in edition one. The modern label and Penn official record identify C404 (551). They remain archived with hashes and derivatives, but have no published work association. The selection remains 15 works, with 57 associated photos including 17 labels. No image files were changed or introduced. See `docs/images-and-vows/round2-review.md`.

## Atlas: complete viewing catalogue

`atlas/` now presents 32 objects / 103 photos / 13 museums. C404 is a separate atlas object reusing the two archived photographs; it is not associated with C429 or added to the 15 long readings. The original batch contains 35 independent objects: three Tang objects (seven photos) and one architectural photo remain in the internal audit only. See `docs/images-and-vows/atlas-review.md`.

Sources of truth:

- `data/atlas-core-metadata.json`: supplemental catalogue fields keyed to existing reading IDs. The original `works.json` still owns their titles, essays, photographs and routes.
- `data/atlas-extras.json`: the other 17 objects, including the confirmed New Orleans 2014.39. `museum_id` is the viewing institution, independent of owner, production region and discovery place. IDs starting `penn-` or `mfa-` can be legacy intake IDs, not museum evidence.
- `data/atlas-museums.json`: viewing institutions, city-level coordinates and evidence. Add one record for a new museum; map pins, counts and filters are derived.
- `data/atlas-photos.json`: personal originals, SHA-256, captions, roles, display rotation and responsive assets. Existing resources use relative references rather than duplicated images.
- `docs/images-and-vows/atlas-photo-audit.json`: complete intake disposition. Keep unresolved and excluded material here; do not fabricate a public identity.

`scripts/build_images_and_vows_atlas.py` merges these sources into `atlas/catalogue.json` and the HTML. Never hand-edit the generated catalogue or HTML. The topic/full-site builds invoke this builder. Atlas CSS/JS are scoped to this subpage.

To add another view, retain its work ID, append its photo association and photo metadata; retain the exact original filename and hash. To add a new object, add one supplemental object record and relevant museum if needed. Its `hero` must be one of its photos. Record `year_start`, `year_end`, `date_kind` and a `date_note` explaining approximate visualization bounds. Use a precise year only where sourced. Keep unknown visit dates null. Append original intake/audit records, including any excluded views, so every new file has a disposition. Never overwrite an old source photograph.

Once photo records exist, `python3 scripts/prepare_images_and_vows_atlas.py --source-dir /path/to/private/originals` copies only missing, hash-verified public originals and generates 400/900/1600px WebP without enlargement. `--refresh` regenerates derivatives only. Shared reading resources are verified and reused. Photos not in the public metadata are not copied.

Checks after changes:

```sh
python3 scripts/build_images_and_vows.py
python3 scripts/check_images_and_vows.py
python3 scripts/check_images_and_vows_atlas.py
python3 scripts/check_images_and_vows_atlas_browser.py
```

The atlas browser check covers desktop 1440 and phones 390/320, map/filter synchronization, browser history, chronological ranges, non-overlapping timeline cards, all photographs and labels, comparison view changes, lightbox zoom/Escape/focus, natural image proportions, aligned captions, deep reading links and no-JS reading. Local screenshots remain in `/tmp`.
