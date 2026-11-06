# 造像与发愿

15 independent readings of 12 core and 3 visual-feature stone sculptures, with 59 personal artwork/detail/label photographs. Route `/museum-notes/images-and-vows/`.

## Sources of truth

- `data/works.json`: stable object identities, museum/owner/display distinction, chronology, material/dimensions, original essays, related works, inscription evidence and publication status. `mfah-526-faxing` uses slug `faxing-526` and shares identity with `/xuzhou/x24/`; the new reading is not a second physical artwork or a redirect.
- `data/photos.json`: object association, exact original filename/SHA-256, view-specific caption, responsive variants and display rotation. Labels 1832 and 1839 rotate 90° counterclockwise in derivatives; originals remain unchanged.
- `data/sources.json`: references, evidence type and research scope. Only cited references render on each page.
- `data/editorial.json`: five narrative chapters, selections/comparisons and documented collection nodes. Counts/catalogue are computed from works, not hand-maintained elsewhere.
- `../../docs/images-and-vows/`: intake audit, full original 111-image manifest, research and outstanding issues. Original archive remains `/home/qingxi/museum/南北朝石像.zip`; all 111 extracted originals remain in that sibling folder's `photos/originals/`. Do not delete unselected photographs.

## Inscription policy

No OCR or visual decipherment of carved text. Eight records contain published full inscriptions or complete published text passages: 490, 494, 511, 526, 528, 530, 533–543 and 545. Each has a source ID and explanation of textual status. Preserve lacunae, difficult words and variant forms; modern paraphrase is explicitly 本站意译. 528 retains the later 743 addition with a separate note. For the remaining works, museum summaries/iconographic studies are not back-translated into invented ancient inscriptions.

The 500-year Cleveland stele has a potential older transcription with a 499 date, but its identity/date correspondence remains unverified: not published as established text. The 526 `二區` is not a count of figures in the triad and does not establish another object's whereabouts. 511 王州子/王叔子 and 543 Helian/李道赞 remain source-specific distinctions.

## Build and check

From repository root:

```sh
python3 scripts/build_museum.py
python3 scripts/check_images_and_vows.py
python3 scripts/check_images_and_vows_browser.py
```

Browser check requires local socket and Chromium access. It opens desktop/mobile viewports, checks all detail pages, photo/caption alignment, gallery views, show-all, labels, full-text disclosures, lightbox zoom/Escape/focus, filters, deep links and parent entrances. Screenshots are local `/tmp/vows-*.png`, never public resources.

`build_images_and_vows.py` builds only this topic and idempotently inserts the two parent entries. Main build invokes it after the existing topics. `build_xuzhou.py` renders optional `context_links`; only x24 uses the new backlink. No unrelated styles are changed; CSS/JS use the `iv-` scope and reuse the existing image dialog.

The handoff initially requested a local draft. The user subsequently explicitly authorized publication, so the completed and checked first edition follows the repository's main-branch GitHub Pages publication flow.

## Add later photographs or objects

Use an existing work ID for another view of the same sculpture, append its photo record and caption, and regenerate derivatives without overwriting originals. New independent objects require their own verified identity/source record before adding to the public works array; candidates remain in the research audit. Never infer visits from upload filenames. Keep temporary scans, third-party images and unpublished book pages out of public assets.

## First-edition validation

Full museum rebuild succeeded. Static checks verified 15 identities, 59 original hashes, 8 sourced transcriptions, all generated links and anchors, and parent/back links. Existing Xuzhou, Japanese Zen and Yongle–Xuande checks also passed. Chromium was exercised at 1440, 390 and 320px: every view in the five extended galleries, every published image and label across all fifteen pages, show-all, keyboard activation, lightbox zoom/Escape/focus, full-text anchors, filters and no-JavaScript reading. Photo/caption widths and left edges match within 2px, with close spacing and natural image aspect ratios. Screenshots were inspected for cover, inscriptions, detail image and north/south comparison. No third-party artwork photography is introduced.
