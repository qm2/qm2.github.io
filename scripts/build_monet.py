"""Build Monet's water-lily notebook from verified photo/label records.
Run python3 scripts/build_monet.py; shared gallery behavior and styling remain unchanged.
"""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/monet-water-lilies'
d=json.loads((BASE/'data/works.json').read_text());works=d['works'];photos=d['photos'];museums=d['museums'];periods=d['periods'];groups=d['groups'];by={w['id']:w for w in works}
assert len(by)==len(works)
for w in works:
    assert w['period'] in {p['id'] for p in periods}
    assert all(str(n) in photos for n in [w['source_number'],*w['extra_photos']])
for p in photos.values(): assert (BASE/'images'/p['file']).is_file()
for g in groups: assert len(set(g['works']))==len(g['works']) and all(x in by for x in g['works'])
paintings=sum(w['record_kind']=='painting' for w in works);ensemble_count=sum(w['record_kind']=='ensemble' for w in works)
summary=f'{paintings}幅睡莲与池塘绘画 · {ensemble_count}组橘园记录'
LIGHTBOX='''<dialog id="art-lightbox" aria-labelledby="lightbox-caption"><div class="lightbox-tools"><button type="button" id="photo-prev" aria-label="上一张照片">←</button><button type="button" id="photo-next" aria-label="下一张照片">→</button><button type="button" id="zoom-toggle" aria-pressed="false">放大细看 ＋</button><a id="original-photo" href="#" target="_blank" rel="noopener">原图 ↗</a><button type="button" id="photo-close" aria-label="关闭大图">关闭 ×</button></div><div id="photo-stage" tabindex="0" aria-label="照片区域；放大后可滚动查看"><img id="large-photo" alt=""></div><p id="lightbox-caption"></p></dialog>'''
def shell(title,desc,body,depth=0):
    topic='../'*depth or './';note='../'*(depth+1)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="{e(desc)}"><link rel="stylesheet" href="{note}museum.css"><link rel="stylesheet" href="{note}caravaggio/caravaggio.css"><link rel="stylesheet" href="{topic}monet.css"><script src="{note}caravaggio/caravaggio.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{note}">Merton</a><nav aria-label="主导航"><a href="{note}european-painting/">欧洲绘画</a><a href="{topic}#collection">全部作品</a><a href="{topic}compare/">并排看画</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="{note}">← 博物馆札记</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
def img(n,prefix='',high=False):
    p=photos[str(n)]
    return f'<img src="{prefix}images/{p["file"]}" alt="{e(p["caption"])} · Merton参观照片" width="{p["width"]}" height="{p["height"]}" {"fetchpriority=high" if high else "loading=lazy"} decoding="async">'
def photo_link(n,prefix='',label=None):
    p=photos[str(n)]
    return f'<a data-photo href="{prefix}images/{p["file"]}" data-caption="{e(p["caption"])} · Merton参观照片">{label or img(n,prefix)}</a>'
def place(w):
    return museums[w['museum']]+(' · 西雅图借展' if w.get('visit') else '')
def card(w,prefix='',compact=False):
    text=' '.join([w['title'],w['original_title'],w['artist'],place(w),w['accession'],w.get('visit',''),*w['paragraphs']])
    badge={'related':'池畔延伸','ensemble':'组画／展厅记录'}.get(w['record_kind'],'')
    return f'''<article class="art-card" data-period="{w['period']}" data-museum="{w['museum']}" data-tags="{' '.join(w['tags'])}" data-search="{e(text)}"><a class="art-thumbnail" href="{prefix}{w['id']}/">{img(w['source_number'],prefix)}</a><div class="art-card-copy"><p class="card-kicker">{e(w['date'])}{'<span class="attribution">'+badge+'</span>' if badge else ''}</p><h3><a href="{prefix}{w['id']}/">{e(w['title'])}</a></h3><p class="card-museum">{e(place(w))}</p>{'' if compact else '<p class="card-look">'+e(w['observation'])+'</p>'}<div class="card-actions"><a href="{prefix}{w['id']}/">读作品札记 →</a>{photo_link(w['source_number'],prefix,'放大照片 ↗')}</div></div></article>'''
def breadcrumb(tail='',depth=0):
    topic='../'*depth or './';note='../'*(depth+1)
    return f'<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="{note}">博物馆札记</a><span>/</span><a href="{note}european-painting/">欧洲绘画</a><span>/</span>'+ (f'<a href="{topic}">莫奈的睡莲</a><span>/</span><span>{e(tail)}</span>' if tail else '<span>莫奈的睡莲</span>')+'</nav>'
def citations(w):
    return '<div class="work-sources">'+''.join(f'<p><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗</a></p>' for label,url in w['sources'])+'</div>'
