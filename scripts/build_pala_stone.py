"""Pala stone notebook. Shared works resolve from Himalayan authority; all images are Merton's."""
from pathlib import Path
from html import escape as e
import json,re,hashlib
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/pala-stone'
URL='/museum-notes/pala-stone/'
TITLE='帕拉黑石造像'
GROUPS={'core':'帕拉时期核心','related':'相关作品','earlier':'前史比较'}

def load(name):return json.loads((BASE/'data'/f'{name}.json').read_text())
def resolve():
    authority={w['work_id']:w for w in json.loads((ROOT/'museum-notes/himalayan-art/data/works.json').read_text())}
    result=[]
    for row in load('catalogue'):
        w=dict(row)
        if w.get('canonical_ref'):
            c=authority[w['canonical_ref']['work_id']]
            w.update(title=w.get('short_title') or c['title_zh'],title_en=c['title_en'],date=c['date_label'],medium=c['materials_display'],collection=c['collection_label'],viewing_museum_id=c['display_museum_id'],accession=c.get('accession'),canonical_url='/museum-notes/himalayan-art/'+c['work_id']+'/')
        result.append(w)
    return result

def build():
    works=resolve();by={w['id']:w for w in works};media=load('media');sources=load('sources');museums=load('museums');mb={m['museum_id']:m for m in museums};readings=load('readings');stories=load('stories');chapters=load('chapters')
    revision=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((BASE/'data').glob('*.json')) if p.name!='atlas-index.json')+(BASE/'pala.js').read_bytes()+(BASE/'pala.css').read_bytes()).hexdigest()[:10]
    def href(w):return URL+(w if isinstance(w,str) else w['id'])+'/'
    def image(n,alt,eager=False,small=False):
        p=media[str(n)];vs=p['variants'];sizes='(max-width:650px) 44vw, 270px' if small else '(max-width:650px) 92vw, 580px'
        return f'<img src="{vs[0 if small else 1]["url"]}" srcset="'+', '.join(f'{v["url"]} {v["width"]}w' for v in vs)+f'" sizes="{sizes}" width="{p["width"]}" height="{p["height"]}" alt="{e(alt)}" loading="'+('eager" fetchpriority="high' if eager else 'lazy')+'" decoding="async">'
    def fig(w,n=None,cap=None,eager=False):
        n=n or w['photo'];cap=cap or w['title']+' · '+w['date'];txt=cap+'｜Merton摄于'+mb[w['viewing_museum_id']]['label_zh']
        return f'<figure class="ps-figure"><a data-photo href="{media[str(n)]["original_url"]}" data-caption="{e(txt)}">{image(n,txt,eager)}</a><figcaption>{e(txt)}</figcaption></figure>'
    def card(w):
        return f'<a class="ps-card" href="{href(w)}">{image(w["photo"],w["title"]+" · "+w["date"],small=True)}<h3>{e(w["title"])}</h3><p>{e(w["date"])}</p><small>亲见：{e(mb[w["viewing_museum_id"]]["label_zh"])}</small></a>'
    def grid(ids):return '<div class="ps-grid">'+''.join(card(by[i]) for i in dict.fromkeys(ids))+'</div>'
    def source_link(k):
        s=sources[k];return media[str(s['photo'])]['original_url'] if s.get('photo') else s['url']
    def inline(text):
        def sub(m):
            k=m[1];s=sources[k];label='展签' if s.get('photo') else '资料'
            return f'<a class="ps-cite" href="{URL}sources/#{k}" aria-label="{e(s["title"])}">[{label}]</a>'
        return re.sub(r'\[\[([A-Z0-9-]+)\]\]',sub,e(text))
    def refs(keys):
        return '<details class="ps-notes"><summary>资料与来源</summary><ul>'+''.join(f'<li><a href="{e(source_link(k))}">{e(sources[k]["title"])}</a> · <a href="{URL}sources/#{k}">查阅说明</a></li>' for k in dict.fromkeys(keys))+'</ul></details>'
    def heading(t,deck=''):
        return f'<header class="ps-heading"><p class="eyebrow">PALA STONE SCULPTURE · A MUSEUM NOTEBOOK</p><h1>{e(t)}</h1>'+ (f'<p class="ps-deck">{e(deck)}</p>' if deck else '')+'</header>'
    def shell(t,b,slug='',cover=3294):
        nav=[('',TITLE),('atlas/','博物馆地图'),('stories/','神的故事'),('guide/','历史与观看'),('compare/','放在一起看')]
        canonical='https://qm2.github.io'+URL+(slug+'/' if slug else '')
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t)} | 博物馆札记 · Merton</title><meta name="description" content="从佛的一生到众神的故事，沿24件亲见石像、48张现场照片，认识东印度的帕拉艺术。"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{e(t)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{media[str(cover)]['variants'][-1]['url']}"><link rel="stylesheet" href="/museum-notes/museum.css"><link rel="stylesheet" href="/museum-notes/caravaggio/caravaggio.css"><link rel="stylesheet" href="{URL}pala.css?v={revision}"><script src="/museum-notes/caravaggio/caravaggio.js" defer></script><script src="{URL}pala.js?v={revision}" defer></script></head><body class="ps-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="/museum-notes/">Merton</a><nav aria-label="专题导航">'''+''.join(f'<a href="{URL}{u}"'+(' aria-current="page"' if u.rstrip('/')==slug else '')+f'>{n}</a>' for u,n in nav)+f'''</nav></header><main class="wrap" id="main"><nav class="breadcrumbs"><a href="/museum-notes/">博物馆札记</a><span>/</span><a href="/museum-notes/south-asian-art/">南亚艺术</a><span>/</span><a href="{URL}">{TITLE}</a></nav>{b}</main><footer class="site-footer wrap"><a href="{URL}">返回专题</a><a href="{URL}sources/">资料与来源</a><a href="/museum-notes/himalayan-art/">喜马拉雅艺术</a><a href="#top">回到顶部</a></footer>{LIGHTBOX}</body></html>'''
    def write(slug,t,b,cover=3294):
        p=BASE/slug;p.mkdir(exist_ok=True,parents=True);(p/'index.html').write_text(shell(t,b,slug,cover))
    def mapbox(compact=False):
        return '''<div class="ps-map-box" data-map-box hidden><div class="ps-map-tools" aria-label="地图范围"><button type="button" data-map="mainland" aria-pressed="true">美国本土</button><button type="button" data-map="east" aria-pressed="false">东部放大</button><button type="button" data-map="hawaii" aria-pressed="false">夏威夷</button></div><svg id="ps-map" viewBox="0 0 1000 470" role="group" aria-label="亲见博物馆分布，使用Tab键选择馆址"></svg><p class="ps-caption">地图标记实际观看的博物馆，包括借展；不是作品产地。底图：<a href="https://www.naturalearthdata.com/">Natural Earth</a>，公有领域。圆点数字为作品数；标“馆”的聚合点可点击放大。夏威夷可切换查看。</p><div id="ps-map-selection" aria-live="polite"></div></div>'''
    museum_buttons='<div class="ps-museum-buttons">'+''.join(f'<a href="{URL}atlas/?museum={m["museum_id"]}#catalogue">{e(m["city"])} · {sum(w["viewing_museum_id"]==m["museum_id"] for w in works)}件</a>' for m in museums)+'</div>'
    # Quiet opening, then a real museum map and five short narrative chapters.
    core_count=sum(w['group']=='core' for w in works);counts=f'{core_count}件核心作品 · {len(works)-core_count}件前史与相关作品 · {len(media)}张现场照片'
    hero=by['p3294'];b='<section class="ps-hero"><div>'+heading(TITLE,'佛陀、众神与东印度的故事')+'<div class="ps-prose"><p>一只指向地面的手，一头托起大地的野猪，一个跪在佛座下的人。石像看起来安静，背后却有成道、冒险、战斗，也有普通人的愿望。</p><p>这辑从博物馆里亲见的作品出发，把帕拉时期的佛教与印度教造像放在一起看：先认识身体与姿态，再走进它们的故事。</p></div><p class="ps-caption">20件核心作品 · 4件前史与相关作品 · 48张现场照片</p><nav class="ps-localnav"><a href="#chapters">从五条线索进入</a><a href="stories/">先认识众神</a></nav></div>'+fig(hero,eager=True)+'</section>'
    b+=f'<section class="ps-section" id="map"><div class="ps-section-heading"><div><p class="eyebrow">WHERE I SAW THEM</p><h2>在{len(museums)}家博物馆相遇</h2></div><a href="atlas/">完整图录与筛选 →</a></div>'+mapbox(True)+museum_buttons+'</section>'
    b+='<section id="chapters" class="ps-section"><p class="eyebrow">FIVE WAYS OF LOOKING</p><h2>从一个动作，走进一个故事</h2>'
    chapter_copy={
      'life':'同样是坐在莲座上的佛，有时正在成道，有时正在说法。手势和身边的小人物，把一生中的不同片刻分开；一块八大事迹碑，又能把这些片刻聚在一起。',
      'compassion':'观音的名字与听见求救、回应苦难相连。看莲花、伸出的手，也看脚边的众生。与他并看的文殊，则把观看引向智慧：姿态相近，职责并不相同。',
      'vishnu':'毗湿奴维持世界的秩序，也会以不同化身来到危机之中。野猪救起大地，迦楼罗承载主神；一块布满小像的背屏，便是一串等待辨认的故事。',
      'power':'难近母把众神的力量集中在一场战斗里，象头神则走进婚姻、旅途与新的开始。一位踏住水牛，一位挺着圆肚，两种截然不同的身体，都回应着人们寻求保护的心愿。',
      'people':'有的石像保留供养人的名字，有的留下石匠的署名。把目光从佛脸移向台座，便能遇见制作、赠献和礼拜的人；戴冠佛首的近代经历，则把另一段历史带到眼前。'}
    for i,ch in enumerate(chapters):
        w=by[ch['cover']];b+=f'<article class="ps-chapter" id="{ch["id"]}"><div class="ps-feature">'+fig(w)+f'<div class="ps-prose"><p class="eyebrow">0{i+1}</p><h2>{e(ch["title"])}</h2><p>{e(chapter_copy[ch["id"]])}</p><p><a href="{href(w)}">细看：{e(w["title"])} →</a></p></div></div>'+grid([k for k in ch['works'] if k!=ch['cover']])+'</article>'
    b+='</section><section class="ps-section ps-paths"><div><h2>这些石像的家乡</h2><p>比哈尔、孟加拉、那烂陀：把展签上的地名放回寺院、神庙与旅行者的世界。</p><a href="guide/">历史与观看 →</a></div><div><h2>换一件，继续看</h2><p>比较降魔的手势、迦楼罗的身体，以及供养人与石匠留下的名字。</p><a href="compare/">四组并看 →</a></div></section>'
    write('',TITLE,b)
    # One thematic page per canonical work, no duplicate object identity.
    for i,w in enumerate(works):
        r=readings[w['id']];b=heading(w['title'],w['title_en'])+f'<p class="ps-meta">{e(w["date"])} · {e(w["region"])}</p><div class="ps-full">'+fig(w,eager=True)+'</div><article class="ps-prose"><p class="ps-lead">'+inline(r['lead'])+'</p>'
        for section in r['sections']:
            b+='<section><h2>'+e(section['title'])+'</h2>'+''.join('<p>'+inline(p)+'</p>' for p in section['paragraphs'])+'</section>'
        b+='<p class="ps-memory">再看时记住：'+e(r['remember'])+'</p></article>'
        linked=[s for s in stories if w['id'] in s['works']]
        if linked:b+='<aside class="ps-prose ps-story-links"><p>认识这个故事：'+' · '.join(f'<a href="{URL}stories/#{s["id"]}">{e(s["title"])}</a>' for s in linked)+'</p></aside>'
        fields=[('年代',w['date']),('地域',w['region']),('材料',w['medium']),('收藏',w['collection']),('馆藏号',w.get('accession') or '未公布／待核'),('亲见地点',mb[w['viewing_museum_id']]['label_zh'])]
        if w.get('dimensions'):fields.append(('尺寸',w['dimensions']))
        if w.get('viewing_context') or w['id']=='w1476':fields.append(('观看场合',w.get('viewing_context','Living with the Gods')))
        b+='<details id="record" class="ps-notes"><summary>作品资料与现场展签</summary><dl class="ps-facts">'+''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k,v in fields)+'</dl>'
        if w.get('notes'):b+=''.join('<p class="ps-caption">'+e(n)+'</p>' for n in w['notes'])
        b+=fig(w,w['label'],'现场展签')+'</details>'
        keys=w['source_ids']+re.findall(r'\[\[([A-Z0-9-]+)\]\]',json.dumps(r,ensure_ascii=False));b+=refs(keys)
        if w.get('canonical_url'):b+='<p class="ps-prose ps-caption">同一件作品也收在<a href="'+w['canonical_url']+'">喜马拉雅艺术作品档案</a>；这里从新照片继续看东印度的故事。</p>'
        b+='<section class="ps-section"><h2>放在一起看</h2>'+grid(r['related'])+'</section><nav class="ps-sequence" aria-label="前后作品">'
        if i:b+=f'<a href="{href(works[i-1])}">← {e(works[i-1]["title"])}</a>'
        b+=f'<a href="{URL}atlas/?museum={w["viewing_museum_id"]}#catalogue">回到观看馆</a>'
        if i<len(works)-1:b+=f'<a href="{href(works[i+1])}">{e(works[i+1]["title"])} →</a>'
        b+='</nav>';write(w['id'],w['title'],b,w['photo'])
    # Stories for re-reading, with recognizable examples rather than a generic encyclopedia.
    b=heading('神的故事','先读一句，再回到石像')+'<nav class="ps-localnav" aria-label="故事目录">'+''.join(f'<a href="#{s["id"]}">{e(s["name"].split(" · ")[0])}</a>' for s in stories)+'</nav>'
    for s in stories:
        b+=f'<section class="ps-section" id="{s["id"]}"><div class="ps-feature">'+fig(by[s['works'][0]])+'<div class="ps-prose"><h2>'+e(s['title'])+'</h2><p class="ps-caption">'+e(s['name'])+'</p><p class="ps-memory">'+e(s['memory'])+'</p><p>'+e(s['text'])+'</p><p>'+e(s['look'])+'</p>'+refs(s['sources'])+'</div></div>'+grid(s['works'][1:])+f'<p><a href="{href(s["works"][0])}">细看这件作品 →</a></p></section>'
    write('stories','神的故事',b,3280)
    raw=(BASE/'content/guide.md').read_text();b=heading('历史与观看','比哈尔、孟加拉与帕拉时期的众神')+'<article class="ps-prose">'
    for paragraph in raw.split('\n\n'):
        if paragraph.startswith('# '):continue
        if paragraph.startswith('## '):b+='<h2>'+e(paragraph[3:])+'</h2>'
        else:b+='<p>'+inline(paragraph.strip())+'</p>'
    b+='</article><section class="ps-section"><h2>带着这些问题回到作品</h2>'+grid(['p3266','p3308','p3296','p3306'])+'</section><p class="ps-prose"><a href="/museum-notes/himalayan-art/regions/#east-india">继续读：东印度与喜马拉雅艺术</a></p>'+refs(re.findall(r'\[\[([A-Z0-9-]+)\]\]',raw))
    write('guide','历史与观看',b,3308)
    pairs=[('life','一生怎样放进一块石头',['p3266','sama-08'],'先找中央触地印佛，再从两侧的小龛辨认出生、说法等时刻。两件都围绕成道组织佛传，但周边场景的空间和主像比例并不完全相同。','L3267'),('garuda','迦楼罗：从坐骑到独立的守护形象',['p3288','p3296','p3310'],'克利夫兰的早期像以扇形尾羽托住毗湿奴；华盛顿像单独跪坐合掌；沃尔特斯像又把主神、两位女神和坐骑组织成一座小小的神龛。留意头、翼与腿，不只看“是不是鸟”。','O3288'),('buddha','同一只触地的手，不同的身体',['w1488','w1579','w1649'],'三件都以右手触地、左掌置于腹前表现成道。比较肩胸的宽度、两膝形成的横线，以及背光和小像占去多少空间；这些差别使同一故事各有面貌。','O3286'),('names','是谁把这件像留了下来',['p3308','w1508'],'沃尔特斯小碑留下供养人Pingalāyana，大都会说法佛留下石匠Vijaka。一个名字连接赠献，一个连接制作；再看台座，佛像周围的小人和文字便有了分量。','O3308')]
    b=heading('放在一起看','同一动作、不同身体；同一信仰、不同的参与者')+'<p class="ps-caption">照片按阅读需要缩放，不表示实物等大。点击可放大现场全图。</p><nav class="ps-localnav">'+''.join(f'<a href="#{pid}">{e(t)}</a>' for pid,t,_,_,_ in pairs)+'</nav>'
    for pid,t,ids,text,key in pairs:
        b+=f'<section id="{pid}" class="ps-section"><h2>{e(t)}</h2><div class="ps-comparison">'+''.join('<div>'+fig(by[i])+f'<p><a href="{href(i)}">{e(by[i]["title"])} · 进入细读</a></p></div>' for i in ids)+'</div><p class="ps-prose">'+inline(text+f'[[{key}]]')+'</p></section>'
    write('compare','放在一起看',b,3288)
    # Atlas: accessible static catalogue first, map and linked filters enhance it.
    b=heading('所见地图与图录',f'{len(works)}件作品 · {len(museums)}家观看博物馆 · {len(media)}张现场照片')+'<p class="ps-prose">地图留下看见它们的地方。四件休斯顿借展作品的收藏方另列在作品资料中；两件更早的造像与两件相关作品，也保留各自的年代和归属。</p>'
    b+='<form id="ps-filters" class="ps-filters" hidden><label>名称、神祇、馆藏号<input id="ps-search" type="search" placeholder="例如：毗湿奴、25.263"></label><label>观看馆<select id="ps-museum"><option value="">全部博物馆</option>'+''.join(f'<option value="{m["museum_id"]}">{e(m["label_zh"])}</option>' for m in museums)+'</select></label><label>信仰<select id="ps-religion"><option value="">全部</option><option>佛教</option><option>印度教</option></select></label><label>范围<select id="ps-group"><option value="">全部作品</option>'+''.join(f'<option value="{k}">{v}</option>' for k,v in GROUPS.items())+'</select></label><label>排列<select id="ps-sort"><option value="catalogue">图录顺序</option><option value="date">年代由早至晚</option><option value="museum">观看博物馆</option></select></label><button type="reset">清除条件</button></form><p id="ps-result-count" aria-live="polite">全部'+str(len(works))+'件</p><section id="map" class="ps-section"><h2>博物馆分布</h2>'+mapbox()+museum_buttons+'</section><section id="catalogue" class="ps-section"><h2>完整图录</h2><p id="ps-empty" hidden>没有符合条件的作品，可以减少条件或清除筛选。</p><div class="ps-grid ps-catalogue">'
    for w in works:b+=f'<article id="{w["id"]}" data-record-id="{w["id"]}">'+card(w)+f'<p class="ps-caption">{e(GROUPS[w["group"]])} · {e(w["religion"])}<br>{e(w["accession"] or "馆藏号待核")}</p></article>'
    b+='</div></section>';write('atlas','所见地图与图录',b)
    public=[{k:w.get(k) for k in ['id','title','title_en','date','date_start','date_end','medium','collection','viewing_museum_id','accession','group','religion']}|{'url':href(w),'image':media[str(w['photo'])]['variants'][0]['url'],'search':' '.join(str(w.get(k) or '') for k in ['title','title_en','date','region','medium','collection','accession'])+' '+mb[w['viewing_museum_id']]['label_zh']} for w in works]
    (BASE/'data/atlas-index.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
    b=heading('资料与来源','作品与展签摄影：Merton')+'<div class="ps-prose"><p>作品基本资料来自现场展签与馆方记录；神话采用各条注明的版本。照片只使用本人的现场摄影，原图可在作品页放大。下列查阅记录说明本次实际使用的内容。</p></div>'
    for k,s in sources.items():b+=f'<details id="{k}" class="ps-notes"><summary>{e(s["title"])}</summary><p><a href="{e(source_link(k))}">打开原始资料</a></p><p>{e(s["read_status"])}</p><p>{e(s["used_for"])}</p><p class="ps-caption">核对日期：{e(s["checked_on"])}</p></details>'
    write('sources','资料与来源',b)
    # Stable parent entrances, regenerated after parent builders.
    p=ROOT/'museum-notes/south-asian-art/index.html';s=p.read_text();s=re.sub(r'<!-- pala-stone -->.*?<!-- /pala-stone -->','',s,flags=re.S)
    entry='<section><a class="issue-link" href="../pala-stone/">'+image(3294,'毗湿奴与诸化身',small=True)+'<div><p class="eyebrow">STONE · BUDDHIST & HINDU ART</p><h2>帕拉黑石造像</h2><p>从佛的一生到众神的故事，沿'+str(len(works))+'件亲见石像，认识东印度的寺院、神庙与供养者。</p><p>'+str(len(chapters))+'条阅读线索 · '+str(len(museums))+'家博物馆 · 地图与完整图录</p><span class="text-link">进入专题 →</span></div></a></section>'
    s=s.replace('</main>','<!-- pala-stone -->'+entry+'<!-- /pala-stone --></main>');p.write_text(s)
    p=ROOT/'museum-notes/index.html';s=p.read_text();s=re.sub(r'<!-- pala-stone-home -->.*?<!-- /pala-stone-home -->','',s,flags=re.S);s=s.replace('<!-- /khajuraho-home -->','<!-- /khajuraho-home --><!-- pala-stone-home --><p class="featured-note"><a href="pala-stone/">新辑：帕拉黑石造像｜佛陀、众神与东印度的故事</a></p><!-- /pala-stone-home -->');p.write_text(s)
    print(f'Pala stone: {len(works)} works, {len(media)} photographs, {len(museums)} viewing museums; {sum(bool(w.get("canonical_ref")) for w in works)} shared authority records.')
if __name__=='__main__':build()
