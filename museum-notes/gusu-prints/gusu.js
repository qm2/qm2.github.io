(() => {
  'use strict';
  // Ordinary work links stay ordinary links; only native fragments scroll within a page.
  const revealHash = () => {
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target) return;
    for (let node = target; node; node = node.parentElement) {
      if (node.tagName === 'DETAILS') node.open = true;
    }
    requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
  };
  const controls = document.querySelector('.gs-filters');
  if (controls) {
    const fields = ['query','chapter','date','depth'];
    const inputs = fields.map(f => document.getElementById('gs-'+f));
    const cards = [...document.querySelectorAll('.gs-card')];
    const update = (save) => {
      const [query, chapter, date, depth] = inputs.map(i => i.value);
      const terms = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(c => {
        const match = terms.every(t => c.dataset.search.toLocaleLowerCase().includes(t)) &&
          (!chapter || c.dataset.chapter === chapter) && (!date || c.dataset.date === date) &&
          (!depth || c.dataset.depth === depth);
        c.hidden = !match; count += match ? 1 : 0;
      });
      document.getElementById('gs-count').textContent = `${count} / ${cards.length} 条作品／成组记录`;
      document.getElementById('gs-empty').hidden = count !== 0;
      if (save) {
        const url = new URL(location.href);
        fields.forEach((f,i) => {if(inputs[i].value) url.searchParams.set(f,inputs[i].value);else url.searchParams.delete(f);});
        if (url.href !== location.href) history.pushState(null,'',url);
      }
    };
    const restore = () => {
      const p = new URLSearchParams(location.search);
      inputs.forEach((el,i) => {el.value = p.get(fields[i]) || '';});
      if (inputs.some(el=>el.value)) {const d=controls.closest('details');if(d)d.open=true;}
      update(false);
    };
    controls.hidden = false;
    let timer;
    inputs[0].addEventListener('input', () => {clearTimeout(timer);timer=setTimeout(()=>update(true),180);});
    inputs.slice(1).forEach(el => el.addEventListener('change',()=>update(true)));
    document.getElementById('gs-reset').addEventListener('click',()=>{clearTimeout(timer);inputs.forEach(el=>el.value='');update(true);});
    addEventListener('popstate',restore);restore();
  }
  const book = document.querySelector('.gs-book');
  if (book) {
    const buttons = [...book.querySelectorAll('[data-open-page]')];
    const pages = [...book.querySelectorAll('[data-book-page]')];
    const select = id => {
      buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.openPage===id)));
      pages.forEach(p=>p.hidden=p.dataset.bookPage!==id);
    };
    buttons.forEach(b=>b.addEventListener('click',()=>select(b.dataset.openPage)));
    book.querySelector('.gs-book-controls').hidden=false;select('3005');
  }
  addEventListener('hashchange',revealHash);
  addEventListener('load',revealHash,{once:true});
})();
