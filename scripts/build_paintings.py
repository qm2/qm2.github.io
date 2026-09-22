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

def frame(title,content,depth=0,description='',sibling=False):
    up='../'*(depth+1);home='./' if depth==0 else '../'
    if sibling:up='../';home='../chinese-painting/'
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
    instruction='按画卷从右至左排列，点击“下一段”依次观看；照片之间有重叠。' if sequence and w['form']=='手卷' and w['id'] not in ['xu-daoning-fishermen','cheng-qi-tilling','cheng-qi-weaving'] else '点击照片可放大；有多张照片时，可以切换查看。'
    return f'''<section class="work-gallery wrap" data-gallery data-direction="{"rtl" if sequence and w['form']=='手卷' else "ltr"}" aria-labelledby="{gid}-title"><div class="gallery-heading"><h2 id="{gid}-title">{title}</h2><p>{instruction}</p></div><div class="gallery-controls" hidden><button type="button" data-prev>上一张</button><span class="gallery-count" role="status" aria-live="polite"></span><button type="button" data-next>{'下一段' if sequence and w['form']=='手卷' else '下一张'}</button><button type="button" data-show-all aria-pressed="false">展开全部</button></div><div class="gallery-stage">{figures}</div><div class="gallery-thumbs" aria-label="选择照片" hidden></div></section>'''

def card(w,prefix=''):
    p=asset(w,w['cover'])
    detail=w.get('cover_kind') or ('局部' if w['form']=='手卷' or w['cover'] in [375,443] else '全貌')
    return f'''<article class="painting-card" data-unit="{w['unit']}"><a class="painting-thumb" href="{prefix}{w['id']}/">{picture(p,prefix+'images/',w['title']+' · '+p['caption'])}<span class="cover-kind">{detail}</span></a><div class="painting-card-body"><p class="painting-artist">{e(w['artist'])} · {e(w['form'])}</p><h3><a href="{prefix}{w['id']}/">{e(w['title'])}</a></h3><p>{e(w['date'])}</p><p class="card-museum">{e(w['museum'])}</p><a class="text-link" href="{prefix}{w['id']}/">{'逐段看画' if w['form']=='手卷' else '查看作品'} →</a></div></article>'''

unit_names={'scrolls':'宋元书画','murals':'寺院壁画','buddhist-scrolls':'佛教卷轴画','dunhuang':'敦煌绘画'}
for index,w in enumerate(works):
    target=PAGE/w['id'];target.mkdir(exist_ok=True)
    rows=''.join(f'<div><dt>{label}</dt><dd>{e(value)}</dd></div>' for label,value in [('作者',w['artist']),('年代',w['date']),('形制',w['form']),('材质',w['medium']),('馆藏编号',w['accession'])])
    paragraphs=''.join(f'<p>{e(p)}</p>' for p in w['notes'])
    note=f'<p class="record-note">{e(w["caveat"])}</p>' if w['caveat'] else ''
    extras=gallery(w,w['extras'],'全景、细节与题跋','extras') if w['extras'] else ''
    related_ids=w.get('related',[])
    if w['id'] in ['qiao-zhongchang-red-cliff','li-song-red-cliff']:
        related_ids=['li-song-red-cliff' if w['id']=='qiao-zhongchang-red-cliff' else 'qiao-zhongchang-red-cliff']
    related=''
    for rid in related_ids:
        ow=next(o for o in works if o['id']==rid)
        related+=f'<p class="featured-note"><a href="../{rid}/">一起看：《{e(ow["title"])}》 →</a></p>'
    peers=[o for o in works if o['unit']==w['unit']];i=peers.index(w)
    previous=peers[i-1] if i else None;following=peers[i+1] if i+1<len(peers) else None
    prevlink=f'<a href="../{previous["id"]}/">← {e(previous["title"])}</a>' if previous else '<span></span>'
    nextlink=f'<a href="../{following["id"]}/">{e(following["title"])} →</a>' if following else '<span></span>'
    return_url=f"../#{w['period']}";return_name='中国书画'
    if w['unit']=='dunhuang':return_url='../../dunhuang-painting/';return_name='敦煌绘画'
    elif w['unit']!='scrolls':return_url='../../buddhist-painting/#'+w['unit'];return_name='佛教绘画'
    source=f'<br><a href="{e(w["url"])}" target="_blank" rel="noopener noreferrer">馆方资料 ↗</a>' if w['url'] else ''
    content=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../../">博物馆札记</a><span>/</span><a href="{return_url}">{return_name}</a><span>/</span><a href="../#{w['period']}">{names[w['period']]}</a></nav>
