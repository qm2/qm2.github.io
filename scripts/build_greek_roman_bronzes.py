"""Build the bronze notebook from canonical works, shared photographs and reviewed prose."""
from pathlib import Path
from html import escape as e
import json,re
from build_homer import LIGHTBOX
from museum_image_urls import image_url
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/greek-roman-bronzes'

def build():
 def load(n):return json.loads((BASE/f'data/{n}.json').read_text())
 works=load('works');by={w['id']:w for w in works};photos=load('photos');notes=load('editorial');chapters=load('sections');museums=load('museums');sources=load('sources');history=load('history');comparisons=load('comparisons');sb={s['id']:s for s in sources};sn={s['id']:i+1 for i,s in enumerate(sources)}
 def cites(keys):return '<span class="rs-cites">'+''.join(f' <a href="{e(sb[k]["url"])}" title="{e(sb[k]["title"])}" aria-label="来源：{e(sb[k]["title"])}">[{sn[k]}]</a>' for k in dict.fromkeys(keys))+'</span>' if keys else ''
 def paras(rows):return ''.join('<p>'+e(p['text'])+cites(p.get('source_ids',[]))+'</p>' for p in rows)
 def bibliography(keys):return '<ol class="rs-bibliography">'+''.join(f'<li value="{sn[k]}"><a href="{e(sb[k]["url"])}">{e(sb[k]["title"])} ↗</a></li>' for k in dict.fromkeys(keys))+'</ol>'
 def asset(name,pre=''):
  return image_url('museum-notes/greek-roman-bronzes/images/'+name,pre+'images/'+name)
 def image(n,pre='',eager=False,sizes='(max-width:600px) 90vw, 580px',alt=None):
  p=photos[str(n)];vs=p['variants'];v=min(vs,key=lambda x:abs(x['width']-960))
  return f'<img src="{asset(v["file"],pre)}" srcset="'+', '.join(f'{asset(v["file"],pre)} {v["width"]}w' for v in vs)+f'" sizes="{sizes}" width="{p["display_width"]}" height="{p["display_height"]}" alt="{e(alt or p["caption"])}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
 def figure(n,pre='',caption=None,eager=False,maxwidth=None):
  p=photos[str(n)];cap=caption or p['caption'];limit=maxwidth or (580 if p['display_height']>p['display_width'] else 960);width=min(limit,p['display_width'])
  return f'<figure class="rs-photo" style="--photo-width:{width}px"><a data-photo href="{asset(p["full"],pre)}" data-original="{asset("originals/"+p["original"],pre)}" data-caption="{e(cap)} · Merton摄" aria-label="放大：{e(cap)}">'+image(n,pre,eager,f'(max-width:600px) 90vw, {width}px',cap)+f'</a><figcaption>{e(cap)} · Merton摄</figcaption></figure>'
 def shell(title,body,depth=0,cover='1987',description=''):
  pre='../'*depth;up='../'*(depth+1)
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton · 博物馆札记</title><meta name="description" content="{e(description or '希腊与罗马世界的青铜：身体、权力与幸存。从亲见作品出发，读姿态、铸造与保存。')}"><meta property="og:image" content="{asset(photos[cover]['full'],'https://qm2.github.io/museum-notes/greek-roman-bronzes/')}"><link rel="stylesheet" href="{up}museum.css"><link rel="stylesheet" href="{up}caravaggio/caravaggio.css"><link rel="stylesheet" href="{up}roman-sarcophagi/roman.css"><link rel="stylesheet" href="{pre}bronzes.css"><script defer src="{up}caravaggio/caravaggio.js"></script><script defer src="{up}roman-sarcophagi/roman.js"></script><script defer src="{pre}bronzes.js"></script></head><body class="rs-page gb-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{up}">Merton</a><nav aria-label="主导航"><a href="{pre or './'}">青铜专题</a><a href="{pre}history/">历史与观看</a><a href="{pre}atlas/">所见图录</a><a href="{pre}compare/">并看</a></nav></header><main id="main" class="wrap">{body}</main><footer class="site-footer wrap"><a href="{up}">← 博物馆札记</a><span>现场摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
 def write(route,body,title,depth=0,cover='1987',description=''):
  target=BASE/route;target.mkdir(parents=True,exist_ok=True);(target/'index.html').write_text(shell(title,body,depth,cover,description))
 def links(ids,pre='../'):
  return '<div class="rs-link-row">'+''.join(f'<a href="{pre}{i}/">{e(by[i]["title_zh"])} →</a>' for i in ids)+'</div>'
 def card(w,pre='',filtered=False):
  attrs=''
  if filtered:attrs=f' data-record="{w["id"]}" data-museum="{w["museum_id"]}" data-theme="{e(w["theme"])}" data-search="{e(" ".join(str(w.get(k) or "") for k in ["title_zh","title_original","accession","viewing_museum","viewing_city","period","type"]))}"'
  return f'<article class="rs-card" id="{w["id"]}"{attrs}><a class="rs-thumb" href="{pre}{w["id"]}/">'+image(w['cover'],pre,sizes='(max-width:600px) 90vw, 350px')+f'</a><p class="rs-meta">{e(w["date_display"])}</p><h3><a href="{pre}{w["id"]}/">{e(w["title_zh"])}</a></h3><p>{e(notes[w["id"]]["lead"])}</p><p class="rs-meta">{e(w["viewing_museum"])} · {len(w["photo_order"])}张作品照'+(f' · <a href="{pre}{w["id"]}/#labels">展签</a>' if w['label_photos'] else '')+'</p></article>'
 def gallery(keys,pre):
  if not keys:return ''
  return '<section class="rs-gallery" data-rs-gallery><h2>换一个角度</h2><div class="rs-gallery-controls" hidden><button type="button" data-prev>上一张</button><span data-count role="status" aria-live="polite"></span><button type="button" data-next>下一张</button><button type="button" data-all aria-pressed="false">展开全部</button></div><div class="rs-slides">'+''.join('<div class="rs-slide">'+figure(n,pre)+'</div>' for n in keys)+'</div></section>'
 def facts(w):
  accession=w['accession'] or ('；'.join(x['name']+' '+(x['accession'] or '编号待核') for x in w['components']) if w.get('components') else '待核实')
  rows=[('年代',w['date_display']),('材料',w['material']),('形制',w['type']),('尺寸',w.get('dimensions')),('收藏与观看',w['viewing_museum']+' · '+w['viewing_city']),('馆藏号',accession)]
  return '<dl class="rs-facts">'+''.join(f'<div><dt>{e(k)}</dt><dd>{e(str(v))}</dd></div>' for k,v in rows if v)+'</dl>'
 def footlinks():return '<p class="rs-return"><a href="../">← 青铜专题</a>　<a href="../history/">历史与观看 →</a>　<a href="../atlas/">所见图录 →</a></p>'
 # Eighteen independent viewing records; components never create extra objects.
 for w in works:
  wid=w['id'];n=notes[wid];c=next((c for c in chapters if wid in c['works']),None)
  body=f'<nav class="breadcrumbs"><a href="../">希腊与罗马世界的青铜</a><span>/</span><a href="../#{c["id"] if c else "afterlife"}">{e(c["title"] if c else "年代争议与后世接受")}</a></nav><header class="rs-title"><p class="eyebrow">BRONZE / {wid.upper()}</p><h1>{e(w["title_zh"])}</h1><p class="rs-meta">{e(w["title_original"])}</p><p class="rs-lead">{e(n["lead"])}</p></header>'
  body+=figure(w['cover'],'../',eager=True)+facts(w)
  body+='<div class="rs-reading"><aside class="gb-looking"><h2>在照片里看</h2><ol>'+''.join('<li>'+e(x)+'</li>' for x in n['look'])+'</ol></aside>'
  for idx,sec in enumerate(n['sections']):
   body+='<section><h2>'+e(sec['title'])+'</h2>'+paras(sec['paragraphs'])+'</section>'
  body+='<p class="gb-memory">'+e(n['memory'])+'</p></div>'
  body+=gallery([k for k in w['photo_order'] if k!=w['cover']],'../')
  if w['label_photos']:body+='<details class="rs-labels" id="labels"><summary>现场展签与背景说明 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+''.join(figure(k,'../') for k in w['label_photos'])+'</details>'
  keys=list(dict.fromkeys(w['source_ids']+[s for sec in n['sections'] for p in sec['paragraphs'] for s in p.get('source_ids',[])]+[s for p in n['notes'] for s in p.get('source_ids',[])]))
  body+='<section class="rs-reading rs-documentation"><h2>资料与来源</h2>'
  if n['notes']:body+='<details><summary>断代、归属与收藏资料 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+paras(n['notes'])+'</details>'
  if w['label_photos']:body+='<p>基本资料亦参见<a href="#labels">本页现场展签</a>；照片中的细节与馆方解释分别叙述。</p>'
  body+=bibliography(keys)+'</section><aside class="rs-related"><h2>接着看</h2>'+links(n['related'])
  for group in comparisons:
   if wid in group['works']:body+=f'<p><a href="../compare/#{group["id"]}">并看：{e(group["title"])} →</a></p>'
  if wid=='b15':body+='<p><a href="../../roman-sarcophagi/stories/#heracles">从圆雕的属性，到石棺上的赫拉克勒斯功业 →</a></p>'
  if wid=='b12':body+='<p><a href="../../roman-sarcophagi/stories/#dionysus-india">从酒神立像，到石棺上的酒神队伍 →</a></p>'
  body+='</aside>'+footlinks();write(wid,body,w['title_zh'],1,w['cover'],n['lead'])
 # Home, limited to four full-height photographs; the catalogue remains independent.
 body='<div class="gb-hero"><header class="rs-title"><p class="eyebrow">GREEK &amp; ROMAN BRONZES</p><h1>希腊与罗马世界的青铜</h1><p class="subtitle">身体、权力与幸存</p><p class="rs-lead">一双停在膝上的手，一个向外伸展的姿势，一张失去嵌眼的脸。从博物馆里的亲见作品，走近铜所塑造的身体，也看它们怎样留到今天。</p><p><a href="b11/">从休息的拳击手开始 →</a></p></header>'+figure('1987',caption='休息的拳击手 · 罗马国家博物馆马西莫宫 · 1055',eager=True,maxwidth=460)+'</div>'
 body+='<nav class="rs-chapter-nav" aria-label="阅读线索">'+''.join(f'<a href="#{c["id"]}"><span>{i+1:02d}</span>{e(c["title"])}</a>' for i,c in enumerate(chapters))+'<a href="#afterlife">母狼：年代与后世</a></nav>'
 body+='<section class="rs-guide-entry"><p class="eyebrow">HISTORY &amp; LOOKING</p><h2>先看身体，再读它的来处</h2><p>现存铸件与希腊原型有什么区别？青铜原来有哪些颜色？从分铸、镶嵌和修复，读懂展签之外的细节。</p><div class="rs-link-row"><a href="history/">历史与观看 →</a><a href="compare/">四组并看 →</a><a href="atlas/">观看地图与年代图录 →</a></div></section>'
 for i,c in enumerate(chapters):
  w=by[c['featured']];body+=f'<section class="rs-chapter" id="{c["id"]}"><div class="rs-section-title"><p class="eyebrow">{i+1:02d} / BRONZE</p><h2>{e(c["title"])}</h2><p>{e(c["intro"])}</p></div>'
  if w['id']=='b11':body+='<div class="gb-feature-text"><h3><a href="b11/">拳击手：停下来的身体</a></h3><p>'+e(notes['b11']['memory'])+'</p><a href="b11/">读姿态、伤痕与红铜的颜色 →</a></div>'
  else:body+='<div class="gb-feature">'+figure(w['cover'],caption=w['title_zh']+' · '+w['date_display'],maxwidth=460)+'<div><h3><a href="'+w['id']+'/">'+e(w['title_zh'])+'</a></h3><p>'+e(notes[w['id']]['lead'])+'</p><p class="gb-memory">'+e(notes[w['id']]['memory'])+'</p><a href="'+w['id']+'/">进入作品细读 →</a></div></div>'
  body+='<div class="rs-grid">'+''.join(card(by[k]) for k in c['works'] if k!=w['id'])+'</div></section>'
 body+='<section class="gb-afterlife" id="afterlife"><p class="eyebrow">AN IMAGE AFTER ANTIQUITY</p><h2>罗马的象征，也有另一段时间</h2><div class="gb-feature">'+figure('1972',caption='卡比托利欧母狼 · 传统古代归属与中世纪测年之间',maxwidth=560)+'<div><h3><a href="b06/">母狼：年代怎样被重新讨论</a></h3><p>'+e(notes['b06']['lead'])+'</p><p>作为年代争议对照单列，保留旧展签、馆方题名与科学测年的不同证据。</p><a href="b06/">查看这组作品 →</a></div></div></section>'
 body+=f'<section class="rs-atlas-entry"><h2>所见青铜</h2><p>{len(works)}组观看记录，来自{len(museums)}家博物馆。{len(works)-1}组古代雕塑与装饰，另有母狼年代争议对照。残件、成组构件和独立雕像，按各自关系整理。</p><div class="rs-link-row"><a href="atlas/">地图、年代与完整图录 →</a><a href="compare/">四组并看 →</a></div></section><section class="rs-guide-entry"><h2>从圆雕身体，到浮雕故事</h2><p>英雄与酒神也出现在罗马石棺上。换一种材料和用途，身体会怎样进入叙事？</p><a href="../roman-sarcophagi/">石棺上的故事 →</a></section><section class="rs-reading rs-documentation"><h2>照片与资料</h2><p>这一辑使用我的现场摄影：24张作品照与20张展签、背景说明，共44张原始照片。共享展牌只计一次；巨像残件和船饰的分件关系见各页。作品资料据现场展签、馆方目录与所列研究整理。</p><p>原图保留在图片查看器中；拍摄日期未有记录的作品，不从文件名推定到访时间。</p></section>'
 write('',body,'希腊与罗马世界的青铜：身体、权力与幸存')
 # Reading guide.
 body='<header class="rs-title"><p class="eyebrow">HISTORY &amp; LOOKING</p><h1>身体怎样铸成，铜像怎样幸存</h1><p class="rs-lead">'+e(history['lead'])+'</p></header><nav class="rs-link-row rs-guide-nav">'+''.join(f'<a href="#{s["id"]}">{e(s["title"])}</a>' for s in history['sections'])+'</nav><div class="rs-reading rs-history">'
 for s in history['sections']:
  body+='<section id="'+s['id']+'"><h2>'+e(s['title'])+'</h2>'+paras(s['paragraphs'])+'<div class="rs-guide-works">'+links(s['works'])+'</div></section>'
  if s['id']=='models':body+='<details><summary>四段时间，四种观看问题 <span class="rs-icon" aria-hidden="true">＋</span></summary><div class="rs-guide-table" tabindex="0" role="region" aria-label="时期与观看问题，窄屏可横向浏览"><table><caption>大致时期相互衔接，具体作品以馆方断代为准</caption><thead><tr><th>阶段</th><th>本辑入口</th><th>观看问题</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(t)+'</td>' for t in row)+'</tr>' for row in history['periods'])+'</tbody></table></div></details>'
 body+='<section id="field-card" class="rs-field-card"><h2>去下一家博物馆时</h2><ol>'+''.join('<li><h3>'+e(q[0])+'</h3><p>'+e(q[1])+f' <a href="../{q[2]}/">看一个例子 →</a></p></li>' for q in history['questions'])+'</ol></section><section class="rs-documentation"><h2>资料与来源</h2>'+bibliography([k for s in history['sections'] for p in s['paragraphs'] for k in p['source_ids']])+'</section></div>'+footlinks()
 write('history',body,'历史与观看 · 青铜',1)
 # Native-ratio comparison, never a reconstructed assembly.
 body='<header class="rs-title"><p class="eyebrow">SIDE BY SIDE</p><h1>让身体彼此照见</h1><p class="rs-lead">从姿势、表面与用途，比较这批亲见作品。</p><p class="rs-meta">照片保留各自比例，并排不表示实物等大。完整尺寸与资料见作品页。</p></header><nav class="rs-link-row">'+''.join(f'<a href="#{g["id"]}">{e(g["title"])}</a>' for g in comparisons)+'</nav>'
 for g in comparisons:
  body+=f'<section class="compare-group rs-comparison" id="{g["id"]}"><h2>{e(g["title"])}</h2><p>{e(g["text"])}</p><div class="rs-compare-grid">'
  for wid in g['works']:
   w=by[wid];body+='<div>'+figure(w['cover'],'../',w['title_zh'])+f'<p class="rs-meta">{e(w["date_display"])} · {e(w["viewing_museum"])}</p><a href="../{wid}/">作品细读与来源 →</a></div>'
  body+='</div><div class="rs-reading"><ul>'+''.join('<li>'+e(p)+'</li>' for p in g['points'])+'</ul></div></section>'
 write('compare',body+footlinks(),'四组并看 · 青铜',1)
 # Atlas. Natural Earth base map is already vendored by the notebook.
 def map_svg(region,bounds):
  x0,x1,y0,y1=bounds;width,height=540,300
  def xy(x,y):return ((x-x0)/(x1-x0)*width,(y1-y)/(y1-y0)*height)
  paths=[];land=json.loads((ROOT/'museum-notes/homer/data/ne_110m_land.geojson').read_text())
  for f in land['features']:
   polys=f['geometry']['coordinates'] if f['geometry']['type']=='MultiPolygon' else [f['geometry']['coordinates']]
   for poly in polys:
    for ring in poly:
     if any(x0<=p[0]<=x1 and y0<=p[1]<=y1 for p in ring):paths.append('M'+'L'.join(f'{xy(*p)[0]:.1f},{xy(*p)[1]:.1f}' for p in ring)+'Z')
  out=f'<svg viewBox="0 0 540 300" role="group" aria-label="{e(region)}观看馆址"><defs><clipPath id="clip-{region}"><rect width="540" height="300"/></clipPath></defs><g clip-path="url(#clip-{region})"><path class="rs-land" d="'+''.join(paths)+'"/></g>'
  offsets={'capitoline':(-72,13),'mnr':(42,-25),'vatican':(-38,-59),'mfah':(0,7),'kimbell':(-8,-9),'cleveland':(-18,-16),'walters':(12,8)}
  for m in museums:
   if not(x0<=m['lon']<=x1 and y0<=m['lat']<=y1):continue
   x,y=xy(m['lon'],m['lat']);dx,dy=offsets.get(m['id'],(0,0));tx=x+dx;ty=y+dy;count=sum(w['museum_id']==m['id'] for w in works);label={'capitoline':'卡比托利欧','mnr':'马西莫宫'}.get(m['id'],m['city']);anchor='end' if tx>410 or m['id']=='capitoline' else 'start';textx=tx-10 if anchor=='end' else tx+10
   out+=f'<circle class="gb-location-dot" cx="{x:.1f}" cy="{y:.1f}" r="2"/><a href="?museum={m["id"]}#catalogue" data-map-museum="{m["id"]}" aria-label="{e(m["name"])}，{count}组"><title>{e(m["name"])} · {count}组</title><line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty:.1f}"/><circle cx="{tx:.1f}" cy="{ty:.1f}" r="7"/><text x="{textx:.1f}" y="{ty+4:.1f}" text-anchor="{anchor}">{e(label)}</text></a>'
  return out+'</svg>'
 body=f'<header class="rs-title"><p class="eyebrow">ATLAS &amp; TIMELINE</p><h1>所见青铜</h1><p class="rs-lead">{len(works)}组观看记录，{len(museums)}家博物馆。按地点与年代，重看身体的不同形式。</p></header><section id="map"><h2>在这些地方相遇</h2><div class="rs-maps"><div><h3>北美</h3>'+map_svg('north-america',(-105,-70,24,48))+'</div><div><h3>欧洲</h3>'+map_svg('europe',(-6,27,35,55))+'</div></div><p class="rs-meta">地图表示观看馆址，不表示古代制作地。罗马区域以引线分开相邻馆名。底图：<a href="https://www.naturalearthdata.com/about/terms-of-use/">Natural Earth · 公共领域</a>。</p><div class="rs-museum-list">'+''.join(f'<a href="?museum={m["id"]}#catalogue" data-map-museum="{m["id"]}">{e(m["name"])}<span>{sum(w["museum_id"]==m["id"] for w in works)}组</span></a>' for m in museums)+'</div></section>'
 body+='<section class="rs-atlas-controls" aria-label="筛选作品"><label>名称、博物馆或编号<input id="rs-search" type="search" placeholder="如：阿波罗、62.19"></label><label>观看机构<select id="rs-museum"><option value="all">全部机构</option>'+''.join(f'<option value="{m["id"]}">{e(m["name"])}</option>' for m in museums)+'</select></label><label>主题<select id="rs-theme"><option value="all">全部主题</option>'+''.join(f'<option>{e(t)}</option>' for t in dict.fromkeys(w['theme'] for w in works))+'</select></label><button type="button" id="rs-clear">清除条件</button><p id="rs-results" role="status" aria-live="polite"></p></section>'
 for m in museums:
  members=[w for w in works if w['museum_id']==m['id']]
  body+=f'<aside class="gb-museum-preview" data-museum-preview="{m["id"]}" hidden><h2>{e(m["name"])}</h2><p>{e(m["city"])} · {len(members)}组观看记录；下方图录显示与当前条件相符的作品。</p><div class="gb-mini-grid">'+''.join(f'<a href="../{w["id"]}/">'+image(w['cover'],'../',sizes='120px')+'<span>'+e(w['title_zh'])+'</span></a>' for w in members[:3])+'</div><a href="#catalogue">查看筛选后的完整列表 ↓</a></aside>'
 body+=f'<p class="rs-meta">{len(photos)}张原始照片，包括24张作品照和20张展签／背景图。共享展签、成组构件与不同视角分别记录。</p><details class="rs-timeline" open><summary>沿年代重看 <span class="rs-icon" aria-hidden="true">＋</span></summary><p>线段表示断代范围；虚线表示宽泛或有争议的约年。骑马像的两点是176年与180年两个候选年代。棕色为主年代，灰色为展签的另一断代。手机可横向浏览。</p><div class="rs-time-scroll" tabindex="0" role="region" aria-label="青铜年代时间线，可横向滚动" style="--time-step:11.111%"><div class="rs-time-axis"><span>公元前 ← → 公元</span><div>'
 for year in range(-500,401,100):
  label='前'+str(-year) if year<0 else ('纪元' if year==0 else str(year))
  body+=f'<b style="left:{(year+500)/900*100}%">{label}</b>'
 body+='</div></div>'
 for w in sorted((w for w in works if w['include_in_core_timeline']),key=lambda w:w['date_start']):
  marks=''
  if w.get('timeline_candidates'):marks=''.join(f'<i class="rs-time-dot" style="left:{(v+500)/900*100}%"></i>' for v in w['timeline_candidates'])
  else:marks=f'<i class="rs-time-range {"approx" if w["id"] in ["b10","b11","b15","b16","b18"] else ""}" style="left:{(w["date_start"]+500)/900*100}%;width:{(w["date_end"]-w["date_start"])/900*100}%"></i>'
  for alt in w.get('alternate_dates',[]):marks+=f'<i class="rs-time-range gb-alternate" style="left:{(alt["start"]+500)/900*100}%;width:{(alt["end"]-alt["start"])/900*100}%" title="{e(alt["label"])}"></i>'
  body+=f'<a class="rs-time-row" data-time-record="{w["id"]}" href="../{w["id"]}/"><span>'+image(w['cover'],'../',sizes='76px')+'<span>'+e(w['title_zh'])+'<small>'+e(w['date_display'])+' · '+e(w['viewing_city'])+'</small></span></span><div>'+marks+'</div></a>'
 body+='</div><p class="rs-meta">赫拉克勒斯的线段示意“1世纪末至3世纪初”；宽泛年代不表示已知起止年份。“纪元”标示公元前后分界，不另设公元0年。</p></details><aside class="gb-wolf-dates" data-time-record="b06"><h2>时间线外的对照：母狼</h2><div><p><strong>公元前5世纪</strong><br>传统归属；现场旧展签与部分馆方目录。</p><p><strong>公元11—12世纪</strong><br>铸芯测年研究支持的中世纪范围。</p></div><a href="../b06/">查看两类证据与完整记录 →</a></aside><section id="catalogue"><h2>完整图录</h2><p id="rs-empty" hidden>没有符合当前条件的记录。</p><div class="rs-grid">'+''.join(card(w,'../',True) for w in works)+'</div></section><p class="rs-return"><a href="../history/#field-card">去下一家博物馆时：六个问题 →</a>　<a href="../compare/">四组并看 →</a></p>'
 write('atlas',body,'所见青铜 · 博物馆与年代',1)
 # Notebook index: regenerate after the other topics, keep entries adjacent.
 home=ROOT/'museum-notes/index.html';text=home.read_text();text=re.sub(r'<!-- bronze-entry -->.*?<!-- /bronze-entry -->','',text,flags=re.S)
 entry='<!-- bronze-entry --><a class="issue-link" href="greek-roman-bronzes/">'+image('1987','greek-roman-bronzes/',sizes='(max-width:600px) 90vw, 500px')+f'<div><p class="eyebrow">CLASSICAL ART / GREEK &amp; ROMAN BRONZES</p><h2>希腊与罗马世界的青铜</h2><p>身体、权力与幸存。从休息的拳击手到皇帝骑马像，近看姿态、铸造与铜像的后来生活。</p><p class="issue-meta">{len(works)}组观看记录 · {len(museums)}家博物馆<br>历史与观看 / 并看 / 地图与年代</p><span class="text-link">走进这个专题 →</span></div></a><!-- /bronze-entry -->'
 assert '<!-- /roman-entry -->' in text;text=text.replace('<!-- /roman-entry -->','<!-- /roman-entry -->'+entry,1);home.write_text(text)
 print(f'Built Greek/Roman bronzes: {len(works)} records, home, history, comparisons, atlas; {len(photos)} originals.')
if __name__=='__main__':build()
