(() => {
  const browser = document.querySelector('[data-episode-browser]');
  if (!browser) return;

  const tabs = [...browser.querySelectorAll('[data-episode-tab]')];
  const panels = [...browser.querySelectorAll('[data-episode-panel]')];
  const activate = (tab, updateUrl = false) => {
    const target = tab.getAttribute('aria-controls');
    tabs.forEach(item => {
      const selected = item === tab;
      item.classList.toggle('is-active', selected);
      item.setAttribute('aria-expanded', String(selected));
      if (selected) item.setAttribute('aria-current', 'true');
      else item.removeAttribute('aria-current');
    });
    panels.forEach(panel => { panel.hidden = panel.id !== target; });
    if (updateUrl) history.replaceState(null, '', `#${target}`);
  };

  const selected = tabs.find(tab => tab.getAttribute('aria-controls') === location.hash.slice(1)) || tabs[0];
  if (selected) activate(selected);

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', event => {
      event.preventDefault();
      activate(tab, true);
    });
    tab.addEventListener('keydown', event => {
      if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
      event.preventDefault();
      const offset = event.key === 'ArrowRight' ? 1 : -1;
      const next = tabs[(index + offset + tabs.length) % tabs.length];
      activate(next, true);
      next.focus();
      next.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    });
  });

  browser.querySelectorAll('[data-scroll-rail]').forEach(button => {
    button.addEventListener('click', () => {
      const rail = browser.querySelector(`[data-rail="${button.dataset.scrollRail}"]`);
      rail?.scrollBy({ left: rail.clientWidth * Number(button.dataset.direction) * .75, behavior: 'smooth' });
    });
  });
  browser.querySelectorAll('[data-scroll-pages]').forEach(button => {
    button.addEventListener('click', () => {
      const rail = button.closest('[data-episode-panel]')?.querySelector('[data-rail="pages"]');
      rail?.scrollBy({ left: rail.clientWidth * Number(button.dataset.scrollPages) * .75, behavior: 'smooth' });
    });
  });
  window.addEventListener('hashchange', () => {
    const tab = tabs.find(item => item.getAttribute('aria-controls') === location.hash.slice(1));
    if (tab) activate(tab);
  });
})();
