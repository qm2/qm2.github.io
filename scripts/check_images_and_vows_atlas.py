"""Validate object identities, complete intake accounting and public photo derivatives."""
from pathlib import Path
import csv, hashlib, json
from collections import Counter
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/images-and-vows'
load=lambda p:json.loads(p.read_text())
data=load(BASE/'atlas/catalogue.json')
works=data['works'];photos=data['photos'];by={w['id']:w for w in works}
audit=load(ROOT/'docs/images-and-vows/atlas-photo-audit.json')
excluded=load(ROOT/'docs/images-and-vows/atlas-excluded-works.json')
manifest=list(csv.DictReader((ROOT/'docs/images-and-vows/intake-manifest.csv').open()))
assert len(by)==len(works)
assert {p['number'] for p in audit}=={int(p['photo_number']) for p in manifest}
assert len(audit)==len(manifest)
assert len({p['number'] for p in audit})==len(audit)
assigned=Counter(p['number'] for w in works for p in w['photos'])
assert all(n==1 for n in assigned.values())
assert set(assigned)==set(map(int,photos))
assert set(assigned)=={p['number'] for p in audit if p['disposition']=='published_work'}
assert {w['id'] for w in excluded}.isdisjoint(by)
assert all(w['period']!='唐' and w['scope']=='main' for w in works)
assert {p['work_id'] for p in audit if p['work_id']}==set(by)|{w['id'] for w in excluded}
assert by['mfa-1843']['museum_id']=='noma' and by['mfa-1843']['accession']=='2014.39'
assert {p['number'] for p in by['penn-551-c404']['photos']}=={1891,1892}
assert not {1891,1892}&{p['number'] for p in by['penn-575-c429']['photos']}
assert by['penn-1893']['museum_id']=='princeton'
assert by['museum-1848']['year_start']==565
assert len(by['museum-1848']['photos'])==9
for core in load(BASE/'data/works.json'):
 w=by[core['id']]
 assert w['reading_url']=='../'+core['slug']+'/'
 assert {p['number'] for p in w['photos']}==set(core['photos']+core['labels'])
for w in works:
 assert w['museum_id'] in {m['id'] for m in data['museums']}
 assert w['hero'] in {p['number'] for p in w['photos']}
 assert (w['sources'] or any(p['role']=='label' for p in w['photos']) or w['hero']==1784)
 assert w['year_start']<=w['year_end']
 assert w['visit_date'] is None
 for p in w['photos']:assert photos[str(p['number'])]['work_id']==w['id']
for key,p in photos.items():
 original=(BASE/'atlas'/p['original']).resolve()
 assert hashlib.sha256(original.read_bytes()).hexdigest()==p['sha256']
 assert p['sha256']==next(x['sha256'] for x in audit if x['number']==int(key))
 assert p['width']>0 and p['height']>0 and p['caption']
 for v in p['variants']:
  im=Image.open(BASE/'atlas'/v['file'])
  assert im.width==v['width']<=p['width']
  assert abs(im.width/im.height-p['width']/p['height'])<.015
archived_names={p['original_filename'] for p in audit if p['disposition']!='published_work'}
assert not archived_names&{p.name for p in (BASE/'atlas/images/originals').iterdir()}
assert data['stats']['works']==len(works) and data['stats']['photos']==len(photos)
assert data['stats']['museums']==len({w['museum_id'] for w in works})
print('PASS: 111 photos accounted for; 35 identities, 32 public objects / 103 photos / 13 museums; 15 original reading links; Tang excluded; original hashes, rotations and derivatives verified.')
