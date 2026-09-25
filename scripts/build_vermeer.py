"""Build the Vermeer photo notebook using the shared European painting presentation.
Edit museum-notes/vermeer/data/works.json, then run this script.
No network access or image processing is needed to rebuild the public pages.
"""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/vermeer'
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
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="{e(desc)}"><link rel="stylesheet" href="{notebook}museum.css"><link rel="stylesheet" href="{notebook}caravaggio/caravaggio.css"><script src="{notebook}caravaggio/caravaggio.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{notebook}">Merton</a><nav aria-label="主导航"><a href="{notebook}european-painting/">欧洲绘画</a><a href="{topic}#collection">全部作品</a><a href="{topic}compare/">并排看画</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="{notebook}">← 博物馆札记</a><span>参观记录 / Merton · 图片来源逐件标注</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
def img(n,prefix='',high=False):
    p=photos[str(n)]
    name=p['caption']
    return f'<img src="{prefix}images/{p["file"]}" alt="{e(name)} · {e(p["credit"])}" width="{p["width"]}" height="{p["height"]}" {"fetchpriority=high" if high else "loading=lazy"} decoding="async">'
def credit(w):
    p=photos[str(w['source_number'])]
    return e(p['credit'])+(f' · <a href="{e(p["source_url"])}" target="_blank" rel="noopener noreferrer">图片来源 ↗</a>' if p.get('source_url') else '')
def caption(w):
    return e(w['title']+' · '+museums[w['museum']]+' · '+photos[str(w['source_number'])]['credit'])
def enlarge(w,prefix='',label='放大照片 ↗'):
    return f'<a class="enlarge" data-photo href="{prefix}images/{w["photo"]}" data-caption="{caption(w)}">{label}</a>'
def card(w,prefix='',compact=False):
    badge='<span class="attribution">补充图</span>' if w['image_kind']=='supplement' else ''

    return f'''<article class="art-card" data-period="{w['period']}" data-museum="{w['museum']}" data-tags="{' '.join(w['tags'])}" data-search="{e(' '.join([w['title'],w['original_title'],w['artist'],w['story'],museums[w['museum']],w['accession']]+w.get('search_aliases',[])))}"><a class="art-thumbnail" href="{prefix}{w['id']}/">{img(w['source_number'],prefix)}</a><div class="art-card-copy"><p class="card-kicker">{e(w['date'])}{badge}</p><h3><a href="{prefix}{w['id']}/">{e(w['title'])}</a></h3><p class="card-museum">{e(w.get('ownership') or museums[w['museum']])}</p>{'' if compact else '<p class="card-look">'+e(w['observation'])+'</p>'}<div class="card-actions"><a href="{prefix}{w['id']}/">读作品札记 →</a>{enlarge(w,prefix)}</div></div></article>'''
def breadcrumb(tail='',depth=0):
    topic='../'*depth or './'; note='../'*(depth+1)
    return f'<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="{note}">博物馆札记</a><span>/</span><a href="{note}european-painting/">欧洲绘画</a><span>/</span>'+ (f'<a href="{topic}">维米尔</a><span>/</span><span>{e(tail)}</span>' if tail else '<span>维米尔</span>')+'</nav>'
