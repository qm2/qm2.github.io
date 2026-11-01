(() => {
  'use strict';
  const all = q => [...document.querySelectorAll(q)];
  const catalogue = document.querySelector('.hm-catalogue');
  const revealHash = () => {
    const target = document.getElementById(location.hash.slice(1));
    if (!target) return;
    if (target.matches('details')) target.open = true;
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
    if (target) { target.open = true; requestAnimationFrame(() => target.querySelector('summary').focus()); }
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
