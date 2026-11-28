"""Khmer notebook: one record catalogue, six readings, contextual map and dated ranges."""
from pathlib import Path
from html import escape as e
import json,re,hashlib
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/khmer-art';URL='/museum-notes/khmer-art/'
KINDS={'ancient_object':'古代作品／组合','historic_cast':'近代翻模','historic_model':'近代模型','label_only':'仅展签'}
CATS={'sculpture':'独立像与残件','architecture':'建筑与构件','ritual':'仪式器具'}
RELS={'known_findspot':'明确发现地点','known_site':'明确原址','prototype_site':'翻模／模型原型','region_only':'区域','style_context_only':'风格背景','associated_or_tentative':'候选／关联','context_site':'历史背景'}
def load(n):return json.loads((BASE/'data'/n).read_text())
def photos(w,role='image'):
 return w.get(role+'_keys',w[role+'_numbers'])
def build():
 works=load('objects.json');by={w['id']:w for w in works};media=load('media.json');readings=load('readings.json');rb={r['id']:r for r in readings};sources=load('sources.json');sb={s['id']:s for s in sources};museums=load('museums.geojson')['features'];origins=load('origins.geojson')['features'];timeline=load('timeline.json');context=load('context_timeline.json');details={d['id']:d for d in load('details.json')}
 rev=hashlib.sha256((BASE/'khmer.css').read_bytes()+(BASE/'khmer.js').read_bytes()+b''.join(p.read_bytes() for p in sorted((BASE/'data').glob('*.json')) if p.name!='atlas-index.json')).hexdigest()[:10]
 def href(id):return URL+id+'/'
 def im(n,small=False,eager=False):
  m=media[str(n)];vs=m['variants'];cap=m['caption']+'｜Merton摄于'+m['museum_seen'];sz='(max-width:650px) 45vw, 310px' if small else '(max-width:650px) 92vw, 950px'
  return f'<img src="{vs[0 if small else min(1,len(vs)-1)]["url"]}" srcset="'+', '.join(f'{v["url"]} {v["width"]}w' for v in vs)+f'" sizes="{sz}" width="{m["display_width"]}" height="{m["display_height"]}" alt="{e(cap)}" loading="'+('eager" fetchpriority="high' if eager else 'lazy')+'" decoding="async">'
 def fig(n,eager=False):
  m=media[str(n)];cap=m['caption']+'｜Merton摄于'+m['museum_seen'];full=m['original_url'];preview=m['variants'][-1]['url'] if m['rotation'] else full
  return f'<figure class="ka-figure '+('ka-portrait' if m['display_height']>m['display_width'] else 'ka-landscape')+f'" id="photo-{n}"><a data-photo href="{preview}" data-caption="{e(cap)}">{im(n,eager=eager)}</a><figcaption>{e(cap)}'+(f' · <a href="{full}" target="_blank" rel="noopener">未旋转原片</a>' if m['rotation'] else '')+'</figcaption></figure>'
 def detail_row(ids):
  out='<div class="ka-detail-row">'
  for id in ids:
   d=details[id];m=media[d['photo']];vs=d['variants'];cap=d['caption']+'（原片局部）'
   marks='<svg class="ka-detail-pointers" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'+''.join(f'<line x1="{50 if id=="pediment" and n=="2" else 8 if x<60 else 92}" y1="{8 if id=="pediment" and n=="2" else max(7,y-10)}" x2="{x}" y2="{y}"/><circle cx="{x}" cy="{y}" r="1"/>' for x,y,n,label in d['markers'])+'</svg>'+''.join(f'<span class="ka-detail-mark" style="left:{50 if id=="pediment" and n=="2" else 8 if x<60 else 92}%;top:{8 if id=="pediment" and n=="2" else max(7,y-10)}%" aria-hidden="true">{e(n)}</span>' for x,y,n,label in d['markers'])
   legends=' · '.join(f'{n} {label}' for x,y,n,label in d['markers'])
   out+=f'<figure class="ka-figure ka-detail" style="--detail-width:{d["max_width"]}px"><a class="ka-detail-image" data-photo href="{vs[-1]["url"]}" data-caption="{e(cap)}"><img src="{vs[-1]["url"]}" srcset="'+', '.join(f'{v["url"]} {v["width"]}w' for v in vs)+f'" sizes="(max-width:650px) 85vw, {d["max_width"]}px" width="{d["width"]}" height="{d["height"]}" alt="{e(cap)}" loading="lazy" decoding="async">'+marks+'</a><figcaption>'+('<span class="ka-detail-key">'+e(legends)+'</span>' if legends else '')+e(cap)+(' '+e(d['credit']) if d.get('credit') else '｜Merton摄于'+e(m['museum_seen']))+f' · <a data-photo href="{m["original_url"]}" data-caption="{e(m["caption"])}">查看完整原片</a></figcaption></figure>'
  return out+'</div>'
 def inline(t):
  def sub(m):
   k=m[1]
   if k.startswith('P'):return f'<a class="ka-cite" href="{URL}sources/#{k}" aria-label="现场照片{e(k[1:])}">[展签]</a>'
   return f'<a class="ka-cite" href="{URL}sources/#{k}" aria-label="{e(sb[k]["title"])}">[资料]</a>'
  return re.sub(r'\[\[([SP][0-9]+)\]\]',sub,e(t))
 def heading(title,deck=''):
  return '<header class="ka-heading"><p class="eyebrow">KHMER ART · A MUSEUM NOTEBOOK</p><h1>'+e(title)+'</h1>'+('<p class="ka-deck">'+e(deck)+'</p>' if deck else '')+'</header>'
 def write(slug,title,body,cover=3632):
  dest=BASE/slug;dest.mkdir(parents=True,exist_ok=True);canonical='https://qm2.github.io'+href(slug) if slug else 'https://qm2.github.io'+URL
  nav=[('','专题'),('#readings','五组细读'),('guide/','历史与形象'),('atlas/','所见地图'),('catalogue/','完整图录')]
  html=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | 高棉艺术 · 博物馆札记</title><meta name="description" content="水、山与神的身体：从西梅奔卧毗湿奴与举山克里希纳，走进高棉神话、建筑和博物馆中的相遇。"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{e(title)}"><meta property="og:image" content="{media[str(cover)]['variants'][-1]['url']}"><link rel="stylesheet" href="/museum-notes/museum.css"><link rel="stylesheet" href="/museum-notes/caravaggio/caravaggio.css"><link rel="stylesheet" href="{URL}khmer.css?v={rev}"><script src="/museum-notes/caravaggio/caravaggio.js" defer></script><script src="{URL}khmer.js?v={rev}" defer></script></head><body class="ka-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="/museum-notes/">Merton</a><nav aria-label="专题导航">'''+''.join(f'<a href="{URL}{u}">{t}</a>' for u,t in nav)+f'''</nav></header><main class="wrap" id="main">{body}</main><footer class="site-footer wrap"><a href="{URL}">返回高棉艺术</a><a href="{URL}sources/">资料与来源</a><a href="/museum-notes/">博物馆札记</a><a href="#top">回到顶部</a></footer>{LIGHTBOX}</body></html>'''
  (dest/'index.html').write_text(html)
 def card(id):
  w=by[id];ns=photos(w);n=ns[0] if ns else None
  return f'<a class="ka-card" href="{href(id)}">'+(im(n,small=True) if n else '<div class="ka-no-image">仅有现场展签<br>实物照片未收录</div>')+f'<h3>{e(w["title_zh"])}</h3><p>{e(w["date_display"])}</p><p class="ka-meta">{e(w["museum_seen"])} · {KINDS[w["record_kind"]]}</p></a>'
 def grid(ids):return '<div class="ka-grid">'+''.join(card(i) for i in dict.fromkeys(ids))+'</div>'
 def info(w):
  d=w['dimensions_cm'];dim=''
  if d:
   if 'height' in d:dim=' × '.join(str(d[k]) for k in ['height','width','depth'] if k in d)+'厘米（高 × 宽 × 深'+('；'+d['scope'] if d.get('scope') else '')+'）'
   else:dim='约600厘米：原来／展览提示的总体尺度，并非完整保存的长度'
  fields=[('年代',w['date_display']),('材料',w['material']),('风格',w['style']),('观看',w['museum_seen']+' · '+w['city_seen']),('收藏／归属',w['owner']),('原址／关联',w['origin_display']),('馆藏编号',w['accession'] or '未记录'),('尺寸',dim),('记录类型',KINDS[w['record_kind']])]
  return '<dl class="ka-data">'+''.join(f'<div><dt>{t}</dt><dd>{e(str(v))}</dd></div>' for t,v in fields if v)+'</dl>'
 def refs(keys):
  keys=list(dict.fromkeys(keys));return '<details class="ka-notes"><summary>资料与来源</summary><ul>'+''.join(f'<li><a href="{s["url"]}">{e(s["title"])}</a> · <a href="{URL}sources/#{s["id"]}">查阅说明</a></li>' for k in keys if (s:=sb.get(k)))+'</ul></details>' if keys else ''
 # Home: photographer's full frame, five personal routes, quiet navigation into context.
 b=heading('高棉艺术','水、山与神的身体')+fig(3632,True)
 intro='<div class="ka-prose ka-intro"><p>在华盛顿看到西梅奔卧毗湿奴，是我最受震撼的一次相遇。如此庞大的青铜身体，头与托住它的手却给人一种安稳的感觉。我也很喜欢克利夫兰的举山克里希纳，尤其是它与原来洞窟环境的联系；吉美的大型像与门龛、金贝尔的宝座佛，以及纽约和金贝尔的早期青铜，各自留下了不同的印象。</p><p>回看这些照片，水、山与建筑渐渐成为线索：一位神托住山，一位神卧在海，巨人与那伽守住进寺的道路。这个专题想留下的，是作品的面貌，也是它们原来怎样与地景、礼拜和人的身体相遇。</p></div>'
 intro+=f'<p class="ka-stats">{len(works)}条作品与展示记录 · {len(media)}张现场照片 · {len(museums)}家观看机构</p><p class="ka-meta ka-prose">从前吴哥、吴哥到相关的泰国东北部传统。目录含组合、近代翻模、模型及仅展签记录，记录数并不等于古代原作件数。</p>'
 b+='<section id="readings" class="ka-section"><p class="eyebrow">FIVE WAYS OF LOOKING</p><h2>五组深刻的相遇</h2><div class="ka-routes">'
 for a in readings[:5]:b+=f'<a class="ka-route" href="{href(a["id"])}">{im(a["hero"],small=True)}<h3>{e(a["title"])}</h3><p>{e(a["subtitle"])}</p></a>'
 b+='</div></section>'+intro+'<section class="ka-section ka-bridge"><div><p class="eyebrow">HISTORY & LOOKING</p><h2>先有一个山水之间的坐标</h2><p>约600年的大型神像、早期菩萨、吴哥的门楣与宝冠佛。沿年代看并存的形象，再把博物馆中的作品放回原来的地域。</p><nav class="ka-links"><a href="guide/">历史与形象</a><a href="atlas/">观看馆与原址地图</a><a href="atlas/#timeline">沿年代重看</a><a href="catalogue/">完整图录</a></nav></div><a class="ka-card" href="buddhist-images/">'+im(3613,small=True)+'<h3>佛、观音与般若佛母</h3><p>从盘蛇上的佛，看到布满小佛的身体。</p></a></section>'
 b+='<aside class="ka-prose ka-related"><h2>继续在亚洲造像之间看</h2><p><a href="/museum-notes/pala-stone/">帕拉黑石造像</a> · <a href="/museum-notes/chola-bronzes/">朱罗青铜</a> · <a href="/museum-notes/xuzhou/">虚舟收藏</a> · <a href="/museum-notes/water-moon-guanyin/">水月观音</a></p></aside>'
 write('','高棉艺术：水、山与神的身体',b)
 # Six substantial readings; captions stay with their photographic containers.
 for a in readings:
  b=heading(a['title'],a['subtitle'])+fig(a['hero'],True)+'<p class="ka-prose ka-deck">'+e(a['deck'])+'</p>'
  b+='<nav class="ka-prose ka-links" aria-label="文章目录">'+''.join(f'<a href="#section-{i+1}">{e(s["title"])}</a>' for i,s in enumerate(a['sections']))+'</nav>'
  for i,s in enumerate(a['sections']):
   b+=f'<section class="ka-section" id="section-{i+1}"><div class="ka-prose"><h2>{e(s["title"])}</h2>'+''.join('<p>'+inline(p)+'</p>' for p in s['paragraphs'])+'</div>'
   if s['photos']:b+='<div class="ka-photo-row">'+''.join(fig(n) for n in s['photos'])+'</div>'
   if s.get('details'):b+=detail_row(s['details'])
   if s['related']:b+='<details class="ka-notes"><summary>放在一起看</summary>'+grid(s['related'])+'</details>'
   b+='</section>'
  b+='<p class="ka-memory ka-prose">'+e(a['memory'])+'</p><section class="ka-section"><h2>作品资料与现场照片</h2>'+grid(a['records'])+'</section>'
  if a.get('labels'):b+='<details class="ka-notes"><summary>完整现场展签</summary>'+''.join(fig(n) for n in a['labels'])+'</details>'
  for note in a.get('notes',[]):b+='<details class="ka-notes"><summary>'+e(note['title'])+'</summary><p>'+inline(note['text'])+'</p></details>'
  keys=re.findall(r'\[\[(S\d+)\]\]',json.dumps(a,ensure_ascii=False));b+=refs(keys)
  region='angkor' if a['map_site'] in ['west-mebon','bayon','preah-khan-angkor'] else 'southeast'
  b+='<nav class="ka-links"><a href="'+URL+'atlas/?view=origins&amp;region='+region+'&amp;site='+a['map_site']+'#map">在地图中看相关地点与作品</a><a href="'+URL+'#readings">回到五组细读</a></nav>'
  write(a['id'],a['title'],b,a['hero'])
 # All records get durable details, rather than expanding 118 files into independent works.
 for w in works:
  ids=photos(w);labs=photos(w,'label');b=heading(w['title_zh'],w['title_en'])
  if ids:b+=fig(ids[0],True)
  else:b+='<p class="ka-prose">这条记录目前只有现场展签，未收录可确认的实物照片。</p>'
  b+='<div class="ka-prose"><p>'+e(w['summary_zh'])+'</p><p class="ka-look"><strong>近看一处</strong> '+e(w['look_for_zh'])+'</p>'+info(w)+'</div>'
  for section in w.get('sections',[]):
   b+='<section class="ka-section ka-prose"><h2>'+e(section['title'])+'</h2>'+''.join('<p>'+inline(p)+'</p>' for p in section['paragraphs'])+'</section>'
   if section.get('details'):b+=detail_row(section['details'])
  if w.get('related_ids'):b+='<section class="ka-section"><h2>放在一起看</h2>'+grid(w['related_ids'])+'</section>'
  if w.get('provenance'):b+='<details class="ka-notes"><summary>馆方公布的收藏记录</summary><ul>'+''.join('<li>'+e(p['date']+' · '+p['name'])+inline('[[S30]]')+'</li>' for p in w['provenance'])+'</ul></details>'
  if w['reading_ids']:b+='<nav class="ka-prose ka-reading-entry" aria-label="精读文章"><span>继续细读</span>'+''.join(f'<a href="{href(i)}">{e(rb[i]["title"])}</a>' for i in w['reading_ids'])+'</nav>'
  if len(ids)>1:b+='<section class="ka-section"><h2>换一个角度</h2><div class="ka-photo-row">'+''.join(fig(n) for n in ids[1:])+'</div></section>'
  if labs:b+='<details class="ka-notes" id="labels"><summary>现场展签与背景资料 · '+str(len(labs))+'张</summary><div class="ka-photo-row">'+''.join(fig(n) for n in labs)+'</div></details>'
  b+=refs(w['source_ids'])
  b+=f'<nav class="ka-links"><a href="{URL}catalogue/#{w["id"]}">回到图录</a><a href="{URL}atlas/?museum={w["museum_seen_id"]}#map">这家博物馆</a><a href="{URL}atlas/?q={w["id"]}#timeline">年代位置</a></nav>'
  write(w['id'],w['title_zh'],b,ids[0] if ids else labs[0])
 # Shared catalogue / map / timeline controls and server-rendered fallback.
 index=[]
 for w in works:
  ns=photos(w);n=ns[0] if ns else None
  index.append(dict(id=w['id'],title=w['title_zh'],museum=w['museum_seen_id'],kind=w['record_kind'],category=w['category'],material=w['material_group'],status=w['status'],date=w['date_display'],start=w['year_start'],end=w['year_end'],lane=w['timeline_lane'],image=media[str(n)]['variants'][0]['url'] if n else None,url=href(w['id']),search=' '.join(str(w.get(k) or '') for k in ['id','title_zh','title_en','museum_seen','city_seen','owner','accession','style','origin_display','date_display','material']),origin_links=w['origin_map_links']))
 (BASE/'data/atlas-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
 def filters():
  select=lambda k,label,options:f'<label>{label}<select name="{k}" id="ka-{k}"><option value="">全部</option>'+''.join(f'<option value="{e(v)}">{e(t)}</option>' for v,t in options)+'</select></label>'
  return '<form id="ka-filters" class="ka-filters" hidden><label class="ka-search">名称、英文、藏号或地点<input type="search" name="q" id="ka-q" placeholder="例如：观音、Plai Bat、1973.106"></label>'+select('museum','观看博物馆',[(m['properties']['id'],m['properties']['museum']) for m in museums])+'<details class="ka-more-filters"><summary>更多筛选</summary><div>'+select('kind','记录类型',list(KINDS.items())+[('pending','待识别')])+select('category','形制',list(CATS.items()))+select('material','材料',[('bronze','青铜'),('stone','石雕'),('other','翻模及其他')])+'</div></details><button type="reset">清除条件</button></form><p id="ka-count" role="status" aria-live="polite">全部'+str(len(works))+'条记录</p>'
 def catalogue():
  s='<section id="catalogue" class="ka-section"><h2>逐件图录</h2><p class="ka-meta">一条记录可包含多件一组或多张照片。每条均可打开基本资料、展签与原片。</p><div class="ka-grid ka-catalogue">'
  for w in works:s+=f'<article class="ka-catalogue-item" data-record="{w["id"]}" id="{w["id"]}">'+card(w['id'])+f'<p class="ka-meta">{e(w["accession"] or "馆藏号未记录")} · {len(set(photos(w)+photos(w,"label")))}张照片</p>'+(''.join(f'<a class="ka-read-link" href="{href(i)}">阅读全文 · {e(rb[i]["title"])}</a>' for i in w['reading_ids'][:1]))+'</article>'
  return s+'</div><p id="ka-empty" hidden>没有符合条件的记录。可清除条件，或试试英文名、馆藏号。</p></section>'
 def timeview():
  out='<section id="timeline" class="ka-section"><h2>沿年代重看</h2><p class="ka-meta">横条显示资料中的年代范围；“约年”和宽泛分期保留原文字，不把横条中点当作制作年份。组合记录覆盖组内作品的年代。现代翻模另列。</p>'
  for lane,title,lo,hi in [('ancient_art','古代作品与组合',500,1450),('modern_display','近代翻模与模型',1800,1950)]:
   out+=f'<details class="ka-notes ka-time-group" open><summary>{title}</summary><div class="ka-axis"><span>{lo}</span><span>{(lo+hi)//2}</span><span>{hi}年</span></div>'
   for w in sorted((w for w in works if w['timeline_lane']==lane and w['year_start'] is not None),key=lambda w:w['year_start']):
    l=max(0,(w['year_start']-lo)/(hi-lo)*100);width=max(.8,(w['year_end']-w['year_start'])/(hi-lo)*100)
    out+=f'<a class="ka-time-row" href="{href(w["id"])}" data-time-record="{w["id"]}">'+(im(photos(w)[0],small=True) if photos(w) else '<span class="ka-meta">仅展签</span>')+f'<div><h3>{e(w["title_zh"])}</h3><p>{e(w["date_display"])} · {e(w["museum_seen"])}</p><div class="ka-range" aria-hidden="true"><span style="left:{l:.3f}%;width:{width:.3f}%"></span></div></div></a>'
   out+='</details>'
  out+='<details class="ka-notes" open><summary>年代待核</summary>'+''.join(f'<div data-time-record="{w["id"]}">{card(w["id"])}</div>' for w in works if w['year_start'] is None)+'</details></section>'
  return out
 def maps():
  out='<section id="map" class="ka-section"><h2>从观看的城市，到作品的山水</h2><p class="ka-meta">观看馆表示亲见地点；原址图分别标出明确来源、原型、关联与区域。坐标为城市或遗址附近的示意定位，不表示精确考古位置。</p><div id="ka-map-tools" hidden><div class="ka-links" role="group" aria-label="地图视图"><button type="button" data-view="museums" aria-pressed="true">观看博物馆</button><button type="button" data-view="origins" aria-pressed="false">古代原址与关联</button></div><div class="ka-links" id="ka-map-regions"></div><svg id="ka-map" role="group" aria-label="可选择的博物馆与原址地图"></svg><p id="ka-map-help" class="ka-meta">数字为当前筛选下的记录数；区域图中的相近地点可点击展开；吴哥核心区单列重要寺院。</p><p id="ka-map-legend" class="ka-meta" hidden><span class="ka-legend known">明确原址</span><span class="ka-legend prototype">原型地点</span><span class="ka-legend tentative">候选／关联</span><span class="ka-legend region">区域</span><span class="ka-legend style">风格背景</span></p><div id="ka-map-selection" aria-live="polite"></div><button id="ka-clear-site" type="button" hidden>清除原址筛选</button></div><p class="ka-meta">底图：<a href="https://www.naturalearthdata.com/about/terms-of-use/">Natural Earth公共领域地理数据</a>（区域国界与洞里萨湖为1:5000万数据）。底图不代表古代疆域；无网络时仍可使用下面的地点入口。</p><details class="ka-notes" open><summary>观看馆列表</summary><div class="ka-place-list">'
  for m in museums:
   p=m['properties'];out+=f'<a href="?museum={p["id"]}#catalogue" data-museum="{p["id"]}">{e(p["museum"])}<span>{e(p["city_zh"])} · {len(p["record_ids"])}条</span></a>'
  out+='</div></details><details class="ka-notes"><summary>原址、区域与关联地点</summary><p class="ka-meta">'+ ' · '.join(RELS.values())+'</p><div class="ka-place-list">'
  for f in origins:
   p=f['properties'];out+=f'<a href="?view=origins&amp;site={p["id"]}#map" data-site="{p["id"]}">{e(p["name_zh"])}<span>{RELS.get(p["relation_type"],p["relation_type"])} · {e(p["note"])}</span></a>'
  return out+'</div></details></section>'
 b=heading('所见地图与年代','在哪座城市遇见，又从哪片山水而来')+filters()+maps()+timeview()+catalogue();write('atlas','所见地图与年代',b)
 b=heading('完整图录',f'{len(works)}条记录 · {len(media)}张照片').replace('ka-heading','ka-heading ka-catalogue-heading')+'<nav class="ka-links"><a href="../atlas/#map">地图</a><a href="../atlas/#timeline">年代时间线</a></nav>'+filters()+catalogue();write('catalogue','完整图录',b)
 # Compact contextual guide: genuine events and objects keep separate labels.
 b=heading('历史与观看','把地名、形象和建筑放回同一张阅读桌')+'<div class="ka-prose"><p>高棉艺术不只属于吴哥窟。约600年的大型神像已经在柬埔寨南部形成成熟的身体语言；后来吴哥地区的水库、寺院与道路，又为供奉创造了新的空间。泰国东北部的早期青铜在这里作为相关传统并读。</p><p>802年与1431年常被用作吴哥时期的阅读界标；具体作品的断代与各地区的变化，仍须分别看待。吴哥是历史区域，吴哥窟则是其中一座寺庙。[[S23]]</p></div>'.replace('[[S23]]',inline('[[S23]]'))
 b+='<section class="ka-section ka-period-overview"><h2>先看时代与地景</h2><p class="ka-meta">分期用来帮助并看，形象与工艺可以跨越时期延续。</p><div class="ka-table-wrap"><table class="ka-period-table"><thead><tr><th>时期</th><th>重要地点</th><th>亲见代表作品</th><th>观看特点</th></tr></thead><tbody>'
 for t in load('periods.json'):
  b+='<tr><th scope="row">'+e(t['title'])+'<span>'+e(t['date'])+'</span></th><td>'+e(t['places'])+'</td><td>'+''.join(f'<a href="{href(id)}">{e(by[id]["title_zh"])}</a>' for id in t['records'])+'</td><td>'+e(t['look'])+inline('[['+t['source']+']]')+'</td></tr>'
 b+='</tbody></table></div></section>'
 for era,title in [('ancient','古代：供奉、城市与寺院'),('modern','近代以来：发现、收藏与修复')]:
  b+='<section class="ka-section"><h2>'+title+'</h2><div class="ka-history">'
  for t in (t for t in context if t['era']==era):
   source=t['source_id'];citation=inline(f'[[{source}]]') if source in sb else '<span class="ka-meta">据相关作品现场展签</span>'
   b+=f'<details class="ka-notes"><summary><span class="ka-date">{e(t["date_display"])}</span>{e(t["title"])}</summary>'+citation+(grid(t['record_ids']) if t['record_ids'] else '')+'</details>'
  b+='</div></section>'
 b+='<section class="ka-section" id="images"><h2>先认几位反复相遇的形象</h2><p class="ka-prose">先看姿态，再找发冠与持物。同一位尊神可以有不同的身体，形象线索也应与展签、题材和伴随人物一起使用。</p>'
 glossary=[('一具身体，两位神','Harihara','观者左侧的发绺与半只第三眼属于湿婆，右侧高冠属于毗湿奴。身体两侧连贯相接，以一尊像结合两位神的力量。',['K03'],['S30']),('毗湿奴与克里希纳','Vishnu · Krishna','卧毗湿奴与永恒之蛇相连；举山的克里希纳是他的化身。一个让宇宙安睡于水上，一个保护人群免受暴雨。',['W03','C02'],['S01','S04']),('湿婆与难近母','Shiva · Durga','骑牛的湿婆与帕尔瓦蒂是一组关系；难近母则战胜水牛魔。残像若没有清楚持物，身份仍需结合馆方记录。',['G07','C08'],[]),('迦楼罗与那伽','Garuda · Naga','鸟喙、翼、鸟爪与人体结合的是迦楼罗；多头蛇可护佛，也可构成栏杆与仪式器具。看它们怎样相对，往往比只记一个名字更有用。',['G09','O02','N01'],['S15']),('观音与弥勒','Avalokiteshvara · Maitreya','本专题早期青铜里，观音发冠中有阿弥陀佛，弥勒发髻前有塔。四臂与相近身形，并不表示同一位菩萨。',['M02','K01'],['S08','S09']),('般若佛母','Prajnaparamita','她是佛教智慧的人格化。莲花、经书与女性身体可以相接，也可展开为多面多臂的形态。',['H01','O03','W01'],['S21']),('天神与阿修罗','Deva · Asura','在进寺道路的拉蛇巨人中，天神面貌常较平静，阿修罗更显威猛；看单独头部时，还要追问它原来属于怎样的构件。',['G01','C01','D01'],['S06'])]
 for i,(title,en,text,ids,ss) in enumerate(glossary):b+=f'<details class="ka-notes" id="image-{i+1}"><summary>{title}<span class="ka-meta">{en}</span></summary><p class="ka-prose">{e(text)}'+''.join(inline(f'[[{s}]]') for s in ss)+'</p>'+grid(ids)+'</details>'
 b+='</section><section class="ka-section"><h2>从雕像回到建筑</h2><div class="ka-prose"><p>门楣横跨入口；尖形山墙收住叙事；门框围出通道；栏杆和端饰沿道路延展。看一件残片时，可以先问：它原来要求人平视、仰望，还是从旁边经过？</p><p>“女王宫风格”“巴戎风格”提供比较的坐标，具体的出土地仍看单件记录。吉美的翻模与模型，另外保存了近代博物馆如何理解建筑的历史。</p><p><a href="../guimet/">进入吉美建筑细读</a> · <a href="../atlas/?view=origins#map">原址与风格背景地图</a></p></div></section>'
 write('guide','历史与观看',b,3536)
 # Source catalogue; photos include every supplied original exactly once in this index.
 b=heading('资料与来源','现场照片、馆方记录与研究文章')+'<div class="ka-prose"><p>作品与展厅照片均为Merton现场摄影。中文说明依据照片、现场展签及下列资料整理；个人观看与历史判断分别表达。</p><p>能阅读全文、仅取得官方检索正文，以及尚需继续核对的条目分别注明。外部链接用于研究，不引入第三方作品图。</p></div>'
 for s in sources:b+=f'<section class="ka-source ka-prose" id="{s["id"]}"><h2>{e(s["title"])}</h2><p><a href="{e(s["url"])}">打开原始资料</a></p><p>{e(s["used_for"])}</p><details class="ka-notes"><summary>查阅范围</summary><p>{e(s["retrieval"])} · {e(s["implementation_review"])}</p></details></section>'
 b+='<section class="ka-section" id="photos"><h2>'+str(len(media))+'张现场照片索引</h2><p class="ka-meta">按原始序号或文件标识追溯；标签、局部、环境与整件共享相应作品记录。</p><div class="ka-photo-index">'
 for n,m in media.items():b+=f'<details class="ka-notes" id="P{n}"><summary>{n} · {e(m["caption"])}</summary>{fig(n)}<p>'+ ' · '.join(f'<a href="{href(a["record_id"])}">{e(by[a["record_id"]]["title_zh"])}</a>' for a in m['assignments'])+'</p></details>'
 b+='</div></section>';write('sources','资料与来源',b)
 # Museum home entry: generated in the site's existing stream, not a new top-level redesign.
 p=ROOT/'museum-notes/index.html';s=p.read_text();s=re.sub(r'<!-- khmer-art -->.*?<!-- /khmer-art -->','',s,flags=re.S)
 entry='<!-- khmer-art --><a class="issue-link" href="khmer-art/">'+im(3632,small=True).replace('<img ','<img style="object-fit:contain" ',1)+'<div><p class="eyebrow">KHMER ART</p><h2>高棉艺术</h2><p>水、山与神的身体。从西梅奔卧毗湿奴与举山克里希纳，走进吴哥建筑及早期青铜。</p><p class="issue-meta">五组个人重点 · '+str(len(works))+'条作品与展示记录<br>'+str(len(media))+'张现场照片 · 观看馆与原址地图</p><span class="text-link">进入专题 →</span></div></a><!-- /khmer-art -->'
 marker='<section class="future-collections"';pos=s.find(marker);assert pos>=0
 # place inside the existing current-collections section before its closing tag
 closing=s.rfind('</section>',0,pos);s=s[:closing]+entry+s[closing:];p.write_text(s)
 print(f'Khmer: {len(works)} records, {len(media)} photos, {len(museums)} viewing museums, {len(readings)} readings; {len(works)+len(readings)+5} pages.')
if __name__=='__main__':build()
