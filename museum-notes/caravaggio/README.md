# Caravaggio / European painting

A personal photo notebook, not a catalogue raisonné. Public signature: Merton.

## Rebuild

From the repository root:

```sh
python3 scripts/build_caravaggio.py
python3 scripts/build_museum.py
```

`data/works.json` is the editorial source of truth. The generator builds the European painting parent, the Caravaggio index, 27 permanent work pages, and a seven-group comparison page. Images and editorial data are shared, not duplicated between views. No framework, package install, external image host, or network call is needed to rebuild.

## Intake

The user’s `Caravaggio.zip` contains 53 JPEGs, numbered 470–522. Extracted sources remain outside the repository. `data/photo-manifest.json` accounts for every file, with SHA-256, role, work associations and the public filename when applicable.

- 27 artwork photos, one for each work.
- 2 context photos: 473 (Cavalletti Chapel), 478 (Contarelli Chapel, shared by three works).
- 24 label/panel photos, retained privately. Three Matthew paintings share panel 479. The Capitoline John (520) has no label; image and collection catalogue were used to identify it.
- No duplicate artwork shots were removed: the two Fortune Tellers and four John the Baptists are distinct paintings.
- All 29 published JPEG files are byte-identical copies. No cropping, perspective reconstruction, recoloring or AI image changes. Photographs show the original frames, glare and viewing angles. CSS uses contain sizing.
- Filename timestamps are not treated as visit dates.

## Editorial decisions

Periods are browsing groups, not exact claims about a painting’s place of execution. Francis (1606) is a transition work; its page does not infer whether it was painted before or after flight from Rome. Overlapping dates and alternate datings remain explicit.

The 27-work count includes the Barberini *Narcissus*, explicitly attributed to Caravaggio **or Spadarino**, and separated from the main chronology. The current Met record and photographed label attribute the private-loan *Holy Family* to Caravaggio. It is not described as Met-owned. The Carpineto *Francis* is FEC property on deposit at Barberini. Corsini collection ownership is recorded without inferring the photographed museum building from file order.

The *Boy with a Basket of Fruit* is Borghese-owned; its French JA-labelled photo records a Paris exhibition context. The Jacquemart-André exhibition record is linked. No personal visit date is inferred.

Each page separates visible observations from the creation/collection story and links to official museum, church, or municipal sources. Short observations are editorial reading prompts, not invented memories. The chronology and stories are concise paraphrases. No third-party artwork photographs are republished.

### Variants retained

- Capitoline Fortune Teller: photographed label 1597; catalogue 1596–97.
- Boy with Fruit: French label c.1596; Borghese catalogue c.1595.
- Uffizi Bacchus: label c.1595–97 vs catalogue c.1598; rediscovery year 1916 vs 1913. The text uses “early 20th century” and notes both years. Uffizi’s conflicting Bacchus/Medusa gift chronology is not repeated.
- Medusa: c.1597 on label; 1596–98 in Uffizi’s virtual exhibition. Correct support is oil on canvas-covered poplar shield, not a conventional stretched canvas.
- Isaac: label c.1603–04; catalogue c.1603.
- Francis: photographed label says Carpineto’s San Francesco; FEC and museum research records say San Pietro. Difference disclosed.
- Borghese John: label c.1610; catalogue 1609–10.
- David: photographed label 1609–10; online record discusses an earlier 1606–07 dating too. Pardon-gift interpretation remains a hypothesis.
- Death of Virgin: rejection documented by the Louvre; sensational model stories are not presented as fact.

## Browsing

The index supports full-text search, collection/venue and subject filters, and a larger two-column gallery mode. All content and original image links remain readable without JavaScript. The native dialog supports previous/next, Escape, focus restoration, original-resolution viewing and scrolling. Comparison groups navigate only the photographs in that group; no implied real-world scale comparison.

Sources were checked on 2026-09-22. Work-specific URLs are in `data/works.json`. Historical exhibition records are not claims about current display locations.
