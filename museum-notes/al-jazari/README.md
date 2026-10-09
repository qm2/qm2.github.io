# Al-Jazari / 贾扎里的奇妙机械

Three personally photographed manuscript leaves; no stock photographs or reconstructed diagrams. Source of truth: `data/works.json`. `data/intake.json` accounts for all six files in `/home/qingxi/museum/伊斯兰奇妙机械知识之书`, with SHA-256 hashes. Three art photographs are copied unchanged; three label photographs remain in the source archive.

Rebuild with `python3 scripts/build_museum.py` (includes `build_jazari.build()`), or `python3 scripts/build_jazari.py` after data-only changes. This creates the topic, three detail pages, comparison, Islamic art parent and idempotent homepage entry. All pages use existing `museum.css` and Caravaggio gallery CSS/JS; no new dependencies.

## Identity audit, 2026-10-08

| Photograph / label | Identification | Evidence |
| --- | --- | --- |
| 696 / 697 | F1930.75 recto, handwashing servant, December 1315, probably Syria | Exact Freer image and label; official record names calligrapher Farruq ibn Abd al-Latif; painter not separately recorded |
| 698 / 699 | F1932.19 recto, seated man / water-clock part, Egypt, 1354 | Exact Freer image and label; elephant-clock identification is from the photographed label, not inferred from the isolated image |
| 700 / 701 | LNS 17 MS, folio 30c, scribe water clock, December 1315, probably Iraq per label | Individual leaf identity, date, medium and mechanism from photographed MFAH label; LNS ownership confirmed by al-Sabah's own other-leaf record and Met 2016 checklist; loan context from MFAH |

## Boundaries and unresolved questions

- The two Freer leaves are from different dated manuscripts. No direct codicological reference linking **F1930.75 specifically to LNS 17 MS folio 30c** was located; their shared 1315 date is not treated as proof of a shared physical codex.
- No publicly accessible individual catalogue record for **30c** was located. Links to the al-Sabah record for **123v** are explicitly labelled as another leaf, never passed off as the pictured object. No dimensions transferred from 123v.
- The 2016 Met checklist names Farrukh ibn Abd al-Latif as scribe and artist for LNS 17 MS, but illustrates the perpetual flute leaf. This is recorded as manuscript-level attribution, not a verified individual signature on 30c. Freer's spelling Farruq is retained in its own record.
- Original composition in 1206 is distinguished from both later manuscript dates, following the Met 1978 Bulletin. Background device count follows Freer/Met; modern superlatives are omitted.
- Handwashing sequence comes from label 697; duck drainage from the Freer catalogue. Internal valves, triggers and complete linkage are not reconstructed.
- Label 699 calls the released object a gold disk; the Met's complete elephant-clock leaf 57.51.23 describes a ball. Difference retained in the note. Met leaf supplies only contextual comparison, not a fourth visit/photo. No missing mechanism added to F1932.19.
- The scribe clock float/string/pulley explanation is attributed to the 1001 Inventions reconstruction commentary. Visible colored components are described but not individually identified without the leaf's text.
- `paragraphs[].evidence` distinguishes label, photo observation, and research; named source keys render beside their paragraphs. No personal feelings or visit dates inferred from filenames.
