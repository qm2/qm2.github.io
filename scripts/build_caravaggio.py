"""Build the European painting landing page and the Caravaggio photo notebook.
Edit museum-notes/caravaggio/data/works.json, then run this script.
No network access or image processing is needed to rebuild the public pages.
"""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/caravaggio'
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
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="{e(desc)}"><link rel="stylesheet" href="{notebook}museum.css"><link rel="stylesheet" href="{topic}caravaggio.css"><script src="{topic}caravaggio.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{notebook}">Merton</a><nav aria-label="主导航"><a href="{notebook}european-painting/">欧洲绘画</a><a href="{topic}#collection">全部作品</a><a href="{topic}compare/">并排看画</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="{notebook}">← 博物馆札记</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
def img(n,prefix='',high=False):
    p=photos[str(n)]
    name=next((w['title'] for w in works if w['source_number']==n),'卡瓦莱蒂礼拜堂全景' if n==473 else '孔塔雷利礼拜堂全景')
    return f'<img src="{prefix}images/{p["file"]}" alt="{e(name)} · Merton参观时拍摄" width="{p["width"]}" height="{p["height"]}" {"fetchpriority=high" if high else "loading=lazy"} decoding="async">'
def enlarge(w,prefix='',label='放大照片 ↗'):
    return f'<a class="enlarge" data-photo href="{prefix}images/{w["photo"]}" data-caption="{e(w["title"])} · {e(museums[w["museum"]])}">{label}</a>'
def card(w,prefix='',compact=False):
    badge='<span class="attribution">归属有争议</span>' if w['period']=='question' else ''
    return f'''<article class="art-card" data-period="{w['period']}" data-museum="{w['museum']}" data-tags="{' '.join(w['tags'])}" data-search="{e(' '.join([w['title'],w['original_title'],w['artist'],w['story'],museums[w['museum']],w['accession']]))}"><a class="art-thumbnail" href="{prefix}{w['id']}/">{img(w['source_number'],prefix)}</a><div class="art-card-copy"><p class="card-kicker">{e(w['date'])}{badge}</p><h3><a href="{prefix}{w['id']}/">{e(w['title'])}</a></h3><p class="card-museum">{e(w.get('ownership') or museums[w['museum']])}</p>{'' if compact else '<p class="card-look">'+e(w['observation'])+'</p>'}<div class="card-actions"><a href="{prefix}{w['id']}/">读作品札记 →</a>{enlarge(w,prefix)}</div></div></article>'''
def breadcrumb(tail='',depth=0):
    topic='../'*depth or './'; note='../'*(depth+1)
    return f'<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="{note}">博物馆札记</a><span>/</span><a href="{note}european-painting/">欧洲绘画</a><span>/</span>'+ (f'<a href="{topic}">卡拉瓦乔</a><span>/</span><span>{e(tail)}</span>' if tail else '<span>卡拉瓦乔</span>')+'</nav>'
