"""Check published identity/photo references and isolated future-growth behaviour."""
import copy
import hashlib
import json
import shutil
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from PIL import Image, ImageOps
from build_himalayan import BASE, ROOT, build

read = lambda name: json.loads((BASE/'data'/f'{name}.json').read_text())
works, photos, units = read('works'), read('photos'), read('reading_units')
wb = {w['work_id']: w for w in works}
pb = {p['photo_id']: p for p in photos}
assert len(wb) == len(works) and len(pb) == len(photos)
assert all(w['public'] for w in works)
assert not {'w1486','w1514','w1625','w1627','w1717'} & wb.keys()
assert not {'h1486','h1487','h1514','h1515','h1625','h1626','h1627','h1628','h1717','h1718'} & pb.keys()
assert set(p.stem for p in (BASE/'images/originals').glob('*')) == pb.keys()
assert all(not p['do_not_publish'] and p['public_asset'] for p in photos)
allowed = {n for w in works for n in w['art_photos'] + w['detail_photos'] + [w['primary_photo']]}
assert allowed == pb.keys(), 'Only mapped artwork photos may be published'
sources = {s['source_id'] for s in read('sources')}
for w in works:
    assert all(s in sources for s in w['source_ids'])
    assert (BASE/w['primary_path']).is_file() and (BASE/w['thumbnail_path']).is_file()
    assert (BASE/w['work_id']/'index.html').is_file()
for u in units:
    assert all(w in wb for w in u['work_ids'])
    assert (BASE/u['unit_id']/'index.html').is_file()
for p in photos:
    path = BASE/p['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == p['sha256'], path
    im = ImageOps.exif_transpose(Image.open(path))
    for size in [400,900,1600]:
        d = Image.open(BASE/'images'/f'{p["photo_id"]}-{size}.webp')
        assert d.width == min(im.width, size) and abs(d.height/d.width-im.height/im.width) < .005
assert wb['w1563']['accession'] == '1964.103' and wb['w1563']['date_end'] == 1310
assert wb['w1552']['accession'] == '1964.370'
assert wb['w1651']['accession'] == '48.166'
assert wb['w1700']['accession'] == 'AP 1979.01'
assert wb['w1664']['accession'] == '44-18' and wb['w1664']['tier'] == 'focus'
assert wb['w1478']['materials_display'] == '布本胶彩'
assert wb['w1711']['date_label'] == '15世纪'
assert not wb['w1689']['map_enabled'] and not wb['w1689']['display_museum_id']
assert len(wb['w1692']['detail_photos']) == 4
for wid in ['w1623','w1641','w1645']:
    assert wb[wid]['collection_museum_id'] == 'rubin' and wb[wid]['display_museum_id'] == 'seattle'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.ids=set(); self.links=[]; self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        for k in ['href','src']:
            if a.get(k): self.links.append(a[k])
        if a.get('srcset'): self.links += [v.strip().split()[0] for v in a['srcset'].split(',')]
        if tag == 'img' and a.get('src'): assert a.get('alt'), 'Missing alternative text'

cache={}
pages=list(BASE.rglob('index.html'))
for path in pages:
    page=cache.setdefault(path, Page(path))
    for href in page.links:
        u=urlsplit(href)
        if u.scheme or u.netloc: continue
        target=(ROOT/u.path.lstrip('/') if u.path.startswith('/') else path.parent/unquote(u.path)).resolve()
        if target.is_dir(): target /= 'index.html'
        assert target.is_file(), (path, href)
        if u.fragment and target.suffix == '.html':
            other=cache.setdefault(target, Page(target))
            assert unquote(u.fragment) in other.ids, (path, href)
print(f'PASS: {len(works)} records, {len(photos)} original hashes, responsive ratios, {len(pages)} pages and all local links.')

# Future entries are exercised in a disposable copy; existing photos are copied,
# never edited. No fixture can leak into public data or the root entrance.
with tempfile.TemporaryDirectory(prefix='himalayan-growth-') as tmp:
    fixture=Path(tmp)/'himalayan-art'
    shutil.copytree(BASE, fixture)
    save=lambda n,d:(fixture/'data'/f'{n}.json').write_text(json.dumps(d,ensure_ascii=False))
    ws=copy.deepcopy(works); ps=copy.deepcopy(photos)
    museums=read('museums'); places=read('places')
    museums.append({'museum_id':'test-museum','label_zh':'测试馆','name_en':'Fixture','city':'Test','latitude':32,'longitude':-98})
    places.append({'place_id':'test-region','label_zh':'测试地区','latitude':28,'longitude':86,'precision':'region'})
    new=copy.deepcopy(ws[0]); new.update(work_id='test-new-work', title_zh='测试新作', tier='catalogue', reading_unit_ids=[],chapter_ids=[],region_ids=['test-region'],display_museum_id='test-museum',collection_museum_id='test-museum',collection_label='测试馆',map_associations=[{'place_id':'test-region','relationship':'regional_attribution','certainty':'regional_only'}])
    ws.append(new)
    revisit=copy.deepcopy(ps[0]); revisit.update(photo_id='test-revisit', path='images/originals/test-revisit.jpg',thumbnail_path='images/test-revisit-400.webp',work_ids=[ws[0]['work_id']],visit_id='test-visit')
    shutil.copyfile(BASE/ps[0]['path'],fixture/revisit['path']);ps.append(revisit)
    ws[0]['art_photos'].append(revisit['photo_id'])
    for n,d in [('works',ws),('photos',ps),('museums',museums),('places',places),('visits',[{'visit_id':'test-visit','work_id':ws[0]['work_id']}])]: save(n,d)
    build(fixture, integrate=False)
    nav=json.loads((fixture/'data/navigation.json').read_text()); html=(fixture/'index.html').read_text()
    assert len(nav['works']) == len(works)+1
    assert any(g['id']=='test-region' for g in nav['groups'])
    assert 'data-museum="test-museum"' in html and 'data-region="test-region"' in html
    assert 'test-revisit.jpg' in (fixture/ws[0]['work_id']/'index.html').read_text()
    assert all((fixture/w['work_id']/'index.html').exists() for w in works)
    assert (fixture/'test-new-work/index.html').exists()
assert not (BASE/'test-new-work').exists()
print('PASS: new work, new institution/region, revisit photo, stable old URLs; fixtures removed.')
