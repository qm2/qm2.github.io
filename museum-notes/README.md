# Museum Notes

Static pages for the existing GitHub Pages site. No client dependencies or build service.

- `/museum-notes/`: cross-cultural notebook entrance.
- `/museum-notes/chinese-painting/`: Chinese painting and calligraphy; first batch has 13 works and 76 photographs from the Nelson-Atkins Song landscape exhibition. See [section notes](chinese-painting/README.md) for pairing, ordering and attribution. Regenerate with `python3 scripts/build_paintings.py`, then `python3 scripts/build_museum.py`.
- `/museum-notes/chinese-buddhist-art/`: Chinese Buddhist Art section, containing material entries and thematic reading.
- `/museum-notes/buddhist-sculpture/`: first collection, 36 objects seen in 14 museums (including loaned works).
- `/museum-notes/wood/`, `/lacquer/`, `/stone/`, `/bronze/`, `/mixed/` (all under `/museum-notes/`): permanent material pages, generated from the same data as the topic. The current counts are 22, 6, 4, 2, and 2. Classification follows structure and technique rather than surface color; the complete material description remains on each card.
- `buddhist-sculpture/data/objects.json`: editorial source of truth, including the exact original photo and label filenames, original museum titles, accession numbers, uncertainties and source links.
- `buddhist-sculpture/images/`: 36 object photos and 3 supplementary sutra photos, copied unchanged from the user's archive and subsequent uploads. Label photos remain in `/home/qingxi/museum/source/` and are not included in the public page.
- `../scripts/build_museum.py`: regenerate the notebook, Chinese Buddhist Art section, topic, and five material pages after editing the JSON. Run `python3 scripts/build_museum.py` from the repository root.
- `museum.css`, `museum.js`: responsive layout, filters, search, image dialog. All object content remains readable without JavaScript.

## Source notes (2026-09-20)

Original archive: `/home/qingxi/museum/中国古代佛教木雕.zip` (64 JPEGs: 33 object photos, 31 label photos). Filename dates are not treated as dates of visits. Two labels cover two objects each; objects 217/218 share label 219, and 220/221 share label 222. Labels 223/225 precede their corresponding object photos 224/226. Every input photo is accounted for in the JSON.

Titles, dates and materials follow the photographed labels unless a note states otherwise. Notes on visible appearance are editorial descriptions of the photos, not invented personal memories. A story without an online link is a paraphrase of the explicitly paired label; it is not a claim of independent online verification. No dimensions, temple origins or personal visit dates have been invented. No third-party image is used.

Online records checked for the additional provenance and conservation notes:

- Nelson-Atkins 34-10: https://art.nelson-atkins.org/objects/597/guanyin-of-the-southern-sea — C. T. Loo by 1933–1934; acquired 1934. The account of Sickman seeing disassembled pieces in snow is a later recollection; the museum flags uncertainty over the first encounter and dealer identity.
- Rijksmuseum AK-MAK-84: https://www.rijksmuseum.nl/en/collection/object/Guanyin--f0a89d281d74f34cb0df0f13a22d4e00 — Paul Houo-Ming-Tse, Edgar Worch, Otto H. Kahn and widow; acquired by the Asian Art Society 1939; museum loan 1972. Willow and paulownia.
- Met 28.56: https://www.metmuseum.org/art/collection/search/42731 — current record says multiple-woodblock construction; the photographed label uses the less precise woodblock construction.
- Cleveland 1984.70, 1980.80, 1963.581, 1981.53, 1983.86: individual records at https://www.clevelandart.org/art/{accession}. 1963.581 was verified against the record (not 1966.581).
- Princeton y1950-66: https://artmuseum.princeton.edu/art/collections/objects/23888 — Yamanaka & Co. by 1923, Mathias Komor, museum 1950; probable Ming surface decoration.
- Walters 25.9: https://art.thewalters.org/object/25.9/ — Yamanaka & Co., Henry Walters 1920, bequest 1931; twelve wood pieces, five lacquer layers.
- Walters 25.256: https://art.thewalters.org/object/25.256/ — bulked lacquer, not simply wood.
- Penn C408A: https://www.penn.museum/collections/object/179391 — purchased from C. T. Loo in 1924; label abbreviates accession C408.
- Seattle 35.17: https://art.seattleartmuseum.org/objects/11035/watermoon-guanyin — online 10th–late 13th century differs from photographed label's 12th–13th century; both noted.
- Cernuschi M.C. 6274: https://www.parismuseescollections.paris.fr/fr/musee-cernuschi/oeuvres/guanyin-assise — bronze, 16th–17th century; label 206 specifically states Don Loo Ching-Tsai, 1921.

Open editorial points, shown on the page where relevant:
- Guimet seated limestone Avalokiteshvara (photo 199): accession illegible; do not invent it. Museum identified from the Guimet labels and batch context. Photo 200 says limestone, not wood.
- Nelson-Atkins 51-42: photographed label says repair/repainting in 1348. A search result for a scholarly book's illustration list refers to a 1349 document; retain the photographed label explicitly until these are reconciled.
- Portland 38.52: museum attribution supported by label's Ella M. Hirsch Fund and matching published collection images; no online object page verified. No earlier provenance added.

Local preview: `python3 -m http.server 8765 --bind 127.0.0.1` from the repository root. This work does not itself push or publish the site.