hero=by[d['hero']]
intro=f'''{breadcrumb()}<section class="car-hero wrap"><div class="car-hero-copy"><p class="eyebrow">EUROPEAN PAINTING / 004</p><h1>莫奈的睡莲</h1><p class="artist-dates">CLAUDE MONET &nbsp; 1840—1926</p><p class="car-lede">同一座池塘，<br>在不同的地方重逢。</p><p class="car-intro">从日本桥走到水面，再走进橘园。把看过的睡莲放在一起，慢慢分辨花、倒影和笔触。</p><div class="hero-links"><a class="text-link" href="#collection">从池塘看起 ↓</a><a class="text-link" href="compare/">并排看画 →</a></div><p class="car-stats"><b>{paintings}</b> 幅睡莲与池塘绘画<br><b>{ensemble_count}</b> 组橘园记录<br>{len(photos)} 张参观照片 · 含展厅与局部细节</p></div><figure class="car-hero-image"><a href="{hero['id']}/">{img(hero['source_number'],high=True)}</a><figcaption>{e(hero['title'])}<br><span>{e(museums[hero['museum']])}</span></figcaption></figure></section>'''
featured=[groups[0],groups[2],groups[4]]
reading='<section class="wrap car-reading"><div class="car-heading"><div><p class="eyebrow">LOOK TOGETHER</p><h2>几条重看的线索</h2></div><a href="compare/">全部五组比较 →</a></div><div class="route-grid">'+''.join(f'<a class="reading-route" href="compare/#{g["id"]}"><span class="eyebrow">{len(g["works"])} 件／组</span><h3>{e(g["title"])} ↗</h3><p>{e(g["text"])}</p></a>' for g in featured)+'</div></section>'
options=''.join(f'<option value="{k}">{e(v)}</option>' for k,v in museums.items())
subjects=''.join(f'<option value="{p["id"]}">{e(p["title"])}</option>' for p in periods)
filters=f'''<div class="art-controls" data-count-unit="条记录" hidden><div class="art-fields"><label>找一幅画<input type="search" id="art-search" placeholder="画名、博物馆、编号…" autocomplete="off"></label><label>收藏机构<select id="art-museum"><option value="all">全部收藏</option>{options}</select></label><label>主题／观看地点<select id="art-subject"><option value="all">全部主题</option>{subjects}<option value="seattle-loan">西雅图 · 私人借展</option></select></label></div><div class="art-results"><p id="art-count" role="status" aria-live="polite">{len(works)} 条记录（含组画与延伸作品）</p><div><button type="button" id="gallery-mode" aria-pressed="false">画廊模式</button><button type="button" id="art-reset">清除筛选</button></div></div></div>'''
nav=''.join(f'<a href="#{p["id"]}">{p["title"]}<span>{sum(w["period"]==p["id"] for w in works)}</span></a>' for p in periods)
sections=''.join(f'<section class="era-section" id="{p["id"]}" aria-labelledby="heading-{p["id"]}"><div class="era-heading"><p class="eyebrow">{p["range"]}</p><h2 id="heading-{p["id"]}">{p["title"]}</h2><p>{p["intro"]}</p></div><div class="art-grid">'+''.join(card(w) for w in sorted(works,key=lambda x:x['year']) if w['period']==p['id'])+'</div></section>' for p in periods)
collection=f'<section class="wrap car-collection" id="collection"><div class="car-heading"><div><p class="eyebrow">THE WATER GARDEN</p><h2>沿着池塘慢慢看</h2></div><p>作品年代依展签与馆方记录；私人借展另注观看地点。</p></div><nav class="era-nav" aria-label="主题">{nav}</nav>{filters}<p id="art-empty" hidden>没有找到符合条件的作品，可以换个词或清除筛选。</p>{sections}</section>'
about=f'''<aside class="editorial-note wrap"><h2>关于这一辑</h2><p>{summary}。橘园的七张照片按一组展厅记录整理，不把视角数量当作作品数量。日本桥画的是同一座睡莲池，保留在专题开头。</p><p>照片均为现场拍摄，保留画框、反光和展厅视角；展签用于核对，不放入画廊。卡内基的局部照片附在同一作品下，近似重复的一张留在本地。</p><p>“看画”记录重看照片时可留意的细节，不代写当时的感受。作品来源与资料疑点分别标注。</p><p class="source">2026年10月整理 · {len(photos)}张现场照片。</p></aside>'''
(BASE/'index.html').write_text(shell('莫奈的睡莲 · 欧洲绘画',summary+'，以现场照片、细节与收藏故事串起吉维尼水园。',intro+reading+collection+about))
ordered=sorted(works,key=lambda w:([p['id'] for p in periods].index(w['period']),w['year']))
for w in works:
    period=next(p for p in periods if p['id']==w['period'])
    fields=[('作者',w['artist']),('年代',w['date']),('材料',w['material']),('收藏／所在',museums[w['museum']]),('编号／位置',w['accession'])]
    if w['dimensions']: fields.insert(3,('尺寸',w['dimensions']))
    if w.get('visit'): fields.append(('观看地点',w['visit']))
    facts='<dl class="work-facts">'+''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in fields)+'</dl>'
    text=''.join(f'<p>{e(p)}</p>' for p in w['paragraphs'])
    note=f'<p class="record-note">{e(w["source_note"])}</p>' if w['source_note'] else ''
    details=''
    if w['extra_photos']:
        title='展厅中的不同视角' if w['record_kind']=='ensemble' else '走近看笔触'
        details=f'<section class="wrap photo-notes"><p class="eyebrow">LOOK CLOSER</p><h2>{title}</h2><p>点击照片放大，可以在大图中切换照片。</p><div class="photo-notes-grid">'+''.join(f'<figure>{photo_link(n,"../")}<figcaption>{e(photos[str(n)]["caption"])} · Merton</figcaption></figure>' for n in w['extra_photos'])+'</div></section>'
    members=[g for g in groups if w['id'] in g['works']]
    ids=list(dict.fromkeys(x for g in members for x in g['works'] if x!=w['id']))
    related='<section class="related-section wrap"><p class="eyebrow">CONTINUE LOOKING</p><h2>也放在一起看</h2><div class="relation-links">'+''.join(f'<a href="../compare/#{g["id"]}">{e(g["title"])} →</a>' for g in members)+'</div><div class="art-grid related-grid">'+''.join(card(by[x],'../',True) for x in ids)+'</div></section>' if ids else ''
    i=ordered.index(w)
    seq='<nav class="work-sequence wrap" aria-label="前后作品">'+(f'<a href="../{ordered[i-1]["id"]}/">← {e(ordered[i-1]["title"])}</a>' if i else '<span></span>')+f'<a href="../#{w["period"]}">返回{e(period["title"])}</a>'+(f'<a href="../{ordered[i+1]["id"]}/">{e(ordered[i+1]["title"])} →</a>' if i+1<len(ordered) else '<span></span>')+'</nav>'
    body=f'''{breadcrumb(w['title'],1)}<header class="work-heading wrap"><p class="eyebrow">CLAUDE MONET / {e(period['title'])}</p><h1>{e(w['title'])}</h1><p class="work-original">{e(w['original_title'])}</p></header><div class="work-layout wrap"><figure class="work-photo">{photo_link(w['source_number'],'../')}<figcaption>Merton参观照片 · 点击放大</figcaption></figure><div class="work-record">{facts}<section><h2>看画</h2><p>{e(w['observation'])}</p></section><section><h2>作品札记与资料</h2>{text}{citations(w)}</section>{note}<p class="source">基本信息据馆方资料与已有现场展签 · 2026年10月核对。</p></div></div>{details}{related}{seq}'''
    target=BASE/w['id'];target.mkdir(exist_ok=True);(target/'index.html').write_text(shell(w['title']+' · 莫奈',w['observation'],body,1))
