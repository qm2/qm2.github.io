"""Validate the Pala notebook's shared identities, venue confirmations, photos and links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,sys
from build_pala_stone import resolve,BASE,ROOT
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.ids=[];self.links=[];self.images=[];self.feed(text)
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id' in d:self.ids.append(d['id'])
  if t=='a' and 'href' in d:self.links.append(d['href'])
  if t=='img':self.images.append(d)
def main():
 load=lambda n:json.loads((BASE/'data'/f'{n}.json').read_text())
 works=resolve();by={w['id']:w for w in works};assert len(by)==len(works)==24
 assert Counter(w['group'] for w in works)=={'core':20,'related':2,'earlier':2}
 assert sum('canonical_ref' in w for w in works)==9
 assert {w['id'] for w in works if w['viewing_museum_id']=='mfah'}=={'p3264','p3266','w1476','p3270'}
 assert by['p3276']['viewing_museum_id']=='met' and by['p3298']['viewing_museum_id']=='noma'
 museums=load('museums');assert len(museums)==12;assert set(w['viewing_museum_id'] for w in works)=={m['museum_id'] for m in museums}
 media=load('media');assert len(media)==48
 assert sorted([w[k] for w in works for k in ['photo','label']])==list(range(3264,3312))
 for n,p in media.items():
  assert p['original_url'].startswith('https://images.mertonmuseum.com/museum-notes/pala-stone/originals/')
  assert all(v['width']<=p['width'] and f'-{v["width"]}.webp' in v['url'] for v in p['variants'])
  assert all(abs(v['width']/v['height']-p['width']/p['height'])<.005 for v in p['variants'])
 assert set(load('readings'))==set(by)
 sources=load('sources')
 for w in works:
  assert all(k in sources for k in w['source_ids'])
  assert w.get('visit_date') is None
  if w.get('canonical_url'):
   target=ROOT/w['canonical_url'].lstrip('/')/'index.html';assert target.exists()
   assert f'/pala-stone/{w["id"]}/' in target.read_text()
 cache={};bad=[];pages=list(BASE.rglob('index.html'));assert len(pages)==30,len(pages)
 for p in pages:
  parsed=Page(p.read_text());assert len(parsed.ids)==len(set(parsed.ids)),p
  assert all(i.get('alt') and i.get('width') and i.get('height') for i in parsed.images if i.get("id")!="large-photo"),p
  for u in parsed.links:
   parts=urlsplit(u)
   if parts.scheme or parts.netloc:continue
   f=(ROOT/parts.path.lstrip('/') if parts.path.startswith('/') else p.parent/parts.path) if parts.path else p
   if f.is_dir():f=f/'index.html'
   if not f.exists():bad.append((str(p),u,'missing file'));continue
   if parts.fragment and f.suffix=='.html':
    key=str(f.resolve())
    if key not in cache:cache[key]=set(Page(f.read_text()).ids)
    if unquote(parts.fragment) not in cache[key]:bad.append((str(p),u,'missing anchor'))
 assert not bad,bad
 assert not list(BASE.rglob('*.jpg')) and not list(BASE.rglob('*.webp'))
 print(f'PASS {len(pages)} pages, 24 works, 48 mapped source photos, 12 venues, 9 shared identities; all internal links and source anchors.')
 print('Museum counts:',Counter(w['viewing_museum_id'] for w in works))
if __name__=='__main__':main()
