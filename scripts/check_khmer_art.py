"""Check coverage, exceptional photo pairings, navigation and dated contexts."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/khmer-art'
def load(n):return json.loads((BASE/'data'/n).read_text())
class Page(HTMLParser):
 def __init__(self,text):self.ids=[];self.urls=[];self.imgs=[];super().__init__();self.feed(text)
 def handle_starttag(self,t,a):
  d=dict(a)
  if d.get('id'):self.ids.append(d['id'])
  if d.get('href'):self.urls.append(d['href'])
  if d.get('src'):self.urls.append(d['src'])
  if t=='img':self.imgs.append(d)
def main():
 works=load('objects.json');by={w['id']:w for w in works};media=load('media.json');manifest=load('photo_manifest.json');readings=load('readings.json');sources={s['id'] for s in load('sources.json')}
 assert len(works)==len(by)==58 and len(media)==len(manifest)==120
 assert len(load('museums.geojson')['features'])==11 and len(readings)==6
 assert set(int(k) for k in media if k.isdigit())==set(range(3534,3652))
 assert set(k for k in media if not k.isdigit())=={'k03-front','k03-label'}
 for m in manifest:
  assert media[str(m.get('key') or m['number'])]['sha256']==m['sha256']
  assert all(a['record_id'] in by for a in m['assignments'])
 for w in works:
  assert w['visit_date'] is None
  assert all(str(n) in media for n in w.get('image_keys',w['image_numbers'])+w.get('label_keys',w['label_numbers']))
  assert all(s in sources for s in w['source_ids'])
  if w['record_kind'] in ['historic_cast','historic_model']:assert w['timeline_lane']=='modern_display'
 assert by['C09']['image_numbers']==by['C11']['image_numbers']==[3610]
 assert by['C10']['image_numbers']==[] and by['C10']['label_numbers']==[3612]
 assert by['O06']['year_start'] is None
 assert by['M02']['accession']=='67.234' and by['K01']['accession']=='AP 1965.01'
 assert by['W03']['owner']!=by['W03']['museum_seen'] and by['W01']['owner']!=by['W01']['museum_seen']
 assert by['H01']['owner']!=by['H01']['museum_seen']
 for f in ['origins.geojson','museums.geojson']:
  for x in load(f)['features']:
   assert all(i in by for i in x['properties']['record_ids']+x['properties'].get('related_record_ids',[]))
 details=load('details.json');assert len(details)==8
 for d in details:
  m=media[d['photo']];assert d['source_sha256']==m['sha256']
  x0,y0,x1,y1=d['box'];assert 0<=x0<x1<=m['width'] and 0<=y0<y1<=m['height']
  assert d['width']==x1-x0 and d['height']==y1-y0 and d['max_width']<=d['width']
  assert all(v['width']<=d['width'] for v in d['variants'])
 assert by['G02']['display_components'][0]['accession']=='MA 5063'
 assert by['G02']['timeline_lane']=='modern_display'
 assert all(t.get('date_display') and t['era'] in ['ancient','modern'] for t in load('context_timeline.json'))
 cache={};bad=[];pages=list(BASE.rglob('index.html'));assert len(pages)==69,len(pages)
 for p in pages:
  h=Page(p.read_text());assert len(h.ids)==len(set(h.ids)),(p,'duplicate ids')
  assert all(im.get('alt') and im.get('width') and im.get('height') for im in h.imgs if im.get('id')!='large-photo'),p
  for u in h.urls:
   x=urlsplit(u)
   if x.scheme or x.netloc:continue
   dest=(ROOT/x.path.lstrip('/') if x.path.startswith('/') else p.parent/x.path).resolve() if x.path else p
   if dest.is_dir():dest=dest/'index.html'
   if not dest.exists():bad.append((p,u,'missing file'));continue
   if x.fragment:
    if dest not in cache:cache[dest]=Page(dest.read_text()).ids
    if unquote(x.fragment) not in cache[dest]:bad.append((p,u,'missing anchor'))
 assert not bad,bad
 s=(BASE/'sources/index.html').read_text();assert all(f'id="P{n}"' in s for n in media)
 assert not list(BASE.rglob('*.jpg')) and not list(BASE.rglob('*.webp'))
 home=(ROOT/'museum-notes/index.html').read_text();assert home.count('<!-- khmer-art -->')==1
 for a in readings:
  text=(BASE/a['id']/'index.html').read_text()
  assert len(a['sections'])>=3 and len(''.join(p for s in a['sections'] for p in s['paragraphs']))>400
  for phrase in ['用户最喜欢','这里可以保留用户','照片顺序：','本包不','待用户阅读认可']:
   assert phrase not in text,(a['id'],phrase)
 print('PASS: 69 pages; 58 records / 120 photos / 11 viewing museums; full coverage, photo exceptions, ownership, timeline lanes and internal links.')
if __name__=='__main__':main()
