"""Build the water-moon main notebook and extension from shared sculpture records.
Run alone to avoid regenerating other unfinished museum topics.
"""
from pathlib import Path
from html import escape as e
from functools import partial
import json
from sculpture_cards import render_card, lightbox
from museum_assets import asset_url, responsive_attributes

ROOT = Path(__file__).resolve().parents[1]
TOPIC = ROOT / 'museum-notes/water-moon-guanyin'

def load_guide(root=ROOT):
    return json.loads((root/'museum-notes/water-moon-guanyin/data/guide.json').read_text())


def topic_info(root=ROOT):
    guide=load_guide(root)
    return dict(id='water-moon-guanyin',title='水月观音',subtitle='一膝支起，一臂舒展。',
                intro='以宋辽金前后的观音木雕为主线，从观看地图与近代收藏记录回到每尊像；另设延展小辑，比较不同姿态与材料。',
                ids=guide['core_ids']+guide['extended_ids'],core_ids=guide['core_ids'],
                extended_ids=guide['extended_ids'],extended_url='extended/',hero=215,
                note=f'主线保留截至波特兰的八尊木雕；波特兰13—14世纪像作为相邻时期参照。另有{len(guide["extended_ids"])}件收在延展看，作品ID与原记录不变。')


def land_paths(geo, bounds, width, height):
    west, south, east, north = bounds
    def point(lon, lat):
        return (lon-west)/(east-west)*width, (north-lat)/(north-south)*height
    paths=[]
    for feature in geo['features']:
        geometry=feature['geometry']
        polygons=geometry['coordinates'] if geometry['type']=='MultiPolygon' else [geometry['coordinates']]
        for polygon in polygons:
            ring=polygon[0]
            if max(x[0] for x in ring)<west or min(x[0] for x in ring)>east or max(x[1] for x in ring)<south or min(x[1] for x in ring)>north:
                continue
            points=[point(*p[:2]) for p in ring]
            paths.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in points)+'Z')
    return ''.join(f'<path d="{p}"/>' for p in paths), point


