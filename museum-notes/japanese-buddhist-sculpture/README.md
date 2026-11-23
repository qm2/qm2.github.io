# 东瀛佛影 · 日本佛教木雕

Repository implementation of `/home/qingxi/museum/日本佛教木雕-Codex专题包.zip`, read from START_HERE.md and CODEX_PROMPT.md; PREVIEW.html reviewed locally. User requested a Japan-specific title during implementation: selected **东瀛佛影**, replacing the package's provisional 华丽中的宁静. Stable route: `/museum-notes/japanese-buddhist-sculpture/`.

## Scope and source of truth

- 62 independent work/group records; **not 62 individual wood statues**. Includes bronze comparison j08, drum stand j18, household altar j60 and multi-object groups.
- 149 unique original photographs; j04/j05 share 3121 and 3122. Both records remain distinct.
- 16 personal recollections (unranked), nine research selections, 25 substantive essays, six complete chapter readings, a viewing/technique guide, ten comparison groups, atlas/timeline and 62 stable detail pages. Total 73 HTML pages.
- `data/catalogue.json`: canonical identities, dating, photo associations and viewing/collection distinction. `display-notes.json`: short reader-facing notes for non-essay entries; preserves original research notes in the canonical intake.
- `content/`: supplied texts, edited to remove handoff directions, third-person references to the author and visible file numbers. Research qualifications and complete paragraphs are retained. IDs in prose render as actual work links.
- `research/source_registry.json`: original research access levels. Sources page explicitly attributes these to the supplied research; it does not claim every linked book has been read in this implementation. CMA 1960.197 and Walters TL.1974.35 were re-opened in this round; Kimbell returned403. No additional historical conclusion was inferred from access failure.
- `data/atlas-index.json` is generated. Map panels and counts are generated from catalogue data; `viewing-museums.geojson` supplies15 physical museum locations. Boston/Mia collections do not become personal visit points; their two records are viewed at MFAH.

## Images

149 originals retained byte-for-byte in the unpacked archive and uploaded to existing R2 at `https://images.mertonmuseum.com/museum-notes/japanese-buddhist-sculpture/originals/`. 447 WebP previews (400/900/up to1600 actual pixels, never upscaled). All596 uploads verified by public GET, content type and SHA256. No binary photographs in Git. Preparation/upload logs are under `/home/qingxi/museum/japanese-wood-assets/`.

`data/media.json` holds hashes, true dimensions and URLs. Full figures precede detail views; j19 uses3152 for whole-body display while keeping3151 as a close view; original main-photo metadata remains traceable. j23: full → drapery → side → back/pattern. j40: full → head/body → detailed drapery. j41: front/back. j58: two distinct figures visible together. j59: full → back → side → garment close views. j04/j05 captions explicitly identify the back bust/front seated figure in the shared image. All labels open full originals. Existing Nelson34-10 image is reused only in the cross-topic Water Moon comparison, not added to this intake count.

## Maps and dates

Local SVG, no map API or third-party runtime. Reuses the site's Homer `ne_110m_land.geojson`, Natural Earth public-domain land (repository provenance in Homer README). Modern museum points and historical context map are distinct. No migration routes. Nearby museums cluster; presets cover Paris, Hawaii, Texas and US east coast. Every museum has a keyboard-accessible, searchable static list. No-JS or missing geometry retains all works and links.

Timeline uses the provided numeric ranges, with original date text preserved. Exact years are not manufactured from midpoints. j42 shows11th/12th-century disagreement, j50 separates figure/base, j62 uses13th-century sculpture dating rather than Saichō's lifespan. j12's components retain separate dates in the essay. Visit dates remain null.

## Build and maintenance

```
python3 scripts/build_museum.py
python3 scripts/check_japanese_wood.py
python3 scripts/check_japanese_wood_browser.py http://127.0.0.1:8774
```

The main build invokes this generator after existing topics. Parent Japan and museum entrances are idempotently integrated, preserving all existing pages. Add new works in the canonical catalogue, associate original photo metadata, update museum coordinate source if needed, then rebuild; map counts, filters and timeline derive from records. Do not override supplied dates or attributions for visual symmetry.

## Remaining research limits

Guimet j04/j05 and Penn j44 accession uncertainties remain. Museum/label dating differences remain for j24, j41, j42 and j45. j20/j25 identities remain qualified. j62 correspondence is based on the author's provided comparison; Walters page has no image. Kōei / Unkei IX is retained without guessing Chinese characters or conflating with the original Unkei. No new temple provenance, visit dates, inscriptions or third-party artwork photographs were introduced.

Screenshots and browser artifacts: `/tmp/japanese-wood/`. Validation covers all73 routes, 1440/768/390px, full-image aspect ratios, photo viewer and labels, search/filter/reset/history, source anchors, museum selection, Paris/Hawaii and map failure/no-JS fallbacks.
