(() => {
  'use strict';
  const $ = (q) => document.querySelector(q);
  const controls = $('.art-controls');
  if (controls) {
    const cards = [...document.querySelectorAll('.car-collection .art-card')];
    const query = $('#art-search'), museum = $('#art-museum'), subject = $('#art-subject');
    const update = () => {
      const terms = query.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let count = 0, core = 0, disputed = 0;
      cards.forEach(card => {
        const show = terms.every(t => card.dataset.search.toLocaleLowerCase().includes(t)) &&
          (museum.value === 'all' || museum.value === card.dataset.museum) &&
          (subject.value === 'all' || card.dataset.tags.split(' ').includes(subject.value));
        card.hidden = !show;
        if (show) { count++; if (card.dataset.scope === 'core_attributed') core++; else disputed++; }
      });
      document.querySelectorAll('.era-section').forEach(section => {
        section.hidden = ![...section.querySelectorAll('.art-card')].some(card => !card.hidden);
      });
      $('#art-count').textContent = `${count}条记录（${core}件归属作品＋${disputed}件待考）`;
      $('#art-empty').hidden = count !== 0;
    };
    controls.hidden = false;
    update();
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
  // Each entry is a work + view, never a globally deduplicated image URL.
  const dialog = $('#art-lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const links = [...document.querySelectorAll('a[data-photo]')];
  const stage = $('#photo-stage'), large = $('#large-photo'), frame = $('#xts-lightbox-view');
  const fullButton = $('#xts-full'), zoomButton = $('#zoom-toggle');
  let active = [], index = 0, opener, zoomed = false;
  const record = link => ({
    id: link.dataset.viewId, workId: link.dataset.workId,
    number: link.dataset.photoNumber, url: link.href,
    caption: link.dataset.caption,
    width: Number(link.dataset.width), height: Number(link.dataset.height),
    crop: link.dataset.crop ? JSON.parse(link.dataset.crop) : null,
    fullCaption: link.dataset.fullCaption
  });
  const fullId = r => `${r.workId}:full:${r.number}`;
  const cropId = r => `${r.workId}:crop:${r.number}`;
  const collect = opening => {
    const records = [], seen = new Set();
    const add = r => { if (!seen.has(r.id)) { seen.add(r.id); records.push(r); } };
    links.filter(link => link.dataset.photoGroup === opening.dataset.photoGroup &&
      !link.closest('[hidden]') && !link.closest('details:not([open])') && link.getClientRects().length).forEach(link => {
      const r = record(link); add(r);
      if (r.crop) add({...r, id:fullId(r), caption:r.fullCaption, crop:null});
    });
    return records;
  };
  const layout = () => {
    if (!dialog.open || !active[index]) return;
    const r = active[index], c = r.crop || {x:0,y:0,width:1,height:1};
    const w = r.width*c.width, h = r.height*c.height, ratio = w/h;
    const fit = Math.min(stage.clientWidth-12,(stage.clientHeight-12)*ratio);
    const displayWidth = zoomed ? Math.max(w,fit*2) : fit;
    frame.style.width = `${displayWidth}px`; frame.style.height = `${displayWidth/ratio}px`;
    frame.style.setProperty('--crop-ratio',String(ratio));
    large.style.width = `${100/c.width}%`; large.style.height = `${100/c.height}%`;
    large.style.left = `${-100*c.x/c.width}%`; large.style.top = `${-100*c.y/c.height}%`;
  };
  const setZoom = value => {
    zoomed = value; stage.classList.toggle('is-zoomed',zoomed);
    zoomButton.setAttribute('aria-pressed',String(zoomed));
    zoomButton.textContent = zoomed ? '适合屏幕 －' : '放大细看 ＋';
    layout(); stage.scrollTop = stage.scrollLeft = 0;
  };
  const show = () => {
    const r = active[index];
    frame.dataset.viewId = r.id; frame.dataset.workId = r.workId;
    frame.dataset.crop = JSON.stringify(r.crop);
    large.src = r.url; large.alt = r.caption;
    $('#original-photo').href = r.url;
    $('#lightbox-caption').textContent = `${index+1} / ${active.length} · ${r.caption}`;
    $('#photo-prev').disabled = index===0;
    $('#photo-next').disabled = index===active.length-1;
    const partner = active.findIndex(v => v.id === (r.crop ? fullId(r) : cropId(r)));
    fullButton.hidden = partner < 0;
    fullButton.textContent = r.crop ? '查看完整合照' : '返回作品局部';
    fullButton.dataset.targetIndex = String(partner);
    setZoom(false);
  };
  links.forEach(link => link.addEventListener('click',event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); opener=link; active=collect(link);
    index=active.findIndex(r => r.id === link.dataset.viewId);
    if (index<0) { active=[record(link)];index=0; }
    dialog.showModal(); document.body.classList.add('photo-open');show();
    $('#photo-close').focus();
  }));
  const step = amount => {
    const next=index+amount;
    if (next>=0 && next<active.length) { index=next;show(); }
  };
  $('#photo-prev').addEventListener('click',()=>step(-1));
  $('#photo-next').addEventListener('click',()=>step(1));
  fullButton.addEventListener('click',()=>{
    const next=Number(fullButton.dataset.targetIndex);
    if (next>=0) { index=next;show(); }
  });
  zoomButton.addEventListener('click',()=>setZoom(!zoomed));
  $('#photo-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('keydown',event=>{
    if (event.key==='ArrowLeft' || event.key==='ArrowRight') {
      // Inside the zoomed photo, arrow keys pan; on the controls they switch views.
      if (zoomed && event.target===stage) return;
      event.preventDefault();step(event.key==='ArrowLeft'?-1:1);
    }
  });
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
  dialog.addEventListener('close',()=>{
    document.body.classList.remove('photo-open');setZoom(false);
    if(opener)opener.focus();
  });
  new ResizeObserver(layout).observe(stage);
})();
