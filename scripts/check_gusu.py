"""Check Gusu's work/group identity, photo ledger, generated links and derivatives."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/gusu-prints'
class Page(HTMLParser):
 def __init__(self,p):
  super().__init__();self.ids=[];self.links=[];self.images=[];self.text=[];self.feed(p.read_text())
 def handle_data(self,s):self.text.append(s)
 def handle_starttag(self,t,pairs):
  a=dict(pairs)
  if a.get('id'):self.ids.append(a['id'])
  for k in ['href','src']:
   if a.get(k):self.links.append(a[k])
  if a.get('srcset'):self.links.extend(s.strip().split()[0] for s in a['srcset'].split(','))
  if t=='img':self.images.append(a)
def check():
 load=lambda n:json.loads((BASE/'data'/f'{n}.json').read_text())
 works=load('works');assets=load('assets');images=load('derivatives');by={w['id']:w for w in works}
 assert len(works)==len(by)==32
 assert len(assets)==129 and {a['photo_number'] for a in assets}==set(range(2945,3074))
 for w in works:
  assert w['main_photo'] in w['full_photos'],w['id']
  for n in w['full_photos']+w['detail_photos']+w['label_photos']:
   a=next(a for a in assets if a['photo_number']==n)
   assert any(m['work_id']==w['id'] for m in a['memberships']),(w['id'],n)
 assert [by[x]['accessions'] for x in ['g26','g27','g28','g30']]==[['2025.48'],['2025.46'],['2025.49'],['2025.47']]
 assert by['b02']['accessions']==['1984.45'] and len(by['b02']['full_photos'])==13
 assert len(by['g02']['accessions'])==2 and len(by['g29']['accessions'])==1
 referenced_files=set()
 for key,im in images.items():
  file=BASE/im['full'];referenced_files.add(file)
  with Image.open(file) as pic:assert pic.size==(im['width'],im['height']),(key,pic.size)
  for v in im['variants']:
   file=BASE/v['path'];referenced_files.add(file)
   with Image.open(file) as pic:
    assert pic.size==(v['width'],v['height']),file
    assert pic.width<=im['width'] and pic.height<=im['height'],file
   if file!=BASE/im['full']:assert file.stem.endswith('-'+str(v['width'])),file
 assert referenced_files==set((BASE/'images').glob('*.webp'))
 assert not list(BASE.rglob('*.jpg'))
 pages={p.resolve():Page(p) for p in BASE.rglob('index.html')};assert len(pages)==37
 used=set()
 for p,doc in list(pages.items()):
  assert len(doc.ids)==len(set(doc.ids)),p
  for im in doc.images:
   if im.get('id')=='large-photo':continue
   assert im.get('alt') and im.get('width') and im.get('height'),(p,im)
   assert not im['src'].startswith('http'),p
  for url in doc.links:
   u=urlsplit(url)
   if u.scheme or u.netloc or not u.path and not u.fragment:continue
   target=(ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)).resolve() if u.path else p
   if target.is_dir():target=target/'index.html'
   assert target.exists(),(p,url,target)
   if u.fragment and target.suffix=='.html':
    if target not in pages:pages[target]=Page(target)
    assert unquote(u.fragment) in pages[target].ids,(p,url)
   used.update(int(n) for n in re.findall(r'/p(\d{4})(?:-|\.)',url))
  assert not re.search(r'\[(?:S\d+|L\d+)\]|\bp\d{4}\b|(?<![A-Za-z0-9])[gb]\d{2}(?![A-Za-z0-9])|CODEX|source_ids|网页应|文字应说|本包','\n'.join(doc.text)),p
 assert used==set(range(2945,3074)),set(range(2945,3074))-used
 for path,marker in [('museum-notes/index.html','gusu-home'),('museum-notes/chinese-painting/index.html','gusu-related')]:assert (ROOT/path).read_text().count('<!-- '+marker+' -->')==1
 print('PASS: 32 records, 129 photographs, 37 pages; mappings, sources, internal links, responsive sizes and entrances.')
if __name__=='__main__':check()
