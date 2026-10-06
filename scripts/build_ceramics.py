"""Build the first Chinese ceramics notebook from paired photographs and label records."""
from pathlib import Path
from html import escape as e
import json,re
ROOT=Path(__file__).resolve().parents[1]
LIGHTBOX='''<dialog id="lightbox" aria-labelledby="lightbox-caption"><button class="close-lightbox" type="button" aria-label="关闭大图">关闭 ×</button><img id="lightbox-image" alt=""><p id="lightbox-caption"></p><a id="original-link" href="#" target="_blank" rel="noopener">单独打开照片 ↗</a></dialog>'''
def build():
 base=ROOT/'museum-notes/yuan-blue-and-white';d=json.loads((base/'data/works.json').read_text());works=d['works'];by={w['id']:w for w in works}
 assert len(by)==len(works)==7
 assert sum(w['unit']=='blue' for w in works)==5
 assert all((base/'images'/w['photo']).is_file() for w in works)
 def image(w,prefix='images/',hero=False):
  return f'<img src="{prefix}{w["photo"]}" alt="{e(w["title"])} · Merton参观照片" width="{w["width"]}" height="{w["height"]}" {"fetchpriority=high" if hero else "loading=lazy"} decoding="async">'
 def shell(title,body,depth=1):
  prefix='../'*depth
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · 博物馆札记 | Merton</title><meta name="description" content="Merton看过的元青花与同时期瓷器：五件青花、两件比较作品，保留现场照片、展签核对与收藏故事。"><link rel="stylesheet" href="{prefix}museum.css"><link rel="stylesheet" href="{prefix}sculpture-topics.css"><link rel="stylesheet" href="{prefix}yuan-blue-and-white/ceramics.css"><script src="{prefix}museum.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{prefix}">Merton</a><nav aria-label="主导航"><a href="{prefix}chinese-ceramics/">中国陶瓷</a><a href="{prefix}yuan-blue-and-white/compare/">并排看器物</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="{prefix}">← 博物馆札记</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
 def card(w):
  sources=''.join(f'<p class="source"><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗</a></p>' for label,url in w['sources'])
  facts=''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k,v in [('年代',w['date']),('材料',w['material']),('编号',w['accession'])])
  label='元青花 · 据现场展签' if w['id']=='wave-vase' else ('元青花' if w['unit']=='blue' else '同时期比较 · 不计入青花')
  return f'''<article class="object-card" id="{w['id']}"><a class="photo-link" href="images/{w['photo']}" data-caption="{e(w['title'])} · {e(w['museum'])} · Merton参观照片" aria-label="放大：{e(w['title'])}">{image(w)}<span class="photo-hint">查看大图 ↗</span></a><div class="object-body"><div class="object-topline"><span>{e(w['museum'])}</span><a href="#{w['id']}" aria-label="作品固定链接">↗</a></div><p class="source">{label}</p><h3>{e(w['title'])}</h3><p class="original-title">{e(w['original_title'])}</p><dl>{facts}</dl><p class="observation">{e(w['observation'])}</p><details><summary>作品札记与资料 <span aria-hidden="true">＋</span></summary><div class="notes"><p>{e(w['story'])}</p>{sources}<p class="record-note">{e(w['note'])}</p><p class="source">基本信息另据现场展签 · 2026年10月核对 · 照片 / Merton</p></div></details></div></article>'''
 hero=by['lion-head-jar']
 body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-ceramics/">中国陶瓷</a><span>/</span><span>元青花</span></nav><section class="hero wrap"><div class="hero-copy"><p class="eyebrow">CHINESE CERAMICS / 001</p><h1>元青花</h1><p class="subtitle">几只瓶罐，一只大盘。<br>慢慢看蓝与白。</p><p class="intro">牡丹、凤凰、层层展开的水波。把在不同展厅里看到的器物放到一起，也留两件同时期的瓷器作比较。</p><p class="edition"><span><b>5</b> 件青花</span><span><b>2</b> 件比较作品</span></p><p class="source">其中水波纹瓶的年代与工艺据现场展签。</p><div class="hero-links"><a class="text-link" href="#blue">从青花看起 ↓</a>　<a class="text-link" href="compare/">并排看器物 →</a></div></div><figure class="hero-image"><img src="images/{hero['photo']}" alt="青花双狮头罐，克利夫兰艺术博物馆" width="{hero['width']}" height="{hero['height']}" fetchpriority="high"><figcaption>{hero['title']} · 元，14世纪<br><span>{hero['museum']} / {hero['accession']}</span></figcaption></figure></section>'''
 for unit,title,desc in [('blue','青花：五件器物','白地上的蓝花，也有蓝色纹样之间留下的白。'),('comparison','同时期比较：蓝釉与高足杯','同样是蓝色，装饰方式却不同。这两件单独看，不计入青花。')]:
  body+=f'<section class="collection wrap" id="{unit}"><div class="collection-heading"><div><p class="eyebrow">{"BLUE AND WHITE" if unit=="blue" else "ALONGSIDE"}</p><h2>{title}</h2></div><p>{desc}</p></div><div class="object-grid">'+''.join(card(w) for w in works if w['unit']==unit)+'</div></section>'
 body+='''<aside class="editorial-note wrap"><h2>这一辑先从这里开始</h2><p>青花以钴料在胎上绘画，再罩透明釉烧成。蓝釉留白梅瓶与浅蓝釉高足杯虽然也呈蓝色，不能因此一并算作青花。<a href="https://www.dpm.org.cn/collection/ceramic/227179.html">青花工艺说明：故宫博物院 ↗</a></p><p>这批七件作品都有自己的现场照片；展签保留作核对材料，不放进画廊。水波纹瓶据展签收录，高足杯的编号差异逐件说明。没有看到的作品，留待以后再遇见。</p></aside>'''
 (base/'index.html').write_text(shell('元青花',body))
 groups=[('jars','两只罐，怎样安排一圈纹样','从肩到腹再到足，看纹样带如何顺着器形展开。',['shanxi-peony-jar','lion-head-jar']),('meiping','两只梅瓶，两种蓝白关系','一只是白地上的青花，另一只是蓝釉地上的白龙。相近器形，工艺不同。',['richard-kan-meiping','blue-glaze-dragon']),('surfaces','画出的线，浮起的纹','凤鸟大盘与水波纹瓶用青花组织纹样；高足杯内的云龙则依靠浮雕、刻划与釉层呈现。',['phoenix-dish','wave-vase','dragon-stem-cup'])]
 compare='<header class="category-header wrap"><p class="eyebrow">YUAN CERAMICS / SIDE BY SIDE</p><h1>并排看器物</h1><p class="index-intro">先看器形，再看纹样怎样贴着它展开。</p><p class="source">图片排列不代表器物实物的大小比例。</p><a href="../">← 返回元青花</a></header>'
 for id,title,text,ids in groups:
  compare+=f'<section class="collection wrap" id="{id}"><h2>{title}</h2><p>{text}</p><div class="object-grid">'
  for wid in ids:
   w=by[wid];compare+=f'<figure class="object-card ceramic-comparison"><a class="photo-link" href="../images/{w["photo"]}" data-caption="{e(w["title"])} · {e(w["museum"])} · Merton参观照片">{image(w,"../images/")}<span class="photo-hint">查看大图 ↗</span></a><figcaption><a href="../#{w["id"]}">{e(w["title"])} →</a><p>{e(w["museum"])}</p><p>{e(w["date"])}</p><p class="source">{"青花" if w["unit"]=="blue" else "比较作品 · 非青花"}</p></figcaption></figure>'
  compare+='</div></section>'
 (base/'compare').mkdir(exist_ok=True);(base/'compare/index.html').write_text(shell('并排看器物 · 元青花',compare,2))
 parent=ROOT/'museum-notes/chinese-ceramics';parent.mkdir(exist_ok=True)
 parentbody=f'''<div class="wrap notebook-index"><p class="eyebrow">MUSEUM NOTES / CHINESE CERAMICS</p><h1>中国陶瓷</h1><p class="index-intro">从几件看过的器物开始，<br>慢慢辨认器形、釉色与纹样。</p><section><h2>第一辑</h2><a class="issue-link" href="../yuan-blue-and-white/">{image(hero,'../yuan-blue-and-white/images/')}<div><p class="eyebrow">001 / YUAN BLUE AND WHITE</p><h2>元青花</h2><p>五件青花，另有蓝釉梅瓶与高足杯作比较。</p><p class="issue-meta">7 件器物 · 7 张参观照片 · 三组比较</p><span class="text-link">走进这一辑 →</span></div></a></section></div>'''
 (parent/'index.html').write_text(shell('中国陶瓷',parentbody))
 homepage=ROOT/'museum-notes/index.html'
 if homepage.exists():
  s=re.sub(r'<!-- ceramics-entry -->.*?<!-- /ceramics-entry -->','',homepage.read_text(),flags=re.S)
  entry=f'''<!-- ceramics-entry --><a class="issue-link" href="chinese-ceramics/">{image(hero,'yuan-blue-and-white/images/')}<div><p class="eyebrow">CHINESE CERAMICS</p><h2>中国陶瓷</h2><p>从元青花看起，比较器形、釉色与纹样。</p><p class="issue-meta">首辑：5 件青花 + 2 件比较作品<br>原拍照片 / 收藏故事 / 并排看器物</p><span class="text-link">进入这个板块 →</span></div></a><!-- /ceramics-entry -->'''
  anchor='<a class="issue-link" href="chinese-painting/">';assert anchor in s;s=s.replace(anchor,entry+anchor,1);homepage.write_text(s)
 print('Built Chinese ceramics: 5 blue-and-white works + 2 comparisons, 14 source photographs paired.')
if __name__=='__main__':build()
