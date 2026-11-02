(() => {
  'use strict';
  const $ = q => document.querySelector(q), $$ = q => [...document.querySelectorAll(q)];
  const openHash = () => {
    const id = decodeURIComponent(location.hash.slice(1)), el = document.getElementById(id);
    if (!el) return;
    for (let p = el; p; p = p.parentElement) if (p.tagName === 'DETAILS') p.open = true;
  };
  openHash();
  window.addEventListener('hashchange', openHash);
  const data = $('#eb-data');
  if (!data) return;
  const {works, map} = JSON.parse(data.textContent), by = Object.fromEntries(works.map(w => [w.id, w]));
  const places = Object.fromEntries(map.places.map(p => [p.id, p]));
  const museums = Object.fromEntries(map.museums.map(m => [m.id, m]));
  const periods = Object.fromEntries(map.periods.map(p => [p.id, p.range]));
  let layer = 'ancient', selected = 'bharhut';
  const matchesPlace = (w, p) => w.place === p || places[w.place]?.parent === p;
  const matchesDate = (w, value) => value === 'all' || (value === 'unknown' ? !w.date_range : w.date_range && w.date_range[0] <= periods[value][1] && w.date_range[1] >= periods[value][0]);
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const writeHash = id => history.replaceState(null, '', '#' + id);
  const render = () => {
    const p = layer === 'ancient' ? places[selected] : museums[selected];
    const title = p?.name_zh || '私人收藏／地点未详';
    const description = layer === 'ancient' ? p.description : selected === 'unlocated' ? '这些作品的现场展出地点尚未确认；已知的私人收藏名称见各件说明。' : '城市级参考位置。私人收藏与馆藏的关系见各件说明；这里不表示作品的古代产地。';
    const ws = works.filter(w => (layer === 'ancient' ? matchesPlace(w, selected) : (w.museum_map || 'unlocated') === selected) && matchesDate(w, $('#eb-period').value) && (!$('#eb-featured').checked || w.units.length));
    $('#eb-map-result').innerHTML = `<h3>${esc(title)}<small>${esc(p?.name_en || p?.city || '')}</small></h3><p>${esc(description)}</p><p class="eb-note">${ws.length} 条作品记录</p>` + (ws.length ? ws.map(w => `<a class="eb-mini" href="${w.units.length ? w.units[0] + '/#' + w.id : '#' + w.id}"><img src="${esc(w.thumbnail)}" alt="${esc(w.title)}" loading="lazy" width="95" height="105"><span>${esc(w.title)}<small>${esc(w.date)}<br>${esc(w.collection_display)}<br>${esc(w.place_relation)}</small></span></a>`).join('') : '<p>这个年代范围内暂无对应作品。可切换“全部年代”继续浏览。</p>');
    $$('[data-map-layer]').forEach(el => el.hidden = el.dataset.mapLayer !== layer);
    $$('[data-layer]').forEach(el => el.setAttribute('aria-pressed', String(el.dataset.layer === layer)));
    $('.eb-place-buttons').hidden = layer !== 'ancient'; $('.eb-museum-buttons').hidden = layer !== 'modern';
    $$('[data-map-key], [data-select-place], [data-select-museum]').forEach(el => {
      const key = el.dataset.mapKey || el.dataset.selectPlace || el.dataset.selectMuseum;
      el.classList.toggle('is-active', key === selected);
      if (key === selected) el.setAttribute('aria-current', 'true'); else el.removeAttribute('aria-current');
    });
    $$('[data-child-of]').forEach(el => el.classList.toggle('is-revealed', el.dataset.childOf === selected || el.dataset.mapKey === selected || el.dataset.childOf === places[selected]?.parent));
  };
  const select = (key, mode = layer, hash = true) => {
    layer = mode; selected = key; render();
    if (hash) writeHash((layer === 'ancient' ? 'place-' : 'museum-') + selected);
  };
  $$('[data-select-place]').forEach(el => el.addEventListener('click', e => {e.preventDefault();select(el.dataset.selectPlace, 'ancient');}));
  $$('[data-select-museum]').forEach(el => el.addEventListener('click', e => {e.preventDefault();select(el.dataset.selectMuseum, 'modern');}));
  $$('[data-map-key]').forEach(el => el.addEventListener('click', e => {e.preventDefault();select(el.dataset.mapKey);}));
  $$('[data-layer]').forEach(el => el.addEventListener('click', () => select(el.dataset.layer === 'ancient' ? 'bharhut' : 'cma', el.dataset.layer)));
  [$('#eb-period'), $('#eb-featured')].forEach(el => el.addEventListener('change', render));
  const cards = $$('.eb-work');
  const filter = () => {
    const query = $('#eb-search').value.trim().toLocaleLowerCase(), place = $('#eb-region-filter').value, museum = $('#eb-museum-filter').value, date = $('#eb-date-filter').value;
    let count = 0;
    cards.forEach(el => {
      const w = by[el.dataset.work];
      const haystack = [w.title,w.title_original,w.date,w.material,w.accession,w.collection_display,w.place_relation,places[w.place]?.name_zh,places[w.place]?.name_en,...(places[w.place]?.aliases_zh || [])].join(' ').toLocaleLowerCase();
      el.hidden = !(query.split(/\s+/).every(t => haystack.includes(t)) && (place === 'all' || matchesPlace(w, place)) && (museum === 'all' || (w.museum_map || 'unlocated') === museum) && matchesDate(w, date));
      if (!el.hidden) count++;
    });
    $('#eb-count').textContent = `${count} / ${works.length} 条作品记录`; $('#eb-empty').hidden = count !== 0;
  };
  const reset = () => {$('#eb-search').value = ''; ['eb-region-filter','eb-museum-filter','eb-date-filter'].forEach(id => $('#' + id).value = 'all'); filter();};
  $('#eb-search').addEventListener('input', filter);
  ['eb-region-filter','eb-museum-filter','eb-date-filter'].forEach(id => $('#' + id).addEventListener('change', filter));
  $('#eb-reset').addEventListener('click', reset);
  $$('[data-focus-work]').forEach(el => el.addEventListener('click', () => {
    const w = by[el.dataset.focusWork]; $('#eb-period').value = 'all'; $('#eb-featured').checked = false;
    select(w.place, 'ancient', false);
    el.nextElementSibling.innerHTML = ' 已选中 · <a href="#places">查看地图 ↑</a>';
  }));
  const handleHash = () => {
    const key = decodeURIComponent(location.hash.slice(1));
    if (key.startsWith('place-') && places[key.slice(6)]) select(key.slice(6), 'ancient', false);
    else if (key.startsWith('museum-') && (museums[key.slice(7)] || key === 'museum-unlocated')) select(key.slice(7), 'modern', false);
    else if (by[key]) {reset(); $('#eb-catalogue').open = true; openHash();}
  };
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#w"]');
    if (a && by[a.getAttribute('href').slice(1)]) {reset(); $('#eb-catalogue').open = true;}
  });
  window.addEventListener('hashchange', handleHash);
  document.body.classList.add('is-enhanced');
  $$('.eb-map-controls, .eb-catalogue-controls, .eb-map-work, #eb-map-result').forEach(el => el.hidden = false);
  render(); filter(); handleHash();
  // Hidden static anchors remain valid for no-script reading; enhanced deep links land at the map.
  if (/^#(place|museum)-/.test(location.hash)) $('#places').scrollIntoView();
})();
