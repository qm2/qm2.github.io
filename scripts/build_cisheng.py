"""Cisheng mural notebook, referencing canonical Chinese painting records."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]

def build():
    from build_paintings import frame, picture, card, asset
    target=ROOT/'museum-notes/cisheng-murals'
    data=json.loads((target/'data/topic.json').read_text())
    works={w['id']:w for w in json.loads((ROOT/'museum-notes/chinese-painting/data/works.json').read_text())['works']}
    def sources(items):
        return '<p class="source">'+' · '.join(f'<a href="{e(x["url"])}" target="_blank" rel="noopener noreferrer">{e(x["name"])}</a>' for x in items)+'</p>'
    def shell(title,body,compare=False):
        page=frame(title,body,description=data['intro'],sibling=True)
        if compare:
            page=page.replace('href="../museum.css"','href="../../museum.css"').replace('href="../chinese-painting/painting.css"','href="../../chinese-painting/painting.css"').replace('src="../chinese-painting/painting.js"','src="../../chinese-painting/painting.js"')
            page=page.replace('class="signature" href="../"','class="signature" href="../../"').replace('<a href="../">博物馆首页','<a href="../../">博物馆首页').replace('<a href="../chinese-painting/">中国书画','<a href="../../chinese-painting/">中国书画').replace('<a href="../">← 博物馆首页','<a href="../../">← 博物馆首页')
        return page.replace('</head>',f'<link rel="stylesheet" href="{"../" if compare else ""}cisheng.css"></head>')
    hero=works[data['hero']];photo=asset(hero,hero['cover'])
    body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>慈胜寺壁画</span></nav>
<header class="painting-intro wrap"><p class="eyebrow">CISHENG TEMPLE / MURAL FRAGMENTS</p><h1>慈胜寺壁画</h1><p class="subtitle">{e(data['subtitle'])}</p><div class="painting-intro-meta"><span>5 件壁画／残片（含相关作品）</span><span>3 家博物馆</span><span>摄影 / Merton</span></div><div class="painting-lead"><figure class="painting-banner"><a class="photo-open" href="../chinese-painting/images/{photo['photo']}" data-caption="如意轮观音坐像 · 纳尔逊－阿特金斯艺术博物馆">{picture(photo,'../chinese-painting/images/',hero['title'],True)}</a><figcaption>如意轮观音坐像 · 纳尔逊 52-6</figcaption></figure><div class="lead-copy"><p class="eyebrow">河南温县 / 五代壁画的线索</p><h2>先看手，再看衣纹</h2><p>{e(data['intro'])}</p><p>坐姿观音的双手收在胸前，焚香菩萨伸手揭盖、投香，普林斯顿的菩萨则端起供盘。同是供养与礼拜的画面，动作把各自的角色慢慢带出来。</p><a class="text-link" href="compare/">看叠在一起的两层壁画 →</a></div></div></header>
<nav class="period-nav wrap" aria-label="本辑目录"><a href="#nelson">纳尔逊三件</a><a href="#related">普林斯顿与吉美</a><a href="#history">寺院与流转</a><a href="../guangsheng-murals/">广胜寺壁画 →</a></nav>'''
    for group in data['groups']:
        body+=f'<section class="period-section wrap" id="{group["id"]}"><div class="period-heading"><h2>{e(group["title"])}</h2><p>{e(group["description"])}</p></div><div class="paintings-grid">'
        for wid in group['works']:
            c=card(works[wid],'../chinese-painting/')
            c=c.replace('<a class="text-link"',f'<p class="cs-card-note">{e(data["card_notes"][wid])}</p><a class="text-link"')
            body+=c
        body+='</div></section>'
    body+='<section class="editorial-note wrap cs-history" id="history"><h2>寺院与流转</h2>'
    for section in data['history']:
        body+=f'<section><h3>{e(section["title"])}</h3><p>{e(section["text"])}</p>{sources(section["sources"])}</section>'
    body+='</section><aside class="related-topics wrap"><p><a href="../guangsheng-murals/">广胜寺壁画：再看元代殿堂中的法会 →</a>　<a href="../buddhist-painting/#murals">全部寺院壁画 →</a></p></aside>'
    (target/'index.html').write_text(shell(data['title'],body))
    def panel(wid,label):
        w=works[wid];p=asset(w,w['cover']);caption=label+' · '+w['title']
        return f'<figure class="cs-panel"><a class="photo-open" href="../../chinese-painting/images/{p["photo"]}" data-caption="{e(caption)}">{picture(p,"../../chinese-painting/images/",caption)}</a><figcaption><p class="eyebrow">{label}</p><h2><a href="../../chinese-painting/{wid}/">{e(w["title"])}</a></h2><p>{e(w["accession"])} · {e(w["date"])}</p></figcaption></figure>'
    body='''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../../">博物馆札记</a><span>/</span><a href="../">慈胜寺壁画</a><span>/</span><span>两层壁画</span></nav><header class="work-heading wrap"><p class="eyebrow">TWO PAINTINGS / TWO LAYERS</p><h1>画下还有一幅观音</h1><p class="work-byline">纳尔逊 50-64A 与 50-64B</p></header><section class="wrap"><p>今天的两件展品，原来是同一块墙面上先后绘制的两层画。焚香图地仗上的破口露出了颜色，才让修复人员发现被覆盖的观音。现场展签留下的1952年工作照片，记录了分离的过程。</p><div class="cs-pair">'''
    body+=panel('cisheng-incense','后绘的上层')+panel('cisheng-guanyin','先绘的下层')
    body+='''</div></section><section class="editorial-note wrap cs-history"><h2>从手势和色块比较</h2><p>上层两人的动作聚向香炉，衣饰和飘带不断交叠；下层观音的身体则舒展成弯曲的“S”形，大块红绿之间留出更清晰的轮廓。前者的热闹来自仪式中的配合，后者更容易让人沿一条身体曲线看下去。</p><p>下层被泥灰覆盖，颜色得到保护。馆方同时注明部分区域经过修补：颜色的鲜明程度，不能单独当作判断先后的尺度。这里更直接的证据，是上下叠压的物质关系。</p><p class="record-note">下层观音的现场展签列937年，官网列约951—953年；上层焚香图列约951—953年。具体断代仍有差异，先后覆盖关系则有馆方的分离记录支持。</p>'''
    body+=sources([s for wid in ['cisheng-incense','cisheng-guanyin'] for s in works[wid]['sources']])+'</section>'
    context=next(p for p in hero['extras'] if p['number']==372)
    body+=f'''<section class="wrap cs-context"><h2>如今在展厅里</h2><figure><a class="photo-open" href="../../chinese-painting/images/{context['photo']}" data-caption="纳尔逊展厅：中央坐姿观音与两侧壁画">{picture(context,'../../chinese-painting/images/','纳尔逊展厅中的三件壁画')}</a><figcaption>中央的坐姿观音与两侧的画，在展厅中可以一起看；原先叠压的两层，也在这里各自成为一件展品。</figcaption></figure></section><nav class="work-pagination wrap"><a href="../">← 返回慈胜寺壁画</a><a href="../../guangsheng-murals/">广胜寺壁画 →</a></nav>'''
    (target/'compare').mkdir(exist_ok=True);(target/'compare/index.html').write_text(shell('慈胜寺壁画 · 画下的观音',body,True))
    home=ROOT/'museum-notes/index.html';s=home.read_text();marker='<a class="issue-link" href="chinese-painting/">';link='<p class="topic-return"><a href="cisheng-murals/">慈胜寺壁画：从焚香的手势，到画下的观音 →</a></p>'
    if link not in s:s=s.replace(marker,link+marker)
    home.write_text(s)
    print('Generated Cisheng index and layer comparison: 5 shared records, 3 museums; 1 new work.')

if __name__=='__main__':build()
