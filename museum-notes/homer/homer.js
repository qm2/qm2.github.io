(() => {
  'use strict';
  const all = q => [...document.querySelectorAll(q)];
  const regions = all('.hm-region');
  let picker;
  const selectRegion = target => {
    regions.forEach(region => { region.open = region === target; region.hidden = region !== target; });
    if (picker) [...picker.children].forEach(b => b.setAttribute('aria-expanded', String(Boolean(target && b.getAttribute('aria-controls') === target.id))));
  };
  if (regions.length) {
    document.getElementById('journeys').classList.add('hm-map-enhanced');
    picker = document.createElement('div'); picker.className = 'hm-region-picker';
    picker.setAttribute('role', 'group'); picker.setAttribute('aria-label', '选择地区，展开对应作品');
    regions.forEach(region => {
      const button = document.createElement('button'); button.type = 'button';
      button.textContent = region.querySelector('summary span').textContent;
      button.setAttribute('aria-controls', region.id); button.setAttribute('aria-expanded', 'false');
      button.addEventListener('click', () => {
        const next = region.open ? null : region; selectRegion(next);
        history.replaceState(null, '', next ? '#' + region.id : '#journeys');
      });
      picker.append(button);
    });
    document.querySelector('.hm-regions').before(picker); selectRegion(null);
  }
  const catalogue = document.querySelector('.hm-catalogue');
  const revealHash = () => {
    const target = document.getElementById(location.hash.slice(1));
    if (!target) return;
    if (target.matches('.hm-region')) selectRegion(target);
    else if (target.matches('details')) target.open = true;
    if (target.id === 'catalogue' && catalogue) catalogue.open = true;
    for (let p = target.parentElement; p; p = p.parentElement) if (p.matches('details')) p.open = true;
  };
  revealHash(); window.addEventListener('hashchange', revealHash);
  all('.hm-map-tools').forEach(e => e.hidden = false);
  const expand = document.getElementById('hm-map-expand');
  if (expand) expand.addEventListener('click', () => {
    const on = document.getElementById('journeys').classList.toggle('hm-map-expanded');
    expand.setAttribute('aria-pressed', String(on));
    expand.textContent = on ? '适合屏幕' : '放大地图';
  });
  all('[data-view]').forEach(button => button.addEventListener('click', () => {
    all('[data-map]').forEach(panel => panel.hidden = panel.dataset.map !== button.dataset.view);
    all('[data-view]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  }));
  all('[data-region]').forEach(link => link.addEventListener('click', () => {
    const target = document.getElementById('region-' + link.dataset.region);
    if (target) { selectRegion(target); requestAnimationFrame(() => picker.querySelector('[aria-controls="' + target.id + '"]').focus({preventScroll:true})); }
  }));
  if (!catalogue) return;
  const input = document.getElementById('hm-search'), medium = document.getElementById('hm-medium'), era = document.getElementById('hm-era');
  const rows = all('.hm-archive-row');
  const update = () => {
    const terms = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    rows.forEach(row => {
      const show = terms.every(t => row.dataset.search.includes(t)) && (medium.value === 'all' || medium.value === row.dataset.medium) && (era.value === 'all' || era.value === row.dataset.era);
      row.hidden = !show; if (show) count++;
    });
    document.getElementById('hm-count').textContent = `${count} / ${rows.length} 条记录`;
    document.getElementById('hm-empty').hidden = count !== 0;
  };
  document.querySelector('.hm-filters').hidden = false;
  input.addEventListener('input', update); [medium, era].forEach(el => el.addEventListener('change', update));
  document.getElementById('hm-reset').addEventListener('click', () => { input.value = ''; medium.value = era.value = 'all'; update(); });
})();
