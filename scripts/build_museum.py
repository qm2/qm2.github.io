"""Regenerate the static museum pages after editing objects.json. Standard library only."""
from pathlib import Path
from html import escape as e
import json
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'museum-notes' / 'buddhist-sculpture'
data = json.loads((PAGE / 'data' / 'objects.json').read_text())
objects = data['objects']
museums = data['museums']
groups = [('all','全部造像'),('seated','水月与自在坐'),('bodhisattva','菩萨的不同面貌'),('buddha','佛与罗汉'),('material','材质之间')]
def render_card(o, i, image_prefix="images/"):
    m,city,en=museums[o['museum']]
    detail = f'<p>{e(o["story"])}</p>' if o['story'] else ''
    for section in o.get('note_sections', []):
        detail += f'<section class="note-section"><h4>{e(section["title"])}</h4><p>{e(section["text"])}</p></section>'
    if o['caveat']: detail += f'<p class="record-note">{e(o["caveat"])}</p>'
    if o['url']: detail += f'<p class="source"><a href="{e(o["url"])}" target="_blank" rel="noopener noreferrer">{e(o.get("source_title", "馆方藏品记录"))} ↗</a></p>'
    for photo in o.get('related_photos', []):
        detail += f'<figure class="related-photo"><a class="photo-link" href="{image_prefix}{e(photo["photo"])}" data-caption="{e(photo["caption"])}" aria-label="放大照片：{e(photo["caption"])}"><img src="{image_prefix}{e(photo["photo"])}" alt="{e(photo["caption"])}" width="{photo["width"]}" height="{photo["height"]}" loading="lazy"><span class="photo-hint">查看大图 ↗</span></a><figcaption>{e(photo["caption"])}</figcaption></figure>'
    detail += '<p class="source">基本信息据现场展签整理；照片 © Merton。</p>'
    personal = ''
    for note in o.get('personal_notes', []):
        if not note.get('text', '').strip():
            continue
        kind = {'visit_memory': '回忆当时', 'photo_reflection': '重看照片', 'onsite': '现场随记'}[note['kind']]
        date = f" · {e(note['written_on'])}记" if note.get('written_on') else ''
        personal += f'<aside class="personal-note"><h4>我的观看 · {kind}{date}</h4><p>{e(note["text"])}</p></aside>'
    return f'''<article class="object-card" id="{o['id']}" data-museum="{o['museum']}" data-material="{o['material_group']}" data-group="{o['group']}">
      <a class="photo-link" href="{image_prefix}{o['photo']}" data-caption="{e(o['title'])} · {e(m)}" aria-label="放大照片：{e(o['title'])}，{e(m)}">
        <img src="{image_prefix}{o['photo']}" alt="{e(o['title'])}，{e(o['date'])}，{e(m)}；{e(o['observation'])}" width="{o['width']}" height="{o['height']}" loading="lazy" decoding="async">
        <span class="photo-hint" aria-hidden="true">查看大图 ↗</span>
      </a>
      <div class="object-body"><div class="object-topline"><span>{e(city)} · {e(m)}</span><a class="permalink" href="#{o['id']}" aria-label="此作品的固定链接">{i+1:02d}</a></div>
      <h3>{e(o['title'])}</h3><p class="original-title">{e(o['original_title'])}</p>
      <dl><div><dt>年代</dt><dd>{e(o['date'])}</dd></div><div><dt>材质</dt><dd>{e(o['material'])}</dd></div><div><dt>编号</dt><dd>{e(o['accession'])}</dd></div></dl>
      <p class="observation">{e(o['observation'])}</p>{personal}
      <details><summary>作品札记与资料 <span aria-hidden="true">＋</span></summary><div class="notes">{detail}</div></details></div>
    </article>'''
materials = [
    ('wood', '木雕', '以木为主要结构，保留彩绘、贴金与后世修整的记录。'),
    ('lacquer', '干漆与漆塑', '夹纻干漆与其他漆塑分别注明，细看不同的成形方式。'),
    ('stone', '石雕', '从砂岩到石灰岩，记录石质、雕刻与残存色彩。'),
    ('bronze', '金属造像', '目前收录铜像，逐件注明合金、髹漆与鎏金信息。'),
    ('mixed', '复合材料', '木、泥、漆与其他材料共同构成的作品，保留完整材料说明。'),
]

