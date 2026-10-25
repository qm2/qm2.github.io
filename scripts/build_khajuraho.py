"""Build the Khajuraho notebook and South Asian Art entrance from reviewed data."""
from pathlib import Path
from html import escape as e
import json,re
from build_paintings import picture,frame
ROOT=Path(__file__).resolve().parents[1]

def build():
 base=ROOT/'museum-notes/khajuraho';d=json.loads((base/'data/works.json').read_text())
 numbers={k:i+1 for i,k in enumerate(d['sources'])};refs={k:[] for k in numbers}
 def cite(keys):
  links=[]
  for k in dict.fromkeys(keys):
   anchor=f'cite-{k}-{len(refs[k])+1}';refs[k].append(anchor)
   links.append(f'<a id="{anchor}" href="#source-{k}" aria-label="资料{numbers[k]}：{e(d["sources"][k][0])}">[{numbers[k]}]</a>')
  return '<sup class="kh-cites">'+''.join(links)+'</sup>' if links else ''
 def paragraphs(items):return ''.join('<p>'+e(p['text'])+cite(p['sources'])+'</p>' for p in items)
 def photo(p,caption,eager=False):
  return f'<a class="photo-open" href="images/{p["photo"]}" data-caption="{e(caption)}" aria-label="放大：{e(caption)}">{picture(p,"images/",caption,eager)}</a>'
 body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../south-asian-art/">南亚艺术</a><span>/</span><span>克久拉霍</span></nav><header class="kh-intro wrap"><p class="eyebrow">KHAJURAHO / TEMPLE AND SCULPTURE</p><h1>{e(d['title'])}</h1><p class="subtitle">{e(d['subtitle'])}</p><div class="kh-measure">{paragraphs(d['opening'])}</div><nav class="kh-nav" aria-label="专题阅读"><a href="#collection">八件作品 ↓</a><a href="#women">天女与建筑</a><a href="#couples">情侣与神祇</a><a href="#jain">耆那教</a><a href="#history">延伸阅读：神庙的世界</a></nav></header>'''
 body+='<section class="wrap kh-section" id="collection"><p class="eyebrow">EIGHT WORKS / FIVE MUSEUMS</p><h2>从八件作品看起</h2><div class="kh-overview">'
 for i,w in enumerate(d['works']):
  body+=f'<a href="#{w["id"]}"><span class="eyebrow">{i+1:02d}</span><h3>{e(w["title"])}</h3><p>{e(w["museum"])}<br>{e(w["date"])}</p><p class="kh-small">{e(w["geography"])}</p></a>'
 body+='</div></section>'
 for sec in d['sections']:
  body+=f'<section class="wrap kh-section" id="{sec["id"]}"><h2>{e(sec["title"])}</h2><p class="kh-measure">{e(sec["intro"])}</p>'
  for w in [w for w in d['works'] if w['section']==sec['id']]:
   facts=[('收藏',w['museum']),('编号',w['accession']),('年代',w['date']),('材料',w['medium']),('尺寸',w['dimensions'])]
   cap=w['title']+' · '+w['museum']+' · '+w['accession']
   body+=f'''<article class="kh-work" id="{w['id']}"><div class="kh-images"><figure>{photo(d['photos'][str(w['photo'])],cap,w['id']=='monkey')}<figcaption>{e(w['title'])} · Merton参观照片</figcaption></figure><details><summary>现场展签</summary><figure>{photo(d['photos'][str(w['label'])],cap+' · 现场展签')}<figcaption>{e(w['title'])} · 现场展签</figcaption></figure></details></div><div class="kh-notes"><h3>{e(w['title'])}</h3><p class="kh-original" lang="en">{e(w['original_title'])}</p><dl>{''.join('<div><dt>'+e(k)+'</dt><dd>'+e(v)+'</dd></div>' for k,v in facts)}</dl><p class="kh-attribution">{e(w['geography'])}</p>{paragraphs(w['notes'])}'''
   body+=f'<a class="text-link" href="{e(d["sources"][w["source"]][1])}">馆藏记录 ↗</a></div></article>'
  body+='</section>'
 body+='<section class="wrap kh-section" id="history"><p class="eyebrow">FURTHER READING</p><h2>回到神庙的世界</h2>'
 site=d['site_photo'];caption='原址参考 · 坎达里亚·马哈代瓦寺（Kandariya Mahadeva），Paul Mannix摄，2000年'
 body+=f'''<figure class="kh-site">{photo(site,caption)}<figcaption>{e(caption)}。层叠的小塔、外墙雕像带与高台基，构成从地面向主塔上升的轮廓。<br><a href="{e(d['sources']['site-photo'][1])}">图片来源</a> · <a href="{site['license_url']}">{site['license']}</a> · 原图未改动</figcaption></figure><div class="kh-history">'''
 for h in d['history']:body+='<section><h3>'+e(h['title'])+'</h3>'+paragraphs(h['paragraphs'])+'</section>'
 body+='</div><h3>四座寺庙，四个参照</h3><div class="kh-scroll" role="region" tabindex="0" aria-label="代表性寺庙对照表，可横向滚动"><table><thead><tr><th scope="col">寺庙</th><th scope="col">年代与供奉</th><th scope="col">建筑与雕塑</th></tr></thead><tbody>'
 for t in d['temples']:body+=f'<tr><th scope="row">{e(t["name"])}<span lang="en">{e(t["english"])}</span></th><td>{e(t["date"])}<br>{e(t["deity"])}</td><td>{e(t["feature"])}{cite(t["sources"])}</td></tr>'
 body+='</tbody></table></div><details class="kh-history-notes"><summary>年代、数量与名称的资料注</summary>'+paragraphs(d['history_notes'])+'</details></section>'
 body+='<section class="wrap kh-section"><details class="kh-history-notes"><summary>作品归属与馆藏资料注</summary><p>“克久拉霍地区”比具体遗址更宽；“可能来自”保留了馆方判断的余地。目前这八件作品尚无可确定原属寺庙的公开记录。</p>'
 for w in d['works']:
  if w['record_note']:body+='<p><a href="#'+w['id']+'">'+e(w['title'])+'</a>：'+e(w['record_note'])+cite([w['source']])+('</p>')
 body+='</details></section><section class="wrap kh-section kh-sources" id="sources"><h2>参考资料</h2><ol>'
 for k,(name,url) in d['sources'].items():
  back=' '.join(f'<a href="#{ref}" aria-label="返回资料{numbers[k]}第{i+1}处引用">↩{i+1}</a>' for i,ref in enumerate(refs[k]))
  body+=f'<li id="source-{k}"><a href="{e(url)}">{e(name)} ↗</a> <span class="kh-backrefs">{back}</span></li>'
 body+='</ol></section>'
 page=frame(d['title'],body,description=d['intro'],sibling=True).replace('<a href="../chinese-painting/">中国书画</a>','<a href="../south-asian-art/">南亚艺术</a>').replace('</head>','<link rel="stylesheet" href="khajuraho.css"></head>').replace('摄影 / Merton','参观摄影 / Merton；原址图片另署名')
 (base/'index.html').write_text(page)
 parent=ROOT/'museum-notes/south-asian-art';parent.mkdir(exist_ok=True)
 entry='''<a class="issue-link" href="../khajuraho/"><img src="../khajuraho/images/monkey.jpg" width="1280" height="1707" alt="克久拉霍地区，被猴子扯衣的天女" loading="lazy" style="object-fit:contain"><div><p class="eyebrow">KHAJURAHO</p><h2>克久拉霍：众神、天女与情侣</h2><p>从神庙外墙到供奉神龛，近看身体、首饰与雕像原来的位置。</p><p class="issue-meta">八件作品 · 五家博物馆<br>天女 / 情侣 / 印度教与耆那教</p><span class="text-link">走进这一辑 →</span></div></a>'''
 parent_body='<section class="wrap notebook-index"><p class="eyebrow">SOUTH ASIAN ART</p><h1>南亚艺术</h1><p class="index-intro">从一片神庙，走近不同的形象与信仰。</p>'+entry+'</section>'
 (parent/'index.html').write_text(frame('南亚艺术',parent_body,description='从克久拉霍的众神、天女与情侣开始，整理美国博物馆中的南亚艺术。',sibling=True).replace('<a href="../chinese-painting/">中国书画</a>','<a href="../khajuraho/">克久拉霍</a>'))
 home=ROOT/'museum-notes/index.html';s=re.sub(r'<!-- khajuraho-home -->.*?<!-- /khajuraho-home -->','',home.read_text(),flags=re.S)
 home_entry=entry.replace('href="../khajuraho/"','href="south-asian-art/"').replace('src="../khajuraho/','src="khajuraho/').replace('<h2>克久拉霍：众神、天女与情侣</h2>','<h2>南亚艺术</h2>').replace('走进这一辑','进入这个板块')
 anchor='<a class="issue-link" href="european-painting/">';assert anchor in s
 home.write_text(s.replace(anchor,'<!-- khajuraho-home -->'+home_entry+'<!-- /khajuraho-home -->'+anchor,1))
 print('Built Khajuraho: 8 works, 16 original photographs, 1 licensed site photograph, 2 entrances.')
if __name__=='__main__':build()
