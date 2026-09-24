# Leonardo / European painting

Personal photo notebook, signed Merton. Editorial data: `data/works.json`.

## Rebuild

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_leonardo.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_museum.py
```

The first command builds the artist index, 11 work pages, four comparison groups, and the European painting directory. `scripts/build_european.py` owns the shared directory; rebuilding either artist retains both topics. Presentation reuses `../caravaggio/caravaggio.css` and `caravaggio.js`. No network, package install or image processing is needed to rebuild.

## Photo intake

`达芬奇.zip` contains 23 JPEGs, numbered 523–545. Originals and label photographs stay outside the repository. The manifest records every source file, SHA-256, role and associated work.

- 11 artwork images, one per work.
- 1 context image: 545, Mona Lisa in its display setting.
- 10 privately retained label images.
- 1 privately retained alternate: 543, another view of Mona Lisa. The closer 544 is the main image.
- All 12 published JPEGs are unchanged copies. Frames, reflections and viewing angles remain; CSS uses contain sizing. No AI alteration, crop or invented reconstruction.
- Filename timestamps are not treated as visit dates.

## Attribution and editorial decisions

The 11-work total includes nine works attributed by the museums to Leonardo, one Verrocchio/Leonardo collaboration (*Baptism*), and one Leonardo-workshop painting attributed to Francesco Melzi (*John*, later altered into *Bacchus*). The latter two are visibly identified on cards, detail pages and the comparison page. The notebook is not a complete catalogue of Leonardo's paintings.

Chronological groups are browsing aids. In particular, the overlapping dates of the late paintings do not establish an exact sequence. Stories are concise paraphrases of linked museum records; visible details are reading prompts rather than invented personal memories. No third-party artwork images are republished. The reverse of *Ginevra* and the London *Virgin of the Rocks* are not counted as photographed works.

Variants retained explicitly:

- Paris *Virgin of the Rocks*: label c.1483–1490; current Louvre catalogue 1483–1494.
- Workshop *John/Bacchus*: label c.1510–1520; online catalogue 1517–1520. The subject's later transformation is distinguished from original authorship.
- *Annunciation*: label c.1472–1475, Inventory 1890 n.1416; website c.1472, n.1618. Both inventory readings retained without claiming a correction.
- *Adoration*: label c.1481–1482, Inventory 1890 n.479; website c.1482, n.1594. Both inventory readings retained.
- *Baptism*: label c.1475; website 1470–1475. Vasari's teacher/student anecdote is explicitly treated as an anecdote.
- *Jerome*: the Vatican distinguishes the traditional two-part rediscovery story from the actual five-piece division of the panel.
- *Mona Lisa*: no label supplied; identification, date, support and inventory number checked against the Louvre catalogue.

Validation includes every local link and fragment, original-image hashes, attribution counts, reciprocal comparison links, every detail page, search/filter combinations, keyboard and focus behavior of the shared lightbox, four responsive widths and no-JavaScript navigation.
