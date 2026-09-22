(() => {
  'use strict';
  document.querySelectorAll('.painting-filters').forEach(filters => {
    const cards = [...document.querySelectorAll('.painting-card')];
    const sections = [...document.querySelectorAll('.period-section')];
    const buttons = [...filters.querySelectorAll('[data-painting-filter]')];
    function select(tag) {
      cards.forEach(card => { card.hidden = tag !== 'all' && !card.dataset.tags.split(' ').includes(tag); });
      sections.forEach(section => {
        const count = section.querySelectorAll('.painting-card:not([hidden])').length;
        section.hidden = count === 0;
        document.querySelectorAll('.period-nav a').forEach(link => {
          if (link.getAttribute('href') !== '#' + section.id) return;
          link.hidden = count === 0;
          const badge = link.querySelector('span');
          if (badge) badge.textContent = count;
        });
      });
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.paintingFilter === tag)));
      filters.querySelector('.filter-result').textContent = `显示 ${cards.filter(card => !card.hidden).length} 件作品 · 同一件作品可以属于多个题材`;
    }
    buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.paintingFilter)));
    filters.hidden = false; select('all');
    function revealPeriod() {
      if (sections.some(section => '#' + section.id === location.hash && section.hidden)) {
        select('all'); document.getElementById(location.hash.slice(1)).scrollIntoView({block:'start'});
      }
    }
    window.addEventListener('hashchange', revealPeriod);
  });

  document.querySelectorAll('[data-gallery]').forEach(gallery => {
    const slides = [...gallery.querySelectorAll('.slide')];
    const controls = gallery.querySelector('.gallery-controls');
    const thumbs = gallery.querySelector('.gallery-thumbs');
    const previous = gallery.querySelector('[data-prev]');
    const next = gallery.querySelector('[data-next]');
    const all = gallery.querySelector('[data-show-all]');
    let selected = 0, expanded = false;
    const buttons = slides.map((slide, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('aria-label', slide.querySelector('figcaption').textContent.trim());
      button.append(slide.querySelector('.image-box').cloneNode(true));
      const number = document.createElement('span'); number.textContent = String(index + 1).padStart(2, '0');
      button.append(number); button.addEventListener('click', () => { selected = index; expanded = false; update(); });
      thumbs.append(button); return button;
    });
    function update() {
      slides.forEach((slide, i) => { slide.hidden = !expanded && i !== selected; });
      slides[selected].querySelector('img').loading = 'eager';
      buttons.forEach((button, i) => button.setAttribute('aria-current', String(i === selected)));
      previous.disabled = expanded || selected === 0;
      next.disabled = expanded || selected === slides.length - 1;
      gallery.querySelector('.gallery-count').textContent = expanded ? `全部 ${slides.length} 张` : `${selected + 1} / ${slides.length}`;
      all.setAttribute('aria-pressed', String(expanded)); all.textContent = expanded ? '收起图组' : '展开全部';
    }
    previous.addEventListener('click', () => { if (selected > 0) { selected--; update(); } });
    next.addEventListener('click', () => { if (selected < slides.length - 1) { selected++; update(); } });
    all.addEventListener('click', () => { expanded = !expanded; update(); });
    if (slides.length > 1) { controls.hidden = false; thumbs.hidden = false; }
    function revealHash() {
      const index = slides.findIndex(slide => '#' + slide.id === location.hash);
      if (index >= 0) { selected = index; expanded = false; update(); slides[index].scrollIntoView({block:'start'}); }
    }
    update(); revealHash(); window.addEventListener('hashchange', revealHash);
  });
  const dialog = document.querySelector('#painting-lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const viewport = dialog.querySelector('.zoom-viewport');
  const toggle = document.querySelector('#zoom-toggle');
  document.querySelectorAll('.photo-open').forEach(link => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); viewport.replaceChildren(link.querySelector('.image-box').cloneNode(true));
    viewport.querySelector('img').loading = 'eager';
    viewport.classList.remove('zoomed'); toggle.setAttribute('aria-pressed','false');toggle.textContent='放大细节';
    document.querySelector('#zoom-caption').textContent=link.dataset.caption;
    document.querySelector('#zoom-original').href=link.href;
    dialog.showModal(); viewport.scrollTo(0,0);
  }));
  toggle.addEventListener('click', () => {
    const zoomed=viewport.classList.toggle('zoomed');toggle.setAttribute('aria-pressed',String(zoomed));
    toggle.textContent=zoomed?'适应窗口':'放大细节';
  });
  document.querySelector('#zoom-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const rect=dialog.getBoundingClientRect();
    if(event.target===dialog&&(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom))dialog.close();
  });
})();
