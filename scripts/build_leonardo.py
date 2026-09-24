"""Build the Leonardo photo notebook using the shared European painting presentation.
Edit museum-notes/leonardo/data/works.json, then run this script.
No network access or image processing is needed to rebuild the public pages.
"""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/leonardo'
data=json.loads((BASE/'data/works.json').read_text())
works=data['works']; by_id={w['id']:w for w in works}; museums=data['museums']
periods=data['periods']; groups=data['groups']; photos=data['photos']
assert len(by_id)==len(works)
assert {w['period'] for w in works} <= {p['id'] for p in periods}
for g in groups:
    assert len(g['works'])==len(set(g['works'])) and all(x in by_id for x in g['works'])
for w in works:
    assert (BASE/'images'/w['photo']).is_file()
    assert w['source_url'].startswith('https://')

LIGHTBOX='''<dialog id="art-lightbox" aria-labelledby="lightbox-caption"><div class="lightbox-tools"><button type="button" id="photo-prev" aria-label="上一张照片">←</button><button type="button" id="photo-next" aria-label="下一张照片">→</button><button type="button" id="zoom-toggle" aria-pressed="false">放大细看 ＋</button><a id="original-photo" href="#" target="_blank" rel="noopener">原图 ↗</a><button type="button" id="photo-close" aria-label="关闭大图">关闭 ×</button></div><div id="photo-stage" tabindex="0" aria-label="照片区域；放大后可滚动查看"><img id="large-photo" alt=""></div><p id="lightbox-caption"></p></dialog>'''
def shell(title,desc,body,depth=0,detail=False):
    topic='../'*depth or './'; notebook='../'*(depth+1)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="{e(desc)}"><link rel="stylesheet" href="{notebook}museum.css"><link rel="stylesheet" href="{notebook}caravaggio/caravaggio.css"><script src="{notebook}caravaggio/caravaggio.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{notebook}">Merton</a><nav aria-label="主导航"><a href="{notebook}european-painting/">欧洲绘画</a><a href="{topic}#collection">全部作品</a><a href="{topic}compare/">并排看画</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="{notebook}">← 博物馆札记</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
def img(n,prefix='',high=False):
    p=photos[str(n)]
    name=p['caption']
    return f'<img src="{prefix}images/{p["file"]}" alt="{e(name)} · Merton参观时拍摄" width="{p["width"]}" height="{p["height"]}" {"fetchpriority=high" if high else "loading=lazy"} decoding="async">'
def enlarge(w,prefix='',label='放大照片 ↗'):
    return f'<a class="enlarge" data-photo href="{prefix}images/{w["photo"]}" data-caption="{e(w["title"])} · {e(museums[w["museum"]])}">{label}</a>'
def card(w,prefix='',compact=False):
    badge='<span class="attribution">'+e({'collaboration':'合作作品','workshop':'工作室 · 归于梅尔齐'}.get(w['status'],''))+'</span>' if w['status']!='autograph' else ''
    return f'''<article class="art-card" data-period="{w['period']}" data-museum="{w['museum']}" data-tags="{' '.join(w['tags'])}" data-search="{e(' '.join([w['title'],w['original_title'],w['artist'],w['story'],museums[w['museum']],w['accession']]+w.get('search_aliases',[])))}"><a class="art-thumbnail" href="{prefix}{w['id']}/">{img(w['source_number'],prefix)}</a><div class="art-card-copy"><p class="card-kicker">{e(w['date'])}{badge}</p><h3><a href="{prefix}{w['id']}/">{e(w['title'])}</a></h3><p class="card-museum">{e(w.get('ownership') or museums[w['museum']])}</p>{'' if compact else '<p class="card-look">'+e(w['observation'])+'</p>'}<div class="card-actions"><a href="{prefix}{w['id']}/">读作品札记 →</a>{enlarge(w,prefix)}</div></div></article>'''
