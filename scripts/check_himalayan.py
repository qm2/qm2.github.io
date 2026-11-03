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
assert not {'w1514','w1625','w1627','w1717'} & wb.keys()
assert wb['w1486']['himalayan_default_inclusion'] is False
assert read('work_aliases')['w1514']=='w1486'
assert not {'h1487','h1515','h1625','h1626','h1627','h1628','h1717','h1718'} & pb.keys()
assert set(p.stem for p in (BASE/'images/originals').glob('*')) == pb.keys()
assert all(not p['do_not_publish'] and p['public_asset'] for p in photos)
allowed = {n for w in works for n in w['art_photos'] + w['detail_photos'] + [w['primary_photo']]}
assert allowed == pb.keys(), 'Only mapped artwork photos may be published'
sources = {s['source_id'] for s in read('sources')}
crops={c['crop_id']:c for c in read('photo_crops')}
assert len(crops)==len(read('photo_crops'))
for c in crops.values():
    assert c['photo_id'] in allowed and c['work_id'] in wb
    assert c['photo_id'] in wb[c['work_id']]['art_photos']+wb[c['work_id']]['detail_photos']
    original=ImageOps.exif_transpose(Image.open(BASE/pb[c['photo_id']]['path'])).convert('RGB')
    x0,y0,x1,y1=c['box']; assert 0<=x0<x1<=original.width and 0<=y0<y1<=original.height
    target=BASE/'images/details'/f'{c["crop_id"]}.webp'
    assert Image.open(target).size==(x1-x0,y1-y0)
    from io import BytesIO
    expected=BytesIO();original.crop(c['box']).save(expected,'WEBP',quality=91,method=5)
    assert target.read_bytes()==expected.getvalue(), 'Crop must be an unretouched derivative of the identified original'
assert {p.stem for p in (BASE/'images/details').glob('*')}==crops.keys()
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
assert wb['w1552']['reading_unit_ids'] == ['u25'] and wb['w1552']['tier']=='focus'
assert wb['w1552']['dimensions_display']=='整体78.1 × 67.6厘米'
assert '有色玻璃' in wb['w1484']['materials_display']
history=read('history'); node_ids=set()
for track in history['tracks']:
    for n in track['nodes']:
        assert n['id'] not in node_ids; node_ids.add(n['id'])
        assert len(n['keywords'])==3 and n['related']
        assert all(r['work_id'] in wb for r in n['related'])
        for p in n['paragraphs']: assert set(p['source_ids'])<=sources
        assert n['review']['remember']
        for p in n['review']['points']:assert set(p['source_ids'])<=sources
        for r in n['related']:
            assert f'../history/#{n["id"]}' in (BASE/r['work_id']/'index.html').read_text()
for u in units:
    for section in u.get('sections',[])+u.get('notes',[]):
        for p in section['paragraphs']:assert set(p['source_ids'])<=sources
        assert set(section.get('crop_ids',[]))<=crops.keys()
assert wb['w1651']['accession'] == '48.166'
assert wb['w1700']['accession'] == 'AP 1979.01'
assert wb['w1664']['accession'] == '44-18' and wb['w1664']['tier'] == 'focus'
assert wb['w1478']['materials_display'] == '布本胶彩'
assert wb['w1711']['date_label'] == '15世纪'
assert not wb['w1689']['map_enabled'] and wb['w1689']['display_museum_id']=='nmaa'
assert wb['w1689']['collection_museum_id']=='nmaa'
assert len(wb['w1692']['detail_photos']) == 4
intro=read('introduction')
home=(BASE/'index.html').read_text()
assert all(p in home for p in intro['paragraphs']) and len(intro['paragraphs'])==3
assert home.index('class="ha-cover"') < home.index('id="preface"') < home.index('id="places"')
assert '曾缄译《六世达赖情歌六十六首》其一节选' in home
assert '夏嘎巴' not in home
assert ('id="recent-notes"' in home)==any(u.get('public',False) for u in read('updates'))
for unit in units:
    html=(BASE/unit['unit_id']/'index.html').read_text()
    assert html.count('data-comparison=')==len(unit['comparison_work_ids'])
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
    fixture_visits=[{'visit_id':'test-visit','work_id':ws[0]['work_id'],'visited_on':None,'photo_ids':['test-revisit'],'observation':'测试重访观察：同一件作品保留原编号。','public':True},
        {'visit_id':'test-two-questions','work_id':ws[1]['work_id'],'visited_on':None,'photo_ids':[], 'confirmed':'测试确认内容','still_unclear':'测试尚未看清内容','public':True},
        {'visit_id':'test-private','work_id':ws[2]['work_id'],'photo_ids':[],'confirmed':'不应公开的测试记录','public':False},
        {'visit_id':'test-empty','work_id':ws[3]['work_id'],'photo_ids':[],'confirmed':' ','still_unclear':'','public':True}]
    fixture_updates=[{'update_id':'test-update','published_on':'2026-11-03','kind':'revisit','work_id':ws[0]['work_id'],'visit_id':'test-visit','summary':'测试重访记录','public':True},
        {'update_id':'test-two-question-update','published_on':'2026-11-03','kind':'revisit','work_id':ws[1]['work_id'],'visit_id':'test-two-questions','summary':'测试两句重访札记','public':True}]
    for n,d in [('works',ws),('photos',ps),('museums',museums),('places',places),('visits',fixture_visits),('updates',fixture_updates)]: save(n,d)
    build(fixture, integrate=False)
    nav=json.loads((fixture/'data/navigation.json').read_text()); html=(fixture/'index.html').read_text()
    assert len(nav['works']) == sum(w.get('himalayan_default_inclusion',True) for w in works)+1
    assert any(g['id']=='test-region' for g in nav['groups'])
    assert 'data-museum="test-museum"' in html and 'data-region="test-region"' in html
    assert 'test-revisit.jpg' in (fixture/ws[0]['work_id']/'index.html').read_text()
    assert all((fixture/w['work_id']/'index.html').exists() for w in works)
    assert (fixture/'test-new-work/index.html').exists()
    assert 'data-update="test-update"' in html and '#visit-test-visit' in html
    record=(fixture/ws[0]['work_id']/'index.html').read_text()
    assert '测试重访观察：同一件作品保留原编号。' in record
    assert '<article id="visit-test-visit"><p>' in record, 'Do not invent a visit date'
    note=(fixture/ws[1]['work_id']/'index.html').read_text()
    assert '<h3>这次确认了什么</h3><p>测试确认内容</p>' in note
    assert '<h3>还有什么没看清</h3><p>测试尚未看清内容</p>' in note
    assert '#visit-test-two-questions' in html, 'Structured notes alone must be reachable from updates'
    assert '<article id="visit-test-two-questions"><h3>' in note, 'No assumed visit date or filler prose'
    assert '不应公开的测试记录' not in (fixture/ws[2]['work_id']/'index.html').read_text()
    assert 'visit-test-empty' not in (fixture/ws[3]['work_id']/'index.html').read_text()
    save('updates',[]);build(fixture, integrate=False)
    assert 'id="recent-notes"' not in (fixture/'index.html').read_text()
assert not (BASE/'test-new-work').exists()
print('PASS: new work/institution/region, revisit photo and observation, recent updates, hidden empty state, stable URLs; fixtures removed.')
