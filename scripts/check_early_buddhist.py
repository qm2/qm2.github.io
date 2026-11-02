"""Check object/photo integrity, map semantics and generated local routes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from PIL import Image
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/early-buddhist-art'
read=lambda f:json.loads((B/'data'/f).read_text())
works=read('works.json');by={w['id']:w for w in works};units=read('readings.json');photos=read('photos.json');geo=read('map.json');deriv=read('derivatives.json')
assert len(works)==len(by)==72 and len(units)==18 and len(photos)==151
assert len({w['id'] for w in works if w['accession']=='1979.6'})==1
assert len({w['id'] for w in works if w['accession']=='45-15'})==1
assert by['w1343']['photos']==['1343','1464']
assert {'N03','1436'}<=set(by['w1436']['photos'])
assert by['wn01']['accession']=='39-19' and by['wn05']['accession']=='1943.278'
assert by['wn07']['date_range']==[591,591] and by['wn07']['place']=='north-india'
assert by['w1351']['collection_museum'] is None and by['w1351']['museum_map']=='met'
assert by['w1367']['place']=='gandhara' and by['w1367']['accession']=='1985.31'
assert by['w1432']['place']=='gummadidurru' and by['w1432']['findspot_known']
assert by['w1381']['accession']=='1969.61' and by['w1381']['photo']=='1381'
assert [by['w1382-'+str(i)]['accession'] for i in range(1,4)]==['1930.328.1','1930.328.2','1930.328.3']
assert by['w1417']['accession']=='F1994.17' and by['w1405']['accession']=='25.266' and by['w1451']['accession']=='44-13'
used={n for w in works for n in w['photos']+w['labels']}
assert not used.intersection({'1347','1348','1438','1439','1453'})
for p in photos:
 if p['asset_id'] in used:
  path=B/'images/originals'/p['original_filename'];assert hashlib.sha256(path.read_bytes()).hexdigest()==p['sha256'],path
for n,m in deriv.items():
 for v in m['variants']:
  assert v['width']<=m['width']
  assert Image.open(B/v['path']).size==(v['width'],v['height'])
for w in works:
 assert w['date_range'] is None or w['date_range'][0]<=w['date_range'][1]
 assert w['photo'] in w['photos'];assert w['labels'] or w['sources']
 for uid in w['units']:assert w['id'] in next(u for u in units if u['id']==uid)['works']
for r in units:
 assert 350<=sum(len(p) for p in r['paragraphs'])<=900
 assert all(w in by for w in r['works'])
for p in geo['places']:
 if p['coordinate']:
  lon,lat=p['coordinate'];assert 62<lon<90 and 9<lat<40
 assert p['coordinate']!=[0,0]
assert sum(p['id']=='mathura' for p in geo['places'])==1
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.ids=[];self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  for key in ['href','src']:
   if a.get(key):self.links.append(a[key])
  if a.get('srcset'):self.links.extend(v.strip().split()[0] for v in a['srcset'].split(','))
  if tag=='img' and a.get('id')!='large-photo':assert a.get('alt') and a.get('width') and a.get('height')
cache={};errors=[]
for path in B.rglob('*.html'):
 page=Page(path.read_text());assert len(page.ids)==len(set(page.ids)),path
 for link in page.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(path.parent/unquote(u.path)).resolve() if u.path else path
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append((str(path.relative_to(ROOT)),link,'missing'));continue
  if u.fragment and target.suffix=='.html':
   if target not in cache:cache[target]=set(Page(target.read_text()).ids)
   if unquote(u.fragment) not in cache[target]:errors.append((str(path.relative_to(ROOT)),link,'fragment'))
assert not errors,errors[:30]
assert len(list(B.rglob('index.html')))==19
for path in [ROOT/'museum-notes/index.html',ROOT/'museum-notes/south-asian-art/index.html']:
 assert path.read_text().count('<!-- early-buddhist-')==1
print('PASS: 72 canonical records; 18 readings; original hashes; crop provenance; temporal and geographic distinctions; all 19 pages and local links.')
