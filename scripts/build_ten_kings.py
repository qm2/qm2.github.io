"""Build the Ten Kings notebook from edited records and selected local derivatives.

No archive access, downloads or image uploads are performed by the site build.
"""
from pathlib import Path
from html import escape as esc
import json
import re
from build_homer import LIGHTBOX

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'museum-notes/ten-kings'
URL = '/museum-notes/ten-kings/'


def build():
    load = lambda n: json.loads((BASE / 'data' / f'{n}.json').read_text())
    works, photos, sources, editorial = [load(n) for n in ['works', 'photos', 'sources', 'editorial']]
    by = {w['id']: w for w in works}
    sb = {s['id']: s for s in sources}
    kings = [w for w in works if w['category'] == 'king']
    paintings = [w for w in works if w['category'] == 'painting']
    objects = [w for w in works if w['category'] == 'object']
    central = by['ksitigarbha_cma']
    comparisons = load('comparisons')

    def href(w):
        if w['category'] == 'king': return URL + w['id'] + '/'
        if w['category'] == 'central': return URL + 'ksitigarbha/'
        if w['category'] == 'context': return URL + w['id'] + '/'
        return URL + ('paintings/' if w['category'] == 'painting' else 'objects/') + '#' + w['id']

    def text(s, w=None):
        def cite(m):
            key = m[1]
            if key == 'label':
                assert w
                return f'<a class="tk-cite" href="#label-{w["id"]}" aria-label="查看{esc(w["name"])}现场展签">[展签]</a>'
            assert key in sb, key
            return f'<a class="tk-cite" href="{URL}sources/#{key}" title="{esc(sb[key]["title"])}">[{int(key[1:])}]</a>'
        return re.sub(r'\[(S\d+|label)\]', cite, esc(s))

    def paras(s, w=None):
        return ''.join('<p>' + text(p, w) + '</p>' for p in (s if isinstance(s, list) else [s]))

    def image(n, caption, eager=False, small=False):
        p = photos[str(n)]
        vs = p['variants']
        ss = ', '.join(f'{URL}{v["path"]} {v["width"]}w' for v in vs)
        sizes = '(max-width: 600px) 44vw, (max-width: 950px) 28vw, 230px' if small else '(max-width: 700px) calc(100vw - 36px), 700px'
        if str(n) == 'hero': sizes = '(max-width: 650px) calc(100vw - 36px), (max-width: 1296px) calc(100vw - 96px), 1200px'
        return (f'<img src="{URL}{vs[min(1, len(vs)-1)]["path"]}" srcset="{ss}" '
                f'sizes="{sizes}" '
                f'width="{p["width"]}" height="{p["height"]}" alt="{esc(caption)}" '
                f'{"fetchpriority=high" if eager else "loading=lazy"} decoding="async">')

    def figure(n, caption, eager=False, cls='', context=''):
        p = photos[str(n)]
        label = context + caption
        return (f'<figure class="tk-figure {cls}"><a data-photo href="{URL}{p["full"]}" '
                f'data-caption="{esc(label)}">{image(n, label, eager)}</a><figcaption>{esc(caption)}</figcaption></figure>')

    def caption(w):
        return f'{w["name"]} · {w["owner"]}' + (f' · {w["accession"]}' if w['accession'] else '') + '｜Merton摄于CMA，2026年11月'

    def mini(w, big=False):
        return (f'<a class="tk-mini" href="{href(w)}">{image(w.get("card_photo", w["full"]), caption(w), small=True)}'
                f'<h3>{esc(w["name"])}</h3><p>{esc(w["subtitle"] if big else w["owner"])}</p></a>')

    def gallery():
        return '<nav class="tk-kings" aria-label="十王长廊：按第一至第十王进入细读">' + ''.join(mini(w, True) for w in kings) + '</nav>'

    def heading(title, sub='', eyebrow='TEN KINGS / GORYEO PAINTING'):
        return f'<header class="tk-heading"><p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(title)}</h1>' + (f'<p class="tk-deck">{esc(sub)}</p>' if sub else '') + '</header>'

    def shell(title, body, slug='', cover=2):
        canon = 'https://qm2.github.io' + URL + (slug + '/' if slug else '')
        og = 'https://qm2.github.io' + URL + photos[str(cover)]['full']
        description = '在克利夫兰重看十王与地藏：2026年11月13—14日现场摄影、完整画幅与细节札记。'
        crumb = f'<a href="{URL}">十王与救赎</a><span>/</span><span>{esc(title)}</span>' if slug else '<span>十王与救赎</span>'
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Merton</title><meta name="description" content="{description}"><link rel="canonical" href="{canon}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{description}"><meta property="og:url" content="{canon}"><meta property="og:type" content="article"><meta property="og:image" content="{og}"><link rel="stylesheet" href="/museum-notes/museum.css"><link rel="stylesheet" href="/museum-notes/caravaggio/caravaggio.css"><link rel="stylesheet" href="{URL}ten-kings.css"><script src="/museum-notes/caravaggio/caravaggio.js" defer></script><script src="{URL}ten-kings.js" defer></script></head><body class="tk-page" id="top"><a class="skip-link" href="#main">跳至正文</a><header class="site-header"><a class="signature" href="/museum-notes/">Merton</a><nav aria-label="专题导航"><a href="{URL}">十王与救赎</a><a href="{URL}overview/">十王长廊</a><a href="{URL}ksitigarbha/">地藏</a><a href="{URL}paintings/">高丽佛画</a><a href="{URL}sources/">资料</a></nav></header><main class="wrap" id="main"><nav class="breadcrumbs" aria-label="当前位置"><a href="/museum-notes/">博物馆札记</a><span>/</span>{crumb}</nav>{body}</main><footer class="site-footer wrap"><a href="/museum-notes/">← 博物馆札记</a><span>现场摄影与札记 / Merton</span><a href="#top">回到顶部 ↑</a></footer>{LIGHTBOX}</body></html>'''

    def write(slug, title, body, cover=2):
        p = BASE / slug if slug else BASE
        p.mkdir(parents=True, exist_ok=True)
        (p / 'index.html').write_text(shell(title, body, slug, cover))

    def facts(w):
        fields = [('原名', w['english']), ('年代', w['date']), ('材料', w['material']), ('收藏', w['owner']), ('编号', w['accession'] or '现场展签未载')]
        if w.get('dimensions'): fields.append(('尺寸', w['dimensions']))
        fields.append(('所见', '克利夫兰艺术博物馆，2026年11月13—14日'))
        return '<dl class="tk-facts">' + ''.join(f'<div><dt>{k}</dt><dd>{esc(v)}</dd></div>' for k, v in fields) + '</dl>'

    def label(w):
        return (f'<details class="tk-label" id="label-{w["id"]}"><summary>现场展签与作品资料 <i aria-hidden="true">＋</i></summary>'
                + facts(w) + figure(w['label'], w['name'] + ' · CMA现场展签，Merton摄') + '</details>')

    def sections(w):
        s = ''
        illustrated = 0
        for i, block in enumerate(w['sections'], 1):
            copy = '<div class="tk-copy"><h2>' + esc(block['title']) + '</h2>' + paras(block['text'], w) + '</div>'
            if 'photo' in block:
                illustrated += 1
                reverse = ' tk-detail-reverse' if illustrated % 2 == 0 else ''
                s += f'<section class="tk-detail compare-group{reverse}" id="reading-{w["id"]}-{i}">' + figure(block['photo'], block['caption'], context=caption(w) + ' · ') + copy + '</section>'
            else:
                s += f'<section class="tk-prose tk-text-section" id="reading-{w["id"]}-{i}">' + copy + '</section>'
        return s

    def reference_note(w):
        return '<p class="tk-source">画面情节与图像解释据本件<a href="#label-' + w['id'] + '">现场展签</a>；照片观察与个人感受另在正文中表述。' + ''.join(text('['+s+']') for s in w['sources']) + '</p>'

    # Home: quiet editorial sequence, full-view previews rather than cropped artwork cards.
    hero = photos['hero']
    complete = photos['2']
    hero_html = f'<figure class="tk-figure tk-hero"><a data-photo href="{URL}{complete["full"]}" data-caption="十王与中央地藏的展厅陈列 · 克利夫兰艺术博物馆 · Merton摄，2026年11月"><picture><source media="(max-width: 600px)" srcset="' + ', '.join(f'{URL}{v["path"]} {v["width"]}w' for v in complete['variants']) + '">' + image('hero', '十王与中央地藏的展厅陈列，CMA，Merton现场摄影', True) + '</picture></a><figcaption>十王与中央地藏的展厅陈列 · 克利夫兰艺术博物馆 · Merton摄，2026年11月</figcaption></figure>'
    body = heading(editorial['title'], editorial['subtitle']) + hero_html
    body += '<div class="tk-prose tk-intro">' + paras(editorial['intro']) + '<p class="tk-source">亲见：2026年11月13—14日<br>Ten Kings of Hell: The Afterlife in Medieval Korea<br>展期：2026年10月11日—2027年1月3日 · CMA与韩国国立中央博物馆合作。[2]</p></div>'
    body = body.replace('合作。[2]', '合作。' + text('[S02]'))
    body += '<nav class="tk-localnav" aria-label="本页目录"><a href="#reunion">十王重聚</a><a href="#kings">十王长廊</a><a href="#dunhuang">敦煌与高丽</a><a href="#central">地藏</a><a href="#paintings">其他佛画</a><a href="#objects">画外之物</a></nav>'
    body += '<section class="tk-section" id="reunion"><div class="tk-prose"><p class="eyebrow">01 / REUNITED</p><h2>分散各地的十幅画</h2>' + paras(editorial['reunion']) + f'<a class="text-link" href="{URL}overview/#reunion">从旧藏到重聚 →</a></div></section>'
    body += '<section class="tk-section" id="kings"><p class="eyebrow">02 / THE TEN COURTS</p><h2>十王长廊</h2><p class="tk-prose tk-left">' + esc(editorial['gallery_intro']) + '</p>' + gallery() + f'<p class="tk-source">基本断代依本展展签；<a href="{URL}overview/#attribution">研究与归属中的开放问题</a>。</p></section>'
    body += '<section class="tk-section tk-feature" id="dunhuang">' + figure(98, '敦煌《十王经图卷》局部 · 大英博物馆 1919,0101,0.80 · Merton摄于CMA') + '<div><p class="eyebrow">BETWEEN THE COURTS</p><h2>从敦煌到高丽</h2><p>十世纪的长卷把法庭、转生道路与地藏串在一起。与十幅高丽竖轴并看，哪些图像语汇延续了，观看的方式又怎样变化？</p>' + f'<a class="text-link" href="{URL}dunhuang/">展开敦煌十王卷 →</a></div></section>'
    body += '<section class="tk-section tk-feature" id="central">' + figure(91, caption(central)) + '<div><p class="eyebrow">03 / KṢITIGARBHA</p><h2>地藏，审判之外</h2>' + paras(editorial['central_intro']) + '<p>面容、锡杖、宝珠与袈裟上的金线——从完整画幅走向它的细密处。</p>' + f'<a class="text-link" href="{URL}ksitigarbha/">读这幅地藏 →</a><p><a class="text-link" href="{URL}ksitigarbha/#leeum-amitabha-national-treasure-218">并看：在华盛顿遇见的阿弥陀三尊 →</a></p></div></section>'
    body += '<section class="tk-section" id="paintings"><p class="eyebrow">04 / OTHER WORLDS</p><h2>高丽佛画的其他世界</h2><p>' + esc(editorial['other_intro']) + '</p><div class="tk-paintings">' + ''.join(mini(w) for w in paintings) + '</div></section>'
    body += '<section class="tk-section tk-feature tk-objects-entry" id="objects">' + figure(379, '《大方广佛华严经》卷七十八 · 卷首画局部 · CMA 1994.25 · Merton摄') + '<div><p class="eyebrow">05 / BEYOND THE PAINTINGS</p><h2>画外之物</h2>' + paras(editorial['objects_intro']) + f'<a class="text-link" href="{URL}objects/">经卷、供养与青瓷 →</a></div></section>'
    body += '<section class="tk-prose tk-closing"><h2>从克利夫兰归来</h2>' + paras(editorial['closing']) + f'<p><a href="{URL}sources/">资料、归属与摄影说明 →</a></p></section>'
    write('', editorial['title'], body)

    body = heading('十王图总览', '审判的十个时刻') + gallery()
    body += f'<aside class="tk-related"><h2>从敦煌到高丽：十王图像的传播与变化</h2><p>从纸本长卷到绢本竖轴，沿着案几、亡者与轮回道路逐段并看。</p><a href="{URL}dunhuang/">读敦煌《十王经图卷》 →</a></aside>'
    body += '<div class="tk-overview">' + ''.join('<section class="tk-prose tk-text-section"><h2>' + esc(s['title']) + '</h2>' + paras(s['text']) + '</section>' for s in editorial['overview_sections']) + '</div>'
    body += '<section class="tk-section" id="reunion"><h2>谁让它们再次相遇？</h2><ol class="tk-timeline">' + ''.join('<li><h3>' + esc(s['date']) + '</h3>' + paras(s['text']) + '</li>' for s in editorial['timeline']) + '</ol></section>'
    body += '<details class="tk-record-table"><summary>今日馆藏一览 <i aria-hidden="true">＋</i></summary><div class="tk-table-scroll" tabindex="0" role="region" aria-label="十王馆藏表，可横向滚动"><table><thead><tr><th>王次与名称</th><th>收藏机构</th><th>编号</th></tr></thead><tbody>' + ''.join(f'<tr><th scope="row"><a href="{href(w)}">{esc(w["name"])}</a></th><td>{esc(w["owner"])}</td><td>{esc(w["accession"])}</td></tr>' for w in kings) + '</tbody></table></div></details>'
    body += '<details class="tk-research" id="attribution"><summary>研究与归属：仍然开放的问题 <i aria-hidden="true">＋</i></summary><div class="tk-prose">' + paras(editorial['dispute']) + '</div></details>'
    body += f'<p class="tk-source">比较资料与本套画分别处理：韩国国立中央博物馆2011年的说明用于追荐背景，不把其中太古寺画组的故事、馆号或收藏史移入本套。<a href="{URL}sources/">完整资料 →</a></p>'
    write('overview', '十王图总览', body)

    w = by['dunhuang']
    body = heading(w['subtitle'], '敦煌《十王经图卷》 · 10世纪 · 大英博物馆', 'DUNHUANG / CONTEXT') + '<p class="tk-lead">' + esc(w['lead']) + '</p>'
    body += figure(w['full'], '现场完整陈列视角：现存残卷在展柜中展开，近大远小的透视予以保留 · Merton摄于CMA', True, 'tk-full')
    body += sections(w) + label(w)
    body += f'<aside class="tk-related"><h2>回到高丽画组</h2><p><a href="{URL}k05/">第五王：证据怎样成为画面 →</a></p><p><a href="{URL}k10/">第十王：另一种轮回道路 →</a></p><p><a href="{URL}ksitigarbha/">中央地藏：卷尾救拔与独立尊像 →</a></p><p><a href="{URL}overview/">返回十王总览 →</a></p></aside>'
    write('dunhuang', w['subtitle'], body, 98)

    for i, w in enumerate(kings):
        body = heading(w['name'], w['subtitle'], 'THE TEN KINGS / ' + str(i+1).zfill(2))
        body += '<p class="tk-lead">' + esc(w['lead']) + '</p>' + figure(w['full'], caption(w), True, 'tk-full')
        body += '<p class="tk-source tk-center">' + esc(w['date'] + ' · ' + w['material']) + '</p>' + sections(w)
        body += reference_note(w) + label(w)
        body += f'<p class="tk-source">本件属前Packard旧藏十王组。<a href="{URL}overview/#reunion">整组流传与重聚</a> · <a href="{URL}overview/#attribution">归属讨论</a></p>'
        body += '<nav class="tk-next" aria-label="逐王阅读">' + (f'<a href="{href(kings[i-1])}">← {esc(kings[i-1]["name"])}</a>' if i else f'<a href="{URL}overview/">← 十王总览</a>') + f'<a href="{URL}#kings">返回长廊</a>' + (f'<a href="{href(kings[i+1])}">{esc(kings[i+1]["name"])} →</a>' if i < 9 else f'<a href="{URL}ksitigarbha/">再看地藏 →</a>') + '</nav>'
        write(w['id'], w['name'] + '｜' + w['subtitle'], body, w['full'])

    body = heading('地藏：审判之外的慈悲', '地藏菩萨立像 · 1300—1350年 · CMA 2025.141') + '<p class="tk-lead">' + esc(central['lead']) + '</p>' + figure(91, caption(central), True, 'tk-full')
    body += '<nav class="tk-localnav" aria-label="地藏细读目录"><a href="#reading-ksitigarbha_cma-1">面容与持物</a><a href="#reading-ksitigarbha_cma-3">金彩衣纹</a><a href="#reading-ksitigarbha_cma-5">青龍公用</a><a href="#reading-ksitigarbha_cma-6">流传</a><a href="#leeum-amitabha-national-treasure-218">阿弥陀三尊并看</a></nav>' + sections(central) + label(central)
    if central.get('research_notes'):
        body += '<details class="tk-research"><summary>研究资料中的待核问题 <i aria-hidden="true">＋</i></summary><div class="tk-prose">' + paras(central['research_notes']) + '</div></details>'
    for c in comparisons:
        body += f'<section class="tk-section" id="{c["id"]}"><div class="tk-prose"><p class="eyebrow">COMPARISON / A RETURN ENCOUNTER</p><h2>{esc(c["name"])}：救拔与接引</h2><p class="tk-source">{esc(c["english"])} · {esc(c["date"])}<br>{esc(c["owner"])} · {esc(c["designation"])}</p>' + paras(c['lead']) + '</div>'
        if c.get('full'):
            body += figure(c['full'], c['name'] + ' · Leeum收藏 · Merton摄于华盛顿国家亚洲艺术博物馆；CMA仅以数字影像展示', cls='tk-full')
        for block in c['sections']:
            body += '<div class="tk-prose tk-text-section"><h3>' + esc(block['title']) + '</h3>' + paras(block['text']) + '</div>'
        body += f'<details class="tk-research" id="label-{c["id"]}"><summary>展签、解释与观看记录 <i aria-hidden="true">＋</i></summary><div class="tk-prose"><p>{esc(c["material"])} · {esc(c["dimensions"])}</p>' + paras(c['notes']) + '</div>'
        if c.get('label'):
            body += figure(c['label'], '华盛顿现场展牌：下半部对应本件《阿弥陀三尊图》，上半部为另一幅《地藏菩萨与眷属图》 · Merton摄', cls='tk-full')
        body += '</details></section>'
    body += f'<aside class="tk-related"><h2>同一种救拔，不同的形象</h2><p><a href="{URL}paintings/#leeum_ksitigarbha_entourage">Leeum地藏与眷属：一群人的护持 →</a></p><p><a href="{URL}paintings/#freer_ksitigarbha">另看国家亚洲艺术博物馆藏地藏 S1992.11 →</a></p><p><a href="{URL}k10/">第十王：从六道去向回看救度 →</a></p><p><a href="{URL}dunhuang/">敦煌卷尾的地藏 →</a></p></aside>'
    write('ksitigarbha', '地藏：审判之外的慈悲', body, 91)

    for category, title, intro, records in [('paintings', '高丽佛画的其他世界', editorial['other_intro'], paintings), ('objects', '画外之物', editorial['objects_intro'], objects)]:
        body = heading(title, intro, 'GORYEO / ' + ('PAINTINGS' if category == 'paintings' else 'TEXTS & OBJECTS'))
        body += '<nav class="tk-localnav" aria-label="作品目录">' + ''.join(f'<a href="#{w["id"]}">{esc(w["name"])}</a>' for w in records) + '</nav>'
        for w in records:
            body += f'<article class="tk-record" id="{w["id"]}"><header><p class="eyebrow">{esc(w["english"])}</p><h2>{esc(w["name"])}</h2><p class="tk-source">{esc(w["date"])}</p></header>'
            if category == 'paintings':
                body += figure(w['full'], caption(w), cls='tk-full') + '<div class="tk-prose tk-text-section">' + paras(w['lead'], w) + '</div>'
            else:
                body += '<div class="tk-feature">' + figure(w['full'], caption(w)) + '<div>' + paras(w['lead'], w) + '<p class="tk-source">基本资料与用途解释据本件<a href="#label-' + w['id'] + '">现场展签</a>。</p>' + facts(w) + '</div></div>'
            body += sections(w)
            if w['id'] == 'avatamsaka-78': body += figure(379, '《大方广佛华严经》卷七十八 · 卷首画局部 · Merton摄', cls='tk-full')
            if w.get('note'): body += '<aside class="tk-note">' + paras(w['note'], w) + '</aside>'
            if w['id'] == 'leeum_amitabha_kshitigarbha_avalok':
                body += f'<p class="tk-prose"><a href="{URL}ksitigarbha/#leeum-amitabha-national-treasure-218">并看：华盛顿亲见的另一幅国宝《阿弥陀三尊图》 →</a></p>'
            if w['id'] == 'leeum_ksitigarbha_entourage':
                body += f'<p class="tk-prose"><a href="{URL}ksitigarbha/">回到CMA中央地藏立像 →</a></p>'
            body += label(w) + '</article>'
        if category == 'paintings': body += f'<p><a href="{URL}ksitigarbha/">返回中央地藏细读 →</a> · <a href="{URL}objects/">再看经卷与器物 →</a></p>'
        write(category, title, body, records[0]['full'])

    body = heading('资料与来源', '现场展签、已读馆录与尚待继续追索的问题', 'SOURCES / RESEARCH')
    body += '<div class="tk-prose"><p>CMA展出作品的信息首先依据2026年11月13—14日的现场展签，再与馆方公开记录对照。另收录此前在华盛顿亲见的国宝《阿弥陀三尊图》作为比较，摄影地点与本次数字影像展示分别注明。正文中的“展签”链接可直接打开相应照片；数字注号指向下列资料。所有公开作品图与局部均为Merton现场摄影，图像不代表实物等比例。</p></div><ol class="tk-sources">'
    body += ''.join(f'<li id="{s["id"]}" value="{int(s["id"][1:])}"><a href="{esc(s["url"], quote=True)}" target="_blank" rel="noopener">{esc(s["title"])} ↗</a><p>{esc(s["read_status"])}</p></li>' for s in sources) + '</ol>'
    body += '<details class="tk-research"><summary>进一步阅读：已知书目，尚未阅读全文 <i aria-hidden="true">＋</i></summary>' + paras(editorial['unread']) + '</details>'
    body += '<section class="tk-prose tk-text-section"><h2>摄影与记录</h2><p>现场摄影用于个人非商业观展札记，未引入馆方高清图、红外图或图录书页。原作收藏机构分别列在图注与资料中；借展到CMA并不改变收藏归属。现场玻璃反光、绢面折痕与原有损伤均予保留。</p><p>已查阅CMA现行摄影政策；其对本馆公版藏品的开放规定，并非所有借展作品的统一授权声明。本站摄影不标作馆方CC0图像，也不提供整套原始档案下载。[S14]</p><p>其余尚待核实的问题，包括十王的具体原寺院、争议中的材料检测依据、部分绘画的断代差异，以及中央地藏题字所指的人物。资料核对日期：2026年11月17日。</p></section>'
    body = body.replace('[S14]', text('[S14]'))
    body += f'<p><a href="{URL}overview/#attribution">十王的归属讨论 →</a> · <a href="{URL}">返回专题首页 →</a></p>'
    write('sources', '资料与来源', body)

    # Idempotent integration into existing generators' output, not a second works database.
    home = ROOT / 'museum-notes/index.html'
    html = re.sub(r'<!-- ten-kings-home -->.*?<!-- /ten-kings-home -->', '', home.read_text(), flags=re.S)
    entry = '<!-- ten-kings-home --><a class="issue-link" href="ten-kings/">' + image(92, '地藏菩萨的面容与金彩 · 十王与救赎 · Merton摄') + '<div><p class="eyebrow">GORYEO BUDDHIST PAINTING</p><h2>十王与救赎</h2><p>高丽佛画中的彼岸世界。从十王的法庭，走向中央地藏的宁静，留下克利夫兰两天所见的金线与祈愿。</p><p class="issue-meta">十王独立细读 · 地藏重点篇<br>敦煌长卷并看 · 经卷与器物</p><span class="text-link">进入这一辑 →</span></div></a><!-- /ten-kings-home -->'
    anchor = '<a class="issue-link" href="japanese-art/">'
    assert anchor in html
    home.write_text(html.replace(anchor, entry + anchor, 1))
    for rel in ['japanese-zen/index.html', 'xuzhou/index.html']:
        p = ROOT / 'museum-notes' / rel
        html = re.sub(r'<!-- ten-kings-related -->.*?<!-- /ten-kings-related -->', '', p.read_text(), flags=re.S)
        entry = f'<aside class="editorial-note"><h2>在别处继续看</h2><p>高丽佛画中的审判、救拔与净土祈愿：<a href="{URL}">十王与救赎 →</a></p></aside>'
        p.write_text(html.replace('</main>', '<!-- ten-kings-related -->' + entry + '<!-- /ten-kings-related --></main>', 1))
    print(f'Built Ten Kings: {len(kings)} king readings, central Ksitigarbha, {len(paintings)} other paintings, Dunhuang context, {len(objects)} object groups; 17 pages.')


if __name__ == '__main__':
    build()
