"""Build the three photographed al-Jazari leaves and the Islamic art entrance."""
from pathlib import Path
from html import escape as e
import json,re
ROOT=Path(__file__).resolve().parents[1]
LIGHTBOX='''<dialog id="art-lightbox" aria-labelledby="lightbox-caption"><div class="lightbox-tools"><button type="button" id="photo-prev" aria-label="上一张照片">←</button><button type="button" id="photo-next" aria-label="下一张照片">→</button><button type="button" id="zoom-toggle" aria-pressed="false">放大细看 ＋</button><a id="original-photo" href="#" target="_blank" rel="noopener">原图 ↗</a><button type="button" id="photo-close" aria-label="关闭大图">关闭 ×</button></div><div id="photo-stage" tabindex="0" aria-label="照片区域；放大后可滚动查看"><img id="large-photo" alt=""></div><p id="lightbox-caption"></p></dialog>'''
def build():
 base=ROOT/'museum-notes/al-jazari';d=json.loads((base/'data/works.json').read_text());works=d['works']
 assert len(works)==len({w['id'] for w in works})==3
 for w in works: assert (base/'images'/w['photo']).is_file()
 def shell(title,body,depth=0):
  note='../'*(depth+1);topic='../'*depth or './'
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · 博物馆札记 | Merton</title><meta name="description" content="{e(d['intro'])}"><link rel="stylesheet" href="{note}museum.css"><link rel="stylesheet" href="{note}caravaggio/caravaggio.css"><script src="{note}caravaggio/caravaggio.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{note}">Merton</a><nav aria-label="主导航"><a href="{note}islamic-art/">伊斯兰艺术</a><a href="{note}al-jazari/#collection">三张书页</a><a href="{note}al-jazari/compare/">并排细读</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="{note}">← 博物馆札记</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''
 def image(w,prefix='',high=False):
  return f'<img src="{prefix}images/{w["photo"]}" alt="{e(w["title"])} · {e(w["visit"])} · Merton参观照片" width="{w["width"]}" height="{w["height"]}" {"fetchpriority=high" if high else "loading=lazy"} decoding="async">'
 def photo(w,prefix='',text=None):
  return f'<a data-photo href="{prefix}images/{w["photo"]}" data-caption="{e(w["title"])} · {e(w["accession"])} · Merton参观照片">{text or image(w,prefix)}</a>'
 def citations(keys):
  return '<div class="work-sources">'+''.join(f'<p><a href="{e(d["sources"][key][1])}" target="_blank" rel="noopener noreferrer">{e(d["sources"][key][0])} ↗</a></p>' for key in keys)+'</div>' if keys else ''
 def crumbs(tail='',depth=0):
  note='../'*(depth+1);topic='../'*depth or './'
  return f'<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="{note}">博物馆札记</a><span>/</span><a href="{note}islamic-art/">伊斯兰艺术</a><span>/</span>'+(f'<a href="{topic}">{e(d["title"])}</a><span>/</span><span>{e(tail)}</span>' if tail else f'<span>{e(d["title"])}</span>')+'</nav>'
 def card(w):
  return f'''<article class="art-card" id="{w['id']}"><a class="art-thumbnail" href="{w['id']}/">{image(w)}</a><div class="art-card-copy"><p class="card-kicker">{e(w['date'])}</p><h3><a href="{w['id']}/">{e(w['title'])}</a></h3><p class="card-museum">{e(w['visit'])}</p><p class="card-look">{e(w['observation'])}</p><div class="card-actions"><a href="{w['id']}/">读这张书页 →</a>{photo(w,text='放大照片 ↗')}</div></div></article>'''
 hero=works[0]
 body=crumbs()+f'''<section class="car-hero wrap"><div class="car-hero-copy"><p class="eyebrow">ISLAMIC ART / 001</p><h1>贾扎里的<wbr><span style="white-space:nowrap">奇妙机械</span></h1><p class="car-lede">{e(d['subtitle'])}</p><p class="artist-dates">{e(d['original_title'])}</p><p class="car-intro">{e(d['intro'])}</p><div class="hero-links"><a href="#collection">从书页看起 ↓</a><a href="compare/">并排细读 →</a></div><p class="car-stats"><b>3</b> 张书页 · 弗利尔与休斯顿<br>1315年与1354年的抄本</p></div><figure class="car-hero-image"><a href="{hero['id']}/">{image(hero,high=True)}</a><figcaption>{e(hero['title'])}<br><span>{e(hero['accession'])} · 1315年</span></figcaption></figure></section><aside class="editorial-note wrap"><h2>从一本机械书开始</h2><p>{e(d['background'])}</p>{citations(d['background_sources'])}</aside><section class="car-collection wrap" id="collection"><div class="car-heading"><div><p class="eyebrow">THREE MANUSCRIPT LEAVES</p><h2>三张书页</h2></div><a href="compare/">把三页放在一起 →</a></div><div class="art-grid">{''.join(card(w) for w in works)}</div></section>'''
 (base/'index.html').write_text(shell(d['title'],body))
 for w in works:
  fields=[('原著作者','贾扎里（al-Jazari）'),('抄本年代',w['date']),('制作地区',w['region']),('材料',w['material']),('尺寸',w['dimensions']),('收藏',w['collection']),('观看地点',w['visit']),('编号',w['accession']),('抄写者',w['copyist']),('绘画者',w['painter'])]
  facts='<dl class="work-facts">'+''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in fields if v)+'</dl>'
  paragraphs=''.join(f'<section><h2>{e(p["title"])}</h2><p>{e(p["text"])}</p>'+('<p class="source">据现场展签。</p>' if p['evidence']=='label' else '')+citations(p['sources'])+'</section>' for p in w['paragraphs'])
  body=crumbs(w['title'],1)+f'''<header class="work-heading wrap"><p class="eyebrow">AL-JAZARI / AUTOMATA</p><h1>{e(w['title'])}</h1><p class="work-original">{e(w['original_title'])}</p></header><div class="work-layout wrap"><figure class="work-photo">{photo(w,'../')}<figcaption>{e(w['visit'])} · Merton参观照片 · 点击放大</figcaption></figure><div class="work-record">{facts}<p>{e(w['observation'])}</p>{paragraphs}<p class="record-note">{e(w['note'])}</p>{citations(w['sources'])}</div></div><nav class="work-sequence wrap" aria-label="继续阅读"><a href="../#collection">← 三张书页</a><a href="../compare/">并排细读 →</a></nav>'''
  target=base/w['id'];target.mkdir(exist_ok=True);(target/'index.html').write_text(shell(w['title'],body,1))
 cells=''.join(f'<figure class="comparison-work">{photo(w,"../")}<figcaption><a href="../{w["id"]}/">{e(w["title"])} →</a><span>{e(w["date"])}</span><span>{e(w["visit"])}</span><span>{e(w["accession"])}</span></figcaption></figure>' for w in works)
 body=crumbs('并排细读',1)+f'''<header class="compare-header wrap"><p class="eyebrow">AL-JAZARI / SIDE BY SIDE</p><h1>水、人物与文字</h1><p>从人物的手开始，再沿着线条看向装置内部。</p><p class="source">图片未按实物尺寸比例排列。</p></header><div class="wrap"><section class="compare-group" id="three-leaves"><h2>三张书页，两种用途</h2><div class="comparison-grid" style="--columns:3">{cells}</div></section></div><aside class="editorial-note wrap"><h2>机械知识怎样进入画面</h2>{''.join('<p>'+e(p)+'</p>' for p in d['comparison'])}{citations(['freer-wash','freer-clock','sabah'])}</aside>'''
 (base/'compare').mkdir(exist_ok=True);(base/'compare/index.html').write_text(shell('并排细读 · 贾扎里的奇妙机械',body,1))
 parent=ROOT/'museum-notes/islamic-art';parent.mkdir(exist_ok=True)
 body=f'''<div class="wrap notebook-index"><p class="eyebrow">MUSEUM NOTES / ISLAMIC ART</p><h1>伊斯兰艺术</h1><p class="index-intro">从几张机械书页开始，<br>看图像、书写与器物之间的联系。</p><section><h2>第一辑</h2><a class="issue-link" href="../al-jazari/">{image(hero,'../al-jazari/')}<div><p class="eyebrow">001 / AL-JAZARI</p><h2>{e(d['title'])}</h2><p>{e(d['subtitle'])}中的洗手装置与水钟。</p><p class="issue-meta">3 张书页 · 3 张参观照片<br>弗利尔 / 休斯顿</p><span class="text-link">走进这一辑 →</span></div></a></section></div>'''
 (parent/'index.html').write_text(shell('伊斯兰艺术',body))
 home=ROOT/'museum-notes/index.html'
 s=re.sub(r'<!-- islamic-entry -->.*?<!-- /islamic-entry -->','',home.read_text(),flags=re.S)
 entry=f'''<!-- islamic-entry --><a class="issue-link" href="islamic-art/">{image(hero,'al-jazari/')}<div><p class="eyebrow">ISLAMIC ART</p><h2>伊斯兰艺术</h2><p>从贾扎里的机械书开始，看水怎样驱动人物，图像怎样解释装置。</p><p class="issue-meta">首辑：贾扎里的奇妙机械<br>3 张书页 / 作品细读 / 并排比较</p><span class="text-link">进入这个板块 →</span></div></a><!-- /islamic-entry -->'''
 anchor='</section>\n<section class="future-collections"';assert anchor in s;s=s.replace(anchor,entry+anchor,1);home.write_text(s)
 print('Built al-Jazari: 3 leaves, 3 unchanged photos, 6 pages including Islamic art entrance.')
if __name__=='__main__':build()
