"""Check intake identity, shared photographs and published links without a browser."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
from collections import Counter
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];base=ROOT/'museum-notes/xiangtangshan'
d=json.loads((base/'data/works.json').read_text());ws={w['id']:w for w in d['works']};a={x['number']:x for x in d['assets']}
assert len(ws)==25 and Counter(w['scope'] for w in ws.values())=={'core_attributed':24,'disputed_related':1}
assert Counter(w['group'] for w in ws.values())=={'NN':8,'NM':1,'NS':3,'S2':6,'S36':4,'unassigned':2,'related':1}
assert len(a)==45 and len(d['excluded'])==1
assert ws['FSG-F1916.346']['accession']=='F1916.346a-b'
for i,pos in [('FSG-F1977.8','左'),('FSG-F1953.86','右'),('FSG-F1953.87','左'),('FSG-F1977.9','右'),('PEN-C113','左'),('PEN-C151','中央'),('PEN-C150','右')]:assert pos in ws[i]['position']
assert a[747]['work_ids']==['FSG-F1921.2']
assert set(a[727]['work_ids'])=={'FSG-F1921.1','FSG-F1921.2','FSG-F1968.45'}
assert set(a[724]['work_ids'])=={'CLE-1923.97','CLE-1972.166'}
assert set(a[739]['work_ids'])=={'PEN-C113','PEN-C151','PEN-C150'}
assert '560' in ws['PAM-51.255']['date']
assert hashlib.sha256((ROOT/'museum-notes/buddhist-sculpture/images/penn-741.jpg').read_bytes()).hexdigest()==a[741]['sha256']
for w in ws.values():
 assert w['visit_date'] is None
 assert len(w['paragraphs'])>=2 and w['sources']
 assert (base/w['slug']/'index.html').is_file()
 for n in set(w['photos']+w['labels']):assert w['id'] in a[n]['work_ids']
for x in a.values():
 if 'web_path' in x:
  assert (base/x['web_path']).is_file() and (base/x['thumbnail_path']).is_file()
 else:assert x['number'] in (741,742)
 if len(sys.argv)>1:assert hashlib.sha256((Path(sys.argv[1])/x['organized_path']).read_bytes()).hexdigest()==x['sha256']
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k not in ('href','src'):continue
   u=urlparse(v)
   if u.scheme or u.netloc:continue
   t=(ROOT/unquote(u.path).lstrip('/')) if u.path.startswith('/') else ((self.path.parent/unquote(u.path)).resolve() if u.path else self.path)
   if t.is_dir():t=t/'index.html'
   assert t.exists(),(self.path,v)
   if u.fragment:assert 'id="'+u.fragment+'"' in t.read_text(),(self.path,v)
paths=list((ROOT/'museum-notes').rglob('*.html'))
for path in paths:
 p=Links();p.path=path;p.feed(path.read_text())
t=json.loads((ROOT/'museum-notes/buddhist-sculpture/data/topics.json').read_text());assert t['selected_count']==59 and t['related_count']==1
print(f'PASS: 24+1 records, 45 photo mappings, shared identities, existing luohan reuse, 59+1 selected sculptures, {len(paths)} pages with valid local links.')
