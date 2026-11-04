"""Validate canonical identities, photo integrity, local links and generated coverage."""
from pathlib import Path
import json,hashlib
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
class Tags(HTMLParser):
 def __init__(self,text):
  super().__init__(); self.tags=[]; self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
def parse(path):return Tags(path.read_text()).tags
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/japanese-zen'
load=lambda n:json.loads((BASE/'data'/n).read_text())
works=load('works.json');photos=load('photos.json');ed=load('editorial.json')
assert len(works)==19 and len(photos)==43
assert len({w['id'] for w in works})==19
assert sorted(w['id'] for w in works)==sorted(x for g in ed['groups'] for x in g['works'])
assert sum(bool(w['inscription_original']) for w in works)==7
assert all(w['visit_date'] is None for w in works)
assert all(w['museum'] for w in works)
for w in works:
 assert len(w['labels'])==1
 for n in w['photos']+w['labels']:assert photos[str(n)]['work_id']==w['id']
 assert (BASE/w['id']/'index.html').exists()
for p in photos.values():
 assert hashlib.sha256((BASE/p['original']).read_bytes()).hexdigest()==p['sha256']
 assert all((BASE/v['file']).exists() for v in p['variants'])
assert photos['1732']['rotation']==90
paths=list(BASE.rglob('*.html'))+[ROOT/'museum-notes/japanese-art/index.html']
for path in paths:
 tags=parse(path);ids=[a['id'] for t,a in tags if 'id' in a];assert len(ids)==len(set(ids)),path
 for tag,attrs in tags:
  if tag=='img' and attrs.get('id')!='large-photo':assert attrs.get('alt')
  for key in ['href','src']:
   if key not in attrs:continue
   value=attrs[key];u=urlsplit(value)
   if u.scheme or u.netloc:continue
   dest=path.parent/unquote(u.path) if u.path else path
   if dest.is_dir():dest=dest/'index.html'
   assert dest.exists(),(path,value)
   if u.fragment and dest.suffix=='.html':assert unquote(u.fragment) in [a.get('id') for t,a in parse(dest)],(path,value)
for w in works:
 path=BASE/w['id']/'index.html';tags=parse(path)
 assert sum(t=='a' and 'data-photo' in a for t,a in tags)==len(w['photos'])+len(w['labels'])
 assert ('纸上的文字' in path.read_text())==bool(w['inscription_original'])
assert len(list((BASE/'images/originals').glob('*.jpg')))==43
print('PASS: 19 identities, 43 original hashes, 7 sourced inscriptions, 5 groups, all local images/links/anchors, no visit dates inferred.')
