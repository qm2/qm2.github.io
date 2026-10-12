"""Build the Nimrud reading page and Ancient West Asia entrance from reviewed data."""
from pathlib import Path
from html import escape as e
import json,re
from build_paintings import picture,frame
ROOT=Path(__file__).resolve().parents[1]
def build():
 base=ROOT/'museum-notes/nimrud-guardians';d=json.loads((base/'data/works.json').read_text());works=d['works']
 def citations(keys):
  return '<p class="source">'+ ' · '.join(f'<a href="{e(d["sources"][k][1])}">{e(d["sources"][k][0])} ↗</a>' for k in keys)+'</p>' if keys else ''
 def paragraphs(items):return ''.join('<p>'+e(p['text'])+'</p>'+citations(p['sources']) for p in items)
 def photo(w,label=False,eager=False):
  n=w['label' if label else 'photo'];p=d['photos'][str(n)];caption=f'{w["title"]} · {w["museum"]} · {w["accession"]}'+(' · 现场展签' if label else ' · Merton参观照片')
  return f'<a class="photo-open" href="images/{p["photo"]}" data-caption="{e(caption)}" aria-label="放大：{e(caption)}">{picture(p,"images/",caption,eager)}</a>'
 def shell(title,body):
  return frame(title,body,description=d['intro'],sibling=True).replace('<a href="../chinese-painting/">中国书画</a>','<a href="../ancient-west-asia/">古代西亚</a>').replace('</head>','<link rel="stylesheet" href="../nimrud-guardians/nimrud.css"></head>')
 hero=works[1]
 body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../ancient-west-asia/">古代西亚</a><span>/</span><span>尼姆鲁德</span></nav><section class="nimrud-hero wrap"><div><p class="eyebrow">NIMRUD / NORTHWEST PALACE</p><h1>尼姆鲁德的<br>有翼守护者</h1><p class="subtitle">{e(d['subtitle'])}</p><p>{e(d['intro'])}</p><nav class="nimrud-links" aria-label="专题阅读"><a href="#collection">从浮雕看起 ↓</a><a href="#background">王都与宫殿</a><a href="#compare">三件并看</a></nav></div><figure>{photo(hero,eager=True)}<figcaption>{e(hero['title'])} · 克利夫兰 · 1943.246</figcaption></figure></section><section class="wrap" id="collection"><h2>石板上的守护者</h2>'''
 for w in works:
  facts=[('收藏',w['museum']),('馆藏号',w['accession']),('年代',w['date']),('材料',w['material']),('尺寸',w['dimensions'])]
  body+=f'''<article class="nimrud-work" id="{w['id']}"><div class="nimrud-images"><figure>{photo(w)}<figcaption>{e(w['title'])} · Merton参观照片 · 点击放大</figcaption></figure><details><summary>现场展签 <span>＋</span></summary><figure>{photo(w,label=True)}<figcaption>{e(w['museum'])} · {e(w['accession'])} · 现场展签</figcaption></figure></details></div><div class="nimrud-notes"><h3>{e(w['title'])}</h3><p class="nimrud-original" lang="en">{e(w['original_title'])}</p><dl>{''.join('<div><dt>'+e(k)+'</dt><dd>'+e(v)+'</dd></div>' for k,v in facts)}</dl>{paragraphs(w['notes'])}</div></article>'''
 body+=f'''</section><section class="wrap nimrud-background" id="background"><p class="eyebrow">KALHU / PALACE AND PROTECTION</p><h2>从王都的宫殿到博物馆</h2>{paragraphs(d['background'])}<h3>圣树与锥形器物</h3>{paragraphs([d['iconography']])}</section><section class="wrap nimrud-compare" id="compare"><p class="eyebrow">SIDE BY SIDE</p><h2>三件并看</h2><p>休斯顿这件高约1.07米，另外两件高约2.3米。照片并排展示，不代表实物等比例。</p><div class="nimrud-comparison-images">'''
 for w in works:body+=f'<figure>{photo(w)}<figcaption><a href="#{w["id"]}">{e(w["title"])}</a><br>{e(w["dimensions"])}</figcaption></figure>'
 body+='</div><div class="nimrud-questions">'+''.join('<div><h3>'+e(t)+'</h3><p>'+e(p)+'</p></div>' for t,p in d['comparisons'])+'</div></section>'
 body+='<section class="wrap nimrud-sources" id="sources"><h2>资料与来源</h2><p>'+e(d['record_note'])+'</p>'+paragraphs([d['location_note']])+'<ul>'+''.join(f'<li><a href="{e(url)}">{e(name)} ↗</a></li>' for name,url in d['sources'].values())+'</ul></section>'
 (base/'index.html').write_text(shell(d['title'],body))
 def entry(prefix,category=False):
  return f'''<a class="issue-link" href="{'ancient-west-asia/' if category else '../nimrud-guardians/'}"><img src="{prefix}images/770.jpg" alt="举手致意的护佑精灵，克利夫兰艺术博物馆1943.246" width="1280" height="1707" loading="lazy"><div><p class="eyebrow">ANCIENT WEST ASIA / MESOPOTAMIA</p><h2>{'古代西亚' if category else e(d['title'])}</h2><p>从尼姆鲁德西北宫的浮雕，看鹰首与人首、手势与树纹，以及刻在人物身上的文字。</p><p class="issue-meta">{'首辑：尼姆鲁德的有翼守护者<br>' if category else ''}休斯顿 / 克利夫兰 / 纳尔逊</p><span class="text-link">走进这一辑 →</span></div></a>'''
 parent=ROOT/'museum-notes/ancient-west-asia';parent.mkdir(exist_ok=True)
 (parent/'index.html').write_text(shell('古代西亚／两河文明','<div class="wrap notebook-index"><p class="eyebrow">ANCIENT WEST ASIA</p><h1>古代西亚</h1><p class="index-intro">两河文明<br>从宫殿中的有翼守护者开始。</p>'+entry('../nimrud-guardians/')+'</div>'))
 home=ROOT/'museum-notes/index.html';s=re.sub(r'<!-- nimrud-entry -->.*?<!-- /nimrud-entry -->','',home.read_text(),flags=re.S);anchor='</section>\n<section class="future-collections"';assert anchor in s
 home.write_text(s.replace(anchor,'<!-- nimrud-entry -->'+entry('nimrud-guardians/',True)+'<!-- /nimrud-entry -->'+anchor,1))
 print('Built Nimrud: 3 works, 6 unchanged photos, topic and Ancient West Asia entrance.')
if __name__=='__main__':build()
