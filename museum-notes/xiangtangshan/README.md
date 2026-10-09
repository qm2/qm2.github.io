# Xiangtangshan: overseas encounters

This topic follows the supplied `xiangtangshan-organized.zip` and its `codex-prompt.md`.
The unchanged ZIP and 45 originals remain outside Git at `/home/qingxi/museum/xiangtangshan-organized`.

## Editing and generation

- `data/works.json`: edited public text, original titles, accessions, attribution limits, named sources, photo relations, 45-file intake manifest including original SHA256 hashes. 24 attributed works + 1 separately disputed Cernuschi Buddha. No visit dates inferred from filenames.
- `images/`, `thumbs/`: 43 shared derived JPEGs in each size; EXIF orientation applied, no cropping/restoration. Long edge capped at 1800/600 pixels, quality 88/80. Original photos are preserved locally and in the ZIP. A shared group photo is stored once, regardless of how many work records reference it.
- `../../scripts/build_xiangtangshan.py` (from repository root: `scripts/build_xiangtangshan.py`): index, 25 work pages and 4 comparison groups on one comparison page. Uses existing notebook base styles and lightbox markup, with a topic-local `xiangtangshan.js` for crop-aware views and filters. The shared Caravaggio script is not loaded on this topic and is unchanged.
- Run `python3 scripts/build_museum.py` from the repository root. It calls this builder after the existing builders and refreshes the Buddhist Art entrance, notebook summary and external-topic metadata. No frontend dependency or new build service.
- Optional image regeneration: `python3 scripts/prepare_xiangtangshan_images.py /home/qingxi/museum/xiangtangshan-organized` (Pillow).
- Data/link check: `python3 scripts/check_xiangtangshan.py /home/qingxi/museum/xiangtangshan-organized`.

The original 35 selected sculptures plus these 24 give **59 selected sculptures, plus one disputed work**, counted across five topics. The six older archived works remain in the legacy archive; this is not a count of every historical archive entry. Penn C66A/B (photos 741/742) is excluded from Xiangtangshan and linked to the existing `/museum-notes/yixian-luohan/#object-741`; photo 741's hash matches the existing published original. It does not add another work or another page here.

## Intake and grouping

North site: North Cave 8, Middle Cave 1, South Cave 3. South site: Cave 2 has 6, range-attributed other caves 4. Two further works retain unresolved original caves (Met 14.50 is specifically southern; Nelson 53-48 has no north/south determination). Cernuschi M.C.8763 remains outside the 24.

- 724 is a shared label: Cleveland 1923.97 above, 1972.166 below.
- 727 shows two reliefs and the independent F1968.45 between them. 728/748 are shared labels. 747 belongs only to F1921.2.
- 734: left F1977.8, right F1953.86. 735: left F1953.87, right F1977.9. Identifications follow the supplied image-to-record matching, not relative-position language on the group label.
- 739: left Penn C113, center C151, right C150; shared label 740.
- 714/718 and 715/719 repeat the Nelson guardian; preferred 714/715. 733/745 repeat the seated Freer bodhisattva; preferred 733, label 746. Alternate images remain mapped but are not repeated as works.
- 741/742 reuse the existing Penn luohan. All 45 originals are in the manifest, including backups and excluded images.

## Research and retained discrepancies

Museum records and Xiangtangshan project pages linked beside each work are the core sources. Background uses the project's introduction and cave pages. ISAW's exhibit identifies the Nelson beast's original wall-niche base. Online records were revisited during this implementation; Met's browser-readable pages were available despite HTTP 429 responses to scripted requests. No claim is made to have read the full 2010 exhibition book or the 2014 petrography paper.

