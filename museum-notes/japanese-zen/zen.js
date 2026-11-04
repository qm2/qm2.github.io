(() => {
  const reveal = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    if (!target) return;
    if (id === 'catalogue') target.querySelector('details').open = true;
    let node = target;
    while (node) { if (node.tagName === 'DETAILS') node.open = true; node = node.parentElement; }
    requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
  };
  window.addEventListener('hashchange', reveal);
  if (location.hash) reveal();
  const input = document.getElementById('zen-search');
  if (input) input.addEventListener('input', () => {
    const terms=input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count=0;
    document.querySelectorAll('[data-search]').forEach(item => {
      item.hidden = !terms.every(term => item.dataset.search.toLocaleLowerCase().includes(term));
      if (!item.hidden) count++;
    });
    document.getElementById('zen-count').textContent = `${count} / 19 件／组`;
  });
})();
