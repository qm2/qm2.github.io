"""Build a focused court-art study from canonical Himalayan object/photo records."""
from pathlib import Path
from html import escape as e
import json, hashlib, re
from build_homer import LIGHTBOX

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'museum-notes/yongle-xuande'
SHARED=ROOT/'museum-notes/himalayan-art'

def build(integrate=True):
    read=lambda p:json.loads(p.read_text())
    d=read(BASE/'data/topic.json')
    works={w['work_id']:w for w in read(SHARED/'data/works.json')}
    photos=read(SHARED/'data/derivatives.json')
    sources={s['source_id']:s for s in read(SHARED/'data/sources.json')}
    museums={m['museum_id']:m for m in read(SHARED/'data/museums.json')}
    aliases=read(SHARED/'data/work_aliases.json')
    visits=read(SHARED/'data/visits.json')
    photo_visits={n:v for v in visits for n in v.get('photo_ids',[])}
    def viewing(v):
        mid=v.get('display_museum_id')
        if not mid:return ''
        when=v.get('visited_month')
        date_label=(when[:4]+'年'+str(int(when[5:]))+'月 · ') if when else ''
        return date_label+museums[mid]['label_zh']
    used=[]
    def cite(ids):
        for k in ids:
            assert k in sources
            if k not in used:used.append(k)
        return ' '.join(f'<a class="yx-ref" href="#source-{k}" aria-label="来源：{e(sources[k]["title"])}">[{used.index(k)+1}]</a>' for k in dict.fromkeys(ids))
    def paras(ps):return ''.join('<p>'+e(p['text'])+' '+cite(p.get('source_ids',[]))+'</p>' for p in ps)
    def sections(ss):return ''.join('<section><h3>'+e(s['title'])+'</h3>'+paras(s['paragraphs'])+'</section>' for s in ss)
    def img(n,alt,high=False,small=False):
        p=photos[n];variants={v['width']:v for v in p['variants']}
        srcset=', '.join('../himalayan-art/'+v['path']+' '+str(w)+'w' for w,v in variants.items())
        size='(max-width:650px) 42vw, 260px' if small else '(max-width:850px) calc(100vw - 40px), 570px'
        return '<img src="../himalayan-art/'+p['variants'][0 if small else 1]['path']+'" srcset="'+srcset+'" sizes="'+size+'" width="'+str(p['width'])+'" height="'+str(p['height'])+'" alt="'+e(alt)+'" decoding="async" '+('fetchpriority="high"' if high else 'loading="lazy"')+'>'
    def figure(n,cap,high=False,small=False):
        p=photos[n]
        return '<figure class="yx-figure" style="--ratio:'+str(p['width']/p['height'])+';--native:'+str(p['width'])+'px"><a data-photo href="../himalayan-art/'+p['original']+'" data-caption="'+e(cap)+'">'+img(n,cap,high,small)+'</a><figcaption>'+e(cap)+' · <span class="yx-credit">Merton摄</span></figcaption></figure>'
    def owner(w):return w['collection_label']
    def caption(w):
        cap=w['title_zh']+' · '+w['date_label']+'｜'+owner(w)+' · '+w['accession']
        v=photo_visits.get(w['primary_photo'])
        return cap+('｜'+viewing(v)+'所见' if v and viewing(v) else '')
    def facts(w):
        location=museums[w['display_museum_id']]['label_zh'] if w.get('display_museum_id') else '两组展陈照片；实际观看地点未完全核实'
        contexts=[viewing(v) for v in visits if v['work_id']==w['work_id'] and viewing(v)]
        if contexts:location='；'.join(dict.fromkeys(contexts))
        origin=w.get('origin_display','中国；宫廷制作背景')
        if w['work_id']=='w1516':origin='中国；北京为馆方列出的可能制作地'
        rows=[('原题名',w['title_en']),('年代',w['date_label']),('材质',w['materials_display']),('尺寸',w.get('dimensions_display')),('收藏机构',owner(w)),('馆藏号',w['accession']),('实际观看',location),('制作地域',origin)]
        out='<details class="yx-record"><summary>作品资料与现场记录</summary><dl>'+''.join('<dt>'+e(k)+'</dt><dd>'+e(v)+'</dd>' for k,v in rows if v)+'</dl>'+cite(w['source_ids'])
        out+=''.join('<p class="yx-note">'+e(x)+'</p>' for x in w['reader_notes'])
        out+='<p><a href="../himalayan-art/'+w['work_id']+'/">完整作品记录 →</a>'
        if w.get('himalayan_default_inclusion',True):out+=' · <a href="../himalayan-art/?work='+w['work_id']+'#places">地区与观看地图 →</a>'
        return out+'</p></details>'
    core=d['core'];selected=core+[d['comparison']]+d['ritual']
    ids=[s['work_id'] for s in selected];assert len(set(ids))==len(ids)
    physical=sum(works[k].get('physical_object_count',1) for k in ids)
    hero=works[d['hero_work_id']]
    body='<nav class="breadcrumbs"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>／</span><a href="../himalayan-art/">喜马拉雅艺术</a></nav>'
    body+='<header class="yx-cover"><div><p class="eyebrow">YONGLE &amp; XUANDE</p><h1>'+e(d['title'])+'</h1><p class="yx-subtitle">'+e(d['subtitle'])+'</p><p class="yx-intro">'+e(d['intro'])+'</p><p class="yx-note">'+str(len(core))+'尊核心造像 · 1件瑞像对照 · '+str(sum(works[s['work_id']].get('physical_object_count',1) for s in d['ritual']))+'件仪式器物</p><nav class="yx-local" aria-label="专题阅读"><a href="#works">从造像看起 ↓</a><a href="#court">宫廷与供养</a><a href="#comparison">同一时期的另一种选择</a><a href="#ritual">仪式器物</a></nav></div>'+figure(d['hero_photo'],caption(hero),high=True)+'</header>'
    body+='<section class="yx-prose yx-background" id="court"><p class="eyebrow">COURT / OFFERING / MAKING</p><h2>金色之下，不同的供养</h2>'+paras(d['background'])+'<p class="yx-note"><a href="../himalayan-art/history/#tibet-networks">回到寺院与供养网络的历史 →</a></p></section>'
    body+='<section id="works" class="yx-core"><header class="yx-section-head"><h2>四种神圣的形体</h2><nav class="yx-local" aria-label="四件作品">'+''.join('<a href="#'+s['work_id']+'">'+e(s['heading'].split('：')[0])+'</a>' for s in core)+'</nav></header>'
    for i,s in enumerate(core):
        w=works[s['work_id']]
        body+='<article class="yx-work" id="'+w['work_id']+'"><div class="yx-work-opening">'+figure(s['photo'],caption(w))+'<div><p class="eyebrow">'+f'{i+1:02d}'+' / CLOSE LOOKING</p><h2>'+e(s['heading'])+'</h2><p class="yx-lead">'+e(s['lead'])+'</p><ol class="yx-looking">'+''.join('<li>'+e(t)+'</li>' for t in s['look_for'])+'</ol><p class="yx-remember">'+e(s['remember'])+'</p></div></div>'
        body+='<div class="yx-prose">'+sections(s['sections'])+'</div>'
        for detail in s.get('detail_photos',[]):body+='<div class="yx-detail">'+figure(detail['photo_id'],detail['caption'])+'</div>'
        body+='<div class="yx-prose">'+facts(w)+'<details class="yx-evidence"><summary>研究与资料注</summary>'+sections(s['notes'])+'</details></div></article>'
    body+='</section><section class="yx-section" id="together"><header class="yx-section-head"><h2>放在一起看</h2></header><div class="yx-compare compare-group">'
    for s in core:
        w=works[s['work_id']];body+='<article>'+figure(s['photo'],w['title_zh']+'｜'+owner(w),small=True)+'<p class="yx-note">'+e(w['dimensions_display'])+'</p><a href="#'+w['work_id']+'">回到作品 ↑</a></article>'
    body+='</div><div class="yx-prose"><p>'+e(d['comparison_summary'])+'</p><p class="yx-note">图片保留各自比例，并非实物等比例比较。尺寸及测量范围见各件资料。</p></div></section>'
    s=d['comparison'];w=works[s['work_id']]
    body+='<section class="yx-section" id="comparison"><article id="'+w['work_id']+'"><header class="yx-section-head"><p class="eyebrow">ANOTHER IMAGE TRADITION</p><h2>'+e(s['heading'])+'</h2></header><div class="yx-work-opening">'+figure(s['photo'],caption(w))+'<div class="yx-comparison-prose"><p class="yx-lead">'+e(s['lead'])+'</p>'+paras(s['paragraphs'])+facts(w)+'</div></div><details class="yx-alternate"><summary>另一次观看 · 同一件作品</summary>'+figure(s['alternate_photo']['photo_id'],s['alternate_photo']['caption'])+'</details><details class="yx-evidence yx-prose"><summary>照片对应与资料注</summary>'+sections(s['notes'])+'</details></article></section>'
    body+='<section class="yx-section" id="ritual"><header class="yx-section-head"><p class="eyebrow">RITUAL OBJECTS</p><h2>斧、钺刀与香炉</h2><p class="yx-prose">'+e(d['ritual_intro'])+'</p></header>'
    for s in d['ritual']:
        w=works[s['work_id']];body+='<article class="yx-work" id="'+w['work_id']+'"><h3>'+e(s['heading'])+'</h3><div class="yx-work-opening">'+figure(s['photo'],caption(w))+'<div class="yx-comparison-prose">'+sections(s['sections'])+facts(w)+'</div></div></article>'
    body+='</section><aside class="yx-onward yx-prose"><h2>继续连回看过的作品</h2><p><a href="../himalayan-art/#topic-studies">喜马拉雅艺术 · 专题深读 →</a><br><a href="../densatil/">丹萨替寺造像 · 塔上的尊神与构件 →</a><br><a href="../chinese-buddhist-art/">中国佛教艺术 · 从材料与寺院进入 →</a></p></aside>'
    body+='<details class="yx-evidence yx-prose" id="open-questions"><summary>仍待追问的几件事</summary><ul>'+''.join('<li>'+e(x)+'</li>' for x in d['research_limits'])+'</ul></details>'
    body+='<section class="yx-sources" id="sources"><h2>资料与来源</h2><p class="yx-note">现场摄影与札记：Merton。作品资料据现场展签及下列馆方与研究记录整理。</p><ol>'
    for k in used:body+='<li id="source-'+k+'"><a href="'+e(sources[k]['url'])+'">'+e(sources[k]['title'])+' ↗</a></li>'
    body+='</ol></section>'
    rev=hashlib.sha256((BASE/'yongle-xuande.css').read_bytes()+(BASE/'yongle-xuande.js').read_bytes()).hexdigest()[:12]
    html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(d['title'])+' · 博物馆札记 | Merton</title><meta name="description" content="'+e(d['intro'])+'"><link rel="canonical" href="https://qm2.github.io/museum-notes/yongle-xuande/"><meta property="og:image" content="https://qm2.github.io/museum-notes/himalayan-art/images/'+d['hero_photo']+'-900.webp"><link rel="stylesheet" href="../museum.css"><link rel="stylesheet" href="../caravaggio/caravaggio.css"><link rel="stylesheet" href="yongle-xuande.css?v='+rev+'"><script defer src="../caravaggio/caravaggio.js"></script><script defer src="yongle-xuande.js?v='+rev+'"></script></head><body class="yx-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="../">Merton</a><nav aria-label="主导航"><a href="../chinese-buddhist-art/">中国佛教艺术</a><a href="../himalayan-art/">喜马拉雅艺术</a><a href="#works">看作品</a></nav></header><main class="wrap" id="main">'+body+'</main><footer class="site-footer wrap"><a href="../">← 博物馆札记</a><span>现场摄影与札记 / Merton</span><a href="#top">回到顶部 ↑</a></footer>'+LIGHTBOX+'</body></html>'
    (BASE/'index.html').write_text(html)
    # Cross-topic work aliases lead to one canonical record, not another object.
    for wid in ids+list(aliases):
        target=aliases.get(wid,wid);dest=BASE/wid;dest.mkdir(exist_ok=True)
        (dest/'index.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=../#'+target+'"><title>'+e(works[target]['title_zh'])+'</title><link rel="canonical" href="https://qm2.github.io/museum-notes/yongle-xuande/#'+target+'"><p><a href="../#'+target+'">阅读这件作品 →</a></p></html>')
    if integrate:
        parent=ROOT/'museum-notes/chinese-buddhist-art/index.html';text=parent.read_text()
        text=re.sub(r'<!-- yongle-entry -->.*?<!-- /yongle-entry -->','',text,flags=re.S)
        card='<!-- yongle-entry --><a class="issue-link" href="../yongle-xuande/"><img src="../himalayan-art/images/h1657-900.webp" width="1280" height="1707" alt="西雅图宣德赐款观音，完整莲座与垂足" loading="lazy" style="object-fit:contain"><div><p class="eyebrow">007 / YONGLE &amp; XUANDE</p><h2>永宣宫廷造像</h2><p>从四种神圣形体，细看宫廷供养、赠献款识与不同的制作历史。</p><p class="issue-meta">'+str(len(core))+'尊核心造像 · 1件瑞像对照 · '+str(physical-len(core)-1)+'件仪式器物</p><span class="text-link">走进这一辑 →</span></div></a><!-- /yongle-entry -->'
        anchor='</section><section class="material-directory"';assert anchor in text;text=text.replace(anchor,card+anchor,1)
        count=len(re.findall(r'<a class="issue-link"',text.split(anchor)[0]))
        text=re.sub(r'造像 · [一二三四五六七八九十\d]+个专题','造像 · '+str(count)+'个专题',text);parent.write_text(text)
        home=ROOT/'museum-notes/index.html';text=home.read_text()
        text=re.sub(r'<!-- yongle-home -->.*?<!-- /yongle-home -->','',text,flags=re.S)
        anchor='<a class="issue-link" href="chinese-painting/">';assert anchor in text
        text=text.replace(anchor,'<!-- yongle-home --><p class="topic-return"><a href="yongle-xuande/">永宣宫廷造像：供养、工艺与不同的神圣形体 →</a></p><!-- /yongle-home -->'+anchor,1)
        text=re.sub(r'\d+ 个造像专题 ·',str(count)+' 个造像专题 ·',text);home.write_text(text)
    print(f'Yongle–Xuande: {len(core)} core, 1 comparison, {physical-len(core)-1} ritual objects; {len(ids)} canonical records, {physical} physical objects; shared photos only.')

if __name__=='__main__':build()