hero=by_id['cardsharps']
hero_html=f'''{breadcrumb()}<section class="car-hero wrap"><div class="car-hero-copy"><p class="eyebrow">EUROPEAN PAINTING / 001</p><h1>卡拉瓦乔</h1><p class="artist-dates">CARAVAGGIO &nbsp; 1571—1610</p><p class="car-lede">把不同旅途中见到的画，<br>放到一起再看一遍。</p><p class="car-intro">从牌桌旁的年轻人，到教堂里的圣马太，再到最后几年的沉默。原来在不同城市看过的那些画，也能这样连起来。</p><div class="hero-links"><a class="text-link" href="#collection">浏览全部作品 ↓</a><a class="text-link" href="compare/">并排看画 →</a></div><p class="car-stats"><b>27</b> 件作品 <span>含 1 件归属讨论</span><br><b>29</b> 张参观照片 <span>包括 2 张教堂全景</span></p></div><figure class="car-hero-image"><a href="cardsharps/">{img(470,high=True)}</a><figcaption>纸牌作弊者 · 约1596—1597年<br><span>金贝尔艺术博物馆 · 沃思堡</span></figcaption></figure></section>'''
ways=''.join(f'<a class="reading-route" href="compare/#{g["id"]}"><span class="eyebrow">0{i+1} / {len(g["works"])} 件作品</span><h3>{g["title"]} ↗</h3><p>{g["text"]}</p></a>' for i,g in enumerate(groups[:3]))
reading=f'<section class="wrap car-reading"><div class="car-heading"><div><p class="eyebrow">LOOK TOGETHER</p><h2>几组画，连着看</h2></div><a href="compare/">全部七组比较 →</a></div><div class="route-grid">{ways}</div></section>'
period_nav=''.join(f'<a href="#{p["id"]}">{p["title"]}<span>{sum(w["period"]==p["id"] for w in works)}</span></a>' for p in periods)
options=''.join(f'<option value="{k}">{e(v)}</option>' for k,v in museums.items())
filters=f'''<div class="art-controls" hidden><div class="art-fields"><label>找一幅画<input type="search" id="art-search" placeholder="作品、收藏地点、故事…" autocomplete="off"></label><label>收藏／展出机构<select id="art-museum"><option value="all">全部机构</option>{options}</select></label><label>题材<select id="art-subject"><option value="all">全部题材</option><option value="deception">牌局与占卜</option><option value="myth">神话人物</option><option value="john">施洗者约翰</option><option value="altar">教堂祭坛与壁面</option><option value="meditation">沉思与悔罪</option></select></label></div><div class="art-results"><p id="art-count" role="status" aria-live="polite">27 件作品</p><div><button type="button" id="gallery-mode" aria-pressed="false">画廊模式</button><button type="button" id="art-reset">清除筛选</button></div></div></div>'''
sections=''.join(f'''<section class="era-section" id="{p['id']}" aria-labelledby="heading-{p['id']}"><div class="era-heading"><p class="eyebrow">{p['range']}</p><h2 id="heading-{p['id']}">{p['title']}</h2><p>{p['intro']}</p></div><div class="art-grid">{''.join(card(w) for w in sorted(works,key=lambda x:x['year']) if w['period']==p['id'])}</div></section>''' for p in periods)
collection=f'''<section id="collection" class="wrap car-collection"><div class="car-heading"><div><p class="eyebrow">THE PAINTINGS</p><h2>沿着创作时期看</h2></div><p>年代重叠处，逐件保留说明。</p></div><nav class="era-nav" aria-label="创作时期">{period_nav}</nav>{filters}<p id="art-empty" hidden>没有找到符合条件的作品，可以换个词或清除筛选。</p>{sections}</section>'''
about='''<aside class="editorial-note wrap"><h2>关于这一辑</h2><p>这里收的是我在博物馆和教堂见过、拍过的作品。画作照片保留现场的画框、角度和反光；教堂作品还附上空间全景。点击照片旁的“放大”可以细看。</p><p>名称、年代和收藏信息依据现场展签与馆方资料整理，每件作品都附有来源链接。看画提示说的是照片中能看到的细节；创作和收藏故事另列。展签与线上目录不一致时，两种说法都留下来。有争议的署名与推测性的故事也会注明。</p><p class="source">2026年9月整理 · 本辑27件，含《纳西索斯》1件归属讨论。照片记录参观时的展出状态。</p></aside>'''
(BASE/'index.html').write_text(shell('卡拉瓦乔 · 欧洲绘画', 'Merton的27件卡拉瓦乔及相关作品参观记录：从早年罗马到晚年，附原拍照片、收藏故事与七组作品比较。',hero_html+reading+collection+about))
# Dedicated work pages; stable URLs, sources next to the claims, reciprocal comparison links.
for w in works:
    prefix='../'; period=next(p for p in periods if p['id']==w['period'])
    fields=[('作者',w['artist']),('年代',w['date']),('材料',w['material']),('收藏／所在',w.get('ownership') or museums[w['museum']]),('编号／位置',w['accession'])]
    if w.get('visit'): fields.append(('照片记录',w['visit']))
    facts='<dl class="work-facts">'+''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in fields)+'</dl>'
    source=f'<a href="{e(w["source_url"])}" target="_blank" rel="noopener noreferrer">馆方／收藏机构资料 ↗</a>'
    if w.get('extra_source'): source+=f'<br><a href="{e(w["extra_source"][1])}" target="_blank" rel="noopener noreferrer">{e(w["extra_source"][0])} ↗</a>'
    note=f'<p class="record-note">{e(w["source_note"])}</p>' if w['source_note'] else ''
    context=''
    if w.get('context'):
        n=w['context']; caption='卡瓦莱蒂礼拜堂：作品与周围壁画' if n==473 else '孔塔雷利礼拜堂：左壁《蒙召》、中央《圣马太与天使》、右壁《殉道》'
        context=f'<section class="context-section wrap"><div><p class="eyebrow">IN THE CHAPEL</p><h2>回到原来的空间</h2><p>{caption}。</p></div><figure><a data-photo href="../images/caravaggio-{n}.jpg" data-caption="{caption}">{img(n,prefix)}</a><figcaption>{caption} · 点击放大</figcaption></figure></section>'
    memberships=[g for g in groups if w['id'] in g['works']]
    related_ids=list(dict.fromkeys([x for g in memberships for x in g['works'] if x!=w['id']]+[n['work'] for n in w.get('related_notes',[])]))
    relation_links=''.join(f'<a href="../compare/#{g["id"]}">{g["title"]} →</a>' for g in memberships)
    extra_relations=''.join(f'<p class="related-reason"><a href="../{n["work"]}/">{e(by_id[n["work"]]["title"])} →</a>　{e(n["reason"])}</p>' for n in w.get('related_notes',[]))
    related=f'<section class="related-section wrap"><p class="eyebrow">CONTINUE LOOKING</p><h2>也放在一起看</h2><div class="relation-links">{relation_links}</div>{extra_relations}<div class="art-grid related-grid">'+''.join(card(by_id[x],prefix,True) for x in related_ids)+'</div></section>' if related_ids else ''
    ordered=sorted(works,key=lambda x:([p['id'] for p in periods].index(x['period']),x['year']))
    i=ordered.index(w); prev=ordered[i-1] if i>0 else None; nxt=ordered[i+1] if i+1<len(ordered) else None
    sequence='<nav class="work-sequence wrap" aria-label="前后作品">'+(f'<a href="../{prev["id"]}/">← {prev["title"]}</a>' if prev else '<span></span>')+f'<a href="../#{w["period"]}">返回{period["title"]}</a>'+(f'<a href="../{nxt["id"]}/">{nxt["title"]} →</a>' if nxt else '<span></span>')+'</nav>'
    body=f'''{breadcrumb(w['title'],1)}<header class="work-heading wrap"><p class="eyebrow">CARAVAGGIO / {e(period['title'])}</p><h1>{e(w['title'])}</h1><p class="work-original">{e(w['original_title'])}</p>{'<p class="attribution work-attribution">作者归属仍有争议：卡拉瓦乔或斯帕达里诺</p>' if w['period']=='question' else ''}</header><div class="work-layout wrap"><figure class="work-photo"><a data-photo href="../images/{w['photo']}" data-caption="{e(w['title'])} · {e(museums[w['museum']])}">{img(w['source_number'],prefix,True)}</a><figcaption>参观照片 / Merton · 点击放大</figcaption></figure><div class="work-record">{facts}<section><h2>看画</h2><p>{e(w['observation'])}</p></section><section><h2>这幅画的故事</h2><p>{e(w['story'])}</p><div class="work-sources">{source}</div></section>{note}<p class="source">基本信息另据配套现场展签；未配展签的作品见上述核对说明。资料核对：2026年9月。</p></div></div>{context}{related}{sequence}'''
    target=BASE/w['id']; target.mkdir(exist_ok=True)
    (target/'index.html').write_text(shell(w['title']+' · 卡拉瓦乔',w['observation'],body,1,True))
