# Guangsheng Temple murals

Independent topic at `/museum-notes/guangsheng-murals/`, with a comparison page. All three canonical records and work pages remain in `chinese-painting/`; the existing `tejaprabha-assembly/` URL is reused. The topic adds two works, not three: Chinese painting data now contains 34 works, including 16 Buddhist paintings (7 temple murals). The general painting index remains 18 works.

## Build

`python3 scripts/build_museum.py` now calls `build_guangsheng.py`, which reuses the painting builder and shared image viewer. The existing `python3 scripts/build_paintings.py` followed by `python3 scripts/build_museum.py` workflow remains valid. No new runtime dependency.

- `data/topic.json`: topic introduction, original wall positions, historical notes and named sources.
- `../chinese-painting/data/works.json`: the single source for artwork records, notes, images and citations.
- `data/intake.json`: all 14 input files, hashes, label pairings and previous Tejaprabha selection.
- `guangsheng.css`: small scoped additions for comparison layout and topic spacing.

## Intake and evidence, 2026-10-09

Source: `/home/qingxi/museum/广胜寺壁画`. Dates in filenames are not visit dates.

- 750–751 / label 752: Met 65.29.2, Medicine Buddha assembly, ca. 1319, east wall of the lower monastery's Mahavira Hall. Dimensions and gift in 1965 from Met collection record; iconography/material observations also supported by photographed label. The two smaller standing Sun/Moon bodhisattvas are distinct from the larger seated attendants. Workshop association is not autograph authorship.
- 753–759 / label 760: Nelson-Atkins 32-91/1, Tejaprabha assembly, early 14th century, west wall. Existing overview 375 retained; six new details and new context 753 replace earlier gallery selections. All older image files remain available. 763 is an alternate context view, not published.
- 761 / label 762: Nelson-Atkins 47-88, Sudhana visiting the wise boy, south wall. Chinese episode title and early-14th-century dating follow the label; online broader 14th-century dating disclosed. Online provenance establishes 1933 Burchard purchase, 1934–1947 loan and 1947 gift.

Ten new artwork photographs copied byte-for-byte; no crop, stitching, recoloring or online replacement photos. Three labels stay local, consistent with the painting section. The whole topic uses 11 selected photos including existing 375. No sculptures in gallery context are attributed to Guangsheng.

Research links are embedded beside public notes. Nelson records describe a 1929 stele recording sale in 1927; Met's current webpage says 1930s. The topic preserves that discrepancy instead of silently harmonizing dates. The relation of the Buddha pairing to the 1303 earthquake is presented as museum interpretation. The modern Nelson temple room is a composite installation, not a reconstruction of the Guangsheng hall.

Validation: full static-site local links/anchors; original-photo SHA-256; desktop/mobile topic, comparison and three work pages; image decode, zoom, gallery navigation and overflow checks. Existing Buddhist entrance, painting index and adjacent-work pagination regenerate from the same data.
