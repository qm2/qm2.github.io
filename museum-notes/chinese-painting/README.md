# Chinese painting and calligraphy

Current collection: 32 works, 150 published photographs from four museums. The two source batches contain 197 files, fully accounted for in `intake.json` and `intake-2.json`.

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


## Second batch and cover review, 2026-09-21

`中国宋元书画2.zip` contains 98 images: 74 published artwork photographs, 19 labels and five excluded alternate/context views (372, 378, 389, 394, 419). Extracted originals remain in `/home/qingxi/museum/song-yuan-source-2/`. Every input is accounted for by SHA-256 and role in `data/intake-2.json`.

The collection now has 18 general painting works, seven Dunhuang paintings, five temple murals and two Buddhist hanging scrolls. All works have one canonical page under `chinese-painting/`; since the September 22 editorial revision, the main chronological index shows the 18 general painting works only. `/museum-notes/buddhist-painting/` references 14 works, and `/museum-notes/dunhuang-painting/` references seven of those. The Chinese Buddhist Art entrance links to both topics. Images and editorial records are not duplicated between topics.

Covers are manually reviewed, with rationale in `cover_reason`. Li Cheng photo 310 replaces Xia Gui on both the notebook entrance and the painting index. Jiang Shen changes from 300 (central glass seam) to 299 (mountains and shoreline); Taigu Yimin from 318 to 315; Xu Daoning from cabinet view 359 to detail 360; Xia Gui from 347 to 349. Qiao Zhongchang 280 and attributed Ma Yuan 332 remain the best available representative details. Single-image works remain limited by the photographed view. No image generation, retouching, reconstruction or file cropping was applied; new sideways detail views are turned with CSS.

### New photo groups

- 373–379 / label 380: Tejaprabha mural, Nelson-Atkins 32-91/1. Keep 379 as gallery context showing a separate sculpture in front. 378 omitted as repeat.
- 381/382, 383/384, 385/386: Cisheng monastery Ruyilun Guanyin, incense-burning bodhisattvas, and earlier Guanyin revealed beneath the latter. Labels distinguish 951–953 upper layer from 937 lower layer. Both 50-64A and B were gifts of C. T. Loo.
- 387–405 / label 399: Freer F1914.53, Nymph of the Luo River. Right-to-left sequence 388,390,391,392,393,395,396,398,397; details 400–405 separately. 389/394 are alternate overlapping views. Southern Song copy following an earlier composition, never presented as a Gu Kaizhi autograph.
- 406–413 and 433–438 / label 412: Freer F1954.21, Tilling Rice. Order of photographed opening scenes is 407,410,408,409,411 (soaking, plowing, raking, harrowing, rolling). The photographs cover the displayed opening portion and details, not all 21 scenes. Attribution follows online “Attributed to Cheng Qi”, with direct label attribution disclosed.
- 414–432 / label 418: Freer F1954.20, Silk Weaving. Opening sequence 415,416,417; overall 414 and photographed details/texts retained separately; 419 omitted as oblique alternate. Do not claim full coverage of all 24 scenes. Photos 420–425,431–432 turn -90 degrees in CSS; text photos 426–430 remain upright.
- 439/440: Freer F1916.521, Luohan Holding a Fly Whisk, Yuan to early Ming; reject obsolete Wu Daozi attribution, disclose substantial glare.
- 441–445: Kimbell AP 1987.03, Arhat Taming the Dragon; main painting 442, details 443/444, mounting 441. Cover 443 is explicitly a detail.
- 446/447: Kimbell AP 2002.02, Bamboo and Rocks; attribution remains the label spelling Tan Zhirui until Chinese name characters are securely established. ca. 1275 and museum Yuan classification both retained. This is bamboo painting, not a devotional icon despite the Buddhist inscription.
- 448–453 / label 453: Freer F1938.4, Gong Kai, Zhongshan Going on Excursion. Sequence 448,449,450; rotated detail 451 and colophon 452 separately. Zhong Kui is not classified as Buddhist painting.
- 454/455: Freer F1935.11, Dunhuang Ksitigarbha; early 11th / late 10th century uncertainty follows label. Patron and unfinished-state explanations attributed to the label, not facts invented from the photograph.
- 456/457: Guimet MA 5020, Akasagarbha mural, Henan, Five Dynasties; French national inventory gives 952. Kept out of Dunhuang.
- 458/459: Guimet MG 17798, Shakyamuni preaching, hemp; 460/461: EO 1143, life-prolonging Avalokiteshvara, silk with gold; 462/463: EO 1135, Maitreya Pure Land, dated 940; 464/465: MG 17688, double-sided bodhisattva banner, hemp, only one side photographed; 466/467: EO 1399 120, monastic-robed bodhisattva banner, silk; 468/469: EO 1129, willow Guanyin banner, hemp. These six Dunhuang works follow the photographed French labels, including Pelliot expedition provenance and dating uncertainty. They are portable cloth paintings, not detached cave-wall murals.

New notes are short paraphrases of photographed labels and linked primary records. Where an individual online record has not been verified, the page cites the photographed label rather than presenting a generic URL as a verified object source. Original labels are retained locally, not published in galleries. All sources are recorded in `works.json`.


## Editorial reduction and comparison groups, 2026-09-22

The Chinese painting entrance and homepage count now include only 18 works with `unit: scrolls`. The 14 Buddhist paintings remain in the Buddhist/Dunhuang indexes; all 32 canonical URLs and images are unchanged. Buddhist breadcrumbs and return links lead to their actual topic instead of empty or unrelated chronological anchors. The main index exposes only its five populated eras. Buddhist cross-links are quieter links after the main collection.

`tags` support overlapping editorial browsing: landscape, figure/narrative and literati painting on the main index; Dunhuang, murals, arhat and Buddha/bodhisattva images on the Buddhist index. These are viewing lenses rather than mutually exclusive historical classifications. No independent calligraphy works exist yet, so calligraphy is a non-clickable pending category. Filters hide empty period groups and update visible counts; without JavaScript all collection cards remain visible.

`comparison_groups` define three reciprocal reading groups with explicit comparison reasons: northern monumental landscapes (Li Cheng, attributed Jing Hao, Winter Mountains, Taigu Yimin); text-to-image (Qiao Zhongchang, Li Song, Luo River); Southern Song landscape unfolding (Xia Gui, attributed Ma Yuan, Jiang Shen). Links are generated for every member. Other existing object relationships (Cisheng layered murals and paired tilling/weaving scrolls) remain intact.

At the user's explicit editorial direction, Bamboo and Rocks now displays `传 檀芝瑞`. `artist_en: Attributed to Tan Zhirui` preserves the museum's spelling in the detail record. This change does not claim new independent verification of the Chinese spelling or remove the attribution qualifier.
