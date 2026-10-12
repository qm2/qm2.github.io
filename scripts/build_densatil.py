"""Build a small Densatil study with original visit photographs and evidence levels."""
from pathlib import Path
from html import escape as e
import json,re
from build_paintings import picture,frame
ROOT=Path(__file__).resolve().parents[1]
def build():
 base=ROOT/'museum-notes/densatil';d=json.loads((base/'data/works.json').read_text())
 numbers={k:i+1 for i,k in enumerate(d['sources'])}; references={k:[] for k in numbers}
 def cites(keys):
  links=[]
  for k in dict.fromkeys(keys):
   ref=f'cite-{k}-{len(references[k])+1}'; references[k].append(ref)
   links.append(f'<a id="{ref}" href="#source-{k}" aria-label="资料{numbers[k]}：{e(d["sources"][k][0])}">[{numbers[k]}]</a>')
  return '<sup class="ds-citations">'+''.join(links)+'</sup>' if links else ''
 def paragraphs(items):return ''.join('<p>'+e(p['text'])+cites(p['sources'])+'</p>' for p in items)
 def founder(w):
  f=d['founder']
  if w['id']!=f['work']:return ''
  return f'<aside class="ds-founder" aria-labelledby="founder-title"><h3 id="founder-title">{e(f["title"])}</h3><p class="ds-founder-name">{e(f["name"])}</p><p class="ds-record-note">{e(f["metadata"])}</p>{paragraphs(f["paragraphs"])}</aside>'
 def photo(w,label=False,eager=False):
  p=d['photos'][str(w['label' if label else 'photo'])];caption=w['title']+' · '+w['museum']+(' · 现场展签' if label else ' · '+w['caption'])
  return f'<a class="photo-open" href="images/{p["photo"]}" data-caption="{e(caption)}" aria-label="放大：{e(caption)}">{picture(p,"images/",caption,eager)}</a>'
 body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>丹萨替寺造像</span></nav><header class="ds-intro wrap"><p class="eyebrow">DENSATIL / SCULPTURE AND SACRED SPACE</p><h1>{e(d['title'])}</h1><p class="subtitle">{e(d['subtitle'])}</p><p class="ds-lede">{e(d['intro'])}</p><nav class="ds-nav" aria-label="专题阅读"><a href="#collection">从三组作品看起 ↓</a><a href="#history">寺院与纪念塔</a><a href="#structure">六层结构示意</a><a href="#positions">它原来在哪里</a></nav></header><section class="wrap" id="collection"><h2>造像，也是建筑的一部分</h2>'''
 # Start with the large relief, then the dancing deity, then architectural supports.
 for i,w in enumerate([d['works'][1],d['works'][2],d['works'][0]]):
  facts=[('收藏',w['museum']),('编号',w['accession']),('年代',w['date']),('材料',w['medium']),('尺寸',w['dimensions'])]
  body+=f'''<article class="ds-work" id="{w['id']}"><div class="ds-images"><figure>{photo(w,eager=i==0)}<figcaption>{e(w['caption'])} · Merton参观照片</figcaption></figure><details><summary>现场展签 <span>＋</span></summary><figure>{photo(w,True)}<figcaption>{e(w['title'])} · 现场展签</figcaption></figure></details>{founder(w)}</div><div class="ds-notes"><p class="eyebrow">{i+1:02d} / DENSATIL</p><h3>{e(w['title'])}</h3><p class="ds-original" lang="en">{e(w['original_title'])}</p><dl>{''.join('<div><dt>'+e(k)+'</dt><dd>'+e(v)+'</dd></div>' for k,v in facts)}</dl><p class="ds-attribution">{e(w['museum_attribution'])}</p>{paragraphs(w['notes'])}<p class="ds-record-note">{e(w['record_note'])}</p><a class="text-link" href="#position-{w['id']}">原位与归属依据 ↓</a></div></article>'''
 body+='</section><section class="wrap ds-section" id="history"><p class="eyebrow">MONASTERY / LINEAGE / RELIQUARIES</p><h2>寺院与吉祥多门塔</h2><div class="ds-history">'
 for h in d['history']:body+='<section><h3>'+e(h['title'])+'</h3>'+paragraphs(h['paragraphs'])+'</section>'
 body+='</div></section><section class="wrap ds-section" id="structure"><h2>一座塔中的六层世界</h2><p class="ds-measure">'+e(d['structure']['intro'])+'</p><div class="ds-tier-diagram" aria-label="六层结构示意，由上至下"><div class="ds-reliquary">上部舍利塔</div><ol>'
 for n,title,desc in d['structure']['tiers']:body+=f'<li style="--tier:{n}"><span class="ds-tier-number">{n}</span><div><h3>{e(title)}</h3><p>{e(desc)}</p></div></li>'
 body+='</ol></div>'+cites(d['structure']['sources'])+'<p class="ds-measure">这是整体图像程序的简图。两件尊像的塔号与层位是下文所列的研究归属；承托柱的具体位置仍未确定。</p></section><section class="wrap ds-section" id="positions"><p class="eyebrow">ORIGINAL SETTING / EVIDENCE</p><h2>它原来在哪里</h2><p class="ds-measure">以下塔序均指八座大型吉祥多门塔中的序号，层数由上往下数。馆方归属、研究重建与尚存空白，分别列出。</p><div class="ds-table-scroll" tabindex="0" role="region" aria-label="三组作品原位对照表，可横向滚动"><table class="ds-positions"><thead><tr><th scope="col">作品</th><th scope="col">馆方说法</th><th scope="col">研究归属</th><th scope="col">仍未知</th></tr></thead><tbody>'
 for w in d['works']:
  q=w['position'];body+=f'<tr id="position-{w["id"]}"><th scope="row"><a href="#{w["id"]}">{e(w["title"])}</a></th><td>{e(q["confirmed"])}{cites(q["confirmed_sources"])}</td><td>{e(q["proposed"])}{cites(q["proposed_sources"])}</td><td>{e(q["unknown"])}</td></tr>'
 body+='</tbody></table></div></section><section class="wrap ds-section" id="old-photos"><h2>旧照片与散藏造像</h2><div class="ds-measure">'+paragraphs(d['old_photos'])+'</div><div class="ds-photo-links">'
 for link in d['photo_links']:body+=f'<article><h3>{e(link["title"])}</h3><p>{e(link["text"])}</p><a class="text-link" href="{e(d["sources"][link["source"]][1])}">查看原始资料中的照片 ↗</a></article>'
 body+='</div></section><section class="wrap ds-section ds-sources" id="sources"><h2>精选参考资料</h2><ol>'
 for k,(name,url) in d['sources'].items():
  back=' '.join(f'<a class="ds-backref" href="#{ref}" aria-label="返回资料{numbers[k]}的第{i+1}处引用">↩{i+1}</a>' for i,ref in enumerate(references[k]))
  body+=f'<li id="source-{k}"><a href="{e(url)}">{e(name)} ↗</a> <span class="ds-backrefs">{back}</span></li>'
 body+='</ol><p>2014年展览图录由Olaf Czaja与Adriana Proser编。上文展品号及页码据各馆公开书目；具体塔位讨论另据所链接的Estournel研究。</p></section>'

 page=frame(d['title'],body,description=d['intro'],sibling=True).replace('<a href="../chinese-painting/">中国书画</a>','<a href="../chinese-buddhist-art/">中国佛教艺术</a>').replace('</head>','<link rel="stylesheet" href="densatil.css"></head>')
 (base/'index.html').write_text(page)
 parent=ROOT/'museum-notes/chinese-buddhist-art/index.html';s=re.sub(r'<!-- densatil-entry -->.*?<!-- /densatil-entry -->','',parent.read_text(),flags=re.S)
 entry='''<!-- densatil-entry --><a class="issue-link" href="../densatil/"><img src="../densatil/images/778.jpg" width="1280" height="1707" loading="lazy" alt="西雅图的金刚亥母，丹萨替寺相关造像"><div><p class="eyebrow">006 / DENSATIL</p><h2>丹萨替寺造像</h2><p>吉祥天母、金刚亥母与一对承托柱：从三组亲见作品，回看吉祥多门塔的宗教空间。</p><p class="issue-meta">原位研究 / 六层结构 / 旧照片的线索</p><span class="text-link">走进这一辑 →</span></div></a><!-- /densatil-entry -->'''
 anchor='</section><section class="material-directory"';assert anchor in s;s=s.replace(anchor,entry+anchor,1).replace('造像 · 五个专题','造像 · 六个专题');parent.write_text(s)
 home=ROOT/'museum-notes/index.html';s=re.sub(r'<!-- densatil-home -->.*?<!-- /densatil-home -->','',home.read_text(),flags=re.S)
 # Keep the home entrance concise; the earlier sculpture ledger is not the count of this independent batch.
 s=re.sub(r'5 个造像专题 · \d+ 件造像＋1件待考（去重） ·','6 个造像专题 ·',s)
 anchor='<a class="issue-link" href="chinese-painting/">';assert anchor in s;s=s.replace(anchor,'<!-- densatil-home --><p class="topic-return"><a href="densatil/">丹萨替寺造像：尊神、承托柱与原来的塔 →</a></p><!-- /densatil-home -->'+anchor,1);home.write_text(s)
 print('Built Densatil: 3 groups (including paired supports), 6 unchanged published photographs, 2 entrances.')
if __name__=='__main__':build()
