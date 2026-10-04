"""Curated sculpture topics; called by build_museum with its existing card renderer."""
from html import escape as e
import json

def build(root, objects, museums, render_card, lightbox):
    by_id={o['id']:o for o in objects}
    topics=[
        dict(id='water-moon-guanyin',title='水月观音',subtitle='一膝支起，一臂舒展。',intro='从大都会的水月观音，到纳尔逊的南海观音，慢慢比较六尊坐像的姿态、面容与残彩。',ids=[215,213,226,195,247,251],hero=215,note='以水月观音为中心，也并置南海观音与自在坐观音。每件作品保留馆方名称；坐姿相近，并不意味着它们都被馆方定名为水月观音。'),
        dict(id='song-liao-jin-wood',title='宋辽金木雕',subtitle='站立的身姿，留下的木色。',intro='从菩萨立像、观音头像到十一面观音，看这一时期木雕的几种面貌。水月观音另成一辑，两边可以连着看。',ids=[233,217,229,218,209,263],hero=233,note='以宋辽金时期为中心，保留馆方的跨朝代断代，包括“五代或辽”。这里只选六件作为观看线索；水月观音专题中的同期木雕不在本页重复铺开。'),
        dict(id='dry-lacquer',title='夹纻干漆造像',subtitle='漆与织物，塑成中空的身体。',intro='从唐代佛像、菩萨与佛首，到元代释迦牟尼像，细看干漆造像的表面与内部。',ids=[265,231,259,245],hero=265,note='夹纻干漆以漆与织物逐层成形，脱去内芯后留下中空像体。这里收录已有资料支持的干漆作品；沃尔特斯的填料漆塑、木芯泥层髹漆的观音不混入这一单元。宾大作品沿用展签的“干漆”材料名称。')]
    selected={f'object-{n}' for t in topics for n in t['ids']}
    def shell(title,body):
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · 博物馆札记 | Merton</title><link rel="stylesheet" href="../museum.css"><link rel="stylesheet" href="../sculpture-topics.css"><script src="../museum.js" defer></script></head><body id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="../">Merton</a><nav aria-label="主导航"><a href="../chinese-buddhist-art/">中国佛教艺术</a><a href="../">博物馆首页</a></nav></header><main id="main">{body}</main><footer class="site-footer wrap"><a href="../chinese-buddhist-art/">← 中国佛教艺术</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{lightbox}</body></html>'''
    def entry(t):
        o=by_id[f'object-{t["hero"]}']
        return f'''<a class="issue-link" href="../{t['id']}/"><img src="../buddhist-sculpture/images/{o['photo']}" alt="{e(o['title'])}，{e(museums[o['museum']][0])}" width="{o['width']}" height="{o['height']}" loading="lazy"><div><p class="eyebrow">{len(t['ids'])} 件作品</p><h2>{t['title']}</h2><p>{t['intro']}</p><span class="text-link">走进这一辑 →</span></div></a>'''
    for t in topics:
        o=by_id[f'object-{t["hero"]}'];selection=[by_id[f'object-{n}'] for n in t['ids']]
        poem='''<section class="topic-poem wrap" aria-labelledby="poem-title"><p class="eyebrow">宋代 · 释心月</p><h2 id="poem-title">水月观音赞</h2><blockquote>觉天无云，性海无风。<br>玉轮蘸影，金浪翻空。<br>非惟观世音，我亦游其中。</blockquote><p class="source"><a href="https://www.sou-yun.cn/Query.aspx?id=227226&amp;type=poem" target="_blank" rel="noopener noreferrer">原文核对：搜韵 ↗</a></p></section>''' if t['id']=='water-moon-guanyin' else ''
        cards=''.join(render_card(x,i,'../buddhist-sculpture/images/') for i,x in enumerate(selection))
        # Keep the shared lightbox and hash behavior; thematic pages do not need archive filters.

        body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>{t['title']}</span></nav><section class="hero wrap"><div class="hero-copy"><p class="eyebrow">CHINESE BUDDHIST SCULPTURE</p><h1>{t['title']}</h1><p class="subtitle">{t['subtitle']}</p><p class="intro">{t['intro']}</p><a class="text-link" href="#collection">细看这{len(selection)}件作品 ↓</a></div><figure class="hero-image"><img src="../buddhist-sculpture/images/{o['photo']}" alt="{e(o['title'])}" width="{o['width']}" height="{o['height']}" fetchpriority="high"><figcaption>{e(o['title'])} · {e(o['date'])}<br><span>{e(museums[o['museum']][0])}</span></figcaption></figure></section>{poem}<section class="collection wrap" id="collection"><div class="collection-heading"><div><p class="eyebrow">SELECTED WORKS</p><h2>一件一件看</h2></div><p>{len(selection)} 件作品</p></div><div class="object-grid">{cards}</div></section><aside class="editorial-note wrap"><h2>这一辑的范围</h2><p>{t['note']}</p><p>照片与现场展签保留原有记录，收藏故事附在作品札记中。</p></aside><section class="wrap topic-next"><h2>接着看</h2>{''.join(f'<a href="../{x["id"]}/">{x["title"]} →</a>' for x in topics if x!=t)}</section>'''
        path=root/'museum-notes'/t['id'];path.mkdir(exist_ok=True);(path/'index.html').write_text(shell(t['title'],body))
    directory=f'''<div class="wrap notebook-index"><p class="eyebrow">MUSEUM NOTES / CHINESE BUDDHIST ART</p><h1>中国佛教艺术</h1><p class="index-intro">选几件值得反复看的作品，<br>一个主题，一个主题地整理。</p><section aria-labelledby="sculpture-title"><p class="eyebrow">SCULPTURE NOTEBOOKS</p><h2 id="sculpture-title">造像 · 三个专题</h2>{''.join(entry(t) for t in topics)}</section><aside class="notebook-about"><h2>下一辑：辽代三彩罗汉</h2><p>等照片整理好，再把这组罗汉单独放到一起看。</p></aside><section class="material-directory" aria-labelledby="painting-title"><p class="eyebrow">BUDDHIST PAINTING</p><h2 id="painting-title">绘画 · 另一路观看</h2><div class="material-grid"><a class="material-entry" href="../dunhuang-painting/"><h3>敦煌绘画 ↗</h3><p>供养画、菩萨幡与地藏像。</p></a><a class="material-entry" href="../buddhist-painting/"><h3>寺院壁画与佛教卷轴 ↗</h3><p>壁画、罗汉与佛菩萨画像。</p></a></div></section><p class="source"><a href="../buddhist-sculpture/">早期整理记录 →</a></p></div>'''
    (root/'museum-notes/chinese-buddhist-art/index.html').write_text(shell('中国佛教艺术',directory))
    # Old URLs and object fragments remain accessible, but the former omnibus no longer acts as a featured issue.
    archive=root/'museum-notes/buddhist-sculpture/index.html';s=archive.read_text()
    start=s.index('<section class="hero wrap"');end=s.index('<section id="collection"',start)
    s=s[:start]+'''<section class="category-header wrap"><p class="eyebrow">EARLIER RECORDS</p><h1>早期造像记录</h1><p class="index-intro">新整理的专题已移到中国佛教艺术首页。<br>这里保留此前的作品记录和固定链接。</p><a class="text-link" href="../chinese-buddhist-art/">浏览精选专题 →</a></section>'''+s[end:]
    s=s.replace('自在之姿 · 佛教造像札记','早期造像记录').replace('<span>自在之姿</span>','<span>早期造像记录</span>').replace('<a href="#reading">阅读线索</a>','')
    archive.write_text(s)
    for material in ['wood','lacquer','stone','bronze','mixed']:
        p=root/'museum-notes'/material/'index.html';p.write_text(p.read_text().replace('自在之姿专题','早期造像记录'))
    p=root/'museum-notes/index.html';s=p.read_text().replace('从观音木雕与像内经卷，继续看到寺院壁画、敦煌绘画与罗汉图。','从水月观音、宋辽金木雕与夹纻干漆开始，一辑一辑细看。').replace(f'{len(objects)} 件造像 ·',f'3 个造像专题 · {len(selected)} 件精选造像 ·').replace('造像 / 经卷 / 寺院壁画 / 敦煌绘画','水月观音 / 宋辽金木雕 / 夹纻干漆 / 佛教绘画');p.write_text(s)
    (root/'museum-notes/buddhist-sculpture/data/topics.json').write_text(json.dumps({'updated':'2026-10-04','topics':topics,'planned':['辽代三彩罗汉'],'archived_ids':[o['id'] for o in objects if o['id'] not in selected]},ensure_ascii=False,indent=2)+'\n')
    print(f'Built 3 curated sculpture topics, {len(selected)} selected works; retained archive URLs.')
