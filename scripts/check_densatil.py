"""Validate source-to-photo identity, paired counting and published assets."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib
from museum_assets import sama_media
R=Path(__file__).resolve().parents[1];B=R/'museum-notes/densatil'
d=json.loads((B/'data/works.json').read_text());m=json.loads((B/'data/intake.json').read_text())
assert len(d['works'])==4 and len(d['photos'])==8
assert [(w['id'],w['photo'],w['label']) for w in d['works'][:3]]==[('supports-cleveland',776,'supports-label'),('palden-lhamo-carlos',774,775),('vajravarahi-seattle',778,779)]
assert '2011.144.1' in d['works'][0]['accession'] and '2011.144.2' in d['works'][0]['accession']
assert len(m['excluded'])==1 and '777' in m['excluded']
assert not (B/'images/777.jpg').exists()
for k,p in d['photos'].items():
 if p.get('remote_asset'):
  assert p['original_url']==sama_media()[p['remote_asset']]['original']; continue
 assert p==m['photos'][k]
 assert hashlib.sha256((B/'images'/p['photo']).read_bytes()).hexdigest()==p['sha256']
 assert p['rotation']==0
for w in d['works']:
 assert d['photos'][str(w['photo'])]['work']==w['id']
 assert d['photos'][str(w['label'])]['work']==w['id']
html=(B/'index.html').read_text()
class Images(HTMLParser):
 def __init__(self):super().__init__();self.src=[]
 def handle_starttag(self,t,a):
  if t=='img':self.src.append(dict(a).get('src'))
p=Images();p.feed(html)
assert len(p.src)==len(set(p.src))==8
assert html.count('<details>')==4 and '<details open' not in html
assert 'href="../densatil/"' in (R/'museum-notes/chinese-buddhist-art/index.html').read_text()
assert 'href="densatil/"' in (R/'museum-notes/index.html').read_text()
assert html.count('ds-tier-number')==6
print('PASS: 4 work groups, correct paired supports, 7 inputs/6 unchanged assets, unique images, six tiers and entrances.')
