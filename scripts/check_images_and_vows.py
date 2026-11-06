"""Validate published coverage, inscription provenance, local links and original photo integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib,csv
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/images-and-vows'
class Parser(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
load=lambda n:json.loads((BASE/'data'/n).read_text())
works=load('works.json');photos=load('photos.json');sources={s['source_id']:s for s in load('sources.json')};ed=load('editorial.json')
assert len(works)==15 and len(photos)==59
assert len(set(w['id'] for w in works))==15 and len(set(w['slug'] for w in works))==15
assert len(ed['chapters'])==5
assert sum(bool(w['inscription_data'].get('full_text')) for w in works)==8
assert sum(p['role']=='label' for p in photos.values())==18
assert all(w['visit_date'] is None for w in works)
for w in works:
 assert w['dimensions'] and w['material'] and w['sources']
 for sid in w['sources']:assert sid in sources
 assert photos[str(w['hero'])]['role']=='artwork'
 for n in w['photos']+w['labels']:assert photos[str(n)]['work_id']==w['id']
 ins=w['inscription_data']
 if ins.get('full_text'):assert ins['full_source_id'] in sources and ins['full_note']
for p in photos.values():
 assert hashlib.sha256((BASE/p['original']).read_bytes()).hexdigest()==p['sha256']
 assert all((BASE/v['file']).exists() and v['width']<=p['width'] for v in p['variants'])
assert {n for n,p in photos.items() if p['rotation']}=={'1832','1839'}
pages=list(BASE.rglob('*.html'));assert len(pages)==16
extras=[ROOT/'museum-notes/index.html',ROOT/'museum-notes/chinese-buddhist-art/index.html',ROOT/'museum-notes/xuzhou/x24/index.html']
cache={}
def tags(p):
 if p not in cache:cache[p]=Parser(p.read_text()).tags
 return cache[p]
for path in pages:
 ids=[a['id'] for _,a in tags(path) if 'id' in a];assert len(ids)==len(set(ids)),(path,'duplicate IDs')
 for tag,a in tags(path):
  if tag=='img' and a.get('id')!='large-photo':assert a.get('alt') and a.get('width') and a.get('height')
  for attr in ['href','src']:
   if attr not in a:continue
   v=urlsplit(a[attr])
   if v.scheme or v.netloc:continue
   target=(ROOT/unquote(v.path).lstrip('/') if v.path.startswith('/') else path.parent/unquote(v.path)).resolve() if v.path else path
   if target.is_dir():target=target/'index.html'
   assert target.exists(),(path,a[attr])
   if v.fragment and target.suffix=='.html':assert unquote(v.fragment) in {x.get('id') for _,x in tags(target)},(path,a[attr],'anchor')
  if tag=='img' and a.get('src'):assert not urlsplit(a['src']).scheme,'external image'
for path in extras:assert 'images-and-vows/' in path.read_text(),path
by={w['id']:w for w in works}
assert '二區' in by['mfah-526-faxing']['inscription_data']['full_text']
assert '乙巳' in by['mfah-526-faxing']['inscription_data']['full_text']
assert '天寶二年' in by['met-528-yiyi']['inscription_data']['full_text']
assert '□' in by['met-543-yiyi']['inscription_data']['full_text']
assert by['cle-570s-dual']['material']=='大理石，彩绘'
assert by['met-543-yiyi']['date']=='533—543'
assert 'full_text' not in by['cle-500-maitreya']['inscription_data']
print('PASS: 15 identities, 59 intact originals, 8 sourced transcripts, 16 generated pages, local links/anchors, navigation and no third-party images.')
