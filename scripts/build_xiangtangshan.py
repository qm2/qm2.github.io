"""Build Xiangtangshan from edited records and shared, derived photo assets."""
from pathlib import Path
from html import escape as e
import json,re
from build_jazari import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1]
GROUPS=[
 ('NN','北响堂北洞','从巨像到柱座','佛手、坐菩萨与六件有翼兽，分别留下主像、佛龛与建筑下部的线索。北洞中央塔柱与壁面上有多组造像，同洞关系还需进一步分辨到不同佛龛。','https://xts.uchicago.edu/content/north-site-north-cave'),
 ('NM','北响堂中洞','洞口的巨大菩萨','大都会的菩萨头像，联系到中洞入口的高大造像。冠与面部的尺度，也把观看带回洞窟外观。','https://xts.uchicago.edu/content/north-site-middle-cave'),
 ('NS','北响堂南洞','刻经洞中的面孔','这座洞窟常称刻经洞，位于北响堂。唐邕题记记载，洞内外的佛经刻写于568—572年；造像也留有分阶段雕刻的迹象。','https://xts.uchicago.edu/content/north-site-south-cave'),
 ('S2','南响堂第二窟','两座博物馆，一座洞窟','弗利尔的两块大浮雕与立菩萨，宾大的三尊立像，在原窟的范围内重新相遇。第二窟的立像与浮雕曾被移走，中央塔柱后来也遭到破坏，旧照片与残件成为研究原貌的重要线索。','https://xts.uchicago.edu/content/south-site-cave-2'),
 ('S36','南响堂其他洞窟','归属到一段范围','三件被联系到第三至第六窟范围；大势至头像按馆方现行资料归于第四至第六窟。佛、弟子与菩萨的身份，可以从发式、衣饰和所持之物分别观察。',''),
 ('unassigned','原窟未定','先留下能够确定的联系','大都会侍立菩萨头像的来源落实到南响堂；纳尔逊天王胸像的南北区与具体洞窟仍未定。',''),
 ('related','相关与待考','巴黎坐佛的年代问题','赛努奇坐佛的现场展签、馆藏年代栏与说明正文并不一致。它单列于此，不计入前面的24件响堂山归属作品。','')]
COMPARISONS=[
 {'id':'guardians','title':'佛龛下的六张面孔','intro':'同属北响堂北洞的有翼兽，如今分在纳尔逊、克利夫兰与弗利尔。先看手是按膝还是抬起，再看牙齿、腹部与卷翼。平直或折角的石面，还保留了它们与建筑相接的方式。','ids':['NEL-35-276','CLE-1957.360','FSG-F1977.8','FSG-F1953.86','FSG-F1953.87','FSG-F1977.9'],'photo_groups':[[716,['NEL-35-276']],[720,['CLE-1957.360']],[734,['FSG-F1977.8','FSG-F1953.86']],[735,['FSG-F1953.87','FSG-F1977.9']]]},
 {'id':'faces','title':'刻经洞的佛与弟子','intro':'克利夫兰和弗利尔的两颗佛头，与传阿难的年轻弟子头像，均按研究归属联系到北响堂南洞。眉眼和口角的转折、发式的不同，比笼统地说“北齐风格”更容易落实到眼前的作品。','ids':['CLE-1923.97','FSG-F1913.67','FSG-F1913.134'],'photo_groups':[[722,['CLE-1923.97']],[729,['FSG-F1913.67']],[731,['FSG-F1913.134']]]},
 {'id':'cave-two','title':'南响堂第二窟：从浮雕到立像','intro':'华盛顿的群像浮雕与费城的独立立像，共同提示第二窟丰富的图像层次。西方净土的莲池化生、集会图中的树木与人物，以及观音冠中的小佛，分别用不同方式说明身份和场景。两馆现在的陈列位置不等于原来的主坛排列。','ids':['FSG-F1921.2','FSG-F1921.1','FSG-F1968.45','PEN-C113','PEN-C151','PEN-C150'],'photo_groups':[[725,['FSG-F1921.2']],[726,['FSG-F1921.1']],[727,['FSG-F1968.45']],[739,['PEN-C113','PEN-C151','PEN-C150']]]},
 {'id':'southern-heads','title':'南响堂范围内的两颗佛头','intro':'大都会与波特兰的两件佛头，都被联系到第三至第六窟范围。比较头顶发卷、耳与下颌的比例，再看眼睑如何与双颊衔接；具体原窟仍未确定。','ids':['MET-57.176','PAM-51.255'],'photo_groups':[[706,['MET-57.176']],[743,['PAM-51.255']]]}]

