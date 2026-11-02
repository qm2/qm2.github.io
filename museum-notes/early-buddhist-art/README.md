# 早期佛教艺术

A photograph-led South Asian Buddhist art notebook at `/museum-notes/early-buddhist-art/`, built from the user's v2 handoff. Five chapters and 18 reading pages cover roughly the second century BCE to the late sixth century CE, including late Gandharan clay/stucco and Gupta-period sculpture. The final dated object is CMA1968.40 (591). No Pala/late Himalayan objects are added.

## Build and data

```sh
python3 scripts/build_early_buddhist.py
python3 scripts/check_early_buddhist.py
# Full site build calls this builder after Homer and Khajuraho:
python3 scripts/build_museum.py
```

- `data/works.json`:72 canonical object records, independent of photo counts. Canonical facts feed the catalogue, map and readings. Date ranges are filter envelopes, not newly asserted exact dates. Unknown dimensions/collection fields remain null.
- `data/readings.json`:18 original Chinese readings (roughly370–470 characters each), specific comparisons, source identifiers and selected photographs. Chapters are editorial reading groups, not an assertion that styles replaced each other in that sequence.
- `data/photos.json`:151 supplied original filenames, asset IDs and SHA-256 values. The complete immutable input remains at `/home/qingxi/museum/early-buddhist-handoff/early_buddhist_art/`; the original ZIP also remains. Only137 photographs used as object/alternate views or label evidence are copied into `images/originals/`. Excluded photographs and contact sheets are not published.
- `data/crops.json`:six explicitly identified single-object crops from two shared photographs, plus two detail crops of the Gummadidurru slab. No colours, reflections or missing parts are altered. The complete photographs remain available. Source boxes and pixel sizes are retained in `derivatives.json`.
- `images/`:400/900/1600-width responsive WebP files capped at native width; a native-resolution WebP viewer image; unchanged source JPEGs for rebuilds. Label1418's display is rotated90°; its original is unchanged.
- `data/map.json`:ancient reference points, broad regions, museum-city references and three intersecting period filters. Broad regions retain null coordinates and separate editorial label positions. Missing coordinates do not become0,0. The local Natural Earth land geometry is reused from Homer; no map service, key or runtime network request is needed.
- `data/sources.json`:read object records/research linked from the page. Every work also retains its photographed label. Search-only or unsuccessful research is not promoted into a read bibliography. Original English titles are label transcriptions unless an `official_title` is also supplied.
- Scoped CSS/JS reuse Museum Notes typography, navigation and the existing Caravaggio lightbox. No framework/dependency or unrelated design change.

The focused builder writes marker-controlled entrances in the Museum Notes home and South Asian Art index. A full build reproduces them. HTML is generated; edit data/the builder rather than generated pages.

## Chinese naming audit, 2026-11-02

