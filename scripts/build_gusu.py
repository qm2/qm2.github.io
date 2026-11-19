"""Gusu print notebook. Build from edited, traceable data without archive or network access."""
from pathlib import Path
from html import escape as e
import json,re
from build_homer import LIGHTBOX
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'museum-notes/gusu-prints';URL='/museum-notes/gusu-prints/'

def build():
    load=lambda name:json.loads((BASE/'data'/f'{name}.json').read_text())
    works=load('works');by={w['id']:w for w in works};assets=load('assets');ab={a['photo_number']:a for a in assets};images=load('derivatives');sources=load('sources');ed=load('editorial')
    chapter_names={c['id']:c['title'] for c in ed['chapters']}
    chapter_names.update({'manuals':'晚明书谱','exchange':'木版的远行'})
    def whref(w):return URL+w['id']+'/'
    def inline(s):
        s=e(s)
        def citations(m):
            refs=re.findall(r'S\d+|L\d+|CMA[\d.]+',m[1]);out=[]
            for ref in refs:
                if ref.startswith('S'):
                    assert ref in sources,ref
                    out.append(f'<a class="gs-cite" href="{URL}sources/#{ref}" title="{e(sources[ref]["title"])}">[{int(ref[1:])}]</a>')
                elif ref.startswith('L'):
                    assert int(ref[1:]) in ab
                    out.append(f'<a class="gs-cite" href="{URL}sources/#{ref}">[展签]</a>')
                else:out.append(f'<a class="gs-cite" href="https://www.clevelandart.org/art/{ref[3:]}" target="_blank" rel="noopener">[馆录]</a>')
            return ''.join(out)
        s=re.sub(r'\[((?:S\d+|L\d+|CMA[\d.]+)[^\]]*)\]',citations,s)
        s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
        s=re.sub(r'\*([^*]+)\*',r'<em>\1</em>',s)
        s=re.sub(r'(?<![A-Za-z0-9])[gb]\d{2}(?![A-Za-z0-9])',lambda m: f'<a href="{whref(by[m[0]])}">{e(by[m[0]]["title_zh"])}</a>' if m[0] in by else m[0],s)
        return s
    def md(s,prefix='section'):
        chunks=re.split(r'\n\s*\n',s.strip());out=[];n=0
        for chunk in chunks:
            lines=chunk.splitlines()
            if lines[0].startswith('# '):continue
            if re.match(r'^#{2,3} ',lines[0]):
                n+=1;title=re.sub(r'^#+ ','',lines[0]);out.append(f'<h2 id="{prefix}-{n}">{inline(title)}</h2>')
                if len(lines)>1:out.append('<p>'+inline(' '.join(lines[1:]))+'</p>')
            elif lines[0].startswith('|'):
                rows=[r for r in lines if not re.match(r'^\|[\s:|\-]+$',r)];cells=lambda r:[x.strip() for x in r.strip('|').split('|')]
                out.append('<div class="gs-table" tabindex="0" role="region" aria-label="资料表，可横向浏览"><table><thead><tr>'+''.join('<th scope="col">'+inline(x)+'</th>' for x in cells(rows[0]))+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in cells(r))+'</tr>' for r in rows[1:])+'</tbody></table></div>')
            elif re.match(r'^(?:- |\d+\. )',lines[0]):
                tag='ul' if lines[0].startswith('- ') else 'ol';out.append('<'+tag+'>'+''.join('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',r))+'</li>' for r in lines)+'</'+tag+'>')
            else:out.append('<p>'+inline(' '.join(lines))+'</p>')
        return ''.join(out)
    def image(n,alt,eager=False,small=False):
        key=str(n) if str(n).startswith(('p','detail-')) else 'p'+str(n);im=images[key];v=im['variants']
        sizes='(max-width: 600px) 43vw, 220px' if small else '(max-width: 680px) calc(100vw - 40px), (max-width: 1050px) 80vw, 760px'
        return f'<img src="{URL}{v[0 if small else min(1,len(v)-1)]["path"]}" srcset="'+', '.join(f'{URL}{x["path"]} {x["width"]}w' for x in v)+f'" sizes="{sizes}" width="{im["width"]}" height="{im["height"]}" alt="{e(alt)}" '+('fetchpriority="high"' if eager else 'loading="lazy"')+' decoding="async">'
    def caption(w,extra=''):
        return w['title_zh']+(' · '+extra if extra else '')+'｜'+w['collection']+(' · '+ '、'.join(w['accessions']) if w['accessions'] else '')+'｜Merton摄'
    def figure(n,cap,cls='',eager=False,anchor=''):
        key=str(n) if str(n).startswith(('p','detail-')) else 'p'+str(n);im=images[key];ratio=im['width']/im['height'];maxw=min(1050,round(760*ratio),im['width'])
        return f'<figure class="gs-figure {cls}"'+(f' id="{anchor}"' if anchor else '')+f' style="--figure-width:{maxw}px"><a data-photo href="{URL}{im["full"]}" data-caption="{e(cap)}">{image(n,cap,eager)}</a><figcaption>{e(cap)}</figcaption></figure>'
    def mini(w):
        return f'<a class="gs-mini" href="{whref(w)}">{image(w["main_photo"],caption(w),small=True)}<h3>{e(w["title_zh"])}</h3><p>{e(w["date_display"])} · '+('、'.join(w['accessions']) or '私人收藏')+'</p></a>'
    def shell(title,body,slug='',cover=3066):
        canonical='https://qm2.github.io'+URL+(slug+'/' if slug else '')
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Merton</title><meta name="description" content="纸上姑苏，烟火江南：克利夫兰亲见的32条作品与成组记录，从花鸟清供到城门舟楫。"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{e(title)}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://qm2.github.io{URL}{images['p'+str(cover)]['full']}"><link rel="stylesheet" href="/museum-notes/museum.css"><link rel="stylesheet" href="/museum-notes/caravaggio/caravaggio.css"><link rel="stylesheet" href="{URL}gusu.css"><script src="/museum-notes/caravaggio/caravaggio.js" defer></script><script src="{URL}gusu.js" defer></script></head><body class="gs-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="/museum-notes/">Merton</a><nav aria-label="专题导航"><a href="{URL}">纸上姑苏</a><a href="{URL}guide/">认识版画</a><a href="{URL}catalogue/">作品目录</a><a href="{URL}collection/">流传与收藏</a><a href="{URL}sources/">资料</a></nav></header><main class="wrap" id="main"><nav class="breadcrumbs" aria-label="当前位置"><a href="/museum-notes/">博物馆札记</a><span>/</span>'''+(f'<a href="{URL}">纸上姑苏</a><span>/</span>' if slug else '')+f'<span>{e(title)}</span></nav>{body}</main><footer class="site-footer wrap"><a href="/museum-notes/">博物馆札记</a><span>现场摄影与观看札记／Merton</span><a href="#top">回到顶部</a></footer>{LIGHTBOX}</body></html>'
    def write(slug,title,body,cover=3066):
        folder=BASE/slug;folder.mkdir(parents=True,exist_ok=True);(folder/'index.html').write_text(shell(title,body,slug,cover))
    def heading(title,sub='',eyebrow='SUZHOU PRINTS / CLEVELAND, 2026'):
        return f'<header class="gs-heading"><p class="eyebrow">{e(eyebrow)}</p><h1>{e(title)}</h1><p class="gs-deck">{e(sub)}</p></header>'
    def relation_map():
        places=[('nanjing','南京','书谱编印','胡正言在南京编印《十竹斋书画谱》。小幅书页提供近距离看颜色与笔墨的入口。','b02','L2998'),('suzhou','苏州','制作中心与图像地点','阊门、胥门与虎丘进入版画；作坊也把杭州西湖和理想园林刻入可以流通的图像。','g03','S10'),('hangzhou','杭州','图像地点','《西湖全景》画的是杭州；其苏州制作语境与今天的收藏、观看地点分别记录。','g29','S16')]
        h='<section class="gs-section" id="places"><div class="gs-prose"><p class="eyebrow">PLACES &amp; RELATIONSHIPS</p><h2>江南与远方</h2><p>先分清哪里编印、画的是哪里，再看同版图像如何在远方留存。这里是一幅地点关系示意，不按距离比例排列，也不表示某张印本的航行路线。</p></div><nav class="gs-place-links" aria-label="江南地点关系">'
        h+=''.join(f'<a href="#place-{pid}"><strong>{name}</strong><span>{role}</span></a>' for pid,name,role,txt,w,s in places)+'</nav>'
        for pid,name,role,txt,w,s in places:
            h+=f'<details class="gs-place" id="place-{pid}"><summary>{name} · {role}<i aria-hidden="true">＋</i></summary><div class="gs-place-body"><div>{md(txt+"["+s+"]")}</div>{mini(by[w])}</div></details>'
        h+='<details class="gs-place" id="place-overseas"><summary>海外：同版保存与今天的收藏<i aria-hidden="true">＋</i></summary><div class="gs-prose">'+md('捷克Veltrusy庄园的画眉、奥地利Eisenstadt的Esterházy宫中的《冬》，是同版印本的保存例证。它们与眼前CMA印本的完整来源链是不同问题。[L3041、L3054]\n\n日本与欧洲收藏保存了许多早期苏州图像。2025年，克利夫兰与纽约两馆购藏冯氏旧藏中的重要一批，成为今天的研究地点。本辑原作收藏以逐件记录为准；私人《笺霞集》与CMA既有《十竹斋书画谱》分别处理。[S02、S03]')+'</div><div class="gs-mini-grid">'+mini(by['g25'])+mini(by['g28'])+'</div></details></section>'
        return h
    def compare(c):
        return f'<section class="gs-comparison compare-group" id="compare-{c["id"]}"><div class="gs-prose"><h2>{e(c["title"])}</h2>{md(c["text"])}</div><div class="gs-compare-row">'+''.join('<div>'+figure(w['main_photo'],caption(w)) + f'<p class="gs-small"><a href="{whref(w)}">进入{e(w["title_zh"])}细读</a></p></div>' for w in [by[x] for x in c['works']])+'</div><p class="gs-small">完整画面保留各自比例；并列不代表原作等比例。</p></section>'
    def catalogue():
        cats=sorted(set(w['chapter'] for w in works));dates=list(dict.fromkeys(w['date_display'] for w in works))
        h='<div class="gs-filters" hidden><label>查找作品<input type="search" id="gs-query" placeholder="题名、馆藏号、人物、工艺"></label><label>主题<select id="gs-chapter"><option value="">全部主题</option>'+''.join(f'<option value="{c}">{chapter_names.get(c,c)}</option>' for c in cats)+'</select></label><label>年代<select id="gs-date"><option value="">全部年代</option>'+''.join(f'<option>{e(d)}</option>' for d in dates)+'</select></label><label>阅读<select id="gs-depth"><option value="">全部记录</option><option value="deep">重点细读</option></select></label><button type="button" id="gs-reset">清除条件</button></div><p class="gs-small" id="gs-count" role="status" aria-live="polite">32条作品／成组记录</p><div class="gs-catalogue">'
        for w in works:
            search=' '.join([w['title_zh'],w['title_en'],w['maker'],w['medium'],w['collection'],' '.join(w['accessions']),w['summary']])
            total=len(set(w['full_photos']+w['detail_photos']+w['label_photos']))
            h+=f'<article class="gs-card" data-search="{e(search)}" data-chapter="{w["chapter"]}" data-date="{e(w["date_display"])}" data-depth="{"deep" if w["deep_read"] else "basic"}">'+mini(w)+f'<p class="gs-small">{e(w["medium"])}<br>{e(w["collection"])} · {total}张照片</p><p class="gs-card-links"><a href="{whref(w)}">{"重点细读" if w["deep_read"] else "作品札记"}</a> · <a href="{whref(w)}#labels">现场展签</a></p></article>'
        return h+'</div><p id="gs-empty" hidden>没有符合条件的记录。可以减少关键词，或清除筛选。</p>'
    # Home keeps the personal narrative and detailed readings on separate reading scales.
    home='<section class="gs-opening"><div>'+heading(ed['title'],ed['subtitle'])+'<p class="gs-cover-note">从一根细线开始，走入月洞门后的江南。</p><a class="text-link" href="#first-look">先看五处细节</a></div>'+figure(3066,caption(by['g30']),eager=True)+'</section>'
    home+='<div class="gs-prose gs-intro">'+md(ed['intro'])+'</div><div class="gs-exhibition"><p><em>Print Revolutions: Chinese Impressions, 1630s–1960s</em><br>克利夫兰艺术博物馆 · 正式展期2026年11月15日—2027年4月4日'+inline('[S01]')+'</p><p>亲见：2026年11月13—14日行程，提前开放期间<br>本辑：32条作品／成组记录，129张现场照片；非原展全目录。</p></div>'
    home+='<section class="gs-section" id="first-look"><h2>先从五处细节看起</h2><p class="gs-small">沿着招牌、细线与花枝，进入各幅作品的完整世界。</p><nav class="gs-detail-index" aria-label="五处局部导览">'+''.join(f'<a href="{whref(by[x["work"]])}">{image("detail-"+x["work"],x["caption"]+" · 原片局部",small=True)}<h3>{e(x["caption"])}</h3><p>{e(by[x["work"]]["title_zh"])} · 局部</p></a>' for x in ed['favorites'])+'</nav></section>'
    home+='<section class="gs-section"><h2>先有一副框架</h2><div class="gs-framework"><a href="'+URL+'guide/#guide-1"><h3>这是什么？</h3><p>以苏州生产、流通为中心的商业木版图像，不只有新年题材。</p></a><a href="'+URL+'guide/#guide-4"><h3>怎样印出来？</h3><p>从线、色、对位到纸面起伏，看印刷与手绘怎样相接。</p></a><a href="'+URL+'collection/"><h3>为什么在海外保存？</h3><p>从日常陈设到私人搜集，再到今天的公共收藏。</p></a></div></section>'+relation_map()
    home+='<nav class="gs-localnav" aria-label="六章阅读">'+''.join(f'<a href="#chapter-{c["id"]}">{e(c["title"])}</a>' for c in ed['chapters'])+'</nav>'
    for c in ed['chapters']:
        w=by[c['hero']]
        home+=f'<section class="gs-section gs-chapter" id="chapter-{c["id"]}"><header><p class="eyebrow">{e(c["subtitle"])}</p><h2>{e(c["title"])}</h2><p class="gs-prose">{e(c["intro"])}</p></header><div class="gs-chapter-lead">'+figure(w['main_photo'],caption(w))+'<div><h3><a href="'+whref(w)+'">'+e(w['title_zh'])+'</a></h3>'+md(w['summary'])+'<p class="gs-memory">'+e(w['memory_line'])+'</p><a class="text-link" href="'+whref(w)+'">读这件作品</a></div></div><div class="gs-mini-grid">'+''.join(mini(by[x]) for x in c['works'][:4])+'</div>'
        if len(c['works'])>4:home+='<p class="gs-small">这一章还可看：'+' · '.join(f'<a href="{whref(by[x])}">{e(by[x]["title_zh"])}</a>' for x in c['works'][4:])+'</p>'
        home+='</section>'
    home+=compare(ed['comparisons'][0])+'<details class="gs-more-comparisons"><summary>再并看：花鸟、城市与三种热闹<i aria-hidden="true">＋</i></summary>'+''.join(compare(c) for c in ed['comparisons'][1:])+'</details>'
    home+='<section class="gs-section" id="catalogue"><details><summary><h2>这次所见的完整目录</h2><span>32条记录</span></summary><p>一对、四联与一本书各自成组；展签与细节照片不另计作品。</p>'+catalogue()+'</details><p><a href="'+URL+'catalogue/">单独打开目录与筛选</a></p></section>'
    home+='<section class="gs-section"><h2>展厅之间</h2><div class="gs-gallery">'+''.join(figure(n,'克利夫兰艺术博物馆 · 姑苏版画展厅 · Merton摄') for n in [3070,3072,3073])+'</div></section>'
    home+='<section class="gs-prose gs-closing"><h2>把下一次观看接在这里</h2><p>下一张遇见的版画，也许能让一处铺号、一组套画或一段远行变得更清楚。先把这一回所见留住，再慢慢补上它们的来处。</p><p><a href="'+URL+'sources/">资料与仍待继续的问题</a> · <a href="/museum-notes/chinese-painting/">回到中国书画</a></p></section>'
    write('',ed['title'],home)
    # Long-form background, not a shortened marketing summary.
    guide=heading('认识姑苏版画','给以后观看留一副框架')+'<div class="gs-prose gs-longform">'+md((BASE/'data/guide.md').read_text(),'guide')+'</div>'+relation_map()+'<aside class="gs-related"><a href="'+URL+'b02/">翻看《十竹斋书画谱》</a> · <a href="'+URL+'collection/">流传与收藏史</a> · <a href="'+URL+'catalogue/">从目录选一件来比较</a></aside>'
    write('guide','认识姑苏版画',guide,3005)
    collection=heading('木版的远行','为什么在克利夫兰，遇见了很少留在本土的姑苏版画？')+figure(3038,caption(by['g25']))+'<div class="gs-prose gs-longform">'+md((BASE/'data/collection.md').read_text(),'collection')+'</div><div class="gs-mini-grid">'+mini(by['g25'])+mini(by['g28'])+mini(by['g30'])+'</div>'
    write('collection','木版的远行：流传与收藏',collection,3038)
    write('catalogue','这次所见的完整目录',heading('这次所见的完整目录','32条作品／成组记录 · 129张现场照片')+'<p class="gs-prose">从晚明书谱到清代苏州单张，一对、四联与多开书页分别成组。原作收藏与本次在克利夫兰的观看记录分开保留。</p>'+catalogue())
    # Work pages: complete view, substantive text, local details, evidence, related works.
    detail_caps={2955:'桥拱、城楼与河岸',2956:'商铺招牌与船只',2957:'桥面上的人群',2961:'远景山丘与塔影',2962:'亭台、栏杆与水岸',2963:'庭院中的人物',2981:'船阵与层叠水纹',2982:'山势、船只与远景',2985:'水纹中的捕鱼活动',2988:'骑马人物与密集战阵',3021:'鸟喙与莲蓬',3022:'题诗、鸟与荷叶',3039:'花枝、山石与鸟身',3040:'画眉与题句',3044:'春幅女子与儿童',3045:'春幅衣纹与孩子的动作',3048:'夏幅插莲与儿童',3049:'夏幅人物上身与莲花',3052:'冬幅手炉、爆竹与小狗',3053:'冬幅室内人物',3060:'第一联建筑与湖岸',3061:'第二联水岸与人物',3062:'第三联桥、船与建筑',3063:'第四联塔影与湖岸',3064:'岸边行人',3067:'母子、纱扇与细线',3068:'母子面容与月洞门'}
    related={'g02':['g03','g29'],'g03':['g29','g02'],'g04':['g03','g07'],'g05':['g06'],'g06':['g05'],'b01':['g09','b02'],'b02':['b01','g17'],'g30':['g27','g09'],'g26':['g27','g28'],'g27':['g26','g30'],'g28':['g26','g29'],'g17':['g22','g24'],'g22':['g17','g24'],'g23':['g25','g20'],'g24':['g22','b02'],'g25':['g23','g28'],'g29':['g03','g28'],'g11':['g12','g13'],'g12':['g11','g13'],'g13':['g11','g12']}
    book_caps={2996:'枯枝与花朵',2997:'荔枝果皮',2999:'孔洞与奇石',3000:'盘中景物',3002:'兰叶',3003:'荔枝枝叶',3004:'瓶花',3005:'荷花与荷叶',3006:'鸟与花枝',3007:'果串与枝叶',3008:'花鸟',3009:'竹叶与花枝',3010:'兰与花枝'}
    for w in works:
        body=heading(w['title_zh'],w['title_en'],'SUZHOU PRINTS / CLOSE LOOK')+f'<p class="gs-meta">{e(w["date_display"])} · {e(w["medium"])}<br>{e(w["collection"])}'+(' · '+'、'.join(w['accessions']) if w['accessions'] else '')+'</p>'
        if w['id']=='b02':
            order=[3005]+[n for n in w['full_photos'] if n!=3005]
            body+='<section class="gs-book" aria-label="书谱开页选择"><p class="gs-small">逐开看：同一本书，不同的物象。</p><div class="gs-book-controls" hidden>'+''.join(f'<button type="button" data-open-page="{n}" aria-pressed="{"true" if n==3005 else "false"}">{book_caps[n]}</button>' for n in order)+'</div>'
            body+=''.join(f'<div data-book-page="{n}">'+figure(n,caption(w,'展开页：'+book_caps[n]),eager=n==3005)+'</div>' for n in order)+'</section>'
        else:body+=figure(w['main_photo'],caption(w),'gs-main-art',True,'full-view')
        body+='<div class="gs-prose gs-intro">'+md(w['summary'])+'<p class="gs-memory">'+e(w['memory_line'])+'</p></div>'
        used=set()
        if w.get('reading'):
            r=w['reading'];body+='<div class="gs-prose"><h2>'+e(r['title'])+'</h2></div>'
            pieces=re.split(r'^### ',r['body'],flags=re.M)
            if len(pieces)>1:segments=[p.strip() for p in pieces if p.strip()]
            else:
                paras=[p for p in r['body'].split('\n\n') if p.strip()];segments=['\n\n'.join(paras[i:i+2]) for i in range(0,len(paras),2)]
            for i,piece in enumerate(segments):
                if len(pieces)>1: title,_,prose=piece.partition('\n');content='<h3>'+inline(title)+'</h3>'+md(prose)
                else: content=md(piece)
                sequence=r.get('photo_sequence',w['detail_photos'])
                if i<len(sequence) and sequence[i]:
                    n=sequence[i];used.add(n)
                    body+=f'<section class="gs-close compare-group {"gs-reverse" if i%2 else ""}">'+figure(n,caption(w,'局部：'+detail_caps.get(n,'画面细节')))+'<div>'+content+'<p class="gs-small"><a href="#full-view">回看完整画面</a></p></div></section>'
                else:body+='<div class="gs-prose gs-reading">'+content+'</div>'
        body+='<section class="gs-prose gs-reading"><h2>再看三处</h2><ul>'+''.join('<li>'+inline(x)+'</li>' for x in w['look'])+'</ul><p class="gs-small">作品与工艺说明据本件'+''.join(inline('['+s+']') for s in w['label_source_ids'])+'；观看路线与记忆句为本站细读。</p></section>'
        if w['id'] in ['g26','g27']:body+=compare(ed['comparisons'][0])
        if w['id']=='g29':
            body+='<section class="gs-section compare-group"><h2>沿现场顺序，逐联看</h2><p class="gs-small">先回看整组，再逐张放大；未将子件编号强配到左右位置。</p><div class="gs-four-leaves">'+''.join(figure(n,f'《西湖全景》第{i+1}联 · 现场从左至右｜Merton摄') for i,n in enumerate([3056,3057,3058,3059]))+'</div></section>';used.update([3056,3057,3058,3059])
        photos=[n for n in w['full_photos']+w['detail_photos'] if n!=w['main_photo'] and n not in used and w['id']!='b02']
        if photos:body+='<details class="gs-album"><summary>更多现场照片<i aria-hidden="true">＋</i></summary><div class="gs-gallery compare-group">'+''.join(figure(n,caption(w,('局部：'+detail_caps.get(n,'画面细节')) if n in w['detail_photos'] else '完整照片／展陈视角')) for n in photos)+'</div></details>'
        body+='<details class="gs-evidence" id="labels"><summary>现场展签与作品资料<i aria-hidden="true">＋</i></summary><dl class="gs-facts">'+''.join(f'<div><dt>{key}</dt><dd>{e(val)}</dd></div>' for key,val in [('原名',w['title_en']),('年代',w['date_display']),('材质',w['medium']),('题署／制作',w['maker']),('收藏',w['collection']),('馆藏号','、'.join(w['accessions']) or '展签未载'),('亲见','克利夫兰艺术博物馆，2026年11月13—14日行程')])+'</dl>'
        if w['reader_note']:body+='<div class="gs-prose">'+md(w['reader_note'])+'</div>'
        body+=''.join(figure(n,w['title_zh']+' · 现场展签，Merton摄；如含第三方图版，仅作展签档案') for n in w['label_photos'])+'</details>'
        body+='<details class="gs-evidence"><summary>馆录与来源<i aria-hidden="true">＋</i></summary><div class="gs-prose">'
        for record in w['official_records']:
            title=record['heading_excerpt'][0] if record.get('heading_excerpt') else record['accession'];body+=f'<p><a target="_blank" rel="noopener" href="{e(record["url"])}">CMA {record["accession"]}：{e(title)}</a></p>'
            if record.get('measurements'):body+='<p class="gs-small">馆录尺寸：'+e(record['measurements'])+'</p>'
        body+='<p class="gs-small">馆录资料由2026年11月18日研究包核查整理；题名与展签的差异保留。原始照片与编号另存档，网页展示其衍生图。</p></div></details>'
        body+='<aside class="gs-related"><h2>把视线移到另一张纸上</h2><div class="gs-mini-grid">'+''.join(mini(by[x]) for x in related.get(w['id'],[]) if x in by)+'</div><p><a href="'+URL+'guide/">认识姑苏版画</a> · <a href="'+URL+'collection/">流传与收藏</a> · <a href="'+URL+'catalogue/">返回完整目录</a></p></aside>'
        write(w['id'],w['title_zh'],body,w['main_photo'])
    # Sources provide stable targets for every photographed evidence reference.
    body=heading('资料与现场展签','研究依据、图像记录与仍待补充的问题')+'<div class="gs-prose"><p>基本信息依据现场展签与素材包已核查的馆录。正文中的观看路线属于本站解读；数字注号链接文献，展签注号链接原始说明的现场照片。</p></div><ol class="gs-sources">'
    for key,s in sources.items():
        scope=inline(re.sub(r'(?<!\[)(L\d{4})', r'[\1]', s['scope'].replace('本包','本辑')))
        body+=f'<li id="{key}" value="{int(key[1:])}"><a target="_blank" rel="noopener" href="{e(s["url"])}">{e(s["title"])}</a><p>{scope}</p></li>'
    body+='</ol><section class="gs-section"><h2>现场展签档案</h2><p class="gs-prose">共享展签可以对应多件作品；展签内所嵌宫室照片、版块示意等属于第三方资料，不是Merton在该地拍摄的作品照片。</p>'
    for a in assets:
        if a['kind'] not in ['label','panel']:continue
        n=a['photo_number'];names=list(dict.fromkeys(by[m['work_id']]['title_zh'] for m in a['memberships']));title=a.get('panel_title') or '／'.join(names) or '现场展签'
        body+=f'<details id="L{n}" class="gs-evidence"><summary>{e(title)}<i aria-hidden="true">＋</i></summary>'+figure(n,title+' · 现场展签，Merton摄')+'</details>'
    body+='</section><details><summary>仍待继续：题款、同版印本与来源<i aria-hidden="true">＋</i></summary><div class="gs-prose"><p>部分题署的中文姓名字形仍需图录或原款校读，先保留可靠英文转写。胥门两张与西湖四联的子件编号尚未逐一对应现场次序；每张印本的完整出海路线也未确认。</p><p>《欧洲冯氏藏中国姑苏版画》全文与《Orientations》2026年11／12月号文章尚未通读；已读目录摘要与书目信息分别注明。下一步可优先补充铺号、题诗与成套关系。</p></div></details><details><summary>另存的展厅视角<i aria-hidden="true">＋</i></summary>'+figure(3071,'克利夫兰艺术博物馆 · 花鸟版画墙与展柜 · Merton摄')+'</details><p class="gs-small">本辑中文标题为编辑题名，并非馆方中文展名。原始129张照片保留在私人档案；网页采用现场摄影的WebP衍生图与明确标注的局部，不加入馆方作品照片或生成式修复图。</p>'
    write('sources','资料与现场展签',body)
    # Insert only scoped, idempotent entrances after all existing generators.
    for path,marker,entry in [
        (ROOT/'museum-notes/index.html','gusu-home','<a class="issue-link" href="gusu-prints/">'+image(3067,'夏日亭畔母子图局部 · 纸上姑苏，烟火江南',small=True)+'<div><p class="eyebrow">SUZHOU PRINTS</p><h2>纸上姑苏，烟火江南</h2><p>从花鸟清供到城门舟楫，重看江南的典雅与日常。克利夫兰亲见的32条作品与成组记录。</p><span class="text-link">进入这一辑</span></div></a>'),
        (ROOT/'museum-notes/chinese-painting/index.html','gusu-related','<aside class="editorial-note"><h2>从笔墨到木版</h2><p><a href="'+URL+'">纸上姑苏，烟火江南</a>：彩印书谱、花鸟清供与城市名胜，另成一辑，保留逐件照片、展签与细读。</p></aside>')]:
        html=re.sub(f'<!-- {marker} -->.*?<!-- /{marker} -->','',path.read_text(),flags=re.S)
        block=f'<!-- {marker} -->'+entry+f'<!-- /{marker} -->'
        if marker=='gusu-home':
            anchor='<!-- ten-kings-home -->';assert anchor in html;html=html.replace(anchor,block+anchor,1)
        else:html=html.replace('</main>',block+'</main>',1)
        path.write_text(html)
    print(f'Gusu: {len(works)} records, {len(assets)} source photos, 37 pages; local derivatives only.')

if __name__=='__main__':build()