def breadcrumb(tail='',depth=0):
    topic='../'*depth or './'; note='../'*(depth+1)
    return f'<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="{note}">博物馆札记</a><span>/</span><a href="{note}european-painting/">欧洲绘画</a><span>/</span>'+ (f'<a href="{topic}">达·芬奇</a><span>/</span><span>{e(tail)}</span>' if tail else '<span>达·芬奇</span>')+'</nav>'
hero=by_id['ginevra-de-benci']
hero_html=f'''{breadcrumb()}<section class="car-hero wrap"><div class="car-hero-copy"><p class="eyebrow">EUROPEAN PAINTING / 002</p><h1>达·芬奇</h1><p class="artist-dates">LEONARDO DA VINCI &nbsp; 1452—1519</p><p class="car-lede">从一张脸，到另一张脸。<br>把看过的达·芬奇放在一起。</p><p class="car-intro">巴黎、佛罗伦萨、梵蒂冈、华盛顿。散在四座博物馆里的画，这次终于能翻到一起：有熟悉的肖像，也有没画完的祭坛画，还有一幅后来变了身份的“酒神”。</p><div class="hero-links"><a class="text-link" href="#collection">浏览全部作品 ↓</a><a class="text-link" href="compare/">并排看画 →</a></div><p class="car-stats"><b>11</b> 件作品 <span>9 件馆方署名达·芬奇 / 1 件合作 / 1 件工作室相关</span><br><b>12</b> 张参观照片 <span>来自 4 家博物馆</span></p></div><figure class="car-hero-image"><a href="ginevra-de-benci/">{img(541,high=True)}</a><figcaption>吉内薇拉·班琪肖像 · 约1474—1478年<br><span>美国国家美术馆 · 华盛顿</span></figcaption></figure></section>'''
ways=''.join(f'<a class="reading-route" href="compare/#{g["id"]}"><span class="eyebrow">0{i+1} / {len(g["works"])} 件作品</span><h3>{g["title"]} ↗</h3><p>{g["text"]}</p></a>' for i,g in enumerate(groups[:3]))
reading=f'<section class="wrap car-reading"><div class="car-heading"><div><p class="eyebrow">LOOK TOGETHER</p><h2>几组画，连着看</h2></div><a href="compare/">全部四组比较 →</a></div><div class="route-grid">{ways}</div></section>'
period_nav=''.join(f'<a href="#{p["id"]}">{p["title"]}<span>{sum(w["period"]==p["id"] for w in works)}</span></a>' for p in periods)
options=''.join(f'<option value="{k}">{e(v)}</option>' for k,v in museums.items())
filters=f'''<div class="art-controls" hidden><div class="art-fields"><label>找一幅画<input type="search" id="art-search" placeholder="作品、收藏地点、故事…" autocomplete="off"></label><label>收藏／展出机构<select id="art-museum"><option value="all">全部机构</option>{options}</select></label><label>题材<select id="art-subject"><option value="all">全部题材</option><option value="portrait">女性肖像</option><option value="unfinished">未完成的画</option><option value="sacred">宗教绘画</option><option value="john">施洗者约翰</option><option value="myth">神话与改绘</option></select></label></div><div class="art-results"><p id="art-count" role="status" aria-live="polite">11 件作品</p><div><button type="button" id="gallery-mode" aria-pressed="false">画廊模式</button><button type="button" id="art-reset">清除筛选</button></div></div></div>'''
sections=''.join(f'''<section class="era-section" id="{p['id']}" aria-labelledby="heading-{p['id']}"><div class="era-heading"><p class="eyebrow">{p['range']}</p><h2 id="heading-{p['id']}">{p['title']}</h2><p>{p['intro']}</p></div><div class="art-grid">{''.join(card(w) for w in sorted(works,key=lambda x:x['year']) if w['period']==p['id'])}</div></section>''' for p in periods)
collection=f'''<section id="collection" class="wrap car-collection"><div class="car-heading"><div><p class="eyebrow">THE PAINTINGS</p><h2>沿着创作时期看</h2></div><p>年代重叠处，逐件保留说明。</p></div><nav class="era-nav" aria-label="创作时期">{period_nav}</nav>{filters}<p id="art-empty" hidden>没有找到符合条件的作品，可以换个词或清除筛选。</p>{sections}</section>'''
about='''<aside class="editorial-note wrap"><h2>关于这一辑</h2><p>这里只整理我看过、拍过的作品。达·芬奇的画本来就少，放到一起看，更容易注意到那些反复出现的手势、目光和远山。</p><p>依照馆方署名，这一辑有9件达·芬奇作品、1件与委罗基奥的合作作品，以及1件归于梅尔齐的工作室作品。后两件分别注明；《蒙娜丽莎》的重复照片只算一件作品。照片保留现场的画框、角度和反光。</p><p>每件作品都附有馆方资料。展签与线上目录不一致的地方，保留两种记录；传说和推测另作说明。看画提示是重看照片时可以留意的细节。</p><p class="source">2026年9月整理 · 11件作品 / 12张照片 / 4家博物馆。</p></aside>'''
(BASE/'index.html').write_text(shell('达·芬奇 · 欧洲绘画', 'Merton在四家博物馆拍摄的11件达·芬奇及相关作品，含合作与工作室作品。附收藏故事、原拍照片与四组比较。',hero_html+reading+collection+about))
# Dedicated work pages; stable URLs, sources next to the claims, reciprocal comparison links.
for w in works:
    prefix='../'; period=next(p for p in periods if p['id']==w['period'])
    fields=[('作者',w['artist']),('年代',w['date']),('材料',w['material']),('收藏／所在',w.get('ownership') or museums[w['museum']]),('编号／位置',w['accession'])]
    if w.get('visit'): fields.append(('照片记录',w['visit']))
    facts='<dl class="work-facts">'+''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in fields)+'</dl>'
    source=f'<a href="{e(w["source_url"])}" target="_blank" rel="noopener noreferrer">馆方／收藏机构资料 ↗</a>'
    if w.get('extra_source'): source+=f'<br><a href="{e(w["extra_source"][1])}" target="_blank" rel="noopener noreferrer">{e(w["extra_source"][0])} ↗</a>'
    for label, url in w.get('naming_sources',[]):
        source+=f'<br><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗</a>'
    note=f'<p class="record-note">{e(w["source_note"])}</p>' if w['source_note'] else ''
    context=''
    if w.get('context'):
        n=w['context']; caption=photos[str(n)]['caption']
        context=f'<section class="context-section wrap"><div><p class="eyebrow">IN THE GALLERY</p><h2>站在展厅里看</h2><p>再留一张稍远的照片，记下画作、玻璃与观看距离。</p></div><figure><a data-photo href="../images/{photos[str(n)]["file"]}" data-caption="{caption}">{img(n,prefix)}</a><figcaption>{caption} · 点击放大</figcaption></figure></section>'
    memberships=[g for g in groups if w['id'] in g['works']]
    related_ids=list(dict.fromkeys([x for g in memberships for x in g['works'] if x!=w['id']]+[n['work'] for n in w.get('related_notes',[])]))
    relation_links=''.join(f'<a href="../compare/#{g["id"]}">{g["title"]} →</a>' for g in memberships)
    extra_relations=''.join(f'<p class="related-reason"><a href="../{n["work"]}/">{e(by_id[n["work"]]["title"])} →</a>　{e(n["reason"])}</p>' for n in w.get('related_notes',[]))
    related=f'<section class="related-section wrap"><p class="eyebrow">CONTINUE LOOKING</p><h2>也放在一起看</h2><div class="relation-links">{relation_links}</div>{extra_relations}<div class="art-grid related-grid">'+''.join(card(by_id[x],prefix,True) for x in related_ids)+'</div></section>' if related_ids else ''
    ordered=sorted(works,key=lambda x:([p['id'] for p in periods].index(x['period']),x['year']))
    i=ordered.index(w); prev=ordered[i-1] if i>0 else None; nxt=ordered[i+1] if i+1<len(ordered) else None
    sequence='<nav class="work-sequence wrap" aria-label="前后作品">'+(f'<a href="../{prev["id"]}/">← {prev["title"]}</a>' if prev else '<span></span>')+f'<a href="../#{w["period"]}">返回{period["title"]}</a>'+(f'<a href="../{nxt["id"]}/">{nxt["title"]} →</a>' if nxt else '<span></span>')+'</nav>'
    body=f'''{breadcrumb(w['title'],1)}<header class="work-heading wrap"><p class="eyebrow">LEONARDO DA VINCI / {e(period['title'])}</p><h1>{e(w['title'])}</h1><p class="work-original">{e(w['original_title'])}</p>{'<p class="attribution work-attribution">'+e(w['artist'])+'</p>' if w['status']!='autograph' else ''}</header><div class="work-layout wrap"><figure class="work-photo"><a data-photo href="../images/{w['photo']}" data-caption="{e(w['title'])} · {e(museums[w['museum']])}">{img(w['source_number'],prefix,True)}</a><figcaption>参观照片 / Merton · 点击放大</figcaption></figure><div class="work-record">{facts}<section><h2>看画</h2><p>{e(w['observation'])}</p></section><section><h2>这幅画的故事</h2><p>{e(w['story'])}</p><div class="work-sources">{source}</div></section>{note}<p class="source">基本信息另据配套现场展签；未配展签的作品见上述核对说明。资料核对：2026年9月。</p></div></div>{context}{related}{sequence}'''
    target=BASE/w['id']; target.mkdir(exist_ok=True)
    (target/'index.html').write_text(shell(w['title']+' · 达·芬奇',w['observation'],body,1,True))
