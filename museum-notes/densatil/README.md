# 丹萨替寺造像 / Densatil

One complete reading page at `densatil/`, under the existing Chinese Buddhist Art entrance. Editorial source: `data/works.json`; intake: `data/intake.json`; generator: `scripts/build_densatil.py`, invoked by `scripts/build_museum.py`. Shared `build_paintings.picture/frame`, fonts, colors, lightbox and no-JS image links are reused. No new dependencies or third-party image assets.

## Identity and photo audit

- 774 artwork / 775 label: Michael C. Carlos Museum, **2001.019.001**, Palden Lhamo (label short form 2001.19.1).
- 776 cabinet photograph / **fdb9f37d9ba696ab47baa46b39d0ffaf.jpg** label: Cleveland **2011.144**, Supports with Addorsed Figures; subrecords **2011.144.1–2** form one paired group. The user explicitly corrected the initial identification. Central portrait 1993.160 is contextual only, not a fourth record. Its identity and founder relationship are mentioned at the user's request; no ancient adjacency or curatorial intention is inferred.
- 778 artwork / 779 label: Seattle **70.2**, Vashya-Vajravarahi.
- 777 is the neighboring portrait's label and is excluded from publishing, but its original hash is retained in intake.

Seven input photos, six published originals, three work groups / four physical objects. No filename date is used as a visit date. Original bytes are unchanged; photographs are not cropped. Each artwork photo appears once on the topic; labels are collapsed. The support pair is shown in its cabinet context, with an explicit caption identifying both sides rather than the central portrait. The old sculpture ledger is unchanged; the homepage counts six topic entrances without claiming its old object aggregate covers this new batch.

## Sources checked

Museum print pages and both Cleveland component records were read in full. Cleveland museum materials/date: gilt bronze, 1400s; label adds semiprecious stones and 1360–1430. Both component records list 33.5 × 9.5 × 8 cm. Provenance: 2008 Christie’s lots 617 and 618 -> Flower -> 2011 museum. All records preserve those differences.

Seattle object record was opened in full: date late 14th–early 15th century, dimensions 35.56 × 23.81 × 14.61 cm plus separate overall h.49.53 cm; purchased October 1969, accessioned 1970. The relation is a gilded stupa **or other shrine**, not a museum-confirmed specific stupa.

Carlos live requests and a normal browser visit returned a JS verification/403 response. The search tool supplied the indexed museum record's full fields, label, bibliography, exhibition history and provenance, not merely a short snippet; those were cross-checked against the user's complete photographed label. Dimensions/provenance derive from that indexed official record. Provenance: Sotheby's 20 March 1997 lot 116 -> purchase from Kapoor Galleries for MCCM by foundation representative March–April 2001. No claim of continuous provenance before 1997. This retrieval limitation should be retained for future research. The photographed museum label itself explicitly says a Densatil memorial stupa component.

Read Estournel’s full 2020 article, figures 88, 89 and 156 (captions fetched directly with urllib when web extraction failed), and inspected their images privately to confirm the photographed objects. **Figure 156** exactly identifies Carlos 2001.19.1 and dates it c.1386; main article places it on the north side of tier 6 of the fourth tashi gomang. **Figure 89** is Seattle 70.2, c.1360, discussed on tier 1 of the second tashi gomang. These are reconstruction proposals, not asserted exact matches to individual figures in Mele's photos. Museum dates remain in the facts, with research dates distinguished. No specific tier/tower assigned to Cleveland; generic columns between tiers 2–5 are not evidence locating these two objects.

Read Rubin/Project Himalayan Art’s Estournel essay, David Weldon’s 2018 essay (including his Seattle comparison and Newari inscription discussion), and Zhong Ziyin's 2015 National Palace Museum article, downloaded PDF pp.108–119. Eighteen memorial stupas in total vs eight major tashi gomang stupas; multiple abbots and commissions across centuries. Six-tier schematic is newly typeset semantic HTML, a generic outline from Rubin, not a copied reconstruction image or exact scale plan. No artist's identity is inferred for the three groups.

Mele historical photos are link-only: University of Zurich Ethnographic Museum copyright, photographer credited; VMZ 402.00.0513 in Seattle's museum guide. Historical image reuse permission was not established. The support pair's official images are CC0, but the site uses only the user's originals. Other historic image in Seattle's guide is anonymous/date unknown, credited David Holler, and not confused with Mele 1948.

2014 exhibition attendance and catalogue references were checked in each museum record; the complete catalogue was not available/read. Carlos cat.14 pp.100–101 and Seattle cat.43 p.166 are cited through museum bibliography. The scholarly tower proposals are independently supported by Estournel's accessible article. No inaccessible catalogue passages are represented as read.

## Verification

`python3 scripts/build_museum.py`
`python3 scripts/check_densatil.py`
`python3 scripts/check_xiangtangshan.py` (whole-site local link/anchor scan)

Desktop/mobile: check all photos, three initially closed labels, zoom/original links, diagram readability, no horizontal overflow, parent/home entrances. Navigation and photos remain usable without JS.