# Comparison groups share the same originals, and never silently crop them.
nav=''.join(f'<a href="#{g["id"]}">{g["title"]}</a>' for g in groups)
comparisons=''
for g in groups:
    cells=''
    for x in g['works']:
        w=by_id[x]
        cells+=f'<figure class="comparison-work"><a data-photo href="../images/{w["photo"]}" data-caption="{e(w["title"])} · {e(museums[w["museum"]])}">{img(w["source_number"],"../")}</a><figcaption><a href="../{w["id"]}/">{e(w["title"])} →</a><span>{e(w["date"])}</span><span>{e(museums[w["museum"]])}</span></figcaption></figure>'
    context=f'<details class="comparison-context"><summary>看看三幅画在教堂中的位置</summary><a data-photo href="../images/caravaggio-478.jpg" data-caption="孔塔雷利礼拜堂全景">{img(478,"../")}</a></details>' if g['id']=='matthew' else ''
    comparisons+=f'<section class="compare-group" id="{g["id"]}" aria-labelledby="compare-{g["id"]}"><h2 id="compare-{g["id"]}">{g["title"]}</h2><p>{g["text"]}</p><div class="comparison-grid" style="--columns:{min(len(g["works"]),4)}">{cells}</div>{context}</section>'
body=breadcrumb('并排看画',1)+f'<header class="compare-header wrap"><p class="eyebrow">CARAVAGGIO / SIDE BY SIDE</p><h1>并排看画</h1><p>同一个题材，不同的手势、目光与命运。<br>点击照片放大，点击画名进入作品札记。</p><p class="source">照片按画面排布，不代表作品实物的比例大小。</p></header><div class="wrap"><nav class="compare-nav" aria-label="选择比较组">{nav}</nav>{comparisons}</div>'
(BASE/'compare').mkdir(exist_ok=True)
(BASE/'compare/index.html').write_text(shell('并排看画 · 卡拉瓦乔','两幅占卜者、四幅施洗者约翰、圣马太三联画，以及收藏和构图上的联系。',body,1))
from build_european import build
build()
print(f'Built Caravaggio: {len(works)} work pages and {len(groups)} comparison groups.')
