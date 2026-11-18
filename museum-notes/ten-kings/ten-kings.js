(() => {
  'use strict';
  // Native details stay usable without JavaScript; deep links reveal the matching evidence.
  function reveal() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (!target) return;
    let node = target;
    while (node) {
      if (node.tagName === 'DETAILS') node.open = true;
      node = node.parentElement;
    }
    requestAnimationFrame(() => target.scrollIntoView({block: 'start', behavior: 'instant'}));
  }
  addEventListener('hashchange', reveal);
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link && link.hash === location.hash) requestAnimationFrame(reveal);
  });
  if (location.hash) reveal();
})();
