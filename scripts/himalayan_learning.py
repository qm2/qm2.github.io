"""Data-driven reading paths, reciprocal links and a local, alias-aware index.

Only use the parent build's canonical works, photo renderer and citations.
No network, third-party image assets or duplicated object records.
"""
from html import escape as e
import json

PATHS=[('history','地域与历史','山谷、时期与交流'),('iconography','认识形象','持物、姿态与组合'),('teachers','上师与传承','人物、寺院与供养'),('review','看展前重温','五分钟与名称查找')]

def navigation(current='', prefix='../'):
    return '<nav class="ha-learning-nav" aria-label="历史与观看阅读入口">'+''.join(f'<a href="{prefix}{route}/"'+(' aria-current="page"' if current==route or current=='regions' and route=='history' else '')+f'><strong>{label}</strong><small>{desc}</small></a>' for route,label,desc in PATHS)+'</nav>'

def all_entries(data):
    return [(p['route'],n) for p in data['pages'] for n in p['entries']]+[('teachers',n) for n in data['traditions']]

def backlinks(data, wid):
    related=[(route,n) for route,n in all_entries(data) if any(r['work_id']==wid for r in n['related'])]
    if not related:return ''
    return '<aside class="ha-history-return ha-prose"><p class="ha-note">从这件作品继续学习</p><ul class="ha-learning-backlinks">'+''.join(f'<li><a href="../{route}/#{n["id"]}">{e(n["title"])}</a></li>' for route,n in related)+'</ul></aside>'