comparisons=''
for g in groups:
    cells=''.join(f'<figure class="comparison-work">{photo_link(by[x]["source_number"],"../")}<figcaption><a href="../{x}/">{e(by[x]["title"])} →</a><span>{e(by[x]["date"])}</span><span>{e(place(by[x]))}</span></figcaption></figure>' for x in g['works'])
    comparisons+=f'<section class="compare-group" id="{g["id"]}" aria-labelledby="compare-{g["id"]}"><h2 id="compare-{g["id"]}">{e(g["title"])}</h2><p>{e(g["text"])}</p><div class="comparison-grid" style="--columns:{min(len(g["works"]),4)}">{cells}</div></section>'
nav=''.join(f'<a href="#{g["id"]}">{e(g["title"])}</a>' for g in groups)
body=breadcrumb('并排看画',1)+f'<header class="compare-header wrap"><p class="eyebrow">CLAUDE MONET / SIDE BY SIDE</p><h1>并排看睡莲</h1><p>从桥的位置、倒影与笔触开始。点击图片放大，点击画名读作品札记。</p><p class="source">照片排布不代表实物比例，也不是组画的数字复原。</p></header><div class="wrap"><nav class="compare-nav" aria-label="比较组">{nav}</nav>{comparisons}</div>'
(BASE/'compare').mkdir(exist_ok=True);(BASE/'compare/index.html').write_text(shell('并排看睡莲 · 莫奈','日本桥、水面倒影与晚年大画幅的五组比较。',body,1))
from build_european import build
build()
print(f'Built Monet: {summary}; {len(photos)} photographs; {len(groups)} comparisons.')