## Additional uploads, 2026-09-20

Twelve loose JPEGs (259–270) in `/home/qingxi/museum/`:

- 259/260: Tang dry-lacquer Buddha head, Xuzhou Collection, displayed at MFA Houston. Collection ownership distinguished from display location. Museum exhibition source: https://www.mfah.org/art/exhibitions/buddhanature . Supporting caption in the museum magazine credits: https://static.mfah.com/documents/spring-2026-h-mag---for-the-apparel-oft-proclaims-the-man.17146491522394815155.pdf .
- 263/264: Jin wood Guanyin, New Orleans Museum of Art, 85.209. Story about the 1985 examination and two cavities follows label 264. Museum attribution also corroborated by Shih-shan Susan Huang, “Reassessing Printed Buddhist Frontispieces from Xi Xia” (2014), color plate 12 and figs. 25–28: https://shihshansusanhuang.com/wp-content/uploads/2022/09/2014_Susan-Huang_Reassessing-Printed-Buddhist-Frontispieces-from-Xi-Xiacompress.pdf .
- 265/266: Met 19.186, dry-lacquer Buddha, probably Amitabha: https://www.metmuseum.org/art/collection/search/42163 .
- 267/268: Heaven Ascending Sutra, 1155, 85.209.4; label explicitly identifies it as found inside the Guanyin. 269/270 show frontispiece and dedication details. These three images appear within object-263's notes, without increasing the sculpture count. Filename 262 is another overview of the same sutra; retained as an alternate, not published twice. Transcription/date follow photographed label 268 (1155) and visible 贞元三年, not the earlier provisional reading.
- 261: label for Northern Qi sandstone Buddhist Votive Stele, 2014.39. User confirmed this was an accidental upload. Recorded as excluded in `data/intake.json`; no outstanding photo request. Original file retained.

Original filenames and image dimensions are kept in JSON. To add work: copy the object photo to `images/`, add a record with photo/label mapping and dimensions, and regenerate. Counts, museum options and material pages update from the data. A `related_photos` list supports supplementary photos with their own captions and source mappings.

## Preview from a remote SSH workspace

Start the server on the remote machine in the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

On the browser's **local** computer, open an SSH tunnel using the same host or alias normally used to connect:

```sh
ssh -N -L 8765:127.0.0.1:8765 USER@HOST
```

Leave that terminal open and browse to `http://localhost:8765/museum-notes/`. VS Code Remote users can instead forward port 8765 in the Ports panel. If local 8765 is occupied, use `8766:127.0.0.1:8765` and browse to local port 8766. The preview is bound to loopback; it does not publish the website.

Expanded object-263 notes cover the sutra title, dated dedication, distinction between print and sculpture dates, Dizang frontispiece, and visible donor wishes. Label and user photographs supply the basic information; iconographic interpretation cites Huang (2014), p. 153, figs. 27–28. The paper lists 82.209.4 in its figure list, whereas the photographed museum label reads 85.209.4; the page follows the label and discloses the discrepancy. No full transcription is claimed.

## Editorial hierarchy and personal notes

The notebook home `/museum-notes/` is the cross-cultural entrance. `/museum-notes/chinese-buddhist-art/` is the parent section for the current objects, material pages and the 自在之姿 topic. Existing object, image and category URLs remain valid; breadcrumbs and return links expose the parent section. Future sections are listed in `sections.json`, as non-clickable plans until content exists. Gandhara/Mathura and Caravaggio are potential topics, not enforced peers of every cultural section. Additional topics should reference shared object records rather than duplicate editorial data.

Objects may optionally contain a `personal_notes` list. Each item requires `kind` (`visit_memory`, `photo_reflection`, or `onsite`) and `text`; `written_on` is an optional actual writing date, never an inferred visit date. Notes render under “我的观看” separately from visual descriptions and scholarly notes, on all pages featuring the object. Empty or missing notes produce no placeholder. No personal recollections have been authored on the user's behalf. Preserve uncertainty in the user's own wording, and distinguish current impressions from memories of the original visit.

## Writing and image budget

User preference: keep Chinese prose conversational and close to the user's own wording. Avoid generic lyrical introductions, formulaic conclusions and inflated descriptions. Personal impressions must come from the user; preserve short, incomplete memories without filling in invented experiences. Factual notes remain precise and sourced.

As of this first publication, the 39 JPEGs total 9,676,342 bytes; all website files total approximately 12.1 MB. Keep original archives and future full-resolution camera files outside this repository. Prefer web-sized copies for new uploads; avoid repeatedly replacing large binaries, since Git keeps their history. Review image hosting/compression as the site grows into hundreds of MB. GitHub Pages currently limits published sites to 1 GB: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits .

Museum pages use the public name Merton in headings, metadata, photography credits and copyright notices. The academic homepage keeps its existing name.

## Chinese painting batch, 2026-09-21

The new batch adds approximately 19.5 MB of unchanged JPEGs. Total website content is approximately 32 MB, excluding Git history. The 99-photo ZIP and extracted originals remain outside the repository; only 76 selected artwork photographs are published. Five era groups contain 1 Five Dynasties, 4 Northern Song, 1 Jin, 6 Southern Song and 1 Yuan work. Labels, repeated views and gallery context are accounted for in the section intake manifest.
