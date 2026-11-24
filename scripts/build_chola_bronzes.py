"""Author's Chola bronze notebook: one identity per work/ensemble, shared atlas data."""
from pathlib import Path
from html import escape as e
import json,re,hashlib
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/chola-bronzes'
URL='/museum-notes/chola-bronzes/'
TITLE='朱罗青铜造像'
GROUPS={'core':'朱罗时期','pre_chola':'前朱罗对照','extension':'晚期与延续'}
def load(n):return json.loads((BASE/'data'/f'{n}.json').read_text())
def build():
 works=load('catalogue');by={w['id']:w for w in works};media=load('media');sources=load('sources');museums=load('museums');mb={m['museum_id']:m for m in museums};readings=load('readings');stories=load('stories');chapters=load('chapters');details=load('details')
 revision=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((BASE/'data').glob('*.json')) if p.name!='atlas-index.json')+(BASE/'chola.js').read_bytes()+(BASE/'chola.css').read_bytes()).hexdigest()[:10]
 total=sum(w['object_count'] for w in works); photo_total=sum(p.get('is_original',True) for p in media.values())
 count=f'{len(works)}组观看对象 · {total}件造像 · {photo_total}张现场照片'
 def href(w):return URL+(w if isinstance(w,str) else w['id'])+'/'
 def image(n,alt,eager=False,small=False):
  p=media[str(n)];vs=p['variants'];v=vs[0 if small else min(1,len(vs)-1)]
  return (f'<img style="max-width:min(100%, {p["width"]}px)"' if p["width"]<400 else '<img')+f' src="{v["url"]}" srcset="'+', '.join(f'{v["url"]} {v["width"]}w' for v in vs)+f'" sizes="'+('(max-width:650px) 44vw, 270px' if small else '(max-width:650px) 92vw, 580px')+f'" width="{p["width"]}" height="{p["height"]}" alt="{e(alt)}" loading="'+('eager" fetchpriority="high' if eager else 'lazy')+'" decoding="async">'
 def fig(w,n=None,cap=None,eager=False):
  n=n or w['photo'];p=media[str(n)];cap=cap or w['title']+' · '+w['date']+(' · 双尊正面合影' if w['id']=='c20' and n==3352 else '');txt=cap+(' · '+p['display_note'] if p.get('display_note') else '')+'｜Merton摄于'+mb[w['viewing_museum_id']]['label_zh'];full=media[p['derived_from']]['original_url'] if p.get('derived_from') else p['variants'][-1]['url'] if p.get('rotation') else p['original_url']
  return f'<figure class="cb-figure{" cb-small-original" if p["width"]<400 else ""}"><a data-photo href="{full}" data-caption="{e(txt)}">{image(n,txt,eager)}</a><figcaption>{e(txt)}'+(f' · <a href="{p["original_url"]}">原始文件</a>' if p.get('rotation') else '')+'</figcaption></figure>'
 def detail_fig(d):
  v=d['variants'];cap=d['caption']+' · 原片局部，Merton摄';full=media[str(d['photo'])]['original_url']
  return f'<figure class="cb-detail"><a data-photo href="{v[-1]["url"]}" data-caption="{e(cap)}"><img src="{v[0]["url"]}" srcset="'+', '.join(f'{i["url"]} {i["width"]}w' for i in v)+f'" sizes="(max-width:650px) 88vw, 350px" width="{d["width"]}" height="{d["height"]}" loading="lazy" alt="{e(cap)}"></a><figcaption>{e(cap)} <a data-photo href="{full}" data-caption="完整原片">查看完整原片</a></figcaption></figure>'
 def card(w):return f'<a class="cb-card" href="{href(w)}"><span class="cb-image-frame">{image(w["photo"],w["title"]+" · "+w["date"],small=True)}</span><h3>{e(w["title"])}</h3><p>{e(w["date"])}</p><small>{e(mb[w["viewing_museum_id"]]["city"])} · {e(w["accession"] or "私人借展")}</small></a>'
 def grid(ids):return '<div class="cb-grid">'+''.join(card(by[i]) for i in dict.fromkeys(ids))+'</div>'
 def source_link(k):
  s=sources[k];return media[str(s['photo'])]['original_url'] if s.get('photo') else s['url']
 def inline(text):
  def sub(m):
   k=m[1];s=sources[k];label='展签' if s.get('photo') else '资料'
   return f'<a class="cb-cite" href="{URL}sources/#{k}" aria-label="{e(s["title"])}">[{label}]</a>'
  return re.sub(r'\[\[([A-Z0-9-]+)\]\]',sub,e(text))
 def refs(keys):return '<details class="cb-notes"><summary>资料与来源</summary><ul>'+''.join(f'<li><a href="{e(source_link(k))}">{e(sources[k]["title"])}</a> · <a href="{URL}sources/#{k}">查阅说明</a></li>' for k in dict.fromkeys(keys))+'</ul></details>'
 def heading(t,deck=''):return '<header class="cb-heading"><p class="eyebrow">CHOLA BRONZES · A MUSEUM NOTEBOOK</p><h1>'+e(t)+'</h1>'+(f'<p class="cb-deck">{e(deck)}</p>' if deck else '')+'</header>'
 def write(slug,t,b,cover=3316):
  nav=[('',TITLE),('atlas/','所见地图'),('stories/','神与圣徒'),('guide/','历史与观看'),('compare/','放在一起看')];canonical='https://qm2.github.io'+URL+(slug+'/' if slug else '')
  html=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t)} | 博物馆札记 · Merton</title><meta name="description" content="从亲见的朱罗铜像走进南印度的神庙、史诗与赞歌。{count}，博物馆地图、年代导览与逐件细读。"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{e(t)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{media[str(cover)]['variants'][-1]['url']}"><link rel="stylesheet" href="/museum-notes/museum.css"><link rel="stylesheet" href="/museum-notes/caravaggio/caravaggio.css"><link rel="stylesheet" href="{URL}chola.css?v={revision}"><script src="/museum-notes/caravaggio/caravaggio.js" defer></script><script src="{URL}chola.js?v={revision}" defer></script></head><body class="cb-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="/museum-notes/">Merton</a><nav aria-label="专题导航">'''+''.join(f'<a href="{URL}{u}"'+(' aria-current="page"' if u.rstrip('/')==slug else '')+f'>{n}</a>' for u,n in nav)+f'''</nav></header><main class="wrap" id="main"><nav class="breadcrumbs"><a href="/museum-notes/">博物馆札记</a><span>/</span><a href="/museum-notes/south-asian-art/">南亚艺术</a><span>/</span><a href="{URL}">{TITLE}</a></nav>{b}</main><footer class="site-footer wrap"><a href="{URL}">返回专题</a><a href="{URL}sources/">资料与来源</a><a href="/museum-notes/pala-stone/">帕拉黑石造像</a><a href="#top">回到顶部</a></footer>{LIGHTBOX}</body></html>'''
  p=BASE/slug;p.mkdir(exist_ok=True,parents=True);(p/'index.html').write_text(html)
 def mapbox():return '''<div class="cb-map-box" data-map-box hidden><div class="cb-map-tools" aria-label="地图范围"><button type="button" data-map="mainland" aria-pressed="true">美国本土</button><button type="button" data-map="east" aria-pressed="false">东部放大</button></div><svg id="cb-map" viewBox="0 0 1000 470" role="group" aria-label="亲见博物馆分布，使用Tab键选择馆址"></svg><p class="cb-caption">地图标记实际观看的博物馆，包括借展；不是古代制作地点。数字为观看组数，标“馆”的聚合点可点击放大。底图：<a href="https://www.naturalearthdata.com/">Natural Earth</a>，公有领域。</p><div id="cb-map-selection" aria-live="polite"></div></div>'''
 def tamil_map():
  geo=json.loads((BASE/'data/tamil-geography.geojson').read_text());xmin,ymin,xmax,ymax=geo['bbox'];width,height=900,650
  def xy(c):return ((c[0]-xmin)/(xmax-xmin)*width,(ymax-c[1])/(ymax-ymin)*height)
  svg='<svg viewBox="0 0 900 650" role="group" aria-label="考弗里河与泰米尔城镇；编号对应下方可展开条目"><rect width="900" height="650" fill="#edece4"/>'
  for f in geo['features']:
   g=f['geometry'];lines=g['coordinates'] if g['type']=='MultiLineString' else [g['coordinates']]
   for line in lines:
    points=' '.join(f'{x:.1f},{y:.1f}' for x,y in map(xy,line));svg+='<polyline points="'+points+'" class="'+('cb-river' if f['properties']['kind']=='river' else 'cb-coast')+'"/>'
  svg+='<text x="80" y="160" class="cb-region-label">泰米尔纳德</text><text x="730" y="350" class="cb-region-label">孟加拉湾</text><text x="120" y="410" class="cb-river-label">考弗里河 Kaveri</text><text x="345" y="460" class="cb-region-label">三角洲地区</text>'
  for i,p in enumerate(load('places'),1):
   x,y=xy((p['lon'],p['lat']));dx,dy={3:(30,28),9:(-22,-25)}.get(i,(0,0))
   if dx or dy:svg+=f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+dx:.1f}" y2="{y+dy:.1f}" class="cb-callout"/>'
   svg+=f'<a href="#place-{p["id"]}" aria-label="{i} {e(p["title"])}"><title>{e(p["title"])} · {e(p["name_en"])}</title><circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="17"/><text x="{x+dx:.1f}" y="{y+dy+6:.1f}" class="cb-map-number">{i}</text></a>'
  return '<section class="cb-section" id="tamil-map"><p class="eyebrow">THE KAVERI DELTA</p><h2>从河谷到海港</h2><p class="cb-prose">这张地图定位历史背景中的寺城、海港与工艺中心。编号可打开地点说明及相关作品；美国博物馆地图仍记录我实际观看的地方。</p><div class="cb-history-map">'+svg+'</svg></div><p class="cb-caption">现代河道与海岸：Natural Earth，公有领域；城镇：GeoNames，CC BY 4.0；三座世界遗产神庙：UNESCO。现代河道只作地理参照，不复原朱罗时代水系或疆域。<a href="'+URL+'sources/#GEONAMES">数据说明</a></p><div class="cb-place-index">'+''.join(f'<a href="#place-{p["id"]}">{i}. {e(p["title"])}</a>' for i,p in enumerate(load('places'),1))+'</div>'+''.join(f'<details class="cb-notes cb-place" id="place-{p["id"]}"><summary>{i}. {e(p["title"])}'+(' · '+e(p['name_en']) if p['name_en']!=p['title'] else '')+'</summary><p>'+inline(p['text'])+'</p><p class="cb-caption">'+e(p['coordinate_note'])+'</p><p class="cb-caption">回到亲见作品：</p>'+grid(p['works'])+'</details>' for i,p in enumerate(load('places'),1))+'</section>'
 museum_buttons='<div class="cb-museum-buttons">'+''.join(f'<a href="{URL}atlas/?museum={m["museum_id"]}#catalogue">{e(m["city"])} · {sum(w["viewing_museum_id"]==m["museum_id"] for w in works)}组</a>' for m in museums)+'</div>'
 b='<section class="cb-hero"><div>'+heading(TITLE,'神的舞步，人的赞歌')+'<div class="cb-prose"><p>抬起的一只脚，指向天空的手，举到嘴边的手指。这些铜像在不同的博物馆里与我相遇，也把观看带向南印度的神庙、史诗和歌声。</p><p>湿婆可以狂舞，也可以弹琴；英雄能够搬山，也会低下头。沿着身体与动作慢慢看，陌生的神名便有了可以记住的性格。</p></div><p class="cb-caption">'+count+'</p><nav class="cb-localnav"><a href="#chapters">六条阅读线索</a><a href="guide/#timeline">沿年代重看</a></nav></div>'+fig(by['c29'],eager=True)+'</section>'
 b+='<section class="cb-section"><p class="eyebrow">FIVE PLACES TO BEGIN</p><h2>先停在这五件</h2><p class="cb-prose">从两尊相伴的身体，到一个低首的英雄；从女神的可能身份，到神像的归还。每一件，都有不止一个值得靠近的地方。</p><div class="cb-picks">'+''.join(card(by[k]) for k in ['c20','c27','c10','c23','c29'])+'</div></section>'
 b+='<nav class="cb-reading-paths" aria-label="专题深读">'+''.join('<a href="'+a['slug']+'/"><span>专题深读</span>'+e(a['title'])+' →</a>' for a in load('essays'))+'</nav>'
 b+=f'<section class="cb-section" id="map"><div class="cb-section-heading"><div><p class="eyebrow">WHERE I SAW THEM</p><h2>在{len(museums)}家博物馆相遇</h2></div><a href="atlas/">完整图录与筛选 →</a></div>'+mapbox()+museum_buttons+'</section>'
 b+='<section class="cb-section" id="chapters"><p class="eyebrow">SIX WAYS OF LOOKING</p><h2>从一个姿态，走进一个故事</h2><nav class="cb-localnav">'+''.join(f'<a href="#{c["id"]}">{e(c["title"])}</a>' for c in chapters)+'</nav>'
 for i,ch in enumerate(chapters):
  if ch['id']=='beyond':
   b+='<article class="cb-chapter" id="beyond"><p class="eyebrow">06 · BUDDHISM AND JAINISM IN THE CHOLA WORLD</p><h2>'+e(ch['title'])+'</h2><p class="cb-prose">'+e(ch['text'])+'</p><div class="cb-faith-pair">'
   for wid,title,text in [('c37','海港里的佛陀','纳加帕蒂南的海路连向东南亚，也让佛教寺院得到跨海的供养。10世纪佛陀伸出的双手，为这一片土地留下另一种礼拜的姿态。'),('c31','不动的身体','耆那圣者放下饰物，双臂垂于身旁。冥想、非暴力与摆脱束缚，在直立而安静的身体里获得了可见的形象。')]:
    w=by[wid];b+='<section><div class="cb-faith-image">'+fig(w)+'</div><h3>'+title+'</h3><p class="cb-meta">'+e(w['date'])+' · 新奥尔良美术馆'+(' · 2021.98' if wid=='c37' else ' · 私人收藏借展')+'</p><p>'+text+'</p><a href="'+href(w)+'">'+e(w['title'])+' · 进入细读 →</a>'+(f'<p><a href="{URL}guide/#buddhist-port">海港里的佛陀 · 历史与观看 →</a></p>' if wid=='c37' else f'<p><a href="{URL}stories/#jina">认识耆那教的解脱之路 →</a></p>')+'</section>'
   b+='</div><section class="cb-boundary"><h3>王朝之前与之后</h3><p class="cb-prose">7世纪泰米尔佛像提供前史；约1300年的安坐湿婆与13—14世纪的森班达尔，则让我们看到王朝更替之后仍在延续的礼拜与制作。</p>'+grid(['c38','c24','c35'])+'</section></article>'
   continue
  w=by[ch['cover']];b+=f'<article class="cb-chapter" id="{ch["id"]}"><div class="cb-feature">'+fig(w)+f'<div class="cb-prose"><p class="eyebrow">0{i+1}</p><h2>{e(ch["title"])}</h2><p>{e(ch["text"])}</p><p><a href="{href(w)}">细看：{e(w["title"])} →</a></p></div></div>'+grid([k for k in ch['works'] if k!=ch['cover']])+(f'<p><a href="{ch["background_link"]}">{e(ch["background_label"])}</a></p>' if ch.get('background_link') else '')+'</article>'
 b+='</section><section class="cb-section cb-paths"><div><h2>铜像怎样走出神庙</h2><p>王朝、诗人、工匠与供养者：把身体放回它曾经生活的世界。</p><a href="guide/">历史与观看 →</a></div><div><h2>换一件，继续看</h2><p>看两位音乐家失去的琴，三位圣童指向神的手，以及不同舞王的平衡。</p><a href="compare/">八组并看 →</a></div></section>'
 write('',TITLE,b,by['c29']['photo'])
 for i,w in enumerate(works):
  r=readings[w['id']];b=heading(w['title'],w['title_en'])+f'<p class="cb-meta">{e(w["date"])} · {e(w["region"])}</p><div class="cb-full">'+fig(w,eager=True)+'</div><article class="cb-prose"><p class="cb-lead">'+inline(r['lead'])+'</p>'
  for si,sec in enumerate(r['sections']):
   b+='<section><h2>'+e(sec['title'])+'</h2>'+''.join('<p>'+inline(p)+'</p>' for p in sec['paragraphs'])+'</section>'
   ds=[d for d in details if d['work']==w['id'] and d['after_section']==si]
   if ds:b+='<div class="cb-detail-row">'+''.join(detail_fig(d) for d in ds)+'</div>'
   if w['id']=='c20' and si==0:b+=fig(w,3387,'湿婆的冠饰、面容与上身 · 现场近照')
   if w['id']=='c33' and si==0:b+=fig(w,3380,'毗湿奴背面 · 后背、腰带与台座')
  b+='</article>'
  linked=[s for s in stories if w['id'] in s['works']]
  if linked:b+='<aside class="cb-prose cb-story-links"><p>认识这个故事：'+' · '.join(f'<a href="{URL}stories/#{s["id"]}">{e(s["title"])}</a>' for s in linked)+'</p></aside>'
  fields=[('年代',w['date']),('地域',w['region']),('材料',w['medium']),('收藏／借出',w['collection']),('馆藏号',w.get('accession') or '展签未列'),('亲见地点',mb[w['viewing_museum_id']]['label_zh'])]
  if w.get('credit'):fields.append(('入藏／借展',w['credit']))
  if w.get('dimensions'):fields.append(('尺寸',w['dimensions']))
  if w.get('viewing_context'):fields.append(('观看场合',w['viewing_context']))
  if w['object_count']>1:fields.append(('组合',f'{w["object_count"]}件单体，作为一组观看记录'))
  b+='<details id="record" class="cb-notes"><summary>作品资料与现场展签</summary><dl class="cb-facts">'+''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k,v in fields)+'</dl>'
  b+=''.join('<p class="cb-caption">'+e(n)+'</p>' for n in w.get('notes',[])+r.get('notes',[]))+fig(w,w['label'],'现场展签')
  for n in w.get('provenance_photos',[]):b+=fig(w,n,'馆方归还与借展说明')
  b+='</details>'
  extras=[n for n in w['photos'] if n not in [w['photo'],w['label'],3387 if w['id']=='c20' else -1,3380 if w['id']=='c33' else -1]+w.get('provenance_photos',[])]
  if extras:b+='<details class="cb-notes"><summary>其余现场照片 · '+str(len(extras))+'张</summary>'+''.join(fig(w,n,{3324:'另一张完整舞姿',3326:'展厅中的大型舞王',3386:'两尊立像全身与台座 · 侧前方视角'}.get(n,w.get('photo_captions',{}).get(str(n),'现场补充视角'))) for n in extras)+'</details>'
  if w.get('backgrounds'):b+='<nav class="cb-localnav" aria-label="相关背景">'+''.join('<a href="'+URL+x['href']+'">'+e(x['title'])+' →</a>' for x in w['backgrounds'])+'</nav>'
  b+=refs(w['source_ids']+re.findall(r'\[\[([A-Z0-9-]+)\]\]',json.dumps(r,ensure_ascii=False)))
  b+=('<p class="cb-prose"><a href="'+URL+'guide/#buddhist-port">海港里的佛陀：南印度佛教背景</a></p>' if w['religion']=='佛教' else '')
  b+='<nav class="cb-localnav"><a href="'+URL+'guide/#timeline">年代与作品</a><a href="'+URL+'guide/#processions">神像与巡游</a><a href="'+URL+'atlas/?museum='+w['viewing_museum_id']+'#catalogue">回到观看馆</a></nav><section class="cb-section"><h2>放在一起看</h2>'+grid(r['related'])+'</section><nav class="cb-sequence" aria-label="前后作品">'
  if i:b+=f'<a href="{href(works[i-1])}">← {e(works[i-1]["title"])}</a>'
  b+='<a href="'+URL+'atlas/">完整图录</a>'
  if i<len(works)-1:b+=f'<a href="{href(works[i+1])}">{e(works[i+1]["title"])} →</a>'
  write(w['id'],w['title'],b+'</nav>',w['photo'])
 for a in load('essays'):
  b=heading(a['title'],a['deck'])+'<nav class="cb-localnav"><a href="'+URL+'guide/">历史与观看</a><a href="'+URL+'guide/#tamil-map">泰米尔历史地图</a>'+''.join('<a href="#'+q['id']+'">'+e(q['title'])+'</a>' for q in a['sections'])+'</nav><div class="cb-full">'+fig(by[a['work']],eager=True)+'</div><article class="cb-prose"><p class="cb-lead">'+inline(a['lead'])+'</p>'
  for q in a['sections']:
   b+='<section id="'+q['id']+'"><h2>'+e(q['title'])+'</h2>'+''.join('<p>'+inline(t)+'</p>' for t in q['paragraphs'])
   if q.get('quote'): b+='<blockquote class="cb-poem"><p lang="'+q.get('lang','zh-CN')+'">'+e(q['quote'])+'</p><p>'+e(q['translation'])+'</p><footer>'+inline(q['attribution'])+'</footer></blockquote>'
   if q.get('detail'):b+='<div class="cb-detail-row">'+''.join(detail_fig(d) for d in details if d['id']==q['detail'])+'</div>'
   if q.get('photo'):b+=fig(by[q.get('work',a['work'])],q['photo'],q['caption'])
   if q.get('works'):b+='<div class="cb-essay-works">'+grid(q['works'])+'</div>'
   b+='</section>'
  b+='</article>'+refs(re.findall(r'\[\[([A-Z0-9-]+)\]\]',json.dumps(a,ensure_ascii=False)))
  write(a['slug'],a['title'],b,by[a['work']]['photo'])
 b=heading('神与圣徒','看懂一个动作，记住一个故事')+'<nav class="cb-localnav" aria-label="故事目录">'+''.join(f'<a href="#{s["id"]}">{e(s["name"].split(" · ")[0])}</a>' for s in stories)+'</nav><p class="cb-prose">以下故事采用各条注明的馆方版本。神话说明人物为何被这样描绘，照片则让我们看到这件作品实际留下的形象。</p>'
 for s in stories:
  b+=f'<section class="cb-section" id="{s["id"]}"><div class="cb-feature">'+fig(by[s['works'][0]])+'<div class="cb-prose"><h2>'+e(s['title'])+'</h2><p class="cb-caption">'+e(s['name'])+'</p><p class="cb-memory">'+e(s['memory'])+'</p><p>'+inline(s['text']+''.join('[['+k+']]' for k in s['sources']))+'</p><p>'+e(s['look'])+'</p><p><a href="'+href(s['works'][0])+'">进入这件作品 →</a></p></div></div>'+grid(s['works'][1:])+'</section>'
 write('stories','神与圣徒',b,3358)
 b=heading('历史与观看','从南印度的神庙，到眼前的一次相遇')+'<nav class="cb-localnav"><a href="#timeline">沿年代重看</a><a href="#tamil-map">泰米尔历史地图</a>'+''.join(f'<a href="#{h["id"]}">{e(h["title"])}</a>' for h in load('history'))+'</nav>'
 b+=tamil_map()
 for h in load('history'):
  b+=f'<section class="cb-section" id="{h["id"]}"><div class="cb-feature">'+fig(by[h['work']])+'<div class="cb-prose"><h2>'+e(h['title'])+'</h2>'+''.join('<p>'+inline(p)+'</p>' for p in h['paragraphs'])+'<p><a href="'+href(h['work'])+'">回到这件作品 →</a></p></div></div></section>'
 periods=[('7世纪 · 前史','early'),('10世纪','c10'),('11世纪','c11'),('12世纪','c12'),('13世纪','c13'),('晚期与延续','later'),('宽年代范围','broad')]
 def period(w):
  if w['group']=='pre_chola':return 'early'
  if w['group']=='extension':return 'later'
  if w['date_precision']=='broad_period':return 'broad'
  mid=(w['date_start']+w['date_end'])/2
  return 'c10' if mid<1000 else 'c11' if mid<1100 else 'c12' if mid<1200 else 'c13'
 b+='<section class="cb-section" id="timeline"><h2>沿年代重看</h2><p class="cb-prose">按馆方年代范围的中点安排位置，原有约年与范围仍显示在卡片上；前史、宽断代及晚期延续另列。向下阅读时，切换控件会留在上方。</p><nav class="cb-time-navigation" hidden aria-label="切换时间线年代"><button type="button" id="cb-time-prev" aria-controls="cb-time-track">← 前一段</button><label for="cb-time-period" class="cb-time-label">跳至时期</label><select id="cb-time-period" aria-controls="cb-time-track" aria-label="跳至时期"><option value="">选择时期</option>'+''.join(f'<option value="{j}">{name}</option>' for j,(name,_) in enumerate(periods))+'</select><button type="button" id="cb-time-next" aria-controls="cb-time-track">后一段 →</button></nav><div class="cb-timeline" id="cb-time-track" tabindex="0" aria-label="横向年代图录">'
 for name,key in periods:b+='<section class="cb-century"><h3>'+name+'</h3>'+''.join('<p class="cb-event">'+inline(t)+'</p>' for t in load('events').get(key,[]))+''.join(grid([w['id']]) for w in sorted(works,key=lambda w:w['date_start']) if period(w)==key)+'</section>'
 b+='</div></section><section class="cb-section cb-prose"><h2>下次看展，可以先问四件事</h2><p>它在做什么动作？手里原本拿着什么？谁站在它旁边？台座怎样让它固定或移动？拍完整身体、侧面与背面，再拍最喜欢的局部和完整展签，下一次就能从这些线索继续读。</p><a href="../atlas/">带着问题回到图录 →</a></section>'
 b+='<section class="cb-section"><h2>继续读</h2><div class="cb-paths">'+''.join('<div><h3><a href="'+URL+a['slug']+'/">'+e(a['title'])+'</a></h3><p>'+e(a['deck'])+'</p></div>' for a in load('essays'))+'</div></section>'
 write('guide','历史与观看',b,3379)
 b=heading('放在一起看','让相似与差别都留在眼前')+'<p class="cb-caption">照片按阅读需要缩放，不表示实物等大。各图保留完整构图，点击可查看原片。</p><nav class="cb-localnav">'+''.join(f'<a href="#{p["id"]}">{e(p["title"])}</a>' for p in load('comparisons'))+'</nav>'
 for p in load('comparisons'):
  b+=f'<section class="cb-section" id="{p["id"]}"><h2>{e(p["title"])}</h2><p class="cb-prose">{inline(p["text"])}</p><div class="cb-comparison">'+''.join('<div>'+fig(by[k])+'<p><a href="'+href(k)+'">'+e(by[k]['title'])+' · 进入细读</a></p><p class="cb-caption">'+e(by[k].get('dimensions','尺寸待补'))+'</p><p class="cb-caption">'+e(p.get('observations',{}).get(k,''))+'</p></div>' for k in p['works'])+'</div></section>'
 write('compare','放在一起看',b,3364)
 b=heading('所见地图与完整图录',count)+f'<p class="cb-prose">作品分布在{len(museums)}家亲见博物馆。两组各含两尊，因此观看组数与单体数分别统计；休斯顿的罗摩、华盛顿归还后借展的舞王，以及私人借展作品，都另列收藏关系。</p>'
 b+='<form id="cb-filters" class="cb-filters" hidden><label>名称、神祇、馆藏号<input id="cb-search" type="search" placeholder="例如：湿婆、Sambandar、1961.94"></label><label>观看馆<select id="cb-museum"><option value="">全部博物馆</option>'+''.join(f'<option value="{m["museum_id"]}">{e(m["label_zh"])}</option>' for m in museums)+'</select></label><label>信仰<select id="cb-religion"><option value="">全部</option><option>印度教</option><option>耆那教</option><option>佛教</option></select></label><label>范围<select id="cb-group"><option value="">全部作品</option>'+''.join(f'<option value="{k}">{v}</option>' for k,v in GROUPS.items())+'</select></label><label>排列<select id="cb-sort"><option value="catalogue">图录顺序</option><option value="date">年代由早至晚</option><option value="museum">观看博物馆</option></select></label><button type="reset">清除条件</button></form><p id="cb-result-count" aria-live="polite">全部'+str(len(works))+'组</p><section id="map" class="cb-section"><h2>博物馆分布</h2>'+mapbox()+museum_buttons+'</section><section id="catalogue" class="cb-section"><h2>完整图录</h2><p id="cb-empty" hidden>没有符合条件的作品，可以减少条件或清除筛选。</p><div class="cb-grid cb-catalogue">'
 for w in works:b+=f'<article id="{w["id"]}" data-record-id="{w["id"]}">'+card(w)+f'<p class="cb-caption">{e(GROUPS[w["group"]])} · {e(w["religion"])} · {sum(media[str(n)].get("is_original",True) for n in w["photos"])}张原片'+(' · 2件组合' if w['object_count']==2 else '')+'</p></article>'
 write('atlas','所见地图与完整图录',b+'</div></section>')
 public=[{k:w.get(k) for k in ['id','title','title_en','date','date_start','date_end','medium','collection','viewing_museum_id','accession','group','religion','object_count']}|{'url':href(w),'image':media[str(w['photo'])]['variants'][0]['url'],'width':media[str(w['photo'])]['width'],'height':media[str(w['photo'])]['height'],'search':' '.join(str(w.get(k) or '') for k in ['title','title_en','date','region','medium','collection','accession'])+' '+mb[w['viewing_museum_id']]['label_zh']} for w in works]
 (BASE/'data/atlas-index.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
 b=heading('资料与来源','作品与展签摄影：Merton')+'<p class="cb-prose">基本资料据现场展签及馆方记录整理，观看地点由作者确认。人物故事采用注明的版本，原片与展签均可从作品页打开。下列记录说明具体使用了哪些资料。</p>'
 for k,s in sources.items():b+=f'<details id="{k}" class="cb-notes"><summary>{e(s["title"])}</summary><p><a href="{e(source_link(k))}">打开原始资料</a></p><p>{e(s["read_status"])}</p><p>{e(s["used_for"])}</p><p class="cb-caption">核对日期：{e(s["checked_on"])}</p></details>'
 write('sources','资料与来源',b)
 # Reinsert only this topic's parent entrances, after existing parent builders.
 p=ROOT/'museum-notes/south-asian-art/index.html';s=p.read_text();s=re.sub(r'<!-- chola-bronzes -->.*?<!-- /chola-bronzes -->','',s,flags=re.S)
 entry='<a class="issue-link" href="../chola-bronzes/">'+image(3316,'湿婆舞王，朱罗青铜造像',small=True).replace('<img ','<img style="object-fit:contain" ')+'<div><p class="eyebrow">CHOLA BRONZES · SOUTH INDIA</p><h2>朱罗青铜造像</h2><p>从舞王的火焰到圣徒的赞歌，沿亲见铜像走进南印度的神庙与史诗。</p><p class="issue-meta">'+str(len(works))+'组作品 · '+str(len(museums))+'家博物馆 · 地图与年代导览</p><span class="text-link">进入专题 →</span></div></a>'
 assert '</section></main>' in s;s=s.replace('</section></main>','<!-- chola-bronzes -->'+entry+'<!-- /chola-bronzes --></section></main>');p.write_text(s)
 p=ROOT/'museum-notes/index.html';s=p.read_text();s=re.sub(r'<!-- chola-bronzes-home -->.*?<!-- /chola-bronzes-home -->','',s,flags=re.S);assert '<!-- /pala-stone-home -->' in s
 s=s.replace('<!-- /pala-stone-home -->','<!-- /pala-stone-home --><!-- chola-bronzes-home --><p class="featured-note"><a href="chola-bronzes/">新辑：朱罗青铜造像｜神的舞步，人的赞歌</a></p><!-- /chola-bronzes-home -->');p.write_text(s)
 print(f'Chola bronzes: {len(works)} groups / {total} objects / {photo_total} photos / {len(museums)} viewing museums; {len(works)+6+len(load("essays"))} pages.')
if __name__=='__main__':build()
