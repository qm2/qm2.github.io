"""Curated sculpture topics; called by build_museum with its existing card renderer."""
from html import escape as e
import json

def build(root, objects, museums, render_card, lightbox):
    by_id={o['id']:o for o in objects}
    topics=[
        dict(id='water-moon-guanyin',title='水月观音',subtitle='一膝支起，一臂舒展。',intro='把看过的水月、南海与自在坐观音放到一起。从夏威夷到波特兰，从木色、石面到金漆，同一个姿态有许多种样子。',ids=[215,213,226,195,235,247,251,255,243,241,199,224],hero=215,note='馆方分别使用“水月”“南海”或“自在坐”等题名。木雕之外，沃尔特斯干漆、吉美石雕和纳尔逊复合材料像，也呈现了相近姿态在不同材料中的变化。'),
        dict(id='song-liao-jin-wood',title='五代至元木雕',subtitle='站立、端坐，也有沉思。',intro='从五代、宋辽金看到元代，收在一起看菩萨、观音与罗汉。同期的水月观音另有专题；隋代佛像与明代侍童也作为前后参照留下。',ids=[201,203,209,233,217,229,218,263,220,227,253,238,257],hero=233,note='这一辑以五代至元木雕为主，隋代佛坐像和明代观音侍童提供前后参照。木雕水月观音另有专题。',subgroups=[dict(title='五代至宋辽金',ids=[201,203,209,233,217,229,218,263]),dict(title='元代',ids=[220,227,253]),dict(title='前后参照：隋与明',ids=[238,257])]),
        dict(id='dry-lacquer',title='干漆与漆塑造像',subtitle='木胎、织物与漆，各有自己的结构。',intro='从沃尔特斯的隋代木胎漆佛，到唐代夹纻干漆、观音与元代漆塑。把佛与菩萨的身份、木胎与脱胎的工艺，逐件分清。',ids=[265,231,259,241,245,249,238,224],hero=238,note='浸漆织物脱去内芯后形成中空像体，沃尔特斯观音（25.256）就是一例。沃尔特斯隋代佛坐像（25.9，可能为阿弥陀佛）则保留拼合木胎；纳尔逊观音由木芯、泥层和金漆构成。几件作品的外表都有漆，内部结构却各不相同。',subgroups=[dict(title='夹纻干漆',ids=[265,231,259,241,245]),dict(title='相关漆塑',ids=[249]),dict(title='材料比较：木胎覆漆',ids=[238,224])]),
        dict(id='yixian-luohan',title='易县三彩罗汉',subtitle='同样的袈裟，不同的面孔。',intro='巴黎、堪萨斯城、纽约、费城。把五尊三彩罗汉放到一起，先看眉眼与手势，再看它们离开原来环境之后的故事。',ids=[614,616,618,741,612],hero=614,note='吉美像的具体尊者身份及易县组属尚不确定。易县洞窟的发现经过已有记述，但组像原属的寺院、数量与确切来源仍有讨论。')]
    assert len(by_id)==len(objects)
    for t in topics:
        assert len(t['ids'])==len(set(t['ids']))
        assert all(f'object-{n}' in by_id for n in t['ids'])
        if t.get('subgroups'):
            assert [n for g in t['subgroups'] for n in g['ids']]==t['ids']
    assert 238 not in topics[0]['ids'], 'The Walters Buddha is not Guanyin.'
    assert 238 in topics[2]['ids'] and 241 in topics[2]['ids']
    selected={f'object-{n}' for t in topics for n in t['ids']}
    def shell(title,body):
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · 博物馆札记 | Merton</title><link rel="stylesheet" href="../museum.css"><link rel="stylesheet" href="../sculpture-topics.css"><script src="../museum.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="../">Merton</a><nav aria-label="主导航"><a href="../chinese-buddhist-art/">中国佛教艺术</a><a href="../">博物馆首页</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="../chinese-buddhist-art/">← 中国佛教艺术</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{lightbox}</body></html>'''
    def entry(t):
        o=by_id[f'object-{t["hero"]}']
        return f'''<a class="issue-link" href="../{t['id']}/"><img src="../buddhist-sculpture/images/{o['photo']}" alt="{e(o['title'])}，{e(museums[o['museum']][0])}" width="{o['width']}" height="{o['height']}" loading="lazy"><div><p class="eyebrow">{len(t['ids'])} 件作品</p><h2>{t['title']}</h2><p>{t['intro']}</p><span class="text-link">走进这一辑 →</span></div></a>'''
    for t in topics:
        o=by_id[f'object-{t["hero"]}'];selection=[by_id[f'object-{n}'] for n in t['ids']]
        poem='''<section class="topic-poem wrap" aria-labelledby="poem-title"><p class="eyebrow">宋代 · 释心月</p><h2 id="poem-title">水月观音赞</h2><blockquote>觉天无云，性海无风。<br>玉轮蘸影，金浪翻空。<br>非惟观世音，我亦游其中。</blockquote><p class="source"><a href="https://www.sou-yun.cn/Query.aspx?id=227226&amp;type=poem" target="_blank" rel="noopener noreferrer">原文核对：搜韵 ↗</a></p></section>''' if t['id']=='water-moon-guanyin' else ''
        def topic_card(n,i):
            obj=by_id[f'object-{n}']
            card=render_card(obj,i,'../buddhist-sculpture/images/')
            also=[x for x in topics if x['id']!=t['id'] and n in x['ids']]
            if also:
                links=' · '.join(f'<a href="../{x["id"]}/#object-{n}">{x["title"]} →</a>' for x in also)
                card=card.replace('<details>',f'<p class="source">也见：{links}</p><details>',1)
            return card
        if t.get('subgroups'):
            cards=''.join(f'<section class="topic-subgroup"><h3>{g["title"]}</h3><div class="object-grid">'+''.join(topic_card(n,t['ids'].index(n)) for n in g['ids'])+'</div></section>' for g in t['subgroups'])
        else:
            cards='<div class="object-grid">'+''.join(topic_card(n,i) for i,n in enumerate(t['ids']))+'</div>'
        context=''
        if t['id']=='yixian-luohan':
            context='''<section class="reading wrap"><div class="section-heading"><p class="eyebrow">THE GROUP AND ITS JOURNEY</p><h2>从易县到不同的展厅</h2></div><div class="reading-grid"><article><h3>先看五张脸</h3><p>纳尔逊像双手作禅定姿势，大都会两尊一正一侧，宾大像右手抬至胸前，吉美像的双手停在身前。相近的三彩袈裟与岩座，并没有抹平各自的神态。</p></article><article><h3>洞窟不是完整的答案</h3><p>宾大研究文章回顾了德国人佩尔津斯基在1912年寻访易县洞窟的经历。组像原属的寺院、总数与成员范围，仍有未解之处。</p><p class="source"><a href="https://www.penn.museum/sites/expedition/the-luohan-that-came-from-afar/">宾大博物馆：The Luohan that Came from Afar ↗</a></p></article><article><h3>各馆的断代</h3><p>大都会依据北京附近古窑址的发现，采用约1000年的断代；纳尔逊、宾大和吉美的记录则给出较宽的辽金范围。</p><p class="source"><a href="https://www.metmuseum.org/art/collection/search/44799">大都会藏品记录 ↗</a></p></article></div></section>'''

        body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>{t['title']}</span></nav><section class="hero wrap"><div class="hero-copy"><p class="eyebrow">CHINESE BUDDHIST SCULPTURE</p><h1 class="{'topic-long-title' if len(t['title'])>5 else ''}">{t['title']}</h1><p class="subtitle">{t['subtitle']}</p><p class="intro">{t['intro']}</p><a class="text-link" href="#collection">细看这{len(selection)}件作品 ↓</a></div><figure class="hero-image"><img src="../buddhist-sculpture/images/{o['photo']}" alt="{e(o['title'])}" width="{o['width']}" height="{o['height']}" fetchpriority="high"><figcaption>{e(o['title'])} · {e(o['date'])}<br><span>{e(museums[o['museum']][0])}</span></figcaption></figure></section>{poem}{context}<section class="collection wrap" id="collection"><div class="collection-heading"><div><p class="eyebrow">SELECTED WORKS</p><h2>一件一件看</h2></div><p>{len(selection)} 件作品</p></div>{cards}</section><aside class="editorial-note wrap"><h2>这一辑的范围</h2><p>{t['note']}</p></aside><section class="wrap topic-next"><h2>接着看</h2>{''.join(f'<a href="../{x["id"]}/">{x["title"]} →</a>' for x in topics if x!=t)}</section>'''
        path=root/'museum-notes'/t['id'];path.mkdir(exist_ok=True);(path/'index.html').write_text(shell(t['title'],body))
    directory=f'''<div class="wrap notebook-index"><p class="eyebrow">MUSEUM NOTES / CHINESE BUDDHIST ART</p><h1>中国佛教艺术</h1><p class="index-intro">把值得反复看的作品聚在一起，<br>一个主题，一个主题地整理。</p><section aria-labelledby="sculpture-title"><p class="eyebrow">SCULPTURE NOTEBOOKS</p><h2 id="sculpture-title">造像 · 四个专题</h2>{''.join(entry(t) for t in topics)}</section><section class="material-directory" aria-labelledby="painting-title"><p class="eyebrow">BUDDHIST PAINTING</p><h2 id="painting-title">绘画 · 另一路观看</h2><div class="material-grid"><a class="material-entry" href="../cisheng-murals/"><h3>慈胜寺壁画 ↗</h3><p>主尊、焚香与画下的观音，五件残片的联系。</p></a><a class="material-entry" href="../guangsheng-murals/"><h3>广胜寺壁画 ↗</h3><p>药师佛、炽盛光佛与善财童子：同一座殿堂的三段画面。</p></a><a class="material-entry" href="../dunhuang-painting/"><h3>敦煌绘画 ↗</h3><p>供养画、菩萨幡与地藏像。</p></a><a class="material-entry" href="../buddhist-painting/"><h3>寺院壁画与佛教卷轴 ↗</h3><p>壁画、罗汉与佛菩萨画像。</p></a></div></section><p class="source"><a href="../buddhist-sculpture/">早期整理记录 →</a></p></div>'''
    (root/'museum-notes/chinese-buddhist-art/index.html').write_text(shell('中国佛教艺术',directory))
    # Old URLs and object fragments remain accessible, but the former omnibus no longer acts as a featured issue.
    archive=root/'museum-notes/buddhist-sculpture/index.html';s=archive.read_text()
    start=s.index('<section class="hero wrap"');end=s.index('<section id="collection"',start)
    s=s[:start]+'''<section class="category-header wrap"><p class="eyebrow">EARLIER RECORDS</p><h1>早期造像记录</h1><p class="index-intro">新整理的专题已移到中国佛教艺术首页。<br>这里保留此前的作品记录和固定链接。</p><a class="text-link" href="../chinese-buddhist-art/">浏览精选专题 →</a></section>'''+s[end:]
    s=s.replace('自在之姿 · 佛教造像札记','早期造像记录').replace('<span>自在之姿</span>','<span>早期造像记录</span>').replace('<a href="#reading">阅读线索</a>','')
    archive.write_text(s)
    for material in ['wood','lacquer','stone','bronze','mixed','ceramic']:
        p=root/'museum-notes'/material/'index.html';p.write_text(p.read_text().replace('自在之姿专题','早期造像记录'))
    p=root/'museum-notes/index.html';s=p.read_text().replace('从观音木雕与像内经卷，继续看到寺院壁画、敦煌绘画与罗汉图。','水月观音、五代至元木雕、干漆与漆塑、易县三彩罗汉，一辑一辑细看。').replace(f'{len(objects)} 件造像 ·',f'{len(topics)} 个造像专题 · {len(selected)} 件造像（去重） ·').replace('造像 / 经卷 / 寺院壁画 / 敦煌绘画','水月观音 / 五代至元木雕 / 干漆与漆塑 / 易县三彩罗汉');p.write_text(s)
    archive_reasons={
        'object-197':'敦煌八臂观音为木、象牙、泥草复合材料，保留在早期记录，待敦煌造像专题。',
        'object-211':'唐代石灰岩僧人像，待石雕专题。',
        'object-207':'隋代石雕观音，待石雕专题。',
        'object-237':'隋代砂岩菩萨，待石雕专题。',
        'object-205':'明代青铜观音，待金属造像专题。',
        'object-221':'明代青铜菩萨，待金属造像专题。'}
    assert set(by_id)-selected == set(archive_reasons), 'Every unselected work needs an explicit review.'
    coverage=[dict(id=o['id'],title=o['title'],topics=[t['id'] for t in topics if int(o['id'].split('-')[1]) in t['ids']],archive_reason=archive_reasons.get(o['id'],'')) for o in objects]
    (root/'museum-notes/buddhist-sculpture/data/topic-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
    (root/'museum-notes/buddhist-sculpture/data/topics.json').write_text(json.dumps({'updated':'2026-10-08','topics':topics,'planned':[],'archived_ids':[o['id'] for o in objects if o['id'] not in selected]},ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(topics)} curated sculpture topics, {len(selected)} selected works; retained archive URLs.')
