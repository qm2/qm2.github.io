"""Guangsheng topic: canonical records and photographs live in chinese-painting."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]

def build():
    # Reuse the existing painting shell, cards, image viewer and canonical builder.
    from build_paintings import frame, picture, card, asset
    target=ROOT/'museum-notes/guangsheng-murals'
    data=json.loads((target/'data/topic.json').read_text())
    works={w['id']:w for w in json.loads((ROOT/'museum-notes/chinese-painting/data/works.json').read_text())['works']}
    items=[works[x['id']] for x in data['works']]
    def refs(ss):
        return '<p class="source">'+ ' · '.join(f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["name"])}</a>' for s in ss)+'</p>'
    def shell(title,body,compare=False):
        page=frame(title,body,description=data['subtitle'],sibling=True)
        if compare:
            # The compare directory is one level deeper than sibling topic pages.
            page=page.replace('href="../museum.css"','href="../../museum.css"').replace('href="../chinese-painting/painting.css"','href="../../chinese-painting/painting.css"').replace('src="../chinese-painting/painting.js"','src="../../chinese-painting/painting.js"')
            page=page.replace('class="signature" href="../"','class="signature" href="../../"').replace('<a href="../">博物馆首页','<a href="../../">博物馆首页').replace('<a href="../chinese-painting/">中国书画','<a href="../../chinese-painting/">中国书画').replace('<a href="../">← 博物馆首页','<a href="../../">← 博物馆首页')
        return page.replace('</head>',f'<link rel="stylesheet" href="{"../" if compare else ""}guangsheng.css"></head>')
    hero=asset(items[0],750)
    body=f'''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../">博物馆札记</a><span>/</span><a href="../chinese-buddhist-art/">中国佛教艺术</a><span>/</span><span>广胜寺壁画</span></nav>
<header class="painting-intro wrap"><p class="eyebrow">GUANGSHENG TEMPLE / YUAN MURALS</p><h1>广胜寺壁画</h1><p class="subtitle">{e(data['subtitle'])}</p><div class="painting-intro-meta"><span>3 件壁画／残片</span><span>2 家博物馆</span><span>元代 · 摄影 / Merton</span></div><figure class="painting-banner"><a class="photo-open" href="../chinese-painting/images/{hero['photo']}" data-caption="药师佛法会图 · 大都会艺术博物馆">{picture(hero,'../chinese-painting/images/','药师佛法会图：正面观看',True)}</a><figcaption>原广胜下寺大雄宝殿东壁 · 药师佛法会图 · 大都会艺术博物馆</figcaption></figure></header>
<nav class="period-nav wrap" aria-label="本辑目录"><a href="#works">三件作品</a><a href="#history">寺院与流转</a><a href="compare/">放在一起看 →</a></nav>
<section class="period-section wrap" id="works"><div class="period-heading"><h2>从三面墙看起</h2><p>东西两壁的法会，与南壁的一次参访。</p></div><div class="paintings-grid">'''
    for x,w in zip(data['works'],items):
        c=card(w,'../chinese-painting/')
        c=c.replace('<p class="painting-artist">',f'<p class="painting-artist">原{x["wall"]} · ')
        c=c.replace('<a class="text-link"',f'<p class="gs-card-note">{e(x["intro"])}</p><a class="text-link"')
        body+=c
    body+='</div></section><section class="editorial-note wrap gs-history" id="history"><h2>寺院与流转</h2>'
    for h in data['history']:
        body+=f'<section><h3>{e(h["title"])}</h3><p>{e(h["text"])}</p>{refs(h["sources"])}</section>'
    body+='</section><aside class="related-topics wrap"><p><a href="compare/">把东壁、西壁与南壁放在一起看 →</a>　<a href="../buddhist-painting/#murals">再看其他寺院壁画 →</a></p></aside>'
    (target/'index.html').write_text(shell('广胜寺壁画',body))
    def panel(w,n,caption):
        p=asset(w,n);alt=w['title']+' · '+caption
        return f'<figure class="gs-panel"><a class="photo-open" href="../../chinese-painting/images/{p["photo"]}" data-caption="{e(alt)}">{picture(p,"../../chinese-painting/images/",alt)}</a><figcaption><h2><a href="../../chinese-painting/{w["id"]}/">{e(w["title"])}</a></h2><p>{e(caption)}</p><p>{e(w["museum"])} · {e(w["accession"])}</p><p>{e(w["dimensions"])}</p></figcaption></figure>'
    body='''<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../../">博物馆札记</a><span>/</span><a href="../">广胜寺壁画</a><span>/</span><span>放在一起看</span></nav><header class="work-heading wrap"><p class="eyebrow">LOOKING TOGETHER</p><h1>从法会到一次相遇</h1><p class="work-byline">两面相对的大壁画，一段南壁的故事。</p></header><section class="wrap"><p>药师佛与炽盛光佛都以端坐的主尊为中心，旁侧人物层层铺开。先比较头光和身体形成的中轴，再看两边较大菩萨与外侧小人物之间的尺度变化。</p><div class="gs-pair">'''
    body+=panel(items[0],750,'原东壁 · 正面观看')+panel(items[1],375,'原西壁 · 主尊局部')
    body+='''</div><p class="source">两张照片的取景范围不同；原壁画的高度都在七米左右，宽度接近十五米。</p><p>两幅画里都有日月相关形象，但在炽盛光佛的法会中，星曜形成了一整组人格化的神祇；药师佛周围的日光、月光菩萨与十二神将，则指向另一套护佑的图像。人物身旁的标志与他们所在的位置，要结合各自的图解来读。</p></section><section class="wrap gs-small"><h2>把距离拉近：善财童子</h2><p>南壁残片高约八十厘米。这里没有占据中央的巨大佛身，带头光的善财在下方合掌，其他孩子的动作把目光带向不同方向。庄严法会之外，同一座殿堂还容纳了这样可逐段阅读的故事。</p>'''
    body+=panel(items[2],761,'原南壁 · 善财参访故事的一段')
    body+='</section><aside class="editorial-note wrap"><h2>位置与图像资料</h2>'+refs([s for w in items for s in w['sources'][:1]])+'</aside><nav class="work-pagination wrap"><a href="../">← 返回广胜寺壁画</a><a href="../../buddhist-painting/">佛教绘画 →</a></nav>'
    (target/'compare').mkdir(exist_ok=True)
    (target/'compare/index.html').write_text(shell('广胜寺壁画 · 放在一起看',body,True))
    # A quiet direct entrance on the notebook homepage, within the Buddhist section.
    home=ROOT/'museum-notes/index.html';s=home.read_text()
    marker='<a class="issue-link" href="chinese-painting/">'
    link='<p class="topic-return"><a href="guangsheng-murals/">新辑 · 广胜寺壁画：三段画面，同一座殿堂 →</a></p>'
    if link not in s:s=s.replace(marker,link+marker)
    home.write_text(s)
    print('Generated Guangsheng topic and comparison; 3 shared works, 2 museums.')

if __name__=='__main__':build()
