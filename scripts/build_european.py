"""Build the European painting directory. Called by either artist notebook builder."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
TOPICS=[
    dict(id='leonardo',title='达·芬奇',dates='LEONARDO DA VINCI / 1452—1519',hero='ginevra-de-benci',intro='三张女性肖像、两幅未完成的画，还有那些熟悉的手势与远山。把四家博物馆里的相遇放到一起。',note='含1件合作、1件工作室相关作品',routes='创作时期 / 收藏故事 / 四组作品比较'),
    dict(id='caravaggio',title='卡拉瓦乔',dates='CARAVAGGIO / 1571—1610',hero='cardsharps',intro='牌桌、果篮、礼拜堂。再看见那些曾经分开看过的画，以及它们之间的关系。',note='含1件归属讨论',routes='创作时期 / 收藏故事 / 七组作品比较')]
def build():
    entries=[]
    for t in TOPICS:
        d=json.loads((ROOT/f'museum-notes/{t["id"]}/data/works.json').read_text())
        w=next(w for w in d['works'] if w['id']==t['hero']); p=d['photos'][str(w['source_number'])]
        entries.append(f'<a class="issue-link" href="../{t["id"]}/"><img src="../{t["id"]}/images/{w["photo"]}" alt="{e(w["title"])} · Merton参观照片" width="{p["width"]}" height="{p["height"]}" loading="lazy"><div><p class="eyebrow">{t["dates"]}</p><h2>{t["title"]}</h2><p>{t["intro"]}</p><p class="issue-meta">{len(d["works"])}件作品（{t["note"]}） · {len(d["photos"])}张参观照片<br>{t["routes"]}</p><span class="text-link">进入这一辑 →</span></div></a>')
    base=ROOT/'museum-notes/european-painting';base.mkdir(exist_ok=True)
    (base/'index.html').write_text(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>欧洲绘画 · 博物馆札记 | Merton</title><meta name="description" content="Merton看过的欧洲绘画：达·芬奇与卡拉瓦乔。按画家整理参观照片，也比较题材、构图与收藏故事。"><link rel="stylesheet" href="../museum.css"></head><body><header class="site-header"><a class="signature" href="../">Merton</a><a href="../">博物馆札记 ↗</a></header><main class="wrap notebook-index"><p class="eyebrow">MUSEUM NOTES / EUROPEAN PAINTING</p><h1>欧洲绘画</h1><p class="index-intro">沿着一位画家，<br>把散在不同城市的相遇连起来。</p><section aria-labelledby="europe-artists"><p class="eyebrow">ARTIST NOTEBOOKS</p><h2 id="europe-artists">从画家开始</h2>{''.join(entries)}</section><aside class="notebook-about"><h2>以后慢慢展开</h2><p>这个板块会继续收录在欧洲和美国见到的绘画。可以沿着一位画家读，也可以比较同一个题材在不同年代的样子。</p></aside></main><footer class="site-footer wrap"><a href="../">← 博物馆札记</a><span>摄影 / Merton</span></footer></body></html>''')
if __name__=='__main__': build()
