"""Structural/data regression checks for the water-moon split and shared cards."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/water-moon-guanyin'
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__();self.ids=[];self.works=[];self.images=[];self.links=[];self.map_links=[];self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='article' and 'object-card' in a.get('class','').split():self.works.append(a['id'])
        if tag=='img' and a.get('id')!='lightbox-image':self.images.append(a);assert a.get('alt'),a
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if 'data-museum-link' in a:self.map_links.append(a['data-museum-link'])
g=json.loads((BASE/'data/guide.json').read_text());archive=json.loads((ROOT/'museum-notes/buddhist-sculpture/data/objects.json').read_text());by_id={o['id']:o for o in archive['objects']}
parsed={p:Page(p) for p in [BASE/'index.html',BASE/'extended/index.html']}
main,ext=parsed.values()
assert main.works==[f'object-{n}' for n in g['core_ids']]
assert ext.works==[f'object-{n}' for n in g['extended_ids']]
assert set(main.works).isdisjoint(ext.works)
assert {m['museum_id'] for m in g['map']['museums']}=={by_id[w]['museum'] for w in main.works}
assert set(main.map_links)=={m['museum_id'] for m in g['map']['museums']}
assert '13—14世纪' in by_id['object-255']['date']
for d in g['dealers']:
    assert d['records']
    for r in d['records']:
        assert f'object-{r["work"]}' in main.works+ext.works
        assert all(r.get(k) for k in ['source','role','date','text'])
for path,page in parsed.items():
    assert len(page.ids)==len(set(page.ids)),f'Duplicate IDs: {path}'
    for a in page.images:
        if not urlsplit(a['src']).scheme:assert (path.parent/unquote(a['src'])).resolve().is_file(),a['src']
    for href in page.links:
        url=urlsplit(href)
        if url.scheme or url.netloc:continue
        target=(path.parent/unquote(url.path)).resolve() if url.path else path
        if target.is_dir():target/= 'index.html'
        assert target.is_file(),(path,href)
        if url.fragment:
            linked=parsed.get(target) or Page(target)
            assert unquote(url.fragment) in linked.ids,(path,href)
for n in g['extended_ids']:
    assert f'object-{n}' in main.ids, 'Legacy fragment fallback missing'
metadata=json.loads((ROOT/'museum-notes/buddhist-sculpture/data/topics.json').read_text())
topic=next(t for t in metadata['topics'] if t['id']=='water-moon-guanyin')
assert topic['ids']==g['core_ids']+g['extended_ids']
assert topic['core_ids']==g['core_ids']
assert all(by_id[w]['photo'] in (BASE/('index.html' if w in main.works else 'extended/index.html')).read_text() for w in main.works+ext.works)
print('PASS: 8 main / 5 extension; canonical photos, museum map, provenance edges, local images, links, anchors and metadata.')

assert 'object-199' not in main.works+ext.works
assert by_id['object-194480']['museum']=='bma'
assert by_id['object-241']['museum']!='bma'
for page in parsed.values():assert 'object-199' in page.ids
photos=json.loads((BASE/'data/bma-1944-80-photos.json').read_text())['photos']
assert len(photos)==6 and len({p['source_photo'] for p in photos})==6
assert all(p['original_url'].startswith('https://images.mertonmuseum.com/') for p in photos)
assert sum(p['role']=='main' for p in photos)==1
assert sum(p['role']=='archived_alternate' for p in photos)==1
print('PASS: BMA / Walters distinct, six photos accounted for, Guimet old anchors preserved.')
