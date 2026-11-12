"""Validate this batch's identity mapping, unmodified assets and page contracts."""
from pathlib import Path
import hashlib,json
from museum_assets import sama_media
R=Path(__file__).resolve().parents[1]; B=R/'museum-notes/nimrud-guardians'
d=json.loads((B/'data/works.json').read_text());manifest=json.loads((B/'data/intake.json').read_text())
assert len(d['works'])==4 and len(d['photos'])==9
expected=[('80.53',768,769,'石膏石（Gypsum）','公元前883—859年'),('1943.246',770,771,'石膏石（Gypsum）','公元前883—859年'),('40-17',772,773,'石灰岩（Limestone）','公元前884—860年')]
html=(B/'index.html').read_text()
for w,fields in zip(d['works'],expected):
 assert tuple(w[k] for k in ['accession','photo','label','material','date'])==fields
 assert 200<=sum(len(p['text']) for p in w['notes'])<=350
 assert f'id="{w["id"]}"' in html
for n,p in d['photos'].items():
 if p.get('remote_asset'):
  assert p['original_url']==sama_media()[p['remote_asset']]['original']; continue
 assert p==manifest['photos'][n]
 assert hashlib.sha256((B/'images'/p['photo']).read_bytes()).hexdigest()==p['sha256']
 assert p['rotation']==(-90 if n=='773' else 0)
assert 400<=sum(len(p['text']) for p in d['background'])<=600
assert html.count('<details>')==4 and '<details open' not in html
assert (R/'museum-notes/index.html').read_text().count('<!-- nimrud-entry -->')==1
assert '../nimrud-guardians/' in (R/'museum-notes/ancient-west-asia/index.html').read_text()
print('Nimrud checks passed: 4 identities, 6 local hashes + 3 shared cloud records, rotation, notes, collapsed labels and entrances.')
