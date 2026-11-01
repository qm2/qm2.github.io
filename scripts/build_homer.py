"""Build the Homer notebook. All artwork images derive from the user's 215-photo handoff."""
from pathlib import Path
from html import escape as e
import json, math, re
from PIL import Image, ImageOps
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/homer'
LIGHTBOX='''<dialog id="art-lightbox" aria-labelledby="lightbox-caption"><div class="lightbox-tools"><button type="button" id="photo-prev" aria-label="上一张照片">←</button><button type="button" id="photo-next" aria-label="下一张照片">→</button><button type="button" id="zoom-toggle" aria-pressed="false">放大细看 ＋</button><a id="original-photo" href="#" target="_blank" rel="noopener">原图 ↗</a><button type="button" id="photo-close" aria-label="关闭大图">关闭 ×</button></div><div id="photo-stage" tabindex="0" aria-label="照片区域；放大后可滚动查看"><img id="large-photo" alt=""></div><p id="lightbox-caption"></p></dialog>'''

def build():
    read=lambda name:json.loads((BASE/'data'/f'{name}.json').read_text())
    works=read('works');photos=read('photos');pby={p['id']:p for p in photos};by={w['photo']:w for w in works};edit=read('editorial');sections=read('sections');regions=read('map');land=json.loads((BASE/'data/ne_110m_land.geojson').read_text())
    selected=[w for w in works if w['presentation']!='archive']
    assert len(works)==67 and len(photos)==215 and len(selected)==30
    used={w['display_photo'] for w in works}|{n for w in works for n in w['detail_photos']}|{p['photo'] for p in edit['gallery']+edit['materials']}
    (BASE/'images').mkdir(exist_ok=True)
    manifest={}
    for n in sorted(used):
        p=pby[n];src=BASE/p['original'];im=ImageOps.exif_transpose(Image.open(src));width,height=im.size;variants=[]
        for limit in [480,960,1600]:
            target=BASE/'images'/f'{n:03d}-{limit}.webp';iw=min(limit,width);ih=round(height*iw/width)
            if not target.exists() or target.stat().st_mtime<src.stat().st_mtime:
                im.resize((iw,ih),Image.Resampling.LANCZOS).convert('RGB').save(target,'WEBP',quality=87,method=6)
            variants.append({'path':str(target.relative_to(BASE)),'width':iw,'height':ih})
        manifest[str(n)]={'width':width,'height':height,'variants':variants,'original':p['original']}
    (BASE/'data/derivatives.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    def date(w):return w['year'].replace('c. ','约').replace('19th century','19世纪')
    def image(n,caption,prefix='',high=False,small=False):
        m=manifest[str(n)];vs=m['variants'];src=vs[0 if small else 1]['path'];ss=', '.join(f'{prefix}{v["path"]} {v["width"]}w' for v in {v['width']:v for v in vs}.values())
        return f'<img src="{prefix}{src}" srcset="{ss}" sizes="{("(max-width: 650px) 42vw, 260px" if small else "(max-width: 650px) calc(100vw - 40px), (max-width: 1100px) 88vw, 1000px")}" width="{m["width"]}" height="{m["height"]}" alt="{e(caption)}" {"fetchpriority=high" if high else "loading=lazy"} decoding="async">'
    def figure(n,caption,prefix='',high=False,small=False,cls=''):
        m=manifest[str(n)];ratio=m['width']/m['height']
        return f'<figure class="hm-figure {cls}" style="--ratio:{ratio:.5f}"><a data-photo href="{prefix}{m["original"]}" data-caption="{e(caption)}">{image(n,caption,prefix,high,small)}</a><figcaption>{e(caption)}</figcaption></figure>'
    def caption(w):return f'{w["title_cn"]} · {date(w)} · {w["material_cn"]} · {w["collection"]}'+(f'，{w["accession"]}' if w['accession'] else '')+' · Merton摄'
    def sources(w,prefix=''):
        return f'<p class="hm-source">作品信息与文中展签说明据<a href="{prefix}{pby[w["label"]]["original"]}" target="_blank" rel="noopener">现场展签 ↗</a>。</p>'
    def details(w,prefix=''):
        return '<details class="hm-details"><summary>走近看局部</summary><div class="hm-details-grid">'+''.join(figure(n,w['title_cn']+' · '+detail_caption.get(n,'局部'),prefix,small=True) for n in w['detail_photos'])+'</div></details>' if w['detail_photos'] else ''
    detail_caption={179:'局部：舟中人、船身与倒影',181:'局部：跃鱼与暗水',182:'局部：鱼头与鳞纹',183:'局部：叶片与水面色痕',185:'局部：林中人与倒木枝杈',187:'局部：浪顶与泡沫',189:'局部：跃鱼、钓者与鱼线',191:'局部：船间的人物',193:'局部：向导与独木舟',195:'局部：提篮女子与海浪',197:'局部：舟中人和跃鱼',199:'局部：潜水者的肩背与海绵',202:'局部：小舟、钓线与树影',204:'局部：急流的浅色浪沫与暗水',207:'局部：岸边人物、漂木与海浪',209:'局部：两名男孩与小艇',211:'局部：草地上的两个男孩',213:'局部：崖边的一家人',215:'局部：沙丘上的两名女子'}
    def mini(w,prefix='',anchor=False):
        href=prefix+(('#work-'+w['slug']) if anchor and w in selected else w['slug']+'/')
        return f'<a class="hm-mini" href="{href}">{image(w["display_photo"],w["title_cn"]+" · 现场整幅照片",prefix,small=True)}<span>{e(w["title_cn"])}<small>{date(w)} · {e(w["title"])}</small></span></a>'
    def shell(title,body,depth=0):
        pre='../'*depth;note='../'*(depth+1)
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="在休斯顿重看霍默：从田园与海岸走进山林、独木舟和水的世界。现场摄影与观看札记。"><link rel="stylesheet" href="{note}museum.css"><link rel="stylesheet" href="{note}caravaggio/caravaggio.css"><link rel="stylesheet" href="{pre}homer.css"><script src="{note}caravaggio/caravaggio.js" defer></script><script src="{pre}homer.js" defer></script></head><body class="hm-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{note}">Merton</a><nav aria-label="主导航"><a href="{pre or './'}">霍默专题</a><a href="{pre or './'}#journeys">地理索引</a><a href="{pre or './'}#catalogue">观展目录</a></nav></header><main id="main" class="wrap">{body}</main><footer class="site-footer wrap"><a href="{note}">← 博物馆札记</a><span>现场摄影与札记 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
    def comparison(g):
        return f'<section class="compare-group hm-compare" id="compare-{g["id"]}"><p class="eyebrow">SIDE BY SIDE</p><h3>{e(g["title"])}</h3><p class="hm-prose">{e(g["text"])}</p><div class="hm-pair">'+''.join(figure(by[n]['display_photo'],caption(by[n])) for n in g['works'])+'</div><p class="hm-source">整幅现场照片；未按原作尺寸等比例排列。'+ ' · '.join(f'<a href="{by[n]["slug"]}/">{e(by[n]["title_cn"])}札记 →</a>' for n in g['works'])+'</p></section>'
    intro=f'<nav class="breadcrumbs" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><span>美国绘画 · 霍默</span></nav><header class="hm-heading"><p class="eyebrow">WINSLOW HOMER / OF LIGHT AND AIR</p><h1>{edit["title"]}<span>{edit["subtitle"]}</span></h1></header>'+figure(by[11]['display_photo'],caption(by[11]),high=True,cls='hm-hero')+'<div class="hm-intro">'+''.join(f'<p>{e(p)}</p>' for p in edit['intro'])+f'<p class="hm-source">{e(edit["exhibition"])}<br>休斯顿美术馆（MFAH） · {edit["dates"]}<br>由波士顿美术馆（MFA Boston）组织，休斯顿展出。<a href="#source-mfah">展览资料 [1]</a></p></div>'
    # Static geographic SVG, enhanced by local JS. Natural Earth land only; no external tile requests.
    def svg_map(view):
        bounds=(-90,10,12,65) if view=='atlantic' else (-79,-64,39,52)
        xmin,xmax,ymin,ymax=bounds
        def xy(lon,lat):return ((lon-xmin)/(xmax-xmin)*900,(ymax-lat)/(ymax-ymin)*500)
        paths=[]
        for feature in land['features']:
            geom=feature['geometry'];polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
            for rings in polys:
                pts=rings[0]
                if max(p[0] for p in pts)<xmin or min(p[0] for p in pts)>xmax or max(p[1] for p in pts)<ymin or min(p[1] for p in pts)>ymax:continue
                paths.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{xy(*p)[0]:.1f},{xy(*p)[1]:.1f}' for i,p in enumerate(pts))+' Z"/>')
        markers=[];callouts={0:(95,155),1:(238,100),2:(270,185),3:(230,250),4:(787,60),5:(200,445),6:(205,365),7:(310,300),8:(55,330)}
        for i,r in enumerate(regions):
            x,y=xy(r['lon'],r['lat'])
            if not 0<x<900 or not 0<y<500:continue
            lx,ly=callouts[i] if view=='atlantic' else (x+(-45 if i==0 else 35),y+(-25 if i in [0,1,2] else 35))
            markers.append(f'<a href="#region-{r["id"]}" data-region="{r["id"]}" aria-label="{i+1} {e(r["name_cn"])}：查看作品"><line x1="{x:.1f}" y1="{y:.1f}" x2="{lx}" y2="{ly}"/><circle class="hm-anchor" cx="{x:.1f}" cy="{y:.1f}" r="3"/><circle class="hm-pin" cx="{lx}" cy="{ly}" r="18"/><text x="{lx}" y="{ly+5}" text-anchor="middle">{i+1}</text></a>')
        label='大西洋' if view=='atlantic' else '北美东北部'
        return f'<div class="hm-map-panel" tabindex="0" aria-label="地图区域，可左右滚动" data-map="{view}" {"hidden" if view!="atlantic" else ""}><svg viewBox="0 0 900 500" role="group" aria-label="{label}区域索引；编号对应下方地区列表"><defs><clipPath id="clip-{view}"><rect width="900" height="500"/></clipPath></defs><g class="hm-land" clip-path="url(#clip-{view})">'+''.join(paths)+'</g><text class="hm-ocean" x="600" y="440">大西洋</text><g class="hm-markers">'+''.join(markers)+'</g></svg></div>'
    map_html='<section class="hm-section" id="journeys"><p class="eyebrow">PLACES &amp; PICTURES</p><h2>霍默笔下的自然与旅程</h2><p class="hm-prose">从北方的森林与湖泊，到大西洋两岸，再到更南方的光。点选地图编号或地区名称，回到画里的舟、水与人。</p><div class="hm-map-tools" hidden><button type="button" data-view="atlantic" aria-pressed="true">大西洋全览</button><button type="button" data-view="northeast" aria-pressed="false">北美东北部放大</button><button type="button" id="hm-map-expand" aria-pressed="false">放大地图</button></div>'+svg_map('atlantic')+svg_map('northeast')+'<p class="hm-source">地点为区域示意，非作品的精确作画坐标，也不是参观地。底图：<a href="#source-natural-earth">Natural Earth</a>；数字标记以引线连接区域锚点。</p><div class="hm-regions">'
    for i,r in enumerate(regions):
        map_html+=f'<details id="region-{r["id"]}" class="hm-region"><summary>{i+1:02d} · {r["name_cn"]}<small>{e(r["name"])}</small></summary><p>{e(r["text"])}</p><div class="hm-region-works">'+''.join(mini(by[n]) for n in r['works'])+f'</div><a class="text-link" href="#{r["section"]}">进入相关章节 ↓</a></details>'
    map_html+='</div></section>'
    nav='<nav class="hm-chapters" aria-label="七章阅读">'+''.join(f'<a href="#{s["id"]}"><small>{i+1:02d}</small>{s["title"]}</a>' for i,s in enumerate(sections))+'</nav>'
    chapters=''
    for i,s in enumerate(sections):
        ordered=sorted([w for w in selected if w['section']==s['id']],key=lambda w:(0 if w['photo'] in [11,74] else 1,works.index(w)))
        chapters+=f'<section class="hm-section hm-chapter" id="{s["id"]}"><header><p class="eyebrow">{i+1:02d} / {e(s["en"].upper())}</p><h2>{e(s["title"])}</h2><p class="hm-prose">{e(s["intro"])}</p></header>'
        if s['id']=='origins':chapters+=figure(edit['gallery'][0]['photo'],edit['gallery'][0]['caption'],cls='hm-gallery-view')
        if s['id']=='woods':chapters+=figure(edit['gallery'][2]['photo'],edit['gallery'][2]['caption'],cls='hm-gallery-view')
        chapters+='<div class="hm-works">'
        for w in ordered:
            deep=w['presentation']=='deep-dive'
            chapters+=f'<article class="hm-work {"hm-deep" if deep else "hm-card"}" id="work-{w["slug"]}" data-presentation="{w["presentation"]}"><header><p class="hm-medium">{e(w["material_cn"])}</p><h3><a href="{w["slug"]}/">{e(w["title_cn"])}</a></h3><p class="hm-original">{e(w["title"])} · {date(w)}</p></header>'+figure(w['display_photo'],caption(w),small=not deep)+'<div class="hm-prose">'+''.join(f'<p>{e(t)}</p>' for t in w['paragraphs'])+'</div>'+sources(w)+(details(w) if deep else '')+f'<a class="hm-more" href="{w["slug"]}/">作品资料与照片 →</a></article>'
        chapters+='</div>'
        if s['id']=='woods':chapters+=comparison(edit['comparisons'][0])
        if s['id']=='finale':chapters+=comparison(edit['comparisons'][1])+comparison(edit['comparisons'][2])
        chapters+='</section>'
    catalogue='<section class="hm-section" id="catalogue"><details class="hm-catalogue"><summary><h2>这次展览的观展目录</h2><span>67条作品／成组展品记录 · 展开浏览</span></summary><p>绘画、版画与素描一起留在这里。同框的两件作品按一组记录；展签、局部与重复照片不另算作品。</p><div class="hm-filters" hidden><label>搜索<input id="hm-search" type="search" placeholder="中文／英文题名、收藏、作者…"></label><label>媒介<select id="hm-medium"><option value="all">全部</option><option value="watercolor">水彩／水粉</option><option value="oil">油画</option><option value="drawing">素描／混合材料</option><option value="print">版画</option></select></label><label>年代<select id="hm-era"><option value="all">全部</option>'+''.join(f'<option value="{y}">{y}年代</option>' for y in range(1840,1910,10))+'</select></label><button id="hm-reset" type="button">清除筛选</button></div><p id="hm-count" role="status" aria-live="polite">67条记录</p><div class="hm-archive">'
    for w in works:
        year=int(re.search(r'\d{4}',w['year'])[0]);search=' '.join([w['title_cn'],w['title'],w['collection'],w['artist'],w['accession'],date(w),w['material_cn']])
        catalogue+=f'<article class="hm-archive-row" data-search="{e(search.lower())}" data-medium="{w["media_type"]}" data-era="{year//10*10}">{mini(w)}<p>{date(w)} · {e(w["material_cn"])}<br>{e(w["collection"])}'+(f'<br>{e(w["artist"])}' if w['photo'] in [97,99,107] else '')+'</p></article>'
    catalogue+='</div><p id="hm-empty" hidden>没有符合条件的记录。试试其他关键词，或清除筛选。</p></details></section>'
    materials='<section class="hm-section" id="materials"><p class="eyebrow">PAPER, WATER &amp; COLOUR</p><h2>霍默如何用水彩</h2><p class="hm-prose">'+e(edit['material_text'])+'</p><div class="hm-pair">'+''.join(figure(p['photo'],p['caption'],small=True) for p in edit['materials'])+'</div><p class="hm-source">材料信息据现场说明：'+ ' · '.join(f'<a href="{pby[n]["original"]}">水彩{t}展签 ↗</a>' for n,t in [(117,'盒'),(119,'色样')])+'</p></section>'
    end=figure(edit['gallery'][1]['photo'],edit['gallery'][1]['caption'],cls='hm-gallery-view')+'<section class="hm-section hm-sources" id="sources"><h2>资料与这份观看记录</h2><p>作品与现场摄影由作者拍摄记录；作品信息据现场展签及馆方说明整理。画面细读与个人感受是这份札记的阅读，文中“展签指出”等表述另标明依据。</p><p>中文题名作阅读译名，英文题名保留展签写法。展览由波士顿美术馆组织，休斯顿展场还包括本馆与私人收藏借展；各件收藏归属分别列在图注与作品页。</p><ol>'+''.join(f'<li id="source-{s["id"]}"><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["title"])} ↗</a></li>' for s in edit['sources'])+'</ol><p class="hm-source">2026年11月整理 · 215张现场照片归为67条作品／成组记录，正文选取30件。本站未使用馆方作品图片或图录复制图。</p></section>'
    (BASE/'index.html').write_text(shell(edit['title']+'｜'+edit['subtitle'],intro+map_html+nav+chapters+materials+catalogue+end))
    for w in works:
        fields=[('作者／制作者',w['artist']),('年代',date(w)),('媒介',w['material_cn']),('展签原文',w['medium']),('收藏',w['collection']),('编号',w['accession'] or '展签未列'),('观看地点','休斯顿美术馆 · Of Light and Air')]
        if w['credit']:fields.append(('入藏来源',w['credit']))
        body=f'<nav class="breadcrumbs" aria-label="当前位置"><a href="../../">博物馆札记</a><span>/</span><a href="../">霍默</a><span>/</span><span>{e(w["title_cn"])}</span></nav><header class="hm-heading hm-work-heading"><p class="eyebrow">WINSLOW HOMER / LOOK CLOSER</p><h1>{e(w["title_cn"])}</h1><p class="hm-original">{e(w["title"])}</p></header>'+figure(w['display_photo'],caption(w),'../',high=True)+'<div class="hm-work-reading"><dl class="hm-facts">'+''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k,v in fields)+'</dl>'
        if w['paragraphs']:body+='<section class="hm-prose"><h2>在画前</h2>'+''.join(f'<p>{e(t)}</p>' for t in w['paragraphs'])+'</section>'
        if w.get('record_note'):body+='<p class="hm-prose">'+e(w['record_note'])+'</p>'
        body+=sources(w,'../')+details(w,'../')+'</div>'
        siblings=[a for a in selected if a['section']==w['section'] and a!=w][:3]
        body+='<section class="hm-section"><h2>继续看这一章</h2><div class="hm-region-works">'+''.join(mini(a,'../') for a in siblings)+f'</div><a class="text-link" href="../#{w["section"]}">返回章节 →</a> · <a href="../#catalogue">完整观展目录 →</a></section>'
        dest=BASE/w['slug'];dest.mkdir(exist_ok=True);(dest/'index.html').write_text(shell(w['title_cn']+' · 霍默',body,1))
    print(f'Built Homer: {len(works)} records, {len(selected)} selections, {len(used)} responsive photographs, 9 map regions, 3 comparisons.')

if __name__=='__main__':build()
