(() => {
  'use strict';
  const $ = (q) => document.querySelector(q);
  const controls = $('.art-controls');
  if (controls) {
    const cards = [...document.querySelectorAll('.car-collection .art-card')];
    const query = $('#art-search'), museum = $('#art-museum'), subject = $('#art-subject');
    const update = () => {
      const terms = query.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        const show = terms.every(t => card.dataset.search.toLocaleLowerCase().includes(t)) &&
          (museum.value === 'all' || museum.value === card.dataset.museum) &&
          (subject.value === 'all' || card.dataset.tags.split(' ').includes(subject.value));
        card.hidden = !show;
        if (show) count++;
      });
      document.querySelectorAll('.era-section').forEach(section => {
        section.hidden = ![...section.querySelectorAll('.art-card')].some(card => !card.hidden);
      });
      $('#art-count').textContent = `${count} / ${cards.length} 件作品`;
      $('#art-empty').hidden = count !== 0;
    };
    controls.hidden = false;
    query.addEventListener('input', update);
    [museum, subject].forEach(el => el.addEventListener('change', update));
    const reset = () => {
      query.value = ''; museum.value = subject.value = 'all'; update();
    };
    $('#art-reset').addEventListener('click', reset);
    document.querySelectorAll('.era-nav a').forEach(link => link.addEventListener('click', () => {
      const target = document.getElementById(link.hash.slice(1));
      if (target && target.hidden) reset();
    }));
    $('#gallery-mode').addEventListener('click', event => {
      const on = document.body.classList.toggle('gallery-mode');
      event.currentTarget.setAttribute('aria-pressed', String(on));
      event.currentTarget.textContent = on ? '恢复札记模式' : '画廊模式';
    });
  }
  const dialog = $('#art-lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const links = [...document.querySelectorAll('a[data-photo]')];
  const stage = $('#photo-stage'), large = $('#large-photo');
  let active = [], index = 0, opener;
  const resetZoom = () => {
    stage.classList.remove('is-zoomed'); stage.scrollTop = stage.scrollLeft = 0;
    $('#zoom-toggle').setAttribute('aria-pressed', 'false');
    $('#zoom-toggle').textContent = '放大细看 ＋';
  };
  const show = () => {
    resetZoom();
    const link = active[index];
    large.src = link.href;
    large.alt = link.dataset.caption;
    $('#original-photo').href = link.href;
    $('#lightbox-caption').textContent = `${index + 1} / ${active.length} · ${link.dataset.caption}`;
    $('#photo-prev').disabled = index === 0;
    $('#photo-next').disabled = index === active.length - 1;
  };
  links.forEach(link => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const group = link.closest('.compare-group');
    active = links.filter(candidate => (!group || group.contains(candidate)) && !candidate.closest('[hidden]') && candidate.getClientRects().length);
    index = active.indexOf(link); opener = link; show();
    dialog.showModal(); document.body.classList.add('photo-open');
    $('#photo-close').focus();
  }));
  const step = (amount) => {
    const next = index + amount;
    if (next >= 0 && next < active.length) { index = next; show(); }
  };
  $('#photo-prev').addEventListener('click', () => step(-1));
  $('#photo-next').addEventListener('click', () => step(1));
  $('#photo-close').addEventListener('click', () => dialog.close());
  $('#zoom-toggle').addEventListener('click', event => {
    const on = stage.classList.toggle('is-zoomed');
    event.currentTarget.setAttribute('aria-pressed', String(on));
    event.currentTarget.textContent = on ? '适合屏幕 －' : '放大细看 ＋';
  });
  dialog.addEventListener('keydown', event => {
    if (stage.classList.contains('is-zoomed')) return;
    if (event.key === 'ArrowLeft') { event.preventDefault(); step(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); step(1); }
  });
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('photo-open'); resetZoom();
    if (opener) opener.focus();
  });
})();
