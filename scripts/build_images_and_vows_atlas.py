"""Build the photo atlas from existing authoritative readings plus supplemental records."""
from pathlib import Path
from html import escape as e
import json
from build_homer import LIGHTBOX
R=Path(__file__).resolve().parents[1];B=R/'museum-notes/images-and-vows';D=B/'data';A=B/'atlas'
def load(name):return json.loads((D/name).read_text())
def build():
 if not (D/'atlas-extras.json').exists():return
 core=load('works.json');meta=load('atlas-core-metadata.json');photos=load('atlas-photos.json');museums=load('atlas-museums.json');mb={m['id']:m for m in museums};sources={x['source_id']:x for x in load('sources.json')};works=[]
 for w in core:
  x=dict(id=w['id'],title=w['title'],date=w['date']+('年' if not w['date'].endswith(('年','年代','世纪')) else ''),period=w['period'],material=w['material'],form=w['type'],dimensions=w['dimensions'],iconography=None,hero=w['hero'],photos=[dict(number=n,role=photos[str(n)]['role']) for n in w['photos']+w['labels']],reading_url='../'+w['slug']+'/',sources=[dict(title=sources[k]['publisher']+'：'+sources[k]['title'],url=sources[k]['url']) for k in w['sources'][:2]],scope='main',visit_date=None,region='南方／成都' if w['region']=='成都' else '北方',track='南朝' if w['region']=='成都' else '北朝',accession=w['accession'],catalogue_note='')
  x.update(meta[w['id']]);works.append(x)
 works+=load('atlas-extras.json')
 for x in works:
  x['city']=mb[x['museum_id']]['city'] if x.get('museum_id') else None
  x['museum']=mb[x['museum_id']]['name'] if x.get('museum_id') else '观看馆待核'
  x['material_group']='石雕' if any(t in x['material'] for t in ['石','岩']) else '金属' if any(t in x['material'] for t in ['铜','铁']) else '其他／待核'
  f=x['form'];x['form_group']='佛首' if '佛首' in f else '建筑构件／石塔' if any(t in f for t in ['构件','石塔','壁板']) else '造像碑' if '碑' in f else '背屏式造像' if any(t in f for t in ['背','龛']) else '单尊造像'
  x['date_kind_label']={'exact':'明确纪年','circa':'约年','period':'时期范围','range':'年代范围','circa_range':'约年范围','approx_range':'约年范围'}.get(x['date_kind'],'年代待核')
  x['reading_url']=x.get('reading_url') or None
 works.sort(key=lambda x:(x['year_start'] if x.get('year_start') is not None else 9999,x['id']))
 used={n['number'] for w in works for n in w['photos']};assert used==set(map(int,photos))
 active_museums=[m for m in museums if any(w.get('museum_id')==m['id'] for w in works)]
 stats=dict(works=len(works),confirmed=sum(w['status']=='confirmed' for w in works),pending=sum(w['status']!='confirmed' for w in works),photos=len(photos),museums=len(active_museums),readings=sum(bool(w['reading_url']) for w in works),exact=sum(w['date_kind']=='exact' for w in works))
 audit=json.loads((R/'docs/images-and-vows/atlas-photo-audit.json').read_text())
 excluded=json.loads((R/'docs/images-and-vows/atlas-excluded-works.json').read_text())
 archive=dict(additional_photos=sum(bool(p.get('remote_asset')) for p in photos.values()),additional_works=sum(bool(w.get('package_id')) for w in works),photos=len(audit),works=len({p['work_id'] for p in audit if p.get('work_id')}),excluded_works=len(excluded),context_photos=sum(not p.get('work_id') for p in audit))
 data=dict(works=works,photos=photos,museums=active_museums,stats=stats,archive=archive)
 def image(n,small=False):
  p=photos[str(n)];v=p['variants'][0] if small else p['variants'][min(1,len(p['variants'])-1)]
  return f'<img src="{v["file"]}" srcset="'+', '.join(f'{q["file"]} {q["width"]}w' for q in p['variants'])+f'" sizes="{"(max-width:650px) 42vw, 260px" if small else "(max-width:650px) 90vw, 580px"}" width="{p["width"]}" height="{p["height"]}" alt="{e(p["caption"])}" loading="lazy" decoding="async">'
 def figure(n,title):
  p=photos[str(n)];href=p['variants'][-1]['file'] if p['rotation_ccw'] else p['original'];caption=title+' · '+p['caption']+' · Merton摄'
  return f'<figure class="va-photo" style="--photo-width:{min(680,700*p["width"]/p["height"]):.1f}px"><a href="{href}" data-photo data-caption="{e(caption)}" aria-label="放大：{e(caption)}">{image(n)}</a><figcaption>{e(caption)}</figcaption>'+ (f'<a class="va-original" href="{p["original"]}">未旋转原片 ↗</a>' if p['rotation_ccw'] else '')+'</figure>'
 def item(w):
  facts=[('年代',w['period']+' · '+w['date']),('定年性质',w['date_kind_label']),('材质',w['material']),('形制',w['form']),('收藏',w.get('owner') or '待核'),('观看',w['museum']+' · '+(w['city'] or '城市待核')),('馆藏编号',w.get('accession') or '未取得'),('制作／地域归属',w.get('origin') or '具体制作地未详'),('出土地',w.get('discovery') or '未取得明确记录')]
  if w.get('dimensions'):facts.append(('尺寸',w['dimensions']))
  art=[p['number'] for p in w['photos'] if p['role']!='label'];labels=[p['number'] for p in w['photos'] if p['role']=='label']
  out=f'<article class="va-card" id="work-{w["id"]}" data-work="{w["id"]}"><details class="va-object"><summary><span class="va-thumb">{image(w["hero"],True)}</span><span class="va-card-title">{e(w["title"])}</span><span class="va-meta">{e(w["period"])} · {e(w["date"])}<br>{e(w["museum"])}</span><span class="va-meta">{e(w.get("accession") or "馆号未取得")} · {len(w["photos"])}张现场照片'+(' · 有细读' if w['reading_url'] else '')+'</span><span class="va-open">资料与全部照片 ＋</span></summary><div class="va-detail">'
  if w.get('title_en'):out+='<p class="va-meta">'+e(w['title_en'])+'</p>'
  if w['reading_url']:out+='<a class="va-reading" href="'+w['reading_url']+'">阅读全文 →</a>'
  out+='<dl>'+''.join('<dt>'+e(k)+'</dt><dd>'+e(v)+'</dd>' for k,v in facts)+'</dl>'
  if w.get('iconography'):out+='<p>'+e(w['iconography'])+'</p>'
  if w.get('catalogue_note'):out+='<p class="va-meta">'+e(w['catalogue_note'])+'</p>'
  if w.get('date_note') and w['date_note'] not in w.get('catalogue_note',''):out+='<p class="va-meta">'+e(w['date_note'])+'</p>'
  if w['status']!='confirmed':out+='<p class="va-meta">待核：'+e(w.get('issue','身份尚待核实'))+'</p>'
  out+='<div class="va-gallery" data-gallery="'+w['id']+'"><div class="va-photo-controls" hidden><button type="button" data-step="-1" aria-label="上一张">←</button><span aria-live="polite"></span><button type="button" data-step="1" aria-label="下一张">→</button><button type="button" data-all aria-expanded="false">展开全部</button></div><div class="va-slides">'+''.join(figure(n,w['title']) for n in art)+'</div><div class="va-photo-tabs" hidden>'+''.join(f'<button type="button" data-view="{i}">{e(photos[str(n)]["caption"])}</button>' for i,n in enumerate(art))+'</div></div>'
  out+='<details class="va-labels"><summary>现场展签'+f'（{len(labels)}张）'+'</summary>'+(''.join(figure(n,w['title']) for n in labels) if labels else '<p>作品照片下方包含展签；本件没有独立的展签照片。</p>')+'</details>'
  out+='<details class="va-evidence"><summary>资料来源与照片档案</summary><p class="va-meta">基本资料据现场展签及以下记录；未从石刻照片另作铭文释读。观看日期未提供。</p><ul>'+''.join('<li><a href="'+e(s['url'],quote=True)+'">'+e(s['title'])+' ↗</a></li>' for s in w['sources'])+'</ul><p class="va-meta">'+e(w.get('viewing_evidence') or w.get('visit_evidence',''))+'</p><ul class="va-files">'+''.join('<li><a href="'+photos[str(p['number'])]['original']+'">'+e(photos[str(p['number'])]['original_filename'])+'</a></li>' for p in w['photos'])+'</ul></details>'
  out+='</div></details><div class="va-card-actions"><label><input type="checkbox" data-compare="'+w['id']+'"> 加入并看</label>'+('<a href="'+w['reading_url']+'">阅读全文 →</a>' if w['reading_url'] else '<span class="va-meta">基础图录</span>')+'</div></article>'
  return out
 filters=''
 for key,label in [('period','朝代'),('region','地域组'),('form_group','形制'),('material_group','材质'),('museum_id','观看博物馆'),('status','核实状态')]:
  vals=sorted(set(w[key] for w in works if w.get(key)))
  filters+=f'<label>{label}<select name="{key}"><option value="">全部</option>'+''.join('<option value="'+e(v)+'">'+e(mb[v]['name'] if key=='museum_id' else {'confirmed':'身份已对应','pending':'待核'}.get(v,v))+'</option>' for v in vals)+'</select></label>'
 body=f'''<nav class="breadcrumbs"><a href="../">造像与发愿</a><span>/</span><span>所见造像</span></nav><header class="va-heading"><p class="eyebrow">ATLAS &amp; TIMELINE</p><h1>所见造像</h1><p class="va-subtitle">博物馆地图 · 年代时间线 · 完整图录</p><p>从一次次观看留下的照片出发，沿城市寻找相遇，沿年代比较面容、衣纹与背屏。每件作品只记一次，正背面、细部与展签共同留在它的记录里。</p><p class="va-meta">本辑{stats['works']}件 · {stats['museums']}家观看机构 · {stats['photos']}张现场照片 · {stats['readings']}篇细读</p></header><nav class="va-nav"><a href="#museum-map">观看地图</a><a href="#timeline">沿年代看</a><a href="#catalogue">完整图录</a><a href="#compare">选两件并看</a></nav><form class="va-filters" id="filters" hidden><label class="va-search">查找作品、馆号或题材<input type="search" name="q" placeholder="如：弥勒、C404、双面"></label>{filters}<label>排序<select name="sort"><option value="year">年代由早至晚</option><option value="year-desc">年代由晚至早</option><option value="museum">按观看馆</option><option value="title">按题名</option></select></label><button type="reset">清除筛选</button></form><p class="va-result" id="result" role="status" aria-live="polite">{stats['works']}件作品</p>
<section id="museum-map"><header class="va-section-heading"><p class="eyebrow">WHERE I SAW THEM</p><h2>在博物馆相遇</h2><p>地图标记实际观看的博物馆，制作地域和出土地另列在作品资料中。点选馆名，可查看本馆作品；全部视图与同一组筛选条件联动。</p></header><div id="map-tools" class="va-tools" hidden><button type="button" data-map-view="world" aria-pressed="true">全部观看地</button><button type="button" data-map-view="america" aria-pressed="false">美国</button><button type="button" data-map-view="asia" aria-pressed="false">中国与日本</button><button type="button" data-map-view="europe" aria-pressed="false">巴黎</button></div><div id="map-canvas" class="va-map" hidden></div><p class="va-meta">馆舍／城市级定位示意，无古代路线。底图：<a href="https://www.naturalearthdata.com/about/terms-of-use/">Natural Earth，公共领域</a>。</p><div id="museum-list" class="va-museum-list">'''
 for m in active_museums:
  ws=[w for w in works if w.get('museum_id')==m['id']];body+=f'<details id="museum-{m["id"]}" data-museum="{m["id"]}"><summary>{e(m["name"])} · {e(m["city"])} <span data-museum-count>{len(ws)}件</span></summary><div class="va-museum-content"><div class="va-miniatures">'+''.join('<a href="#work-'+w['id']+'" data-object-link="'+w['id']+'">'+image(w['hero'],True)+'<span>'+e(w['title'])+'</span></a>' for w in ws[:3])+'</div><ul>'+''.join('<li data-museum-work="'+w['id']+'"><a href="#work-'+w['id']+'">'+e(w['title']+' · '+w['date'])+'</a></li>' for w in ws)+'</ul><p class="va-meta">'+e(m['coordinate_note'])+' <a href="'+m['url']+'">馆方网站 ↗</a></p></div></details>'
 body+='''</div></section><section id="timeline"><header class="va-section-heading"><p class="eyebrow">TIME &amp; FORM</p><h2>沿年代重看</h2><p>南北两条轨道共用公元年份横轴。同年的作品分行排列；线段表示年代范围，虚线表示时期或约年范围，约年点保留“约”。时期范围不是已知制作年份。</p></header><div id="timeline-scroll" class="va-timeline-scroll" tabindex="0" aria-label="年代时间线，可横向滚动；方向键可滚动" hidden><div id="timeline-board"></div></div><noscript><p>下方图录已按年代排列；开启JavaScript可浏览时间线、联动筛选及并看。</p></noscript><p id="timeline-unplaced" class="va-meta"></p><details class="va-style-note"><summary>比较时，可以先看哪几处？</summary><p>以494年尹受国像与526年法兴像并看，比较面容、衣领和膝前衣摆；再看北齐时期部分作品的体量与衣纹。变化并不只有一个方向：地域、用途、材料与供养选择都参与塑造形象。</p><p>成都490年弥勒像与北方同期造像，可以比较同一背屏中人物的安排；双面碑则适合正背对读。每件的尺寸和断代依据见资料卡，图片并排不代表实物等比例。</p><p><a href="../na-494-yin/">北魏太和造像细读 →</a> · <a href="../faxing-526/">宽衣与石面线条 →</a> · <a href="../#north-south">成都与北方并看 →</a></p></details></section>
<section id="compare"><header class="va-section-heading"><p class="eyebrow">LOOK SIDE BY SIDE</p><h2>让两件作品相邻</h2><p>在图录中选两件，再分别切换正面、背面或细节。保留照片完整比例；实际尺寸会随图显示。</p></header><div class="va-tools" id="compare-tools" hidden><span id="compare-status" role="status" aria-live="polite">尚未选择作品</span><button type="button" id="compare-clear">清空并看</button></div><div id="compare-pair" class="va-compare"></div></section>
<section id="catalogue"><header class="va-section-heading"><p class="eyebrow">A PERSONAL CATALOGUE</p><h2>完整图录</h2><p>展开一件作品，查看全部自拍、现场展签和资料。已有独立文章的作品保留“阅读全文”入口。</p></header><div class="va-catalogue">'''+''.join(item(w) for w in works)+'''</div><p id="empty" hidden>没有符合当前条件的作品。可清除筛选重新浏览。</p></section>'''
 body+=f'''<section class="va-method"><h2>这份图录怎样计数</h2><p>初次整理的原始包共{archive['photos']}张照片，去重后识别出{archive['works']}件独立作品。此后又补入圣安东尼奥的{archive['additional_photos']}张现场照片。本辑现收录{stats['works']}件南北朝造像；{archive['excluded_works']}件唐代作品暂不展示，另有{archive['context_photos']}张建筑照片不属于本专题。正面、背面、细部和展签不重复计为作品。</p><p>馆藏身份已对应{stats['confirmed']}件，待确认身份{stats['pending']}件。{stats['exact']}件采用明确纪年，其余采用约年或范围；具体材料、出土信息与异文的空缺仍在各卡片保留。现代展签用于基本编目，石刻铭文没有据照片重新识读。</p><p>作品与现场展签摄影：Merton。馆方图片未加入图库。<a href="../">回到十五件作品的精读 →</a></p></section>'''
 A.mkdir(exist_ok=True)
 embedded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 land=(R/'museum-notes/homer/data/ne_110m_land.geojson').read_text().replace('</','<\\/')
 html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>所见造像 · 博物馆地图与年代时间线 | Merton</title><meta name="description" content="从亲见造像的博物馆、年代与多面照片，重看南北朝佛教艺术。"><link rel="canonical" href="https://qm2.github.io/museum-notes/images-and-vows/atlas/"><link rel="stylesheet" href="../../museum.css"><link rel="stylesheet" href="../../caravaggio/caravaggio.css"><link rel="stylesheet" href="../vows.css"><link rel="stylesheet" href="atlas.css"><script src="atlas.js" defer></script></head><body class="iv-page va-page" id="top"><a class="iv-skip" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="../../">Merton</a><nav aria-label="主导航"><a href="../../chinese-buddhist-art/">中国佛教艺术</a><a href="../">造像与发愿</a><a href="#catalogue">所见图录</a></nav></header><main class="wrap" id="main">'''+body+'''</main><footer class="site-footer wrap"><a href="../">← 造像与发愿</a><span>现场摄影与札记 / Merton</span><a href="#top">回到顶部 ↑</a></footer>'''+LIGHTBOX+'<script type="application/json" id="atlas-data">'+embedded+'</script><script type="application/json" id="atlas-land">'+land+'</script></body></html>'
 (A/'index.html').write_text(html)
 (A/'catalogue.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Atlas:',stats)
if __name__=='__main__':build()
