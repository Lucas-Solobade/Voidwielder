(() => {
  if (!document.querySelector('[data-medieval-reader]')) return;
  document.addEventListener('keydown', (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
    if (document.querySelector('[data-search-dialog]')?.open) return;
    const link = event.key === 'ArrowLeft' ? document.querySelector('[rel="prev"]') : event.key === 'ArrowRight' ? document.querySelector('[rel="next"]') : null;
    if (link) window.location.assign(link.href);
  });
})();
