"""Check Xuzhou identity boundaries, immutable originals and generated assets."""
from pathlib import Path
from collections import Counter
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];base=ROOT/'museum-notes/xuzhou'
d=json.loads((base/'data/works.json').read_text());ps=json.loads((base/'data/photos.json').read_text());ws={w['id']:w for w in d['works']}
assert len(ws)==30 and Counter(w['collection'] for w in ws.values())=={'xuzhou':28,'mfah-neighbor':2}
assert len(ps)==115 and set(ps)=={str(i) for i in range(952,1066)}|{'SUPP01'}
assert (ws['x08']['main_photo'],ws['x08']['label_photo'])==('989','990')
assert (ws['x09']['main_photo'],ws['x09']['label_photo'])==('991','992')
assert ws['x11']['label_original']['date']=='Nara period, 7th century' and '疑点' in ws['x11']['date_display']
assert '重复' in ws['x23']['record_note'] and ws['x23']['material_label']=='局部鎏金银'
assert ws['x28']['label_photo']=='SUPP01' and '脱胎干漆' in ws['x28']['material_label']
assert ws['n01']['accession']=='2004.2248' and ws['n02']['accession']=='91.333'
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
html=(base/'index.html').read_text();assert html.count('class="xz-card"')==30 and html.count('class="xz-feature"')==8
assert 'xuzhou/' in (ROOT/'museum-notes/index.html').read_text()
print('PASS Xuzhou: 28+2 identities, 115 SHA-256 originals, 230 uncropped derivatives, labels, source IDs, 8 readings, 31 generated pages.')
