(() => {
  const filters = document.querySelector('.xz-filters');
  if (filters) {
    const buttons = [...filters.querySelectorAll('[data-region-filter]')];
    const sections = [...document.querySelectorAll('[data-region-section]')];
    filters.hidden = false;
    buttons.forEach(button => button.addEventListener('click', () => {
      const key = button.dataset.regionFilter;
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      let count = 0;
      sections.forEach(section => {
        section.hidden = key !== 'all' && key !== section.dataset.regionSection;
        if (!section.hidden) count += section.querySelectorAll('.xz-card').length;
      });
      document.querySelector('.xz-count').textContent = `${count}件虚舟收藏作品`;
    }));
  }
  // A direct label link should reveal the folded evidence as well as scroll to it.
  function revealLabel() {
    if (location.hash === '#label') {
      const details = document.querySelector('#label details');
      if (details) details.open = true;
    }
  }
  window.addEventListener('hashchange', revealLabel);
  document.querySelectorAll('a[href="#label"]').forEach(link => {
    link.addEventListener('click', () => {
      const details = document.querySelector('#label details');
      if (details) details.open = true;
    });
  });
  revealLabel();
})();
