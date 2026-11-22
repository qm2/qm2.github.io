"""Validate source-to-photo identity, paired counting and published assets."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib
from museum_assets import sama_media
R=Path(__file__).resolve().parents[1];B=R/'museum-notes/densatil'
d=json.loads((B/'data/works.json').read_text());m=json.loads((B/'data/intake.json').read_text())
assert len(d['works'])==4 and len(d['photos'])==13
assert [(w['id'],w['photo'],w['label']) for w in d['works'][:3]]==[('supports-cleveland',776,'revisit-support-label'),('palden-lhamo-carlos',774,775),('vajravarahi-seattle',778,779)]
assert '2011.144.1' in d['works'][0]['accession'] and '2011.144.2' in d['works'][0]['accession']
assert len(m['excluded'])==1 and '777' in m['excluded']
assert not (B/'images/777.jpg').exists()
revisit=json.loads((R/'museum-notes/data/cleveland-revisit-media.json').read_text())['photos']
for k,p in d['photos'].items():
 if p.get('source_batch'):
  q=revisit[Path(p['source_photo']).stem];assert p['original_url']==q['original_url'] and p['sha256']==q['sha256'];continue
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
assert len(p.src)==len(set(p.src))==13
assert html.count('<details>')==5 and '<details open' not in html
assert 'href="../densatil/"' in (R/'museum-notes/chinese-buddhist-art/index.html').read_text()
assert 'href="densatil/"' in (R/'museum-notes/index.html').read_text()
assert html.count('ds-tier-number')==6
print('PASS: 4 work groups, correct paired supports, original intake intact plus 5 revisit photos, unique images, six tiers and entrances.')