def material_nav(prefix='../', active=''):
    current = ' aria-current="page"'
    links = ''.join(f'<a href="{prefix}{key}/"{current if active == key else ""}>{name}</a>' for key,name,_ in materials)
    return f'<nav class="material-nav" aria-label="按材质浏览"><span>按材质</span>{links}<a href="{prefix}buddhist-sculpture/#collection">全部造像</a></nav>'

def collection_markup(selection, image_prefix='images/'):
    options = ''.join(f'<option value="{k}">{e(v[0])} · {e(v[1])}</option>' for k,v in museums.items() if any(o['museum']==k for o in selection))
    buttons = ''.join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{v}</button>' for k,v in groups)
    material_options = ''.join(f'<option value="{k}">{v}</option>' for k,v,_ in materials if any(o['material_group']==k for o in selection))
    cards = ''.join(render_card(o, objects.index(o), image_prefix) for o in selection)
    return f'''<section id="collection" class="collection wrap" aria-labelledby="collection-title"><div class="collection-heading"><div><p class="eyebrow">THE COLLECTION</p><h2 id="collection-title">在展厅里遇见</h2></div><p>保留全貌，也留住每件作品的不同。</p></div>
<div class="controls" hidden><div class="filter-tabs" role="group" aria-label="按题材筛选">{buttons}</div><div class="filter-fields"><label class="search-label">寻找作品<input type="search" id="search" placeholder="观音、卢芹斋、山中商会、藏品编号…" autocomplete="off"></label><label>博物馆<select id="museum"><option value="all">全部博物馆</option>{options}</select></label><label>材质<select id="material"><option value="all">全部材质</option>{material_options}</select></label></div><div class="results-line"><p id="result-count" role="status" aria-live="polite">共 {len(selection)} 件造像</p><button id="reset" type="button">清除筛选</button></div></div>
<noscript><p class="no-script">以下为本页全部{len(selection)}件作品。点击照片可查看大图，展开札记可阅读作品资料。</p></noscript>
<p id="empty" hidden>没有找到符合条件的作品。试试更短的关键词，或清除筛选。</p><div class="object-grid">{cards}</div></section>'''

lightbox = '''<dialog id="lightbox" aria-labelledby="lightbox-caption"><button class="close-lightbox" type="button" aria-label="关闭大图">关闭 ×</button><img id="lightbox-image" alt=""><p id="lightbox-caption"></p><a id="original-link" href="#" target="_blank" rel="noopener">单独打开照片 ↗</a></dialog>'''

