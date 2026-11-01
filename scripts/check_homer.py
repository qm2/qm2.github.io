"""Verify Homer photo provenance, counts, metadata corrections and generated local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/homer'
load=lambda n:json.loads((BASE/'data'/f'{n}.json').read_text())
w=load('works');p=load('photos');d=load('derivatives');s=load('editorial_shortlist')
assert len(w)==67 and len(p)==215 and len(s)==33
assert sum(a['presentation']=='deep-dive' for a in w)==12
assert sum(a['presentation']=='gallery-card' for a in w)==21
assert {a['slug'] for a in s}=={a['slug'] for a in w if a['presentation']!='archive'}
pb={a['id']:a for a in p};wb={a['photo']:a for a in w}
for photo in p:
 f=BASE/photo['original'];assert f.is_file();assert hashlib.sha256(f.read_bytes()).hexdigest()==photo['sha256']
for a in w:
 assert pb[a['photo']]['kind']=='main' and pb[a['label']]['kind']=='label'
 assert pb[a['display_photo']]['folder']==pb[a['photo']]['folder']
 assert all(pb[n]['folder']==pb[a['photo']]['folder'] for n in a['detail_photos'])
 assert len(a['detail_photos'])<=3 and a['display_photo'] not in a['detail_photos']
 assert a['material_cn'] and a['collection'] and a['title_cn']
 n=sum(len(t) for t in a['paragraphs'])
 if a['presentation']=='deep-dive':assert 120<=n<=250,(a['slug'],n)
 if a['presentation']!='archive':
  assert a['home_note'] and a['home_note'] not in a['paragraphs']
  assert n>0
 assert (BASE/a['slug']/'index.html').is_file()
assert wb[154]['year']=='1885' and wb[151]['year']=='1881–82' and wb[136]['year']=='1887'
assert wb[157]['year']=='c. 1886' and wb[171]['year']=='1883'
assert 'John Parker Davis' in wb[97]['artist'] and 'Crows' in wb[97]['title']
assert all('佚名' in wb[n]['artist'] and 'after Winslow Homer' in wb[n]['artist'] for n in [99,107])
assert wb[46]['collection']==wb[173]['collection']=='私人收藏'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.urls=[];self.ids=[];self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='img':
   self.images.append(a);assert 'alt' in a and (a['alt'] or a.get('id')=='large-photo')
  for key in ['src','href']:
   if key in a:self.urls.append(a[key])
  for v in a.get('srcset','').split(','):
   if v.strip():self.urls.append(v.strip().split()[0])
parsed={}
for f in BASE.rglob('*.html'):
 parser=Parser();parser.feed(f.read_text());parsed[f]=parser;assert len(parser.ids)==len(set(parser.ids)),f
 for im in parser.images:
  if 'src' in im:assert not im['src'].startswith('http'),(f,im)
for f,parser in parsed.items():
 for url in parser.urls:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  path=(f.parent/unquote(u.path)).resolve() if u.path else f
  if path.is_dir():path=path/'index.html'
  assert path.exists(),(f,url,path)
  if u.fragment and path in parsed:assert unquote(u.fragment) in parsed[path].ids,(f,url)
for row in d.values():
 for v in row['variants']:
  assert (BASE/v['path']).is_file();assert v['width']<=row['width']
assert len(parsed)==68
print(f'Homer checks passed: 215 unchanged originals, 67 matched records, 33 selected (12/21), {len(parsed)} pages, {len(d)} responsive photo sets; local links and corrections checked.')

edit=load('editorial');sections=load('sections')
assert edit['hero']['photo']==179 and wb[11]['display_photo']==11
assert {a['photo'] for a in w if a.get('featured')}=={11,62,3,17,58,74,72}
assert len(sections)==7 and sections[0]['works']==[95,13,46]
assert len({n for section in sections for n in section['works']})==33
assert wb[15]['section']=='finale'
assert len(edit['techniques'])==4
from PIL import Image,ImageOps
for crop in edit['crops']:
 row=d[crop['id']];source=ImageOps.exif_transpose(Image.open(BASE/row['source_original'])).convert('RGB')
 actual=Image.open(BASE/row['original']).convert('RGB')
 assert actual.tobytes()==source.crop(tuple(row['crop_box'])).tobytes(),crop['id']
print('Refinement checks passed: 33 selections, seven featured works, four technique examples; lossless editorial crops match unchanged originals.')
