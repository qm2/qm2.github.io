# SAMA additions — November 2026

The supplied `sama-existing-topics-codex-pack` contributes **30 distinct works and 87 original photographs** to seven existing topics. The four photographs of the deferred Liao stone Guanyin (2461–2464) remain outside public data, assets, counts and updates. A month-level visit context was supplied; no exact visit day is inferred from filenames.

## Stable records and entrances

| Primary topic | Added records | Main entrance |
|---|---:|---|
| Nimrud | 1 | `nimrud-guardians/#sama-head` |
| Roman sarcophagi | 1 | `roman-sarcophagi/r28/` |
| Early Buddhist art | 4 | `early-buddhist-art/#museum-sama`; existing u01/u05/u06/u12 |
| Himalayan art | 19 | `himalayan-art/?museum=sama#places`; `sama-07`–`sama-25` |
| Wood sculpture | 1 | `song-liao-jin-wood/#object-2455` |
| Images and vows | 1 | `images-and-vows/atlas/#work-sama-eastern-wei-maitreya` |
| Yuan ceramics | 3 | `yuan-blue-and-white/#sama-duck-dish` and comparison page |

Densatil's fourth viewing group links to canonical Himalayan `sama-14`; its photographs are the same URLs, not copied assets or another Himalayan object. The 10th-century Pala stele links to early Buddhist u09 as a later comparison, without entering its period catalogue. Maitreya 2005.17 and torana L.2011.9 retain separate identities despite their shared display.

## Photos and reproducibility

`museum-notes/data/sama-2026-media.json` is the shared image manifest. Originals are byte-identical JPEGs; WebP variants retain complete composition and EXIF-correct orientation, with real pixel dimensions in filenames. All 368 objects (about 73 MB) were uploaded and publicly downloaded for SHA-256/content-type verification. No original or derivative binary was added to Git.

`python3 scripts/prepare_sama_images.py PACKAGE_DIR OUTPUT_DIR` regenerates the images outside the repository. Upload is a separate explicit operation using the existing R2 configuration; no credentials belong here. Public prefix: `https://images.mertonmuseum.com/museum-notes/sama-2026/`.

`intake-map.json` records package identities, assigned photographs and initial duplicate checks. Accession-number text hits were reviewed, not automatically merged. Existing object IDs and reading URLs remain stable. Checks preserve the original 111-photo Images-and-Vows intake audit separately from the new three photographs.

## Sources and evidence

- Supplied OBJECT notes, catalogue and photographed labels are the primary evidence for this batch. Contact sheets were visually reviewed; key label photographs were also opened individually. No inscription was independently transcribed from an artwork photograph.
- SAMA's **Kingship and Power in Assyria** exhibition page was read directly. Photograph 2388 supplies S-10, its south-wall context, and George Harding's 1926 acquisition. S-06 belongs to the previously researched Cleveland relief. These are two panels, not one sculpture.
- The SAMA digital catalogue's Mipham record was available as indexed text; the direct page was inaccessible. Its 2004.7.1, dimensions, purchase credit and older name are distinguished from the photographed Phuntsho Sherab label. No resolution of the identity disagreement or translation of the Tibetan inscription is claimed.
- Aimée Froom's 2020 **Arts of Asia** article was read directly, especially figures 15–16 and the Shah Jahan paragraph. AH 1043 / 1633–34 concerns the later mark, not manufacture. No underside photograph was supplied.
- Met records 38615 and 705435 were read directly for the relation of eight events to pilgrimage geography. They are different works. Their provenance and detailed scene placement were not transferred. The SAMA stele's reading sequence follows its own label (2411), with Nalagiri treated as an elephant's name rather than a place.
- Rubin / Project Himalayan Art, Jean-Luc Estournel's **Densatil Monastery**, was read for tower structure and the religious ensemble. It does not locate the SAMA panel in a particular tower or tier.
- The garland sarcophagus's online object record was blocked; its detailed hunting scenes, reused architectural lid, and the reported twentieth-century recarving opinion follow photograph 2395. No original tomb or workshop is assigned.
- Other SAMA/Crow records supplied in the package retain their stated access scope. Search-index information or supplied research notes are not represented as newly read full publications.

## Matters kept open

The lama's name/date discrepancy; Densatil panel's precise tower, level, orientation and individual female identities; torana's original relationship to the displayed Maitreya; crowned Buddha's precise production place; possible Longmen relationship of the Eastern Wei Maitreya; the sarcophagus's recarving history; unrecorded dimensions and earlier provenance. The new crowned Buddha is not added to the Yongle–Xuande topic.

The labels for loans L.2019.4.3, L.2019.4.1, L.2019.4.4 and L.2005.2.2 spell the lender John L. Hendry **III**. The torana label omits the suffix. The site follows these labels rather than silently extending one spelling to every record.

## Validation

Run `python3 scripts/build_museum.py`, the existing affected-topic checks, and `python3 scripts/check_sama_batch.py`. The latter checks all 87 public originals, actual derivative dimensions when the local archive exists, canonical IDs, source references, exclusion of deferred photographs and cross-topic links.

`python3 scripts/check_sama_browser.py` exercises all 19 new Himalayan records and their labels/lightboxes, early Buddhist readings, SAMA viewing filters, Roman and Vows timelines, and remaining topic anchors at 1440 and 390 pixels. Existing Himalayan/browser/learning and Vows atlas checks additionally cover 320/360px layouts, keyboard navigation, no-JavaScript fallbacks and future data growth. Screenshots remain in `/tmp`, outside the public site.
