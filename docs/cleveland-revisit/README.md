# Cleveland revisit photography — 2026-11-22 integration

This is a photographic revision, not a redating or new attribution study. User supplied 18 original JPEGs in `/home/qingxi/museum/extra`, personally taken at Cleveland. The visit date remains unspecified. Source JPEGs are preserved byte-for-byte outside Git and on the existing image CDN; the repository holds metadata and HTML only. WebP derivatives preserve full compositions, color and aspect ratio; no generative edits, reflection removal, retouching or upscaling. Native sizes are 960–1707 pixels, so original capture resolution limits enlargement.

## Selection and identity

- Dry-lacquer Bodhisattva **1983.86**, canonical `object-231`: ce622… replaces the more reflective previous front photograph; head, arms and surviving foot remain visible. Four new side/detail views and a readable label accompany it. Previous full front photograph remains in a collapsed disclosure. Main object text/attribution/source are retained; the short observation now points to visible features rather than calling it small.
- Xiangtangshan: **1957.360** winged monster (b512…), **1923.97** Buddha head (3146… front, 9f52… side), **1972.166** Kashyapa (2d3e…). New front images appear consistently in the catalogue, detail pages and existing comparisons. All older views and labels remain available. Original 45-photo intake remains unchanged; seven new mapped assets use internal IDs 9001–9007, which are not original camera numbers.
- Densatil paired supports **2011.144.1–2**: 23fe… shows the left-hand object in the old cabinet view, 67ba… the right-hand one. Their jewellery, hand positions and bases match the existing overview. Captions use cabinet position, **not an unverified .1/.2 assignment**. The pair remains one viewing group/two physical objects. Both whole-object photos are shown; the older full cabinet view and label are retained in a disclosure. No inscriptions were independently transcribed from the object.
- **1993.160**, Phagmo Drupa: 2f0f… and d491… illustrate the already existing founder sidebar and its label. It remains a separate contextual portrait, not part of the paired supports or a newly claimed Densatil find.

The new photographed labels were visually checked against the existing accessions and titles. This photo-only round adds no new web-derived historical claim. Museum/source links and attribution qualifications are retained.

## File mapping

| Original filename | Existing work/group | Use |
|---|---|---|
| `19442b8f8c9ad476a467a4553d765177.jpg` | `object-231` | label |
| `1bcbf7cbf7f67c330aeaf8c18b13728f.jpg` | `CLE-1923.97` | label |
| `23fef167459222e7105a0fab67b4cb0f.jpg` | `supports-cleveland` | photo |
| `2d3e46bd143987f52690e0cf7e443be2.jpg` | `CLE-1972.166` | photo |
| `2f0f6431f41c789b8eb1b0f12a00b2fa.jpg` | `founder-cleveland` | photo |
| `31466dec7022e4de4918e7ea576bb42b.jpg` | `CLE-1923.97` | photo |
| `41033d42df442e8f96dc31213f82d801.jpg` | `CLE-1957.360` | label |
| `67baaec40e8126cb5398518b14da0b68.jpg` | `supports-cleveland` | photo |
| `9113dfedc5569bf3d50f811bf2a066ff.jpg` | `supports-cleveland` | label |
| `9f52cf95f2ad44eacc9e15e37cebd567.jpg` | `CLE-1923.97` | photo |
| `ac7a2ec40cb456955b790e9a734fdc85.jpg` | `object-231` | detail |
| `b512109e756103fd4b727bea4b0303cb.jpg` | `CLE-1957.360` | photo |
| `bec1da17dd637fa9b42023515f2d3fb0.jpg` | `object-231` | detail |
| `c1e0b22c8bb6fe1cac47c19869392dfa.jpg` | `CLE-1972.166` | label |
| `c89c6fcfdf9f993e2f42d45624e6fbaa.jpg` | `object-231` | detail |
| `ce6223f24cf3dc556c35b28680db00f4.jpg` | `object-231` | main |
| `d49199db67ab0386ef89315f9d967952.jpg` | `founder-cleveland` | label |
| `d9135d43e50b1507c39a8f0ba9055042.jpg` | `object-231` | detail |

## Validation

Full `build_museum.py`; `check_xiangtangshan.py`, `check_densatil.py`, `check_sama_batch.py`, `check_water_moon.py`, `check_ten_kings.py`, and `git diff --check`. Shared records remain single identities. The Xiangtangshan count checker now computes the cross-topic unique count from current data (the old fixed 59 predated the Baltimore addition).

Existing Xiangtangshan Playwright regression checks all 27 pages, unchanged eight crop geometries, filters, no-JS views, keyboard/zoom/full-view controls at 360/1440px. Targeted review covers new photographs, old-photo disclosures, labels and both pillar captions at 390/768/1440px; artifacts under `/tmp/cleveland-revisit/`. CDN upload verifies all 72 assets (18 originals + 54 WebPs) by public GET, content type and SHA256. No old remote assets deleted.
