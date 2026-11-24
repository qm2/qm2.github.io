"""Verify intake coverage, identity-sensitive facts and generated local links."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit,unquote
from check_pala_stone import Page
import json,re
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/chola-bronzes'
load=lambda n:json.loads((BASE/'data'/f'{n}.json').read_text())
ws=load('catalogue');by={w['id']:w for w in ws};media=load('media');sources=load('sources');ms=load('museums')
assert len(ws)==38 and sum(w['object_count'] for w in ws)==40
counts=Counter(str(n) for w in ws for n in w['photos']);assert all(counts[str(n)]==1 for n in range(3312,3390))
assert counts['noma_three_buddhas_case']==2
assert len([m for m in media.values() if m.get('is_original',True)])==81
assert by['c05']['collection']==by['c06']['collection']=='休斯顿美术馆'
assert len(load('places'))==10 and len(load('essays'))==3
assert load('chapters')[-1]['title']=='同一片土地，不同的修行'
assert len(load('comparisons')[0]['works'])==7
assert by['c37']['accession']=='2021.98' and by['c37']['group']=='core'
assert by['c38']['group']=='pre_chola' and by['c38']['accession'] is None
for k,m in media.items():
 if not m.get('is_original',True):assert m['derived_from']=='noma_three_buddhas_case' and all(v['width']<=m['width'] for v in m['variants'])
assert set(media)=={str(x) for x in counts};assert len(ms)==12
assert by['c02']['viewing_museum_id']=='mfah' and by['c02']['collection']=='费城艺术博物馆'
assert by['c04']['accession']=='62.265' and by['c17']['accession']=='1969.117'
assert by['c20']['photos']==[3352,3353,3386,3387] and by['c20']['photo']==3352
assert by['c29']['ownership_status']=='returned_to_india_on_loan'
assert by['c24']['group']==by['c35']['group']=='extension'
assert not any(w['visit_date'] for w in ws)
ids=[id for ch in load('chapters') for id in ch['works']];assert len(ids)==38 and set(ids)==set(by)
for w in ws:assert w['photo'] in w['photos'] and w['label'] in w['photos']
for name in ['readings','stories','history','essays','places','events','comparisons']:
 for key in re.findall(r'\[\[([A-Z0-9-]+)\]\]',json.dumps(load(name),ensure_ascii=False)):assert key in sources,key
for d in load('details'):
 assert d['photo'] in by[d['work']]['photos']
 for v in d['variants']:assert v['width']<=d['width']
cache={};nlinks=0
for p in BASE.rglob('index.html'):
 parsed=Page(p.read_text());assert len(parsed.ids)==len(set(parsed.ids)),p
 for im in parsed.images:
  if im.get('id')=='large-photo':continue
  assert im.get('alt') and im.get('width') and im.get('height'),(p,im)
  assert im['src'].startswith('https://images.mertonmuseum.com/museum-notes/chola-bronzes/'),im['src']
 for url in parsed.links:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  target=(ROOT/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (p.parent/unquote(u.path)) if u.path else p
  target=target.resolve()
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(p,url,target)
  if u.fragment and target.suffix=='.html':
   if target not in cache:cache[target]=set(Page(target.read_text()).ids)
   assert unquote(u.fragment) in cache[target],(p,url)
  nlinks+=1
assert len(list(BASE.rglob('index.html')))==47
for parent in ['index.html','south-asian-art/index.html']:assert 'chola-bronzes/' in (ROOT/'museum-notes'/parent).read_text()
print(f'PASS: 38 groups, 40 objects, 81 originals (one shared display photo), 12 museums, 47 pages, {nlinks} local links; source and crop references valid.')
