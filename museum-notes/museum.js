(() => {
  'use strict';
  const cards = [...document.querySelectorAll('.object-card')];
  if (!cards.length) return;
  const search = document.querySelector('#search');
  const museum = document.querySelector('#museum');
  const material = document.querySelector('#material');
  const tabs = [...document.querySelectorAll('[data-filter]')];
  let category = 'all';
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase().trim();
  const texts = new Map(cards.map(card => [card, normalize(card.textContent)]));
  function update() {
    const words = normalize(search.value).split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      card.hidden = !((category === 'all' || card.dataset.group === category) &&
        (museum.value === 'all' || card.dataset.museum === museum.value) &&
        (material.value === 'all' || card.dataset.material === material.value) &&
        words.every(word => texts.get(card).includes(word)));
      if (!card.hidden) count++;
    }
    document.querySelector('#result-count').textContent = `显示 ${count} / ${cards.length} 件造像`;
    document.querySelector('#empty').hidden = count !== 0;
    for (const tab of tabs) tab.setAttribute('aria-pressed', String(tab.dataset.filter === category));
  }
  update();
  function reset() { search.value = ''; museum.value = material.value = category = 'all'; update(); }
  tabs.forEach(tab => tab.addEventListener('click', () => { category = tab.dataset.filter; update(); }));
  search.addEventListener('input', update);
  museum.addEventListener('change', update);
  material.addEventListener('change', update);
  document.querySelector('#reset').addEventListener('click', reset);
  document.querySelector('.controls').hidden = false;
  function revealHash() {
    const target = document.getElementById(location.hash.slice(1));
    if (target && target.classList.contains('object-card')) {
      if (target.hidden) reset();
      target.querySelector('details').open = true;
      target.scrollIntoView({block: 'start'});
    }
  }
  window.addEventListener('hashchange', revealHash);
  if (location.hash) revealHash();
  const dialog = document.querySelector('#lightbox');
  if (typeof dialog.showModal === 'function') {
    const large = document.querySelector('#lightbox-image');
    document.querySelectorAll('.photo-link').forEach(link => link.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      large.src = link.href;
      large.alt = link.querySelector('img').alt;
      document.querySelector('#lightbox-caption').textContent = link.dataset.caption;
      document.querySelector('#original-link').href = link.href;
      dialog.showModal();
    }));
    dialog.querySelector('button').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => {
      const rect = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
    });
  }
})();