Reviewed before publication at the user's request. The handoff's “佛陀的形象与故事” was an editorial title, not a fixed scholarly term. The public title now uses “早期佛教艺术”, attested in the Palace Museum's [《犍陀罗艺术引介》, p.30](https://www.dpm.org.cn/Uploads/File/2023/05/08/u6458b201c3473.pdf) and the [Tsz Shan Museum's Chinese object description](https://www.tszshanmuseum.org/cn/collection/item/釋迦牟尼佛說法浮雕/2). The subtitle and introduction continue to delimit this notebook's period; this does not assert a universally fixed periodization or a measured most-frequent name.

| Existing name | Original | Decision | Read Chinese source / limit |
| --- | --- | --- | --- |
| 马图拉 | Mathura | Keep; add 秣菟罗 as an alternative and search term | [Fudan lecture introduction](https://clcrr.fudan.edu.cn/Data/View/214); Cheng Jincheng, [《丝绸之路艺术史纲（下）》, 2022, p.23](https://dflt.qdu.edu.cn/__local/5/13/81/653A67520AC2ED8DDBD5465361F_5065BE5C_16AF65.pdf) explicitly pairs both forms. |
| 鹿野苑 | Sarnath | Keep; add 萨尔纳特 as an alternative and search term | Same Fudan introduction and Cheng article. |
| 巴尔胡特 | Bharhut | Keep | [Fudan:《早期印度佛塔象征含义研究》 lecture report](https://clcrr.fudan.edu.cn/Data/View/260). |
| 阿马拉瓦蒂 | Amaravati / Amaravathi | Keep; 阿玛拉瓦蒂 retained as a searchable variant | [British Museum Chinese Room 33a](https://britishmuseum.org.cn/G_33a.html) and the Fudan report use 阿马拉瓦蒂; the Palace Museum article uses 阿玛拉瓦蒂. No need to invent or impose an archaic alternative. |
| 龙树山 | Nagarjunakonda | Keep, with original in the map | Palace Museum article, p.30 explicitly pairs 龙树山 with Nāgārjunakoṇḍa. |
| 犍陀罗 | Gandhara | Keep | Palace Museum article; Fudan introduction; Guimet Chinese collection page. |
| 哈达 | Hadda | Keep | [Guimet: 持花精灵](https://www.guimet.fr/zh-hans/nos-collections/afghanistan-pakistan/le-genie-aux-fleurs). |
| Tapa-Kalan | Tapa-Kalan | 塔帕—卡兰（Tapa-Kalan） in contextual fields | Same Guimet page uses 塔帕-卡兰. Original titles, filenames and excavation codes unchanged. |
| 塔赫特巴希 | Takht-i-Bahi | 塔克特依巴依; old form remains a search alias | [UNESCO Chinese heritage entry](https://whc.unesco.org/zh/list/140). This follows a named authority, not a claim that other transliterations are incorrect. |
| 沙巴兹加里 | Shahbaz Garhi | Use original Shahbaz Garhi | Chinese transliterations vary; no sufficiently strong basis found to call the existing form the prevalent scholarly name. [Guimet's object record](https://www.guimet.fr/fr/nos-collections/afghanistan-pakistan/bodhisattva-debout) supplies the original spelling and Mekhasanda relationship. |
| Gummadidurru; Mekhasanda; Dhanesar Khera | Same | Keep originals | No stable Chinese forms established in this review; do not manufacture transliterations. These remain separate places, not aliases for better-known nearby sites. |
| 安得拉地区 | Andhra | Keep | British Museum Chinese page uses 安得拉邦 for the present state. This notebook retains 地区 to describe the regional grouping without asserting ancient administrative boundaries. |
| 北印度 | Northern India | Keep | Descriptive broad region, not an ancient city or exact findspot. |

Only naming evidence was taken from the newly consulted Chinese sources; their other historical interpretations were not automatically imported. Public naming notes are folded into the existing final reference section. Source English titles, source photographs, identifiers, dates, coordinates and attributions remain unchanged.

## Identity and evidence review,2026-11-02

All supplied contact sheets and the local REVIEW.html were inspected, followed by full-size priority photographs/labels and official object records. Material/collection labels are retained even where another nearby work differs.

Important corrections to the intake:

- CMA standing bodhisattva1376 is1965.476, not1965.477.
- Freer Mathura torso1417 isF1994.17, confirmed by the rotated label and official record. F1980.17 is an unrelated Japanese vase and is not used.
- Nelson copper Buddha1451 is44-13, not44-11. Its Dhanesar Khera record is distinct from the591 bronze.
- Walters preaching Buddha1405 is25.266, not25.246 (an unrelated Devi).
- Nelson Maitreya1442 is35-32; Indra fragment1446's label readsF99-2.
- CMA1381 is the separately photographed Maitreya1969.61. The shared label's “Right” refers to this statue. Photo1382 instead shows three Buddhist-stupa friezes: top1930.328.1, middle1930.328.3, bottom1930.328.2. Official photographs were viewed privately to confirm correspondence; none were added to the site. The intake's mistaken assignment of Maitreya to the third strip has been removed.
- Met1979.6:photos1343/1464 merged. Second viewing location not inferred from file order. Nelson45-15:1436/N03 merged; N03 selected, both views preserved. Nelson39-19 and CMA1943.278 remain distinct objects.
- Four great events individually registered, with confirmed set accessionF1949.9a–d. No guessed suffixes or group-width-as-individual-size. A pair of hands37-31/16 remains one museum record.
- Year5 triad:private loan to the Met, label235 versus2023 study's232 retained. Its pre1973 origin is unknown. No Peshawar site is claimed as an excavated provenance.
- Gummadidurru49-29 has a documented excavation record; it is not assigned to Amaravati. CMA1985.31 is only broadly Gandharan, not a known Hadda find.591 bronze production in northern India remains separate from the Nepalese nun's place of origin.

## Scope exclusions and remaining gaps

Not published:7–8c Kabul Maitreya1347/48 (after endpoint), Surya1438/39 and painting1453 (outside subject). Atlas1337, pillar1374, gateway1384, naga1386 and lion1387 remain archived:their specific Buddhist architectural context was not established in this review. Musicians1379 and the three1930.328 friezes are included on the museum's Buddhist architectural interpretation.

Label-backed records1401 (57.003.8) and1454 (2005.184) retain unknown collection/display institutions rather than guessing from adjacent photos. Robert Gottschall's1462 is identified as private collection; display institution remains unknown. These remain accessible in the catalogue and modern map's “地点未详” list. Portland59.14 is label-backed; a directly readable current official object page is still lacking. Hadda TK121's precise restoration/reconstruction boundaries have not been established. Four-events individual accession suffixes and some dimensions remain unconfirmed.

The package's sources were leads, not automatically accepted facts. Current CMA records replace earlier label date ranges only with an explicit note. A precise131/132 conversion for the Kimbell Buddha is not asserted; the photographed label and broad early-second-century date are retained. No unknown maker, temple, excavation, visit date or emotional experience is invented.

## Verification and updates

Static checks verify original hashes, single-object IDs, merged rephotographs, separate shared-frame subjects, group accessions, exclusions, ancient/modern relations, dimensions of image derivatives,18 readings,19 pages and every local link/fragment. Chromium checks cover1440px and390px, light/dark, both map layers, Mathura across periods, Andhra subnodes, private loans, catalogue search/filters, anchor reopening, image load/zoom/close and no-JavaScript fallback. Browser screenshots and reference images remain in `/tmp`, outside the repo.

For a future photograph, append its immutable filename/asset ID/hash to the photo manifest and attach it to an existing object where appropriate. For new research, revise the object record and source entry, then rebuild. Do not create a second catalogue object for a new angle. Additional crops must have explicit source boxes and be captioned as crops.
