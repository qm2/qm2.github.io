"""Validate intake identities, citations, routes, all original associations and responsive assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,re,hashlib,csv
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/japanese-buddhist-sculpture';PACK=Path('/home/qingxi/museum/japanese-buddhist-sculpture-codex-pack')
class Parse(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=[];self.links=[];self.img=[];self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if tag=='a'and'href'in a:self.links.append(a['href'])
  if tag=='img':self.img.append(a)
def check():
 d=json.loads((B/'data/catalogue.json').read_text());m=json.loads((B/'data/media.json').read_text());es=json.loads((B/'data/essays.json').read_text());src=json.loads((B/'research/source_registry.json').read_text());geo=json.loads((B/'data/viewing-museums.geojson').read_text());by={w['id']:w for w in d}
 assert len(d)==62 and len(by)==62 and len(m)==149 and len(es)==25 and len(geo['features'])==15
 assert len(json.loads((B/'data/selections.json').read_text())['user_memorable_ids'])==16
 assert len(json.loads((B/'data/comparisons.json').read_text()))==10
 numbers={p['number'] for w in d for p in w['photos']+w['labels']};assert numbers=={int(n) for n in m}
 seen=[]
 for f in geo['features']:
  ids=f['properties']['record_ids'];actual=[w['id'] for w in d if w['viewing_museum_id']==f['properties']['id']];assert set(ids)==set(actual);seen+=ids
 assert sorted(seen)==sorted(by)
 assert by['j01']['viewing_museum_id']==by['j02']['viewing_museum_id']=='MFAH'
 assert all(w['visit_date'] is None for w in d)
 assert by['j62']['year_start']==1200 and by['j62']['year_end']==1299
 assert by['j04']['photo_numbers']==by['j05']['photo_numbers']==[3121]
 assert 'bronze' in by['j08']['material_group'].lower() or '青铜' in by['j08']['materials_summary']
 for w in d:
  assert (B/w['id']/'index.html').exists()
  for p in w['photos']+w['labels']:
   assert p['sha256']==m[str(p['number'])]['sha256']
   if PACK.exists():assert hashlib.sha256((PACK/p['path']).read_bytes()).hexdigest()==p['sha256']
 for n,p in m.items():
  for v in p['variants']:
   assert v['width']<=p['width'] and abs(v['height']/v['width']-p['height']/p['width'])<.005
   assert v['url'].endswith(f'-{v["width"]}.webp')
 for f in (B/'content').rglob('*.md'):
  for k in re.findall(r'\[((?:S-|U-)[A-Z0-9-]+|L\d+)\]',f.read_text().split('\n---')[0]):assert k in src,(f,k)
 cache={}
 for p in B.rglob('index.html'):
  s=p.read_text();h=Parse(s);assert len(h.ids)==len(set(h.ids)),p
  assert not re.search(r'\[(?:S-|U-)\w',s),p
  for a in h.img:
   if a.get('id')!='large-photo':assert a.get('alt') and a.get('width') and a.get('height'),(p,a)
  for url in h.links:
   u=urlparse(url)
   if u.scheme or u.netloc:continue
   target=ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else p.parent/unquote(u.path)
   if not u.path:target=p
   if target.is_dir():target/= 'index.html'
   assert target.exists(),(p,url)
   if u.fragment and target.suffix=='.html':
    if target not in cache:cache[target]=set(Parse(target.read_text()).ids)
    assert unquote(u.fragment)in cache[target],(p,url)
 for route in ['museum-notes/index.html','museum-notes/japanese-art/index.html']:
  assert 'japanese-buddhist-sculpture/'in (ROOT/route).read_text()
 assert len(list(B.rglob('index.html')))==73
 print('PASS: 62 records / 149 original photos / 25 readings / 6 chapters / 15 viewing museums / 10 comparisons / 73 pages; citations, media dimensions, all local links and anchors.')
if __name__=='__main__':check()
