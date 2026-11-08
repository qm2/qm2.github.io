"""Build Roman sarcophagi from canonical objects, photographs and reviewed notes."""
from pathlib import Path
from html import escape as e
import json,re
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/roman-sarcophagi'

def build():
 def read(name):return json.loads((BASE/f'data/{name}.json').read_text())
 works=read('works'); by={w['id']:w for w in works};photos=read('photos');notes=read('editorial');sections=read('sections');comparisons=read('comparisons');museums=read('museums');sources=read('sources');history=read('history');sb={s['id']:s for s in sources};sn={s['id']:i+1 for i,s in enumerate(sources)}
 stories=read('stories')
 story_by_work={wid:entry for entry in stories['myths'] for wid in entry['works']}
 def source_links(ids):
  return '<span class="rs-cites">'+''.join(f' <a href="{e(sb[k]["url"])}" title="{e(sb[k]["title"])}" aria-label="来源：{e(sb[k]["title"])}">[{sn[k]}]</a>' for k in dict.fromkeys(ids) if k in sb)+'</span>' if ids else ''
 def paras(items):return ''.join('<p>'+e(p['text'])+source_links(p.get('source_ids',[]))+'</p>' for p in items)
 def image(key,pre='',eager=False,alt=None,sizes='(max-width:650px) 92vw, (max-width:1000px) 80vw, 1080px'):
  p=photos[str(key)];variants=p['variants'];small=min(variants,key=lambda v:abs(v['width']-960));text=alt or p['caption']
  return f'<img src="{pre}images/{small["file"]}" srcset="'+', '.join(f'{pre}images/{v["file"]} {v["width"]}w' for v in variants)+f'" sizes="{sizes}" width="{p["display_width"]}" height="{p["display_height"]}" alt="{e(text)}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
 def figure(key,pre='',caption=None,eager=False):
  key=str(key);p=photos[key];src=photos[p['source']] if p.get('source') else p;cap=caption or p['caption']
  return f'<figure class="rs-photo" style="--photo-width:{p["display_width"]}px"><a data-photo href="{pre}images/{p["full"]}" data-original="{pre}images/originals/{src["original"]}" data-caption="{e(cap)} · Merton摄" aria-label="放大：{e(cap)}">{image(key,pre,eager,cap)}</a><figcaption>{e(cap)} · Merton摄</figcaption></figure>'
 def bibliography(keys):
  return '<ol class="rs-bibliography">'+''.join(f'<li value="{sn[k]}"><a href="{e(sb[k]["url"])}">{e(sb[k]["title"])} ↗</a></li>' for k in dict.fromkeys(keys) if k in sb)+'</ol>'
 def work_sources(w):
  content=notes[w['id']];return list(dict.fromkeys(w.get('source_ids',[])+[k for s in content['sections'] for p in s['paragraphs'] for k in p.get('source_ids',[])]+[k for p in content['notes'] for k in p.get('source_ids',[])]))
 def shell(title,body,depth=0,cover='1925',description=''):
  pre='../'*depth;up='../'*(depth+1);p=photos[cover];share='https://qm2.github.io/museum-notes/roman-sarcophagi/images/'+p['full']
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton · 博物馆札记</title><meta name="description" content="{e(description or '从战争、酒神与英雄的故事，走近古罗马石棺中的人物和纪念。Merton的博物馆现场摄影与札记。')}"><meta property="og:image" content="{share}"><link rel="stylesheet" href="{up}museum.css"><link rel="stylesheet" href="{up}caravaggio/caravaggio.css"><link rel="stylesheet" href="{pre}roman.css"><script src="{up}caravaggio/caravaggio.js" defer></script><script src="{pre}roman.js" defer></script></head><body class="rs-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{up}">Merton</a><nav aria-label="主导航"><a href="{pre or './'}">罗马石棺</a><a href="{pre}history/">历史与观看</a><a href="{pre}stories/">人物与故事</a><a href="{pre}atlas/">所见图录</a><a href="{pre}compare/">并看</a></nav></header><main id="main" class="wrap">{body}</main><footer class="site-footer wrap"><a href="{up}">← 博物馆札记</a><span>现场摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
 def write(route,html):
  target=BASE/route;target.mkdir(exist_ok=True,parents=True);(target/'index.html').write_text(html)
 def card(w,pre='',filterable=False):
  content=notes[w['id']];data=''
  if filterable:data=f' data-record="{w["id"]}" data-museum="{w["museum_id"]}" data-theme="{e(w["theme"])}" data-search="{e(w["title_zh"]+" "+str(w.get("accession") or "")+" "+w["viewing_museum"]+" "+w.get("title_en",w.get("title_original","")))}"'
  return f'<article class="rs-card" id="{w["id"]}"{data}><a class="rs-thumb" href="{pre}{w["id"]}/">{image(w["cover"],pre,alt=w["title_zh"]+(" · 原片局部" if photos[w["cover"]].get("crop") else ""),sizes="(max-width:600px) 92vw, (max-width:900px) 44vw, 350px")}</a><p class="rs-meta">{e(w["date_display"])} · {e(w["viewing_city"])}</p><h3><a href="{pre}{w["id"]}/">{e(w["title_zh"])}</a></h3><p>{e(content["lead"])}</p><p class="rs-meta">{e(w["viewing_museum"])} · {e(str(w.get("accession") or "馆藏号待核"))}</p></article>'
 def gallery(keys,pre,title='从另一个角度看'):
  if not keys:return ''
  return '<section class="rs-gallery" data-rs-gallery><h2>'+e(title)+'</h2><div class="rs-gallery-controls" hidden><button data-prev type="button">上一张</button><span data-count role="status" aria-live="polite"></span><button data-next type="button">下一张</button><button data-all type="button" aria-pressed="false">展开全部</button></div><div class="rs-slides">'+''.join('<div class="rs-slide">'+figure(n,pre)+'</div>' for n in keys)+'</div></section>'
 def facts(w):
  rows=[('年代',w['date_display']),('材料',w.get('material')),('收藏',w['collection']),('观看地点',w['viewing_museum']+' · '+w['viewing_city']),('馆内位置',w.get('viewing_venue')),('馆藏号',w.get('accession') or '待核'),('制作地区',w.get('production_region')),('发现地记录',w.get('findspot'))]
  return '<dl class="rs-facts">'+''.join(f'<div><dt>{e(k)}</dt><dd>{e(str(v))}</dd></div>' for k,v in rows if v)+'</dl>'
 # Independent reading pages.
 for w in works:
  wid=w['id'];content=notes[wid];pre='../';chapter=next(s for s in sections if wid in s['works'])
  body=f'<nav class="breadcrumbs"><a href="../">罗马石棺</a><span>/</span><a href="../#{chapter["id"]}">{e(chapter["title"])}</a></nav><header class="rs-title"><p class="eyebrow">ROMAN SARCOPHAGI / {wid.upper()}</p><h1>{e(w["title_zh"])}</h1><p class="rs-meta">{e(w.get("title_en",w.get("title_original","")))}</p><p class="rs-lead">{e(content["lead"])}</p></header>'
  body+=figure(w['cover'],pre,eager=True)+facts(w)
  entry=story_by_work.get(wid)
  context=stories['context_previews'].get(wid)
  if entry or context:
   anchor=entry['id'] if entry else context['entry'];preview=entry['preview'] if entry else context['text']
   body+='<aside class="rs-reading rs-story-entry"><details><summary>先认识这个故事 <span class="rs-icon" aria-hidden="true">＋</span></summary><p>'+e(preview)+f'</p><a href="../stories/#{anchor}">人物、故事与照片线索 →</a></details></aside>'
  # Images are placed by the relevant reading passage; unused angles stay in the gallery.
  inserts={'r11':{0:['portonaccio-rider']},'r20':{0:['1947','1948','1949'],1:['1950']},'r21':{0:['1957','1958'],1:['1954','1955']},'r13':{2:['1931']},'r15':{0:['1935','1936']}}
  used={w['cover']};body+='<div class="rs-reading">'
  for i,s in enumerate(content['sections']):
   body+='<section><h2>'+e(s['title'])+'</h2>'+paras(s['paragraphs'])+'</section>'
   if i in inserts.get(wid,{}):
    items=inserts[wid][i];body+='<div class="rs-insets">'+''.join(figure(k,pre) for k in items)+'</div>';used.update(items)
  if wid=='r13':
   lid=notes['r13-lid'];body+='<aside class="rs-lid" id="lid-932"><h2>独立的棺盖：Myron一家</h2>'+figure('lid-932',pre)+paras(lid['sections'][0]['paragraphs'])+'<details><summary>棺盖资料注 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+paras(lid['notes'])+'</details></aside>'
  body+='</div>'
  remaining=[k for k in w['photo_order'] if k not in used]
  body+=gallery(remaining,pre)
  if w['labels']:
   body+='<details class="rs-labels" id="labels"><summary>现场展签 · '+str(len(w['labels']))+'张 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+''.join(figure(n,pre) for n in w['labels'])+'</details>'
  body+='<section class="rs-reading rs-documentation"><h2>资料与来源</h2>'
  if content['notes']:body+='<details><summary>断代、收藏与文献说明 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+paras(content['notes'])+'</details>'
  body+=bibliography(work_sources(w))+'</section>'
  related=[g for g in comparisons if wid in g['works']]
  if related:
   body+='<section class="rs-related"><h2>放在一起看</h2>'+''.join(f'<p><a href="../compare/#{g["id"]}">{e(g["title"])} →</a></p>' for g in related)+'</section>'
  body+=f'<p class="rs-return"><a href="../#{chapter["id"]}">← {e(chapter["title"])}</a>　<a href="../atlas/#{wid}">在完整图录中找这件 →</a>　<a href="../history/">历史与观看 →</a></p>'
  write(wid,shell(w['title_zh'],body,1,w['cover'],content['lead']))
 # Topic home.
 hero=by['r11']
 body='''<header class="rs-title rs-home-title"><p class="eyebrow">ROMAN SARCOPHAGI / 古罗马浮雕石棺</p><h1>石棺上的故事</h1><p class="subtitle">我在博物馆看过的古罗马浮雕石棺</p></header>'''
 body+=figure('1925',caption='波尔托纳乔战争石棺 · 180—190年 · 罗马国家博物馆马西莫宫 · 112327',eager=True)
 body+='''<div class="rs-preface"><p>在罗马国家博物馆看到波尔托纳乔石棺时，最震撼我的是那些密密麻麻、高低起伏的战争场景。人和马彼此挤压，身体从石面里凸出来，又陷入深暗的缝隙。远看是一整片翻动的形体，靠近才逐渐分出骑兵、俘虏与倒下的人。</p><p>休斯顿的几件石棺则有另一种亲近感。我看过它们很多次，仍然喜欢这些交错的身体、衣褶和神话人物。这一页把不同博物馆里的石棺放到一起，也为重看留一条路。</p></div>'''
 body+='<nav class="rs-chapter-nav" aria-label="五条阅读线索">'+''.join(f'<a href="#{s["id"]}"><span>{i+1:02d}</span> {e(s["title"])}</a>' for i,s in enumerate(sections))+'<a href="atlas/">所见图录与地图 ↗</a></nav>'
 body+='<section class="rs-guide-entry" id="history"><p class="eyebrow">HISTORY &amp; LOOKING</p><h2>历史与观看</h2><p>为什么葬具上有欢乐、爱情和战争？从现有作品出发，读墓葬中的纪念、工坊的制作与图像的变化。</p><div class="rs-link-row"><a href="history/">打开导读 →</a><a href="history/#field-card">带着六个问题看下一件 →</a><a href="stories/">人物与故事：九组神话与五条生活线索 →</a></div></section>'
 for i,s in enumerate(sections):
  w=by[s['featured']];body+=f'<section class="rs-chapter" id="{s["id"]}"><div class="rs-section-title"><p class="eyebrow">{i+1:02d} / READ THE RELIEF</p><h2>{e(s["title"])}</h2><p>{e(s["intro"])}</p></div>'
  if w['id']=='r11':body+='<div class="rs-feature-copy"><h3><a href="r11/">波尔托纳乔：一张没有完成的脸</a></h3><p>'+e(notes['r11']['lead'])+'</p><a class="text-link" href="r11/">从中央骑手，读到棺盖的人生场景 →</a></div>'
  else:body+='<div class="rs-feature">'+figure(w['cover'],caption=w['title_zh']+' · '+w['date_display']+' · '+w['viewing_museum'])+'<div class="rs-feature-copy"><h3><a href="'+w['id']+'/">'+e(w['title_zh'])+'</a></h3><p>'+e(notes[w['id']]['lead'])+'</p><a class="text-link" href="'+w['id']+'/">进入这件作品 →</a></div></div>'
  others=[by[k] for k in s['works'] if k!=w['id']]
  body+='<div class="rs-grid">'+''.join(card(o) for o in others)+'</div></section>'
 body+=f'<section class="rs-atlas-entry"><p class="eyebrow">ATLAS / TIMELINE / CATALOGUE</p><h2>所见石棺</h2><p>{len(works)}条作品记录，另附一件独立棺盖；来自{len(museums)}处观看机构。按博物馆、年代和题材重新浏览，也把不同地方看过的作品放在一起比较。</p><div class="rs-link-row"><a href="atlas/">打开地图、时间线与完整图录 →</a><a href="compare/">{len(comparisons)}组并看 →</a></div></section>'
 body+='<details class="rs-directory"><summary>逐件目录 <span class="rs-icon" aria-hidden="true">＋</span></summary><ol>'+''.join(f'<li><a href="{w["id"]}/">{e(w["title_zh"])}</a><span>{e(w["date_display"])} · {e(w["viewing_city"])}</span></li>' for w in works)+'</ol></details>'
 body+='<section class="rs-reading rs-documentation"><h2>照片与资料</h2><p>本辑照片均为我的现场摄影。作品资料依据现场展签、馆藏目录与所附研究；四件托洛尼亚藏品是在卢浮宫借展时看到的，观看地点与收藏归属分别记录。每件作品保留原图及已有展签。</p><p>梵蒂冈的陈列包含独立的棺身、棺盖和前板；目录按文物记录整理，共用的现场照片只存一份。</p>'+bibliography(['S29','S15','S05'])+'</section>'
 write('',shell('石棺上的故事 · 古罗马浮雕石棺',body))
 # Fixed comparison groups, no third-party photos, native ratios.
 body='<header class="rs-title"><p class="eyebrow">SIDE BY SIDE</p><h1>让石棺彼此照见</h1><p class="rs-lead">比较人物的手、身体的方向，以及故事在石面上展开的方式。</p><p class="rs-meta">照片保持各自比例，并排不表示实物等大。具体年代与资料见作品页。</p></header><nav class="rs-link-row">'+''.join(f'<a href="#{g["id"]}">{e(g["title"])}</a>' for g in comparisons)+'</nav>'
 for g in comparisons:
  body+=f'<section class="compare-group rs-comparison" id="{g["id"]}"><h2>{e(g["title"])}</h2><p>{e(g["text"])}</p><div class="rs-compare-grid">'
  for wid in g['works']:
   w=by[wid];body+='<div>'+figure(w['cover'],'../',g.get('captions',{}).get(wid,w['title_zh']+' · '+w['date_display']))+f'<p><a href="../{wid}/">{e(w["viewing_museum"])} · 阅读札记 →</a></p></div>'
  body+='</div>'
  if g.get('sections'):
   body+='<div class="rs-reading rs-comparison-reading">'+''.join('<section><h3>'+e(s['title'])+'</h3>'+paras(s['paragraphs'])+'</section>' for s in g['sections'])
   if g.get('notes'):body+='<details><summary>题名与人物归属 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+paras(g['notes'])+'</details>'
   keys=[k for s in g['sections'] for p in s['paragraphs'] for k in p.get('source_ids',[])]+[k for p in g.get('notes',[]) for k in p.get('source_ids',[])]
   body+='<h3>这一组的来源</h3>'+bibliography(keys)+'<p><a href="../history/#stories">继续读：墓中的故事与纪念 →</a></p></div>'
  body+='</section>'
 write('compare',shell('石棺并看',body,1))
 # Reading guide: structured prose and a reusable field card, using existing photographs.
 body='<nav class="breadcrumbs"><a href="../">罗马石棺</a><span>/</span><span>历史与观看</span></nav><header class="rs-title"><p class="eyebrow">HISTORY &amp; LOOKING</p><h1>'+e(history['title'])+'</h1><p class="subtitle">'+e(history['subtitle'])+'</p><p class="rs-lead">'+e(history['intro'])+'</p></header>'
 body+='<nav class="rs-link-row rs-guide-nav" aria-label="导读章节">'+''.join(f'<a href="#{s["id"]}">{e(s["title"])}</a>' for s in history['sections'])+'<a href="#field-card">现场观看卡 ↓</a><a href="../stories/">查阅人物与故事 →</a></nav><article class="rs-reading rs-history">'
 history_sources=[]
 for s in history['sections']:
  body+=f'<section id="{s["id"]}"><h2>{e(s["title"])}</h2>'
  if s.get('image'):body+=figure(s['image'],'../',s['caption'])
  body+=paras(s['paragraphs'])
  history_sources.extend(k for p in s['paragraphs'] for k in p.get('source_ids',[]))
  if s.get('table'):
   t=s['table'];body+='<div class="rs-guide-table" tabindex="0" role="region" aria-label="三种制作传统比较，窄屏可横向浏览"><table><caption>'+e(t['caption'])+source_links(t['source_ids'])+'</caption><thead><tr>'+''.join('<th scope="col">'+e(v)+'</th>' for v in t['headers'])+'</tr></thead><tbody>'
   for row in t['rows']:body+='<tr><th scope="row">'+e(row[0])+'</th>'+''.join('<td>'+e(v)+'</td>' for v in row[1:])+'</tr>'
   body+='</tbody></table></div><p class="rs-table-hint">左右滑动表格，查看“观看方式”一栏 →</p>';history_sources.extend(t['source_ids'])
  body+=paras(s.get('after',[]))
  history_sources.extend(k for p in s.get('after',[]) for k in p.get('source_ids',[]))
  body+='<p class="rs-guide-works">回到作品：'+''.join(f'<a href="../{wid}/">{e(by[wid]["title_zh"])}</a>' for wid in s['works'])+'</p></section>'
 field=history['field_card'];body+='</article><section class="rs-reading rs-field-card" id="field-card"><p class="eyebrow">TAKE A CLOSER LOOK</p><h2>'+e(field['title'])+'</h2><p>'+e(field['intro'])+'</p><ol>'
 for item in field['questions']:body+='<li><h3>'+e(item['question'])+'</h3><p>'+e(item['text'])+f' <a href="../{item["link"]}">{e(item["label"])} →</a></p></li>'
 body+='</ol><p class="rs-photo-checklist">'+e(field['photography'])+'</p><p><a href="../atlas/">回到所见图录 →</a></p></section>'
 body+='<section class="rs-reading rs-documentation"><h2>资料与来源</h2><details><summary>本页的阅读依据 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+''.join('<p>'+e(p)+'</p>' for p in history['reading_notes'])+'</details>'+bibliography(history_sources)+'</section><p class="rs-return"><a href="../">← 石棺上的故事</a>　<a href="../compare/#battle-and-submission">交战与降服：两件并看 →</a></p>'
 write('history',shell('历史与观看 · 罗马石棺',body,1,'1940',history['intro']))
 # Reusable story reference: no duplicate objects or third-party photographs.
 def story_works(ids,pictures=None):
  out='<div class="rs-story-works">'
  for wid in ids:
   w=by[wid];pic=(pictures or {}).get(wid,{});key=pic.get('photo',w['cover']);caption=pic.get('caption',w['title_zh']+(' · 原片局部' if photos[key].get('crop') else ''))
   out+='<div>'+figure(key,'../',caption)+f'<h4><a href="../{wid}/">{e(w["title_zh"])} →</a></h4><p class="rs-meta">{e(w["viewing_museum"])}'
   if w['labels']:out+=f' · <a href="../{wid}/#labels">现场展签</a>'
   out+='</p></div>'
  return out+'</div>'
 body='<nav class="breadcrumbs"><a href="../">罗马石棺</a><span>/</span><span>人物与故事</span></nav><header class="rs-title"><p class="eyebrow">PEOPLE &amp; STORIES</p><h1>'+e(stories['title'])+'</h1><p class="rs-lead">'+e(stories['intro'])+'</p></header>'
 body+='<nav class="rs-story-directory" aria-label="人物与故事条目"><div><h2>九组神话</h2><ol>'+''.join(f'<li><a href="#{s["id"]}">{e(s["title"])}</a></li>' for s in stories['myths'])+'</ol></div><div><h2>罗马生活与纪念</h2><ul>'+''.join(f'<li><a href="#{s["id"]}">{e(s["title"])}</a></li>' for s in stories['contexts'])+'</ul><p><a href="../history/">历史与观看 →</a></p></div></nav><div class="rs-reading rs-stories">'
 keys=[]
 for s in stories['myths']:
  body+=f'<details class="rs-story" id="{s["id"]}"><summary><span class="rs-story-heading"><span class="rs-story-name">{e(s["title"])}</span><span class="rs-story-cue">速记：{e(s["recap"])}</span></span><span class="rs-icon" aria-hidden="true">＋</span></summary><div class="rs-story-content"><p class="rs-story-names">{e(s["names"])}</p>'
  if s.get("relationships"):body+='<p class="rs-story-relationships"><strong>人物关系：</strong>'+e(s["relationships"])+'</p>'
  body+='<h3>故事里发生了什么</h3>'+paras([s['story']])+'<h3>在我的石棺上找什么</h3><p>'+e(s['cue'])+'</p><ul class="rs-looking">'
  for look in s['look']:body+='<li>'+e(look['text'])+source_links(look.get('source_ids',[]))+'</li>'
  body+='</ul>'+story_works(s['works'],s.get('pictures'))+'<h3>版本与解读</h3>'+paras(s['version'])
  if s['id']=='apollo-muses':
   mt=stories['muses'];body+='<details id="nine-muses"><summary>九缪斯：姓名、领域与常见属性 <span class="rs-icon" aria-hidden="true">＋</span></summary><p>'+e(mt['intro'])+source_links(mt['source_ids'])+'</p><div class="rs-guide-table rs-muses-table" tabindex="0" role="region" aria-label="九缪斯对照表，窄屏可横向浏览"><table><caption>九缪斯对照</caption><thead><tr><th scope="col">姓名</th><th scope="col">领域</th><th scope="col">常见属性</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+e(row[0])+'</th><td>'+e(row[1])+'</td><td>'+e(row[2])+'</td></tr>' for row in mt['rows'])+'</tbody></table></div></details>';keys+=mt['source_ids']
  keys+=[k for paragraph in [s['story']]+s['look']+s['version'] for k in paragraph.get('source_ids',[])]
  body+='<p class="rs-story-back"><a href="#main">回到条目目录 ↑</a>　<a href="../history/#stories">故事为何进入墓葬 →</a></p></div></details>'
 body+='<h2 id="roman-life">罗马生活与纪念</h2><p>神话之外，手势与持物也让家庭、公共事务和理想人格进入身后记忆。</p>'
 for s in stories['contexts']:
  body+=f'<details class="rs-story rs-context" id="{s["id"]}"><summary><span class="rs-story-name">{e(s["title"])}</span><span class="rs-icon" aria-hidden="true">＋</span></summary><div class="rs-story-content">'+paras([s['text']])+story_works(s['works'])+f'<p><a href="../history/#{s["history"]}">继续读：历史与观看 →</a>　<a href="#main">回到目录 ↑</a></p></div></details>'
  keys+=s['text']['source_ids']
 body+='</div><section class="rs-reading rs-documentation"><h2>资料与来源</h2><details><summary>阅读范围与版本说明 <span class="rs-icon" aria-hidden="true">＋</span></summary>'+''.join('<p>'+e(t)+'</p>' for t in stories['reading_notes'])+'</details>'+bibliography(keys)+'</section><p class="rs-return"><a href="../">← 石棺上的故事</a>　<a href="../history/">历史与观看 →</a>　<a href="../atlas/">所见图录 →</a></p>'
 write('stories',shell('人物与故事 · 罗马石棺',body,1,'1940',stories['intro']))
 # Atlas: one canonical object list feeds map, dates, and cards.
 def map_svg(region,bounds):
  x0,x1,y0,y1=bounds; width,height=540,260
  def xy(lon,lat):return ((lon-x0)/(x1-x0)*width,(y1-lat)/(y1-y0)*height)
  land=json.loads((ROOT/'museum-notes/homer/data/ne_110m_land.geojson').read_text());paths=[]
  for f in land['features']:
   coords=f['geometry']['coordinates']; polys=coords if f['geometry']['type']=='MultiPolygon' else [coords]
   for poly in polys:
    for ring in poly:
     if not any(x0<=p[0]<=x1 and y0<=p[1]<=y1 for p in ring):continue
     paths.append('M'+'L'.join(f'{xy(*p)[0]:.1f},{xy(*p)[1]:.1f}' for p in ring)+'Z')
  out=f'<svg viewBox="0 0 {width} {height}" role="group" aria-label="{region}观看地点"><defs><clipPath id="clip-{region}"><rect width="540" height="260"/></clipPath></defs><g clip-path="url(#clip-{region})"><path class="rs-land" d="'+''.join(paths)+'"/></g>'
  for m in museums:
   if not (x0<=m['lon']<=x1 and y0<=m['lat']<=y1):continue
   x,y=xy(m['lon'],m['lat']);dx,dy=(0,0)
   if m['city']=='罗马':dx,dy=0,0
   if '梵蒂冈' in m['city']:dx,dy=0,0
   textx=x+dx+8; texty=y+dy+4; anchor='start'
   if m['city']=='罗马':texty=y-7
   if '梵蒂冈' in m['city']:texty=y+17
   if textx>480:textx=x+dx-8;anchor='end'
   count=sum(w['museum_id']==m['id'] for w in works)
   out+=f'<a href="?museum={m["id"]}#catalogue" data-map-museum="{m["id"]}" aria-label="{e(m["name"])}：{count}条记录"><title>{e(m["name"])} · {count}条记录</title><line x1="{x}" y1="{y}" x2="{x+dx}" y2="{y+dy}"/><circle cx="{x+dx}" cy="{y+dy}" r="6"/><text x="{textx}" y="{texty}" text-anchor="{anchor}">{e(m["city"])}</text></a>'
  return out+'</svg>'
 body=f'<header class="rs-title"><p class="eyebrow">ATLAS &amp; TIMELINE</p><h1>所见石棺</h1><p class="rs-lead">从{len(museums)}处博物馆的相遇，回到人物、题材与年代。</p><p>共{len(works)}条作品记录，另附独立棺盖932。地图表示观看地点；古代制作地区与发现地记录见各作品页。</p></header>'
 body+='<p class="rs-field-entry"><a href="../history/#field-card">现场观看卡：六个问题与拍摄记录 →</a></p>'
 body+='<section id="map"><h2>在这些地方相遇</h2><div class="rs-maps"><div><h3>北美</h3>'+map_svg('north-america',(-105,-70,23,47))+'</div><div><h3>欧洲</h3>'+map_svg('europe',(-6,25,36,54))+'</div></div><p class="rs-meta">城市区域示意；罗马与梵蒂冈在此比例下接近重合，馆名可分别选择。底图：<a href="https://www.naturalearthdata.com/about/terms-of-use/">Natural Earth，公共领域</a>。点击地点筛选，或使用下方馆名列表。</p><div class="rs-museum-list">'+''.join(f'<a href="?museum={m["id"]}#catalogue" data-map-museum="{m["id"]}">{e(m["name"])} <span>{sum(w["museum_id"]==m["id"] for w in works)}</span></a>' for m in museums)+'</div></section>'
 body+='<section class="rs-atlas-controls" aria-label="筛选图录"><label>搜索题名或编号<input id="rs-search" type="search" placeholder="如：缪斯、墨勒阿格洛斯"></label><label>观看机构<select id="rs-museum"><option value="all">全部机构</option>'+''.join(f'<option value="{m["id"]}">{e(m["name"])}</option>' for m in museums)+'</select></label><label>题材<select id="rs-theme"><option value="all">全部题材</option>'+''.join(f'<option>{e(t)}</option>' for t in dict.fromkeys(w['theme'] for w in works))+'</select></label><button id="rs-clear" type="button">清除条件</button><p id="rs-results" role="status" aria-live="polite"></p></section>'
 body+='<details class="rs-timeline"><summary>沿年代重看 <span class="rs-icon" aria-hidden="true">＋</span></summary><p>全部为公元纪年。线段表示馆录给出的区间；圆点标示约年。宽时段作品以空心标记帮助定位，具体年代始终以文字为准；窄屏可横向浏览。</p><div class="rs-time-scroll" tabindex="0" aria-label="年代时间线，可横向滚动"><div class="rs-time-axis"><span>公元</span><div>'+''.join(f'<b style="left:{(year-100)/250*100}%">{year}</b>' for year in range(100,351,50))+'</div></div>'
 for w in sorted(works,key=lambda w:w['date_anchor']):
  x=(w['date_anchor']-100)/250*100;start=(w['date_start']-100)/250*100;length=(w['date_end']-w['date_start'])/250*100
  mark=f'<i class="rs-time-range {"approx" if "circa" in w["date_kind"] else ""}" style="left:{start}%;width:{length}%"></i>' if w['date_kind'] in ['range','circa_range'] else f'<i class="rs-time-dot {"period" if w["date_kind"]=="period" else ""}" style="left:{x}%"></i>'
  body+=f'<a class="rs-time-row" data-time-record="{w["id"]}" href="../{w["id"]}/"><span>{image(w["cover"],"../",sizes="76px")}<span>{e(w["title_zh"])}<small>{e(w["date_display"])} · {e(w["viewing_city"])}</small></span></span><div>{mark}</div></a>'
 body+='</div></details><section id="catalogue"><h2>完整图录</h2><p id="rs-empty" hidden>没有符合当前条件的记录。</p><div class="rs-grid">'+''.join(card(w,'../',True) for w in works)+'</div></section>'
 pending=[k for k,p in photos.items() if p['role']=='unresolved']
 if pending:body+='<details class="rs-pending"><summary>另有一组陈列待核 <span class="rs-icon" aria-hidden="true">＋</span></summary><p>这组陈列与914、932、933号不同，具体编号尚未确认。</p>'+''.join(figure(k,'../') for k in pending)+'</details>'
 body+='<p class="rs-return"><a href="../">← 返回石棺上的故事</a>　<a href="../compare/">进入并排比较 →</a></p>'
 write('atlas',shell('所见石棺 · 地图与年代',body,1))
 # Idempotent entrance in the existing homepage, no extra empty category page.
 home=ROOT/'museum-notes/index.html';s=home.read_text();s=re.sub(r'<!-- roman-entry -->.*?<!-- /roman-entry -->','',s,flags=re.S)
 entry=f'<a class="issue-link" href="roman-sarcophagi/"><img src="roman-sarcophagi/images/1925-960.webp" width="{photos["1925"]["display_width"]}" height="{photos["1925"]["display_height"]}" alt="波尔托纳乔战争石棺，密集交叠的人物与马匹" loading="lazy"><div><p class="eyebrow">CLASSICAL ART / ROMAN SARCOPHAGI</p><h2>石棺上的故事</h2><p>从罗马的战争场景，看到休斯顿反复相遇的神话人物。沿着身体、手势与衣褶，读石棺上的纪念。</p><p class="issue-meta">古罗马浮雕石棺 · 五条阅读线索<br>{len(works)}条作品记录 · 地图 / 年代 / 并看</p><span class="text-link">走进这个专题 →</span></div></a>'
 anchor='</section>\n<section class="future-collections"';assert anchor in s;s=s.replace(anchor,'<!-- roman-entry -->'+entry+'<!-- /roman-entry -->'+anchor,1)
 s=re.sub(r'<li><h3>古希腊与罗马艺术</h3>.*?</li>','',s,flags=re.S);home.write_text(s)
 print(f'Built Roman sarcophagi: {len(works)} pages, home, comparisons, atlas, history, stories; {len(photos)} photo/crop records.')

if __name__=='__main__':build()
