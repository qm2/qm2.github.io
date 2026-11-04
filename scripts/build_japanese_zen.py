"""Build Japanese Zen pages from canonical works, photography and editorial data."""
from pathlib import Path
from html import escape as e
import json,re
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/japanese-zen'
def build():
 load=lambda name:json.loads((BASE/'data'/name).read_text())
 works=load('works.json'); by={w['id']:w for w in works}; photos=load('photos.json'); sources={s['id']:s for s in load('sources.json')}; opening=load('opening.json'); ed=load('editorial.json')
 captions={1737:'十牛颂图卷 · 第六段“骑牛归家” · 现场局部',1738:'十牛颂图卷 · 第八段“人牛俱忘” · 现场局部',1739:'十牛颂图卷 · 卷末布袋 · 现场局部',1741:'政黄牛与郁山主 · 双幅全貌；右为政黄牛，左为郁山主',1753:'寒山拾得图 · 双幅全貌；右为寒山，左为拾得',1759:'补陀洛山观音 · 全幅与题赞',1760:'补陀洛山观音 · 人物与山石近照',1761:'补陀洛山观音 · 题赞近照',1767:'双猿捞月 · 立轴全貌',1768:'双猿捞月 · 双猿与枝干近照'}
 def img(n,pre='',small=False,eager=False,alt=''):
  p=photos[str(n)];vs=p['variants'];v=vs[0 if small else 1];ss=', '.join(f'{pre}{a["file"]} {a["width"]}w' for a in vs)
  return f'<img src="{pre}{v["file"]}" srcset="{ss}" sizes="{("(max-width:640px) 90vw, 380px" if small else "(max-width:720px) 92vw, 680px")}" width="{p["width"]}" height="{p["height"]}" alt="{e(alt)}" loading="{("eager" if eager else "lazy")}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
 def figure(w,n,pre='',label=False,eager=False):
  p=photos[str(n)];caption=(w['title']+' · 现场展签' if label else captions.get(n,w['title']+' · 全貌'))+' · Merton摄'
  href=p['variants'][-1]['file'] if p['rotation'] else p['original']
  width=min(720,700*p['width']/p['height'])
  return f'<figure class="jz-figure" style="--figure-width:{width:.0f}px"><a data-photo href="{pre}{href}" data-caption="{e(caption)}" aria-label="放大：{e(caption)}">{img(n,pre,eager=eager,alt=caption)}</a><figcaption>{e(caption)}</figcaption></figure>'
 def shell(title,body,depth=0,entrance=False):
  pre='../' if depth else '';note='../../' if depth else '../';zen='../japanese-zen/' if entrance else pre
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="Merton的日本禅宗书画亲见札记：十九件作品、现场摄影、题跋与收藏资料。"><link rel="stylesheet" href="{note}museum.css"><link rel="stylesheet" href="{note}caravaggio/caravaggio.css"><link rel="stylesheet" href="{zen}zen.css"><script src="{note}caravaggio/caravaggio.js" defer></script><script src="{zen}zen.js" defer></script></head><body class="jz-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{note}">Merton</a><nav aria-label="主导航"><a href="{note}japanese-art/">日本艺术</a><a href="{zen or './'}">禅宗书画</a><a href="{zen or './'}#catalogue">观展目录</a></nav></header><main class="wrap" id="main">{body}</main><footer class="site-footer wrap"><a href="{note}">← 博物馆札记</a><span>现场摄影与札记 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
 def card(w,pre='',compact=False):
  return f'<article class="jz-card" id="{w["id"]}"><a href="{pre}{w["id"]}/">{img(w["photos"][0],pre,small=True,alt=w["title"]+" · "+w["author"]+" · 现场照片")}<h3>{e(w["title"])}</h3></a><p class="jz-meta">{e(w["author"])}<br>{e(w["date"])} · {e(w["museum"] or "")}</p>'+('' if compact else '<p>'+e(w['short_introduction'])+'</p>')+'</article>'
 def refs(w):
  lis=''.join(f'<li id="ref-{sid}"><a href="{e(sources[sid]["url"],quote=True)}">{e(sources[sid]["title"])} ↗</a>'+(' <small>馆方公开索引；原页访问受限。</small>' if sid in ['S11','S14'] else '')+'</li>' for sid in w['source_ids'])
  return f'<section class="jz-prose jz-sources" id="sources"><h2>资料与来源</h2><ol>{lis}<li><a href="#labels">Merton现场展签照片</a>；馆名另据个人观看记录核对。</li></ol></section>'
 for index,w in enumerate(works):
  first=w['photos'][0]
  info=' · '.join(filter(None,[w['date'],w['material'],w['museum'],w['accession']]))
  body=f'<header class="jz-heading"><p class="eyebrow"><a href="../">松声与月影</a> / {w["id"].upper()}</p><h1>{e(w["title"])}</h1><p>{e(w["author"])}</p><p class="jz-meta">{e(info)}</p><p class="jz-deck">{e(w["short_introduction"])}</p></header>'+figure(w,first,'../',eager=True)
  body+='<article class="jz-prose"><h2>画前细读</h2>'
  for i,p in enumerate(w['paragraphs']):
   keys=w['paragraph_sources'][i]
   citation=''.join(f' <a class="jz-cite" href="#ref-{sid}" aria-label="{e(sources[sid]["title"])}">[{w["source_ids"].index(sid)+1}]</a>' for sid in keys)
   body+='<p>'+e(p)+citation+'</p>'
  body+='</article>'
  if w['inscription_original']:
   body+=f'<section class="jz-prose jz-inscription"><h2>纸上的文字</h2><blockquote lang="zh-Hant">{e(w["inscription_original"]).replace(chr(10),"<br>")}</blockquote><p class="jz-meta">{e(w["inscription_note"])} <a href="#ref-{w["inscription_source_ids"][0]}">出处 ↓</a></p></section>'
  if len(w['photos'])>1:body+='<section class="jz-gallery" aria-label="其他现场照片">'+''.join(figure(w,n,'../') for n in w['photos'][1:])+'</section>'
  body+='<section class="jz-prose"><h2>收藏与流转</h2><p>'+e(w['collection_history'])+' <a class="jz-cite" href="#sources">[来源]</a></p>'
  if w['notes']:body+='<details><summary>资料注</summary><p>'+e(w['notes'])+'</p></details>'
  body+='</section><section class="jz-prose"><details id="labels"><summary>现场展签</summary>'+''.join(figure(w,n,'../',label=True) for n in w['labels'])+'</details></section>'
  body+=refs(w)
  if w['related']:body+='<section class="jz-related"><h2>放在一起看</h2><div class="jz-grid">'+''.join(card(by[x],'../',True) for x in w['related'])+'</div></section>'
  if w['id'] in ['j16','j17','j18']:body+='<p class="jz-prose"><a href="../../water-moon-guanyin/">从绘画回看观音木雕 →</a></p>'
  path=BASE/w['id'];path.mkdir(exist_ok=True);(path/'index.html').write_text(shell(w['title'],body,1))
 poem=opening['poem'];poemurl=sources['S41']['url']
 body='<header class="jz-heading"><p class="eyebrow">JAPANESE ZEN PAINTING &amp; CALLIGRAPHY</p><h1>日本禅宗书画</h1><p class="jz-subtitle">松声与月影</p></header>'
 body+='<section class="jz-prose jz-opening"><blockquote>'+ '<br>'.join(e(x) for x in poem['display_lines'])+f'<cite><a href="{e(poemurl)}">{e(poem["attribution"])}</a></cite></blockquote>'+''.join('<p>'+e(x)+'</p>' for x in opening['personal_preface'])+'</section>'
 body+='<nav class="jz-chapters" aria-label="阅读章节">'+''.join(f'<a href="#{g["id"]}">{e(g["title"])}</a>' for g in ed['groups'])+'</nav><p class="jz-prose jz-meta">十九件／组亲见作品，从中世墨迹到近代观音画。禅僧、其他宗派的僧人和文人画家，在这里保持各自的身份。</p>'
 for i,g in enumerate(ed['groups']):
  body+=f'<section class="jz-section" id="{g["id"]}"><header><p class="eyebrow">{i+1:02}</p><h2>{e(g["title"])}</h2><p>{e(g["intro"])}</p></header><div class="jz-grid">'+''.join(card(by[x]) for x in g['works'])+'</div></section>'
 body+='<section class="jz-prose jz-section"><h2>从中世到近代</h2><ol class="jz-timeline">'+''.join(f'<li><span>{e(t)}</span><a href="{k}/">{e(v)}</a></li>' for t,v,k in ed['timeline'])+'</ol><p>禅画不是把所有简笔、空白与佛教题材装进同一个盒子。慈云、寂严属于真言宗，豪潮属于天台宗；蕪村与铁斋则各有诗人、文人的背景。这些区别让并看更有意思，也使“禅宗书画”成为一条阅读路径，而非每件作品唯一的身份。</p></section>'
 body+='<section class="jz-prose jz-section"><h2>在收藏中重新相遇</h2><p>'+e(ed['collection_intro'])+'</p><p>每件作品下的“收藏与流转”保留已知节点，现场展签则记录观看时的著录。旧展签与今天馆方记录有所不同的地方，放在该件资料注中对读。</p></section>'
 body+='<section class="jz-section" id="catalogue"><details><summary>十九件观展目录</summary><label class="jz-search">按作品、作者或博物馆查找 <input type="search" id="zen-search" placeholder="如：观音、即非、波特兰"></label><p id="zen-count" aria-live="polite">19 件／组</p><ul class="jz-directory">'
 for w in works:body+=f'<li data-search="{e(" ".join(str(w[k] or "") for k in ["title","author","museum","date","accession"]))}"><a href="{w["id"]}/">{e(w["title"])}</a><span>{e(w["author"])} · {e(w["date"])}<br>{e(w["museum"] or "")} · {e(w["accession"])}</span></li>'
 body+='</ul></details></section><aside class="jz-prose jz-sources"><h2>继续阅读</h2><p><a href="../chinese-painting/">中国书画</a> · <a href="../water-moon-guanyin/">水月观音</a></p><p>作品照片与现场展签均为Merton摄。题跋释文依据各件所列馆方记录；尚无可靠释文的题字保留在照片中。原作、局部和双幅的关系见图注。</p><p>开篇寒山诗据<a href="'+e(poemurl)+'">识典古籍《寒山诗集》</a>核对。</p></aside>'
 (BASE/'index.html').write_text(shell('日本禅宗书画 · 松声与月影',body))
 entrance=ROOT/'museum-notes/japanese-art';entrance.mkdir(exist_ok=True)
 body='<header class="jz-heading"><p class="eyebrow">JAPANESE ART</p><h1>日本艺术</h1><p class="jz-deck">从松声与月影开始，留下纸墨之间的相遇。</p></header><a class="issue-link" href="../japanese-zen/">'+img(1767,'../japanese-zen/',alt='伊藤若冲《双猿捞月》全貌',eager=True)+'<div><h2>日本禅宗书画</h2><p>松声与月影</p><p>从梦窗疏石的墨迹，到若冲的双猿与近代观音画。十九件／组作品，沿着字、画与留白慢慢看。</p><span class="text-link">进入这一辑 →</span></div></a>'
 (entrance/'index.html').write_text(shell('日本艺术',body,entrance=True))
 home=ROOT/'museum-notes/index.html';html=home.read_text();html=re.sub(r'<!-- japanese-home -->.*?<!-- /japanese-home -->','',html,flags=re.S)
 entry='<!-- japanese-home --><a class="issue-link" href="japanese-art/"><img src="japanese-zen/images/1767-900.webp" alt="伊藤若冲《双猿捞月》，现场全貌" width="'+str(photos['1767']['width'])+'" height="'+str(photos['1767']['height'])+'" loading="lazy" style="object-fit:contain"><div><p class="eyebrow">JAPANESE ART</p><h2>日本艺术</h2><p>松声与月影：从中世墨迹到近代观音画，看字、画与留白如何相遇。</p><p class="issue-meta">首辑：日本禅宗书画 · 十九件／组</p><span class="text-link">进入这一辑 →</span></div></a><!-- /japanese-home -->'
 html=html.replace('<a class="issue-link" href="european-painting/">',entry+'<a class="issue-link" href="european-painting/">',1);home.write_text(html)
 print('Built Japanese art entrance, Zen topic and 19 detail pages.')
if __name__=='__main__':build()