hero=by_id['view-delft']
hero_html=f'''{breadcrumb()}<section class="car-hero wrap"><div class="car-hero-copy"><p class="eyebrow">EUROPEAN PAINTING / 003</p><h1>维米尔</h1><p class="artist-dates">JOHANNES VERMEER &nbsp; 1632—1675</p><p class="car-lede">从代尔夫特的街道，<br>走进窗边的房间。</p><p class="car-intro">把在荷兰、巴黎和美国看过的维米尔放到一起。信纸、乐器、桌上的小物件，还有那些短暂抬头的人。</p><div class="hero-links"><a class="text-link" href="#collection">浏览全部作品 ↓</a><a class="text-link" href="compare/">并排看画 →</a></div><p class="car-stats"><b>20</b> 件作品 <span>来自 7 家收藏机构</span><br><b>15</b> 张参观照片 <span>另有 5 张补充图</span></p></div><figure class="car-hero-image"><a href="view-delft/">{img(588,high=True)}</a><figcaption>代尔夫特风景 · 约1660—1661年<br><span>莫瑞泰斯皇家美术馆 · 海牙</span></figcaption></figure></section>'''
ways=''.join(f'<a class="reading-route" href="compare/#{g["id"]}"><span class="eyebrow">0{i+1} / {len(g["works"])} 件作品</span><h3>{g["title"]} ↗</h3><p>{g["text"]}</p></a>' for i,g in enumerate(groups[:3]))
reading=f'<section class="wrap car-reading"><div class="car-heading"><div><p class="eyebrow">LOOK TOGETHER</p><h2>几组画，连着看</h2></div><a href="compare/">全部六组比较 →</a></div><div class="route-grid">{ways}</div></section>'
period_nav=''.join(f'<a href="#{p["id"]}">{p["title"]}<span>{sum(w["period"]==p["id"] for w in works)}</span></a>' for p in periods)
options=''.join(f'<option value="{k}">{e(v)}</option>' for k,v in museums.items())
subject_options=''.join(f'<option value="{p["id"]}">{p["title"]}</option>' for p in periods)
filters=f'''<div class="art-controls" hidden><div class="art-fields"><label>找一幅画<input type="search" id="art-search" placeholder="作品、收藏地点、故事…" autocomplete="off"></label><label>收藏机构<select id="art-museum"><option value="all">全部机构</option>{options}</select></label><label>主题／观看记录<select id="art-subject"><option value="all">全部主题</option>{subject_options}<option value="frick-2025">弗里克 · 2025年8月</option></select></label></div><div class="art-results"><p id="art-count" role="status" aria-live="polite">20 件作品</p><div><button type="button" id="gallery-mode" aria-pressed="false">画廊模式</button><button type="button" id="art-reset">清除筛选</button></div></div></div>'''
sections=''.join(f'''<section class="era-section" id="{p['id']}" aria-labelledby="heading-{p['id']}"><div class="era-heading"><p class="eyebrow">{p['range']}</p><h2 id="heading-{p['id']}">{p['title']}</h2><p>{p['intro']}</p></div><div class="art-grid">{''.join(card(w) for w in sorted(works,key=lambda x:x['year']) if w['period']==p['id'])}</div></section>''' for p in periods)
collection=f'''<section id="collection" class="wrap car-collection"><div class="car-heading"><div><p class="eyebrow">THE PAINTINGS</p><h2>按题材慢慢看</h2></div><p>年代依馆方记录；借展作品保留所属收藏。</p></div><nav class="era-nav" aria-label="题材">{period_nav}</nav>{filters}<p id="art-empty" hidden>没有找到符合条件的作品，可以换个词或清除筛选。</p>{sections}</section>'''
frick='''<aside class="editorial-note wrap"><h2>2025年8月，在弗里克</h2><p>那次看到了五幅维米尔。由于没有现场照片，这里用补充图记下这次观看。</p><p>夏季专题展“Vermeer’s Love Letters”把馆藏《女主人与女仆》与借来的《情书》《写信的女子与女仆》放到一起。另两件馆藏《军官与微笑的女子》《音乐课被打断的少女》，那次也都看到了。</p><p>《情书》属于荷兰国立博物馆，《写信的女子与女仆》属于爱尔兰国家美术馆；这两件的观看地点都是纽约。</p><p class="source"><a href="https://www.frick.org/press/frick_vermeers_love_letters">弗里克展览资料 ↗</a> · <a href="compare/#letters">把几幅书信画放在一起看 →</a></p></aside>'''
about='''<aside class="editorial-note wrap"><h2>关于这一辑</h2><p>这一辑收录20件看过的作品：15件有自己的参观照片，另5件是2025年8月在弗里克看过的作品，以补充图呈现。现场照片保留画框、反光和拍摄角度，展签只用于核对资料。</p><p>补充图采用 Wikimedia Commons 标记为公共领域的忠实复制图，来源逐件注明。收藏机构与观看地点分别记录。</p><p>作品资料和故事附有来源；“看画”是重看图片时可以留意的细节，不代写当时的个人感受。</p><p class="source">2026年9月整理 · 20件作品 / 15张参观照片 / 5张补充图。</p></aside>'''
(BASE/'index.html').write_text(shell('维米尔 · 欧洲绘画','Merton看过的20件维米尔作品：15张参观照片、5张补充图，含2025年夏季弗里克书信专题展与六组比较。',hero_html+reading+frick+collection+about))
# Dedicated work pages; stable URLs, sources next to the claims, reciprocal comparison links.
for w in works:
    prefix='../'; period=next(p for p in periods if p['id']==w['period'])
    fields=[('作者',w['artist']),('年代',w['date']),('材料',w['material']),('收藏／所在',w.get('ownership') or museums[w['museum']]),('编号／位置',w['accession'])]
    if w.get('visit'): fields.append(('观看记录',w['visit']))
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
    body=f'''{breadcrumb(w['title'],1)}<header class="work-heading wrap"><p class="eyebrow">JOHANNES VERMEER / {e(period['title'])}</p><h1>{e(w['title'])}</h1><p class="work-original">{e(w['original_title'])}</p>{'<p class="attribution work-attribution">'+e(w['artist'])+'</p>' if w['status']!='autograph' else ''}</header><div class="work-layout wrap"><figure class="work-photo"><a data-photo href="../images/{w['photo']}" data-caption="{caption(w)}">{img(w['source_number'],prefix,True)}</a><figcaption>{credit(w)} · 点击放大</figcaption></figure><div class="work-record">{facts}<section><h2>看画</h2><p>{e(w['observation'])}</p></section><section><h2>这幅画的故事</h2><p>{e(w['story'])}</p><div class="work-sources">{source}</div></section>{note}<p class="source">基本信息据馆方目录及已有现场展签。资料核对：2026年9月。</p></div></div>{context}{related}{sequence}'''
    target=BASE/w['id']; target.mkdir(exist_ok=True)
    (target/'index.html').write_text(shell(w['title']+' · 维米尔',w['observation'],body,1,True))
