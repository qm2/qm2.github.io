"""Render the small map guide using Xuzhou's existing photographs and frame."""
from html import escape as e


def entry(d, photo):
    return ('<aside class="xz-map-entry" aria-label="地图导览">'
            '<a href="map/">'+photo('map-full','展厅佛教传播地图 · 进入地图导览',card=True)+'</a>'
            '<div><p class="eyebrow">A GUIDE THROUGH THE COLLECTION</p>'
            '<h3><a href="map/">山海之间</a></h3><p>'+e(d['entry'])+'</p>'
            '<a class="text-link" href="map/">展开地图导览 →</a></div></aside>')


def render(d, works, photo):
    order=list(d['sources'])
    def refs(keys):
        return ' <span class="xz-map-cites">'+''.join('<a href="#ref-'+key+'" aria-label="来源：'+e(d['sources'][key]['title'])+'">['+str(order.index(key)+1)+']</a> ' for key in keys)+'</span>'
    def figure(key):
        cap=d['photos'][key]['caption']
        return '<figure class="xz-map-photo">'+photo(key,cap,'../',eager=key=='map-full')+'<figcaption>'+e(cap)+' · 点击放大</figcaption></figure>'
    b='<nav class="breadcrumbs wrap" aria-label="当前位置"><a href="../../">博物馆札记</a><span>/</span><a href="../">虚舟收藏</a><span>/</span><span>地图导览</span></nav>'
    b+='<header class="wrap xz-work-heading xz-prose"><p class="eyebrow">MOUNTAINS / SEAS / ENCOUNTERS</p><h1>'+e(d['title'])+'</h1><p>'+e(d['intro'])+'</p><nav class="xz-nav" aria-label="交流网络">'+''.join('<a href="#'+g['id']+'">'+e(g['title'])+'</a>' for g in d['groups'])+'</nav></header>'
    b+='<section class="wrap xz-prose" aria-label="展厅地图">'+figure('map-full')+'<details><summary>怎样读这幅图</summary>'+''.join('<p>'+e(t)+'</p>' for t in d['map_notes'])+refs(['rubin','acri'])+figure('map-legend')+'</details></section>'
    for g in d['groups']:
        b+='<section class="wrap xz-section xz-prose" id="'+g['id']+'"><h2>'+e(g['title'])+'</h2><p>'+e(g['text'])+refs(g['sources'])+'</p><details class="xz-map-places"><summary>沿途的地点与名字</summary><dl>'
        for p in g['places']:
            b+='<div><dt>'+e(p['title'])+(' <span class="xz-meta">· 补充地点</span>' if p['supplementary'] else '')+'</dt><dd>'+e(p['text'])+refs(p['sources'])+'</dd></div>'
        b+='</dl></details><h3>回到收藏</h3><div class="xz-map-works">'
        for rel in g['works']:
            w=works[rel['id']]
            b+='<article><a href="../'+w['id']+'/">'+photo(w['main_photo'],w['title']+' · '+w['region_label'],'../',card=True)+'<h4>'+e(w['title'])+'</h4></a><p class="xz-meta">'+e(w['region_label'])+' · '+e(w['date_display'])+'</p><p>'+e(rel['relation'])+'</p></article>'
        b+='</div>'
        if g['id']=='sea':b+='<details><summary>展厅地图的海域局部</summary>'+figure('map-sea')+'</details>'
        b+='</section>'
    b+='<section class="wrap xz-section xz-prose"><h2>道路之外，也有人的愿望</h2><p>造像承载的不只是样式。<a href="../x10/">诞生佛与灌沐</a>、<a href="../x24/">法兴像座上的发愿文</a>，以及<a href="../x09/">背光后留下的供养者姓名</a>，让礼拜与供养有了具体的形象。地图帮助辨认远近，作品则留下人与信仰相遇的细节。</p><details id="references"><summary>资料与延伸阅读</summary><p>地图照片记录休斯顿美术馆的展厅表达；网络与地点说明另据以下资料。藏品的年代、地区与个别研究依据，见各作品页。</p><ol class="xz-map-sources">'
    for key in order:
        s=d['sources'][key];b+='<li id="ref-'+key+'"><a href="'+e(s['url'])+'">'+e(s['title'])+' ↗</a></li>'
    b+='</ol></details></section><nav class="wrap xz-bottom-nav"><a href="../#about">← 返回虚舟收藏</a> · <a href="../#catalogue">浏览图录 →</a></nav>'
    return b
