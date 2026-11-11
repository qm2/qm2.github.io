"""Data, provenance, URL and image contracts for the Etruscan notebook."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json,sys
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'museum-notes/etruscans'
load=lambda n:json.loads((B/'data'/f'{n}.json').read_text())
works=load('objects');photos=load('photos');readings=load('deep_readings');by={w['id']:w for w in works};pb={p['photo_id']:p for p in photos}
assert len(by)==len(works)==131 and len(pb)==len(photos)==377 and len(readings)==53
assert Counter(p['kind'] for p in photos)=={'object':202,'label':129,'detail':20,'panel':16,'context':10}
assert len({r['object_id'] for r in readings})==53
assert set(w['id'] for w in works if w['is_deep_reading'])=={r['object_id'] for r in readings}
assert set(x for c in load('chapters') for x in c['object_ids'])==set(by)
assert len([p for p in load('places') if p['longitude'] is not None])==18
assert all(w['date_start']<=w['date_end'] for w in works)
assert all(w['visit_date'] is None and all(v['date'] is None for v in w['visits']) for w in works)
for w in works:
 assert (B/w['id']/'index.html').is_file()
 assert w['primary_photo'] in w['object_photos']+w['detail_photos']
 for pid in w['object_photos']+w['detail_photos']+w['label_photos']:
  assert pid in pb,(w['id'],pid)
  assert w['id'] in [x.get('object_id') for x in pb[pid]['links']],(w['id'],pid,'missing inverse')
 assert w['title_status']=='label_original' and w['title_zh'] is None
for p in photos:
 assert p['variants'] and p['sha256']
 assert max(v['width'] for v in p['variants'])<=p['display_width']
 for x in p['links']:
  if x.get('object_id'):assert x['object_id'] in by
for wid,num in {'e008':'20461','e087':'919.27.5','e093':'68.AE.17','e114':'24997.A-B','e111':'Cp5193.1-2'}.items():
 assert num.replace(' ','').lower() in by[wid]['inventory_number_as_read'].replace(' ','').lower(),(wid,by[wid]['inventory_number_as_read'])
assert by['e122']['date_start']==1 and by['e122']['date_end']==100
assert all('p215' in by[f'e{i:03d}']['object_photos'] for i in range(69,77))
assert all(not list(B.rglob('*'+ext)) for ext in ['.jpg','.jpeg','.png','.webp','.avif'])
allowed={p['path'] for p in photos}|{v['file'] for p in photos for v in p['variants']}|{v['file'] for c in load('detail-crops').values() for v in c['variants']}
origin='https://images.mertonmuseum.com/museum-notes/etruscans/images/'
class Doc(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.refs=[];self.images=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for k in ['href','src','data-original']:
   if a.get(k):self.refs.append(a[k])
  if tag=='img':
   self.images.append(a)
   for v in a.get('srcset','').split(','):
    if v.strip():self.refs.append(v.strip().split()[0])
cache={}
def doc(p):
 if p not in cache:cache[p]=Doc(p.read_text())
 return cache[p]
errors=[]
for path in B.rglob('index.html'):
 d=doc(path)
 if len(d.ids)!=len(set(d.ids)):errors.append((str(path),'duplicate ID'))
 for a in d.images:
  if a.get('id')=='large-photo':continue
  if not a.get('alt') or not a.get('width') or not a.get('height'):errors.append((str(path),'image missing text/dimensions',a))
 for ref in d.refs:
  if ref.startswith(origin):
   if ref[len(origin):] not in allowed:errors.append((str(path),'unmapped image',ref))
   continue
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  target=(ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else path.parent/unquote(u.path)) if u.path else path
  if target.is_dir():target/='index.html'
  if not target.exists():errors.append((str(path),'broken local link',ref));continue
  if u.fragment and target.suffix=='.html' and unquote(u.fragment) not in doc(target).ids:errors.append((str(path),'missing fragment',ref))
 for phrase in ['Qingxi','等待用户','不得','用户在本轮','根据研究摘要整理','{record_count}','{reading_count}','{photo_count}']:
  if phrase in path.read_text():errors.append((str(path),'editorial residue',phrase))
assert len(list(B.rglob('index.html')))==137
assert 'etruscan-entry' in (ROOT/'museum-notes/index.html').read_text()
for rel in ['greek-roman-bronzes/index.html','roman-sarcophagi/index.html','roman-sarcophagi/stories/index.html']:
 assert (ROOT/'museum-notes'/rel).read_text().count('<!-- etruscan-related -->')==1
if errors:
 for e in errors[:40]:print(e)
 sys.exit(f'{len(errors)} errors')
print(f'PASS: {len(works)} records, {len(readings)} readings, {len(photos)} photos; 137 pages, image manifest and all internal links/anchors.')