def build():
 base=ROOT/'museum-notes/xiangtangshan';d=json.loads((base/'data/works.json').read_text());works=d['works'];byid={w['id']:w for w in works};assets={a['number']:a for a in d['assets']}
 assert len(works)==len(byid)==25
 assert sum(w['scope']=='core_attributed' for w in works)==24
 assert len(assets)==45 and len(d['excluded'])==1
 identities={(w['museum_key'],re.sub(r'[^a-z0-9]','',w['accession'].lower())) for w in works};assert len(identities)==25
 for w in works:
  for n in set(w['photos']+w['labels']):
   assert w['id'] in assets[n]['work_ids']
   assert (base/assets[n]['web_path']).is_file()
 def sources(ss):
  return '<div class="work-sources">'+''.join(f'<p><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["title"])} ↗</a></p>' for s in ss)+'</div>'
 def shell(title,body,depth=0):
  note='../'*(depth+1);topic='../'*depth or './'
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · 博物馆札记 | Merton</title><meta name="description" content="{e(d['intro'])}"><link rel="stylesheet" href="{note}museum.css"><link rel="stylesheet" href="{note}caravaggio/caravaggio.css"><link rel="stylesheet" href="{topic}xiangtangshan.css"><script src="{note}caravaggio/caravaggio.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="{note}">Merton</a><nav aria-label="主导航"><a href="{note}chinese-buddhist-art/">中国佛教艺术</a><a href="{topic}#collection">原属洞窟</a><a href="{topic}compare/">跨馆比较</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="{note}">← 博物馆札记</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX.replace('原图 ↗','大图 ↗')}</body></html>'''
 def crumbs(tail='',depth=0):
  note='../'*(depth+1);topic='../'*depth or './'
  return f'<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="{note}">博物馆札记</a><span>/</span><a href="{note}chinese-buddhist-art/">中国佛教艺术</a><span>/</span>'+ (f'<a href="{topic}">响堂山石窟</a><span>/</span><span>{e(tail)}</span>' if tail else '<span>响堂山石窟</span>')+'</nav>'
 def img(n,prefix='',large=False,alt='',high=False):
  a=assets[n];p='web' if large else 'thumbnail'
  return f'<img src="{prefix}{a[p+"_path"]}" alt="{e(alt)}" width="{a[p+"_width"]}" height="{a[p+"_height"]}" {"fetchpriority=high" if high else "loading=lazy"} decoding="async">'
 def caption(w,n):
  if n==w['hero']:return f'{w["title"]} · {w["museum"]} · {w["accession"]}'+ (' · '+w['position'] if w['position'] else '')
  if n==747:return '西方净土浮雕细部：中央佛、华盖与莲池 · F1921.2'
  if n==727:return '弗利尔展厅：两块浮雕与中央独立菩萨立像F1968.45'
  return f'{w["title"]} · {w["accession"]} · 补充视角'
 def photo(n,cap,prefix='',large=False,high=False,text=None):
  return f'<a data-photo href="{prefix}{assets[n]["web_path"]}" data-caption="{e(cap)}">{text or img(n,prefix,large,cap,high)}</a>'
 def card(w,prefix=''):
  search=' '.join(str(w[k]) for k in ('title','name_en','accession','museum','cave_zh','observation'))
  return f'''<article class="art-card" id="{w['slug']}" data-search="{e(search)}" data-museum="{w['museum_key']}" data-tags="{w['group']}"><a class="art-thumbnail" href="{prefix}{w['slug']}/">{img(w['hero'],prefix,alt=caption(w,w['hero']))}</a><div class="art-card-copy"><p class="card-kicker">{e(w['date'])} · {e(w['accession'])}</p><h3><a href="{prefix}{w['slug']}/">{e(w['title'])}</a></h3><p class="card-museum">{e(w['museum'])}{(' · '+e(w['position'])) if w['position'] else ''}</p><p class="card-look">{e(w['observation'])}</p><div class="card-actions"><a href="{prefix}{w['slug']}/">作品札记 →</a>{photo(w['hero'],caption(w,w['hero']),prefix,text='放大照片 ↗')}</div></div></article>'''
 hero=byid['MET-51.52']
 intro=f'''<aside class="editorial-note wrap"><h2>从残件回到洞窟</h2><p>响堂山石窟位于河北邯郸地区。北齐（550—577）以邺城为重要政治中心，皇室、官员与僧人参与了这一地区的石窟营造。北响堂的三座主要洞窟与南响堂的较小洞窟群，各自包含佛、菩萨、弟子及建筑装饰。</p><p>20世纪初以来，大量造像被凿离、售出，留在原地的石像也多有头、手残缺。今天在纽约、华盛顿、费城等城市遇见的独立雕塑，曾经与佛龛、塔柱、经文共同构成礼拜空间。芝加哥大学响堂山项目通过原窟调查、旧照片及散件记录，研究这些联系。</p>{sources([{'title':'芝加哥大学响堂山石窟项目：项目介绍','url':'https://xts.uchicago.edu/zh-hans/node/1'}])}</aside>'''
 opts=''.join(f'<option value="{k}">{e(v)}</option>' for k,v in sorted({w['museum_key']:w['museum'] for w in works}.items()))
 nav='<nav class="era-nav" aria-label="按洞窟浏览">'+''.join(f'<a href="#{g[0]}">{g[1]}</a>' for g in GROUPS)+'</nav>'
 controls=f'''<div class="art-controls" hidden data-count-unit="件条目（含待考）"><div class="art-fields"><label>搜索名称、编号或细节<input id="art-search" type="search" placeholder="佛头、莲池、F1921.2…"></label><label>按收藏机构<select id="art-museum"><option value="all">全部博物馆</option>{opts}</select></label><label>原属洞窟<select id="art-subject"><option value="all">全部分组</option>{''.join(f'<option value="{g[0]}">{g[1]}</option>' for g in GROUPS)}</select></label></div><div class="art-results"><span id="art-count" role="status" aria-live="polite">25 / 25 件条目（含待考）</span><div><button id="art-reset" type="button">重置筛选</button><button id="gallery-mode" type="button" aria-pressed="false">画廊模式</button></div></div></div><p id="art-empty" hidden>没有符合条件的作品。</p>'''
 groups=''
 for key,title,sub,desc,url in GROUPS:
  sel=[w for w in works if w['group']==key]
  groups+=f'<section class="era-section" id="{key}"><header class="era-heading"><p class="eyebrow">{e(sub)} · {len(sel)} 件</p><h2>{e(title)}</h2><p>{e(desc)}</p>'+ (sources([{'title':'响堂山项目：'+title,'url':url}]) if url else '')+'</header><div class="art-grid">'+''.join(card(w) for w in sel)+'</div></section>'
 routes='<section class="car-reading wrap"><h2>在不同博物馆之间看</h2><div class="route-grid">'+''.join(f'<a class="reading-route" href="compare/#{c["id"]}"><h3>{e(c["title"])}</h3><p>{e(c["intro"])}</p></a>' for c in COMPARISONS[:3])+'</div></section>'
 body=crumbs()+f'''<section class="car-hero wrap"><div class="car-hero-copy"><p class="eyebrow">XIANGTANGSHAN / NORTHERN QI</p><h1>响堂山石窟</h1><p class="car-lede">海外所见</p><p class="car-intro">{e(d['intro'])}</p><div class="hero-links"><a href="#collection">沿着洞窟看 ↓</a><a href="compare/">跨馆比较 →</a></div><p class="car-stats"><b>24</b> 件响堂山归属作品 · 6 家博物馆<br>另有巴黎坐佛 1 件，归属待考</p></div><figure class="car-hero-image">{photo(hero['hero'],caption(hero,hero['hero']),large=True,high=True)}<figcaption>巨型菩萨头像 · 北响堂中洞<br><span>大都会艺术博物馆 · 51.52</span></figcaption></figure></section>'''+intro+routes+f'<section class="car-collection wrap" id="collection"><div class="car-heading"><h2>沿着原属洞窟看</h2><p>归属范围与资料差异见各件札记</p></div>{nav}{controls}{groups}</section>'
 (base/'index.html').write_text(shell(d['title'],body))
 for w in works:
  fields=[('收藏',w['museum']),('编号',w['accession']),('年代',w['date']),('材料',w['material']),('原属洞窟',w['cave_zh'])]
  if w['position']:fields.append(('照片位置',w['position']))
  facts='<dl class="work-facts">'+''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in fields)+'</dl>'
  paragraphs='<section><h2>作品札记</h2>'+''.join(f'<p>{e(p)}</p>' for p in w['paragraphs'])+'</section>'
  labels=[w['label']]
  if w['label']==728:labels=[728,748]
  labelhtml='<details class="xts-labels"><summary>现场展签</summary>'+''.join('<figure>'+photo(n,f'{w["museum"]} · 现场展签 · '+('上段对应1923.97，下段对应1972.166' if n==724 else ('共用展签' if len(assets[n]['work_ids'])>1 else w['accession'])),'../',large=True)+'</figure>' for n in labels)+'</details>'
  other=[n for n in w['photos'] if n!=w['hero']]
  gallery=('<section class="related-section wrap"><h2>现场与细部</h2><div class="xts-extra">'+''.join('<figure>'+photo(n,caption(w,n),'../',large=True)+f'<figcaption>{e(caption(w,n))}</figcaption></figure>' for n in other)+'</div></section>') if other else ''
  comparisons=[c for c in COMPARISONS if w['id'] in c['ids']]
  others=[x for x in works if x['group']==w['group'] and x['id']!=w['id']]
  related='<section class="related-section wrap"><h2>接着看</h2><div class="relation-links">'+''.join(f'<a href="../compare/#{c["id"]}">{e(c["title"])} →</a>' for c in comparisons)+''.join(f'<a href="../{x["slug"]}/">{e(x["museum"])} · {e(x["title"])} · {e(x["accession"])} →</a>' for x in others[:6])+f'<a href="../#{w["group"]}">返回这一组 →</a></div></section>'
  body=crumbs(w['title'],1)+f'''<header class="work-heading wrap"><p class="eyebrow">XIANGTANGSHAN / {e(w['cave_zh'])}</p><h1>{e(w['title'])}</h1><p class="work-original">{e(w['name_en'])}</p></header><div class="work-layout wrap"><figure class="work-photo">{photo(w['hero'],caption(w,w['hero']),'../',large=True,high=True)}<figcaption>{e(caption(w,w['hero']))} · 点击放大</figcaption></figure><div class="work-record">{facts}{paragraphs}{('<p class="record-note">'+e(w['note'])+'</p>') if w['note'] else ''}{sources(w['sources'])}{labelhtml}</div></div>{gallery}{related}'''
  target=base/w['slug'];target.mkdir(exist_ok=True);(target/'index.html').write_text(shell(w['title'],body,1))
 body=crumbs('跨馆比较',1)+'<header class="compare-header wrap"><p class="eyebrow">XIANGTANGSHAN / SIDE BY SIDE</p><h1>把散件放在一起看</h1><p>从表情、姿态和装饰，逐步看到原来洞窟中的关系。</p><p class="source">照片按版面排列，未按实物等比例显示。</p><nav class="compare-nav">'+''.join(f'<a href="#{c["id"]}">{e(c["title"])}</a>' for c in COMPARISONS)+'</nav></header><div class="wrap">'
 for c in COMPARISONS:
  cells=''
  for n,ids in c['photo_groups']:
   ws=[byid[i] for i in ids];cap='；'.join(caption(w,n) for w in ws)
   cells+='<figure class="comparison-work">'+photo(n,cap,'../',large=True)+'<figcaption>'+''.join(f'<a href="../{w["slug"]}/">{e(w["title"])} · {e(w["accession"])} →</a><span>{e(w["museum"])}{(" · "+e(w["position"])) if w["position"] else ""}</span>' for w in ws)+'</figcaption></figure>'
  body+=f'<section class="compare-group" id="{c["id"]}"><h2>{e(c["title"])}</h2><p>{e(c["intro"])}</p><div class="comparison-grid" style="--columns:{min(3,len(c["photo_groups"]))}">{cells}</div></section>'
 body+='</div>'
 (base/'compare').mkdir(exist_ok=True);(base/'compare/index.html').write_text(shell('跨馆比较 · 响堂山石窟',body,1))
 integrate(d,hero,assets)
 print('Built Xiangtangshan: 24 attributed + 1 disputed; 27 pages; 45 assets accounted for; existing Penn luohan reused.')