def build_learning(data, history, by, sources, img, fig, mini, paragraphs, refs, write, gallery):
    entries=all_entries(data)
    assert len({(r,n['id']) for r,n in entries})==len(entries)
    def source_ids(value):
        if isinstance(value,dict):
            for k,v in value.items():
                if k=='source_ids':yield from v
                else:yield from source_ids(v)
        elif isinstance(value,list):
            for v in value:yield from source_ids(v)
    for route,n in entries:
        assert all(r['work_id'] in by for r in n['related'])
        assert set(source_ids(n))<=sources.keys()
        assert not n.get('photo_work_id') or n['photo_work_id'] in by
    def links(items):
        return '<nav class="ha-guide-links" aria-label="继续阅读">'+''.join(f'<a href="{e(x["href"])}">{e(x["label"])} →</a>' for x in items)+'</nav>' if items else ''
    def top(title,subtitle,route):
        return '<nav class="breadcrumbs"><a href="../">喜马拉雅艺术</a><span>/</span><a href="../history/">历史与观看</a></nav><header class="ha-heading"><p class="eyebrow">HISTORY &amp; LOOKING</p><h1>'+e(title)+'</h1><p>'+e(subtitle)+'</p></header>'+navigation(route)
    def search_form():
        return '<form class="ha-guide-search" action="../review/" method="get" role="search"><label for="learning-query">找一个名字或线索</label><div><input id="learning-query" name="q" type="search" placeholder="例如：金刚杵、Jeung…" autocomplete="off"><button type="submit">查找</button><button type="button" id="learning-clear" hidden>清除</button></div><p class="ha-note">可搜索中文、英文异名、持物、人物与寺院，例如 Vajrasattva、俄尔、谷穗。</p></form>'.replace('例如：金刚杵、Jeung…','例如：金刚杵、俄尔、Tara')
    def entry(n,route,ids,opened=False):
        wid=n.get('photo_work_id')
        if not wid and route in {'regions','iconography'} and n['related']:wid=n['related'][0]['work_id']
        photo=by[wid] if wid else None
        out=f'<details class="ha-guide-entry" id="{n["id"]}"'+(' open' if opened else '')+'><summary>'
        if photo:out+='<span class="ha-guide-thumb">'+img(photo['primary_photo'],n.get('photo_note') or photo['image_alt_zh'],'../',small=True)+'</span>'
        out+='<span class="ha-guide-heading"><strong>'+e(n['title'])+'</strong><span>'+e(n['summary'])+'</span></span></summary><div class="ha-guide-body"><p class="ha-remember">'+e(n['remember'])+'</p>'
        if n.get('display_names'):out+='<p class="ha-guide-names ha-note">'+e(n['display_names'])+'</p>'
        if n.get('photo_note'):out+='<p class="ha-note">'+e(n['photo_note'])+'</p>'
        if route=='thangka' and photo:
            out+=fig(photo['primary_photo'],photo['title_zh']+' · '+photo['collection_label'],'../')
            if n['id']=='mandala':out+=fig('h1693','《金刚鬘四曼荼罗》右上区域 · 现场局部照片','../')
        for section in n['sections']:
            out+='<section class="ha-prose"><h3>'+e(section['title'])+'</h3>'+paragraphs(section['paragraphs'],ids)+'</section>'
        if n['clues']:
            out+='<section class="ha-prose"><h3>在照片上找</h3><ul class="ha-clues">'
            for clue in n['clues']:out+='<li>'+paragraphs([clue],ids)+'</li>'
            out+='</ul></section>'
        if n['related']:
            out+='<section class="ha-guide-related"><h3>回到亲见作品</h3><div class="ha-history-works">'
            for r in n['related']:out+='<div>'+mini(by[r['work_id']])+'<p class="ha-note">'+e(r['relation'])+'</p></div>'
            out+='</div></section>'
        return out+links(n['links'])+'</div></details>'
    for page in data['pages']:
        route=page['route'];ids=[]
        body=top(page['title'],page['subtitle'],route)+'<p class="ha-prose ha-reading-lead">'+e(page['intro'])+'</p>'
        if route=='regions':
            body+=links([{'href':'../history/#tibet','label':'西藏时间线'},{'href':'../history/#nepal','label':'尼泊尔时间线'},{'href':'../#places','label':'打开互动地域地图'}])
        if route=='iconography':
            body+='<div class="ha-prose ha-note">'+paragraphs([{'text':'“本尊”（yidam）是修持中所观修的尊神；“护法”强调守护教法的角色，同一形象可能兼具两者。忿怒是一种表现方式，并非邪恶的标记。','source_ids':['S27','S83']}],ids)+'</div>'
            body+=links([{'href':'../thangka/','label':'怎样看一幅唐卡'},{'href':'../review/','label':'按异名或持物查找'}])
        if route=='teachers':
            body+='<section id="traditions"><h2>先认清几条传统</h2><p class="ha-prose">宁玛、噶举、萨迦、格鲁在不同地方并存，各有内部支系。它们不是依次更替的朝代，帽色也不能替代人物题名与传承记录。</p>'
            body+=''.join(entry(n,'traditions',ids) for n in data['traditions'])+'</section><h2>八个人物，从作品进入</h2>'
        body+='<nav class="ha-entry-index" aria-label="本页条目">'+''.join(f'<a href="#{n["id"]}">{e(n["title"].split("：")[0])}</a>' for n in page['entries'])+'</nav>'
        body+=''.join(entry(n,route,ids,route=='thangka' and i==0) for i,n in enumerate(page['entries']))
        body+='<p class="ha-prose"><a href="../review/">带着问题查阅：名称、持物与寺院 →</a></p>'+refs(ids)
        write(route,page['title'],body,by[next((n['photo_work_id'] for n in page['entries'] if n.get('photo_work_id')),'w1692')]['primary_photo'])
    # One search index is derived from the same entries and existing timelines.
    # Static markup keeps the full index useful even when scripting is disabled.
    index=[]
    def add(route,n,label):
        names=[n['title'].split('：')[0]]+n.get('aliases',[])
        features=n.get('recognition_terms',[])+[p['text'] for p in n.get('clues',[])]
        texts=[n['title'],n.get('display_names',''),n.get('summary',''),n.get('remember','')]+n.get('keywords',[])
        for section in n.get('sections',[]):texts += [section['title']]+[p['text'] for p in section['paragraphs']]
        for r in n['related']:
            w=by[r['work_id']];texts += [w['title_zh'],w['title_en'],w.get('accession',''),r['relation']]
        index.append({'href':f'../{route}/#{n["id"]}','title':n['title'],'summary':n.get('summary',''),'label':label,'search':[names,features,[t for t in texts if t]],'wid':n.get('photo_work_id') or (n['related'][0]['work_id'] if n['related'] and route not in {'teachers'} else None)})
    labels={'regions':'地域','iconography':'形象','teachers':'人物与传承','thangka':'读唐卡'}
    for route,n in entries:add(route,n,labels[route])
    for track in history['tracks']:
        for n in track['nodes']:
            add('history',{'id':n['id'],'title':n['title'],'summary':n['summary'],'keywords':[n['period']]+n['keywords'],'related':n['related'],'sections':[{'title':track['title'],'paragraphs':n['paragraphs']+n['review']['points']}]},'时期')
    body=top('看展前重温','五分钟，然后带着一个问题回到作品','review')+search_form()
    body+=f'<details id="learning-index"><summary>名称与线索索引 · {len(index)}条</summary><p id="learning-count" role="status" aria-live="polite">{len(index)}条</p><div class="ha-search-results">'
    for item in index:
        body+='<article class="ha-search-item" data-learning-search="'+e(json.dumps(item['search'],ensure_ascii=False))+'"><a href="'+e(item['href'])+'">'
        if item['wid']:
            w=by[item['wid']];body+=img(w['primary_photo'],w['image_alt_zh'],'../',small=True)
        body+='<span><small>'+e(item['label'])+'</small><strong>'+e(item['title'])+'</strong><span>'+e(item['summary'])+'</span><small class="ha-search-reason" hidden></small></span></a></article>'
    body+='</div><p id="learning-empty" hidden>没有找到相符条目。可试试更短的名称，或使用展签上的英文。</p></details><section class="ha-five-minutes"><h2>带着这五个问题看展</h2>'
    for i,n in enumerate(data['review']):
        body+='<article><h3>'+e(n['title'])+'</h3><p>'+e(n['text'])+'</p>'+links(n['links'])+'</article>'
    prompt=data['revisit_prompt']
    body+='</section><details class="ha-prose ha-revisit-prompt" id="revisit-prompt"><summary>'+e(prompt['title'])+'</summary><p>'+e(prompt['intro'])+'</p>'
    for field in prompt['fields']:body+='<h3>'+e(field['label'])+'</h3><p>'+e(field['hint'])+'</p>'
    body+='<p><a href="../#catalogue">从目录找到这件作品 →</a></p></details><p class="ha-prose ha-note">每条说明的来源、作品和具体疑点，随链接保留在详细条目中。重访仍沿用原作品编号；新增照片与观察会继续接回这些入口。</p>'
    write('review','看展前重温',body,'h1552')
