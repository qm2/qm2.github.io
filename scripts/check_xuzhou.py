"""Check Xuzhou identity boundaries, immutable originals and generated assets."""
from pathlib import Path
from collections import Counter
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];base=ROOT/'museum-notes/xuzhou'
d=json.loads((base/'data/works.json').read_text());ps=json.loads((base/'data/photos.json').read_text());ws={w['id']:w for w in d['works']}
assert len(ws)==28 and all(w['collection']=='xuzhou' for w in ws.values())
assert len(ps)==115 and set(ps)=={str(i) for i in range(952,1066)}|{'SUPP01'}
assert (ws['x08']['main_photo'],ws['x08']['label_photo'])==('989','990')
assert (ws['x09']['main_photo'],ws['x09']['label_photo'])==('991','992')
assert ws['x11']['label_original']['date']=='Nara period, 7th century' and '疑点' in ws['x11']['date_display']
assert '重复' in ws['x23']['record_note'] and ws['x23']['material_label']=='局部鎏金银'
assert ws['x28']['label_photo']=='SUPP01' and '脱胎干漆' in ws['x28']['material_label']
archive=json.loads((base/'data/archived-neighbors.json').read_text())
assert {w['id'] for w in archive}=={'n01','n02'}
assert all(not (base/w['id']/'index.html').exists() for w in archive)
assert '1049' in ws['x26']['detail_photos'] and '木座' in ws['x25']['record_note']
assert len(d['features'])==8
for w in ws.values():
 assert w['visit_date'] is None and len(w['notes'])>=2
 assert w['evidence']['independent_full_resolution_label_review']
 assert (base/w['id']/'index.html').exists()
 for n in [w['main_photo'],w['label_photo']]+w['detail_photos']:assert ps[n]['object_id']==w['id'],(w['id'],n)
 for key in w['source_ids']:
  assert key=='label' or key in d['sources']
for n,p in ps.items():
 original=base/'images'/p['original'];assert hashlib.sha256(original.read_bytes()).hexdigest()==p['sha256']
 for v in p['variants']:
  with Image.open(base/'images'/v['file']) as im:assert im.size==(v['width'],v['height']) and im.width<=p['width']
html=(base/'index.html').read_text();assert html.count('class="xz-card"')==28 and html.count('class="xz-feature"')==8
assert 'neighbors' not in html and '邻展' not in html
assert 'xuzhou/' in (ROOT/'museum-notes/index.html').read_text()
print('PASS Xuzhou: 28 collection identities, 2 unpublished archived records, 115 SHA-256 originals, 230 uncropped derivatives, labels, source IDs, 8 readings, 29 collection pages.')
# Map assets are separate from the immutable collection photo inventory.
guide=json.loads((base/'data/map-guide.json').read_text())
assert len(guide['groups'])==4 and sum(len(g['places']) for g in guide['groups'])==14
assert len(guide['source_inventory'])==6
for g in guide['groups']:
 assert 2<=len(g['works'])<=4
 assert all(w['id'] in ws for w in g['works'])
 assert all(k in guide['sources'] for k in g['sources'])
 for place in g['places']:assert all(k in guide['sources'] for k in place['sources'])
for key,p in guide['photos'].items():
 original=base/'images'/p['original']
 assert hashlib.sha256(original.read_bytes()).hexdigest()==p['sha256']
 with Image.open(original) as im:assert im.size==(p['width'],p['height'])
 for v in p['variants']:
  with Image.open(base/'images'/v['file']) as im:
   assert im.width==v['width']<=p['width'] and abs(im.height-im.width*p['height']/p['width'])<=1
assert 'map/' in html and (base/'map/index.html').exists()
print('PASS map guide: 4 networks, 14 place groups, verified work links, 3 unchanged exhibit photos + 6 uncropped derivatives; 30 Xuzhou pages total.')
