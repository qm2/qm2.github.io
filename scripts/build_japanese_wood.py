"""Japanese sculpture notebook: structured intake, complete readings, shared CDN photographs."""
from pathlib import Path
from html import escape as e
import csv,json,re
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/japanese-buddhist-sculpture';URL='/museum-notes/japanese-buddhist-sculpture/'
TITLE='东瀛佛影';SUB='日本佛教木雕：木胎、金彩与亲见札记'
def build():
 load=lambda n:json.loads((BASE/'data'/n).read_text())
 museum_readings=load('museum-reading-notes.json');compare_readings=load('comparison-readings.json');makers=load('makers.json');maker_by={m['id']:m for m in makers};history_guide=load('history-guide.json');display_notes=load('display-notes.json');works=load('catalogue.json');by={w['id']:w for w in works};media=load('media.json');sources=json.loads((BASE/'research/source_registry.json').read_text());essays={x['work_id']:x for x in load('essays.json')};chapters=load('chapters.json');comparisons=load('comparisons.json');selection=load('selections.json');museums=load('viewing-museums.geojson')['features'];hist=load('historical-context.geojson')['features']
 # Keep canonical source photo mappings; the full-body display choice is editorial only.
 full={w['id']:w['main_photo'] for w in works};full['j19']=3152
 caps={3135:'侧看三尊、飞天与展厅中的间距',3146:'展厅远景：坐像与周围空间',3147:'面容、双手与坐姿近照',3151:'地藏面容与胸前衣褶近照',3152:'地藏立像全貌，玻璃反光保留',3157:'面容、衣纹与光背近照',3162:'胸腹以下层叠衣纹与金色细线',3163:'侧面：手势与衣服离开身体的距离',3164:'背面：袈裟沿身体垂下',3165:'衣饰近照：细密纹样与衣缘',3168:'侧面：坐椅、宽袍与头部轮廓',3171:'侧面：身体、莲座与光背',3172:'斜侧面：抬手与坐姿',3173:'台座近照：莲瓣与下方结构',3174:'面部、胸前衣褶及残存金饰',3205:'上半身与镂空光背近照',3206:'面容、举手与光背近照',3207:'垂落衣褶近照',3210:'背面：躯干、衣褶与残存彩饰',3232:'面容、胸腹与双手近照',3242:'侧看云座上的三尊',3243:'三尊与云气近照',3247:'仁王一对中的一尊',3248:'仁王一对中的另一尊',3251:'绕到背后：袈裟展开的形状',3252:'侧面：锡杖与身体的关系',3253:'背部袈裟近照：纹样的分区',3254:'前侧衣纹与装饰近照',3257:'佛坛打开后的内部空间',3258:'中央佛像与供具近照',3259:'中央佛像、莲座与悬挂饰件'}
 def href(w):return URL+(w if isinstance(w,str) else w['id'])+'/'
 def image(n,alt,eager=False,small=False,wide=False):
  p=media[str(n)];vs=p['variants'];return f'<img src="{vs[0 if small else min(1,len(vs)-1)]["url"]}" srcset="'+', '.join(f'{x["url"]} {x["width"]}w' for x in vs)+f'" sizes="{("(max-width:650px) 43vw, 260px" if small else "(max-width:1100px) 92vw, 1050px" if wide else "(max-width:650px) 92vw, 650px")}" width="{p["width"]}" height="{p["height"]}" alt="{e(alt)}" loading="{("eager" if eager else "lazy")}" '+('fetchpriority="high" ' if eager else '')+'decoding="async">'
 def figure(n,w,cap=None,eager=False):
  cap=cap or ('合照后方的胸像' if w['id']=='j04' else '合照前方的坐像' if w['id']=='j05' else caps.get(n,'现场全貌'));txt=f'{w["publish_title"]} · {cap}｜Merton摄于{w["viewing_museum"]}'
  return f'<figure class="jw-figure"><a data-photo href="{media[str(n)]["original_url"]}" data-caption="{e(txt)}">{image(n,txt,eager,wide=w["id"]=="j12")}</a><figcaption>{e(cap)}</figcaption></figure>'
 def card(w):
  relation='<span class="jw-image-relation">'+e(w['image_relation'])+'</span>' if w.get('image_relation') else ''
  note='<small class="jw-date-note">'+e(w['date_note'])+'</small>' if w.get('date_note') else ''
  return f'<a class="jw-card" href="{href(w)}">{image(full[w["id"]],w["publish_title"]+" · "+w["viewing_museum"],small=True)}<h3>{e(w["publish_title"])}</h3>{relation}<p>{e(w["date_short"])}</p>{note}<p>{e(w["viewing_museum"])}</p></a>'
 def grid(ids):return '<div class="jw-grid">'+''.join(card(by[x]) for x in dict.fromkeys(ids))+'</div>'
 def heading(t,sub=''):return f'<header class="jw-heading"><p class="eyebrow">JAPANESE BUDDHIST SCULPTURE</p><h1>{e(t)}</h1><p class="jw-deck">{e(sub)}</p></header>'
 def shell(t,body,slug='',cover=3161):
  canon='https://qm2.github.io'+URL+(slug+'/' if slug else '')
  nav=''.join(f'<a href="{URL}{u}">{n}</a>' for u,n in [('',TITLE),('#chapters','六章阅读'),('atlas/','地图与图录'),('compare/','并看'),('guide/','历史与工艺')])
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t)} | 博物馆札记 · Merton</title><meta name="description" content="{e(SUB)}。六章阅读、25篇精读与62条亲见作品／组合档案。"><link rel="canonical" href="{canon}"><meta property="og:title" content="{e(t)}"><meta property="og:image" content="{media[str(cover)]['variants'][-1]['url']}"><meta property="og:url" content="{canon}"><link rel="stylesheet" href="/museum-notes/museum.css"><link rel="stylesheet" href="/museum-notes/caravaggio/caravaggio.css"><link rel="stylesheet" href="{URL}wood.css"><script src="/museum-notes/caravaggio/caravaggio.js" defer></script><script src="{URL}wood.js" defer></script></head><body class="jw-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="/museum-notes/">Merton</a><nav aria-label="专题导航">{nav}</nav></header><main class="wrap" id="main"><nav class="breadcrumbs"><a href="/museum-notes/">博物馆札记</a><span>/</span><a href="/museum-notes/japanese-art/">日本艺术</a><span>/</span><a href="{URL}">{TITLE}</a></nav>{body}</main><footer class="site-footer wrap"><a href="{URL}">返回专题</a><a href="{URL}sources/">资料与来源</a><a href="#top">回到顶部</a></footer>{LIGHTBOX}</body></html>'''
 def write(slug,t,body,cover=3161):
  p=BASE/slug;p.mkdir(exist_ok=True,parents=True);(p/'index.html').write_text(shell(t,body,slug,cover))
 def source_url(k):
  s=sources[k]
  if k.startswith('L'):return media[k[1:]]['original_url']
  return s.get('url')
 def inline(s):
  s=e(s);tokens=[]
  def keep(html):tokens.append(html);return f'@@TOKEN{len(tokens)-1}@@'
  s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:keep(f'<a href="{m[2]}">{m[1]}</a>'),s)
  s=re.sub(r'\[((?:S-|U-)[A-Z0-9-]+|L\d+)\]',lambda m:keep(f'<a class="jw-cite" href="{URL}sources/#{m[1]}" title="{e(sources[m[1]]["title"])}">[{"展签" if m[1].startswith("L") else "资料"}]</a>'),s)
  s=re.sub(r'j\d{2}',lambda m:keep(f'<a href="{href(m[0])}">{e(by[m[0]]["short_title"])}</a>'),s)
  for name,mid in [('康俊（Kōshun）','koshun'),('定朝（Jōchō）','jocho'),('快庆（Kaikei／快慶）','kaikei')]:
   s=s.replace(name,keep(f'<a href="{URL}guide/#maker-{mid}">{name}</a>'))
  s=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',s)
  return re.sub(r'@@TOKEN(\d+)@@',lambda m:tokens[int(m[1])],s)
 def diagram():
  return '<figure class="jw-concept"><svg viewBox="0 0 680 210" role="img" aria-label="寄木概念：多块木材，局部掏空，再组合并施表面层；不是任何一件作品的剖面复原"><g fill="#d7c6a7" stroke="#826944" stroke-width="2"><rect x="30" y="30" width="65" height="110"/><rect x="112" y="30" width="65" height="110"/><path d="M260 30h65v110h-65z M270 45v80h40V45z" fill-rule="evenodd"/><path d="M342 30h65v110h-65z M352 45v80h40V45z" fill-rule="evenodd"/><rect x="500" y="30" width="130" height="110" rx="12"/></g><path d="M565 34v102" stroke="#826944" stroke-dasharray="4 4"/><g fill="#403c33" text-anchor="middle" font-size="17"><text x="104" y="177">多块木材</text><text x="334" y="177">局部掏空</text><text x="565" y="177">接合与表面整饰</text></g></svg><figcaption>寄木的技术概念，本站绘制。方块仅说明材料关系，不表示西雅图像的部件数量、接缝或实际剖面；工序概述据西雅图馆方。</figcaption></figure>'
 def markdown(s):
  # Only our reviewed paragraphs/headings/tables, not arbitrary raw HTML.
  chunks=[];buf=[];table=[]
  def flush():
   if buf:chunks.append('<p>'+inline(' '.join(buf))+'</p>');buf.clear()
   if table:
    rows=[x.strip().strip('|').split('|') for x in table];chunks.append('<div class="jw-table"><table><thead><tr>'+''.join('<th>'+inline(x.strip())+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in row)+'</tr>' for row in rows[2:])+'</tbody></table></div>');table.clear()
  for line in s.strip().splitlines():
   if line.startswith('::photo '):
    flush();wid,n,cap=line[8:-2].split(' ',2);chunks.append('<div class="jw-inline-photo'+(' jw-wide' if wid=='j12' else '')+'">'+figure(int(n),by[wid],cap)+'</div>');continue
   if line.startswith('::pair '):
    flush();figs=[]
    for item in line[7:-2].split(' | '):
     wid,n,cap=item.split(' ',2);figs.append(figure(int(n),by[wid],cap))
    chunks.append('<div class="jw-pair">'+''.join(figs)+'</div>');continue
   if line=='::diagram yosegi::':flush();chunks.append(diagram());continue
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
  if w.get('evidence_notes'):fields.append(('资料札记','；'.join(w['evidence_notes'])))
  return '<dl class="jw-facts">'+''.join(f'<div><dt>{k}</dt><dd>{e(str(v))}</dd></div>' for k,v in fields)+'</dl>'
 def maker_info(w):
  credits=w.get('maker_credits',[])
  if not credits:return ''
  h='<details class="jw-sources"><summary>制作者、协作与归属依据</summary>'
  for c in credits:
   m=maker_by[c['maker_id']];h+=f'<h3><a href="{URL}guide/#maker-{m["id"]}">{e(m["display"])}</a></h3><p>{e(c["role"])} · {e(c["attribution"])}。{e(m["identity_status"])}</p>'
  return h+'</details>'
 def overview():
  return '<div class="jw-history-overview">'+''.join(f'<a href="{URL}guide/#era-{h["id"]}">{image(full[h["works"][0]],by[h["works"][0]]["short_title"],small=True)}<strong>{e(h["title"])}</strong><span>{e(h["dates"])}</span></a>' for h in history_guide)+'</div>'
 def history_html():
  h='<section id="history" class="jw-section"><h2>四个历史路标</h2><p>分期帮助定位，作品仍保留各自的年代。平安通常以794—1185年为界；南北朝与室町的政治分期部分重叠。这里按观看问题分组，不将分界当作样式突然改变的时刻。</p>'+overview()
  for era in history_guide:
   h+=f'<details id="era-{era["id"]}" class="jw-era"><summary><strong>{e(era["title"])}</strong> · {e(era["dates"])}</summary><p class="jw-caption">{e(era["china"])}</p><div class="jw-prose"><p>{inline(era["text"])}</p></div>'+grid(era['works'])+refs(era['sources'])+'</details>'
  return h+'</section>'
 def makers_html():
  h='<section id="makers" class="jw-section"><h2>是谁制作了这些像</h2><p>仏师是佛教造像制作者的称谓。主作、协作、推定归属与风格周边分别记录；姓名汉字可靠，也不意味着同名者的全部生平已经确定。</p>'
  for m in makers:
   h+=f'<details id="maker-{m["id"]}" class="jw-maker"><summary>{e(m["display"])}</summary><p>{e(m["note"])}</p><dl class="jw-facts"><div><dt>姓名</dt><dd>{e(m["original_han"] or "汉字待核")} · {e(m["romanized"])}</dd></div><div><dt>活动年代</dt><dd>{e(m["activity"])}</dd></div><div><dt>辨识范围</dt><dd>{e(m["identity_status"])}</dd></div></dl><p>'+ ' · '.join(f'<a href="{href(wid)}">{e(by[wid]["short_title"])}</a>' for wid in m['works'])+'</p>'+refs(m['name_sources'])+'</details>'
  h+='<details id="hokkyo"><summary>法桥、法眼：姓名之外的称号</summary><p>法桥、法眼原属僧位体系，后来也授予仏师等人。CMA阿弥陀的主作康俊记有法桥；金贝尔快庆像的署名研究记有法眼。这些是位阶或称号，不是另一个人的名字，也不能单凭称号断定个人出家经历。</p>'+refs(['S-CMA-AMIDA','S-YALE-KAIKEI','S-OSAKA-HOKKYO'])+'</details></section>'
  return h
 # Home: full figure, personal foreword, concise pathways rather than all records.
 hero=by['j23'];body=heading(TITLE,SUB)+'<div class="jw-hero">'+figure(3161,hero,'完整立像 · 1269年',True)+'</div><section class="jw-prose jw-foreword" aria-label="个人序言">'+reading('content/00-foreword.md')+'</section>'
 body+='<nav class="jw-localnav"><a href="#memories">记忆较深</a><a href="#chapters">六章阅读</a><a href="#readings">25篇细读</a><a href="atlas/">所见地图与年表</a><a href="guide/">怎样看木雕</a></nav>'
 body+='<nav class="jw-pathways" aria-label="从一个问题进入"><a href="compare/#c04">从衣纹进入 · 比较四尊阿弥陀</a><a href="03-pureland/">从信仰进入 · 接引如何成为身体</a><a href="guide/#history">从历史进入 · 四个时代路标</a></nav>'
 body+='<section class="jw-section" id="memories"><p class="eyebrow">PLACES TO RETURN TO</p><h2>记忆较深的形象</h2><p>有时是金线，有时是面容；再看全身，又被一个姿态留住。这里放着我想再回去看的十六件／组。</p>'+grid(selection['user_memorable_ids'])+'</section>'
 chcover={'crossing':'j03','body':'j51','pureland':'j23','wrath':'j01','people':'j24','survival':'j25'}
 body+='<section class="jw-section" id="chapters"><p class="eyebrow">SIX CHAPTERS</p><h2>从跨海的形象，到木像的后来生活</h2><div class="jw-chapters">'
 for ch in chapters[1:7]:
  key=ch['id'][3:];wid=chcover[key];body+=f'<a href="{URL}{ch["id"]}/">{image(full[wid],by[wid]["publish_title"],small=True)}<span class="eyebrow">{ch["id"][:2]}</span><h3>{e(ch["title"])}</h3></a>'
 body+='</div></section><section class="jw-section" id="readings"><h2>二十五篇细读</h2><div class="jw-reading-list">'+''.join(f'<a href="{href(wid)}"><span>{e(by[wid]["short_title"])}</span>{e(x["title"])}</a>' for wid,x in essays.items())+'</div></section>'
 body+='<section class="jw-section jw-entry-pair"><div><h2>所见地图与年表</h2><p>十五处观看馆址，六十二条作品／组合档案。一件作品的年代、收藏地与我看见它的地方，分别留下来。</p><a href="atlas/">打开地图、年代与完整图录</a></div><div><h2>放在一起看</h2><p>同一尊格的不同身体，木与铜的不同重量。十组并看，把衣纹、手印和表面的疑问带回具体作品。</p><a href="compare/">进入十组并看</a><p><a href="guide/">怎样看木雕：观看与工艺</a></p></div></section>'
 write('',TITLE,body)
 # Chapters, all supplied narrative retained.
 for ch in chapters[1:7]:
  key=ch['id'][3:];wid=chcover[key];ids=[w['id'] for w in works if w.get('chapter_id')==key];mentioned=re.findall(r'\bj\d{2}\b',(BASE/ch['file']).read_text().split('\n---')[0]);ids=list(dict.fromkeys(ids+mentioned))
  b=heading(ch['title'])+'<div class="jw-full">'+figure(full[wid],by[wid],eager=True)+'</div><article class="jw-prose">'+reading(ch['file'])+'</article>'+refs(textkeys(ch['file']))+'<section class="jw-section"><h2>本章的作品</h2>'+grid(ids)+'</section>'
  write(ch['id'],ch['title'],b,full[wid])
 ch=chapters[-1];write('guide','历史与工艺：怎样看木雕',heading('历史与工艺','从一处细节，回到整个身体')+'<nav class="jw-localnav"><a href="#history">历史路标</a><a href="#makers">仏师与协作</a><a href="../atlas/#timeline">所见作品年表</a></nav>'+'<article class="jw-prose">'+reading('content/07-looking-and-technique.md')+'</article>'+refs(textkeys('content/07-looking-and-technique.md'))+history_html()+makers_html())
 # Every record has a stable page. Readings interleave actual detail photographs.
 for w in works:
  wid=w['id'];entry=essays.get(wid);b=heading(w['publish_title'],w['date_short'])
  if wid=='j58':b+='<div class="jw-pair">'+''.join(figure(n,w,eager=i==0) for i,n in enumerate(w['photo_numbers']))+'</div>'
  else:b+='<div class="jw-full'+(' jw-wide' if wid=='j12' else '')+'">'+figure(full[wid],w,eager=True)+'</div>'
  b+='<div class="jw-core">'+f'<p>{e(w["materials_summary"])} · {e(w["artist"])}</p><p>收藏：{e(w["collection_museum"])}'+(f'｜亲见：{e(w["viewing_museum"])}' if w['collection_museum']!=w['viewing_museum'] else '')+'</p>'+ (f'<p><a href="#label">{e(w["date_note"])}</a></p>' if w['date_note'] else '')+'</div>'
  extra=[n for n in w['photo_numbers'] if n!=full[wid]] if wid!='j58' else []
  if entry:
   explicit=bool(re.search(r'^::(?:photo|pair|diagram) ',(BASE/entry['file']).read_text(),re.M));placed={int(n) for n in re.findall(r'^::photo j\d{2} (\d+)',(BASE/entry['file']).read_text(),re.M)};extra=[n for n in extra if n not in placed]
   html=reading(entry['file'],True);parts=re.split(r'(?=<h2>)',html);parts=[x for x in parts if x];b+=f'<p class="jw-reading-title">{e(entry["title"])}</p>'
   for idx,part in enumerate(parts):
    b+='<section class="jw-prose">'+part+'</section>'
    if extra and idx<2 and not explicit:
     n=extra.pop(0);b+='<div class="jw-detail">'+figure(n,w)+'</div>'
  else:b+='<div class="jw-prose"><p>'+inline(display_notes.get(wid,w['notes']))+'</p></div>'
  if extra:b+='<section class="jw-section"><h2>再换一个距离</h2><div class="jw-pair">'+''.join(figure(n,w) for n in extra)+'</div></section>'
  b+='<details class="jw-label" id="label"><summary>作品资料与现场展签</summary>'+facts(w)+''.join(figure(p['number'],w,'现场展签') for p in w['labels'])+'</details>'
  b+=maker_info(w)
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
  cr=compare_readings.get(c['id'],{});b+=f'<section class="jw-section compare-group" id="{c["id"]}"><h2>{e(c["title"])}</h2><div class="jw-prose"><p>{inline(cr.get("intro",note))}</p></div><div class="'+('jw-back-comparisons' if c['id']=='c08' else 'jw-compare')+'">'
  for wid in c['record_ids']:
   w=by[wid];b+='<div class="jw-comparison-work">'
   if c['id']=='c08':b+=f'<h3><a href="{href(w)}">{e(w["short_title"])}</a></h3><div class="jw-front-back">'+''.join(figure(n,w,cap) for n,cap in zip(cr['pairs'][wid],['正面 · 同件作品','背面 · 同件作品']))+'</div>'
   else:b+=figure(full[wid],w)+f'<h3><a href="{href(w)}">{e(w["short_title"])}</a></h3>'
   b+=f'<p class="jw-caption">{e(w["date_short"])} · {e(w["materials_summary"])}</p>'
   if wid in cr.get('observations',{}):b+='<p class="jw-comparison-note">'+inline(cr['observations'][wid])+'</p>'
   d=cr.get('details',{}).get(wid)
   if d:
    fig=figure(d['photo'],w,d['caption'])
    if 'position'in d:fig=fig.replace('class="jw-figure"',f'class="jw-figure jw-crop" style="--focus:{d["position"]}"')
    b+='<details class="jw-comparison-detail"><summary>再看衣饰局部</summary>'+fig+'</details>'
   b+='</div>'
  if c['id']=='c09':b+='<div class="jw-prose"><figure class="jw-figure"><a data-photo href="/museum-notes/buddhist-sculpture/images/nelson-215.jpg" data-caption="南海观音 · 纳尔逊—阿特金斯艺术博物馆，34-10｜Merton现场摄影"><img src="/museum-notes/buddhist-sculpture/images/nelson-215.jpg" alt="纳尔逊南海观音完整坐姿，Merton摄" width="1279" height="1706" loading="lazy"></a><figcaption>南海观音 · 纳尔逊—阿特金斯艺术博物馆，34-10｜Merton摄；沿用水月观音专题原图。</figcaption></figure><h3><a href="/museum-notes/water-moon-guanyin/#object-215">回到水月观音专题</a></h3><p>从托腮、膝部与支撑的手看起，再把持物与馆方名称放回观察。现有水月观音作品保留各自的记录与页面。</p></div>'

  b+='</div>'
  if cr.get('conclusion'):b+='<div class="jw-prose"><p>'+inline(cr['conclusion'])+'</p></div>'
  keys=re.findall(r'\[((?:S-|U-)[A-Z0-9-]+|L\d+)\]',json.dumps(cr,ensure_ascii=False));b+=refs(keys)+'</section>'
 write('compare','放在一起看',b)
 # Sources retain the supplied study's explicit reading scope.
 b=heading('资料与来源','作品信息据现场展签、馆方记录与相关研究整理')+'<div class="jw-prose"><p>本站照片均为Merton现场拍摄。各来源分别说明研究时实际查阅的范围；索引、摘要与未读书目分别注明，不等同于查阅全文。个人观看与造型分析不冒充馆方定论。</p></div>'
 for k,s in sources.items():
  name='现场展签' if k.startswith('L') else s['title'];u=source_url(k)
  b+=f'<details class="jw-source" id="{k}"><summary>{e(name)}</summary><p>{e(s["access_status"])}</p>'+ (f'<p><a href="{u}">打开'+('展签原图' if k.startswith('L') else '来源')+'</a></p>' if u else '<p>据作者提供的观看或作品对应记录。</p>')+'</details>'
 b+='<section class="jw-prose jw-section"><h2>延伸阅读</h2><p>Nishikawa, Kyotaro & Emily J. Sano, <i>The Great Age of Japanese Buddhist Sculpture, AD 600–1300</i>，Kimbell Art Museum，1982。仅核书目信息，未阅全文；不据此补写单件断代或来源。</p></section>'
 write('sources','资料与来源',b)
 # Atlas: all content is server-rendered; JS adds shared filtering and map selection.
 def options(vals,key=None):return '<option value="">全部</option>'+''.join(f'<option value="{e(v)}">{e(v)}</option>' for v in sorted(set(vals),key=key))
 b=heading('所见造像','博物馆地图 · 年代时间线 · 完整图录')+'<p class="jw-prose">'+str(len(works))+'条作品／组合档案，'+str(len(media))+'张现场照片，'+str(len(museums))+'处实际观看馆址。地图记录观看地点，收藏与历史关联另列；参观日期未由照片文件名推定。</p>'
 b+='<form class="jw-filters" id="jw-filters" hidden><label>找作品、人物或馆藏号<input id="jw-search" type="search" placeholder="例如：阿弥陀、快庆、1269"></label><label>观看馆<select id="jw-museum"><option value="">全部</option>'+''.join(f'<option value="{f["properties"]["id"]}">{e(f["properties"]["name_zh"])}</option>' for f in museums)+'</select></label><label>年代<select id="jw-period">'+options([w['period_bucket'] for w in works],key=lambda v:min(w['year_start'] for w in works if w['period_bucket']==v))+'</select></label><label>形象<select id="jw-subject">'+options([w['category'] for w in works])+'</select></label><label>阅读<select id="jw-reading"><option value="">全部</option><option value="personal">记忆较深</option><option value="essay">有精读</option></select></label><button type="reset">清除条件</button></form><p id="jw-count" aria-live="polite">62条档案</p><p id="jw-empty" hidden>没有符合条件的作品。可以减少筛选条件，或清除后重看。</p>'
 b+='<nav class="jw-localnav"><a href="#map">观看地图</a><a href="#timeline">年代时间线</a><a href="#catalogue">完整图录</a><a href="#context">历史地点</a></nav><section id="map" class="jw-section"><h2>我在哪里看过</h2><div id="jw-map-box" hidden><p class="jw-caption">地图视角（只改变地图范围，保留筛选条件）</p><div class="jw-map-tools"><button type="button" data-map="all">所有馆址</button><button type="button" data-map="america">美国本土</button><button type="button" data-map="east">美国东部</button><button type="button" data-map="texas">德州</button><button type="button" data-map="paris">巴黎</button><button type="button" data-map="hawaii">夏威夷</button></div><p id="jw-map-status" role="status"></p><p id="jw-map-empty" hidden>这个地图视角内没有符合当前条件的馆址。<button type="button" id="jw-map-clear">清除筛选</button>，或选择“所有馆址”。</p><svg id="jw-map" viewBox="0 0 1000 450" role="group" aria-label="博物馆地图；可选择馆址或放大聚合点"></svg><p class="jw-caption">底图：<a href="https://www.naturalearthdata.com/">Natural Earth</a>，公有领域。馆址为约略中心；聚合圆点的数字表示馆址数，不是作品数；点击可放大。地图与以下馆址列表使用同一组记录。</p></div><div class="jw-museums">'
 for f in museums:
  m=f['properties'];ids=[w['id'] for w in works if w['viewing_museum_id']==m['id']]
  b+=f'<details id="museum-{m["id"]}" data-museum-panel="{m["id"]}"><summary>{e(m["name_zh"])} · {e(m["city"])} <span class="jw-museum-count">{len(ids)}条</span></summary><p><a href="{m["website"]}">博物馆官网与馆址</a></p><p>该馆的作品：{inline(museum_readings[m["id"]])}</p><div class="jw-grid">'+''.join(f'<div data-related-id="{wid}">{card(by[wid])}</div>' for wid in ids)+'</div></details>'
 b+='</div><details><summary>两处借展作品的收藏机构</summary><p>明尼阿波利斯艺术博物馆与波士顿美术馆为本批两件借展作品的收藏方；两件均在休斯顿亲见，不计为本批的两处到访点。</p>'+grid(['j01','j02'])+'</details></section>'
 b+='<section id="timeline" class="jw-section"><h2>沿年代重看</h2><p>先从四组代表作定位，再阅读详细年表。实线表示作品的约年或世纪范围，短标记为确年；点线底纹表示宽泛时代归属，分开的两条线表示来源断代不同。分期边界不等于已知制作年，照片也不按实物比例排列。</p>'+overview()+'<div class="jw-time-axis-shell" aria-hidden="true"><div class="jw-time-axis">'+''.join(f'<span style="left:{(y-700)/1200*100}%">{y}</span>' for y in range(700,1901,100))+'</div></div><div class="jw-time-scroll" tabindex="0" aria-label="详细年代图，可横向滑动；纵向随整页滚动">'
 for w in sorted(works,key=lambda w:w['year_start']):
  x=(w['year_start']-700)/1200*100;end=(w['year_end']-700)/1200*100
  range_class='jw-range'
  if w['year_start']==w['year_end']:range_class+=' jw-exact'
  if w['id']=='j17':range_class+=' jw-period-range'
  bars=f'<a class="{range_class}" style="left:{x:.3f}%;width:{max(end-x,.3):.3f}%" href="{href(w)}" aria-label="{e(w["date_display"])}"></a>'
  if w['id']=='j42':bars=''.join(f'<a class="jw-range jw-version-range" style="left:{(start-700)/1200*100:.3f}%;width:{99/1200*100:.3f}%;top:{top}px" href="{href(w)}#label" aria-label="{label}"></a>' for start,top,label in [(1000,5,'馆方：11世纪'),(1100,14,'展签：12世纪')])
  b+=f'<div class="jw-time-row" data-related-id="{w["id"]}"><a class="jw-time-label" href="{href(w)}">{image(full[w["id"]],w["short_title"],small=True)}<span>{e(w["short_title"])}<small>{e(w["date_short"])}</small></span></a><div class="jw-time-plot">{bars}<a class="jw-time-card" style="left:{min(x,75):.3f}%" href="{href(w)}"><span>{e(w["date_short"])}<small>{e(w["date_note"] or w["viewing_museum"])}</small></span></a></div></div>'
 b+='</div></section><section id="catalogue" class="jw-section"><h2>完整图录</h2><div class="jw-grid jw-catalogue">'
 for w in works:b+=f'<article id="{w["id"]}" data-record-id="{w["id"]}">'+card(w)+f'<p class="jw-caption">{e(w["materials_summary"])} · {len(w["photos"])+len(w["labels"])}张照片'+(' · <strong>有精读</strong>' if w['id'] in essays else '')+'</p></article>'
 b+='</div></section><section id="context" class="jw-section"><h2>理解作品的历史地点</h2><p>这些地点提供寺院、工房或信仰的背景，不是本批作品一律确定的制作地或出土地。</p><div id="jw-context-map" hidden></div>'
 for f in hist:
  p=f['properties'];b+=f'<details id="context-{p["id"]}"><summary>{e(p["name_zh"])}</summary><p>{e(p["relation_note"])}</p>'+grid(p['record_ids'])+refs([p['source']])+'</details>'
 b+='</section>';write('atlas','所见造像',b)
 # A derived public interaction index, always regenerated from the canonical catalogue.
 public=[{k:w.get(k) for k in ['id','publish_title','date_display','year_start','year_end','period_bucket','category','viewing_museum_id','viewing_museum','collection_museum','accession','artist','materials_summary','personal_highlight']}|{'essay':w['id'] in essays,'search':' '.join(str(w.get(k,'')) for k in ['publish_title','date_display','category','viewing_museum','collection_museum','accession','artist','subject_tags','notes'])} for w in works]
 (BASE/'data/atlas-index.json').write_text(json.dumps(public,ensure_ascii=False)+'\n')
 # Keep the downloadable tabular and timeline views in step with canonical records.
 csvpath=BASE/'data/catalogue.csv'
 with csvpath.open(newline='') as f:
  reader=csv.DictReader(f);columns=reader.fieldnames;rows=list(reader)
 with csvpath.open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=columns,lineterminator="\n");writer.writeheader()
  for row in rows:
   w=by[row['id']];writer.writerow({k:w.get(k,row[k]) if not isinstance(w.get(k),list) else row[k] for k in columns})
 timeline=load('timeline.json')
 for row in timeline:
  w=by[row['id']];row.update({k:w[k] for k in ['date_display','year_start','year_end','viewing_museum_id']});row['title']=w['publish_title'];row['route']=href(w)
 (BASE/'data/timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
 # Integrate with the existing parent pages; no new parallel Japan entrance.
 p=ROOT/'museum-notes/japanese-art/index.html';s=p.read_text();entry='<section class="jw-parent"><a class="issue-link" href="../japanese-buddhist-sculpture/">'+image(3161,'1269年阿弥陀立像，克利夫兰艺术博物馆',small=True)+f'<div><h2>{TITLE}</h2><p>{SUB}</p><p>六章阅读 · 25篇精读 · 62条作品／组合档案</p><span class="text-link">进入木雕专题</span></div></a></section>'
 s=re.sub(r'<!-- japanese-wood -->.*?<!-- /japanese-wood -->','',s,flags=re.S);s=s.replace('</main>','<!-- japanese-wood -->'+entry+'<!-- /japanese-wood --></main>');s=s.replace('从松声与月影开始，留下纸墨之间的相遇。','从纸墨到木胎与金彩，留下在日本艺术中的相遇。');p.write_text(s)
 p=ROOT/'museum-notes/index.html';s=p.read_text();s=s.replace('松声与月影：从中世墨迹到近代观音画，看字、画与留白如何相遇。','从禅宗书画到日本佛教木雕，在纸墨、木胎与金彩之间观看。');s=re.sub(r'首辑：日本禅宗书画 · \d+件／组','禅宗书画 · 东瀛佛影',s)
 s=re.sub(r'<!-- japanese-wood-home -->.*?<!-- /japanese-wood-home -->','',s,flags=re.S);s=s.replace('<!-- /japanese-home -->',f'<!-- /japanese-home --><!-- japanese-wood-home --><p class="featured-note"><a href="japanese-buddhist-sculpture/">新辑：{TITLE}｜日本佛教木雕</a></p><!-- /japanese-wood-home -->');p.write_text(s)
 print(f'Japanese sculpture: {len(works)} records, {len(essays)} readings, 6 chapters, {len(media)} originals, {len(museums)} viewing museums.')
if __name__=='__main__':build()
