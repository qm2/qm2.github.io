"""Build the Xuzhou notebook from reviewed content and preserved photo mappings."""
from pathlib import Path
from html import escape as e
import json,re
from build_paintings import frame
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/xuzhou'
def build():
 d=json.loads((BASE/'data/works.json').read_text());photos=json.loads((BASE/'data/photos.json').read_text());works=d['works'];byid={w['id']:w for w in works}
 def photo(n,caption,prefix='',eager=False,card=False):
  p=photos[n];src=prefix+'images/'+p['original'];variants=p['variants'];v=variants[0 if card else -1]
  sizes='(max-width: 600px) 90vw, (max-width: 1000px) 45vw, 360px' if card else '(max-width: 700px) 90vw, 960px'
  markup=f'<span class="image-box" style="--ratio:{p["width"]/p["height"]:.8f};--native-width:{p["width"]}px"><img src="{prefix}images/{v["file"]}" srcset="'+', '.join(f'{prefix}images/{v["file"]} {v["width"]}w' for v in variants)+f', {src} {p["width"]}w" sizes="{sizes}" alt="{e(caption)}" width="{p["width"]}" height="{p["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async"></span>'
  if card:return markup
  return f'<a class="photo-open" href="{src}" data-full-src="{src}" data-caption="{e(caption)}" aria-label="放大：{e(caption)}">{markup}</a>'
 def shell(title,body,detail=False):
  s=frame(title,body,description=d['brief'],sibling=True)
  if detail:s=s.replace('href="../"','href="../../"').replace('../museum.css','../../museum.css').replace('../chinese-painting/','../../chinese-painting/')
  s=s.replace(f'<a href="{"../../" if detail else "../"}chinese-painting/">中国书画</a>',f'<a href="{"../" if detail else "./"}">虚舟收藏</a>')
  return s.replace('</head>',f'<link rel="stylesheet" href="{"../" if detail else ""}xuzhou.css"><script src="{"../" if detail else ""}xuzhou.js" defer></script></head>')
 def sources(keys,detail=False):
  return '<p class="source">'+ ' · '.join(f'<a href="{e(d["sources"][k]["url"])}">{e(d["sources"][k]["title"])} ↗</a>' for k in dict.fromkeys(keys) if k!='label')+'</p>' if any(k!='label' for k in keys) else ''
 def links(ids,prefix=''):
  return ' · '.join(f'<a href="{prefix}{i}/">{e(byid[i]["title"])} →</a>' for i in ids)
 def card(w,prefix=''):
  return f'<article class="xz-card" id="{w["id"]}" data-region="{w["region_group"]}"><a href="{prefix}{w["id"]}/">{photo(w["main_photo"],w["title"]+" · "+w["region_label"],prefix,card=True)}<h3>{e(w["title"])}</h3></a><p class="xz-meta">{e(w["region_label"])} · {e(w["date_display"])}</p><p class="xz-material">{e(w["material_label"])}</p><p>{e(w["short"])}</p></article>'
 body=f'<div class="wrap xz-heading"><p class="eyebrow">THE XUZHOU COLLECTION / HOUSTON</p><h1>{d["title"]}</h1><nav class="xz-nav" aria-label="专题章节"><a href="#reading">八组细读</a><a href="#catalogue">浏览图录</a><a href="#about">收藏与资料</a></nav></div>'
 intro_paragraphs=''.join('<p>'+e(t)+'</p>' for t in d['intro'])
 body+=f'<figure class="wrap xz-hero">{photo(d["hero"],"休斯顿美术馆的虚舟收藏展厅 · 中央为智慧佛立像",eager=True)}<figcaption>休斯顿美术馆 · 展厅中央的智慧佛与周围造像 · Merton摄</figcaption></figure><section class="wrap xz-intro"><blockquote class="xz-epigraph"><p>“{e(d["epigraph"]["text"])}”</p><footer>——{e(d["epigraph"]["source"])}</footer></blockquote>{intro_paragraphs}<p class="xz-meta">{e(d["brief"])} <a href="#about">关于这份收藏 ↓</a></p></section>'
 body+='<section class="wrap xz-section" id="reading"><p class="eyebrow">LOOKING CLOSER</p><h2>从八个问题看起</h2><div class="xz-reading-grid">'
 for f in d['features']:
  body+=f'<article class="xz-feature" id="{f["id"]}"><a href="{f["works"][0]}/">{photo(f["photo"],f["title"],card=True)}<h3>{e(f["title"])}</h3></a><p>{e(f["text"])}</p><p class="xz-related">{links(f["works"])}</p></article>'
 body+='</div></section><section class="wrap xz-section" id="catalogue"><p class="eyebrow">THE NOTEBOOK / 28 WORKS</p><h2>虚舟图录</h2><p>按地区翻看，也从一尊像走向相近的姿态、材料或故事。</p><div class="xz-filters" hidden aria-label="按地区筛选"><button type="button" data-region-filter="all" aria-pressed="true">全部</button>'+''.join(f'<button type="button" data-region-filter="{k}" aria-pressed="false">{e(t)}</button>' for k,t in d['groups'])+'</div><p class="xz-count" role="status" aria-live="polite">28件虚舟收藏作品</p>'
 for k,t in d['groups']:
  body+=f'<section class="xz-region" data-region-section="{k}"><h3>{e(t)}</h3><div class="xz-grid">'+''.join(card(w) for w in works if w['collection']=='xuzhou' and w['region_group']==k)+'</div></section>'
 body+='</section><section class="wrap xz-section xz-prose" id="about"><p class="eyebrow">COLLECTION / CONTEXT</p><h2>在休斯顿重看亚洲造像</h2><p>虚舟收藏由一位不具名的私人收藏者建立，自2021年起长期借展于休斯顿美术馆。南亚、东南亚、喜马拉雅与东亚的造像，在这里共同呈现。参观时所见的地区名称有不同尺度：犍陀罗是历史文化区域，斯瓦特是河谷，大克什米尔也不等同于一条现代国界。</p>'+sources(['mfah-press','mfah-exhibition'])
 body+='<p>展厅总说明把“虚舟”联系到佛教以舟筏比喻教法的传统：借助教法渡越无明。回到作品上，材料、手势与题记各自提供了入口。漆布怎样塑成佛首，嵌银怎样显出衣缝，供养者怎样把父母的愿望写入像座，这些具体的问题，让不同地区的造像有了可以互相参照的地方。</p><details><summary>展厅说明与观看空间</summary><div class="xz-context">'
 for n,c in [('954','虚舟收藏总说明'),('1062','同柜的朝鲜半岛与日本造像'),('988','展厅与相邻空间')]:body+=f'<figure>{photo(n,c)}<figcaption>{c} · Merton摄</figcaption></figure>'
 body+='</div></details><h3>继续阅读</h3><p><cite>Approaching the Buddha: Transmission and Transformation</cite>，Hao Sheng著，另有八位研究者参与撰写，休斯顿美术馆出版、耶鲁大学出版社发行，2026年，128页。图录从供养、观看、传播与保护研究等方面讨论这一收藏。</p>'+sources(['catalog-description','catalog-publisher'])
 body+='<details id="sources"><summary>资料说明与参考链接</summary><p>逐件年代、材质与题名主要依据现场展签，照片可在作品页展开查看；观看分析来自所附实拍。图录列作延伸阅读。尚有分歧的年代、展签错配及未释清的题记，分别记在相关作品的资料注中。</p><ul>'+''.join(f'<li><a href="{e(v["url"])}">{e(v["title"])} ↗</a></li>' for v in d['sources'].values())+'</ul></details></section>'
 (BASE/'index.html').write_text(shell(d['title'],body))
 for w in works:
  out=BASE/w['id'];out.mkdir(exist_ok=True);prefix='../';owned=w['collection']=='mfah-neighbor'
  epigraph=''
  if w.get('epigraph'):
   q=w['epigraph'];epigraph='<blockquote class="xz-work-epigraph"><p>“'+e(q['text'])+'”</p><footer>——<a href="'+e(q['url'])+'" title="'+e(q['location'])+'">'+e(q['source'])+'</a></footer></blockquote>'
  b=f'<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../../">博物馆札记</a><span>/</span><a href="../">虚舟收藏</a><span>/</span><span>{"邻展作品" if owned else e(w["region_label"])}</span></nav><section class="wrap xz-work-heading"><p class="eyebrow">{"MFAH COLLECTION / NEIGHBORING WORK" if owned else "THE XUZHOU COLLECTION"}</p><h1>{e(w["title"])}</h1><p class="xz-original" lang="en">{e(w["original_title"])}</p><p class="subtitle">{e(w["short"])}</p>{epigraph}</section><section class="wrap xz-work"><figure>{photo(w["main_photo"],w["title"]+" · Merton摄",prefix,True)}<figcaption>{e(w["title"])} · 休斯顿美术馆所见 · 点击放大</figcaption></figure><div class="xz-facts"><dl>'
  facts=[('地区',w['region_label']),('年代',w['date_display']),('材料',w['material_label']),('收藏','休斯顿美术馆' if owned else '虚舟收藏（私人收藏）'),('观看地点','休斯顿美术馆（MFAH）')]
  if w.get('dimensions'):facts.append(('尺寸',w['dimensions']))
  if w['accession']:facts.append(('馆藏号',w['accession']))
  b+=''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in facts)+'</dl><a class="text-link" href="#label">查看现场展签 ↓</a></div></section><section class="wrap xz-notes xz-prose"><h2>作品札记</h2>'
  def work_references(keys):
   return '<p class="source">'+' · '.join('<a href="'+e(w['references'][k]['url'])+'">'+e(w['references'][k]['title'])+' ↗</a>' for k in keys)+'</p>' if keys else ''
  for p in w['notes']:
   if p.get('heading'):b+='<h3>'+e(p['heading'])+'</h3>'
   b+='<p>'+e(p['text'])+'</p>'
   if p.get('quote'):
    q=p['quote'];b+='<blockquote class="xz-note-quote" lang="'+e(q['lang'])+'"><p>'+e(q['text'])+'</p></blockquote><p class="xz-meta">'+e(q['credit'])+'</p>'
   b+=work_references(p.get('references',[]))
  for note in w.get('reading_notes',[]):
   b+='<details class="xz-record"><summary>'+e(note['title'])+'</summary>'+''.join('<p>'+e(t)+'</p>' for t in note['paragraphs'])+work_references(note.get('references',[]))+'</details>'
  b+='<p class="source"><a href="#label">休斯顿美术馆现场展签'+('' if w.get('natural_captions') else ' · 照片'+w['label_photo'])+'</a></p>'+sources(w['source_ids'])
  if w.get('inscription'):b+='<p class="source"><a href="'+e(w['inscription']['source']['url'])+'">佳士得：本件造像与纹饰说明 ↗</a></p>'
  if w['record_note'] and not w.get('history'):b+='<details class="xz-record"><summary>资料注</summary><p>'+e(w['record_note'])+'</p></details>'
  b+='</section>'
  history_photos=set()
  if w.get('inscription'):
   ins=w['inscription'];n=ins['photo'];history_photos.add(n)
   b+='<section class="wrap xz-section xz-prose xz-dedication" id="inscription"><h2>'+e(ins['title'])+'</h2><figure id="photo-'+n+'">'+photo(n,ins['caption'],prefix)+'<figcaption>'+e(ins['caption'])+'</figcaption></figure><p class="xz-meta">'+e(ins['credit'])+'</p><blockquote>'+e(ins['text'])+'</blockquote><p class="source"><a href="'+e(ins['source']['url'])+'">'+e(ins['source']['title'])+' ↗</a></p><h3>发愿文说了什么</h3>'
   b+=''.join('<p>'+e(t)+'</p>' for t in ins['reading'])
   if ins.get('collation'):b+='<div class="xz-collation"><h3>校读说明</h3>'+''.join('<h4>'+e(t['title'])+'</h4><p>'+e(t['text'])+'</p>' for t in ins['collation'])+'</div>'
   b+='</section>'
  if w.get('history'):
   h=w['history'];history_photos.update(p['number'] for p in h['photos'])
   def history_sources(keys):
    return '<p class="source">'+' · '.join('<a href="'+e(h['sources'][k]['url'])+'">'+e(h['sources'][k]['title'])+' ↗</a>' for k in keys)+'</p>' if keys else ''
   b+='<section class="wrap xz-section xz-history" id="'+e(h.get('id','wood-stand'))+'"><div class="xz-prose wrap"><h2>'+e(h['title'])+'</h2>'
   for p in h['paragraphs']:b+='<p>'+e(p['text'])+'</p>'
   b+=history_sources(list(dict.fromkeys(k for p in h['paragraphs'] for k in p['sources'])))
   b+='</div>'
   if h['photos']:b+='<div class="xz-inscription-photos">'
   for p in h['photos']:
    b+='<figure id="photo-'+p['number']+'">'+photo(p['number'],p['caption'],prefix)+'<figcaption>'+e(p['caption'])+'</figcaption></figure>'
   if h['photos']:b+='</div>'
   b+='<div class="xz-prose wrap">'+('<p class="xz-meta">'+e(h['photo_note'])+'</p>' if h['photo_note'] else '')+'<h3>'+e(h.get('timeline_title','公开拍卖记录'))+'</h3><ol class="xz-provenance">'
   for t in h['timeline']:b+='<li><h4>'+e(t['date'])+'</h4><p>'+e(t['text'])+'</p><p class="xz-meta">'+e(t['status'])+'</p>'+history_sources(t['sources'])+'</li>'
   b+='</ol>'
   if h.get('publications'):
    pub=h['publications'];b+='<h3>出版记录</h3><p class="xz-meta">'+e(pub['note'])+'</p><ul>'+''.join('<li>'+e(t)+'</li>' for t in pub['entries'])+'</ul>'+history_sources(pub['sources'])
   b+='<details class="xz-record"><summary>题记与递藏：资料注</summary>'+''.join('<p>'+e(t)+'</p>' for t in h['notes'])+'</details></div></section>'
  if w['detail_photos']:
   b+='<section class="wrap work-gallery xz-section" data-gallery data-direction="ltr" aria-labelledby="details-title"><h2 id="details-title">其他角度与细部</h2><div class="gallery-controls" hidden><button type="button" data-prev>上一张</button><span class="gallery-count" role="status" aria-live="polite"></span><button type="button" data-next>下一张</button><button type="button" data-show-all aria-pressed="false">展开全部</button></div><div class="gallery-stage">'
   special={'958':'背面残损与中空像身','960':'面容与胸前璎珞','961':'斜侧面与冠饰','981':'侧面：胸背与衣纹','982':'背面衣纹','1037':'台座正面题记','1041':'木座正面文字','1042':'木座侧面文字','1043':'木座另一侧文字','1049':'背光的背面','1050':'底座题记'}
   for n in w['detail_photos']:
    if n in history_photos:continue
    cap=w['title']+' · '+special.get(n,'另一角度与细部')+' · 照片'+n
    if w.get('natural_captions'):cap=w.get('photo_captions',{}).get(n,w['title']+' · 另一角度与细部')
    b+=f'<figure class="slide" id="photo-{n}">{photo(n,cap,prefix)}<figcaption>{e(cap)}</figcaption></figure>'
   b+='</div><div class="gallery-thumbs" aria-label="选择照片" hidden></div></section>'
  b+='<section class="wrap xz-prose xz-section" id="label"><details><summary>现场展签与原始记录</summary><figure>'+photo(w['label_photo'],w['title']+' · 现场展签',prefix)+'<figcaption>休斯顿美术馆现场展签 · Merton摄</figcaption></figure><dl class="xz-label-record">'+''.join('<div><dt>'+k+'</dt><dd lang="en">'+e(v)+'</dd></div>' for k,v in [('题名',w['original_title']),('地区',w['label_original']['region']),('年代',w['label_original']['date']),('材料',w['label_original']['material'])])+'</dl></details></section>'
  if w['related']:b+='<section class="wrap xz-prose xz-section"><h2>放在一起看</h2><p class="xz-related">'+links(w['related'],'../')+'</p></section>'
  if w.get('shared_identity'):b+='<p class="wrap xz-prose"><a href="'+e(w['shared_identity']['url'])+'">同一件佛首，也见于夹纻干漆专题 →</a></p>'
  b+='<nav class="wrap xz-bottom-nav" aria-label="图录导航"><a href="../#'+('neighbors' if owned else 'catalogue')+'">← 返回'+('邻展作品' if owned else '虚舟图录')+'</a></nav>'
  (out/'index.html').write_text(shell(w['title'],b,True))
 # Main index is regenerated before this idempotent insertion.
 home=ROOT/'museum-notes/index.html';s=re.sub(r'<!-- xuzhou-entry -->.*?<!-- /xuzhou-entry -->','',home.read_text(),flags=re.S)
 anchor='</section>\n<section class="future-collections"';assert anchor in s
 p=photos[d['hero']];v=p['variants'][0]
 entry=f'<a class="issue-link" href="xuzhou/"><img src="xuzhou/images/{v["file"]}" alt="休斯顿美术馆虚舟收藏展厅" width="{p["width"]}" height="{p["height"]}" loading="lazy"><div><p class="eyebrow">THE XUZHOU COLLECTION / HOUSTON</p><h2>虚舟收藏</h2><blockquote class="xz-entry-epigraph"><p>“{e(d["epigraph"]["text"])}”</p><cite>——{e(d["epigraph"]["source"])}</cite></blockquote><p class="issue-meta">28件虚舟造像<br>南亚 / 东南亚 / 喜马拉雅 / 东亚</p><span class="text-link">进入这个专题 →</span></div></a>'
 home.write_text(s.replace(anchor,'<!-- xuzhou-entry -->'+entry+'<!-- /xuzhou-entry -->'+anchor,1))
 print('Built Xuzhou: 28 collection works; 8 readings; 29 pages.')
if __name__=='__main__':build()
