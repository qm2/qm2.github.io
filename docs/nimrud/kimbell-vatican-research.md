# Kimbell and Vatican additions — 2026-11-11

Four user chat attachments were extracted byte-for-byte from the matching user message, after confirming the images were not supplied as server files. The preserved attachment files live outside Git at `/home/qingxi/museum/nimrud-kimbell-vatican-assets/originals/`. The archive's upload manifest and upload report verify SHA-256 for all four JPEGs and twelve full-frame WebP derivatives. No cropping, retouching, third-party image or inferred visit date is introduced. Attachment resolution is 1280×1707, except the Kimbell pair at 1707×1280. These are the received attachment bytes, not a claim to camera-original resolution.

Canonical records: `museum-notes/nimrud-guardians/data/works.json`.

- `kimbell-pair`: attachment 2 (pair) / attachment 1 (label). AP 1981.04 a,b: two objects presented in one viewing group. The a/b dimensions are not assigned to left/right by inference. Label “105” is not used as accession. Official c.874–860 BCE, Gypsum, a 92×70 cm, b 90.7×73.5 cm. Room L; no specific slab number confirmed. The museum's full provenance text explicitly qualifies the alleged 1854 Bombay acquisition. Page body, dimensions and provenance were available in the web tool's official-domain cached full text; direct HTTP access returned 403. https://kimbellart.org/collection/ap-198104-ab
- `vatican-14990`: attachment 3 (figure) / attachment 4 (label). English title, 883–859 BCE and Room L follow the photographed label; IX.3 is distinguished from Inv.14990. No dimensions, exact stone composition, acquisition date or route are inferred from another Vatican relief.

## A real room-attribution discrepancy

Read the Barracco museum's MB 47 record in full. It identifies Room I and describes VAT/14990 as the lower register associated with MB 47's kneeling figure. This is a proposed reconstruction, not a fresh independent physical join by this website.

https://museobarracco.it/en/percorsi/percorsi_per_sale/piano_primo/sala_ii_arte_egizia_e_mesopotamica/genio_alato_inginocchiato

Downloaded and read the university-hosted excerpt of *Gli Assiri all’ombra del Vesuvio* (2019), object entry 7, printed p.206, signed GPB (Gian Pietro Basello, identified in the credits). It assigns MB 47 to I-04 and names VAT 14990 among fragments proposed for the same orthostat. This gives the exact I-04 research lead, while the user's Vatican label says L. Both records are preserved with their sources. No unified room claim or speculative reconstruction diagram is published.

https://unora.unior.it/retrieve/dfd1bedd-6b1a-d55a-e053-3705fe0af723/Graziani2019%20SCHEDE%20Assiri%20ombra%20del%20Vesuvio%20Mostra%20MANN.pdf

Cagni 1995 pp.96–97 no.2 and Paley/Sobolewski 1987 are references cited by the 2019 entry, not independently read. The Vatican web feature “Rilievo con Genio alato” describes a human-headed figure with horned crown; it is not used as the accession-level record for the photographed eagle-headed Inv.14990. The general Room IX page likewise does not establish this object's provenance.

## Counts and maintenance

Six viewing groups, seven collection objects if AP 1981.04 a and b are counted separately; thirteen photographs. “Seven” is not a count of physical broken stone pieces: Cleveland's joined relief is one collection object. Four prior IDs and original image hashes are preserved. Site/home/Ancient West Asia entrances and room links are generated from the same source data.

The full museum build and Nimrud checks pass. The broader old `check_xiangtangshan.py` traversed all site links successfully but then failed its unrelated hardcoded `selected_count == 59` assertion, already stale in HEAD after the previous SAMA addition. It was not changed in this task. `check_sama_batch.py` provides an additional cross-topic regression and link check.

Browser validation passed at 1440×1000, 768×1024 and 390×844: six viewing anchors; native label and research-note disclosure; original JPEG in lightbox; zoom, Escape and close button; source/room/compare anchors; matching photograph/caption widths and a 12px gap; no horizontal overflow or JavaScript errors. Desktop and mobile screenshots were visually reviewed, including the complete Kimbell pair, Vatican figure, room connections and comparison area. Preview artifacts remain in `/tmp/nimrud-*`, outside the published repository.
