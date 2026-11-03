"""Identity, shared records, aliases, photos, sources and navigation integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/yongle-xuande';HA=ROOT/'museum-notes/himalayan-art'
read=lambda p:json.loads(p.read_text())
d=read(BASE/'data/topic.json');works=read(HA/'data/works.json');wb={w['work_id']:w for w in works};pb={p['photo_id']:p for p in read(HA/'data/photos.json')}
selected=d['core']+[d['comparison']]+d['ritual'];ids=[s['work_id'] for s in selected]
assert len(d['core'])==4 and len(set(ids))==7
assert sum(wb[k]['physical_object_count'] for k in ids)==8
assert wb['w1486']['aliases']==['w1514'] and 'w1514' not in wb
assert set(wb['w1486']['art_photos'])=={'h1486','h1514'}
assert set(wb['w1486']['label_photos'])=={'h1487','h1515'}
assert not wb['w1486']['himalayan_default_inclusion']
nav=read(HA/'data/navigation.json')
assert 'w1486' not in {w['work_id'] for w in nav['works']}
assert len(nav['works'])==sum(w.get('himalayan_default_inclusion',True) for w in works)
for wid,mid in [('w1512','british'),('w1516','berlin')]:
 assert wb[wid]['display_museum_id']=='met' and wb[wid]['collection_museum_id']==mid
 assert '拍摄展出地点待核' not in (HA/wid/'index.html').read_text()
assert wb['w1512']['accession']=='1908,0420.4' and wb['w1516']['accession']=='I D 31831'
assert '不含方台与背光' in wb['w1512']['dimensions_display']
assert '不含尾羽' in wb['w1516']['dimensions_display']
visits=[v for v in read(HA/'data/visits.json') if v['work_id']=='w1486']
assert len(visits)==2 and all(v['visited_on'] is None for v in visits)
vb={v['visit_id']:v for v in read(HA/'data/visits.json')}
assert vb['cernuschi-view-a']['display_museum_id']=='cernuschi' and vb['cernuschi-view-a']['visited_month']=='2024-12'
for vid in ['cernuschi-view-b','met-2025-08-british-buddha']:
 assert vb[vid]['display_museum_id']=='met' and vb[vid]['visited_month']=='2025-08' and vb[vid]['visited_on'] is None
assert vb['nmaa-shrine-room']['display_museum_id']=='nmaa' and not vb['nmaa-shrine-room'].get('visited_month')
assert {n for v in visits for n in v['photo_ids']}=={'h1486','h1514'}
for n in ['h1486','h1514']:
 p=pb[n];assert p['work_ids']==['w1486'];assert hashlib.sha256((HA/p['path']).read_bytes()).hexdigest()==p['sha256']
assert not list(BASE.rglob('*.jpg')) and not list(BASE.rglob('*.webp')), 'Reuse shared photo bytes'
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__();self.ids=set();self.links=[];self.images=[];self.feed(path.read_text())
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):
   assert a['id'] not in self.ids,('duplicate ID',a['id']);self.ids.add(a['id'])
  for k in ['href','src']:
   if a.get(k):self.links.append(a[k])
  if a.get('srcset'):self.links.extend(s.strip().split()[0] for s in a['srcset'].split(','))
  if tag=='img' and a.get('src'):
   assert a.get('alt') and a.get('width') and a.get('height');self.images.append(a['src'])
cache={};paths=list(BASE.rglob('index.html'))+[HA/'index.html',HA/'u23/index.html',HA/'w1486/index.html',HA/'w1514/index.html',ROOT/'museum-notes/densatil/index.html',ROOT/'museum-notes/chinese-buddhist-art/index.html',ROOT/'museum-notes/index.html']
for path in paths:
 page=cache.setdefault(path,Page(path))
 for link in page.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(ROOT/u.path.lstrip('/') if u.path.startswith('/') else path.parent/unquote(u.path)).resolve()
  if target.is_dir():target/='index.html'
  assert target.is_file(),(path,link)
  if u.fragment and target.suffix=='.html':assert unquote(u.fragment) in cache.setdefault(target,Page(target)).ids,(path,link)
index=Page(BASE/'index.html');assert set(ids)<=index.ids
assert all('/himalayan-art/images/' in u for u in index.images)
assert not any('/originals/' in u for u in index.images), 'Thumbnails first; originals through lightbox'
home=(HA/'index.html').read_text()
assert home.index('id="history-entry"')<home.index('id="topic-studies"')<home.index('id="chapters"')
assert 'href="#topic-studies"' in home and '../yongle-xuande/' in home and '../densatil/' in home
assert '../../yongle-xuande/' in (HA/'u23/index.html').read_text()
assert '../himalayan-art/teachers/#phagmodrupa' in (ROOT/'museum-notes/densatil/index.html').read_text()
assert '../yongle-xuande/' in (ROOT/'museum-notes/chinese-buddhist-art/index.html').read_text()
assert 'href="yongle-xuande/"' in (ROOT/'museum-notes/index.html').read_text()
print(f'PASS: 4 core + 1 comparison + 3 ritual objects; 7 unique records; Cernuschi alias and Paris/Met views; August 2025 at month precision; NMAA shrine; {len(paths)} pages, sources and image paths.')