# Comparison groups share the same originals, and never silently crop them.
nav=''.join(f'<a href="#{g["id"]}">{g["title"]}</a>' for g in groups)
comparisons=''
for g in groups:
    cells=''
    for x in g['works']:
        w=by_id[x]
        cells+=f'<figure class="comparison-work"><a data-photo href="../images/{w["photo"]}" data-caption="{e(w["title"])} · {e(museums[w["museum"]])}">{img(w["source_number"],"../")}</a><figcaption><a href="../{w["id"]}/">{e(w["title"])} →</a><span>{e(w["date"])}</span><span>{e(w["artist"])}</span><span>{e(museums[w["museum"]])}</span></figcaption></figure>'
    context=''
    comparisons+=f'<section class="compare-group" id="{g["id"]}" aria-labelledby="compare-{g["id"]}"><h2 id="compare-{g["id"]}">{g["title"]}</h2><p>{g["text"]}</p><div class="comparison-grid" style="--columns:{min(len(g["works"]),4)}">{cells}</div>{context}</section>'
body=breadcrumb('并排看画',1)+f'<header class="compare-header wrap"><p class="eyebrow">LEONARDO DA VINCI / SIDE BY SIDE</p><h1>并排看画</h1><p>同一个题材，不同的手势、目光与命运。<br>点击照片放大，点击画名进入作品札记。</p><p class="source">照片按画面排布，不代表作品实物的比例大小。</p></header><div class="wrap"><nav class="compare-nav" aria-label="选择比较组">{nav}</nav>{comparisons}</div>'
(BASE/'compare').mkdir(exist_ok=True)
(BASE/'compare/index.html').write_text(shell('并排看画 · 达·芬奇','三张女性肖像、两幅未完成的画，以及人物手势与施洗者约翰题材的比较。',body,1))

from build_european import build
build()
print(f'Built Leonardo: {len(works)} work pages and {len(groups)} comparison groups.')
