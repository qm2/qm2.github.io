"""Shared sculpture card and viewer, used by the archive and focused topics."""
from html import escape as e
from museum_assets import asset_url, responsive_attributes

def render_card(o, i, image_prefix="images/", *, museums):
    m,city,en=museums[o['museum']]
    detail = f'<p>{e(o["story"])}</p>' if o['story'] else ''
    for section in o.get('note_sections', []):
        detail += f'<section class="note-section"><h4>{e(section["title"])}</h4><p>{e(section["text"])}</p></section>'
        if section.get('url'):
            detail += f'<p class="source"><a href="{e(section["url"])}" target="_blank" rel="noopener noreferrer">{e(section["source_title"])} ↗</a></p>'
    if o['caveat']: detail += f'<p class="record-note">{e(o["caveat"])}</p>'
    if o['url']: detail += f'<p class="source"><a href="{e(o["url"])}" target="_blank" rel="noopener noreferrer">{e(o.get("source_title", "馆方藏品记录"))} ↗</a></p>'
    for photo in o.get('related_photos', []):
        detail += f'<figure class="related-photo"><a class="photo-link" href="{photo.get("original_url") or asset_url(image_prefix,photo["photo"])}" data-caption="{e(photo["caption"])}" aria-label="放大照片：{e(photo["caption"])}"><img src="{asset_url(image_prefix,photo["photo"])}"{responsive_attributes(photo)} alt="{e(photo["caption"])}" width="{photo["width"]}" height="{photo["height"]}" loading="lazy"><span class="photo-hint">查看大图 ↗</span></a><figcaption>{e(photo["caption"])}</figcaption></figure>'
    for group in o.get('photo_groups', []):
        detail += '<details class="sc-photo-group"><summary>'+e(group['title'])+'</summary><div class="sc-detail-gallery">'
        for photo in group['photos']:
            url=photo.get('original_url') or asset_url(image_prefix,photo['photo'])
            detail += f'<figure><a class="photo-link" href="{url}" data-caption="{e(photo["caption"])}" aria-label="放大：{e(photo["caption"])}"><img src="{asset_url(image_prefix,photo["photo"])}"{responsive_attributes(photo, "(max-width:650px) 42vw, 320px")} alt="{e(photo["caption"])}" width="{photo["width"]}" height="{photo["height"]}" loading="lazy"></a><figcaption>{e(photo["caption"])}</figcaption></figure>'
        detail += '</div></details>'
    if o.get('archived_photos'):
        detail += '<details class="previous-photos"><summary>此前观看的照片</summary>'
        for photo in o['archived_photos']:
            url=photo.get('original_url') or asset_url(image_prefix,photo['photo'])
            detail += f'<figure class="related-photo"><a class="photo-link" href="{url}" data-caption="{e(photo["caption"])}"><img src="{asset_url(image_prefix,photo["photo"])}" alt="{e(photo["caption"])}" width="{photo["width"]}" height="{photo["height"]}" loading="lazy"></a><figcaption>{e(photo["caption"])}</figcaption></figure>'
        detail += '</details>'
    detail += '<p class="source">基本信息据现场展签整理；照片 © Merton。</p>'
    personal = ''
    for note in o.get('personal_notes', []):
        if not note.get('text', '').strip():
            continue
        kind = {'visit_memory': '回忆当时', 'photo_reflection': '重看照片', 'onsite': '现场随记'}[note['kind']]
        date = f" · {e(note['written_on'])}记" if note.get('written_on') else ''
        personal += f'<aside class="personal-note"><h4>我的观看 · {kind}{date}</h4><p>{e(note["text"])}</p></aside>'
    return f'''<article class="object-card" id="{o['id']}" data-museum="{o['museum']}" data-material="{o['material_group']}" data-group="{o['group']}">
      <a class="photo-link" href="{o.get('original_url') or asset_url(image_prefix,o['photo'])}" data-caption="{e(o['title'])} · {e(m)}" aria-label="放大照片：{e(o['title'])}，{e(m)}">
        <img src="{asset_url(image_prefix,o['photo'])}"{responsive_attributes(o)} alt="{e(o['title'])}，{e(o['date'])}，{e(m)}；{e(o['observation'])}" width="{o['width']}" height="{o['height']}" loading="lazy" decoding="async">
        <span class="photo-hint" aria-hidden="true">查看大图 ↗</span>
      </a>
      <div class="object-body"><div class="object-topline"><span>{e(city)} · {e(m)}</span><a class="permalink" href="#{o['id']}" aria-label="此作品的固定链接">{i+1:02d}</a></div>
      <h3>{e(o['title'])}</h3><p class="original-title">{e(o['original_title'])}</p>
      <dl><div><dt>年代</dt><dd>{e(o['date'])}</dd></div><div><dt>材质</dt><dd>{e(o['material'])}</dd></div><div><dt>编号</dt><dd>{e(o['accession'])}</dd></div></dl>
      <p class="observation">{e(o['observation'])}</p>{personal}
      <details><summary>作品札记与资料 <span aria-hidden="true">＋</span></summary><div class="notes">{detail}</div></details></div>
    </article>'''
lightbox = '''<dialog id="lightbox" aria-labelledby="lightbox-caption"><button class="close-lightbox" type="button" aria-label="关闭大图">关闭 ×</button><img id="lightbox-image" alt=""><p id="lightbox-caption"></p><a id="original-link" href="#" target="_blank" rel="noopener">单独打开照片 ↗</a></dialog>'''