- Cernuschi: label and date field Northern Qi; museum prose argues Liao archaism. Separate disputed entry, no final redating claimed.
- Freer F1913.134: structured fields/project/label point to Northern Qi, northern South Cave; the museum's older Label text still proposes Tang Longmen. Public note retains both.
- F1977.8: Geography/Provenance and project use northern North Cave; Label says Cave 7. No conversion to southern Cave 7.
- F1916.346a-b: full accession retained; label range 3–7, project 3–6, current museum field 4–6. Main record follows the latter, with adjacent note.
- Penn C113/C151: different dimension sets on museum/project records; dimensions omitted. Current display is not evidence for an intact original triad. C150 remains generically a bodhisattva; possible Dashizhi identity is attributed to research.
- Portland 51.255: **corrected supplied approximate 550 date to 560 CE**, clearly legible on original photo 744. Donation wording follows that label. No separate official museum object URL was established; project entry and photographed label are provided.
- Cleveland Kashyapa: label Northern Qi 550–577; website c.550, both retained.
- Nelson beast: label Northern Qi 550–577; ISAW narrows to 550–559.
- Met 57.176 donor credit corrected to **Mr. and Mrs. Albert Roothbert** after checking the Met record.

Mechanical build checks and browser checks cover counts, shared-image positions, internal URLs/anchors, image decoding, all 25 detail pages, the index and comparison page at 360/1440 pixels, expanded labels, zoom/navigation, museum/cave/search filters and JavaScript-disabled reading. Existing four sculpture topics keep their 12/13/8/5 work counts.


## Display crops and reading revision

Eight `display_crop` rectangles are normalized to the original composition and stored once on their work records. `hero` continues to reference the existing shared asset. Cards, detail hero images, comparison images and lightbox views all use this mapping; the JPEGs and source thumbnails are unchanged. The CSS viewport has the rectangle's natural aspect ratio; it is not a uniform `object-fit: cover` crop.

| Work | Photo | Original group position | x, y, width, height |
|---|---:|---|---|
| F1977.8 | 734 | left | .055, .130, .385, .730 |
| F1953.86 | 734 | right | .510, .105, .450, .855 |
| F1953.87 | 735 | raised-hand figure, left | .045, .065, .465, .875 |
| F1977.9 | 735 | right | .570, .150, .330, .710 |
| C113 | 739 | left | .040, .090, .245, .850 |
| C151 | 739 | center | .435, .170, .180, .770 |
| C150 | 739 | right; source already cuts off part of the figure | .780, .055, .220, .905 |
| F1968.45 | 727 | independent standing bodhisattva, center | .390, .005, .220, .990 |

Each of these detail pages has a “查看完整合照” link and the unchanged full group photograph in its context gallery. The guardian comparison shows six individual views; complete 734/735 images occur once each in its secondary gallery. Cave 2 presents the two reliefs uncut, F1968.45 as a crop, and the complete Penn 739 once with three linked identities. Shared labels 724/740/746 remain available with explicit shared captions. Alternate photos are still intake assets rather than additional works.

`xiangtangshan.js` uses work + view IDs, not URL deduplication. A crop links to its full view within the same work. The homepage cover has its own group. The lightbox computes the same normalized rectangle for both fitted and zoomed views; keyboard navigation, Escape and focus return remain supported. No shared gallery JS/CSS was modified. Styles are scoped under `.xts-page`.

Copy was reviewed across all 25 records. In particular, Met 30.81 is **52.1 cm high**, the transport and repair account gives March 29, 1921 and November 1922, and F1977.8 distinguishes transfer to the study collection in 1973 from permanent accession in 1977. Original-cave disagreements remain in adjacent “资料说明” disclosures; the Ananda comparison also has a visible attribution note. Portland remains 560 CE. All prior museum and research-project sources remain linked.

Browser regression command (optional Playwright dependency):

```sh
python3 scripts/check_xiangtangshan_browser.py
```

This checks all 27 topic pages at 360 and 1440 pixels, rendered crop geometry at both sizes, all eight lightbox targets, zoom/full-view switches, keyboard and focus, shared-label views, museum/cave/search filters, empty/reset behavior, cover isolation, no-JavaScript reading, and five other gallery lightboxes. Screenshots of all eight actual hero crops, the raised-hand figure in the mobile lightbox, the home cards and comparison groups were visually inspected. The main build is also checked for repeatability and the 45-file original intake for unchanged hashes.
