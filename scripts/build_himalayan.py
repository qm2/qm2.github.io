"""Build Himalayan Art from stable public records. No network, npm or handoff required."""
from pathlib import Path
from html import escape as e
import json, re, hashlib
from datetime import date
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/himalayan-art'

def build(base=BASE, integrate=True):
    read=lambda n:json.loads((base/'data'/f'{n}.json').read_text())
    dump=lambda n,d:(base/'data'/f'{n}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    works=read('works'); by={w['work_id']:w for w in works}; units=read('reading_units'); ub={u['unit_id']:u for u in units}
    chapters=read('chapters'); places=read('places'); pb={p['place_id']:p for p in places}; museums=read('museums'); mb={m['museum_id']:m for m in museums}
    sources={s['source_id']:s for s in read('sources')}; photos=read('photos'); caps=read('photo_captions')
    introduction=read('introduction'); visits=read('visits'); updates=read('updates'); history=read('history')
    history_nodes=[n for track in history['tracks'] for n in track['nodes']]
    visit_by={v['visit_id']:v for v in visits}
    assert len(visit_by)==len(visits)
    for v in visits:
        assert v['work_id'] in by
        if v.get('visited_on'): date.fromisoformat(v['visited_on'])
        assert set(v.get('photo_ids',[])) <= set(by[v['work_id']]['art_photos']+by[v['work_id']]['detail_photos'])
    assert len({u['update_id'] for u in updates})==len(updates)
    for update in updates:
        assert update['work_id'] in by and update['kind'] in {'new','research','revisit'}
        date.fromisoformat(update['published_on'])
        assert all(s in sources for s in update.get('source_ids',[]))
        if update.get('visit_id'):
            assert visit_by[update['visit_id']]['work_id']==update['work_id']
    recent=sorted([u for u in updates if u.get('public',False)],key=lambda u:u['published_on'],reverse=True)[:3]
    # Keep HTML, navigation and scoped assets on the same revision after publishing.
    revision=hashlib.sha256(b''.join(p.read_bytes() for p in [base/'himalayan.js',base/'himalayan.css']+sorted(p for p in (base/'data').glob('*.json') if p.stem not in {'navigation','derivatives'}))).hexdigest()[:12]
    assert len(by)==len(works) and all(w['public'] for w in works)
    def derive(p):
        n=p['photo_id']; src=base/'images/originals'/f'{n}.jpg'
        im=ImageOps.exif_transpose(Image.open(src)).convert('RGB'); variants=[]
        for size in [400,900,1600]:
            iw=min(size,im.width);ih=round(im.height*iw/im.width);dest=base/'images'/f'{n}-{size}.webp'
            if not dest.exists():im.resize((iw,ih),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=86,method=5)
            variants.append({'path':f'images/{n}-{size}.webp','width':iw,'height':ih})
        return n,{'width':im.width,'height':im.height,'variants':variants,'original':f'images/originals/{n}.jpg','sha256':p['sha256']}
    with ThreadPoolExecutor(max_workers=6) as pool: manifest=dict(pool.map(derive,photos))
    dump('derivatives',manifest)
    def collection(w):
        c=w['collection_label'];mid=w.get('display_museum_id')
        if mid and mid!=w.get('collection_museum_id'):c+=' · 在'+mb[mid]['label_zh']+'展出'
        return c
    def caption(w):return w['title_zh']+' · '+w['date_label']+'｜'+collection(w)+((' · '+w['accession']) if w.get('accession') else '')
    def img(n,alt,pre='',high=False,small=False):
        m=manifest[n];vs=m['variants'];ss=', '.join(pre+v['path']+' '+str(v['width'])+'w' for v in {v['width']:v for v in vs}.values())
        sz='(max-width: 650px) 42vw, 330px' if small else '(max-width: 650px) calc(100vw - 40px), 680px'
        return f'<img src="{pre}{vs[0 if small else 1]["path"]}" srcset="{ss}" sizes="{sz}" width="{m["width"]}" height="{m["height"]}" alt="{e(alt)}" decoding="async" '+('fetchpriority="high"' if high else 'loading="lazy"')+'>'
    def fig(n,cap,pre='',high=False):
        m=manifest[n]
        return f'<figure class="ha-figure" style="--ratio:{m["width"]/m["height"]:.5f};--native:{m["width"]}px"><a data-photo href="{pre}{m["original"]}" data-caption="{e(cap)}">{img(n,cap,pre,high)}</a><figcaption>{e(cap)} · Merton摄</figcaption></figure>'
    def refmark(ids):return ' '.join(f'<a class="ha-ref" href="#source-{k}" aria-label="资料 {k[1:]}">[{k[1:]}]</a>' for k in dict.fromkeys(ids) if k in sources)
    def refs(ids):
        out='<section class="ha-sources" id="sources"><h2>资料与来源</h2><p class="ha-note">作品基本资料据现场展签及下列馆方记录整理；文字中的观看描述基于这里的现场照片。</p><ul>'
        for k in dict.fromkeys(ids):
            if k not in sources:continue
            s=sources[k];out+=f'<li id="source-{k}"><span>[{k[1:]}]</span> <a href="{e(s["url"])}">{e(s["title"])} ↗</a></li>'
        return out+'</ul></section>'
    def shell(title,body,depth=0,photo='h1677'):
        pre='../'*depth; note='../'*(depth+1)
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="从山口与河谷，到金属、木与色彩：以亲见作品阅读喜马拉雅艺术中的供养、传承与制作。"><meta property="og:image" content="https://qm2.github.io/museum-notes/himalayan-art/images/{photo}-900.webp"><link rel="stylesheet" href="{note}museum.css"><link rel="stylesheet" href="{note}caravaggio/caravaggio.css"><link rel="stylesheet" href="{pre}himalayan.css?v={revision}"><script defer src="{note}caravaggio/caravaggio.js"></script><script defer src="{pre}himalayan.js?v={revision}"></script></head><body class="ha-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{note}">Merton</a><nav aria-label="主导航"><a href="{pre or './'}">喜马拉雅艺术</a><a href="{pre}#places">地域导览</a><a href="{pre}#catalogue">亲见目录</a></nav></header><main id="main" class="wrap">{body}</main><footer class="site-footer wrap"><a href="{note}">← 博物馆札记</a><span>现场摄影与札记 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
    def facts(w):
        rel={'regional_attribution':'地域归属','candidate_origin':'候选制作地区','style_and_candidate_origin':'风格联系／候选制作地区'}
        assoc='；'.join(pb[a['place_id']]['label_zh']+'（'+rel.get(a['relationship'],'相关地区')+'）' for a in w['map_associations'])
        fields=[('原题名',w['title_en']),('年代',w['date_label']),('材料',w.get('materials_display') or '尚未核录'),('尺寸',w.get('dimensions_display')),('收藏／展出',collection(w)),('馆藏号',w.get('accession')),('地区与传统',assoc)]
        return '<dl class="ha-facts">'+''.join(f'<dt>{k}</dt><dd>{e(v)}</dd>' for k,v in fields if v)+'</dl>'
    def links(w):return '<p class="ha-note">'+' · '.join(f'<a href="{e(a["href"])}">{e(a["label"])} →</a>' for a in w.get('site_links',[]))+'</p>' if w.get('site_links') else ''
    def notes(w):return ''.join('<p class="ha-note">'+e(t)+'</p>' for t in w['reader_notes'])
    def mini(w,pre='../'):
        return f'<a class="ha-mini" href="{pre}{w["work_id"]}/">{img(w["primary_photo"],w["image_alt_zh"],pre,small=True)}<span>{e(w["title_zh"])}<small>{e(w["date_label"])}</small></span></a>'
    def paragraphs(paras, ids):
        out=''
        for p in paras:
            ids.extend(p.get('source_ids',[]))
            out+='<p>'+e(p['text'])+' '+refmark(p.get('source_ids',[]))+'</p>'
        return out
    def research_sections(sections,ids):
        return ''.join('<section><h2>'+e(s['title'])+'</h2>'+paragraphs(s['paragraphs'],ids)+'</section>' for s in sections)
    def history_links(wid):
        nodes=[n for n in history_nodes if any(r['work_id']==wid for r in n['related'])]
        if not nodes:return ''
        return '<aside class="ha-history-return ha-prose"><p class="ha-note">历史与观看 · '+ ' · '.join(f'<a href="../history/#{n["id"]}">{e(n["period"])}：{e(n["title"])}</a>' for n in nodes)+'</p></aside>'
    def gallery(w,pre='../'):
        ns=w['detail_photos']
        if not ns:return ''
        if w['work_id']=='w1692':
            ns=[w['primary_photo']]+ns
            out='<section class="ha-detail-view"><h2>从全图到四个局部</h2><div class="ha-tabs" role="group" aria-label="曼荼罗观看区域" hidden>'
            for i,n in enumerate(ns):out+=f'<button data-plate="{i}" aria-pressed="{str(i==0).lower()}">'+(['全图','右上','左上','右下','左下'][i])+'</button>'
            out+='</div>'
            for i,n in enumerate(ns):out+=f'<div data-plate-panel="{i}">'+fig(n,caps.get(n,w['title_zh']+' · 局部'),pre,high=i==0)+'</div>'
            return out+'</section>'
        return '<section class="ha-details"><h2>靠近一点</h2><div class="ha-plates">'+''.join(fig(n,caps.get(n,w['title_zh']+' · 现场细部'),pre) for n in ns)+'</div></section>'
    def write(route,title,body,photo='h1677'):
        dest=base/route;dest.mkdir(parents=True,exist_ok=True);(dest/'index.html').write_text(shell(title,body,bool(route),photo))
    # Individual records: unchanged original photographs and compact label-based facts.
    for w in works:
        wid=w['work_id'];photo=w['primary_photo'];body=f'<nav class="breadcrumbs"><a href="../">喜马拉雅艺术</a><span>/</span><a href="../#catalogue">亲见目录</a></nav><header class="ha-heading"><p class="eyebrow">OBJECT NOTE</p><h1>{e(w["title_zh"])}</h1><p>{e(w["date_label"])}</p></header>'
        body+=gallery(w) if wid=='w1692' else fig(photo,caption(w),'../',True)
        us=[ub[u] for u in w['reading_unit_ids'] if u in ub]
        if us:
            body+='<div class="ha-prose"><p>'+e('；'.join(us[0]['look_for'][:2]))+'。</p><p>'+' · '.join(f'<a href="../{u["unit_id"]}/">细读：{e(u["title_zh"])} →</a>' for u in us)+'</p></div>'
        body+=notes(w)+(gallery(w) if wid!='w1692' else '')+f'<section class="ha-section ha-prose"><h2>作品资料</h2>{facts(w)}{links(w)}<p><a href="../?work={wid}#places">在地图中看相关地区 →</a></p></section>'
        # Independent labels are explicitly private in the supplied photo manifest.
        if w['label_photos']:body+='<details class="ha-prose"><summary>现场资料</summary><p>基本资料依据现场展签整理。'+e(w['title_en'])+(('；馆藏号 '+w['accession']) if w.get('accession') else '')+'。</p>'+notes(w)+'</details>'
        others=[n for n in w['art_photos'] if n!=photo]
        if others:body+='<details class="ha-alternates"><summary>其他现场视角</summary><div class="ha-plates">'+''.join(fig(n,caps.get(n,w['title_zh']+' · 另一张现场照片'),'../') for n in others)+'</div></details>'
        observations=[v for v in visits if v['work_id']==wid and v.get('public',False) and v.get('observation')]
        if observations:
            body+='<section class="ha-prose ha-visit-notes" id="visit-notes"><h2>重访札记</h2>'
            for v in observations:
                body+=f'<article id="visit-{e(v["visit_id"])}">'
                if v.get('visited_on'):body+=f'<p class="ha-note"><time datetime="{v["visited_on"]}">{v["visited_on"]}</time></p>'
                body+='<p>'+e(v['observation'])+'</p></article>'
            body+='</section>'
        body+=history_links(wid)+refs(w['source_ids']);write(wid,w['title_zh'],body,photo)
    # Reading units: the photograph leads, comparisons remain optional.
    for index,u in enumerate(units):
        w=by[u['focus_work_id']];wid=w['work_id'];ids=list(u['source_ids'])+w['source_ids']
        body=f'<nav class="breadcrumbs"><a href="../">喜马拉雅艺术</a><span>/</span><a href="../#{u["chapter_id"]}">{e(next(c["title_zh"] for c in chapters if c["chapter_id"]==u["chapter_id"]))}</a></nav><header class="ha-heading"><p class="eyebrow">{u["unit_id"][1:]} / CLOSE LOOKING</p><h1>{e(u["title_zh"])}</h1></header>'
        if u.get('lead'):body+='<p class="ha-reading-lead ha-prose">'+e(u['lead'])+'</p>'
        body+=gallery(w) if wid=='w1692' else fig(w['primary_photo'],caption(w),'../',True)
        body+='<div class="ha-prose"><p>'+e(u['body_zh'])+' '+refmark(u.get('lead_source_ids',ids))+'</p>'
        if u.get('sections'):
            body+=research_sections(u['sections'],ids)
            if u.get('notes'):body+='<details class="ha-research-notes"><summary>资料注 · 记录与解释</summary>'+research_sections(u['notes'],ids)+'</details>'
        else:body+='<p class="ha-look">细看：'+e('；'.join(u['look_for']))+'。</p>'
        body+='</div>'
        if wid!='w1692':body+=gallery(w)
        body+=f'<p class="ha-prose ha-note"><a href="../{wid}/">完整作品资料 →</a> · <a href="../?work={wid}#places">看相关地区 →</a></p>'+links(w)
        if u['comparison_work_ids']:
            body+='<section class="ha-comparisons" aria-labelledby="comparison-title"><h2 id="comparison-title">放在一起看</h2>'
            if u.get('comparison_intro'):body+='<p class="ha-prose">'+e(u['comparison_intro'])+'</p>'
            body+='<div class="ha-comparison-preview compare-group">'
            for k in u['comparison_work_ids']:
                a=by[k];photo=a['primary_photo']
                body+=f'<article data-comparison="{k}"><a data-photo href="../{manifest[photo]["original"]}" data-caption="{e(caption(a))}">{img(photo,a["image_alt_zh"],"../",small=True)}</a><div><h3><a href="../{k}/">{e(a["title_zh"])}</a></h3><p class="ha-note">{e(collection(a))}</p>'
                if a.get('has_shared_frame'):body+=notes(a)
                body+='</div></article>'
            body+='</div><details class="ha-comparison"><summary>展开并看 · '+str(len(u['comparison_work_ids']))+'条相关记录</summary><p class="ha-note">图片按各自比例展示，实物不等大。</p><div class="ha-comparison-grid compare-group">'
            for k in u['comparison_work_ids']:
                a=by[k];ids+=a['source_ids'];body+='<article>'+fig(a['primary_photo'],caption(a),'../')+f'<h3><a href="../{k}/">{e(a["title_zh"])}</a></h3><p class="ha-note">{e(a.get("materials_display") or "材料尚未核录")}</p>'+notes(a)+links(a)+refmark(a['source_ids'])+'</article>'
            body+='</div></details></section>'
        body+=history_links(wid)+refs(ids)+'<nav class="ha-next" aria-label="细读翻页">'
        if index:body+=f'<a href="../{units[index-1]["unit_id"]}/">← {e(units[index-1]["title_zh"])}</a>'
        if index+1<len(units):body+=f'<a href="../{units[index+1]["unit_id"]}/">{e(units[index+1]["title_zh"])} →</a>'
        body+='</nav>';write(u['unit_id'],u['title_zh'],body,w['primary_photo'])
    # Parallel contextual histories reuse canonical works and photographs. Native
    # details keep every period usable by keyboard and without JavaScript.
    ids=[]
    body='<nav class="breadcrumbs"><a href="../">喜马拉雅艺术</a><span>/</span><span>历史与观看</span></nav><header class="ha-heading"><p class="eyebrow">HISTORY &amp; LOOKING</p><h1>'+e(history['title'])+'</h1><p>'+e(history['subtitle'])+'</p></header><div class="ha-prose"><p>'+e(history['introduction'])+'</p></div>'
    body+='<nav class="ha-history-nav" aria-label="背景导览"><a href="#tibet">西藏时间线 ↓</a><a href="#nepal">尼泊尔时间线 ↓</a><a href="../#places">回到地域地图 →</a></nav><p class="ha-note">点击时期，展开历史与相关作品。两列按大致时代并看，时间段不按比例绘制。</p><div class="ha-history-grid">'
    for track in history['tracks']:
        col=track['column']
        body+=f'<h2 id="{track["id"]}" class="ha-track-title" style="--column:{col};--row:1;--span:1">{e(track["title"])}</h2>'
        for n in track['nodes']:
            body+=f'<details class="ha-period" id="{n["id"]}" style="--column:{col};--row:{n["row"]};--span:{n["span"]}"><summary><span class="ha-period-date">{e(n["period"])}</span><span class="ha-period-title">{e(n["title"])}</span><span class="ha-keywords">'+e(' · '.join(n['keywords']))+'</span></summary><div class="ha-period-body"><p class="ha-period-intro">'+e(n['summary'])+'</p>'+paragraphs(n['paragraphs'],ids)+'<div class="ha-history-works">'
            for r in n['related']:
                w=by[r['work_id']];body+='<div>'+mini(w)+'<p class="ha-note">'+e(r['relation'])+'</p></div>'
            body+='</div></div></details>'
    body+='</div><section class="ha-prose"><h2>几个地名，几种联系</h2><p>古格是西部的历史政权；托林是寺院。俄尔是萨迦传统中的一座寺院，丹萨替则与帕木竹巴传承及家族供养相连。它们各自影响了艺术，却都不能单凭一种面容或饰件来辨认。</p>'+refmark(['S61','S62','S63'])+'</section><details class="ha-prose ha-research-notes"><summary>关于分期与资料</summary>'+paragraphs(history['framing']+history['notes'],ids)+'</details>'
    body+=refs(ids)+'<nav class="ha-next"><a href="../#chapters">← 回到六章细读</a><a href="../#catalogue">打开亲见目录 →</a></nav>'
    write('history',history['title'],body)
    # The map and every filter consume the same records. Groups are editorial geography, not work ID lists.
    groups=read('map_groups')
    member={p:g['id'] for g in groups for p in g['members']}
    for p in places:
        if p['place_id'] not in member:
            groups.append({'id':p['place_id'],'label':p['label_zh'],'members':[p['place_id']],'longitude':p['longitude'],'latitude':p['latitude'],'extension':True})
    def filter_tags(w):
        m=w.get('materials_display') or ''
        mat=next((v for ks,v in [('象牙','象牙'),('泥','泥塑'),('木','木'),('布纸绣','绘画与织物'),('铜银铁','金属'),('石','石')] if any(k in m for k in ks)),'其他／未详')
        title=w['title_zh'];tag='其他尊神与人物'
        # Match complete terms, not individual characters.
        for terms,val in [(['观音'],'观音'),(['文殊'],'文殊'),(['佛塔','经板','佛龛','法冠','仪式','转经轮','项链','佛坛'],'器物与供养'),(['唐卡','曼荼罗','肖像'],'绘画与传承'),(['金刚','亥母','明妃','空行','大黑天'],'本尊与护法'),(['湿婆','难近母','乌玛','因陀罗','苏利耶','婆苏'],'印度教诸神'),(['佛'],'佛')]:
            if any(t in title for t in terms):tag=val;break
        return mat,tag
    client=[]
    for w in works:
        mat,tag=filter_tags(w)
        client.append({**{k:w.get(k) for k in ['work_id','title_zh','title_en','date_start','date_end','date_label','region_ids','display_museum_id','collection_museum_id','map_enabled','map_associations','primary_photo','chapter_ids']},'collection':collection(w),'search':' '.join(str(w.get(k) or '') for k in ['title_zh','title_en','accession','materials_display','collection_label','museum_label']),'material':mat,'theme':tag,'reading_unit_ids':[u['unit_id'] for u in units if w['work_id'] in u['work_ids']]})
    dump('navigation',{'works':client,'units':[{'id':u['unit_id'],'title':u['title_zh'],'works':u['work_ids']} for u in units],'groups':groups,'places':places,'museums':museums})
    # Natural Earth paths are embedded: the map stays usable without network tiles.
    land=json.loads((ROOT/'museum-notes/homer/data/ne_110m_land.geojson').read_text())
    def map_svg(mode,bounds):
        xmin,xmax,ymin,ymax=bounds;ww,hh=900,490
        xy=lambda lon,lat:((lon-xmin)/(xmax-xmin)*ww,(ymax-lat)/(ymax-ymin)*hh)
        shapes=[]
        for f in land['features']:
            g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
            for rings in polys:
                pts=rings[0]
                if max(p[0] for p in pts)<xmin or min(p[0] for p in pts)>xmax or max(p[1] for p in pts)<ymin or min(p[1] for p in pts)>ymax:continue
                shapes.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{xy(*p)[0]:.1f},{xy(*p)[1]:.1f}' for i,p in enumerate(pts))+'Z"/>')
        pins=[]
        candidates=([g for g in groups if mode=='extended' or not g.get('extension')] if mode!='museums' else [m for m in museums if m.get('latitude') is not None and any(w.get('display_museum_id')==m['museum_id'] for w in works)])
        occupied=[];label_boxes=[]
        for i,d in enumerate(candidates):
            key=d['museum_id'] if mode=='museums' else d['id'];label=d['label_zh'] if mode=='museums' else d['label'];x,y=xy(d['longitude'],d['latitude']);lx,ly=x,y
            # Automatic callouts, including newly added institutions. Full labels live in the equivalent list.
            for j in range(90):
                if all(abs(lx-ox)>36 or abs(ly-oy)>34 for ox,oy in occupied):break
                import math
                angle=j*2.4;radius=12+j*1.5;lx=max(22,min(878,x+radius*math.cos(angle)));ly=max(24,min(466,y+radius*math.sin(angle)))
            occupied.append((lx,ly))
            attrs=f'data-museum="{key}"' if mode=='museums' else f'data-region="{key}"'
            text=str(i+1) if mode=='museums' else label
            if mode!='museums':
                # Reserve room for the larger mobile labels, including map edges.
                half=len(label)*15+12
                lx=max(half,min(900-half,x));ly=max(40,min(470,y))
                for j in range(120):
                    if all(abs(lx-ox)>half+oh+10 or abs(ly-oy)>44 for ox,oy,oh in label_boxes):break
                    import math
                    angle=j*2.4;radius=18+j*2
                    lx=max(half,min(900-half,x+radius*math.cos(angle)));ly=max(40,min(470,y+radius*math.sin(angle)))
                label_boxes.append((lx,ly,half))
            pins.append(f'<a href="?{("museum" if mode=="museums" else "region")}={key}#places" {attrs} aria-label="{e(label)}"><title>{e(label)}</title><line x1="{x:.1f}" y1="{y:.1f}" x2="{lx:.1f}" y2="{ly:.1f}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{6 if mode=="museums" else 18}"/><text x="{lx:.1f}" y="{ly-13:.1f}" text-anchor="middle">{e(text)}</text></a>')
        rivers=''
        if mode!='museums':
            rd=json.loads((ROOT/'museum-notes/early-buddhist-art/data/rivers.geojson').read_text())
            riverpaths=[]
            for feature in rd['features']:
                for line in feature['geometry']['coordinates']:
                    riverpaths.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{xy(*p)[0]:.1f},{xy(*p)[1]:.1f}' for i,p in enumerate(line))+'"/>')
            rivers=f'<g class="ha-rivers" clip-path="url(#clip-{mode})">'+''.join(riverpaths)+'</g>'
            rivers+='<g class="ha-river-labels">'+''.join(f'<text x="{xy(lon,lat)[0]:.1f}" y="{xy(lon,lat)[1]:.1f}">{name}</text>' for name,lon,lat in [('印度河',70.2,28.6),('恒河',82,24.6)])+'</g>'
        return f'<svg viewBox="0 0 900 490" role="group" aria-label="{("已知拍摄展馆" if mode=="museums" else "地区与传统示意图")}"><defs><clipPath id="clip-{mode}"><rect width="900" height="490"/></clipPath></defs><g class="ha-land" clip-path="url(#clip-{mode})">'+''.join(shapes)+'</g>'+rivers+'<g class="ha-pins">'+''.join(pins)+'</g></svg>'
    def select(name,label,options):return f'<label>{label}<select id="ha-{name}"><option value="">全部</option>'+''.join(f'<option value="{e(k)}">{e(v)}</option>' for k,v in options)+'</select></label>'
    maphtml='<section class="ha-section" id="places"><p class="eyebrow">REGIONS &amp; ENCOUNTERS</p><h2>山口与河谷之间</h2><p class="ha-prose">从地区与传统进入，再看看这些作品在哪些展柜中相遇。一个地名，有时指制作地域，有时指风格或寺院的联系；具体关系留在每件作品的资料里。</p><div class="ha-controls" hidden><div class="ha-tabs" role="group" aria-label="地图视角"><button data-view="regions" aria-pressed="true">地区与传统</button><button data-view="museums" aria-pressed="false">在博物馆相遇</button><button data-view="collections" aria-pressed="false">收藏机构</button></div><label><input id="ha-extended" type="checkbox"> 宫廷交流与候选地区</label></div><details class="ha-map-fold" open><summary>展开／收起地图</summary><div data-map="regions">'+map_svg('regions',(69,100,21,39))+'</div><div data-map="extended" hidden>'+map_svg('extended',(64,124,19,52))+'</div><div data-map="museums" hidden>'+map_svg('museums',(-130,9,22,55))+'</div><p class="ha-note">区域示意，不是精确制作地址或迁徙路线。底图：<a href="https://www.naturalearthdata.com/about/terms-of-use/">Natural Earth，公共领域</a>；以现代地理作参照。</p></details><div id="ha-map-lists">'
    for mode in ['regions','museums','collections']:
        maphtml+=f'<nav class="ha-place-list" data-list="{mode}" aria-label="{mode}"'+(' hidden' if mode!='regions' else '')+'>'
        if mode=='regions':
            for g in groups:maphtml+=f'<a href="?region={g["id"]}#places" data-region="{g["id"]}"'+(' data-extension hidden' if g.get('extension') else '')+f'>{e(g["label"])} <small data-count-region="{g["id"]}"></small></a>'
        else:
            mids=[m for m in museums if any(w.get('display_museum_id' if mode=='museums' else 'collection_museum_id')==m['museum_id'] for w in works)]
            for i,m in enumerate(mids):maphtml+=f'<a href="?{("museum" if mode=="museums" else "collection")}={m["museum_id"]}#places" data-{("museum" if mode=="museums" else "collection")}="{m["museum_id"]}">{str(i+1)+" · " if mode=="museums" else ""}{e(m["label_zh"])}</a>'
            maphtml+=f'<a href="?{("museum" if mode=="museums" else "collection")}=unknown#places" data-{("museum" if mode=="museums" else "collection")}="unknown">'+('展出地点未详' if mode=='museums' else '私人收藏／机构未详')+'</a>'
        maphtml+='</nav>'
    maphtml+='</div><p id="ha-map-status" class="ha-note" role="status"></p><div class="ha-filters" hidden><label>搜索<input id="ha-search" type="search" placeholder="题名、馆名、馆藏号"></label>'+select('region','大区域',[(g['id'],g.get('filter_label',g['label'])) for g in groups])+'<label id="ha-place-label" hidden>相关地区／寺院<select id="ha-place" aria-describedby="ha-map-status"><option value="">全部关联地点</option></select></label>'+select('museum','观看机构',[(m['museum_id'],m['label_zh']) for m in museums if any(w.get('display_museum_id')==m['museum_id'] for w in works)]+[('unknown','地点未详')])+select('period','年代',[('0,799','9世纪以前'),('800,1199','9—12世纪'),('1200,1499','13—15世纪'),('1500,2099','16世纪以后'),('unknown','年代未详')])+select('material','材料',[(v,v) for v in sorted({c['material'] for c in client})])+select('theme','题材',[(v,v) for v in sorted({c['theme'] for c in client})])+'<label class="ha-checkbox"><input id="ha-unknown" type="checkbox" checked> 包含年代未定</label><button type="button" data-reset>清除筛选</button></div><div id="ha-map-result" hidden><p id="ha-count" role="status"></p><div id="ha-matches" class="ha-mini-grid"></div><div id="ha-readings-result"></div><p><a href="#catalogue" id="ha-open-catalogue">查看全部筛选结果 ↓</a></p></div><noscript><p>可通过下方章节与完整目录阅读全部作品；地图中的地区名称提供地理参照。</p></noscript></section>'
    cover=by['w1677']
    body='<nav class="breadcrumbs"><a href="../">博物馆札记</a><span>/</span><span>喜马拉雅艺术</span></nav><section class="ha-cover"><div><p class="eyebrow">HIMALAYAN ART</p><h1>喜马拉雅艺术</h1><p class="ha-subtitle">山口、河谷与神圣的形体</p><p class="ha-prose">'+e(introduction['lead'])+'</p><p><a href="#chapters">开始阅读 ↓</a> · <a href="#places">打开地域导览 ↓</a>'+(' · <a href="#recent-notes">最近札记 ↓</a>' if recent else '')+'</p></div><div>'+fig('h1677',caption(cover),high=True)+'<p class="ha-note"><a href="w1677/">封面作品资料 →</a></p></div></section>'
    epigraph=introduction['epigraph']
    body+='<section class="ha-preface ha-prose" id="preface" aria-labelledby="preface-title"><h2 id="preface-title">缘起</h2><blockquote class="ha-epigraph"><p>'+'<br>'.join(e(line) for line in epigraph['lines'])+'</p><cite><a href="'+e(epigraph['source_url'])+'" title="'+e(epigraph['source_title'])+'">'+e(epigraph['credit'])+'</a></cite></blockquote><div class="ha-personal-text">'+''.join('<p>'+e(t)+'</p>' for t in introduction['paragraphs'])+'</div></section>'
    body+='<p class="ha-scope">从斯瓦特、克什米尔与尼泊尔到西藏，也收入与这些传统相连的东印度作品及部分宫廷供养器物。</p>'+maphtml
    body+='<aside class="ha-history-entry" id="history-entry"><p class="eyebrow">HISTORY &amp; LOOKING</p><h2><a href="history/">历史与观看</a></h2><p>展签上的年代，放回山谷与寺院的历史。展开西藏、尼泊尔的两条时间线，再回到一尊像、一顶法冠、一幅画。</p><p><a href="history/#tibet">西藏：译经、寺院与供养 →</a>　<a href="history/#nepal">尼泊尔：城市、礼仪与手艺 →</a></p></aside>'
    body+='<nav class="ha-chapters" id="chapters" aria-label="章节阅读">'+''.join(f'<a href="#{c["chapter_id"]}"><small>{i+1:02d}</small>{e(c["title_zh"])}</a>' for i,c in enumerate(chapters))+'</nav>'
    for c in chapters:
        body+=f'<section class="ha-section" id="{c["chapter_id"]}"><header><p class="eyebrow">{e(c["subtitle_zh"])}</p><h2>{e(c["title_zh"])}</h2><p>{e(c["intro_zh"])}</p></header><div class="ha-readings">'
        for i,uid in enumerate(c['unit_ids']):
            u=ub[uid];w=by[u['focus_work_id']]
            featured=i==0 or u.get('featured',False)
            body+=f'<article class="ha-reading {"ha-featured" if featured else ""}" data-reading="{uid}"><a href="{uid}/" class="ha-reading-image">{img(w["primary_photo"],w["image_alt_zh"],small=not featured)}</a><div><p class="eyebrow">{uid[1:]} / 细读</p><h3><a href="{uid}/">{e(u["title_zh"])}</a></h3><p>{e(u["teaser"])}</p><p class="ha-note">{e(w["title_zh"])} · {e(w["date_label"])}</p><a class="text-link" href="{uid}/">展开照片与札记 →</a></div></article>'
        body+='</div><p class="ha-return"><a href="#places">回到地域导览 ↑</a></p></section>'
    if recent:
        body+='<section class="ha-recent ha-section" id="recent-notes" aria-labelledby="recent-title"><h2 id="recent-title">最近新增／重访札记</h2><ul>'
        for update in recent:
            w=by[update['work_id']];kind={'new':'新增作品','research':'资料更新','revisit':'重访札记'}[update['kind']]
            fragment='#visit-'+update['visit_id'] if update.get('visit_id') and visit_by[update['visit_id']].get('public') and visit_by[update['visit_id']].get('observation') else ''
            body+=f'<li data-update="{e(update["update_id"])}"><p class="ha-note">{kind} · 发布于 <time datetime="{update["published_on"]}">{update["published_on"]}</time></p><h3><a href="{w["work_id"]}/{fragment}">{e(w["title_zh"])} →</a></h3><p>{e(update["summary"])}</p></li>'
        body+='</ul></section>'
    ninst=sum(w['scope']=='installation' for w in works)
    body+=f'<section class="ha-section" id="catalogue"><p class="eyebrow">THE VIEWING RECORD</p><h2>完整亲见目录</h2><p>{len(works)-ninst}条作品／组合记录'+(f'，以及{ninst}条佛堂陈设记录' if ninst else '')+'。同一件作品的重访照片合并保留。</p><details id="ha-catalogue"><summary>展开目录 · 查找作品与现场资料</summary><p><a href="#places">按地区、年代、材料或题材筛选 ↑</a></p><div class="ha-catalogue-grid">'
    for w in works:
        body+=f'<article class="ha-record" id="{w["work_id"]}" data-work="{w["work_id"]}"><a href="{w["work_id"]}/">{img(w["primary_photo"],w["image_alt_zh"],small=True)}<h3>{e(w["title_zh"])}</h3></a><p class="ha-note">{e(w["date_label"])}<br>{e(collection(w))}</p><button class="ha-map-work" data-focus="{w["work_id"]}" hidden>在地图中看</button></article>'
    body+='</div><p id="ha-empty" hidden>没有符合条件的记录。<button data-reset>清除筛选</button></p></details></section><section class="ha-section"><h2>沿着同一件作品继续读</h2><p><a href="../xuzhou/">虚舟收藏 →</a>　<a href="../densatil/">丹萨替寺造像 →</a>　<a href="../early-buddhist-art/">早期佛教艺术 →</a></p><details><summary>资料与摄影</summary><p>现场摄影：Merton。作品资料依据拍摄展签及各馆公开记录；具体来源随作品列出。地域图中的点与圆用于阅读导航，收藏机构与拍摄展馆分别记录。</p><p>作品年代及归属可能随研究更新，旧展签与现行馆录的差异保留在相应作品页。</p></details></section>'
    write('', '喜马拉雅艺术',body)
    if integrate:
        home=ROOT/'museum-notes/index.html';h=home.read_text();entry='<!-- himalayan-home --><a class="issue-link" href="himalayan-art/"><img src="himalayan-art/images/h1677-900.webp" width="1280" height="1707" loading="lazy" alt="古格观音全貌，冠饰、双手与底座；Merton现场摄影" style="object-fit:contain"><div><p class="eyebrow">HIMALAYAN ART</p><h2>喜马拉雅艺术</h2><p>山口、河谷与神圣的形体。从供养铭文到曼荼罗，重新连接散见于不同博物馆的作品。</p><p class="issue-meta">'+str(len(chapters))+'章 · '+str(len(units))+'篇细读 · 地域与观看机构导览</p><span class="text-link">走进这一辑 →</span></div></a><!-- /himalayan-home -->'
        h=re.sub(r'<!-- himalayan-home -->.*?<!-- /himalayan-home -->','',h,flags=re.S)
        h=h.replace('<!-- early-buddhist-home -->',entry+'<!-- early-buddhist-home -->',1)
        h=re.sub(r'<li><h3>喜马拉雅艺术</h3>.*?</li>','',h);home.write_text(h)
    print(f'Himalayan Art: {len(works)} records, {len(units)} readings, {len(manifest)} own-photo assets')

if __name__=='__main__':build()