html=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>自在之姿 · 佛教造像札记 | Merton</title>
<meta name="description" content="Merton在欧美博物馆拍摄的{len(objects)}件中国佛教造像：以宋辽金元木雕与水月观音为线索，记录姿态、材料、修复与收藏历史。">
<link rel="stylesheet" href="../museum.css"><script src="../museum.js" defer></script></head>
<body id="top"><a class="skip-link" href="#collection">跳至藏品</a>
<header class="site-header"><a class="signature" href="../">Merton</a><nav aria-label="主导航"><a href="../chinese-buddhist-art/">中国佛教艺术</a><a href="#reading">阅读线索</a><a href="#collection">浏览藏品</a></nav></header>
<main>
<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>自在之姿</span></nav>
<section class="hero wrap" aria-labelledby="page-title"><div class="hero-copy"><p class="eyebrow">MUSEUM NOTES &nbsp; / &nbsp; 001</p><p class="pretitle">中国佛教艺术 · 造像札记</p><h1 id="page-title">自在之姿</h1><p class="subtitle">从水月观音出发，<br>重看博物馆里的中国佛教造像。</p><p class="intro">把旅途中拍下的造像放在一起，慢慢看清一只手的垂落、一层衣纹的转折，以及木色与残彩之间留下的时间。</p><p class="intro">这一辑以宋辽金元时期的观音木雕为中心，也收录更早与更晚的作品，以及石、铜和漆塑造像。</p><a class="text-link" href="#collection">走近这批造像 <span aria-hidden="true">↓</span></a><div class="edition"><span><b>{len(objects)}</b> 件造像</span><span><b>{len(museums)}</b> 家博物馆</span><span>摄影 / Merton</span></div></div>
<figure class="hero-image"><img src="images/nelson-215.jpg" alt="纳尔逊－阿特金斯艺术博物馆的南海观音，彩绘木雕，一臂搭在抬起的膝上，坐于岩座。" width="1279" height="1706" fetchpriority="high"><figcaption>南海观音 · 辽或金<br><span>纳尔逊－阿特金斯艺术博物馆 / 34-10</span></figcaption></figure></section>
<section id="reading" class="reading wrap" aria-labelledby="reading-title"><div class="section-heading"><p class="eyebrow">WAYS OF LOOKING</p><h2 id="reading-title">三条阅读线索</h2><p>从姿态到材料，再到一件作品的流转。</p></div>
<div class="reading-grid"><article><span class="chapter-number">01</span><h3>同样自在，各不相同</h3><p>抬起的膝、舒展的臂、垂落的足，构成这批坐像之间的联系。各馆使用“水月”“南海”或“自在坐”等名称，这里保留各自的命名，一起比较。</p><a href="#object-213">从大都会的水月观音看起 ↗</a></article>
<article><span class="chapter-number">02</span><h3>表面也有自己的年代</h3><p>木胎、泥底、彩绘和金漆可能经历多次修整。普林斯顿观音的裙饰或为明代补加；纳尔逊馆另一尊金漆观音的内外层，也可能并非同一时代。</p><a href="#object-247">看一尊观音的修整痕迹 ↗</a></article>
<article><span class="chapter-number">03</span><h3>从寺院走进博物馆</h3><p>有些来源只能追溯到近代市场。卢芹斋经手过纳尔逊馆的南海观音；山中商会则出现在沃尔特斯佛像的记录中。每条线索都落实到具体作品。</p><a href="#object-238">看山中商会经手的佛坐像 ↗</a></article></div></section>
<div class="wrap">{material_nav()}</div>
{collection_markup(objects)}
<aside class="editorial-note wrap"><h2>关于这一辑</h2><p>照片均为Merton在博物馆参观时拍摄。藏品名称、年代、材质和编号根据对应展签整理；涉及收藏流转的补充资料附有馆方或研究文献链接。展签与线上记录存在差异时，保留说明。“水月与自在坐”是本页的比较视角，并不意味着组内每件作品都被馆方命名为水月观音。</p><p>作品下的观看提示描述照片中可见的细节；更早的寺院来源、未获证实的商人关系，不作推定。照片中的展厅布置记录的是参观时的状态。</p><p class="source">首辑整理：2026年9月 · 持续补充</p></aside>
</main><footer class="site-footer wrap"><a href="../">← 返回博物馆首页</a><span>Merton · 博物馆札记</span><a href="#top">回到顶部 ↑</a></footer>
{lightbox}
</body></html>'''
(PAGE/'index.html').write_text(html)
painting_data = json.loads((ROOT/'museum-notes/chinese-painting/data/works.json').read_text())
painting_count = sum(w['unit']=='scrolls' for w in painting_data['works'])
buddhist_painting_count = sum(w['unit']!='scrolls' for w in painting_data['works'])
dunhuang_count = sum(w['unit']=='dunhuang' for w in painting_data['works'])
category_cards = ''.join(f'<a class="material-entry" href="../{key}/"><span class="eyebrow">{sum(o["material_group"]==key for o in objects):02d} 件造像</span><h3>{name} <span aria-hidden="true">↗</span></h3><p>{description}</p></a>' for key,name,description in materials)
CHINESE = ROOT/'museum-notes'/'chinese-buddhist-art'
CHINESE.mkdir(exist_ok=True)
(CHINESE/'index.html').write_text(f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>中国佛教艺术 · 博物馆札记 | Merton</title><meta name="description" content="Merton的博物馆参观照片与藏品札记。按材质浏览中国佛教造像，也循专题比较不同展厅里的作品。"><link rel="stylesheet" href="../museum.css"></head><body>
<header class="site-header"><a class="signature" href="../">Merton</a><a href="../">博物馆札记 ↗</a></header><main class="wrap notebook-index"><p class="eyebrow">MUSEUM NOTES / CHINESE BUDDHIST ART</p><h1>中国佛教艺术</h1><p class="index-intro">造像、经卷与绘画，<br>把不同博物馆里的作品慢慢放在一起。</p>
<section class="material-directory" aria-labelledby="materials-title"><p class="eyebrow">BROWSE BY MATERIAL</p><h2 id="materials-title">从材料开始</h2><p class="directory-intro">先从中国佛教造像整理起。按主要结构与工艺归类，每件作品保留展签上的完整材料说明。</p><div class="material-grid">{category_cards}</div><a class="text-link" href="../buddhist-sculpture/#collection">浏览全部 {len(objects)} 件造像 →</a></section>
<section class="material-directory" aria-labelledby="paintings-title"><p class="eyebrow">BUDDHIST PAINTING</p><h2 id="paintings-title">佛教绘画</h2><p class="directory-intro">壁画、卷轴与幡画，按原来的形制和使用环境整理。</p><div class="material-grid"><a class="material-entry" href="../dunhuang-painting/"><span class="eyebrow">{dunhuang_count} 件作品</span><h3>敦煌绘画 ↗</h3><p>吉美与弗利尔的供养画、菩萨幡和地藏像。</p></a><a class="material-entry" href="../buddhist-painting/#murals"><span class="eyebrow">寺院中的画</span><h3>寺院壁画 ↗</h3><p>广胜寺、慈胜寺与河南的壁画。</p></a><a class="material-entry" href="../buddhist-painting/#buddhist-scrolls"><span class="eyebrow">卷轴中的佛教形象</span><h3>罗汉 ↗</h3><p>从两幅元至明初的罗汉画开始。</p></a></div><a class="text-link" href="../buddhist-painting/">浏览全部 {buddhist_painting_count} 件佛教绘画 →</a></section>
<section class="topic-directory" aria-labelledby="topics-title"><p class="eyebrow">READ BY THEME</p><h2 id="topics-title">循着一个问题看</h2><a class="issue-link" href="../buddhist-sculpture/"><img src="../buddhist-sculpture/images/nelson-215.jpg" alt="彩绘木雕南海观音" width="1279" height="1706"><div><p class="eyebrow">001 / 中国佛教造像</p><h2>自在之姿</h2><p>从水月观音出发，观看木雕、石雕、铜像与漆塑中的姿态、色彩和时间。</p><p class="issue-meta">{len(objects)} 件造像 · {len(museums)} 家博物馆的相遇</p><span class="text-link">阅读这一辑 →</span></div></a><p class="featured-note"><a href="../buddhist-sculpture/#object-263">延伸阅读：藏在观音腹中的《佛说生天经》 →</a></p></section></main><footer class="site-footer wrap"><a href="../">← 返回博物馆札记</a><span>摄影 / Merton</span></footer></body></html>''')

