"""Static-first historical map and chronological reading, sharing the object catalogue."""
from html import escape as e
import json
from pathlib import Path

def context(base,works,grid,inline):
 load=lambda n:json.loads((base/'data'/f'{n}.json').read_text())
 places=load('history-places');periods=load('history-periods')
 # Modern Natural Earth reference geometry reused from the site's earlier atlas.
 root=base.parent;land=json.loads((root/'homer/data/ne_110m_land.geojson').read_text());rivers=json.loads((root/'early-buddhist-art/data/rivers.geojson').read_text())
 def xy(c):return ((c[0]-83.7)/7.3*1000,(26.9-c[1])/4.8*650)
 def path(cs,close=False):return 'M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in map(xy,cs))+('Z' if close else '')
 svg='<svg viewBox="0 0 1000 650" role="group" aria-label="东印度历史地理：五处圣地与寺院"><defs><clipPath id="homeland-clip"><rect width="1000" height="650"/></clipPath></defs><g clip-path="url(#homeland-clip)">'
 for f in land['features']:
  polys=f['geometry']['coordinates'];polys=polys if f['geometry']['type']=='MultiPolygon' else [polys]
  for poly in polys:
   if any(82<c[0]<93 and 20<c[1]<29 for c in poly[0]):svg+=f'<path class="ps-land" d="'+''.join(path(r,True) for r in poly)+'"/>'
 for f in rivers['features']:
  if f['properties']['name']!='Ganges':continue
  for line in f['geometry']['coordinates']:svg+='<path class="ps-river" d="'+path(line)+'"/>'
 svg+='</g><text x="220" y="95" class="ps-region-label">比哈尔 Bihar</text><text x="740" y="440" class="ps-region-label">孟加拉 Bengal</text><text x="620" y="315" class="ps-river-label">恒河 Ganges</text><text x="820" y="610" class="ps-region-label">孟加拉湾</text>'
 offsets=[(-90,55),(30,-35),(0,-30),(110,55),(20,-30)]
 for i,(p,(dx,dy)) in enumerate(zip(places,offsets),1):
  x,y=xy([p['lon'],p['lat']]);svg+=f'<a href="#place-{p["id"]}" aria-label="{p["name"]}：{p["type"]}"><line x1="{x}" y1="{y}" x2="{x+dx}" y2="{y+dy}" class="ps-callout"/><circle cx="{x}" cy="{y}" r="17"/><text x="{x}" y="{y+5}" class="ps-map-number">{i}</text><text x="{x+dx}" y="{y+dy-10}" text-anchor="middle" class="ps-place-label">{p["name"]}</text></a>'
 svg+='</svg>'
 b='<section class="ps-section" id="homeland"><p class="eyebrow">ALONG THE GANGES</p><h2>黑石的家乡</h2><p class="ps-prose">从比哈尔到孟加拉，圣地、寺院与地方造像传统沿恒河中下游展开。下图标出历史背景地点；美国地图记录的则是我今天看见作品的地方。</p><div class="ps-history-map" tabindex="0" aria-label="历史地图，可横向浏览">'+svg+'</div><p class="ps-caption">点击地图标记或下方地点名称，展开历史与相关作品。比哈尔与孟加拉是地域标签，不表示王朝边界。河道采用Natural Earth现代地理数据，不是古河道复原。地点坐标据UNESCO、Getty TGN及GeoNames；点击名称查看出处。<a href="../sources/#G-RIVER">底图与数据说明</a> · <a href="../atlas/#map">美国观看地图 →</a></p><nav class="ps-localnav" aria-label="历史地点">'+''.join(f'<a href="#place-{p["id"]}">{i} {p["name"]}</a>' for i,p in enumerate(places,1))+'</nav>'
 for p in places:
  b+=f'<details class="ps-notes ps-place" id="place-{p["id"]}"><summary>{p["name"]} · {p["english"]}</summary><p class="ps-caption">{p["type"]}｜{p["period"]}</p><p>'+inline(p['text']+f'[[{p["source"]}]]')+'</p><p>'+e(p['relation'])+'</p>'+grid(p['works'])+'<p class="ps-caption">'+inline('地图定位依据'+f'[[{p["coordinate_source"]}]]')+'</p></details>'
 b+='</section><section class="ps-section" id="timeline"><h2>沿年代重看</h2><p class="ps-prose">同一时期可以有简净的佛身，也有密布眷属的碑像。这里按作品年代范围的中点编排，标签保留约年和跨世纪范围；不是精确制作年份。前史单列，20件核心与2件相关作品进入主体。</p><div class="ps-map-tools" id="ps-time-filters" hidden aria-label="时间线信仰筛选"><button type="button" data-time="" aria-pressed="true">全部作品</button><button type="button" data-time="佛教" aria-pressed="false">佛教</button><button type="button" data-time="印度教" aria-pressed="false">印度教</button></div><p id="ps-time-count" class="ps-caption" aria-live="polite">24件作品</p><p class="ps-caption">向右浏览9—13世纪；作品保持完整比例，可点击进入细读。</p><div class="ps-timeline" tabindex="0" aria-label="按世纪排列的作品，横向浏览">'
 for j,p in enumerate(periods):
  ids=[]
  for w in works:
   mid=(w['date_start']+w['date_end'])/2
   idx=0 if w['group']=='earlier' else 1 if mid<800 else 2 if mid<900 else 3 if mid<1000 else 4 if mid<1100 else 5
   if idx==j:ids.append(w)
  b+=f'<section class="ps-century"><h3>{p["label"]}</h3><p class="ps-caption">{p["range"]}</p><p>'+inline(p['text']+f'[[{p["source"]}]]')+'</p>'
  for w in sorted(ids,key=lambda w:w['date_start']):b+=f'<div data-time-work="{w["id"]}" data-faith="{e(w["religion"])}">'+grid([w['id']])+'</div>'
  if not ids:b+='<p class="ps-caption">这一栏提供历史起点；现有核心作品的年代主要从9世纪展开。</p>'
  b+='</section>'
 b+='</div></section>'
 return b
