"""Build the early Buddhist notebook from canonical data; no network or source archive required."""
from pathlib import Path
from html import escape as e
import json,re
from PIL import Image,ImageOps
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'museum-notes/early-buddhist-art'
def build():
 read=lambda f:json.loads((B/'data'/f).read_text())
 works=read('works.json');by={w['id']:w for w in works};units=read('readings.json');chapters=read('chapters.json');sources=read('sources.json');photos=read('photos.json');photo_by={p['asset_id']:p for p in photos};geo=read('map.json');museums={m['id']:m for m in geo['museums']};places={p['id']:p for p in geo['places']}
 used={n for w in works for n in w['photos']+w['labels']};manifest={}
 for n in sorted(used):
  p=photo_by[n];src=B/'images/originals'/p['original_filename'];im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
  # Label 1418 was photographed sideways. Rotate only the display derivative, never its archived JPEG.
  if n=='1418':im=im.rotate(90,expand=True)
  variants=[]
  for size in [400,900,1600]:
   iw=min(im.width,size);ih=round(im.height*iw/im.width);dest=B/'images'/f'{n}-{size}.webp'
   if not dest.exists():im.resize((iw,ih),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=86,method=6)
   variants.append({'path':str(dest.relative_to(B)),'width':iw,'height':ih})
  # Full-resolution viewer uses a correctly oriented image, with no crop or upscaling.
  full=B/'images'/f'{n}-full.webp'
  if not full.exists():im.save(full,'WEBP',quality=94,method=6)
  manifest[n]={'width':im.width,'height':im.height,'variants':variants,'full':str(full.relative_to(B)),'original':'images/originals/'+p['original_filename'],'sha256':p['sha256']}
 for crop in read('crops.json'):
  src=B/manifest[crop['source_photo']]['original'];im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
  box=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(crop['box']));im=im.crop(box);vs=[]
  for size in [400,900,1600]:
   iw=min(size,im.width);ih=round(im.height*iw/im.width);dest=B/'images'/f'{crop["id"]}-{size}.webp'
   if not dest.exists():im.resize((iw,ih),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=87,method=6)
   vs.append({'path':str(dest.relative_to(B)),'width':iw,'height':ih})
  full=B/'images'/f'{crop["id"]}-full.webp'
  if not full.exists():im.save(full,'WEBP',quality=94,method=6)
  manifest[crop['id']]={'width':im.width,'height':im.height,'variants':vs,'full':str(full.relative_to(B)),'original':manifest[crop['source_photo']]['original'],'source_photo':crop['source_photo'],'crop_box':box}
 (B/'data/derivatives.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 def collection(w):
  if w['private_collection']:
   name='虚舟收藏' if 'Xuzhou' in w['private_collection'] else w['private_collection']
   return name+(' · 在'+museums[w['viewing_museum']]['name_zh']+'展出' if w['viewing_museum'] else ' · 展出机构未详')
  return museums[w['collection_museum']]['name_zh'] if w['collection_museum'] else '收藏机构未详'
 def caption(w):return w['title']+' · '+w['date']+' · '+w['material']+'｜'+collection(w)+((' · '+w['accession']) if w['accession'] else '')
 def img(n,alt,pre='',high=False,small=False):
  m=manifest[n];v=m['variants'];ss=', '.join(pre+x['path']+' '+str(x['width'])+'w' for x in {x['width']:x for x in v}.values())
  sizes='(max-width: 680px) 43vw, 300px' if small else '(max-width: 680px) calc(100vw - 40px), (max-width: 1100px) 80vw, 780px'
  return f'<img src="{pre}{v[0 if small else 1]["path"]}" srcset="{ss}" sizes="{sizes}" width="{m["width"]}" height="{m["height"]}" alt="{e(alt)}" decoding="async" '+('fetchpriority="high"' if high else 'loading="lazy"')+'>'
 def figure(n,cap,pre='',high=False,cls=''):
  m=manifest[n];return f'<figure class="eb-figure {cls}" style="--ratio:{m["width"]/m["height"]:.5f};--native:{m["width"]}px"><a data-photo href="{pre}{m["full"]}" data-caption="{e(cap)}">{img(n,cap,pre,high)}</a><figcaption>{e(cap)}</figcaption></figure>'
 def mini(w,pre='',direct=False):
  href=(pre+w['units'][0]+'/#'+w['id']) if w['units'] and not direct else pre+'#'+w['id']
  return f'<a class="eb-mini" href="{href}">{img(w["photo"],w["title"],pre,small=True)}<span>{e(w["title"])}<small>{e(w["date"])}</small></span></a>'
 def shell(title,body,depth=0):
  pre='../'*depth;note='../'*(depth+1)
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="从佛塔栏楯到笈多造像，沿着亲见照片比较身体、衣纹、礼拜与佛传故事。"><link rel="stylesheet" href="{note}museum.css"><link rel="stylesheet" href="{note}caravaggio/caravaggio.css"><link rel="stylesheet" href="{pre}early-buddhist.css"><script src="{note}caravaggio/caravaggio.js" defer></script><script src="{pre}early-buddhist.js" defer></script></head><body class="eb-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{note}">Merton</a><nav aria-label="主导航"><a href="{pre or './'}">早期佛教艺术</a><a href="{pre}#places">地域导览</a><a href="{pre}#catalogue">亲见目录</a></nav></header><main id="main" class="wrap">{body}</main><footer class="site-footer wrap"><a href="{note}south-asian-art/">← 南亚艺术</a><span>现场摄影与札记 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
 def refs(keys,pre='',labels=None):
  out='<section class="eb-sources"><h2>资料与来源</h2><ol>'
  for i,k in enumerate(keys):s=sources[k];out+=f'<li id="source-{k}"><a href="{e(s["url"])}">{e(s["title"])} ↗</a></li>'
  out+='</ol>'
  if labels:out+='<details><summary>现场展签</summary><div class="eb-labels">'+''.join(figure(n,'现场展签 · '+', '.join(dict.fromkeys(by[w]['title'] for w in labels[n])),pre) for n in labels)+'</div></details>'
  return out+'</section>'
 def facts(w,pre='',link=True):
  fields=[('原题名',w['title_original']),('年代',w['date']),('材料',w['material']),('尺寸',w['dimensions']),('编号',w['accession']),('收藏／展出',collection(w)),('地域关系',w['place_relation'])]
  html='<dl class="eb-facts">'+''.join('<dt>'+k+'</dt><dd>'+e(v)+'</dd>' for k,v in fields if v)+'</dl>'
  if w['sources']:html+='<p class="eb-note">'+ ' · '.join(f'<a href="{e(sources[k]["url"])}">馆藏／研究 [{i+1}] ↗</a>' for i,k in enumerate(w['sources']))+'</p>'
  if w['notes']:html+='<div class="eb-note">'+''.join('<p>'+e(n)+'</p>' for n in w['notes'])+'</div>'
  return html
 # Static geographic maps: same offline Natural Earth land as the existing Homer notebook.
 land=json.loads((ROOT/'museum-notes/homer/data/ne_110m_land.geojson').read_text())
 rivers=read('rivers.geojson')
 def svg(mode):
  bounds=(62,90,9,40) if mode=='ancient' else (-175,15,10,57);xmin,xmax,ymin,ymax=bounds;ww,hh=(690,550) if mode=='ancient' else (900,420)
  xy=lambda lon,lat:((lon-xmin)/(xmax-xmin)*ww,(ymax-lat)/(ymax-ymin)*hh)
  paths=[]
  for f in land['features']:
   g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
   for rings in polys:
    pts=rings[0]
    if max(a[0] for a in pts)<xmin or min(a[0] for a in pts)>xmax or max(a[1] for a in pts)<ymin or min(a[1] for a in pts)>ymax:continue
    paths.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{xy(*p)[0]:.1f},{xy(*p)[1]:.1f}' for i,p in enumerate(pts))+' Z"/>')
  markers=[];river_html=''
  if mode=='ancient':
   river_paths=[]
   for f in rivers['features']:
    for line in f['geometry']['coordinates']:
     river_paths.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{xy(*p)[0]:.1f},{xy(*p)[1]:.1f}' for i,p in enumerate(line))+'"/>')
   river_labels=[]
   for name,lon,lat in [('印度河',69.8,29.8),('恒河',84.8,27.4),('克里希纳河',76.9,18.2)]:
    x,y=xy(lon,lat);river_labels.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{name}</text>')
   river_html='<g class="eb-rivers" clip-path="url(#clip-ancient)" role="img" aria-label="印度河、恒河与克里希纳河的现代河道示意">'+''.join(river_paths)+'</g><g class="eb-river-labels" aria-hidden="true">'+''.join(river_labels)+'</g>'
   offsets={'bharhut':(35,40),'mathura':(-55,-25),'sarnath':(40,0),'hadda':(-50,-35),'andhra':(35,0),'gandhara':(60,-15),'north-india':(50,-10),'amaravati':(65,25),'gummadidurru':(65,-68),'nagarjunakonda':(-75,15),'takht-i-bahi':(65,10)}
   for p in geo['places']:
    coord=p['coordinate'] or p.get('label_position')
    if not coord:continue
    x,y=xy(*coord);dx,dy=offsets.get(p['id'],(0,0));lx,ly=x+dx,y+dy;region=p['coordinate'] is None;cl='eb-region' if region else 'eb-point'
    markers.append(f'<a class="{cl}" href="#place-{p["id"]}" data-map-key="{p["id"]}" aria-label="{e(p["name_zh"])}：查看相关作品"'+(f' data-child-of="{p["parent"]}"' if p.get('parent') else '')+'>'+('' if region else f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{lx:.1f}" y2="{ly:.1f}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5"/>')+f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle">{e(p["name_zh"])}</text></a>')
   country='<g class="eb-country"><text x="60" y="45">阿富汗</text><text x="145" y="215">巴基斯坦</text><text x="390" y="350">印度</text><text x="70" y="420">阿拉伯海</text><text x="560" y="430">孟加拉湾</text></g>'
  else:
   # City-level callouts prevent the East Coast and Texas museum points from overlapping.
   pos={'guimet':(825,55),'carlos':(440,270),'dma':(300,220),'met':(650,115),'cma':(455,55),'nmaa':(620,190),'walters':(650,245),'mfah':(350,330),'sam':(190,30),'pam':(175,105),'nelson':(335,135),'kimbell':(210,295),'homa':(72,370)}
   for m in geo['museums']:
    if not any(w['museum_map']==m['id'] for w in works):continue
    x,y=xy(*m['coordinate']);lx,ly=pos[m['id']]
    markers.append(f'<a href="#museum-{m["id"]}" data-map-key="{m["id"]}" aria-label="{e(m["name_zh"])}"><line x1="{x:.1f}" y1="{y:.1f}" x2="{lx}" y2="{ly}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="4"/><text x="{lx}" y="{ly}" text-anchor="middle">{e(m["city"])}</text></a>')
   country=''
  return f'<svg viewBox="0 0 {ww} {hh}" role="group" aria-label="'+('古代地域参考地图' if mode=='ancient' else '现代馆藏与借展的城市参考地图')+f'"><defs><clipPath id="clip-{mode}"><rect width="{ww}" height="{hh}"/></clipPath></defs><g class="eb-land" clip-path="url(#clip-{mode})">'+''.join(paths)+'</g>'+river_html+country+'<g class="eb-map-pins">'+''.join(markers)+'</g></svg>'
 def place_matches(w,p):return w['place']==p or places[w['place']].get('parent')==p
 maphtml='<section id="places" class="eb-section"><p class="eyebrow">PLACES &amp; IMAGES</p><h2>从地域走近作品</h2><p class="eb-prose">同一个马图拉，既有贵霜时期的坐佛，也有笈多时期的立像。地图上的位置是阅读的起点；点选地域，再看材料、年代与作品之间的差别。</p><div class="eb-map-controls" hidden><div role="group" aria-label="地图图层"><button data-layer="ancient" aria-pressed="true">古代地域</button><button data-layer="modern" aria-pressed="false">今日馆藏／借展</button></div><label>年代 <select id="eb-period">'+''.join(f'<option value="{p["id"]}">{p["label"]}</option>' for p in geo['periods'])+'</select></label><label><input type="checkbox" id="eb-featured"> 只看正文作品</label></div><div class="eb-map-layout"><div><div data-map-layer="ancient" class="eb-map">'+svg('ancient')+'</div><div data-map-layer="modern" class="eb-map" hidden>'+svg('modern')+'</div><p class="eb-note">实点为遗址或城市参考位置，斜体区域名不代表精确出土地。现代国名与河道用于方位参照。<a href="#map-sources">Natural Earth · 地图资料 ↓</a></p><nav class="eb-place-buttons" aria-label="古代地域">'+''.join(f'<a href="#place-{p["id"]}" data-select-place="{p["id"]}">{p["name_zh"]}</a>' for p in geo['places'])+'</nav><nav class="eb-museum-buttons" aria-label="今日馆藏" hidden>'+''.join(f'<a href="#museum-{m["id"]}" data-select-museum="{m["id"]}">{m["name_zh"]}</a>' for m in geo['museums'])+'<a href="#museum-unlocated" data-select-museum="unlocated">地点未详</a></nav></div><div id="eb-map-result" class="eb-map-result" hidden aria-live="polite"></div></div><div class="eb-map-fallback"><details><summary>按地域查找作品</summary>'
 for p in geo['places']:
  ws=[w for w in works if place_matches(w,p['id'])]
  maphtml+=f'<section id="place-{p["id"]}"><h3>{p["name_zh"]} <small>{p["name_en"]}</small></h3><p>{p["description"]}</p><ul>'+''.join(f'<li><a href="#{w["id"]}">{w["title"]}</a> · {w["date"]} · {collection(w)}</li>' for w in ws)+'</ul></section>'
 maphtml+='</details><details><summary>按今日馆藏／借展查找作品</summary>'
 for m in geo['museums']+[{'id':'unlocated','name_zh':'地点未详'}]:
  ws=[w for w in works if (w['museum_map'] or 'unlocated')==m['id']]
  maphtml+=f'<section id="museum-{m["id"]}"><h3>{m["name_zh"]}</h3><ul>'+''.join(f'<li><a href="#{w["id"]}">{w["title"]}</a> · {collection(w)}</li>' for w in ws)+'</ul></section>'
 maphtml+='</details></div><p class="eb-note">年代按范围相交筛选；私人借展以实际展出馆定位，与永久馆藏分别标注。未确定的原址仍可从目录阅读。</p></section>'
 intro='<nav class="breadcrumbs" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../south-asian-art/">南亚艺术</a></nav><header class="eb-heading"><p class="eyebrow">EARLY BUDDHIST ART</p><h1>早期佛教艺术</h1><p>从早期佛塔艺术到笈多及其余绪——我的亲见作品录</p></header>'+figure('1351',caption(by['w1351'])+' · Merton摄',high=True,cls='eb-hero')+'<div class="eb-intro"><p class="eb-personal-preface">'+e(read('introduction.json')['preface'])+'</p><p class="eb-scope">'+e(read('introduction.json')['scope'])+'</p></div>'
 chapter_intros={'stupa':'沿着栏楯与佛塔，先看礼拜发生的地方。','images':'同是佛与菩萨，身体、袈裟和装束有不同的表达。','stories':'树、宫殿、山洞与人群，让石面上的故事继续展开。','late':'泥与灰泥构成面容，也把人物带入龛和塔的空间。','gupta':'马图拉与鹿野苑并看，再由铜像和供养铭文收束。'}
 nav='<nav class="eb-chapter-nav" aria-label="五章细读">'+''.join(f'<a href="#chapter-{c["id"]}"><small>0{i+1}</small><span>{e(c["title"])}</span></a>' for i,c in enumerate(chapters))+'</nav>'
 body=intro+maphtml+nav
 for i,c in enumerate(chapters):
  body+=f'<section id="chapter-{c["id"]}" class="eb-section eb-chapter"><header><p class="eyebrow">CHAPTER 0{i+1}</p><h2>{e(c["title"])}</h2><p>{chapter_intros[c["id"]]}</p></header><div class="eb-readings">'
  for j,r in enumerate(u for u in units if u['chapter']==c['id']):
   w=by[r['works'][0]];large=r['id'] in ['u03','u04','u07','u09','u15','u17']
   body+=f'<article class="eb-reading {"eb-wide" if large else ""}" id="reading-{r["id"]}"><a class="eb-reading-photo" href="{r["id"]}/">'+img(w['photo'],caption(w))+'</a><div><p class="eyebrow">'+r['id'][1:]+' / 细读</p><h3><a href="'+r['id']+'/">'+e(r['title'])+'</a></h3><p>'+e(r['teaser'])+'</p><p class="eb-note">'+e(w['title'])+' · '+e(w['date'])+'</p><a class="text-link" href="'+r['id']+'/">展开照片与札记 →</a></div></article>'
  body+='</div><p class="eb-return"><a href="#places">回到地域导览 ↑</a></p></section>'
 body+='<section class="eb-section" id="catalogue"><p class="eyebrow">THE VIEWING RECORD</p><h2>完整亲见目录</h2><p class="eb-prose">'+str(len(works))+'条作品记录。多次拍摄合并，同框作品分别登记；一对手沿用馆方的成组编号。</p><details id="eb-catalogue"><summary>展开目录 · 按地域、年代或馆藏查找</summary><div class="eb-catalogue-controls" hidden><label>搜索 <input id="eb-search" type="search" placeholder="题名、材料、馆号"></label><label>地域 <select id="eb-region-filter"><option value="all">全部</option>'+''.join(f'<option value="{p["id"]}">{p["name_zh"]}</option>' for p in geo['places'])+'</select></label><label>馆藏／展出 <select id="eb-museum-filter"><option value="all">全部</option>'+''.join(f'<option value="{m["id"]}">{m["name_zh"]}</option>' for m in geo['museums'])+'<option value="unlocated">地点未详</option></select></label><label>年代 <select id="eb-date-filter">'+''.join(f'<option value="{p["id"]}">{p["label"]}</option>' for p in geo['periods'])+'<option value="unknown">年代未详</option></select></label><button id="eb-reset">重置</button><p id="eb-count" role="status"></p></div><div class="eb-catalogue-grid">'
 for w in works:
  cap=caption(w)+((' · '+w['photo_caption']) if w.get('photo_caption') else '')
  body+=f'<article class="eb-work" id="{w["id"]}" data-work="{w["id"]}">'+figure(w.get('catalogue_photo',w['photo']),cap+(' · 单件裁切' if w.get('catalogue_photo') else ''))+f'<h3>{e(w["title"])}</h3><p class="eb-note">{e(w["date"])} · {e(w["material"])}</p><p class="eb-note">{e(collection(w))}'+((' · '+e(w['accession'])) if w['accession'] else '')+'</p>'
  if w['units']:body+='<p>'+ ' · '.join(f'<a href="{uid}/#{w["id"]}">细读 {uid[1:]} →</a>' for uid in w['units'])+'</p>'
  body+=f'<button class="eb-map-work" data-focus-work="{w["id"]}" hidden>在地图中选中</button><span class="eb-map-status"></span><details><summary>作品资料与现场展签</summary>'+facts(w)
  body+=(f'<p><a data-photo href="{manifest[w["photo"]]["full"]}" data-caption="同框现场全景 · {e(w["photo_caption"])}">同框完整照片 ↗</a></p>' if w.get('catalogue_photo') else '')
  body+='<p class="eb-note">'+ ' · '.join(f'<a data-photo href="{manifest[n]["full"]}" data-caption="{e(w["title"])} · 现场展签">现场展签'+(str(i+1) if len(w['labels'])>1 else '')+' ↗</a>' for i,n in enumerate(w['labels']))+'</p></details></article>'
 body+='</div><p id="eb-empty" hidden>没有符合条件的作品。</p></details></section>'
 body+='<section class="eb-section" id="map-sources"><h2>地域与资料</h2><details><summary>地图的坐标与阅读方式</summary><p>遗址点表示地理参考，作品与它的关系仍以每条作品资料为准。哈达是寺院群；龙树山点位表示古代遗址区域，不能当作现代岛上博物馆内某件雕塑的出土坐标。Shahbaz Garhi 的具体点位暂不绘制，相关寺院关系保留在列表。</p><ul><li>底图：<a href="https://www.naturalearthdata.com/about/terms-of-use/">Natural Earth，公共领域陆地数据</a>，离线使用；不绘制古代政权边界。</li><li>河道：<a href="https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-rivers-lake-centerlines/">Natural Earth 1:10m Rivers + lake centerlines，5.0.0</a>，公共领域；选取印度河、恒河与克里希纳河，以0.02度容差简化。这里显示现代地理参照，不复原古代河道。</li><li>巴尔胡特：<a href="https://jatakastories.div.ed.ac.uk/artistic-sites/bharhut">爱丁堡大学 Jātaka Stories 遗址记录</a>。</li><li>马图拉、鹿野苑：Getty TGN <a href="https://www.getty.edu/vow/TGNFullDisplay?find=Mathura&place=&nation=&subjectid=7001569">7001569</a>、<a href="https://www.getty.edu/vow/TGNFullDisplay?find=Sarnath&place=&nation=&subjectid=7001588">7001588</a>的地域参考点。</li><li>阿马拉瓦蒂、Gummadidurru：<a href="https://ignca.gov.in/Asi_data/50352.pdf">Debala Mitra，《Buddhist Monuments》，第200、212页</a>刊载的分级坐标。</li><li>龙树山：<a href="https://www.museumsofindia.gov.in/repository/museum/nkm_hyd">印度考古调查局馆舍与遗址说明</a>；哈达：<a href="https://chre.ashmus.ox.ac.uk/hoard/18819">牛津 Ashmolean CHRE 地点参考</a>（取村镇位置，不用于推断雕像出土点）；塔克特依巴依：<a href="https://whc.unesco.org/en/list/140/maps/">UNESCO 遗产地图</a>。</li><li>今日馆藏图使用城市级近似位置；不表示作者的旅行先后，也不把私人收藏称为展出馆永久藏品。</li></ul></details><p>作品资料据现场展签及各篇链接的馆藏记录整理。照片均为 Merton 现场拍摄。</p></section>'
 # Chinese alternatives belong in the reference area, without lengthening every label.
 naming='<details id="place-names"><summary>地名与中文异译</summary><p>马图拉亦作秣菟罗，鹿野苑亦称萨尔纳特。两组写法可对照程金城《丝绸之路艺术史纲（下）》第23页及复旦大学的佛教艺术史讲座介绍；本辑沿用马图拉与鹿野苑。<a href="https://dflt.qdu.edu.cn/__local/5/13/81/653A67520AC2ED8DDBD5465361F_5065BE5C_16AF65.pdf">《东方论坛》论文 ↗</a> · <a href="https://clcrr.fudan.edu.cn/Data/View/214">复旦大学讲座介绍 ↗</a></p><p>阿马拉瓦蒂见于大英博物馆中文导览；巴尔胡特见于复旦大学的佛塔研究讲座纪要。龙树山与犍陀罗的写法见《紫禁城》所刊《犍陀罗艺术引介》，该文将 Amaravati 写作阿玛拉瓦蒂。<a href="https://britishmuseum.org.cn/G_33a.html">大英博物馆：阿马拉瓦蒂 ↗</a> · <a href="https://clcrr.fudan.edu.cn/Data/View/260">复旦大学：早期印度佛塔象征含义研究 ↗</a> · <a href="https://www.dpm.org.cn/Uploads/File/2023/05/08/u6458b201c3473.pdf">《犍陀罗艺术引介》，第30页 ↗</a></p><p>哈达、塔帕—卡兰采用吉美博物馆中文页面的译名；塔克特依巴依采用联合国教科文组织中文遗产条目的名称。Shahbaz Garhi、Gummadidurru、Mekhasanda、Dhanesar Khera 保留原文，以便与馆藏及考古记录对应。<a href="https://www.guimet.fr/zh-hans/nos-collections/afghanistan-pakistan/le-genie-aux-fleurs">吉美博物馆：持花精灵 ↗</a> · <a href="https://whc.unesco.org/zh/list/140">UNESCO：塔克特依巴依佛教遗址 ↗</a></p></details>'
 end=body.rfind('</section>');body=body[:end]+naming+body[end:]
 # Keep the serialised UI payload free from image bytes and editorial intake flags.
 payload={'works':[dict(w,collection_display=collection(w),thumbnail=manifest[w.get('catalogue_photo',w['photo'])]['variants'][0]['path']) for w in works],'map':geo}
 body+='<script type="application/json" id="eb-data">'+json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')+'</script>'
 (B/'index.html').write_text(shell('早期佛教艺术',body))
 # Eighteen reading pages, all facts supplied by the same object records as the catalogue/map.
 for idx,r in enumerate(units):
  keys=r['sources'];numbers={k:i+1 for i,k in enumerate(keys)};pre='../';c=next(c for c in chapters if c['id']==r['chapter'])
  article=f'<nav class="breadcrumbs"><a href="../">早期佛教艺术</a><span>/</span><a href="../#chapter-{c["id"]}">{e(c["title"])}</a></nav><header class="eb-heading"><p class="eyebrow">{r["id"][1:]} / {e(c["title"])}</p><h1>{e(r["title"])}</h1><p>{e(r["teaser"])}</p></header>'
  mainphotos=r['primary_photos'][:r['show_first']]
  article+='<div class="eb-plates compare-group">'+''.join(figure(n,caption(next(by[wid] for wid in r['works'] if by[wid]['photo']==n)),pre,high=i==0) for i,n in enumerate(mainphotos))+'</div>'
  if len(r['works'])>1:
   scale='全图与局部均各自缩放，每组局部对应同一身体部位，并非实物等比例；实际残高见下方资料表。' if r['id']=='u17' else '图片各自缩放，非实物等比例；尺寸见作品资料。'
   article+='<p class="eb-note eb-scale">'+scale+'</p>'
  article+='<div class="eb-prose eb-body">'
  for i,p in enumerate(r['paragraphs']):
   # A short citation points to the unit's evidence list rather than repeating full titles.
   cites=''
   paragraph_keys=r.get('paragraph_sources',{}).get(str(i),keys if i==1 else [])
   if paragraph_keys:cites=' <span class="eb-cites">'+''.join(f'<a href="#source-{k}" aria-label="资料{numbers[k]}">[{numbers[k]}]</a>' for k in paragraph_keys)+'</span>'
   if i==1 and not keys:cites=' <a class="eb-cites" href="#object-records">[现场展签]</a>'
   article+='<p>'+e(p)+cites+'</p>'
   for group in r.get('detail_groups',[]):
    if group['after_paragraph']!=i:continue
    article+='</div><section class="eb-details" id="detail-'+group['id']+'"><h2>'+e(group['title'])+'</h2>'
    if group.get('note'):
     cite=f' <a href="#source-{group["source"]}" class="eb-cites">[{numbers[group["source"]]}]</a>' if group.get('source') else ''
     article+='<p class="eb-note">'+e(group['note'])+cite+'</p>'
    article+='<div class="eb-plates compare-group">'+''.join(figure(d['photo'],d['caption'],pre) for d in group['photos'])+'</div></section><div class="eb-prose eb-body">'
  article+='</div>'
  if r.get('details'):article+='<section class="eb-section"><h2>近看石面</h2><div class="eb-plates compare-group">'+''.join(figure(d['photo'],d['caption'],pre) for d in r['details'])+'</div></section>'
  others=[n for n in r['primary_photos'] if n not in mainphotos]
  if others:
   article+='<section class="eb-section"><h2>相互参看</h2><div class="eb-plates compare-group">'
   for n in others:
    w=next(by[wid] for wid in r['works'] if by[wid]['photo']==n);cap=caption(w)
    if n=='1371':cap='佛坐像、在家礼拜者与僧人 · 克利夫兰 · 三件分别登记'
    article+=figure(n,cap,pre)
   article+='</div></section>'
  if r['id']=='u17':article+='<div class="eb-table"><table><caption>三件躯干的材料与残高</caption><thead><tr><th>馆藏号</th><th>归属</th><th>材料</th><th>残高</th></tr></thead><tbody><tr><td>45-15</td><td>马图拉</td><td>杂色红砂岩</td><td>114.94厘米</td></tr><tr><td>39-19</td><td>鹿野苑</td><td>浅黄色砂岩</td><td>86.36厘米</td></tr><tr><td>1943.278</td><td>鹿野苑</td><td>砂岩</td><td>76.2厘米</td></tr></tbody></table></div>'
  article+='<section id="object-records" class="eb-section"><h2>本篇作品</h2>'
  for wid in r['works']:
   w=by[wid];article+=f'<details id="{wid}"><summary>{e(w["title"])} · {e(w["accession"] or collection(w))}</summary>'+facts(w,pre)+f'<p><a href="../#{wid}">在完整目录中查看 →</a> · <a href="../#place-{w["place"]}">地域关系 →</a></p>'
   alt=[n for n in w['photos'] if n!=w['photo']]
   if alt:article+='<div class="eb-plates">'+''.join(figure(n,w['title']+' · 同件另一张现场照片',pre) for n in alt)+'</div>'
   article+='</details>'
  article+='</section>'
  labels={}
  for wid in r['works']:
   for n in by[wid]['labels']:labels.setdefault(n,[]).append(wid)
  article+=refs(keys,pre,labels)
  article+='<nav class="eb-next" aria-label="前后细读">'+(f'<a href="../{units[idx-1]["id"]}/">← {e(units[idx-1]["title"])}</a>' if idx else '<a href="../">← 专题首页</a>')+(f'<a href="../{units[idx+1]["id"]}/">{e(units[idx+1]["title"])} →</a>' if idx+1<len(units) else '<a href="../#catalogue">完整目录 →</a>')+'</nav>'
  dest=B/r['id'];dest.mkdir(exist_ok=True);(dest/'index.html').write_text(shell(r['title'],article,1))
 # Marker-controlled entrances survive full builds and repeated focused builds.
 entry='<a class="issue-link" href="../early-buddhist-art/"><img src="../early-buddhist-art/images/1351-900.webp" width="'+str(manifest['1351']['width'])+'" height="'+str(manifest['1351']['height'])+'" alt="树冠下的佛三尊与台座铭文" loading="lazy" style="object-fit:contain"><div><p class="eyebrow">EARLY BUDDHIST ART</p><h2>早期佛教艺术</h2><p>从早期佛塔艺术到笈多及其余绪，沿着身体、衣纹与礼拜重新看。</p><p class="issue-meta">五章 · 十八篇细读 · 地域与馆藏地图</p><span class="text-link">走进这一辑 →</span></div></a>'
 parent=ROOT/'museum-notes/south-asian-art/index.html';s=re.sub(r'<!-- early-buddhist-entry -->.*?<!-- /early-buddhist-entry -->','',parent.read_text(),flags=re.S);anchor='<a class="issue-link" href="../khajuraho/">';assert anchor in s;s=s.replace(anchor,'<!-- early-buddhist-entry -->'+entry+'<!-- /early-buddhist-entry -->'+anchor,1);s=s.replace('从一片神庙，走近不同的形象与信仰。','从佛塔到神庙，走近不同的形象与信仰。');parent.write_text(s)
 home=ROOT/'museum-notes/index.html';s=re.sub(r'<!-- early-buddhist-home -->.*?<!-- /early-buddhist-home -->','',home.read_text(),flags=re.S);anchor='<!-- khajuraho-home -->';assert anchor in s;home.write_text(s.replace(anchor,'<!-- early-buddhist-home -->'+entry.replace('href="../early-buddhist-art/"','href="early-buddhist-art/"').replace('src="../early-buddhist-art/','src="early-buddhist-art/')+'<!-- /early-buddhist-home -->'+anchor,1))
 print(f'Built early Buddhist art: {len(works)} object records, {len(units)} reading pages, {len(used)} used photographs; original archive remains separate.')
if __name__=='__main__':build()
