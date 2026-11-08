# Roman sarcophagi — research and delivery, 2026-11-08

## Evidence and intake

The handoff is retained verbatim under `handoff/`. Its original assertions are not the final authority: new direct photo comparisons corrected both Vatican and Marcus Claudianus associations. Public canonical data and build instructions are in `museum-notes/roman-sarcophagi/`.

Research files distinguish modern label observations, institutional catalogues, scholarly excerpts/reproductions and material not independently read. External images were inspected for matching only; no third-party images, book pages or PDFs were added to the site.

- `research-war.json`: Portonaccio, Vatican933, independent932, panel914. Newby directly checked at printed p.215 via Library of Congress open book; Calandra/Spinola through explicitly attributed catalogue reproductions.
- `research-1930.json`: identifies the lower object as Vatican942 (new r24); upper915 is a frieze, not a sarcophagus. Middle lid remains unnumbered. Original package assigned this photograph to the wrong group.
- `research-houston.json`: the three Houston sarcophagi; newly located independent Panther Side Panel catalogue2003.53.2, official180–195 dating and dimensions.
- `research-catalogue.json`: remaining17 records, original modern labels, institution records, catalogue reception and colour-research scope. Corrects1922: the continuous inscribed lid just above the body is the identified component, not both higher fragments.

## Implemented

24 canonical object pages, five home reading chapters, four comparison groups, atlas with modern viewing map and date-aware chronology; 8 viewing institutions. 932 is explained as an independent associated lid within r13. 60 original photographs remain byte-for-byte intact; five crops and upright/responsive derivatives use only those originals. Louvre viewing does not overwrite Torlonia ownership. No visit date is inferred.

## Specific unresolved matters

- r09 museum accession, beyond the published catalogue item251.
- r23 detailed museum catalogue and dating: currently a reference image archive plus Christian's attribution of914 to the Muses group.
- Number/date/original association of the middle lid in1930; exact identity of central deity on the unrelated upper915 frieze.
- Number and expanded names of children in the two published summaries of932; no new Latin transcription was fabricated.
- Original tombs and patrons where no direct evidence survives; no precise ancient map routes.

## Validation

`python3 scripts/build_museum.py` completed, with no changes to other topic pages. `check_roman_sarcophagi.py` checks27 pages, IDs, sources, all local links/fragments, date types, corrected photo matching and all60 SHA256 values. `check_roman_sarcophagi_browser.py` uses actual Chromium at1440,390,320px, checks gallery switching/show-all, original links, rotated label, modal zoom/Escape, synchronized filtering, back navigation and decoded images on all24 detail pages. Screenshots remain in/tmp, not public assets.

The source photo1930 added a new securely identified sarcophagus without adding photographs. Therefore the final24 records intentionally differ from the handoff's23. Associated unidentified context objects are not silently counted as confirmed sarcophagi.