def integrate(d,hero,assets):
 """Update existing generated directories; repeated builds replace marked entries."""
 notes=ROOT/'museum-notes';p=notes/'chinese-buddhist-art/index.html';s=p.read_text()
 s=re.sub(r'<!-- xiangtangshan-entry -->.*?<!-- /xiangtangshan-entry -->','',s,flags=re.S)
 s=s.replace('造像 · 四个专题','造像 · 五个专题')
 a=assets[hero['hero']]
 entry=f'''<!-- xiangtangshan-entry --><a class="issue-link" href="../xiangtangshan/"><img src="../xiangtangshan/{a['thumbnail_path']}" alt="响堂山中洞巨型菩萨头像" width="{a['thumbnail_width']}" height="{a['thumbnail_height']}" loading="lazy"><div><p class="eyebrow">005 / XIANGTANGSHAN</p><h2>响堂山石窟：海外所见</h2><p>从佛头、菩萨、有翼兽与大浮雕，回看分散在不同博物馆里的洞窟造像。</p><p class="issue-meta">24 件响堂山归属作品 · 另有 1 件待考<br>原属洞窟 / 收藏机构 / 跨馆比较</p><span class="text-link">走进这一辑 →</span></div></a><!-- /xiangtangshan-entry -->'''
 marker='</section><section class="material-directory"';assert marker in s;s=s.replace(marker,entry+marker,1);p.write_text(s)
 p=notes/'buddhist-sculpture/data/topics.json';topics=json.loads(p.read_text());old_ids={n for t in topics['topics'] for n in t['ids']}
 assert 741 in old_ids and d['excluded'][0]['existing_url'].endswith('#object-741')
 topics['external_topics']=[{'id':'xiangtangshan','title':d['title'],'data':'../../xiangtangshan/data/works.json','core_count':24,'related_count':1,'reused_ids':['object-741']}]
 topics['selected_count']=len(old_ids)+24;topics['related_count']=1
 p.write_text(json.dumps(topics,ensure_ascii=False,indent=2)+'\n')
 p=notes/'index.html';s=p.read_text()
 s=s.replace('水月观音、五代至元木雕、干漆与漆塑、易县三彩罗汉，一辑一辑细看。','从水月观音、木雕、漆塑与三彩罗汉，继续走进响堂山石窟。')
 s=s.replace(f'4 个造像专题 · {len(old_ids)} 件造像（去重） ·',f'5 个造像专题 · {len(old_ids)+24} 件造像＋1件待考（去重） ·')
 s=s.replace('水月观音 / 五代至元木雕 / 干漆与漆塑 / 易县三彩罗汉','水月观音 / 五代至元木雕 / 干漆与漆塑 / 易县三彩罗汉 / 响堂山石窟')
 p.write_text(s)
if __name__=='__main__':build()