<header class="work-heading wrap"><p class="eyebrow">{names[w['period']]} / {e(w['form'])}</p><h1>{e(w['title'])}</h1><p class="work-byline">{e(w['artist'])} · {e(w['museum'])}</p></header>
{gallery(w,w['sequence'],'看画','painting',True)}
<section class="work-notes wrap"><div><h2>作品札记</h2>{paragraphs}{note}{related}</div><aside><dl>{rows}</dl><p class="source">基本信息据现场展签整理。{source}</p><p class="source">照片 © Merton</p><p class="source"><a href="../#{w['period']}">在中国书画年代目录中查看 →</a></p></aside></section>
{extras}<nav class="work-pagination wrap" aria-label="前后作品">{prevlink}<a href="{return_url}">返回{return_name}</a>{nextlink}</nav>'''
    (target/'index.html').write_text(frame(w['title'],content,1,f'{w["artist"]}《{w["title"]}》，{w["date"]}。Merton在{w["museum"]}拍摄的作品照片与札记。'))

nav=''.join(f'<a href="#{key}">{name}<span>{sum(w["period"]==key for w in works)}</span></a>' for key,name,_ in periods)
sections=''
for key,name,description in periods:
    cards=''.join(card(w) for w in works if w['period']==key)
    sections+=f'<section class="period-section wrap" id="{key}" aria-labelledby="heading-{key}"><div class="period-heading"><h2 id="heading-{key}">{name}</h2><p>{description}</p></div><div class="paintings-grid">{cards}</div></section>'
hero_work=next(w for w in works if w['id']==data['hero']['work']);hero=asset(hero_work,data['hero']['number'])
featured_ids=['qiao-zhongchang-red-cliff','xu-daoning-fishermen','jiang-shen-verdant','taigu-yimin-traveling','xia-gui-twelve-views','luo-river-nymph','gong-kai-zhongshan']
featured=''.join(f'<a href="{wid}/">{next(w["title"] for w in works if w["id"]==wid)} ↗</a>' for wid in featured_ids)
counts={unit:sum(w['unit']==unit for w in works) for unit in unit_names}
content=f'''<section class="painting-intro wrap"><p class="eyebrow">CHINESE PAINTING &amp; CALLIGRAPHY</p><h1>中国书画</h1><p class="subtitle">从看过的宋元书画，慢慢往前后整理。</p><div class="painting-intro-meta"><span>{len(works)} 件作品</span><span>{len(set(w['museum'] for w in works))} 家博物馆</span><span>摄影 / Merton</span></div>
<div class="painting-lead"><figure class="painting-banner"><a href="{hero_work['id']}/">{picture(hero,'images/','传李成《晴峦萧寺图》',True)}</a><figcaption>传 李成《晴峦萧寺图》 · 北宋</figcaption></figure><div class="lead-copy"><p class="eyebrow">从这幅开始</p><h2>晴峦萧寺图</h2><p>先看山脚的行人，再找半山的寺院。整座山的尺度，是被这些很小的人和建筑慢慢带出来的。</p><a class="text-link" href="li-cheng-temple/">看这幅画 →</a><div class="lead-second"><h3>再展开《后赤壁赋图》</h3><p>沿着苏轼的文字和人物的行踪，一段一段看。</p><a href="qiao-zhongchang-red-cliff/">进入长卷 →</a></div></div></div></section>
<section class="painting-start wrap"><h2>也可以从这些作品看起</h2><div class="featured-works">{featured}</div></section>
<section class="painting-units wrap" aria-label="专题入口"><a href="#chronology"><h3>按时代看画</h3><p>从唐、五代到宋元，以宋元书画为主。</p><span>{len(works)} 件 · 进入年代目录 ↓</span></a><a href="../dunhuang-painting/"><h3>敦煌绘画</h3><p>供养画、菩萨幡与画中的供养人。</p><span>{counts['dunhuang']} 件 · 单独成篇 →</span></a><a href="../buddhist-painting/"><h3>佛教绘画</h3><p>寺院壁画、罗汉画与敦煌绘画。</p><span>{len(works)-counts['scrolls']} 件 · 进入专题 →</span></a></section>
<nav class="period-nav wrap" id="chronology" aria-label="按时代浏览">{nav}</nav>{sections}
<aside class="editorial-note wrap"><h2>关于这些照片</h2><p>第一批是在纳尔逊－阿特金斯艺术博物馆 <a href="{data['exhibition']['url']}" target="_blank" rel="noopener noreferrer">Legendary Landscapes</a> 展览中拍摄的13件作品。后来补入弗利尔、金贝尔和吉美的绘画，以及纳尔逊的寺院壁画。</p><p>年代目录收录全部作品；敦煌与佛教绘画也有独立的专题入口。金与南宋在时间上并存，跨朝代的断代和“传”的署名都在作品页保留。</p><p>封面逐件选取较清楚、有代表性的画面，长卷封面注明局部。看画页保留原有次序、全景和题跋；反光或遮挡明显但没有替代照片的作品，仍作为现场记录留下。</p></aside>'''
(PAGE/'index.html').write_text(frame('中国书画',content,description=f'Merton在博物馆拍摄的{len(works)}件中国绘画：宋元书画、敦煌绘画与寺院壁画。'))

# Topic pages reference the same canonical work pages and images.
dunhuang=[w for w in works if w['unit']=='dunhuang']
buddhist=[w for w in works if w['unit']!='scrolls']
for slug,title,items in [('dunhuang-painting','敦煌绘画',dunhuang),('buddhist-painting','佛教绘画',buddhist)]:
    if slug=='dunhuang-painting':
        intro='把在吉美与弗利尔看到的敦煌绘画放在一起。既看佛与菩萨，也看画下方留下姓名的供养人。'
        groups=[('votive','供养画',[w for w in items if '幡' not in w['form']]),('banners','幡画',[w for w in items if '幡' in w['form']])]
        note='这些作品画在绢或麻布上，并非从洞窟墙面切下来的壁画。吉美这组的展签注明来自莫高窟、属伯希和1906—1909年考察带回的藏品；弗利尔的地藏像另见其作品资料。'
    else:
        intro='从寺院墙面上的佛与菩萨，到可以悬挂的罗汉画与敦煌幡画。先按作品原来的形制和环境放在一起，再慢慢补。'
        groups=[('murals','寺院壁画',[w for w in items if w['unit']=='murals']),('buddhist-scrolls','佛教卷轴画',[w for w in items if w['unit']=='buddhist-scrolls']),('dunhuang','敦煌绘画',dunhuang)]
        note='宋元佛画暂不按朝代拆成很小的栏目。罗汉画放在“佛教卷轴画”，广胜寺与慈胜寺等壁画放在“寺院壁画”；敦煌自成一个单元。每件作品仍可从中国书画的年代目录找到。'
    links=''.join(f'<a href="#{gid}">{gtitle}<span>{len(gitems)}</span></a>' for gid,gtitle,gitems in groups)
    body=f'<nav class="breadcrumbs wrap"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>{title}</span></nav><header class="painting-intro wrap"><p class="eyebrow">CHINESE BUDDHIST ART / PAINTING</p><h1>{title}</h1><p class="subtitle">{intro}</p><p class="intro">{len(items)} 件作品 · 摄影 / Merton</p><p class="topic-return"><a href="../chinese-painting/">中国书画年代目录 →</a>　<a href="../buddhist-painting/">佛教绘画 →</a>　<a href="../dunhuang-painting/">敦煌绘画 →</a></p></header><nav class="period-nav wrap">{links}</nav>'
    for gid,gtitle,gitems in groups:
        body+=f'<section class="period-section wrap" id="{gid}"><div class="period-heading"><h2>{gtitle}</h2></div><div class="paintings-grid">'+''.join(card(w,'../chinese-painting/') for w in gitems)+'</div></section>'
    body+=f'<aside class="editorial-note wrap"><h2>这一单元</h2><p>{note}</p></aside>'
    target=ROOT/'museum-notes'/slug;target.mkdir(exist_ok=True)
    (target/'index.html').write_text(frame(title,body,description=intro,sibling=True))
print(f'Generated Chinese painting index, {len(works)} work pages and 2 Buddhist painting topic pages.')
