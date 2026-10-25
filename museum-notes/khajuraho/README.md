# Khajuraho notebook — 2026-10-25

Source: `data/works.json`. Build with `python3 scripts/build_museum.py` (includes `build_khajuraho.py`); validate with `python3 scripts/check_khajuraho.py` and `python3 scripts/check_xiangtangshan.py`. The builder also creates `/south-asian-art/` and its homepage entrance. Existing shared photography/lightbox helpers are reused; no new runtime dependencies.

## Intake

All 16 files in `/home/qingxi/museum/印度克久拉霍` were inspected, including all labels at full resolution. The hash filenames in the attachment were not present; the actual files are `Image_20261025124215_<number>_19.jpg`. Identification is by photographed subject and label, not upload order. Every original is copied byte-for-byte, with its source filename, dimensions and SHA-256 recorded in JSON. Filename timestamps are not visit dates.

| Work | Accession | Photo / label | Attribution |
|---|---|---|---|
| Cleveland Lovers | 1982.64 | 931 / 932 | Museum: Khajuraho |
| Nelson monkey-undressed celestial woman | 81-27/26 | 933 / 934 | Label: Khajuraho region |
| Nelson dancing bracket | 40-18 | 935 / 936 | Label: Khajuraho region; ceiling bracket is a possibility |
| Nelson standing Shiva | 60-68 | 937 / 938 | Label: Khajuraho region |
| Nelson Chakreshvari | 60-82 | 939 / 940 | Label: Khajuraho region; Jain guardian |
| Seattle Uma-Maheshvara | 38.23 | 941 / 942 | Label: probably Khajuraho, retained over abbreviated web field |
| NOMA Female Figure | 94.324 | 943 / 944 | Web: Khajuraho, Chandela period 950–1310; label: MP, 11th century |
| Freer 24-Jina shrine | F1993.11 | 945 / 946 | Web: Khajuraho region; label: Khajuraho; metal shrine, not wall sculpture |

Labels 944 and 946 are naturally landscape and readable without rotation. Label 936 also discusses unrelated southern Indian columns; they are not added as works. No source supports a specific original temple for any of these eight works. Site architecture is context, not asserted provenance.

## Research and limits

All eight official object records were read, alongside the labels. Smithsonian's current direct page returned access errors; its full indexed official record (including provenance notes and the January 2023 research update) was read via search, together with the old official archive. The shrine's 1097 date and 1096 acquisition-memo date remain distinct; the old/current description's uncertain central identity is not resolved by assigning a name. The unidentified French collection claim is explicitly qualified in the museum record. No inference of illicit export is made from the conditional Indian Embassy clearance letter.

Historical sources read: UNESCO listing; ASI Khajuraho page (full HTML via local fetch); Devangana Desai, *Khajuraho* (OUP 2000), relevant sections on history, patrons, sculpture interpretation and temples via a digitized copy; MP Tourism *Discovering Madhya Pradesh*, pp. 101–103; Met's Hinduism essay; Ministry of Tourism Lakshman page. ASI's 25 surviving temples and UNESCO's approximately 20 are not harmonized without an inventory; 85 is identified as local tradition. No claim that all missing buildings were destroyed in war. Burt's 1838 account is a colonial survey milestone, with local knowledge acknowledged. ASI/Desai disagree on Kandariya patronage; only broad dating appears in the table.

The three further scholarly titles supplied in the brief (1993 exhibition, Mason article, 2016 Nelson book) were not read in full. Museum bibliographies/exhibition histories may be reported as museum records, but those publications are not cited as independently checked evidence.

## Chinese naming audit

| Draft / original | Adopted | Basis / limitation |
|---|---|---|
| 旃陀罗 / Chandella–Chandela | 昌德拉王朝 | User's explicit naming requirement; retain both English forms once |
| Khajuraho | 克久拉霍 | User's preferred form; alternate 卡久拉霍 in a note only |
| 拉克什曼那 / Lakshmana | 拉克什曼寺 | Indian Ministry of Tourism Chinese page uses 拉克什曼神庙 |
| 坎达里亚·摩诃提婆 / Kandariya Mahadeva | 坎达里亚·马哈代瓦寺 | Same institution's Chinese destination/monument pages |
| 毗湿婆那他 / Vishvanatha | 维什瓦纳特寺 | Same divine epithet's Chinese rendering in Ministry's Varanasi page; not a source for this temple's history |
| 帕尔湿婆那他 / Parshvanatha | 帕尔斯瓦那特 | Ministry's Khajuraho destination page; its group page also uses 帕斯瓦纳特 |
| Adinatha / Neminatha | 阿迪纳特 / 内米纳特 | Ministry's Chinese monument / Mount Abu pages; no claim of sole standard |
| 轮女神 / Chakreshvari | 护卫女神查克雷什瓦里（Chakreshvari） | No sufficiently established Chinese form found; explicit phonetic rendering, not invented semantic title |
| Nagara | 北印度式（Nagara） | Plain descriptive wording avoids an unnecessary disputed transliteration |
| Shiva / Parvati / Vishnu / Garuda | 湿婆 / 帕尔瓦蒂 / 毗湿奴 / 迦楼罗 | Retain familiar Chinese religious/art-history forms; English on first explanatory occurrence as useful |

Chinese Tourism pages were read in full indexed form when live requests timed out; their historical simplifications are not adopted. Lesser-known ruler names include original spelling; no claim that these are official or universally dominant Chinese translations.

## Reference photograph

`images/kandariya-mahadeva-paul-mannix.jpg`: Paul Mannix, 26 August 2000, *Khajuraho - Kandariya Mahadeo Temple*, Wikimedia Commons (originally Flickr), CC BY-SA 2.0. The Commons file page and license were checked; image inspected; original unchanged. Attribution and license are adjacent to the photograph. This is one reference image, not a Merton visit or a ninth object. All 16 personal originals remain separate.

## Validation

Eight objects, five museums, sixteen original photo/label images, one licensed site reference. Automated checks validate identifiers, exact photo hashes, qualified attribution, unique images/IDs and source anchors. Shared site check validates all local paths and anchors. Playwright tested 1440px desktop and 390px mobile: image decoding, folded labels, lightbox, zoom, Escape, footnotes/backlinks, horizontal table scroll, no page overflow and no JavaScript errors. Screenshots were inspected. No images cropped or digitally reconstructed.

## Reading order refinement, 2026-10-25

The opening now contains 264 Chinese characters (roughly 300 including names and punctuation), followed immediately by the eight-work overview and three object groups. The unchanged site photograph, detailed history, four-temple table and historical notes follow the works. Record discrepancies and a single shared attribution caveat are folded near the references; the unrelated-column label production note is removed. Source data, all photographs and citations remain. The checker also verifies reading order and that the first image is the original monkey/apsara photograph, with the site reference last. Desktop/mobile browser checks were rerun.
