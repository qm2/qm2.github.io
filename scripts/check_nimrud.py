"""Validate this batch's identity mapping, unmodified assets and page contracts."""
from pathlib import Path
import hashlib,json
from museum_assets import sama_media
R=Path(__file__).resolve().parents[1]; B=R/'museum-notes/nimrud-guardians'
d=json.loads((B/'data/works.json').read_text());manifest=json.loads((B/'data/intake.json').read_text())
assert len(d['works'])==6 and len(d['photos'])==13
expected=[('80.53',768,769,'石膏石（Gypsum）','公元前883—859年'),('1943.246',770,771,'石膏石（Gypsum）','公元前883—859年'),('40-17',772,773,'石灰岩（Limestone）','公元前884—860年')]
html=(B/'index.html').read_text()
for w,fields in zip(d['works'],expected):
 assert tuple(w[k] for k in ['accession','photo','label','material','date'])==fields
 assert 200<=sum(len(p['text']) for p in w['notes'])<=350
 assert f'id="{w["id"]}"' in html
for n,p in d['photos'].items():
 if p.get('remote_asset'):
  assert p['original_url']==sama_media()[p['remote_asset']]['original']; continue
 if p.get('source_type')=='user_chat_attachment':
  assert p['original_url'].startswith('https://images.mertonmuseum.com/museum-notes/nimrud-kimbell-vatican/originals/')
  assert len(p['sha256'])==64 and len(p['variants'])==3
  assert all(v['width']<=p['width'] for v in p['variants'])
  assert p['work'] in {w['id'] for w in d['works']}
  continue
 assert p==manifest['photos'][n]
 assert hashlib.sha256((B/'images'/p['photo']).read_bytes()).hexdigest()==p['sha256']
 assert p['rotation']==(-90 if n=='773' else 0)
assert 400<=sum(len(p['text']) for p in d['background'])<=600
assert html.count('<details>')==6 and '<details open' not in html
assert (R/'museum-notes/index.html').read_text().count('<!-- nimrud-entry -->')==1
assert '../nimrud-guardians/' in (R/'museum-notes/ancient-west-asia/index.html').read_text()
new={w['id']:w for w in d['works'][-2:]}
assert new['kimbell-pair']['accession']=='AP 1981.04 a,b' and new['kimbell-pair']['object_count']==2
assert new['vatican-14990']['accession']=='Inv.14990'
assert sum(w['object_count'] for w in d['works'])==7
assert len({w['id'] for w in d['works']})==6
assert {w['photo'] for w in d['works'][-2:]}=={'kimbell-pair','vatican-eagle'}
assert {w['label'] for w in d['works'][-2:]}=={'kimbell-label','vatican-label'}
assert all(w['visit_date'] is None for w in d['works'][-2:])
for w in d['works']:
 assert f'id="{w["id"]}"' in html
 for note in w['notes']+w.get('research_notes',[]):
  assert all(k in d['sources'] for k in note['sources'])
assert 'I-04' in html and 'Inv.14990' in html and '六组亲见' in html
assert '四件并看' not in html and '四家博物馆' not in html
print('Nimrud checks passed: 6 viewing groups / 7 collection objects, 13 photographs, preserved original identities, separate room evidence, links and labels.')
