# Chinese painting and calligraphy

First batch: 13 works photographed by Merton at the Nelson-Atkins exhibition *Legendary Landscapes: Sublime Visions from China’s Song Dynasty*. Exhibition dates verified against the museum site (2026-03-21 to 2026-09-27); these are not inferred visit dates.

## Editing and regeneration

- `data/works.json`: reviewed titles, label mapping, original filenames, dimensions, display orientation, ordered sequences, supplements, notes, accession and primary-source URLs.
- `data/intake.json`: all 99 photographs accounted for individually (76 published object images, 13 labels retained as sources, 8 alternate/repeated photographs, 2 gallery environment photographs). Original archive and extracted files remain outside Git at `/home/qingxi/museum/`.
- `images/`: exact copies of the selected photographs. No resampling, cropping, reconstruction or color alteration. CSS rotates photographs 273–282 by -90 degrees for reading; original files remain untouched. Intake SHA-256 hashes allow copy verification.
- `../../scripts/build_paintings.py`: builds section index and 13 work pages from JSON using the standard library. Run `python3 scripts/build_paintings.py` followed by `python3 scripts/build_museum.py` to update the notebook entrance too.
- `painting.js`: progressive enhancement for ordered photographs, thumbnails, expand-all and magnification. With JavaScript disabled, all photos and captions remain visible, and links open original images.

The five era groups are editorial navigation, not a strictly consecutive timeline: Jin and Southern Song overlap. The first batch contains paintings and their accompanying colophons, not independent calligraphy works. Six works are offered as starting points; every identified work is accessible in the era sections.

## Image pairing and ordering

- Qiao Zhongchang: 273–292, label 293, overall 365. Sequence from right to left checked against overlapping banks, houses, rocks, trees and passages of the Red Cliff text. 286/291/292 omitted as alternate overlapping views of already represented passages/colophons. Retain 282 despite the cabinet support obstruction because it contains distinct trees. 290 is a colophon, captioned as such and placed in supplements.
- Attributed Jing Hao: 294, label 295.
- Jiang Shen: 296–303, label 304, overall 366. Partial overlap between 296/297 is needed to preserve right margin and inscription coverage. End at left mounting border in 303.
- Temple Hidden Among Lofty Cliffs: 305, label 306.
- Li Song: 308 shows the painting, 307 shows the mounting, label 309.
- Attributed Li Cheng: 310 painting, 311 mounting, label 312. 369 is a more oblique repeat of 311.
- Taigu Yimin: 313–324, label 325, overall 367. Start at right edge with imperial seals and end at left mounting border. Preserve overlapping sections rather than deleting parts as duplicates.
- Attributed Ma Yuan: 326–333, 335; label 336; overall 368. 334 replaced by 335, which includes the left mounting border. Sequence checked against full-view photo 368.
- Winter Ferry: 337, label 338. Gazing at a Waterfall: 339, label 340.
- Xia Gui: 341,343–350; label 354; supplements 364 and colophons 351–353. Full-view 364 and the four titled views establish right-to-left order. 342 is a near-repeat of first view; 355/356 are less frontal cabinet overviews. Four surviving scenes are not a failure of photographic coverage.
- Winter Mountains: 357, label 358.
- Xu Daoning: overall 359, detail photographs 360–362, label 363. The three details do not cover the entire scroll and are explicitly presented as selected details rather than a seamless, complete close-up sequence.
- 370/371: gallery context, retained locally, not published.

## Attribution and sources

All 13 records link to the museum's object records. Basic details follow the photographed labels unless a difference is explicitly explained. In particular:

- Jing Hao: label Chinese heading says Five Dynasties and attributed; English expands to Five Dynasties–Song; online record is narrower. Retain attribution and wider label date.
- Ma Yuan: label gives artist directly, online record says “Attributed to”; use 传马远 and disclose both.
- Jiang Shen: label ink and light color, online medium shortened to ink. Retain label wording.
- Temple Hidden Among Lofty Cliffs: label late Southern Song / 1200s, online date mid-13th century; retain both. Do not retain obsolete attribution or guess the artist.
- Xia Gui: only four of the original twelve scenes survive, per label and museum. Scene inscriptions attributed to Empress Xie; no unqualified handwriting claim. Photo captions follow visible titles. 1932 Roberts/Warner acquisition note follows museum provenance.
- Gazing at a Waterfall: number 2007.7 is not treated as a donation date; online provenance explicitly dates Ellsworth's gift to 1970.

Personal voice remains Merton. Notes describe visible details and paraphrase labels/linked museum research; no visit feelings, memories, exact visit dates or names of companions are invented. Original labels are not shown in the public image galleries.
