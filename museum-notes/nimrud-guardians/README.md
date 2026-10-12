# Nimrud / 尼姆鲁德的有翼守护者

Editorial source: `data/works.json`. Build: `python3 scripts/build_museum.py` (includes `build_nimrud.py`). The topic is one complete reading page, with an Ancient West Asia entrance and homepage link. Shared painting lightbox and image orientation code are reused without modification.

## Intake and research, 2026-10-11

Six original JPEGs from `/home/qingxi/museum/亚述有翼精灵` are copied byte-for-byte. `data/intake.json` records SHA-256 hashes, filename suffix matching, dimensions, and display rotation. Artwork/label pairs: 768/769 MFAH 80.53; 770/771 Cleveland 1943.246; 772/773 Nelson 40-17. Label 773 is displayed with CSS rotation -90°; original bytes remain unchanged. All three labels are collapsed by default. Filenames are not visit dates. Cleveland's joined sections are one collection object.

Sources in works.json were opened and checked; all six photographs were inspected. MFAH's canonical English route returned 403; its official `/fr/objects/5273/guardian-figure` route supplies the English object text and provenance. Cleveland provenance was checked against its official open-access API (not just the abbreviated object page). Nelson's provenance identifies Room L; its bibliography cites Meuszyński 1981, p.67, no.L-10. The underlying 1981 publication was not independently read; the public text attributes this identification to the museum's record and bibliography. No modern gallery number is used as a palace room.

Museum dates/materials/dimensions retained independently, including Nelson's Limestone and 884–860 BCE. Houston’s exact original room remains unresolved. Cleveland is identified as Room S, slab S-06 by its museum bibliography and CDLI P427317; its label describes a room adjacent to the throne room. Cleveland's early provenance dates are ambiguous in the API; the notes state only Amherst, Brummer, and the secure 1943 acquisition. Nelson's 1855 gift/departure is not confused with arrival in Saint Louis. Houston provenance is independent of those routes.

Met objects support shared iconography and historical context only; neither is counted as a visit. Tree fertilization is identified as Nelson's interpretation, alongside purification/protection readings. Museum labels support observations and the Cleveland adjacent-room statement; their reconstruction illustration is not extracted. No additional images, inferred deity names, modern display statuses or personal feelings are added.

Checks: `python3 scripts/check_nimrud.py`; full-site links via `python3 scripts/check_xiangtangshan.py`; browser tests at desktop and mobile widths (lightbox, rotated label, full images, overflow and navigation).

## Room identification follow-up

The user supplied the S-06 / L-10 lead. Independently opened Cleveland’s printable collection record and CDLI https://cdli.earth/artifacts/427317: both explicitly identify S-06; the museum bibliography also cites Klaudia Englund, Room S, S-6. Nelson’s collection record was rechecked: provenance Room L and bibliography Meuszyński 1981 p.67 no.L-10. Updated canonical room fields, the two notes and the shared source note. CDLI uses Limestone for Cleveland; the displayed material continues to follow the holding museum’s Gypsum, as required. No original publication beyond these online records is claimed as directly read.

## Context and citation cleanup

Added an approximately 150-character paragraph from TARII’s Nimrud project report: 2015–2016 destruction, Iraqi Nimrud Rescue Team recovery and stabilization from 2017, subsequent TARII support and the 2025 emergency stabilization focus. These activities are not described as completed reconstruction. The historical introduction now states the Ashurbanipal/Nineveh distinction directly. Work-note citations are deduplicated and grouped at each entry’s end, preserving paragraph-level source associations in JSON. The readable Cleveland print record replaces its API link in public citations; earlier API research remains documented above.
