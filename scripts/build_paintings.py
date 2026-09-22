"""Build the Chinese painting section from reviewed photo sequences; stdlib only."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'museum-notes/chinese-painting'
data=json.loads((PAGE/'data/works.json').read_text())
works=data['works'];periods=data['periods'];names={p[0]:p[1] for p in periods}

def asset(work,number):
    return next(p for p in work['sequence']+work['extras'] if p['number']==number)

def picture(p,prefix,alt,eager=False):
    rotated=p['rotation']!=0
    w,h=(p['height'],p['width']) if rotated else (p['width'],p['height'])
    style=f'--ratio:{w/h:.8f};--native-width:{w}px;'
    if rotated:style+=f'--inner-width:{p["width"]/p["height"]*100:.8f}%;--inner-height:{p["height"]/p["width"]*100:.8f}%;'
    return f'<span class="image-box{" rotated" if rotated else ""}" style="{style}"><img src="{prefix}{p["photo"]}" alt="{e(alt)}" width="{p["width"]}" height="{p["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async"></span>'

def frame(title,content,depth=0,description=''):
    up='../'*(depth+1);home='./' if depth==0 else '../'
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} | Merton · 博物馆札记</title><meta name="description" content="{e(description)}"><link rel="stylesheet" href="{up}museum.css"><link rel="stylesheet" href="{home}painting.css"><script src="{home}painting.js" defer></script></head>
<body id="top"><a class="skip-link" href="#content">跳至正文</a><header class="site-header"><a class="signature" href="{up}">Merton</a><nav aria-label="主导航"><a href="{up}">博物馆首页</a><a href="{home}">中国书画</a></nav></header>
<main id="content">{content}</main><footer class="site-footer wrap"><a href="{up}">← 博物馆首页</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>
<dialog id="painting-lightbox" aria-labelledby="zoom-caption"><div class="zoom-toolbar"><button type="button" id="zoom-toggle" aria-pressed="false">放大细节</button><button type="button" id="zoom-close">关闭 ×</button></div><div class="zoom-viewport"></div><p id="zoom-caption"></p><a id="zoom-original" href="#" target="_blank" rel="noopener">打开原始照片 ↗</a></dialog>
</body></html>'''

def gallery(w,photos,title,gid,sequence=False):
    figures=''
    for i,p in enumerate(photos):
        alt=f'{w["title"]} · {p["caption"]}'
        figures+=f'<figure class="slide" id="{gid}-{i+1}"><a class="photo-open" href="../images/{p["photo"]}" data-caption="{e(alt)}" aria-label="放大：{e(alt)}">{picture(p,"../images/",alt,i==0 and sequence)}</a><figcaption><span>{i+1:02d} / {len(photos):02d}</span> {e(p["caption"])}</figcaption></figure>'
    instruction='按画卷从右至左排列，点击“下一段”依次观看；照片之间有重叠。' if sequence and w['form']=='手卷' and w['id']!='xu-daoning-fishermen' else '点击照片可放大；有多张照片时，可以切换查看。'
    return f'''<section class="work-gallery wrap" data-gallery data-direction="{"rtl" if sequence and w['form']=='手卷' else "ltr"}" aria-labelledby="{gid}-title"><div class="gallery-heading"><h2 id="{gid}-title">{title}</h2><p>{instruction}</p></div><div class="gallery-controls" hidden><button type="button" data-prev>上一张</button><span class="gallery-count" role="status" aria-live="polite"></span><button type="button" data-next>{'下一段' if sequence and w['form']=='手卷' else '下一张'}</button><button type="button" data-show-all aria-pressed="false">展开全部</button></div><div class="gallery-stage">{figures}</div><div class="gallery-thumbs" aria-label="选择照片" hidden></div></section>'''

for index,w in enumerate(works):
    target=PAGE/w['id'];target.mkdir(exist_ok=True)
    rows=''.join(f'<div><dt>{label}</dt><dd>{e(value)}</dd></div>' for label,value in [('作者',w['artist']),('年代',w['date']),('形制',w['form']),('材质',w['medium']),('馆藏编号',w['accession'])])
    paragraphs=''.join(f'<p>{e(p)}</p>' for p in w['notes'])
    note=f'<p class="record-note">{e(w["caveat"])}</p>' if w['caveat'] else ''
    extras=gallery(w,w['extras'],'全景与题跋','extras') if w['extras'] else ''
    related=''
    if w['id'] in ['qiao-zhongchang-red-cliff','li-song-red-cliff']:
        other='li-song-red-cliff' if w['id']=='qiao-zhongchang-red-cliff' else 'qiao-zhongchang-red-cliff'
        ow=next(o for o in works if o['id']==other)
        related=f'<p class="featured-note"><a href="../{other}/">对着看：{e(ow["artist"])}《{e(ow["title"])}》 →</a></p>'
    previous=works[index-1] if index else None;following=works[index+1] if index+1<len(works) else None
    prevlink=f'<a href="../{previous["id"]}/">← {e(previous["title"])}</a>' if previous else '<span></span>'
    nextlink=f'<a href="../{following["id"]}/">{e(following["title"])} →</a>' if following else '<span></span>'
    content=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../../">博物馆札记</a><span>/</span><a href="../">中国书画</a><span>/</span><a href="../#{w['period']}">{names[w['period']]}</a></nav>
<header class="work-heading wrap"><p class="eyebrow">{names[w['period']]} / {e(w['form'])}</p><h1>{e(w['title'])}</h1><p class="work-byline">{e(w['artist'])} · {e(data['museum'])}</p></header>
{gallery(w,w['sequence'],'看画','painting',True)}
<section class="work-notes wrap"><div><h2>作品札记</h2>{paragraphs}{note}{related}</div><aside><dl>{rows}</dl><p class="source">基本信息据现场展签整理。<br><a href="{e(w['url'])}" target="_blank" rel="noopener noreferrer">馆方藏品记录 ↗</a></p><p class="source">照片 © Merton</p></aside></section>
{extras}<nav class="work-pagination wrap" aria-label="前后作品">{prevlink}<a href="../#{w['period']}">返回目录</a>{nextlink}</nav>'''
    (target/'index.html').write_text(frame(w['title'],content,1,f'{w["artist"]}《{w["title"]}》，{w["date"]}。Merton在纳尔逊－阿特金斯艺术博物馆拍摄的作品照片与札记。'))

nav=''.join(f'<a href="#{key}">{name}<span>{sum(w["period"]==key for w in works)}</span></a>' for key,name,_ in periods)
sections=''
for key,name,description in periods:
    cards=''
    for w in [o for o in works if o['period']==key]:
        p=asset(w,w['cover']);is_detail=w['form']=='手卷' and w['cover']!=359
        cards+=f'''<article class="painting-card"><a class="painting-thumb" href="{w['id']}/">{picture(p,'images/',w['title']+' · '+p['caption'])}<span class="cover-kind">{'局部' if is_detail else '全貌'}</span></a><div class="painting-card-body"><p class="painting-artist">{e(w['artist'])} · {e(w['form'])}</p><h3><a href="{w['id']}/">{e(w['title'])}</a></h3><p>{e(w['date'])}</p><a class="text-link" href="{w['id']}/">{'逐段看画' if w['form']=='手卷' else '查看作品'} →</a></div></article>'''
    sections+=f'<section class="period-section wrap" id="{key}" aria-labelledby="heading-{key}"><div class="period-heading"><h2 id="heading-{key}">{name}</h2><p>{description}</p></div><div class="paintings-grid">{cards}</div></section>'
featured=''.join(f'<a href="{w["id"]}/">{w["title"]} ↗</a>' for w in works if w['featured'])
hero=asset(next(w for w in works if w['id']=='xia-gui-twelve-views'),347)
content=f'''<section class="painting-intro wrap"><p class="eyebrow">CHINESE PAINTING &amp; CALLIGRAPHY</p><h1>中国书画</h1><p class="subtitle">先从纳尔逊的宋代山水看起。</p><p class="intro">这一批整理了{len(works)}件作品，从五代到元，以宋画为主。长卷分段看，册页和立轴看全貌；题跋也一起留下。</p><div class="painting-intro-meta"><span>{len(works)} 件作品</span><span>纳尔逊－阿特金斯艺术博物馆</span><span>摄影 / Merton</span></div><figure class="painting-banner"><a href="xia-gui-twelve-views/">{picture(hero,'images/','夏圭《山水十二景图卷》局部：渔舟与岸边',True)}</a><figcaption>夏圭《山水十二景图卷》局部 · 渔笛清幽</figcaption></figure></section>
<section class="painting-start wrap"><h2>可以先看这几幅</h2><div class="featured-works">{featured}</div></section>
<nav class="period-nav wrap" aria-label="按时代浏览">{nav}</nav>{sections}
<aside class="editorial-note wrap"><h2>这批照片</h2><p>照片拍摄于纳尔逊－阿特金斯艺术博物馆的 <a href="{data['exhibition']['url']}" target="_blank" rel="noopener noreferrer">Legendary Landscapes: Sublime Visions from China’s Song Dynasty</a> 展览。馆方公布的展期为2026年3月21日至9月27日。</p><p>作品名称和基本信息按现场展签整理，补充资料链接到馆方记录。金与南宋在时间上并存；“传”与宽断代均保留在具体作品说明中。</p><p>原照片按作品配对并筛选。长卷依画面和文字核对次序，以分段照片展示；题跋与展柜全景另列。照片中的反光、遮挡与角度差异仍保留，未做无缝拼接或补绘。本批以绘画及附随题跋为主，独立书法作品以后再补。</p></aside>'''
(PAGE/'index.html').write_text(frame('中国书画 · 五代至宋元',content,description='Merton在纳尔逊－阿特金斯艺术博物馆拍摄的13件五代至宋元绘画，按时代整理，长卷分段浏览。'))
print(f'Generated Chinese painting index and {len(works)} work pages.')
