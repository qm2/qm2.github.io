"""Verify Homer photo provenance, counts, metadata corrections and generated local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/homer'
load=lambda n:json.loads((BASE/'data'/f'{n}.json').read_text())
w=load('works');p=load('photos');d=load('derivatives');s=load('editorial_shortlist')
assert len(w)==67 and len(p)==215 and len(s)==35
assert sum(a['presentation']=='deep-dive' for a in w)==15
assert sum(a['presentation']=='gallery-card' for a in w)==20
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
print(f'Homer checks passed: 215 unchanged originals, 67 matched records, 35 selected (15/20), {len(parsed)} pages, {len(d)} responsive photo sets; local links and corrections checked.')

edit=load('editorial');sections=load('sections')
assert edit['hero']['photo']==179 and wb[11]['display_photo']==11
assert {a['photo'] for a in w if a.get('featured')}=={11,62,3,17,58,74,72,50,146,76,56}
assert len(sections)==7 and sections[0]['works']==[95,13,46]
assert len({n for section in sections for n in section['works']})==35
assert wb[15]['section']=='finale'
assert len(edit['techniques'])==4
from PIL import Image,ImageOps
for crop in edit['crops']:
 row=d[crop['id']];source=ImageOps.exif_transpose(Image.open(BASE/row['source_original'])).convert('RGB')
 actual=Image.open(BASE/row['original']).convert('RGB')
 assert actual.tobytes()==source.crop(tuple(row['crop_box'])).tobytes(),crop['id']
print('Refinement checks passed: 35 selections, eleven featured works, four technique examples; lossless editorial crops match unchanged originals.')

assert edit['favorites']['works']==[11,76,56,146,50]
assert wb[56]['year']=='1897' and wb[56]['display_photo']==188 and 52 not in edit['favorites']['works']
assert wb[50]['medium']=='Oil on canvas' and wb[50]['accession']=='53.2552' and wb[50]['display_photo']==210
assert wb[146]['year']=='1882' and wb[146]['accession']=='48.727' and wb[146]['display_photo']==194
assert wb[50]['photo'] in wb[50]['detail_photos'] and wb[146]['photo'] in wb[146]['detail_photos']
assert all(wb[n].get('featured') and wb[n].get('personal_favorite') for n in edit['favorites']['works'])
print('Personal selection checked: five distinct works, 1897 fishing scene, two new featured works and their original views.')

expected_details={11:179,76:191,56:189,146:195,50:211}
for n,photo in expected_details.items():
 assert wb[n]['reading_detail']['photo']==photo
 assert photo in wb[n]['detail_photos'] and photo!=wb[n]['display_photo']
 assert pb[photo]['folder']==pb[n]['folder']
 assert wb[n]['reading_detail']['caption'] and wb[n]['reading_detail']['text']
assert [wb[n]['display_photo'] for n in edit['favorites']['works']]==[11,190,188,194,210]
print('Detail guide checked: five own detail photos; all five complete-composition displays unchanged.')
