"""Build the Nimrud reading page and Ancient West Asia entrance from reviewed data."""
from pathlib import Path
from html import escape as e
import json,re
from museum_assets import asset_url
from build_paintings import picture,frame
ROOT=Path(__file__).resolve().parents[1]
def build():
 base=ROOT/'museum-notes/nimrud-guardians';d=json.loads((base/'data/works.json').read_text());works=d['works']
 def citations(keys):
  return '<p class="source">'+ ' · '.join(f'<a href="{e(d["sources"][k][1])}">{e(d["sources"][k][0])} ↗</a>' for k in keys)+'</p>' if keys else ''
 def paragraphs(items,group_sources=False):
  if group_sources:
   keys=list(dict.fromkeys(k for p in items for k in p['sources']))
   return ''.join('<p>'+e(p['text'])+'</p>' for p in items)+citations(keys)
  return ''.join('<p>'+e(p['text'])+'</p>'+citations(p['sources']) for p in items)
 def photo(w,label=False,eager=False):
  n=w['label' if label else 'photo'];p=d['photos'][str(n)];caption=f'{w["title"]} · {w["museum"]} · {w["accession"]}'+(' · 现场展签' if label else ' · Merton参观照片')
  return f'<a class="photo-open" href="{p.get("original_url") or asset_url("images/",p["photo"])}" data-full-src="{p.get("original_url") or asset_url("images/",p["photo"])}" data-caption="{e(caption)}" aria-label="放大：{e(caption)}">{picture(p,"images/",caption,eager)}</a>'
 def figure(w,label=False,eager=False,caption=None):
  p=d['photos'][str(w['label' if label else 'photo'])]
  width,height=(p['height'],p['width']) if p['rotation'] else (p['width'],p['height'])
  if caption is None:caption=e(w['title'])+(' · 现场展签' if label else ' · Merton摄 · 点击放大')
  return f'<figure class="nimrud-figure" style="--photo-ratio:{width/height:.8f}">{photo(w,label,eager)}<figcaption>{caption}</figcaption></figure>'
 def shell(title,body):
  return frame(title,body,description=d['intro'],sibling=True).replace('<a href="../chinese-painting/">中国书画</a>','<a href="../ancient-west-asia/">古代西亚</a>').replace('</head>','<link rel="stylesheet" href="../nimrud-guardians/nimrud.css"></head>')
 hero=works[1]
 body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../ancient-west-asia/">古代西亚</a><span>/</span><span>尼姆鲁德</span></nav><section class="nimrud-hero wrap"><div><p class="eyebrow">NIMRUD / NORTHWEST PALACE</p><h1>尼姆鲁德的<br>有翼守护者</h1><p class="subtitle">{e(d['subtitle'])}</p><p>{e(d['intro'])}</p><nav class="nimrud-links" aria-label="专题阅读"><a href="#collection">从浮雕看起 ↓</a><a href="#background">王都与宫殿</a><a href="#rooms">回到宫殿房间</a><a href="#compare">并看这些浮雕</a></nav></div>{figure(hero,eager=True,caption=e(hero["title"])+" · 克利夫兰 · 1943.246")}</section><section class="wrap" id="collection"><h2>石板上的守护者</h2>'''
 body+='<p class="nimrud-collection-note">'+e(d['collection_note'])+'</p><nav class="nimrud-work-index" aria-label="按观看地点阅读">'+''.join(f'<a href="#{w["id"]}">{e(w["viewing_city"])}</a>' for w in works)+'</nav>'
 for w in works:
  facts=[('收藏／展出',w['museum']),('编号',w['accession']),('年代',w['date']),('材料',w['material']),('尺寸',w['dimensions'])]
  research='<details class="nimrud-research"><summary>原位与资料注 <span>＋</span></summary>'+paragraphs(w['research_notes'])+'</details>' if w.get('research_notes') else ''
  body+=f'''<article class="nimrud-work" id="{w['id']}"><div class="nimrud-images">{figure(w)}<details><summary>现场展签 <span>＋</span></summary>{figure(w,label=True)}{''.join(figure(dict(w,label=n),label=True,caption='宫殿复原与壁板位置说明 · 现场展板') for n in w.get('extra_labels',[]))}</details></div><div class="nimrud-notes"><h3>{e(w['title'])}</h3><p class="nimrud-original" lang="en">{e(w['original_title'])}</p><dl>{''.join('<div><dt>'+e(k)+'</dt><dd>'+e(v)+'</dd></div>' for k,v in facts)}</dl>{paragraphs(w['notes'],group_sources=True)}{research}</div></article>'''
 body+=f'''</section><section class="wrap nimrud-background" id="background"><p class="eyebrow">KALHU / PALACE AND PROTECTION</p><h2>从王都的宫殿到博物馆</h2>{paragraphs(d['background'])}<h3>圣树与锥形器物</h3>{paragraphs([d['iconography']])}</section><section class="wrap nimrud-compare" id="compare"><p class="eyebrow">SIDE BY SIDE</p><h2>并看这些浮雕</h2><p>{e(d["comparison_intro"])}</p><div class="nimrud-comparison-images">'''
 for w in works:body+=figure(w,caption=f'<a href="#{w["id"]}">{e(w["title"])}</a><br>{e(w["dimensions"])}')
 body+='</div><div class="nimrud-questions">'+''.join('<div><h3>'+e(t)+'</h3><p>'+e(p)+'</p></div>' for t,p in d['comparisons'])+'</div></section>'
 rooms='<section class="wrap nimrud-rooms" id="rooms"><p class="eyebrow">ROOMS AND FRAGMENTS</p><h2>回到宫殿房间</h2><div class="nimrud-room-grid">'
 for r in d['rooms']:
  rooms+='<article><h3>'+e(r['title'])+'</h3>'+paragraphs([r])+'<p class="nimrud-room-links">'+' · '.join('<a href="#'+wid+'">'+e(next(w['viewing_city'] for w in works if w['id']==wid))+'</a>' for wid in r['works'])+'</p></article>'
 rooms+='</div></section>'
 body=body.replace('<section class="wrap nimrud-compare"',rooms+'<section class="wrap nimrud-compare"',1)
 body+='<section class="wrap nimrud-sources" id="sources"><h2>资料与来源</h2><p>'+e(d['record_note'])+'</p>'+paragraphs([d['location_note']])+'<ul>'+''.join(f'<li><a href="{e(url)}">{e(name)} ↗</a></li>' for name,url in d['sources'].values())+'</ul></section>'
 (base/'index.html').write_text(shell(d['title'],body))
 def entry(prefix,category=False):
  return f'''<a class="issue-link" href="{'ancient-west-asia/' if category else '../nimrud-guardians/'}"><img src="{prefix}images/770.jpg" alt="举手致意的护佑精灵，克利夫兰艺术博物馆1943.246" width="1280" height="1707" loading="lazy"><div><p class="eyebrow">ANCIENT WEST ASIA / MESOPOTAMIA</p><h2>{'古代西亚' if category else e(d['title'])}</h2><p>从尼姆鲁德西北宫的浮雕，看鹰首与人首、手势与树纹，以及刻在人物身上的文字。</p><p class="issue-meta">{'首辑：尼姆鲁德的有翼守护者<br>' if category else ''}{e(" / ".join(w["viewing_city"] for w in works))}</p><span class="text-link">走进这一辑 →</span></div></a>'''
 parent=ROOT/'museum-notes/ancient-west-asia';parent.mkdir(exist_ok=True)
 (parent/'index.html').write_text(shell('古代西亚／两河文明','<div class="wrap notebook-index"><p class="eyebrow">ANCIENT WEST ASIA</p><h1>古代西亚</h1><p class="index-intro">两河文明<br>从宫殿中的有翼守护者开始。</p>'+entry('../nimrud-guardians/')+'</div>'))
 home=ROOT/'museum-notes/index.html';s=re.sub(r'<!-- nimrud-entry -->.*?<!-- /nimrud-entry -->','',home.read_text(),flags=re.S);anchor='</section>\n<section class="future-collections"';assert anchor in s
 home.write_text(s.replace(anchor,'<!-- nimrud-entry -->'+entry('nimrud-guardians/',True)+'<!-- /nimrud-entry -->'+anchor,1))
 print(f'Built Nimrud: {len(works)} works, {len(d["photos"])} photos.')
if __name__=='__main__':build()
