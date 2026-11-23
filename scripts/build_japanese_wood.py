"""Japanese sculpture notebook: structured intake, complete readings, shared CDN photographs."""
from pathlib import Path
from html import escape as e
import json,re
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/japanese-buddhist-sculpture';URL='/museum-notes/japanese-buddhist-sculpture/'
TITLE='东瀛佛影';SUB='日本佛教木雕：木胎、金彩与亲见札记'
def build():
 load=lambda n:json.loads((BASE/'data'/n).read_text())
 display_notes=load('display-notes.json');works=load('catalogue.json');by={w['id']:w for w in works};media=load('media.json');sources=json.loads((BASE/'research/source_registry.json').read_text());essays={x['work_id']:x for x in load('essays.json')};chapters=load('chapters.json');comparisons=load('comparisons.json');selection=load('selections.json');museums=load('viewing-museums.geojson')['features'];hist=load('historical-context.geojson')['features']
 # Keep canonical source photo mappings; the full-body display choice is editorial only.
 full={w['id']:w['main_photo'] for w in works};full['j19']=3152
 caps={3135:'侧看三尊、飞天与展厅中的间距',3146:'展厅远景：坐像与周围空间',3147:'面容、双手与坐姿近照',3151:'地藏面容与胸前衣褶近照',3152:'地藏立像全貌，玻璃反光保留',3157:'面容、衣纹与光背近照',3162:'胸腹以下层叠衣纹与金色细线',3163:'侧面：手势与衣服离开身体的距离',3164:'背面：袈裟沿身体垂下',3165:'衣饰近照：细密纹样与衣缘',3168:'侧面：坐椅、宽袍与头部轮廓',3171:'侧面：身体、莲座与光背',3172:'斜侧面：抬手与坐姿',3173:'台座近照：莲瓣与下方结构',3174:'面部、胸前衣褶及残存金饰',3205:'上半身与镂空光背近照',3206:'面容、举手与光背近照',3207:'垂落衣褶近照',3210:'背面：躯干、衣褶与残存彩饰',3232:'面容、胸腹与双手近照',3242:'侧看云座上的三尊',3243:'三尊与云气近照',3247:'仁王一对中的一尊',3248:'仁王一对中的另一尊',3251:'绕到背后：袈裟展开的形状',3252:'侧面：锡杖与身体的关系',3253:'背部袈裟近照：纹样的分区',3254:'前侧衣纹与装饰近照',3257:'佛坛打开后的内部空间',3258:'中央佛像与供具近照',3259:'中央佛像、莲座与悬挂饰件'}
 def href(w):return URL+(w if isinstance(w,str) else w['id'])+'/'
 def image(n,alt,eager=False,small=False):
  p=media[str(n)];vs=p['variants'];return f'<img src="{vs[0 if small else min(1,len(vs)-1)]["url"]}" srcset="'+', '.join(f'{x["url"]} {x["width"]}w' for x in vs)+f'" sizes="{("(max-width:650px) 43vw, 260px" if small else "(max-width:650px) 92vw, 650px")}" width="{p["width"]}" height="{p["height"]}" alt="{e(alt)}" loading="{("eager" if eager else "lazy")}" '+('fetchpriority="high" ' if eager else '')+'decoding="async">'
 def figure(n,w,cap=None,eager=False):
  cap=cap or ('合照后方的胸像' if w['id']=='j04' else '合照前方的坐像' if w['id']=='j05' else caps.get(n,'现场全貌'));txt=f'{w["publish_title"]} · {cap}｜Merton摄于{w["viewing_museum"]}'
  return f'<figure class="jw-figure"><a data-photo href="{media[str(n)]["original_url"]}" data-caption="{e(txt)}">{image(n,txt,eager)}</a><figcaption>{e(txt)}</figcaption></figure>'
 def card(w):
  return f'<a class="jw-card" href="{href(w)}">{image(full[w["id"]],w["publish_title"]+" · "+w["viewing_museum"],small=True)}<h3>{e(w["publish_title"])}</h3><p>{e(w["date_display"])}</p><p>{e(w["viewing_museum"])}</p></a>'
 def grid(ids):return '<div class="jw-grid">'+''.join(card(by[x]) for x in dict.fromkeys(ids))+'</div>'
 def heading(t,sub=''):return f'<header class="jw-heading"><p class="eyebrow">JAPANESE BUDDHIST SCULPTURE</p><h1>{e(t)}</h1><p class="jw-deck">{e(sub)}</p></header>'
 def shell(t,body,slug='',cover=3161):
  canon='https://qm2.github.io'+URL+(slug+'/' if slug else '')
  nav=''.join(f'<a href="{URL}{u}">{n}</a>' for u,n in [('',TITLE),('#chapters','六章阅读'),('atlas/','地图与图录'),('compare/','并看'),('guide/','观看与工艺')])
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t)} | 博物馆札记 · Merton</title><meta name="description" content="{e(SUB)}。六章阅读、25篇精读与62条亲见作品／组合档案。"><link rel="canonical" href="{canon}"><meta property="og:title" content="{e(t)}"><meta property="og:image" content="{media[str(cover)]['variants'][-1]['url']}"><meta property="og:url" content="{canon}"><link rel="stylesheet" href="/museum-notes/museum.css"><link rel="stylesheet" href="/museum-notes/caravaggio/caravaggio.css"><link rel="stylesheet" href="{URL}wood.css"><script src="/museum-notes/caravaggio/caravaggio.js" defer></script><script src="{URL}wood.js" defer></script></head><body class="jw-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="/museum-notes/">Merton</a><nav aria-label="专题导航">{nav}</nav></header><main class="wrap" id="main"><nav class="breadcrumbs"><a href="/museum-notes/">博物馆札记</a><span>/</span><a href="/museum-notes/japanese-art/">日本艺术</a><span>/</span><a href="{URL}">{TITLE}</a></nav>{body}</main><footer class="site-footer wrap"><a href="{URL}">返回专题</a><a href="{URL}sources/">资料与来源</a><a href="#top">回到顶部</a></footer>{LIGHTBOX}</body></html>'''
 def write(slug,t,body,cover=3161):
  p=BASE/slug;p.mkdir(exist_ok=True,parents=True);(p/'index.html').write_text(shell(t,body,slug,cover))
 def source_url(k):
  s=sources[k]
  if k.startswith('L'):return media[k[1:]]['original_url']
  return s.get('url')
 def inline(s):
  s=e(s)
  s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<a href="{m[2]}">{m[1]}</a>',s)
  s=re.sub(r'\[((?:S-|U-)[A-Z0-9-]+|L\d+)\]',lambda m:f'<a class="jw-cite" href="{URL}sources/#{m[1]}" title="{e(sources[m[1]]["title"])}">[{"展签" if m[1].startswith("L") else "资料"}]</a>',s)
  s=re.sub(r'\bj\d{2}\b',lambda m:f'<a href="{href(m[0])}">{e(by[m[0]]["publish_title"])}</a>',s)
  s=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',s)
  return s
 def markdown(s):
  # Only our reviewed paragraphs/headings/tables, not arbitrary raw HTML.
  chunks=[];buf=[];table=[]
  def flush():
   if buf:chunks.append('<p>'+inline(' '.join(buf))+'</p>');buf.clear()
   if table:
    rows=[x.strip().strip('|').split('|') for x in table];chunks.append('<div class="jw-table"><table><thead><tr>'+''.join('<th>'+inline(x.strip())+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in row)+'</tr>' for row in rows[2:])+'</tbody></table></div>');table.clear()
  for line in s.strip().splitlines():
   if line.startswith('|'):table.append(line);continue
   if not line.strip():flush();continue
   if line.startswith('#'):flush();chunks.append('<h2>'+inline(line.lstrip('# '))+'</h2>')
   else:buf.append(line)
  flush();return ''.join(chunks)
 def reading(file,work=False):
  raw=(BASE/file).read_text().split('\n---')[0]
  if work:raw=raw[raw.find('### '):]
  else:raw='\n'.join(raw.splitlines()[1:])
  return markdown(raw)
 def refs(keys):
  keys=list(dict.fromkeys(keys));items=[]
  for k in keys:
   if k.startswith('https://'):
    items.append(f'<li><a href="{e(k)}">馆方资料</a></li>');continue
   s=sources[k];u=source_url(k);name=s['title']
   if k.startswith('L'):name='现场展签（可放大查看）'
   if k.startswith('U-'):name='观看与作品对应：据作者提供的记录'
   items.append('<li>'+ (f'<a href="{u}">{e(name)}</a>' if u else e(name)) +f' · <a href="{URL}sources/#{k}">资料说明</a></li>')
  return '<details class="jw-sources"><summary>资料与来源</summary><ol>'+''.join(items)+'</ol></details>' if items else ''
 def textkeys(file):return re.findall(r'\[((?:S-|U-)[A-Z0-9-]+|L\d+)\]',(BASE/file).read_text().split('\n---')[0])
 def facts(w):
  fields=[('年代',w['date_display']),('材料',w['materials_summary']),('作者',w['artist']),('收藏',w['collection_museum']),('编号',w['accession']),('亲见',w['viewing_museum'])]
  if w.get('ownership_note') and w['ownership_note']!='馆方馆藏记录':fields.append(('收藏说明',w['ownership_note']))
  return '<dl class="jw-facts">'+''.join(f'<div><dt>{k}</dt><dd>{e(str(v))}</dd></div>' for k,v in fields)+'</dl>'
 # Home: full figure, personal foreword, concise pathways rather than all records.
 hero=by['j23'];body=heading(TITLE,SUB)+'<div class="jw-hero">'+figure(3161,hero,'完整立像 · 1269年',True)+'</div><section class="jw-prose jw-foreword" aria-label="个人序言">'+reading('content/00-foreword.md')+'</section>'
 body+='<nav class="jw-localnav"><a href="#memories">记忆较深</a><a href="#chapters">六章阅读</a><a href="#readings">25篇细读</a><a href="atlas/">所见地图与年表</a><a href="guide/">怎样看木雕</a></nav>'
 body+='<section class="jw-section" id="memories"><p class="eyebrow">PLACES TO RETURN TO</p><h2>记忆较深的形象</h2><p>有时是金线，有时是面容；再看全身，又被一个姿态留住。这里放着我想再回去看的十六件／组。</p>'+grid(selection['user_memorable_ids'])+'</section>'
 chcover={'crossing':'j03','body':'j51','pureland':'j40','wrath':'j01','people':'j24','survival':'j25'}
 body+='<section class="jw-section" id="chapters"><p class="eyebrow">SIX CHAPTERS</p><h2>从跨海的形象，到木像的后来生活</h2><div class="jw-chapters">'
 for ch in chapters[1:7]:
  key=ch['id'][3:];wid=chcover[key];body+=f'<a href="{URL}{ch["id"]}/">{image(full[wid],by[wid]["publish_title"],small=True)}<span class="eyebrow">{ch["id"][:2]}</span><h3>{e(ch["title"])}</h3></a>'
 body+='</div></section><section class="jw-section" id="readings"><h2>二十五篇细读</h2><div class="jw-reading-list">'+''.join(f'<a href="{href(wid)}"><span>{e(by[wid]["publish_title"])}</span>{e(x["title"])}</a>' for wid,x in essays.items())+'</div></section>'
 body+='<section class="jw-section jw-entry-pair"><div><h2>所见地图与年表</h2><p>十五处观看馆址，六十二条作品／组合档案。一件作品的年代、收藏地与我看见它的地方，分别留下来。</p><a href="atlas/">打开地图、年代与完整图录</a></div><div><h2>放在一起看</h2><p>同一尊格的不同身体，木与铜的不同重量。十组并看，把衣纹、手印和表面的疑问带回具体作品。</p><a href="compare/">进入十组并看</a><p><a href="guide/">怎样看木雕：观看与工艺</a></p></div></section>'
 write('',TITLE,body)
 # Chapters, all supplied narrative retained.
 for ch in chapters[1:7]:
  key=ch['id'][3:];wid=chcover[key];ids=[w['id'] for w in works if w.get('chapter_id')==key];mentioned=re.findall(r'\bj\d{2}\b',(BASE/ch['file']).read_text().split('\n---')[0]);ids=list(dict.fromkeys(ids+mentioned))
  b=heading(ch['title'])+'<div class="jw-full">'+figure(full[wid],by[wid],eager=True)+'</div><article class="jw-prose">'+reading(ch['file'])+'</article>'+refs(textkeys(ch['file']))+'<section class="jw-section"><h2>本章的作品</h2>'+grid(ids)+'</section>'
  write(ch['id'],ch['title'],b,full[wid])
 ch=chapters[-1];write('guide','怎样看木雕',heading('怎样看木雕','从一处细节，回到整个身体')+'<article class="jw-prose">'+reading('content/07-looking-and-technique.md')+'</article>'+refs(textkeys('content/07-looking-and-technique.md'))+grid(['j23','j59','j11','j51']))
 # Every record has a stable page. Readings interleave actual detail photographs.
 for w in works:
  wid=w['id'];entry=essays.get(wid);b=heading(w['publish_title'],w['date_display'])
  if wid=='j58':b+='<div class="jw-pair">'+''.join(figure(n,w,eager=i==0) for i,n in enumerate(w['photo_numbers']))+'</div>'
  else:b+='<div class="jw-full">'+figure(full[wid],w,eager=True)+'</div>'
  b+=f'<p class="jw-caption jw-center">{e(w["collection_museum"])} · {e(w["accession"])}'+(' · 木雕之外的青铜对照' if wid=='j08' else '')+'</p>'
  extra=[n for n in w['photo_numbers'] if n!=full[wid]] if wid!='j58' else []
  if entry:
   html=reading(entry['file'],True);parts=re.split(r'(?=<h2>)',html);parts=[x for x in parts if x];b+=f'<p class="jw-reading-title">{e(entry["title"])}</p>'
   for idx,part in enumerate(parts):
    b+='<section class="jw-prose">'+part+'</section>'
    if extra and idx<2:
     n=extra.pop(0);b+='<div class="jw-detail">'+figure(n,w)+'</div>'
  else:b+='<div class="jw-prose"><p>'+inline(display_notes.get(wid,w['notes']))+'</p></div>'
  if extra:b+='<section class="jw-section"><h2>再换一个距离</h2><div class="jw-pair">'+''.join(figure(n,w) for n in extra)+'</div></section>'
  b+='<details class="jw-label" id="label"><summary>作品资料与现场展签</summary>'+facts(w)+''.join(figure(p['number'],w,'现场展签') for p in w['labels'])+'</details>'
  keys=textkeys(entry['file']) if entry else [];keys+=['L'+str(p['number']) for p in w['labels'] if 'L'+str(p['number']) in sources]
  b+=refs(keys)
  if w['source_urls']:b+='<p class="jw-caption">馆藏及相关记录：'+ ' · '.join(f'<a href="{e(u)}">{e(u.split("/")[2])}</a>' for u in w['source_urls'])+'</p>'
  related=[c for c in comparisons if wid in c['record_ids']];b+='<nav class="jw-localnav" aria-label="继续观看">'+''.join(f'<a href="{URL}compare/#{c["id"]}">{e(c["title"])}</a>' for c in related)
  if w.get('chapter_id'):
   ch=next(c for c in chapters[1:7] if c['id'][3:]==w['chapter_id']);b+=f'<a href="{URL}{ch["id"]}/">回到本章：{e(ch["title"])}</a>'
  if wid=='j24':b+='<a href="/museum-notes/japanese-zen/">禅宗书画：形貌与墨迹</a>'
  if wid=='j41':b+='<a href="/museum-notes/water-moon-guanyin/">水月观音：相似姿态，不同身份</a>'
  b+=f'<a href="{URL}atlas/?museum={w["viewing_museum_id"]}">在{e(w["viewing_museum"])}还看过什么</a></nav>'
  write(wid,w['publish_title'],b,full[wid])
 # Comparisons with complete images and explicit non-scale relation.
 notes=['从僧形、手部与衣褶看地藏的不同身体；纳尔逊一件的手与足趾为后补。','中央、两侧与云座怎样安排接引？大都会的展厅陈设包含不同时代、不同收藏记录的组成。','先看胸前手印，再比较身体比例、莲座与光背的展开。','沿衣褶从胸前走到脚边，再看金饰和现存表面怎样改变节奏。','比较坐姿的宽度、衣纹的深浅与面貌；克利夫兰一件仍保留尊名未定。','从支点与手势，看骑牛大威德、不动、爱染和藏王权现各自的力量。','僧衣、坐姿与合掌是外观线索；历史人物、神祇与传说中的人物各有身份。','正面留下手势，侧面与背面让身体重新获得厚度。','托腮与自在坐姿带来相近的观看感受；如意轮与水月观音仍属不同的图像身份。','木与青铜各有构造和表面；目黑大佛的尺度、拆卸与运输还须结合其收藏记录。']
 b=heading('放在一起看','十组观看问题')+'<p class="jw-prose">照片按各自完整构图显示，不采用统一实物比例。年代、材料与尊名列在每件下方；相似姿态提供比较入口，不单独作为身份或断代依据。</p><nav class="jw-localnav">'+''.join(f'<a href="#{c["id"]}">{e(c["title"])}</a>' for c in comparisons)+'</nav>'
 for c,note in zip(comparisons,notes):
  b+=f'<section class="jw-section compare-group" id="{c["id"]}"><h2>{e(c["title"])}</h2><p class="jw-prose">{note}</p><div class="jw-compare">'
  for wid in c['record_ids']:
   w=by[wid];b+='<div>'+figure(full[wid],w)+f'<h3><a href="{href(w)}">{e(w["publish_title"])}</a></h3><p>{e(w["date_display"])}</p><p>{e(w["materials_summary"])}</p><p>{e(w["collection_museum"])}</p>'
   if c['id']=='c08':b+=figure({'j23':3164,'j41':3210,'j59':3251}[wid],w)
   b+='</div>'
  if c['id']=='c09':b+='<div class="jw-prose"><figure class="jw-figure"><a data-photo href="/museum-notes/buddhist-sculpture/images/nelson-215.jpg" data-caption="南海观音 · 纳尔逊—阿特金斯艺术博物馆，34-10｜Merton现场摄影"><img src="/museum-notes/buddhist-sculpture/images/nelson-215.jpg" alt="纳尔逊南海观音完整坐姿，Merton摄" width="1279" height="1706" loading="lazy"></a><figcaption>南海观音 · 纳尔逊—阿特金斯艺术博物馆，34-10｜Merton摄；沿用水月观音专题原图。</figcaption></figure><h3><a href="/museum-notes/water-moon-guanyin/#object-215">回到水月观音专题</a></h3><p>从托腮、膝部与支撑的手看起，再把持物与馆方名称放回观察。现有水月观音作品保留各自的记录与页面。</p></div>'
  b+='</div></section>'
 write('compare','放在一起看',b)
 # Sources retain the supplied study's explicit reading scope.
 b=heading('资料与来源','作品信息据现场展签及素材包所附研究整理')+'<div class="jw-prose"><p>本站照片均为Merton现场拍摄。来源下方说明素材包研究阶段的查阅范围；索引、摘要与未读书目分别注明，不等同于查阅全文。个人观看与造型分析不冒充馆方定论。</p></div>'
 for k,s in sources.items():
  name='现场展签' if k.startswith('L') else s['title'];u=source_url(k)
  b+=f'<details class="jw-source" id="{k}"><summary>{e(name)}</summary><p>{e(s["access_status"])}</p>'+ (f'<p><a href="{u}">打开'+('展签原图' if k.startswith('L') else '来源')+'</a></p>' if u else '<p>据作者提供的观看或作品对应记录。</p>')+'</details>'
 b+='<section class="jw-prose jw-section"><h2>延伸阅读</h2><p>Nishikawa, Kyotaro & Emily J. Sano, <i>The Great Age of Japanese Buddhist Sculpture, AD 600–1300</i>，Kimbell Art Museum，1982。本轮仅核书目信息，未阅全文；不据此补写单件断代或来源。</p></section>'
 write('sources','资料与来源',b)
 # Atlas: all content is server-rendered; JS adds shared filtering and map selection.
 def options(vals):return '<option value="">全部</option>'+''.join(f'<option value="{e(v)}">{e(v)}</option>' for v in sorted(set(vals)))
 b=heading('所见造像','博物馆地图 · 年代时间线 · 完整图录')+'<p class="jw-prose">'+str(len(works))+'条作品／组合档案，'+str(len(media))+'张现场照片，'+str(len(museums))+'处实际观看馆址。地图记录观看地点，收藏与历史关联另列；参观日期未由照片文件名推定。</p>'
 b+='<form class="jw-filters" id="jw-filters" hidden><label>找作品、人物或馆藏号<input id="jw-search" type="search" placeholder="例如：阿弥陀、快庆、1269"></label><label>观看馆<select id="jw-museum"><option value="">全部</option>'+''.join(f'<option value="{f["properties"]["id"]}">{e(f["properties"]["name_zh"])}</option>' for f in museums)+'</select></label><label>年代<select id="jw-period">'+options([w['period_bucket'] for w in works])+'</select></label><label>形象<select id="jw-subject">'+options([w['category'] for w in works])+'</select></label><label>阅读<select id="jw-reading"><option value="">全部</option><option value="personal">记忆较深</option><option value="essay">有精读</option></select></label><button type="reset">清除条件</button></form><p id="jw-count" aria-live="polite">62条档案</p><p id="jw-empty" hidden>没有符合条件的作品。可以减少筛选条件，或清除后重看。</p>'
 b+='<nav class="jw-localnav"><a href="#map">观看地图</a><a href="#timeline">年代时间线</a><a href="#catalogue">完整图录</a><a href="#context">历史地点</a></nav><section id="map" class="jw-section"><h2>我在哪里看过</h2><div id="jw-map-box" hidden><div class="jw-map-tools"><button type="button" data-map="all">所有馆址</button><button type="button" data-map="america">美国本土</button><button type="button" data-map="east">美国东部</button><button type="button" data-map="texas">德州</button><button type="button" data-map="paris">巴黎</button><button type="button" data-map="hawaii">夏威夷</button></div><svg id="jw-map" viewBox="0 0 1000 450" role="group" aria-label="博物馆地图；可选择馆址或放大聚合点"></svg><p class="jw-caption">底图：<a href="https://www.naturalearthdata.com/">Natural Earth</a>，公有领域。馆址为约略中心；近邻点聚合，点击可放大。地图与以下馆址列表使用同一组记录。</p></div><div class="jw-museums">'
 for f in museums:
  m=f['properties'];ids=[w['id'] for w in works if w['viewing_museum_id']==m['id']]
  b+=f'<details id="museum-{m["id"]}" data-museum-panel="{m["id"]}"><summary>{e(m["name_zh"])} · {e(m["city"])} <span class="jw-museum-count">{len(ids)}条</span></summary><p><a href="{m["website"]}">博物馆官网与馆址</a></p><div class="jw-grid">'+''.join(f'<div data-related-id="{wid}">{card(by[wid])}</div>' for wid in ids)+'</div></details>'
 b+='</div><details><summary>两处借展作品的收藏机构</summary><p>明尼阿波利斯艺术博物馆与波士顿美术馆为本批两件借展作品的收藏方；两件均在休斯顿亲见，不计为本批的两处到访点。</p>'+grid(['j01','j02'])+'</details></section>'
 b+='<section id="timeline" class="jw-section"><h2>沿年代重看</h2><p>横轴以公元年份定位，短标记为确年，横线为范围／约年；卡片保留原始断代写法。每件独占一行，手机可横向滑动。组合与后配部分的年代仍分别见作品资料。</p><div class="jw-time-scroll" tabindex="0" aria-label="年代图；可横向滚动"><div class="jw-time-axis">'+''.join(f'<span style="left:{(y-700)/1200*100}%">{y}</span>' for y in range(700,1901,100))+'</div>'
 for w in sorted(works,key=lambda w:w['year_start']):
  x=(w['year_start']-700)/1200*100;end=(w['year_end']-700)/1200*100
  b+=f'<div class="jw-time-row" data-related-id="{w["id"]}"><a class="jw-time-label" href="{href(w)}">{e(w["publish_title"])}</a><div class="jw-time-plot"><a class="jw-range" style="left:{x:.3f}%;width:{max(end-x,.3):.3f}%" href="{href(w)}" aria-label="{e(w["publish_title"]+w["date_display"])}"></a><a class="jw-time-card" style="left:{min(x,75):.3f}%" href="{href(w)}">{image(full[w["id"]],w["publish_title"],small=True)}<span>{e(w["date_display"])}<small>{e(w["viewing_museum"])}</small></span></a></div></div>'
 b+='</div></section><section id="catalogue" class="jw-section"><h2>完整图录</h2><div class="jw-grid jw-catalogue">'
 for w in works:b+=f'<article id="{w["id"]}" data-record-id="{w["id"]}">'+card(w)+f'<p class="jw-caption">{e(w["materials_summary"])} · {len(w["photos"])+len(w["labels"])}张照片'+(' · <strong>有精读</strong>' if w['id'] in essays else '')+'</p></article>'
 b+='</div></section><section id="context" class="jw-section"><h2>理解作品的历史地点</h2><p>这些地点提供寺院、工房或信仰的背景，不是本批作品一律确定的制作地或出土地。</p><div id="jw-context-map" hidden></div>'
 for f in hist:
  p=f['properties'];b+=f'<details id="context-{p["id"]}"><summary>{e(p["name_zh"])}</summary><p>{e(p["relation_note"])}</p>'+grid(p['record_ids'])+refs([p['source']])+'</details>'
 b+='</section>';write('atlas','所见造像',b)
 # A derived public interaction index, always regenerated from the canonical catalogue.
 public=[{k:w.get(k) for k in ['id','publish_title','date_display','year_start','year_end','period_bucket','category','viewing_museum_id','viewing_museum','collection_museum','accession','artist','materials_summary','personal_highlight']}|{'essay':w['id'] in essays,'search':' '.join(str(w.get(k,'')) for k in ['publish_title','date_display','category','viewing_museum','collection_museum','accession','artist','subject_tags','notes'])} for w in works]
 (BASE/'data/atlas-index.json').write_text(json.dumps(public,ensure_ascii=False)+'\n')
 # Integrate with the existing parent pages; no new parallel Japan entrance.
 p=ROOT/'museum-notes/japanese-art/index.html';s=p.read_text();entry='<section class="jw-parent"><a class="issue-link" href="../japanese-buddhist-sculpture/">'+image(3161,'1269年阿弥陀立像，克利夫兰艺术博物馆',small=True)+f'<div><h2>{TITLE}</h2><p>{SUB}</p><p>六章阅读 · 25篇精读 · 62条作品／组合档案</p><span class="text-link">进入木雕专题</span></div></a></section>'
 s=re.sub(r'<!-- japanese-wood -->.*?<!-- /japanese-wood -->','',s,flags=re.S);s=s.replace('</main>','<!-- japanese-wood -->'+entry+'<!-- /japanese-wood --></main>');s=s.replace('从松声与月影开始，留下纸墨之间的相遇。','从纸墨到木胎与金彩，留下在日本艺术中的相遇。');p.write_text(s)
 p=ROOT/'museum-notes/index.html';s=p.read_text();s=s.replace('松声与月影：从中世墨迹到近代观音画，看字、画与留白如何相遇。','从禅宗书画到日本佛教木雕，在纸墨、木胎与金彩之间观看。');s=re.sub(r'首辑：日本禅宗书画 · \d+件／组','禅宗书画 · 东瀛佛影',s)
 s=re.sub(r'<!-- japanese-wood-home -->.*?<!-- /japanese-wood-home -->','',s,flags=re.S);s=s.replace('<!-- /japanese-home -->',f'<!-- /japanese-home --><!-- japanese-wood-home --><p class="featured-note"><a href="japanese-buddhist-sculpture/">新辑：{TITLE}｜日本佛教木雕</a></p><!-- /japanese-wood-home -->');p.write_text(s)
 print(f'Japanese sculpture: {len(works)} records, {len(essays)} readings, 6 chapters, {len(media)} originals, {len(museums)} viewing museums.')
if __name__=='__main__':build()