def build(root=ROOT, objects=None, museums=None, render=None, viewer=lightbox, sync_entrance=True):
    if objects is None:
        archive=json.loads((root/'museum-notes/buddhist-sculpture/data/objects.json').read_text())
        objects,museums=archive['objects'],archive['museums']
    render=render or partial(render_card,museums=museums)
    guide=load_guide(root)
    core,extra=guide['core_ids'],guide['extended_ids']
    by_id={(int(o['id'][7:]) if o['id'][7:].isdigit() else o['id'][7:]):o for o in objects}
    assert not set(core)&set(extra)
    assert len(core+extra)==len(set(core+extra))
    assert set(m['museum_id'] for m in guide['map']['museums'])=={by_id[n]['museum'] for n in core}
    def work_url(n,extended=False):
        return (('../' if extended else '') if n in core else ('' if extended else 'extended/'))+f'#object-{n}'
    def photo(n,prefix='../'):
        return asset_url(prefix+'buddhist-sculpture/images/',by_id[n]['photo'])
    def mini(n,text='',extended=False,legacy=False):
        o=by_id[n];m=museums[o['museum']]
        identity=f' id="object-{n}" data-extension-target="extended/#object-{n}"' if legacy else ''
        return f'''<article class="wm-mini"{identity}><a href="{work_url(n,extended)}"><img src="{photo(n,'../../' if extended else '../')}" {responsive_attributes(o)} alt="{e(o['title'])}，{e(m[0])}" width="{o['width']}" height="{o['height']}" loading="lazy"></a><div><p class="wm-kicker">{e(m[1])} · {'延展看' if n in extra else '木雕主线'}</p><h3><a href="{work_url(n,extended)}">{e(o['title'])}</a></h3><p class="source">{e(o['date'])} · {e(o['accession'])}<br>{e(m[0])}</p>{text}</div></article>'''
    def card(n,index,extended=False):
        markup=render(by_id[n],index,'../../buddhist-sculpture/images/' if extended else '../buddhist-sculpture/images/')
        links=[]
        for dealer in guide['dealers']:
            if any(rec['work']==n for rec in dealer['records']):
                links.append(f'<a href="{"../" if extended else ""}#dealer-{dealer["id"]}">{e(dealer["name"])}的相关作品</a>')
        if n in [241,224]:
            links.append(f'<a href="{"../../" if extended else "../"}dry-lacquer/#object-{n}">也见：干漆与漆塑</a>')
        if links:
            markup=markup.replace('<details>','<p class="source">'+' · '.join(links)+'</p><details>',1)
        return markup
    def shell(title,body,extended=False):
        p='../../' if extended else '../';local='../' if extended else ''
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · 博物馆札记 | Merton</title><meta name="description" content="以宋辽金木雕为主，重看亲见的水月、南海与自在坐观音；从博物馆地图与近代收藏记录，回到每一尊像。"><link rel="stylesheet" href="{p}museum.css"><link rel="stylesheet" href="{p}sculpture-topics.css"><link rel="stylesheet" href="{local}water-moon.css"><script src="{p}museum.js" defer></script><script src="{local}water-moon.js" defer></script></head><body id="top" class="wm-page"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{p}">Merton</a><nav aria-label="主导航"><a href="{p}chinese-buddhist-art/">中国佛教艺术</a><a href="{local or './'}">水月观音</a><a href="{local}extended/">延展看</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="{p}chinese-buddhist-art/">← 中国佛教艺术</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{viewer}</body></html>'''
    hero=by_id[core[0]]
    poem='''<section class="topic-poem wrap" aria-labelledby="poem-title"><p class="eyebrow">宋代 · 释心月</p><h2 id="poem-title">水月观音赞</h2><blockquote>觉天无云，性海无风。<br>玉轮蘸影，金浪翻空。<br>非惟观世音，我亦游其中。</blockquote><p class="source"><a href="https://www.sou-yun.cn/Query.aspx?id=227226&amp;type=poem" target="_blank" rel="noopener noreferrer">原文核对：搜韵 ↗</a></p></section>'''
    intro=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>水月观音</span></nav><section class="hero wrap"><div class="hero-copy"><p class="eyebrow">WOOD · SONG / LIAO / JIN</p><h1>水月观音</h1><p class="subtitle">一膝支起，一臂舒展。</p><p class="intro">这一辑，先把目光留给宋辽金前后的观音木雕。抬起的膝、舒展的手臂、残彩下的木色，在不同展厅里各有神情。</p><p class="intro">从堪萨斯城看到波特兰，八尊木雕构成主线。另把几件姿态、年代或材料不同的作品收进“延展看”，继续比较水月图像的不同呈现。</p><nav class="wm-nav" aria-label="本辑导览"><a href="#collection">八尊木雕</a><a href="#museum-map">观看地图</a><a href="#dealers">古董商线索</a><a href="extended/">延展看 →</a></nav></div><figure class="hero-image"><a class="photo-link" href="{photo(core[0])}" data-caption="{e(hero['title'])} · {e(museums[hero['museum']][0])}"><img src="{photo(core[0])}" alt="南海观音，右臂舒展，搭在抬起的膝上，坐于岩座。" width="{hero['width']}" height="{hero['height']}" fetchpriority="high"></a><figcaption>{e(hero['title'])} · {e(hero['date'])}<br><span>{e(museums[hero['museum']][0])} · {e(hero['accession'])}</span></figcaption></figure></section>'''
    # Natural Earth land outlines are reused, clipped, and projected at build time.
    geo=json.loads((root/'museum-notes/homer/data/ne_110m_land.geojson').read_text())
    regions=[('north-america','北美大陆',(-130,25,-65,56),780,420),('hawaii','夏威夷',(-161,18,-154,24),300,230),('europe','欧洲',(-7,46,18,59),300,230)]
    panels=[]
    for region,name,bounds,w,h in regions:
        land,point=land_paths(geo,bounds,w,h)
        markers=[]
        for m in guide['map']['museums']:
            if m['region']!=region:continue
            key=m['museum_id'];x,y=point(m['longitude'],m['latitude']);tx=x+m['label_dx'];ty=y+m['label_dy'];city=museums[key][1]
            anchor='end' if m['label_dx']<0 else ('start' if m['label_dx']>0 else 'middle')
            markers.append(f'''<a href="#museum-{key}" data-museum-link="{key}" aria-label="{e(museums[key][0])}，{e(city)}"><title>{e(museums[key][0])}</title><line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty-5:.1f}"/><circle class="wm-hit" cx="{x:.1f}" cy="{y:.1f}" r="15"/><circle class="wm-dot" cx="{x:.1f}" cy="{y:.1f}" r="5"/><text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{e(city)}</text></a>''')
        panels.append(f'''<figure class="wm-map-panel wm-{region}"><figcaption>{name}</figcaption><div class="wm-map-scroll" tabindex="0" role="region" aria-label="{name}地图，可横向浏览"><svg viewBox="0 0 {w} {h}" aria-label="{name}观看城市地图" role="group"><defs><clipPath id="clip-{region}"><rect width="{w}" height="{h}"/></clipPath></defs><g class="wm-land" clip-path="url(#clip-{region})">{land}</g><g class="wm-markers">{''.join(markers)}</g></svg></div></figure>''')
    museum_nav=[];museum_panels=[]
    for m in guide['map']['museums']:
        key=m['museum_id'];works=[n for n in core if by_id[n]['museum']==key];name,city,_=museums[key]
        museum_nav.append(f'<a href="#museum-{key}" data-museum-link="{key}">{e(city)}<span>{len(works)} 件</span></a>')
        museum_panels.append(f'<section class="wm-museum-result" id="museum-{key}" data-museum-panel="{key}" aria-label="{e(name)}">'+''.join(mini(n,'<p><a href="'+work_url(n)+'">展开这尊像的照片与札记 ↓</a></p>') for n in works)+'</section>')
    map_section=f'''<section class="wrap wm-section" id="museum-map"><p class="eyebrow">MUSEUMS I VISITED</p><h2>在这些展厅里遇见</h2><p class="wm-lead">八尊主线木雕，分别在{len(guide['map']['museums'])}家博物馆。点一个城市，从地图回到那尊像。</p><div class="wm-maps">{''.join(panels)}</div><nav class="wm-museum-nav" aria-label="选择观看城市">{''.join(museum_nav)}</nav><p class="wm-map-help">地图标出观看博物馆所在的城市，不是造像的制作地或古代流转路线。北美地图在窄屏上可横向浏览，也可直接选择下方城市。</p><div class="wm-museum-results">{''.join(museum_panels)}</div><p class="source">底图：<a href="{guide['map']['basemap_source']}">Natural Earth · 公共领域</a>，沿用本站地理数据；坐标为城市级示意，各分图比例不同。</p></section>'''
    collection=f'''<section class="collection wrap" id="collection"><div class="collection-heading"><div><p class="eyebrow">EIGHT WOOD SCULPTURES</p><h2>一件一件看</h2></div><p>{len(core)} 件主线作品</p></div><p class="wm-lead">以宋辽金木雕为重心，保留馆方各自的“水月”“南海”与“自在坐”题名。波特兰像沿用展签的13—14世纪，作为相邻时期的参照。</p><div class="object-grid">{''.join(card(n,i) for i,n in enumerate(core))}</div></section>'''
    dealers=[]
    for dealer in guide['dealers']:
        records=[]
        for rec in dealer['records']:
            content=f'<p class="wm-record-date">{e(rec["date"])}</p><p>{e(rec["text"])}</p><p class="source">关系：{e(rec["role"])}</p><p class="source"><a href="{e(rec["source"])}">{e(rec["source_title"])} ↗</a>'
            if rec.get('data_source'):content+=f' · <a href="{e(rec["data_source"])}">馆方开放数据</a>'
            content+='</p>'
            records.append(mini(rec['work'],content))
        dealers.append(f'''<details class="wm-dealer" id="dealer-{dealer['id']}"><summary><span class="wm-dealer-label">{e(dealer['name'])}<small>{e(dealer['english'])} · {len(dealer['records'])} 件相关作品</small></span><span class="wm-disclosure" aria-hidden="true">＋</span></summary><div class="wm-dealer-body"><p>{e(dealer['intro'])}</p><div class="wm-records">{''.join(records)}</div></div></details>''')
    dealer_section=f'''<section class="wrap wm-section" id="dealers"><p class="eyebrow">ANOTHER WAY TO CONNECT</p><h2>沿着古董商的名字重看</h2><p class="wm-lead">有些相隔很远的作品，在近代收藏记录里又碰到一起。这里按经手人的名字并看，分别说明交易、收藏与捐赠；相关作品来自主线，也来自延展。</p>{''.join(dealers)}<p class="source">这些是各馆已公布的流转片段，并不能据此确定同一寺院、作坊或完整离散路线。其余作品暂不归入商人组；没有记录，也不等于没有经手关系。</p></section>'''
    extensions=f'''<section class="wrap wm-section" id="extensions"><p class="eyebrow">FURTHER LOOKING</p><h2><a href="extended/">延展看：水月图像的不同材料 →</a></h2><p class="wm-lead">从宾大的宽厚木雕，转向青白瓷、干漆、金属与覆金漆塑。{len(extra)}件作品收在独立小辑，保留各自的全图、札记与资料。</p><div class="wm-extension-grid">{''.join(mini(n,legacy=True) for n in extra)}</div></section>'''
    def relocated(extended=False):
        prefix='../../' if extended else '../'
        return '<aside class="wrap editorial-note">'+''.join(f'<p id="object-{x["id"]}" data-extension-target="{prefix}{x["path"]}#object-{x["id"]}"><a href="{prefix}{x["path"]}#object-{x["id"]}">{e(x["title"])} →</a>：{e(x["reason"])}</p>' for x in guide.get('relocated',[]))+'</aside>'
    ending='''<section class="wrap topic-next"><h2>接着看</h2><a href="../song-liao-jin-wood/">五代至元木雕 →</a><a href="../dry-lacquer/">干漆与漆塑 →</a><a href="../yixian-luohan/">易县三彩罗汉 →</a></section>'''
    path=root/'museum-notes/water-moon-guanyin';(path/'extended').mkdir(parents=True,exist_ok=True)
    (path/'index.html').write_text(shell('水月观音',intro+poem+map_section+collection+dealer_section+extensions+relocated()+ending))
    ext_intro=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">水月观音</a><span>/</span><span>延展看</span></nav><header class="wrap wm-extension-header"><p class="eyebrow">FURTHER LOOKING</p><h1>延展看</h1><p class="subtitle">水月图像的延展</p><p>一膝抬起的姿态，在不同的材料与年代里，形成了不同的体量与衣纹。这里从宾大木雕继续看向青白瓷、干漆、金属与漆塑；各件年代仍沿用馆方记录，材料与样式并不排成单一的演变顺序。</p><nav class="wm-nav" aria-label="延展导览"><a href="../#collection">← 八尊木雕主线</a><a href="../#museum-map">观看地图</a><a href="../#dealers">古董商线索</a><a href="#collection">细看{len(extra)}件作品 ↓</a></nav></header>'''
    ext_cards=''.join('<section class="wm-extension-work"><p class="wm-lead">'+e(guide['extension_notes'][str(n)])+'</p>'+card(n,i,True)+'</section>' for i,n in enumerate(extra))
    ext_body=ext_intro+f'<section class="wrap collection" id="collection"><div class="collection-heading"><h2>姿态之外，再看材料</h2><p>{len(extra)} 件作品</p></div><div class="wm-extension-works">{ext_cards}</div></section><section class="wrap topic-next"><a href="../">← 回到水月观音主辑</a><a href="../../dry-lacquer/">干漆与漆塑造像 →</a></section>'
    (path/'extended/index.html').write_text(shell('延展看 · 水月观音',ext_body+relocated(True),True))
    import re
    directory=root/'museum-notes/chinese-buddhist-art/index.html'
    current=directory.read_text()
    info=topic_info(root)
    def entrance(match):
        block=match.group(0)
        block=re.sub(r'<p class="eyebrow">.*?</p>',f'<p class="eyebrow">{len(core)} 件主线 · {len(extra)} 件延展</p>',block,count=1)
        block=re.sub(r'(<h2>水月观音</h2>)<p>.*?</p>',lambda m:m[1]+'<p>'+info['intro']+'</p>',block,count=1)
        return block
    current,n=re.subn(r'<a class="issue-link" href="../water-moon-guanyin/">.*?</a>',entrance,current,count=1,flags=re.S)
    if sync_entrance:
        assert n==1, 'Expected one Chinese Buddhist Art entrance'
        directory.write_text(current)
    metadata=root/'museum-notes/buddhist-sculpture/data/topics.json'
    md=json.loads(metadata.read_text())
    md['topics']=[info if t['id']=='water-moon-guanyin' else t for t in md['topics']]
    metadata.write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n')
    print(f'Water moon: {len(core)} main works, {len(extra)} extended, {len(guide["map"]["museums"])} museums, {sum(len(d["records"]) for d in guide["dealers"])} provenance links.')

if __name__=='__main__':
    build()
