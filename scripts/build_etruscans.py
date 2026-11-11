"""Etruscan notebook: canonical objects, visits and photographs; image bytes live in R2.
Run after other topic builders so cross-topic entry patches survive a full rebuild.
"""
from pathlib import Path
from html import escape as esc
from urllib.parse import quote
import json,re
from build_homer import LIGHTBOX
from museum_image_urls import image_url
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'museum-notes/etruscans'; U='/museum-notes/etruscans/'
def load(n):return json.loads((BASE/'data'/f'{n}.json').read_text())
def build():
 works=load('objects');by={w['id']:w for w in works};photos={p['photo_id']:p for p in load('photos')};reads={r['object_id']:r for r in load('deep_readings')};caps=load('captions');notes=load('object-notes');chapters=load('chapters');places=load('places');pb={p['id']:p for p in places};sources=load('sources');sb={s['id']:s for s in sources};crops=load('detail-crops');favs=load('personal-favorites');groups=load('comparisons');taxonomy=load('function_taxonomy');collections=load('collections');timeline=load('timeline');panels=load('panels')
 for w in works:w['title_zh']=w.get('title_zh') or w['title_en']
 editing=load('photo-editing');derivatives=load('image-derivatives');photos.update(derivatives)
 photo_count=len(load('photos'))
 favorites={f['object_id']:f for f in favs['items']}
 relation={'findspot':'发现地点','possible_findspot':'可能发现于','probable_findspot':'很可能发现于','near_findspot':'发现于附近','production':'制作地','attributed_production':'归属制作中心','probable_production':'可能制作地','label_place_unspecified':'展签所列地点','label_region':'展签所列地域','unknown':'地域未详'}
 kind={'object':'作品','detail':'局部','label':'现场展签','panel':'展厅说明','context':'展陈环境'}
 def a(path):return image_url('museum-notes/etruscans/images/'+path,U+'images/'+path)
 def cover(w):return editing['full_views'].get(w['id'],favorites.get(w['id'],{}).get('full_photo',w['primary_photo']))
 def date(w):
  s=w['date_label'];s=re.sub(r'\babout\s*','约',s,flags=re.I);s=s.replace('BC','公元前').replace('AD','公元')
  # Keep the original date string in metadata; use a natural Chinese reading here.
  s=re.sub(r'([\d–—\- ]+)\s*公元前',lambda m:'公元前'+m[1].strip()+'年',s)
  s=re.sub(r'公元\s*([\d–—\- ]+)',lambda m:'公元'+m[1].strip()+'年',s)
  return s
 def english_subtitle(w):return esc(w["title_en"]) if w["title_zh"]!=w["title_en"] else ""
 def cname(w):return w['collection_label'].split(' / ')[0]
 def caption(pid):
  p=photos[pid]
  if pid in derivatives:return p['caption']+(' · 原片局部' if p['kind']=='detail' else '')
  if pid in caps:return caps[pid]
  if p['kind']=='label':
   names=list(dict.fromkeys(by[x['object_id']]['title_zh'] for x in p['links'] if x.get('object_id') in by))
   return ('共用现场展签' if len(names)>2 else '现场展签：'+'、'.join(names)) if names else '现场展签'
  if p['kind']=='panel':
   match=next((s for s in panels if s['photo_id']==pid),None)
   return '展厅说明：'+(match['title_zh'] if match else p['description'])
  return p['description']+(' · 原片局部' if p['kind']=='detail' else '')
 def img(pid,eager=False,sizes='(max-width:650px) 90vw, 580px',alt=None):
  p=photos[pid];v=min(p['variants'],key=lambda v:abs(v['width']-960))
  return f'<img src="{a(v["file"])}" srcset="'+', '.join(f'{a(v["file"])} {v["width"]}w' for v in p['variants'])+f'" sizes="{sizes}" width="{p["display_width"]}" height="{p["display_height"]}" alt="{esc(alt or caption(pid))}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
 def figure(pid,cap=None,eager=False,limit=None):
  p=photos[pid];cap=cap or caption(pid);width=min(p['display_width'],limit or (560 if p['display_height']>p['display_width'] else 960),780*p['display_width']/p['display_height'])
  return f'<figure class="rs-photo" style="--photo-width:{width}px"><a data-photo href="{a(p["variants"][-1]["file"])}" data-original="{a(p["path"])}" data-caption="{esc(cap)} · Merton摄" aria-label="放大：{esc(cap)}">'+img(pid,eager,f'(max-width:650px) 90vw, {width}px',cap)+f'</a><figcaption>{esc(cap)} · Merton摄</figcaption></figure>'
 def cites(ids):return '<span class="rs-cites">'+''.join(f' <a href="{esc(sb[k]["url"])}" title="{esc(sb[k]["title"])}">[{int(k[1:])}]</a>' for k in dict.fromkeys(ids) if k in sb)+'</span>'
 def plink(pid,label='现场展签'):return f'<a class="et-evidence" href="{U}photos/#{pid}">{label}</a>'
 def links(ids):return '<div class="rs-link-row">'+''.join(f'<a href="{U}{wid}/">{esc(by[wid]["title_zh"])} →</a>' for wid in dict.fromkeys(ids) if wid in by)+'</div>'
 def bibliography(ids):return '<ol class="rs-bibliography">'+''.join(f'<li value="{int(k[1:])}"><a href="{esc(sb[k]["url"])}">{esc(sb[k]["institution"])}：{esc(sb[k]["title"])} ↗</a> <a class="et-evidence" href="{U}sources/#{k}">查阅范围</a></li>' for k in dict.fromkeys(ids) if k in sb)+'</ol>'
 def shell(title,body,coverpid='c001-full',description='从圣安东尼奥美术馆的亲见作品，走近伊特鲁里亚的城市、身体、宴饮与祈愿。'):
  nav=[('', '专题首页'),('guide/','认识文明'),('atlas/','地图与图录'),('compare/','八组并看'),('photos/','现场档案')]
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Merton · 博物馆札记</title><meta name="description" content="{esc(description)}"><meta property="og:image" content="{a(photos[coverpid]['variants'][-1]['file'])}"><meta property="og:title" content="{esc(title)}"><link rel="preconnect" href="https://images.mertonmuseum.com"><link rel="stylesheet" href="/museum-notes/museum.css"><link rel="stylesheet" href="/museum-notes/caravaggio/caravaggio.css"><link rel="stylesheet" href="/museum-notes/roman-sarcophagi/roman.css"><link rel="stylesheet" href="{U}etruscans.css"><script defer src="/museum-notes/caravaggio/caravaggio.js"></script><script defer src="/museum-notes/roman-sarcophagi/roman.js"></script><script defer src="{U}etruscans.js"></script></head><body class="rs-page et-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="/museum-notes/">Merton</a><nav aria-label="专题导航">{''.join(f'<a href="{U}{path}">{label}</a>' for path,label in nav)}</nav></header><main id="main" class="wrap">{body}</main><footer class="site-footer wrap"><a href="/museum-notes/">← 博物馆札记</a><a href="{U}sources/">资料与来源</a><span>现场摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
 def write(route,title,body,coverpid='c001-full',desc=''):
  body=body.replace('{record_count}',str(len(works))).replace('{reading_count}',str(len(reads))).replace('{photo_count}',str(photo_count))
  d=BASE/route;d.mkdir(exist_ok=True,parents=True);(d/'index.html').write_text(shell(title,body,coverpid,desc or title))
 def heading(title,lead='',en='ETRUSCANS'):
  return f'<header class="rs-title"><p class="eyebrow">{esc(en)}</p><h1>{esc(title)}</h1>'+('<p class="rs-lead">'+esc(lead)+'</p>' if lead else '')+'</header>'
 def mini(w):
  pid=cover(w);p=photos[pid];width=min(260,180*p['display_width']/p['display_height'])
  return f'<a class="et-mini" href="{U}{w["id"]}/"><span class="et-mini-photo" style="--mini-width:{width}px">'+img(pid,sizes=f'(max-width:650px) 40vw, {width}px')+'<span class="et-mini-caption">'+esc(w['title_zh'])+'<small>'+esc(date(w))+'</small></span></span></a>'
 def card(w,filterable=False):
  ds=''
  if filterable:
   vals={'record':w['id'],'place':w['place_id'] or 'unknown','collection':w['collection_code'],'material':material(w),'chapter':w['chapter_id'],'function':' '.join(w['function_tags']),'start':w['date_start'],'end':w['date_end'],'deep':'yes' if w['id'] in reads else 'no','search':' '.join(str(w.get(k) or '') for k in ['title_zh','title_en','inventory_number_as_read','culture_label','material_zh','collection_label','looking_note'])+' '+(pb.get(w['place_id'],{}).get('name_zh',''))+' '+(pb.get(w['place_id'],{}).get('name_en',''))}
   ds=''.join(f' data-{k}="{esc(str(v))}"' for k,v in vals.items())
  count=len(set(w['object_photos']+w['detail_photos']+w['label_photos']))
  return f'<article class="rs-card" id="{w["id"]}"{ds}><a class="rs-thumb" href="{U}{w["id"]}/">'+img(cover(w),sizes='(max-width:650px) 90vw, 330px')+f'</a><p class="rs-meta">{esc(date(w))} · {esc(w["material_zh"])}</p><h3><a href="{U}{w["id"]}/">{esc(w["title_zh"])}</a></h3><p class="et-en">{english_subtitle(w)}</p><p class="rs-meta">{esc(cname(w))}<br>{esc(str(w["inventory_number_as_read"] or "馆藏号待核"))} · {count}张关联照片</p><p><a href="{U}{w["id"]}/">'+('进入细读' if w['id'] in reads else '查看资料与照片')+f' →</a>　<a href="{U}{w["id"]}/#labels">展签</a></p></article>'
 def material(w):
  s=w['material_zh']
  for key,val in [('陶','陶'),('费昂斯','费昂斯'),('金','金银与复合金属'),('银','金银与复合金属'),('青铜','青铜'),('石','石'),('凝灰岩','石'),('木','木'),('骨','骨'),('蛋壳','蛋壳')]:
   if key in s:return val
  return s
 def gallery(pids):
  if not pids:return ''
  return '<section class="rs-gallery" data-rs-gallery><h2>绕到另一面，走近一点</h2><div class="rs-gallery-controls" hidden><button type="button" data-prev>上一张</button><span data-count role="status" aria-live="polite"></span><button type="button" data-next>下一张</button><button type="button" data-all aria-pressed="false">展开全部</button></div><div class="rs-slides">'+''.join('<div class="rs-slide">'+figure(pid)+'</div>' for pid in dict.fromkeys(pids))+'</div></section>'
 # Shared geographical interface: numbered dots keep labels legible without implying survey coordinates.
 def mapview():
  width,height=650,560;x0,x1,y0,y1=10.1,13.4,41.3,44.0
  def xy(x,y):return ((x-x0)/(x1-x0)*width,(y1-y)/(y1-y0)*height)
  paths=[]
  for f in json.loads((BASE/'data/basemap_countries.geojson').read_text())['features']:
   geom=f['geometry'];polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
   for poly in polys:
    for ring in poly:
     paths.append('M'+'L'.join(f'{xy(*v)[0]:.1f},{xy(*v)[1]:.1f}' for v in ring)+'Z')
  svg='<svg viewBox="0 0 650 560" role="group" aria-label="伊特鲁里亚相关城市与遗址区域"><defs><clipPath id="et-map-clip"><rect width="650" height="560"/></clipPath></defs><g clip-path="url(#et-map-clip)"><path class="et-land" d="'+''.join(paths)+'"/>'
  for f in json.loads((BASE/'data/basemap_rivers.geojson').read_text())['features']:
   lines=f['geometry']['coordinates'] if f['geometry']['type']=='MultiLineString' else [f['geometry']['coordinates']]
   for line in lines:svg+='<path class="et-river" d="M'+'L'.join(f'{xy(*v)[0]:.1f},{xy(*v)[1]:.1f}' for v in line)+'"/>'
  svg+='<text x="80" y="470" class="et-water">第勒尼安海</text><text x="420" y="250" class="et-water">台伯河</text></g>'
  # Offsets only separate symbols; a leader terminates at the regional point.
  offsets={'san-gimignano':(16,-16),'volterra':(-6,12),'falerii':(22,-12),'narce':(0,8),'san-casciano':(-15,0),'chiusi':(9,-4)}
  for idx,p in enumerate([p for p in places if p['longitude'] is not None]):
   x,y=xy(p['longitude'],p['latitude']);dx,dy=offsets.get(p['id'],(0,0));tx,ty=x+dx,y+dy
   svg+=f'<a href="{U}atlas/?place={p["id"]}#catalogue" data-map-place="{p["id"]}" data-tier="{p["map_tier"]}" aria-label="{esc(p["name_zh"])}"'+(' hidden="hidden" class="et-extra-dot"' if p['map_tier']>1 else '')+f'><title>{esc(p["name_zh"])} · {esc(p["name_en"])}</title><line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty:.1f}"/><circle cx="{tx:.1f}" cy="{ty:.1f}" r="12"/><text x="{tx:.1f}" y="{ty+4:.1f}" text-anchor="middle">{idx+1}</text></a>'
  svg+='</svg>'
  out='<section id="map" class="et-map"><header><p class="eyebrow">PLACES &amp; CONNECTIONS</p><h2>把器物放回山川之间</h2><p>地点为城市或遗址区域示意。发现地点、制作归属和展签地域，分别见每件资料。</p></header><div class="et-map-tools"><button type="button" data-map-zoom aria-pressed="false">放大地图</button><button type="button" data-map-more aria-pressed="false">更多地点</button><a href="'+U+'atlas/">完整地点与年代索引 →</a></div><div class="et-map-layout"><div class="et-map-scroll" tabindex="0" role="region" aria-label="地图，放大后可横向滚动">'+svg+'</div><div class="et-map-list">'
  for idx,p in enumerate([p for p in places if p['longitude'] is not None]):
   out+=f'<button type="button" data-map-place="{p["id"]}" data-tier="{p["map_tier"]}" aria-expanded="false" aria-controls="place-{p["id"]}"'+(' hidden' if p['map_tier']>1 else '')+f'><span>{idx+1:02d}</span>{esc(p["name_zh"])}<small>{esc(p["name_en"])}</small></button>'
  out+='</div></div><p class="rs-meta">底图与河流：<a href="https://www.naturalearthdata.com/about/terms-of-use/">Natural Earth · 公共领域</a>。现代海岸用于定位；标记不表示精确发掘坐标。</p><div class="et-place-previews">'
  for p in places:
   members=[w for w in works if w['place_id']==p['id']]
   out+=f'<section id="place-{p["id"]}" data-place-preview="{p["id"]}" hidden><h3>{esc(p["name_zh"])} <small>{esc(p["name_en"])}</small></h3><p>{esc(p.get("theme","相关器物"))}。{esc(p["note"])}{cites(p.get("source_ids",[]))}</p><div class="et-mini-grid">'+''.join(mini(w) for w in sorted(members,key=lambda w:w['id'] not in reads)[:3])+f'</div><a href="{U}atlas/?place={p["id"]}#catalogue">查看这里的{len(members)}条记录 →</a></section>'
  return out+'</div><noscript><p>也可通过<a href="'+U+'atlas/#filters">图录的地点选择</a>查阅相关记录。</p></noscript></section>'
 # Independent object pages preserve complete views before close details.
 for w in works:
  wid=w['id'];r=reads.get(wid);chapter=next(c for c in chapters if c['id']==w['chapter_id']);pid=cover(w)
  body=f'<nav class="breadcrumbs"><a href="{U}">伊特鲁里亚</a><span>/</span><a href="{U}#{chapter["id"]}">{esc(chapter["title_zh"])}</a></nav>'
  body+=heading(w['title_zh'],r['question'] if r else w['looking_note'],'ETRUSCANS / OBJECT NOTE' if w['title_zh']==w['title_en'] else w['title_en'])+figure(pid,eager=True)
  place=pb.get(w['place_id']);placevalue=esc(place['name_zh']+' · '+place['name_en']) if place else '未详'
  if place:placevalue=f'<a href="{U}atlas/?place={place["id"]}#catalogue">{placevalue}</a>'
  facts=[('年代',esc(date(w))+' <small>('+esc(w['date_label'])+')</small>'),('材料',esc(w['material_zh'])),('文化归属',esc(w['culture_label'])),(relation.get(w['place_relation'],'地域'),placevalue),('收藏',esc(w['collection_label'])),('馆藏号',esc(str(w['inventory_number_as_read'] or '待核实'))),('观看记录','<br>'.join(esc(('圣安东尼奥美术馆' if v['venue']=='San Antonio Museum of Art' else v['venue'])+' · '+(v.get('date_display') or v.get('date') or '日期未记')) for v in w.get('visits',[])))]
  body+='<dl class="rs-facts">'+''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in facts)+'</dl>'
  if wid in [f'e{n:03}' for n in range(69,77)]:body+='<p class="et-shared-note">照片为共用展柜总览。本件对应展签编号 '+str(int(wid[1:])-68)+'；<a href="#labels">展签位置图 ↓</a></p>'
  sourceids=list(dict.fromkeys(w['research_source_ids']+(r['supplementary_source_ids'] if r else [])))
  if r:
   body+='<article class="rs-reading"><h2>作品札记</h2>'
   for j,para in enumerate(r['paragraphs']):
    body+='<p>'+esc(para)+(' <a class="et-evidence" href="#labels">[展签]</a>' if w['label_photos'] else '')+(cites(sourceids) if j==len(r['paragraphs'])-1 else '')+'</p>'
    for detail in editing['narrative'].get(wid,[]):
     if detail['after_paragraph']==j:body+='<div class="et-reading-photo">'+figure(detail['image'],limit=520)+'</div>'
   body+='<p class="et-memory">'+esc(r['remember'])+'</p></article>'
  else:body+='<div class="rs-reading"><h2>看一处细节</h2><p>'+esc(w['looking_note'])+'</p></div>'
  shown={derivatives.get(pid,{}).get('photo_id',pid)}|{derivatives.get(d['image'],{}).get('photo_id',d['image']) for d in editing['narrative'].get(wid,[])}
  body+=gallery([p for p in w['object_photos']+w['detail_photos'] if p not in shown])
  body+='<details class="rs-labels" id="labels"><summary>现场展签 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+''.join(figure(p) for p in dict.fromkeys(w['label_photos']))+'</details>'
  body+='<section class="rs-reading rs-documentation"><h2>资料与来源</h2>'
  if wid in notes:body+='<details><summary>资料注 <span class="rs-icon" aria-hidden="true">＋</span></summary><p>'+esc(notes[wid])+cites(sourceids)+'</p></details>'
  body+='<p>基本资料与图像解释据本页现场展签；照片观察与补充研究见正文及所列来源。</p>'+bibliography(sourceids)+'</section><aside class="rs-related"><h2>从这件作品继续看</h2>'
  body+=links(r['comparison_ids'] if r else [x for x in chapter['object_ids'] if x!=wid and x in reads][:3])
  body+='<div class="rs-link-row">'+''.join(f'<a href="{U}compare/#{g["id"]}">{esc(g["title"])} →</a>' for g in groups if wid in g['object_ids'])+f'<a href="{U}guide/#{chapter_guide(chapter["id"])}">认识文明：背景与术语 →</a></div></aside>'
  body+=f'<p class="rs-return"><a href="{U}#{chapter["id"]}">← 回到这一章</a>　<a href="{U}atlas/#{wid}">在完整图录中找到它 →</a></p>'
  write(wid,w['title_zh'],body,pid,r['question'] if r else w['looking_note'])
 # Home: personal entry, discrete geographical chooser, nine varied editorial chapters.
 body='<div class="et-hero">'+heading('泥土、青铜与永恒的宴席','伊特鲁里亚文明的现场观看','ETRUSCANS / A VIEWING NOTEBOOK')+figure(editing['hero'],cap='狮首饰青铜大釜 · 公元前675—650年 · 圣安东尼奥特展所见',eager=True,limit=480)+'</div>'
 body+='<div class="rs-preface">'+''.join('<p>'+esc(t)+'</p>' for t in favs['foreword_paragraphs'])+'</div>'
 body+='<p class="et-exhibition">2026年11月 · 圣安东尼奥美术馆<br><i>The Etruscans: From the Heart of Ancient Italy</i><br>展期：2026年10月31日—2027年3月14日 · 旧金山美术博物馆与圣安东尼奥美术馆合作'+cites(['S01'])+'</p>'
 body+='<section class="et-favorites"><p class="eyebrow">FIRST ENCOUNTERS</p><h2>初见最爱</h2><p>'+esc(favs['section_intro'])+'</p><div class="et-favorite-grid">'
 for f in favs['items']:
  c=crops[f['object_id']];v=c['variants']
  body+=f'<a href="{U}{f["object_id"]}/"><div class="et-detail-thumb">'+img(editing['favorites'][f['object_id']],sizes='(max-width:650px) calc((100vw - 54px)/2), (max-width:1280px) calc((100vw - 112px)/5), 230px',alt=f['title_zh']+'：'+c['caption']+'，原片局部')+f'</div><small>原片局部</small><h3>{esc(f["title_zh"])}</h3><p>{esc(f["detail_caption"])}</p></a>'
 body+='</div></section><section class="rs-guide-entry"><p class="eyebrow">A FRAMEWORK FOR THE NEXT ENCOUNTER</p><h2>从一件喜欢的东西，认识一个世界</h2><p>城邦与海路、为逝者安排的居所、神前的祈愿，以及金属与泥土的手艺。先建立几条线索，往后每次看展，都能再添一笔。</p><div class="rs-link-row"><a href="'+U+'guide/">认识伊特鲁里亚 →</a><a href="'+U+'guide/#materials">从材料开始 →</a><a href="'+U+'guide/#gods">神名与器形速查 →</a></div></section>'+mapview()
 body+='<nav class="rs-chapter-nav" aria-label="九章阅读">'+''.join(f'<a href="#{c["id"]}"><span>{i+1:02d}</span>{esc(c["title_zh"])}</a>' for i,c in enumerate(chapters))+'</nav>'
 featureids=['e010','e022','e033','e045','e084','e091','e106','e111','e122']
 for i,c in enumerate(chapters):
  w=by[featureids[i]];r=reads[w['id']];deep=[k for k in c['object_ids'] if k in reads and k!=w['id']]
  body+=f'<section id="{c["id"]}" class="rs-chapter"><header class="rs-section-title"><p class="eyebrow">{i+1:02d} / {esc(c["wall_title_en"])}</p><h2>{esc(c["title_zh"])}</h2><p>{esc(c["intro"])}</p></header><div class="et-feature">'+figure(cover(w),cap=w['title_zh']+' · '+date(w),limit=620)+f'<div><p class="rs-meta">{english_subtitle(w)}</p><h3><a href="{U}{w["id"]}/">{esc(w["title_zh"])}</a></h3><p>{esc(r["question"])}</p><p class="et-memory">{esc(r["remember"])}</p><a href="{U}{w["id"]}/">看完整照片，进入细读 →</a></div></div><div class="rs-grid">'+''.join(card(by[k]) for k in deep[:3])+'</div>'
  if len(deep)>3:body+='<details><summary>这一章还有'+str(len(deep)-3)+'篇细读 <span class="rs-icon" aria-hidden="true">＋</span></summary><div class="et-mini-grid">'+''.join(mini(by[k]) for k in deep[3:])+'</div></details>'
  body+=f'<p class="rs-return"><a href="{U}atlas/?chapter={c["id"]}#catalogue">本章全部{len(c["object_ids"])}条记录 →</a>　<a href="{U}photos/#{c["panel_photos"][0]}">展厅说明 →</a></p></section>'
 body+='<section class="rs-guide-entry"><h2>再让器物彼此照见</h2><p>骨灰瓮怎样重新组成身体？文字是在记录赠礼，还是划定墓葬用途？八组并看，让材料、姿态与人的行动相互解释。</p><a href="'+U+'compare/">进入八组比较 →</a></section><section id="catalogue"><h2>这次展览的完整观展目录</h2><p>{record_count}条器物、成组或部件记录，{reading_count}篇细读，{photo_count}张现场照片。记录条数与馆方“约130件展品”的计数口径不同。</p><p><a href="'+U+'atlas/">打开地图、年代与筛选图录 →</a></p><details><summary>展开{record_count}条记录 <span class="rs-icon" aria-hidden="true">＋</span></summary><div class="et-catalogue-list">'+''.join(f'<a href="{U}{w["id"]}/">{esc(w["title_zh"])}<small>{esc(date(w))}'+(' · 细读' if w['id'] in reads else '')+'</small></a>' for w in works)+'</div></details></section>'
 body+='<section class="et-context"><h2>展厅里的相邻关系</h2><div class="rs-insets">'+figure('p050')+figure('p136')+'</div><p><a href="'+U+'photos/?kind=context">查看展柜总览与现场照片 →</a></p></section><section class="rs-guide-entry"><h2>走向希腊与罗马的展厅</h2><p>这里的英雄、宴饮和青铜身体，也能接回此前的观看。</p><div class="rs-link-row"><a href="/museum-notes/greek-roman-bronzes/">希腊与罗马世界的青铜 →</a><a href="/museum-notes/roman-sarcophagi/">古罗马浮雕石棺 →</a><a href="/museum-notes/roman-sarcophagi/stories/">人物与故事 →</a></div></section><section class="rs-reading"><h2>照片与资料</h2><p>作品照片与现场展签均为Merton摄。基本资料依据现场展签整理，背景与补充研究分别链接到馆方、遗产机构及研究资料。书目介绍与检索摘要的查阅范围另列。</p><a href="'+U+'sources/">资料、来源差异与查阅范围 →</a></section>'
 write('','泥土、青铜与永恒的宴席 · 伊特鲁里亚文明',body)
 # Reusable inline references: make handoff identifiers useful links rather than public workflow notation.
 def inline(text):
  text=re.sub(r'e(\d{3})[–—-](\d{3})',lambda m:'、'.join(f'e{n:03d}' for n in range(int(m[1]),int(m[2])+1)),text)
  text=esc(text)
  text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
  def ref(m):
   keys=re.findall(r'S\d\d',m[1]);pids=re.findall(r'p\d{3}',m[1]);wids=re.findall(r'e\d{3}',m[1]);parts=[cites(keys)] if keys else []
   if pids:parts+=[plink(pid,'现场说明' if photos.get(pid,{}).get('kind')=='panel' else '照片与展签') for pid in dict.fromkeys(pids) if pid in photos]
   if wids:parts+=[f'<a class="et-evidence" href="{U}{wid}/">{esc(by[wid]["title_zh"])}</a>' for wid in dict.fromkeys(wids) if wid in by]
   if '各自展签' in m[1]:parts.append(f'<a class="et-evidence" href="{U}photos/?kind=label">现场展签</a>')
   return ' <span class="et-inline-refs">'+' · '.join(parts)+'</span>' if parts else m[0]
  text=re.sub(r'\[([^\]]+)\]',ref,text)
  # Links are added only to bare IDs outside generated HTML attributes.
  chunks=re.split(r'(<[^>]+>)',text)
  for i in range(0,len(chunks),2):chunks[i]=re.sub(r'(?<![A-Za-z0-9])e\d{3}',lambda m:f'<a class="et-evidence" href="{U}{m[0]}/" aria-label="{esc(by[m[0]]["title_zh"])}">↗</a>' if m[0] in by else m[0],chunks[i])
  return ''.join(chunks)
 guideids=['geography','periods','cities','funerary','materials','religion','exchange','field-card','museums']
 guide=(BASE/'content/civilization-guide.md').read_text();parts=re.split(r'^## (.+)$',guide,flags=re.M)
 body=heading('认识伊特鲁里亚','让以后每一次观看，都能找到新的联系。','HISTORY &amp; LOOKING')+'<nav class="rs-chapter-nav">'+''.join(f'<a href="#{gid}">{esc(parts[i*2+1].split("、",1)[-1])}</a>' for i,gid in enumerate(guideids))+'<a href="#gods">神名</a><a href="#terms">术语</a></nav><div class="rs-reading">'
 body+='<p>'+inline('\n'.join(parts[0].splitlines()[2:]).strip())+'</p>'
 guideworks=[['e003','e054'],['e028','e122'],['e010','e063'],['e114','e112'],['e005','e035'],['e043','e084'],['e091','e126'],[],[]]
 for i,gid in enumerate(guideids):
  title,content=parts[2*i+1:2*i+3];body+=f'<section id="{gid}"><h2>{esc(title)}</h2>'
  blocks=re.split(r'\n\s*\n',content.strip())
  for block in blocks:
   if block.startswith('|'):
    rows=[line.strip().strip('|').split('|') for line in block.splitlines() if line.strip()];rows=[r for r in rows if not all(re.fullmatch(r'\s*[-:]+\s*',x) for x in r)]
    body+='<div class="et-table" tabindex="0" role="region" aria-label="对照表，窄屏可横向浏览"><table><thead><tr>'+''.join('<th>'+inline(x.strip())+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x.strip())+'</td>' for x in r)+'</tr>' for r in rows[1:])+'</tbody></table></div>'
   else:body+='<p>'+inline(block.replace('\n',' '))+'</p>'
  body+='<div class="et-mini-grid">'+''.join(mini(by[k]) for k in guideworks[i])+'</div></section>'
 body+='</div><section id="gods"><h2>神名与形象</h2><p>希腊、罗马名称帮助记忆，具体身份和故事仍需回到每件作品的展签。下列图例均为这次所见。</p><label class="et-lookup">查神名、持物或术语<input type="search" id="et-lookup" placeholder="如：护符、Vanth、bucchero"></label>'
 for i,d in enumerate(load('deities')):
  body+=f'<details data-lookup="{esc(" ".join(str(d[k]) for k in ["name","name_zh","comparison","recognition"]))}" id="god-{i+1}"><summary>{esc(d["name_zh"])} · {esc(d["name"])} <span class="rs-icon" aria-hidden="true">＋</span></summary><p>{esc(d["comparison"])}。{esc(d["recognition"])}。</p><p>{esc(d["note"])}</p><div class="et-mini-grid">'+''.join(mini(by[k]) for k in d['object_ids'])+'</div><p class="rs-meta">辨识依据见对应作品页的现场展签。</p></details>'
 body+='</section><section id="terms"><h2>遇见一个陌生词时</h2>'
 for i,d in enumerate(load('glossary')):
  body+=f'<details id="term-{i+1}" data-lookup="{esc(d["term"]+" "+d["term_zh"]+" "+d["meaning"])}"><summary>{esc(d["term_zh"])} · {esc(d["term"])} <span class="rs-icon" aria-hidden="true">＋</span></summary><p>{esc(d["meaning"])}</p>'+links(d['object_ids'])+'</details>'
 body+='</section><p class="rs-return"><a href="'+U+'">← 回到亲见作品</a>　<a href="'+U+'sources/">完整资料与查阅范围 →</a></p>'
 write('guide','认识伊特鲁里亚 · 历史与观看',body)
 # Eight comparisons with full photographs, never synthetic assembled views.
 explanations=[
 '盔盖瓮以头盔暗示身份，人首瓮把盖与腹组成简化身体，全身形瓮则让整个人形成为容器。银手原来可能依附于已失去的躯干。这些并行的做法，回答的是火化或丧葬之后，身体怎样继续可见。',
 '前三件盛放骨灰，以门、屋脊和屋身将容器变为死者的居所；末件是古代圣所奉献的神庙模型。同样的建筑形象，在家庭纪念与献神之间承担不同用途。',
 '罗得岛制作的费昂斯、腓尼基银碗、鸵鸟蛋容器、在Caere工作的希腊画家与雅典进口器，保存了不同的交流关系。原料、成品、工匠与图像并非沿着同一条已知路线流动。',
 '火盆上的动物由滚印重复，红地白绘以明亮线条展开纹带，黑色陶器则依靠器形、磨光与刻划。黑绘和红绘又将叙事放到不同的明暗关系中。牛首盒的技术记载分歧见其资料注。',
 '赠铭让器物以“我”的口吻记住赠礼；祈祷像记录奉献；油瓶排列字母与音节；suthina将器物划归墓葬。拉丁文献辞又提醒人们，语言的变化可以发生在延续的器形之上。铭文释意依据各件现场说明。',
 '赫丘勒的狮皮让人想起希腊英雄，成年英雄接受乌尼哺乳的故事，却呈现不同的神界关系。Vanth引导死者，适合从职责与持物认识，而非勉强寻找一位完全对应的希腊女神。',
 '半倚宴饮、平卧停灵、安眠般的身体和握手告别，安排了不同的纪念时间。先看躯干角度、手臂与周围人物，再问图像怎样联系生前身份、丧葬仪式和死后期待。',
 '男子头像的个体面貌、罗马姓名与拉丁文献辞、公元1世纪的Veiovis，以及圣所还愿的身体形象，分别显示语言、政治身份与地方实践的变化。它们的速度并不整齐一致。']
 body=heading('让器物彼此照见','沿身体、房屋、文字与交流，重看同一次展览。','SIDE BY SIDE')+'<p class="rs-meta">图片保持完整比例；并排不表示实物等大。各件来源与断代见详情页。</p><nav class="rs-chapter-nav">'+''.join(f'<a href="#{g["id"]}">{esc(g["title"])}</a>' for g in groups)+'</nav>'
 for g,t in zip(groups,explanations):
  body+=f'<section class="compare-group rs-comparison" id="{g["id"]}"><header class="rs-section-title"><h2>{esc(g["title"])}</h2><p>{esc(t)}</p></header><div class="et-comparison-grid">'
  for wid in g['object_ids']:
   w=by[wid];body+='<div>'+figure(cover(w),cap=w['title_zh']+' · '+date(w),limit=420)+f'<p class="rs-meta">{esc(cname(w))}</p><a href="{U}{wid}/">资料、展签与完整照片 →</a></div>'
  body+='</div></section>'
 write('compare','八组并看 · 伊特鲁里亚',body)
 # Catalogue uses one object dataset for facets and dated range rows.
 body=heading('所见器物','从城市、年代与用途，重新组织这次观看。','ATLAS & TIMELINE')+mapview()
 body+='<section id="filters" class="et-filters" aria-label="筛选图录"><label>名称、地名或馆藏号<input id="et-search" type="search" placeholder="如：金镯、Caere、Cp5193"></label>'
 facets=[('place','地点关系',[(p['id'],p['name_zh']) for p in places]+[('unknown','地域未详')]),('collection','收藏机构',[(k,v.split(' / ')[0]) for k,v in collections.items()]),('material','材料',[(k,k) for k in sorted({material(w) for w in works})]),('function','用途',list(taxonomy.items())),('chapter','章节',[(c['id'],c['title_zh']) for c in chapters]),('deep','阅读层次',[('yes','有独立细读'),('no','基本资料')])]
 for key,title,options in facets:body+=f'<label>{title}<select data-filter="{key}"><option value="all">全部</option>'+''.join(f'<option value="{esc(k)}">{esc(v)}</option>' for k,v in options)+'</select></label>'
 body+='<label>年代从<input data-filter="start" type="number" min="-1000" max="100" placeholder="-900"></label><label>年代至<input data-filter="end" type="number" min="-1000" max="100" placeholder="100"></label><label>排序<select id="et-sort"><option value="chapter">章节顺序</option><option value="date">年代由早至晚</option><option value="collection">收藏机构</option></select></label><button type="button" id="et-reset">清除条件</button><p class="rs-meta">负数表示公元前。年代按区间相交筛选；收藏机构是出借方或本馆，并不表示此次逐馆到访。</p><p id="et-results" role="status" aria-live="polite"></p></section>'
 body+='<details id="timeline" class="et-timeline"><summary>沿制作年代重看 <span class="rs-icon" aria-hidden="true">＋</span></summary><p>横线保留展签年代范围，圆点表示单年；约年以虚线表示。每条记录独占一行，手机可横向浏览。</p><div class="et-time-scroll" tabindex="0" role="region" aria-label="年代时间线，可横向浏览"><div class="et-time-axis"><span>器物与年代</span><div>'
 for year in range(-900,101,100):body+=f'<b style="left:{(year+900)/1000*100}%">{("前"+str(-year)) if year<0 else ("纪元" if year==0 else str(year))}</b>'
 body+='</div></div>'
 for w in sorted(works,key=lambda w:w['date_start']):
  left=(w['date_start']+900)/1000*100;width=(w['date_end']-w['date_start'])/1000*100
  body+=f'<a class="et-time-row" data-time-record="{w["id"]}" href="{U}{w["id"]}/"><span>'+img(cover(w),sizes='56px')+'<span>'+esc(w['title_zh'])+'<small>'+esc(date(w))+'</small></span></span><div><i class="'+('approx' if w['date_is_approximate'] else '')+f'" style="left:{left}%;width:{max(.35,width)}%"></i></div></a>'
 body+='</div><p class="rs-meta">“纪元”仅表示公元前后分界，不另设公元0年。</p></details><details><summary>另一个时间：现代发现 <span class="rs-icon" aria-hidden="true">＋</span></summary><div class="et-modern">'
 modern={'1836':('Regolini–Galassi墓发现。不同葬式与奢侈器物在同墓相遇。',['S04'],None),'2010':('Hinthial供养青年于2010—2011年的考古发现中重见天日。',['S12'],None),'2012':('银手墓发现；随后由意大利中央修复研究所开展研究与修复。',['S11'],'p317'),'2022':('San Casciano dei Bagni温泉圣所的青铜发现，引出新的疗愈与奉献研究。',['S14'],'p373')}
 for t in timeline:
  if t['kind']!='modern_discovery':continue
  desc,keys,pid=modern[str(t['start'])];body+=f'<section><h3>{("2010—2011" if t["start"]==2010 else t["start"])} · {esc(t["title"])}</h3><p>{esc(desc)}{cites(keys)}'+(' '+plink(pid) if pid else '')+'</p>'+links(t['object_ids'])+'</section>'
 body+='</div></details><section id="catalogue"><h2>完整图录</h2><p>一条记录可以包含成组器物或一件构件；角度、局部与共用展签分别关联。全部{record_count}条均有现场照片。</p><p id="et-empty" hidden>没有符合当前条件的记录。</p><div class="rs-grid et-record-grid">'+''.join(card(w,True) for w in works)+'</div></section>'
 write('atlas','所见器物 · 地图与年代',body)
 # All 377 images have a stable archive anchor; labels and wall texts remain photographs, not OCR transcriptions.
 body=heading('现场档案','完整作品、展签、展墙与展陈环境，各自留下观看的依据。','PHOTOGRAPHS & LABELS')+'<p>{photo_count}张原始照片；共享照片只保存一次。点击图片查看大图，原始文件可从查看器打开。</p><label class="et-lookup">照片类型<select id="et-photo-kind"><option value="all">全部</option>'+''.join(f'<option value="{k}">{v}</option>' for k,v in kind.items())+'</select></label><p id="et-photo-count" role="status"></p>'
 for p in load('photos'):
  pid=p['photo_id'];matching=next((x for x in panels if x['photo_id']==pid),None)
  body+=f'<details id="{pid}" data-photo-kind="{p["kind"]}"><summary>{esc(caption(pid))} <small>{kind[p["kind"]]}</small><span class="rs-icon" aria-hidden="true">＋</span></summary>'
  if matching:body+='<p>'+esc(matching['summary_zh'])+'</p>'
  body+=figure(pid)+'<div class="rs-link-row">'+''.join(f'<a href="{U}{x["object_id"]}/">{esc(by[x["object_id"]]["title_zh"])} →</a>' for x in p['links'] if x.get('object_id') in by)+'</div></details>'
 write('photos','现场照片与展签档案',body)
 # Source provenance is explicit: no whole catalogue is implied read.
 body=heading('资料与来源','先从现场展签确认这件器物，再以馆录与研究扩展理解。','SOURCES & RESEARCH')+'<div class="rs-reading"><p>{record_count}条记录以现场照片和对应展签为基本依据。背景文字综合资料包中的研究与本轮补充核对；少数链接仅取得检索摘要、馆方元数据或书目说明，分别注明。展览图录未阅读全文。</p><p>“伊特鲁里亚”见于大英博物馆中文导览和中文展览资料；普通器物名与描述性题名采用中文译写，英文保留展签原名。地名、神名采用查到的中文用法，并保留原文对照；尚未核实中文译名的专名则沿用原名。</p>'
 for s in sources:
  level=s['checked_level'];status='已读网页正文' if level.endswith('full_page') else ('仅核对书目介绍，未读全书' if 'catalogue' in level else ('仅核对馆方元数据' if 'metadata' in level else ('仅核对官方视频说明，未观看全片' if 'video' in level else '仅取得检索摘要／部分记录')))
  body+=f'<section id="{s["id"]}"><h2><small>[{int(s["id"][1:])}]</small> {esc(s["institution"])}</h2><p><a href="{esc(s["url"])}">{esc(s["title"])} ↗</a></p><p class="rs-meta">{status}</p><p>{esc(s["usage_note"])}</p></section>'
 body+='<section id="differences"><h2>仍待核实的几处资料</h2><ul>'+''.join(f'<li><a href="{U}{wid}/">{esc(by[wid]["title_zh"])}</a>：{esc(notes[wid])}</li>' for wid in ['e035','e083','e085','e105','e072','e130','e131'])+'</ul></section><section><h2>照片与地图</h2><p>照片为Merton在2026年11月于圣安东尼奥美术馆特展中拍摄。图注中的“原片局部”表示由现场照片裁切；查看器同时提供完整原图。</p><p>地图底图及台伯河数据来自Natural Earth，公共领域。点位为城市或遗址区域的近似定位，不是发掘测绘数据；未有坐标的地名仍可通过图录筛选。</p></section></div>'
 names=load('naming-review')['verified_proper_names']
 body+='<details class="rs-reading et-naming"><summary>中文专名用例 <span class="rs-icon" aria-hidden="true">＋</span></summary><p>以下资料用于核对名称的中文写法；考古背景与单件释读仍据各自馆录。</p><ul>'+''.join('<li>'+esc(n['chinese'])+'（'+esc(n['original'])+'） · <a href="'+esc(n['url'])+'">中文名称用例</a>'+('（检索摘要）' if n['read_scope'].startswith('search') else '')+'</li>' for n in names)+'</ul></details>'
 write('sources','资料与来源 · 伊特鲁里亚',body)
 # Idempotent neighbouring-topic links are applied last by the full notebook build.
 home=ROOT/'museum-notes/index.html';text=home.read_text();text=re.sub(r'<!-- etruscan-entry -->.*?<!-- /etruscan-entry -->','',text,flags=re.S)
 entry='<!-- etruscan-entry --><a class="issue-link" href="etruscans/">'+img('p003',sizes='(max-width:650px) 90vw, 480px',alt='狮首饰青铜大釜 · 伊特鲁里亚专题')+'<div><p class="eyebrow">ANCIENT ITALY / ETRUSCANS</p><h2>泥土、青铜与永恒的宴席</h2><p>伊特鲁里亚文明的现场观看。从五件初见最爱，走向城邦、工艺、葬俗与祈愿。</p><p class="issue-meta">圣安东尼奥所见 · {record_count}条记录 · {reading_count}篇细读<br>文明导读 / 地图与年代 / 八组并看</p><span class="text-link">走进这个专题 →</span></div></a><!-- /etruscan-entry -->'
 entry=entry.replace('{record_count}',str(len(works))).replace('{reading_count}',str(len(reads)))
 anchor='<!-- /bronze-entry -->';assert anchor in text;text=text.replace(anchor,anchor+entry,1);home.write_text(text)
 for rel in ['greek-roman-bronzes/index.html','roman-sarcophagi/index.html','roman-sarcophagi/stories/index.html']:
  p=ROOT/'museum-notes'/rel;t=p.read_text();t=re.sub(r'<!-- etruscan-related -->.*?<!-- /etruscan-related -->','',t,flags=re.S)
  t=t.replace('</main>','<!-- etruscan-related --><aside class="rs-guide-entry"><h2>再向伊特鲁里亚看一眼</h2><p>相近的英雄、青铜身体与宴饮形象，在古代意大利的地方传统中又有不同用途。</p><a href="'+U+'">泥土、青铜与永恒的宴席 →</a></aside><!-- /etruscan-related --></main>',1);p.write_text(t)
 print(f'Built Etruscans: {len(works)} records, {len(reads)} readings, {photo_count} photographs; 6 guide/index pages.')
def chapter_guide(chapter):return {'luxury':'exchange','origins':'funerary','pottery':'materials','gods-writing':'religion','adornment':'cities','banquet':'exchange','temples':'materials','afterlife':'funerary','rome-healing':'exchange'}[chapter]
if __name__=='__main__':build()
