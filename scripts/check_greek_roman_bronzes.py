"""Validate group identity, every original photograph, dates and generated links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,hashlib
from museum_image_urls import HOSTS,image_url
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/greek-roman-bronzes'
def load(n):return json.loads((BASE/f'data/{n}.json').read_text())
w=load('works');by={x['id']:x for x in w};p=load('photos');m=load('museums');notes=load('editorial');sources={x['id'] for x in load('sources')}
assert len(w)==len(by)==18 and len(m)==8
assert Counter(i for s in load('sections') for i in s['works'])==Counter(set(by)-{'b06'})
assert len(p)==44 and Counter(x['role'] for x in p.values())=={'artwork':24,'label_or_context':20}
assert '1997' not in p and all(x['visit_date'] is None for x in w)
assert not by['b06']['include_in_core_timeline'] and by['b06']['date_start'] is None
assert by['b14']['photo_order']==['1993','1994'] and len(by['b14']['components'])==2
assert len(by['b03']['components'])==3 and by['b16']['photo_order']==['1998','2001']
assert by['b01']['photo_order']==['1962','1963'] and len(by['b09']['photo_order'])==3
assert p['1966']['rotation']==90 and p['1992']['rotation']==90 and p['1993']['rotation']==-90
assert by['b17']['date_start']==1 and by['b17']['alternate_dates'][0]['start']==-100
assert by['b09']['timeline_candidates']==[176,180]
assert all(by[i]['accession'] is None for i in ['b07','b08','b13','b14'])
for wid,o in by.items():
 assert set(o['source_ids'])<=sources
 assert o['museum_id'] in {x['id'] for x in m} and o['cover'] in o['photo_order']
 assert not o['include_in_core_timeline'] or o['date_start']<=o['date_end']
 for k in o['photo_order']+o['label_photos']:assert wid in p[k]['works'],(wid,k)
 for sec in notes[wid]['sections']:
  for para in sec['paragraphs']:assert set(para['source_ids'])<=sources
for key,photo in p.items():
 raw=BASE/'images/originals'/photo['original'];assert hashlib.sha256(raw.read_bytes()).hexdigest()==photo['sha256']
 assert all(by[i]['photo_order'].count(key)+by[i]['label_photos'].count(key)==1 for i in photo['works'])
 for v in photo['variants']:
  assert (BASE/'images'/v['file']).is_file() and v['width']<=photo['display_width']
assert len(list((BASE/'images/originals').glob('*.jpg')))==44
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.links=[];self.ids=[];self.images=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for k in ['href','src','data-original']:
   if a.get(k):self.links.append(a[k])
  if a.get('srcset'):self.links.extend(t.strip().split()[0] for t in a['srcset'].split(','))
  if tag=='meta' and a.get('property')=='og:image':self.links.append(a['content'])
  if tag=='img':self.images.append(a)
files=list(BASE.rglob('index.html'));assert len(files)==22
cache={}
for f in files:
 page=Page(f.read_text());assert len(page.ids)==len(set(page.ids)),f
 for im in page.images:
  if im.get('id')=='large-photo':continue
  assert im.get('alt') and im.get('width') and im.get('height'),(f,im)
  src=im.get('src','');u=urlsplit(src)
  if u.scheme:
   key=unquote(u.path).lstrip('/')
   assert src==image_url(key,''),(f,'unconfigured image host',src)
   assert key.startswith('museum-notes/greek-roman-bronzes/images/'),(f,src)
 for link in page.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:
   if u.scheme+'://'+u.netloc not in HOSTS.values():continue
   assert link==image_url(unquote(u.path).lstrip('/'),''),(f,link)
   assert (ROOT/unquote(u.path).lstrip('/')).is_file(),(f,link)
   continue
  target=Path(unquote(u.path));target=(ROOT/target.as_posix().lstrip('/')) if target.is_absolute() else f.parent/target
  target=target.resolve()
  if target.is_dir():target=target/'index.html'
  assert target.is_file(),(f,link,target)
  if u.fragment and target.suffix=='.html':
   if target not in cache:cache[target]=Page(target.read_text()).ids
   assert unquote(u.fragment) in cache[target],(f,link)
for path,marker in [('museum-notes/index.html','<!-- bronze-entry -->'),('museum-notes/roman-sarcophagi/index.html','../greek-roman-bronzes/')]:assert (ROOT/path).read_text().count(marker)==1
print('PASS: 18 groups / 8 museums / 44 original hashes / 22 pages; photo ownership, dates, local links and anchors.')
assert image_url('museum-notes/xuzhou/images/example.webp','../images/example.webp')=='../images/example.webp'
for f in files:
 page=Page(f.read_text())
 for src in page.links:
  u=urlsplit(src)
  if not u.scheme and (f.parent/unquote(u.path)).resolve().is_relative_to(BASE/'images'):
   assert not HOSTS.get('museum-notes/greek-roman-bronzes/images/'),(f,'unmigrated image URL',src)
print('PASS: migrated image URLs resolve to retained local assets; other topics remain local.')
