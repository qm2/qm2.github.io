"""Validate stable object/image mappings, responsive files and all local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'museum-notes/ten-kings'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links, self.images = path, [], [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if a.get('id'): self.ids.append(a['id'])
        for key in ['href', 'src']:
            if a.get(key): self.links.append(a[key])
        if a.get('srcset'):
            self.links.extend(x.strip().split()[0] for x in a['srcset'].split(','))
        if tag == 'img': self.images.append(a)


def check():
    works = json.loads((BASE/'data/works.json').read_text())
    photos = json.loads((BASE/'data/photos.json').read_text())
    comparisons = json.loads((BASE/'data/comparisons.json').read_text())
    pairings = json.loads((BASE/'data/parallel_readings.json').read_text())
    by = {w['id']: w for w in works}
    for w in works:
        order = w.get('reading_order', list(range(1, len(w['sections']) + 1)))
        assert sorted(order) == list(range(1, len(w['sections']) + 1)), w['id']
    assert len({p['id'] for p in pairings}) == len(pairings)
    for pair in pairings:
        assert all(work in by for work in pair['pages'])
        for item in pair['items']:
            work = by[item['work']]
            assert item['photo'] in work['photo_indices'], item
            assert str(item['photo']) in photos, item
            assert item['target'].startswith('reading-' + work['id'] + '-'), item
    assert len(works) == len(by) == 26
    assert sum(w['category'] != 'object' for w in works) == 20
    assert by['dunhuang']['accession'] == '1919,0101,0.80'
    assert (by['dunhuang']['full'], by['dunhuang']['label']) == (97, 115)
    assert by['leeum_ksitigarbha_entourage']['full'] == 118
    assert by['leeum_ksitigarbha_entourage']['visit_id'] == 'cma-2026-11'
    expected = [(9,13),(16,21),(24,29),(32,36),(39,46),(49,55),(58,64),(67,71),(74,78),(81,88)]
    for i, (full, label) in enumerate(expected, 1):
        w = by[f'k{i:02}']
        assert (w['full'],w['label']) == (full,label)
        assert all(s.get('photo',full) in w['photo_indices'] for s in w['sections'])
    assert by['ksitigarbha_cma']['accession']=='2025.141'
    assert by['k04']['accession']=='2019.224'
    assert by['freer_ksitigarbha']['accession']=='S1992.11'
    assert '释迦' in by['leeum_sakyamuni_16_arhats']['name']
    assert '13世纪' in by['met_amitabha_triad']['date'] and '14世纪末' in by['met_amitabha_triad']['date']
    assert len(comparisons) == 1
    c = comparisons[0]
    assert c['id'] == 'leeum-amitabha-national-treasure-218'
    assert c['full'] == 'leeum-218-full' and c['label'] == 'leeum-218-label'
    assert c['id'] not in by and c['full'] != str(by['leeum_amitabha_kshitigarbha_avalok']['full'])
    assert [v['mode'] for v in c['viewings']] == ['原作','数字影像']
    referenced = set()
    for p in photos.values():
        assert (BASE/p['full']).exists()
        for v in p['variants']:
            f=BASE/v['path']; referenced.add(f.resolve())
            with Image.open(f) as im:
                assert im.size == (v['width'],v['height']), f
            assert f.stem.endswith('-'+str(v['width'])), f
    assert referenced == {p.resolve() for p in (BASE/'images').glob('*.webp')}
    assert not list(BASE.rglob('*.jpg')) and not list(BASE.rglob('*.csv'))
    assert not any('contact' in p.name or 'original_photos' in str(p) for p in BASE.rglob('*'))
    pages={p.resolve():Page(p) for p in BASE.rglob('*.html')}
    assert len(pages)==17
    for p, doc in list(pages.items()):
        assert len(doc.ids)==len(set(doc.ids)), p
        for im in doc.images:
            if im.get('id')=='large-photo': continue
            assert im.get('alt') and im.get('width') and im.get('height'), (p, im)
            assert not im.get('src','').startswith('http'), (p,im)
        for url in doc.links:
            u=urlsplit(url)
            if u.scheme or u.netloc or not u.path and not u.fragment: continue
            target=(ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)).resolve() if u.path else p
            if target.is_dir(): target=target/'index.html'
            assert target.exists(), (p,url,target)
            if u.fragment and target.suffix=='.html':
                if target not in pages: pages[target]=Page(target)
                assert unquote(u.fragment) in pages[target].ids, (p,url)
        assert not re.search(r'【图】|Codex|img_\d|\[S\d+\]|用户现场|网站可以|建议用|不要仅靠',p.read_text()), p
    home=(ROOT/'museum-notes/index.html').read_text()
    assert home.count('<!-- ten-kings-home -->')==1
    for rel in ['japanese-zen','xuzhou']:
        assert (ROOT/'museum-notes'/rel/'index.html').read_text().count('<!-- ten-kings-related -->')==1
    print(f'Ten Kings checks passed: {len(works)} exhibition records + {len(comparisons)} comparison, {len(photos)-1} source photos, 17 pages; mappings, dimensions, local links and private-archive exclusions.')


if __name__=='__main__': check()
