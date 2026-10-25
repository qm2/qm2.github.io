"""Check curated identity pairs, originals, source references and public entrances."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib
R=Path(__file__).resolve().parents[1];B=R/'museum-notes/khajuraho'
d=json.loads((B/'data/works.json').read_text())
expected={'lovers':('1982.64',931,932),'monkey':('81-27/26',933,934),'bracket':('40-18',935,936),'shiva':('60-68',937,938),'chakra':('60-82',939,940),'uma':('38.23',941,942),'female':('94.324',943,944),'jinas':('F1993.11',945,946)}
assert len(d['works'])==8 and len(d['photos'])==16
for w in d['works']:
 assert (w['accession'],w['photo'],w['label'])==expected[w['id']]
 for kind in ['photo','label']:
  p=d['photos'][str(w[kind])];assert p['work']==w['id'] and p['kind']==kind
for p in list(d['photos'].values())+[d['site_photo']]+d['site_photo']['variants']:
 assert hashlib.sha256((B/'images'/p['photo']).read_bytes()).hexdigest()==p['sha256']
 assert p.get('rotation',0)==0
w={w['id']:w for w in d['works']}
assert '可能' in w['uma']['geography']
assert '官网' in w['female']['geography'] and '现场展签' in w['female']['date']
assert all('地区' in w[k]['geography'] for k in ['monkey','bracket','shiva','chakra','jinas'])
assert '铜合金' in w['jinas']['medium'] and '神龛' in w['jinas']['title']
class Page(HTMLParser):
 def __init__(self):super().__init__();self.images=[];self.ids=[];self.anchors=[];self.details=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.append(a['id'])
  if t=='img':self.images.append(a['src']);assert a.get('alt')
  if t=='a' and a.get('href','').startswith('#') and a['href']!='#':self.anchors.append(a['href'][1:])
  if t=='details':self.details.append(a)
s=(B/'index.html').read_text();p=Page();p.feed(s)
assert len(p.images)==len(set(p.images))==17
assert len(p.ids)==len(set(p.ids)) and all(a in p.ids for a in p.anchors)
assert len(p.details)==10 and all('open' not in a for a in p.details)
assert '旃陀罗' not in s and '昌德拉王朝' in s
assert 'CC0' in s and 'Ms Sarah Welch' in s
assert 'href="south-asian-art/"' in (R/'museum-notes/index.html').read_text()
assert 'href="../khajuraho/"' in (R/'museum-notes/south-asian-art/index.html').read_text()
print('PASS: 8 identities/16 photo-label pairs, 16 original photos plus verified responsive site assets, evidence qualifiers, naming, source anchors and both entrances.')

assert s.index('id="collection"') < s.index('id="women"') < s.index('id="jain"') < s.index('id="history"')
assert p.images[0]=="images/monkey.jpg" and p.images[-1]=="images/kandariya-mahadeva-sarah-welch-1200.jpg"
