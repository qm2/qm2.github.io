"""Check object identity, source/crop provenance and generated local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/roman-sarcophagi'
def load(name):return json.loads((BASE/f'data/{name}.json').read_text())
w=load('works');p=load('photos');s=load('sources');notes=load('editorial');chapters=load('sections');m=load('museums')
by={o['id']:o for o in w};sb={x['id'] for x in s}
assert len(w)==len(by)==24 and len(m)==8
assert Counter(i for c in chapters for i in c['works'])==Counter(by.keys())
assert len([x for x in p.values() if x.get('original')])==60
assert len([x for x in p.values() if x['role']=='label'])==23
assert p['1930']['object_ids']==['r24']
assert set(p['1931']['object_ids'])=={'r13','r23','r13-lid'}
assert by['r13']['photos']==by['r23']['photos']==[1931]
assert by['r20']['photos']==[1946,1947,1948,1949,1950]
assert by['r09']['accession'] is None
assert by['r16']['date_start']==150 and by['r16']['date_end']==180
assert all(o.get('visit_date') is None for o in w)
for k,photo in p.items():
 if photo.get('original'):
  raw=BASE/'images/originals'/photo['original'];assert raw.is_file();assert hashlib.sha256(raw.read_bytes()).hexdigest()==photo['sha256'];assert photo['object_ids'],k
 else:
  assert photo['source'] in p and len(photo['crop'])==4
  assert '原片局部' in photo['caption']
 for v in photo['variants']:
  assert (BASE/'images'/v['file']).is_file();assert v['width']<=photo['display_width']
for o in w:
 assert o['id'] in notes and o['cover'] in p
 assert o['museum_id'] in {x['id'] for x in m}
 assert set(o['source_ids'])<=sb
 assert all(str(n) in p for n in o['photos']+o['labels'])
 if o['date_kind']=='circa':assert o['date_start']==o['date_end']
for content in notes.values():
 for sec in content['sections']:
  for paragraph in sec['paragraphs']:assert set(paragraph.get('source_ids',[]))<=sb
history=load('history');comparisons=load('comparisons')
assert len(history['field_card']['questions'])==6
assert next(g for g in comparisons if g['id']=='battle-and-submission')['works']==['r11','r24']
for sec in history['sections']:
 assert set(sec['works'])<=set(by)
 if sec.get('image'):assert sec['image'] in p
 for paragraph in sec['paragraphs']+sec.get('after',[]):assert set(paragraph.get('source_ids',[]))<=sb
 if sec.get('table'):assert set(sec['table']['source_ids'])<=sb
for group in comparisons:
 for sec in group.get('sections',[]):
  for paragraph in sec['paragraphs']:assert set(paragraph.get('source_ids',[]))<=sb
 for paragraph in group.get('notes',[]):assert set(paragraph.get('source_ids',[]))<=sb
stories=load('stories')
assert len(stories['myths'])==9 and len(stories['contexts'])==5
entries=stories['myths']+stories['contexts'];entry_ids={x['id'] for x in entries}
assert len(entry_ids)==14
for entry in entries:
 assert set(entry['works'])<=set(by)
 paragraphs=([entry['story']]+entry['look']+entry['version']) if 'story' in entry else [entry['text']]
 for paragraph in paragraphs:assert set(paragraph.get('source_ids',[]))<=sb
 if 'story' in entry:
  assert 150<=len(entry['story']['text'])<=250
  assert 80<=len(entry['preview'])<=120
  assert 2<=len(entry['look'])<=3
 else:assert 100<=len(entry['text']['text'])<=180
for wid,context in stories['context_previews'].items():
 assert wid in by and context['entry'] in entry_ids
 assert 80<=len(context['text'])<=120
assert len(stories['muses']['rows'])==9
assert set(stories['muses']['source_ids'])<=sb
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.links=[];self.ids=[];self.images=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  for key in ['href','src','data-original']:
   if a.get(key):self.links.append(a[key])
  if a.get('srcset'):self.links.extend(x.strip().split()[0] for x in a['srcset'].split(','))
  if tag=='img':self.images.append(a)
parsed={f:Page(f.read_text()) for f in BASE.rglob('*.html')}
assert len(parsed)==29
for file,doc in parsed.items():
 assert len(doc.ids)==len(set(doc.ids)),file
 for img in doc.images:
  # Empty lightbox image is populated by the shared viewer.
  if img.get('id')=='large-photo':continue
  assert img.get('alt') and img.get('width') and img.get('height'),(file,img)
  assert not img.get('src','').startswith(('http:','https:'))
 for link in doc.links:
  url=urlsplit(link)
  if url.scheme or url.netloc:continue
  path=unquote(url.path)
  target=(ROOT/path.lstrip('/') if path.startswith('/') else file.parent/path).resolve() if path else file
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(file,link)
  if url.fragment and target.suffix=='.html':
   other=parsed.get(target) or Page(target.read_text());assert unquote(url.fragment) in other.ids,(file,link)
for o in w:
 text=(BASE/o['id']/'index.html').read_text()
 assert 'href="../history/"' in text and 'href="../stories/"' in text
 myth=next((x for x in stories['myths'] if o['id'] in x['works']),None)
 entry=myth['id'] if myth else stories['context_previews'].get(o['id'],{}).get('entry')
 if entry:assert f'href="../stories/#{entry}"' in text
for entry in entries:
 for wid in entry['works']:assert f'href="../{wid}/"' in (BASE/'stories/index.html').read_text()

assert 'history/#field-card' in (BASE/'atlas/index.html').read_text()
assert 'href="history/"' in (BASE/'index.html').read_text()
assert 'roman-sarcophagi/' in (ROOT/'museum-notes/index.html').read_text()
assert not list(BASE.rglob('*.pdf'))
print('Roman checks passed: 24 canonical records, 8 viewing institutions, 60 unchanged originals, 5 honest crops, 29 pages; sources, date types, identity corrections and local links valid.')