# Comparison groups share the same originals, and never silently crop them.
nav=''.join(f'<a href="#{g["id"]}">{g["title"]}</a>' for g in groups)
comparisons=''
for g in groups:
    cells=''
    for x in g['works']:
        w=by_id[x]
        cells+=f'<figure class="comparison-work"><a data-photo href="../images/{w["photo"]}" data-caption="{caption(w)}">{img(w["source_number"],"../")}</a><figcaption><a href="../{w["id"]}/">{e(w["title"])} →</a><span>{e(w["date"])}</span><span>{e(w["artist"])}</span><span>{e(museums[w["museum"]])}</span><span>{credit(w)}</span></figcaption></figure>'
    context=''
    comparisons+=f'<section class="compare-group" id="{g["id"]}" aria-labelledby="compare-{g["id"]}"><h2 id="compare-{g["id"]}">{g["title"]}</h2><p>{g["text"]}</p><div class="comparison-grid" style="--columns:{min(len(g["works"]),4)}">{cells}</div>{context}</section>'
body=breadcrumb('并排看画',1)+f'<header class="compare-header wrap"><p class="eyebrow">JOHANNES VERMEER / SIDE BY SIDE</p><h1>并排看画</h1><p>同一个题材，不同的手势、目光与命运。<br>点击照片放大，点击画名进入作品札记。</p><p class="source">照片按画面排布，不代表作品实物的比例大小。</p></header><div class="wrap"><nav class="compare-nav" aria-label="选择比较组">{nav}</nav>{comparisons}</div>'
(BASE/'compare').mkdir(exist_ok=True)
(BASE/'compare/index.html').write_text(shell('并排看画 · 维米尔','维米尔的书信、人物面容、城市、日常动作、音乐与寓意，六组作品比较。',body,1))

from build_european import build
build()
print(f'Built Vermeer: {len(works)} work pages and {len(groups)} comparison groups.')
