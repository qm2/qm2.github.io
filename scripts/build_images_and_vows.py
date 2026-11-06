"""Rebuild Images and Vows from audited works, published inscriptions and personal photos."""
from pathlib import Path
from html import escape as e
import json,re
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/images-and-vows'

def build(integrate=True):
 read=lambda n:json.loads((BASE/'data'/n).read_text())
 works=read('works.json'); by={w['id']:w for w in works}; photos=read('photos.json');sources={s['source_id']:s for s in read('sources.json')};ed=read('editorial.json')
 used=[]
 def cite(ids):
  for k in ids:
   assert k in sources,k
   if k not in used:used.append(k)
  return ' '.join(f'<a class="iv-cite" href="#ref-{k}" aria-label="来源：{e(sources[k]["title"])}">[{used.index(k)+1}]</a>' for k in dict.fromkeys(ids))
 def para(p):return '<p>'+e(p['text'])+' '+cite(p.get('sources',[]))+'</p>'
 def img(n,pre='',small=False,eager=False,alt=''):
  p=photos[str(n)];vs=p['variants'];v=vs[0 if small else min(1,len(vs)-1)]
  sizes='(max-width:600px) 44vw, 300px' if small else '(max-width:720px) 92vw, 620px'
  return f'<img src="{pre}{v["file"]}" srcset="'+', '.join(f'{pre}{a["file"]} {a["width"]}w' for a in vs)+f'" sizes="{sizes}" width="{p["width"]}" height="{p["height"]}" alt="{e(alt)}" decoding="async"'+(' fetchpriority="high" loading="eager"' if eager else ' loading="lazy"')+'>'
 def figure(w,n,pre='',eager=False,cap=None):
  p=photos[str(n)];caption=cap or w['title']+' · '+p['caption']+' · Merton摄';href=p['variants'][-1]['file'] if p['rotation'] else p['original']
  width=min(800,740*p['width']/p['height'])
  return f'<figure class="iv-figure" id="photo-{n}" style="--figure-width:{width:.1f}px" data-view="{e(p["caption"])}"><a href="{pre}{href}" data-photo data-caption="{e(caption)}" aria-label="放大：{e(caption)}">{img(n,pre,eager=eager,alt=caption)}</a><figcaption>{e(caption)}</figcaption></figure>'
 def card(w,pre='',note=None):
  return f'<article class="iv-card"><a href="{pre}{w["slug"]}/">{img(w["hero"],pre,small=True,alt=w["title"]+" · 全貌")}<h3>{e(w["title"])}</h3></a><p class="iv-meta">{e(w["period"])} · {e(w["date"])}年<br>{e(w["place"])}</p>'+('<p>'+e(note)+'</p>' if note else '')+'</article>'
 def source_list():
  out='<section class="iv-prose iv-sources" id="sources"><h2>资料与来源</h2><ol>'
  for k in used:
   s=sources[k];out+=f'<li id="ref-{k}"><a href="{e(s["url"],quote=True)}">{e(s["publisher"])}：{e(s["title"])} ↗</a></li>'
  return out+'</ol><p>作品与现场展签摄影：Merton。铭文按各件所列已刊录文或提供的转录本呈现；白话解读为本站意译。公开资料中的缺字与异文保留在对应作品页。</p></section>'
 def shell(title,body,slug='',hero=1864,description='从亲见的南北朝石造像，看供养者、发愿文与石上的佛国。'):
  pre='../' if slug else '';note='../../' if slug else '../';url='https://qm2.github.io/museum-notes/images-and-vows/'+(slug+'/' if slug else '')
  og='https://qm2.github.io/museum-notes/images-and-vows/'+photos[str(hero)]['variants'][-1]['file']
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="{e(description)}"><link rel="canonical" href="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:image" content="{og}"><link rel="stylesheet" href="{note}museum.css"><link rel="stylesheet" href="{note}caravaggio/caravaggio.css"><link rel="stylesheet" href="{pre}vows.css"><script src="{note}caravaggio/caravaggio.js" defer></script><script src="{pre}vows.js" defer></script></head><body class="iv-page" id="top"><a class="iv-skip" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{note}">Merton</a><nav aria-label="主导航"><a href="{note}chinese-buddhist-art/">中国佛教艺术</a><a href="{pre or './'}">造像与发愿</a><a href="{pre or './'}#catalogue">作品目录</a></nav></header><main class="wrap" id="main">{body}</main><footer class="site-footer wrap"><a href="{note}">← 博物馆札记</a><span>现场摄影与札记 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
 for w in works:
  used.clear();ins=w['inscription_data'];pre='../'
  body='<nav class="breadcrumbs"><a href="../../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><a href="../">造像与发愿</a></nav>'
  body+=f'<header class="iv-heading"><p class="eyebrow">IMAGES AND VOWS / {e(w["date"])}</p><h1>{e(w["title"])}</h1><p class="iv-meta">{e(w["period"])} · {e(w["date"])}年｜{e(w["place"])}'+(' · '+e(w['accession']) if w['accession'] else '')+f'</p><p class="iv-deck">{e(w["lead"])}</p></header>'
  body+='<section class="iv-gallery compare-group" aria-label="正背面与细部现场照片"><div class="iv-gallery-controls" hidden><button type="button" data-prev aria-label="上一张现场照片">←</button><span class="iv-gallery-count" aria-live="polite"></span><button type="button" data-next aria-label="下一张现场照片">→</button><button type="button" data-all aria-expanded="false">展开全部照片</button></div><div class="iv-slides">'
  body+=''.join(figure(w,n,pre,eager=n==w['hero']) for n in [w['hero']]+[x for x in w['photos'] if x!=w['hero']])
  body+='</div><div class="iv-gallery-tabs" aria-label="选择视角" hidden></div></section>'
  body+='<div class="iv-prose iv-facts"><p>'+e(w['material'])+'｜'+e(w['dimensions'])+'</p><details><summary>基本资料与现场展签</summary><dl>'
  for k,v in [('年代',w['period']+'，'+w['date']+'年'),('收藏与展出',w['place']),('馆藏号',w['accession']),('图录编号',w.get('catalogue')),('形制',w['type']),('材质',w['material']),('尺寸',w['dimensions'])]:
   if v:body+='<dt>'+e(k)+'</dt><dd>'+e(v)+'</dd>'
  body+='</dl>'+cite(w['sources'][:1])+''.join(figure(w,n,pre) for n in w['labels'])+'</details></div>'
  body+='<article class="iv-prose iv-reading">'
  for s in w['sections']:body+='<section><h2>'+e(s['title'])+'</h2>'+''.join(para(p) for p in s['paragraphs'])+'</section>'
  body+='</article>'
  if ins.get('quote') or ins.get('full_text'):
   body+='<section class="iv-prose iv-inscription" id="inscription"><p class="eyebrow">WORDS ON STONE</p><h2>石上的发愿文</h2>'
   if ins.get('quote'):body+='<blockquote>'+e(ins['quote']).replace('\n','<br>')+'</blockquote><p class="iv-meta">已刊释文节录 '+cite([ins['source_id']])+'</p>'
   if ins.get('translation'):body+='<p><span class="iv-small-label">本站意译</span>'+e(ins['translation'])+'</p>'
   if ins.get('full_text'):
    body+='<details class="iv-fulltext" id="full-inscription"'+(' open' if len(ins['full_text'])<230 else '')+'><summary>读已刊原文'+('（保留缺字与异文）' if '□' in ins['full_text'] else '')+'</summary><p class="iv-meta">'+e(ins['full_note'])+' '+cite([ins['full_source_id']])+'</p><div class="iv-transcription">'+''.join('<p>'+e(x).replace('\n','<br>')+'</p>' for x in ins['full_text'].split('\n\n'))+'</div></details>'
   body+='</section>'
  body+='<section class="iv-prose"><h2>石佛远行</h2>'+para(w['provenance'])
  if w.get('existing_record'):body+='<p class="iv-crosslink"><a href="'+e(w['existing_record']['url'])+'">'+e(w['existing_record']['text'])+' →</a></p>'
  if w['id']=='penn-575-c429':body+='<p><a href="../../xiangtangshan/">可能的原址背景：响堂山石窟 →</a></p>'
  if w['notes']:body+='<details id="notes"><summary>录文、断代与研究资料注</summary>'+''.join(para(p) for p in w['notes'])+'</details>'
  body+='</section>'+source_list()
  body+='<section class="iv-related"><h2>放在一起看</h2><div class="iv-grid">'+''.join(card(by[k],pre) for k in w['related'])+'</div></section><p class="iv-prose"><a href="../#catalogue">← 回到十五件作品</a></p>'
  dest=BASE/w['slug'];dest.mkdir(exist_ok=True);(dest/'index.html').write_text(shell(w['title'],body,w['slug'],w['hero'],w['lead']))
 used.clear();hero=by['na-494-yin']
 body='<header class="iv-cover"><div><p class="eyebrow">IMAGES AND VOWS</p><h1>造像与发愿</h1><p class="iv-subtitle">南北朝的佛教信仰<br><span>约五至六世纪</span></p><p class="iv-epigraph">石会风化，人的姓名却有时<br class="iv-desktop-break">因一尊佛像而留存。</p><p class="iv-cover-note">十五件亲见石刻，从佛的面容，读到为父母、师长与众人留下的愿望。</p><a class="text-link" href="#parents">从一份发愿看起 ↓</a></div>'+figure(hero,1864,eager=True,cap='尹受国造释迦佛像 · 北魏494年 · 纳尔逊—阿特金斯艺术博物馆 · Merton摄')+'</header>'
 body+='<section class="iv-prose iv-opening">'+''.join('<p>'+e(x)+'</p>' for x in ed['opening'])+'</section>'
 body+='<nav class="iv-chapter-nav" aria-label="专题章节">'+''.join(f'<a href="#{g["id"]}"><span>{i+1:02}</span> {e(g["title"])}</a>' for i,g in enumerate(ed['chapters']))+'<a href="#catalogue">全部作品</a></nav>'
 for i,g in enumerate(ed['chapters']):
  body+=f'<section class="iv-chapter" id="{g["id"]}"><header class="iv-prose"><p class="eyebrow">{i+1:02} / {e(g["english"])}</p><h2>{e(g["title"])}</h2>'+''.join(para(x) for x in g['intro'])+'</header>'
  for f in g.get('features',[]):
   w=by[f['work']];body+='<article class="iv-feature">'+figure(w,f.get('photo',w['hero']))+'<div><p class="iv-meta">'+e(w['period'])+' · '+e(w['date'])+'年</p><h3>'+e(f['title'])+'</h3>'+''.join(para(p) for p in f['paragraphs'])+'<a class="text-link" href="'+w['slug']+'/">细读'+e(w['title'])+' →</a></div></article>'
  if g.get('cards'):body+='<div class="iv-grid">'+''.join(card(by[k],note=t) for k,t in g['cards'])+'</div>'
  if g.get('comparison'):
   body+='<div class="iv-comparison compare-group">'
   for c in g['comparison']:
    w=by[c['work']];body+='<article>'+figure(w,c['photo'])+'<h3><a href="'+w['slug']+'/">'+e(w['title'])+'</a></h3><p>'+e(c['text'])+'</p><p class="iv-meta">'+e(w['dimensions'])+'</p></article>'
   body+='</div><p class="iv-meta iv-prose">图片为并看而排，未按实物等比例缩放。</p>'
  if g.get('journeys'):
   body+='<ol class="iv-journeys">'
   for j in g['journeys']:
    w=by[j['work']];body+='<li><span>'+e(j['date'])+'</span><div><h3><a href="'+w['slug']+'/">'+e(w['title'])+'</a></h3>'+para(j['paragraph'])+'</div></li>'
   body+='</ol>'
  body+='</section>'
 body+='<section class="iv-prose iv-closing"><p>“为亡考”“师徒父母”“一切众生”，这些文字把造像与具体的人重新联系起来。照片留下眼前的形体，录文则让我们听见其中一部分愿望。还有些姓名与经历尚不清楚，留给以后的观看与阅读。</p></section>'
 body+='<section class="iv-chapter" id="catalogue"><header class="iv-prose"><p class="eyebrow">490—575 / INDEX</p><h2>沿年代重看十五件</h2><p>一件作品的正面、背面和题记归入同一条记录。目录按本辑作品年代排列；明确的纪年与约年各自保留。</p></header><form class="iv-filters" role="search" hidden><label>作品、人物或馆藏<input id="iv-search" type="search" placeholder="如：父母、成都、法兴"></label><label>地域<select id="iv-region"><option value="">全部</option><option>成都</option><option>北方</option></select></label><label>录文<select id="iv-text"><option value="">全部</option><option value="full">有已刊原文</option><option value="summary">摘要或图像研究</option></select></label><button type="reset">清除条件</button><p id="iv-count" aria-live="polite">15件</p></form><ol class="iv-catalogue">'
 for w in sorted(works,key=lambda w:w['year']):
  text='full' if w['inscription_data'].get('full_text') else 'summary';search=' '.join([w['title'],w['place'],w['accession'],w['period'],w['date'],w['lead']])
  body+=f'<li id="{w["id"]}" data-search="{e(search)}" data-region="{e(w["region"])}" data-text="{text}"><span class="iv-year">{e(w["date"])}<small>{e(w["period"])}</small></span><a href="{w["slug"]}/">{img(w["hero"],small=True,alt=w["title"]+" · 全貌")}<span><strong>{e(w["title"])}</strong><small>{e(w["place"])}'+(' · '+e(w['accession']) if w['accession'] else '')+'</small><small>'+('已刊原文与意译' if text=='full' else '图像与馆方研究')+'</small></span></a></li>'
 body+='</ol><p class="iv-empty" hidden>没有符合这些条件的作品。</p></section>'+source_list()
 body+='<nav class="iv-prose iv-crosslinks" aria-label="相关专题"><a href="../chinese-buddhist-art/">中国佛教艺术 →</a><a href="../xuzhou/">虚舟收藏 →</a><a href="../xiangtangshan/">响堂山石窟 →</a><a href="../early-buddhist-art/">早期佛教艺术 →</a></nav>'
 (BASE/'index.html').write_text(shell('造像与发愿 · 南北朝的佛教信仰',body))
 if integrate:
  parent=ROOT/'museum-notes/chinese-buddhist-art/index.html';text=parent.read_text();text=re.sub(r'<!-- vows-entry -->.*?<!-- /vows-entry -->','',text,flags=re.S)
  entry='<!-- vows-entry --><a class="issue-link" href="../images-and-vows/"><img src="../images-and-vows/images/1864-900.webp" width="1280" height="1707" alt="北魏494年尹受国造释迦佛像，正面全貌" loading="lazy" style="object-fit:contain"><div><p class="eyebrow">IMAGES AND VOWS</p><h2>造像与发愿</h2><p>南北朝的佛教信仰：从佛的面容，读到为父母、师长与众人刻下的愿望。</p><p class="issue-meta">十五件亲见石刻 · 铭文与正背细读</p><span class="text-link">进入这一辑 →</span></div></a><!-- /vows-entry -->'
  anchor='</section><section class="material-directory"';assert anchor in text;text=text.replace(anchor,entry+anchor,1);count=len(re.findall(r'<a class="issue-link"',text.split(anchor)[0]));text=re.sub(r'造像 · [一二三四五六七八九十\d]+个专题','造像 · '+str(count)+'个专题',text);parent.write_text(text)
  home=ROOT/'museum-notes/index.html';text=home.read_text();text=re.sub(r'<!-- vows-home -->.*?<!-- /vows-home -->','',text,flags=re.S);anchor='<a class="issue-link" href="chinese-painting/">';assert anchor in text
  text=text.replace(anchor,'<!-- vows-home --><p class="topic-return"><a href="images-and-vows/">造像与发愿：十五件南北朝石刻中的人、名字与祈愿 →</a></p><!-- /vows-home -->'+anchor,1);text=re.sub(r'\d+ 个造像专题 ·',str(count)+' 个造像专题 ·',text);home.write_text(text)
 print(f'Built Images and Vows: {len(works)} detail pages, {len(photos)} photos, {sum(bool(w["inscription_data"].get("full_text")) for w in works)} published transcriptions.')
if __name__=='__main__':build()
