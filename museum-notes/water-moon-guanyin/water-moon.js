(() => {
  'use strict';
  const panels = [...document.querySelectorAll('[data-museum-panel]')];
  const links = [...document.querySelectorAll('[data-museum-link]')];
  function selectMuseum(key) {
    if (!panels.some(panel => panel.dataset.museumPanel === key)) return;
    panels.forEach(panel => { panel.hidden = panel.dataset.museumPanel !== key; });
    links.forEach(link => {
      if (link.dataset.museumLink === key) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
  }
  function reveal() {
    const target = document.getElementById(location.hash.slice(1));
    if (!target) return;
    if (target.dataset.extensionTarget) {
      location.replace(target.dataset.extensionTarget);
      return;
    }
    if (target.dataset.museumPanel) selectMuseum(target.dataset.museumPanel);
    if (target.matches('details.wm-dealer')) target.open = true;
    if (target.matches('[data-museum-panel], details.wm-dealer')) {
      requestAnimationFrame(() => target.scrollIntoView({block: 'start'}));
    }
  }
  if (panels.length) selectMuseum(panels[0].dataset.museumPanel);
  // Anchors are functional without JS; hash changes also cover back/forward.
  links.forEach(link => link.addEventListener('click', () => {
    selectMuseum(link.dataset.museumLink);
  }));
  window.addEventListener('hashchange', reveal);
  reveal();
})();