for key,name,description in materials:
    selection = [o for o in objects if o['material_group']==key]
    directory = ROOT/'museum-notes'/key
    directory.mkdir(exist_ok=True)
    directory.joinpath('index.html').write_text(f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{name} · 博物馆札记 | Merton</title><meta name="description" content="{e(description)} Merton拍摄的{len(selection)}件佛教造像。"><link rel="stylesheet" href="../museum.css"><script src="../museum.js" defer></script></head>
<body id="top"><a class="skip-link" href="#collection">跳至藏品</a><header class="site-header"><a class="signature" href="../">Merton</a><nav aria-label="主导航"><a href="../chinese-buddhist-art/">中国佛教艺术</a><a href="../buddhist-sculpture/">自在之姿专题</a></nav></header>
<main><nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>{name}</span></nav><section class="category-header wrap"><p class="eyebrow">MUSEUM NOTES / MATERIAL</p><h1>{name}</h1><p class="index-intro">{description}</p><p class="category-count">{len(selection)} 件造像 · 持续补充</p>{material_nav(active=key)}</section>
{collection_markup(selection, '../buddhist-sculpture/images/')}
<aside class="editorial-note wrap"><h2>材料与归类</h2><p>彩绘、贴金与髹漆属于表面处理时，作品仍按主要结构归类。夹纻干漆与其他漆塑单列；多种材料共同成形的作品另列“复合材料”。具体工艺以每件作品的展签和札记为准。</p><p>同一件作品也可以出现在专题中。馆名记录参观地点，借展作品另注所属收藏。</p></aside></main><footer class="site-footer wrap"><a href="../chinese-buddhist-art/">← 返回中国佛教艺术</a><span>摄影 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{lightbox}</body></html>''')
print(f'Generated notebook, collection ({len(objects)} objects), and {len(materials)} material pages.')

sections = json.loads((ROOT/'museum-notes'/'sections.json').read_text())

caravaggio_data = json.loads((ROOT/'museum-notes/caravaggio/data/works.json').read_text())
caravaggio_count = len(caravaggio_data['works'])
caravaggio_photos = len(caravaggio_data['photos'])
leonardo_data = json.loads((ROOT/'museum-notes/leonardo/data/works.json').read_text())
europe_count = caravaggio_count + len(leonardo_data['works'])
europe_photos = caravaggio_photos + len(leonardo_data['photos'])

future = ''.join(f'<li><h3>{e(section["title"])}</h3><p>{e(section["description"])}</p></li>' for section in sections['planned'])
(ROOT/'museum-notes'/'index.html').write_text(f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>博物馆札记 | Merton</title><meta name="description" content="Merton的博物馆照片、作品资料与观看札记。从中国佛教艺术开始，逐步走向不同地区、时代与艺术传统。"><link rel="stylesheet" href="museum.css"></head><body>
<header class="site-header"><a class="signature" href="./">Merton</a><a href="./">博物馆首页</a></header>
<main class="wrap notebook-index"><p class="eyebrow">MUSEUM NOTES</p><h1>博物馆札记</h1><p class="index-intro">把看过的作品留下来，<br>也为重看时的新发现留一点空白。</p>
<section aria-labelledby="current-title"><p class="eyebrow">EXPLORE THE COLLECTIONS</p><h2 id="current-title">正在整理</h2><a class="issue-link" href="chinese-buddhist-art/"><img src="buddhist-sculpture/images/nelson-215.jpg" alt="纳尔逊－阿特金斯艺术博物馆的南海观音木雕" width="1279" height="1706"><div><p class="eyebrow">CHINESE BUDDHIST ART</p><h2>中国佛教艺术</h2><p>从观音木雕与像内经卷，继续看到寺院壁画、敦煌绘画与罗汉图。</p><p class="issue-meta">{len(objects)} 件造像 · {buddhist_painting_count} 件绘画<br>造像 / 经卷 / 寺院壁画 / 敦煌绘画</p><span class="text-link">进入这个板块 →</span></div></a><a class="issue-link" href="chinese-painting/"><img src="chinese-painting/images/nelson-310.jpg" alt="传李成《晴峦萧寺图》" width="1280" height="1707" loading="lazy"><div><p class="eyebrow">CHINESE PAINTING &amp; CALLIGRAPHY</p><h2>中国书画</h2><p>从《晴峦萧寺图》与《后赤壁赋图》看起，再看人物、耕织与竹石。</p><p class="issue-meta">{painting_count} 件作品 · 按时代浏览<br>山水 / 人物叙事 / 文人画</p><span class="text-link">进入这个板块 →</span></div></a><a class="issue-link" href="european-painting/"><img src="caravaggio/images/caravaggio-470.jpg" alt="卡拉瓦乔《纸牌作弊者》，金贝尔艺术博物馆" width="1707" height="1280" loading="lazy"><div><p class="eyebrow">EUROPEAN PAINTING</p><h2>欧洲绘画</h2><p>从达·芬奇到卡拉瓦乔，把不同城市里看过的画放到一起。</p><p class="issue-meta">达·芬奇 / 卡拉瓦乔 · {europe_count} 件作品（含合作、工作室及归属讨论）<br>{europe_photos} 张参观照片 / 收藏故事 / 并排看画</p><span class="text-link">进入这个板块 →</span></div></a></section>
<section class="future-collections" aria-labelledby="future-title"><p class="eyebrow">FURTHER JOURNEYS</p><h2 id="future-title">以后慢慢展开</h2><p class="directory-intro">还有一些旅途中的相遇，等待照片与记忆归位。</p><ul class="future-grid">{future}</ul><p class="directory-intro">也会循着专题回看：例如健陀罗与马图拉的早期佛像，以及不同地区的艺术交流。</p></section>
<aside class="notebook-about"><h2>资料之外，也留下观看</h2><p>一件作品的年代、材料与流转，可以慢慢查证；个人的观看，也容得下零碎的记忆与后来重看的感受。</p><p>有些印象来自展厅，有些在重看照片时才浮现。能记起多少，就留下多少。</p></aside>
</main><footer class="site-footer wrap"><a href="./">← 返回博物馆首页</a><span>摄影 / Merton</span></footer></body></html>''')
