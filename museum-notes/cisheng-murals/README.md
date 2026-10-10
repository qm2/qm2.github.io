# Cisheng mural notebook

`/museum-notes/cisheng-murals/` stands alongside Guangsheng, with a two-layer comparison at `compare/`. Five canonical records are reused from Chinese painting data; only Princeton y1952-41 is newly added. Total Chinese painting records: 35; Buddhist paintings: 17; murals: 8. Guimet MA 5020 is explicitly a related fragment, with temple provenance not independently established by its public museum record.

## Sources and build

- `data/topic.json`: topic copy, groups, card observations, named historical sources.
- `../chinese-painting/data/works.json`: all work notes, titles, image selections, dates and source links. Existing URLs preserved.
- `data/intake.json`: every input file, original name, SHA-256 and label pair.
- `scripts/build_cisheng.py`: called by `build_museum.py`; reuses painting shell, cards and lightbox. `python3 scripts/build_museum.py` regenerates these pages. Existing painting-then-museum workflow remains valid.
- `cisheng.css`: limited topic layout additions; no JS or dependency added.

## Photo mapping, reviewed 2026-10-10

Source directory: `/home/qingxi/museum/河南温县慈胜寺`, 11 files.

- 381 / 382: Nelson 52-6, Ruyilun Guanyin.
- 383 / 384: Nelson 50-64A, two bodhisattvas burning incense (upper layer).
- 385 / 386: Nelson 50-64B, Guanyin discovered below the preceding work.
- 456 / 457: Guimet MA 5020, Akashagarbha, related fragment.
- 764 / 765: Princeton y1952-41, attendant bodhisattvas. Adjacent small exhibits in 764 are not part of the mural.
- 372: Nelson room context, placed in the Ruyilun gallery and comparison page; not a new work or reconstruction.

Four object photographs exactly match existing published files and are reused. Two new unchanged copies (372, 764) total about 602 KiB. Labels stay local. No cropping, stitching, generated imagery or inferred visit dates.

## Research boundaries

Nelson 50-64B: photographed label gives 937, current online record ca. 951–953; both retained visibly, while the established lower/upper relation is explained without calculating an exact interval. 50-64A and B were gifts of C. T. Loo in 1950; the 1952 separation photographs are documented on label 386. 52-6's purchase credit does not independently establish a dealer, so no dealer or purchase year is supplied from the accession number.

Princeton's museum record describes the fragment as believed from Cisheng, with no signature or date. Its conjectured counterpart at the Smithsonian is mentioned only in prose, not added to the user's viewing list. Princeton provenance establishes purchase from C. T. Loo in 1952. The two-stage mud and lime preparation description follows label 765 and the same museum record.

Guimet's label and French national inventory identify a Henan temple, not Cisheng. The inventory lists 952, dimensions 194 × 172 cm, acquisition 1986 and previous owner Loo, Ching Tsai. A 2021 research abstract explicitly discusses the Guimet Akashagarbha in the attributed Cisheng group. This supports comparison, not a new secure provenance assertion. The museum title remains; an alternative Suryaprabha identification is attributed to that research.

Research abstract consulted: 황선우, “Rethinking the Date and Iconography of the Mural Attributed to Cishengsi Monastery in Henan Province,” 2021, pp. 99–122, DOI 10.17300/dah.2021.29.4; https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002733973 . Only abstract-level claims are used, not a claim to have read the full paper. The Chinese title on the source link is a descriptive translation. Temple attribution and date remain research questions; no exact room/wall reconstruction, common production date or original group size supplied.

The SYSU 2025 field-course report supports the distinction between surviving Yuan-era structures and the attributed early mural group. Its broader source and chronology discussion is not treated as final archaeological proof. Other museum records and corresponding photographed labels supply work-level facts.

## Verification

Check all local paths and anchors with `python3 scripts/check_xiangtangshan.py /home/qingxi/museum/xiangtangshan-organized` (also traverses the full museum site). Browser checks cover 390/1440 px layouts, five canonical work pages, both Cisheng pages, Guangsheng and category entrances, image decode/zoom, mural filters and no-JavaScript readability. Intake hashes verify all six published images.
