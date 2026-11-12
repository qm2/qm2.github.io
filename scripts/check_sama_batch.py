"""Check the 2026 SAMA additions across existing topic schemas and shared media."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import hashlib,json
from PIL import Image
from museum_assets import sama_media
ROOT=Path(__file__).resolve().parents[1];M=ROOT/'museum-notes'
read=lambda p:json.loads(p.read_text())
media=sama_media();intake=read(ROOT/'docs/sama-2026/intake-map.json')
assert len(intake)==30 and len({r['package_id'] for r in intake})==30
assert len(media)==87
assert {str(n) for r in intake for n in r['photos']}==set(media)
assert not {'2461','2462','2463','2464'}&set(media)
assert not any(r['package_id']=='sama-27' for r in intake)
assert Counter(r['topic'] for r in intake)=={'nimrud-guardians':1,'roman-sarcophagi':1,'early-buddhist-art':4,'himalayan-art':19,'song-liao-jin-wood':1,'images-and-vows':1,'yuan-blue-and-white':3}
h=read(M/'himalayan-art/data/works.json');new=[w for w in h if w.get('package_id')]
assert len(new)==19 and len({w['work_id'] for w in new})==19
assert all(w['display_museum_id']=='sama' for w in new)
assert all(w.get('visit_date') is None for w in new)
assert next(w for w in new if w['work_id']=='sama-14')['accession']=='L.2019.4.4'
assert all('sama-27' not in w['work_id'] for w in h)
sourceids={s['source_id'] for s in read(M/'himalayan-art/data/sources.json')}
for w in new:
 assert w['public_label_photos']
 for sec in w.get('catalogue_sections',[]):
  for p in sec['paragraphs']:assert set(p['source_ids'])<=sourceids
nav=read(M/'himalayan-art/data/navigation.json')
assert sum(w['display_museum_id']=='sama' for w in nav['works'])==19
assert len(read(M/'early-buddhist-art/data/readings.json'))==18
assert len(read(M/'images-and-vows/data/works.json'))==15
v=read(M/'images-and-vows/atlas/catalogue.json');w=next(w for w in v['works'] if w['id']=='sama-eastern-wei-maitreya')
assert w['date_kind']=='period' and w['year_start']==534 and w['year_end']==550 and not w['discovery']
assert v['stats']['works']==33 and v['stats']['photos']==106
class Page(HTMLParser):
 def __init__(self,path):super().__init__();self.ids=[];self.links=[];self.feed(path.read_text())
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  self.links.extend(a[k] for k in ['src','href','data-original'] if a.get(k))
  if a.get('srcset'):self.links.extend(x.strip().split()[0] for x in a['srcset'].split(','))
topics={r['topic'] for r in intake}|{'densatil'}
parsed={p:Page(p) for t in topics for p in (M/t).rglob('*.html')}
links={u for doc in parsed.values() for u in doc.links}
for n,p in media.items():
 assert p['original'] in links,(n,'no original photograph link')
 assert p['full'] in links or any(v['path'] in links for v in p['variants']),(n,'no displayed version')
 assert len(p['variants'])==len({v['width'] for v in p['variants']})
 for v in p['variants']:
  assert v['width']<=p['width'] and v['height']<=p['height']
  assert v['path'].endswith(f'-{v["width"]}.webp')
 # Optional original/derivative verification where the local, non-Git archive is present.
 cache=ROOT.parent/'museum/sama-2026-assets'
 if cache.exists():
  assert hashlib.sha256((cache/'originals'/p['original_filename']).read_bytes()).hexdigest()==p['sha256']
  for v in p['variants']:assert Image.open(cache/Path(v['path']).name).size==(v['width'],v['height'])
for file,doc in parsed.items():
 assert len(doc.ids)==len(set(doc.ids)),file
 for link in doc.links:
  assert '/images/https:' not in link,(file,link)
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else file.parent/unquote(u.path)).resolve() if u.path else file
  if target.is_dir():target/='index.html'
  assert target.exists(),(file,link)
  if u.fragment and target.suffix=='.html':
   other=parsed.get(target) or Page(target)
   assert unquote(u.fragment) in other.ids,(file,link)
print(f'PASS: 30 works / 87 photographs, 7 primary topics, 19 SAMA Himalayan records, deferred photos excluded; {len(parsed)} pages and links checked.')
