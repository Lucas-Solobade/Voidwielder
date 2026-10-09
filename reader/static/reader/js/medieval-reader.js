(() => {
  if (!document.querySelector('[data-medieval-reader]')) return;
  document.addEventListener('keydown', (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
    if (document.querySelector('[data-search-dialog]')?.open) return;
    const link = event.key === 'ArrowLeft' ? document.querySelector('[rel="prev"]') : event.key === 'ArrowRight' ? document.querySelector('[rel="next"]') : null;
    if (link) window.location.assign(link.href);
  });

  const drawBalloonTails = () => {
    document.querySelectorAll('.twilight-panel-dialogue').forEach((panel) => {
      const svg = panel.querySelector('.twilight-balloon-tails');
      const art = panel.querySelector('.twilight-panel-art');
      if (!svg || !art) return;
      const panelBox = panel.getBoundingClientRect();
      const artBox = art.getBoundingClientRect();
      svg.setAttribute('viewBox', `0 0 ${panelBox.width} ${panelBox.height}`);
      svg.replaceChildren();
      panel.querySelectorAll('.twilight-speech').forEach((balloon) => {
        const box = balloon.getBoundingClientRect();
        const startX = box.left - panelBox.left + box.width * .56;
        const startY = box.bottom - panelBox.top - 1;
        const targetX = artBox.left - panelBox.left + artBox.width * Number(balloon.dataset.targetX) / 100;
        const targetY = artBox.top - panelBox.top + artBox.height * Number(balloon.dataset.targetY) / 100;
        if (![startX, startY, targetX, targetY].every(Number.isFinite)) return;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M ${startX - 8} ${startY} Q ${startX - 1} ${startY + 16} ${targetX} ${targetY} Q ${startX + 2} ${startY + 15} ${startX + 8} ${startY} Z`);
        path.setAttribute('fill', '#fffdf6');
        path.setAttribute('stroke', '#1a232a');
        path.setAttribute('stroke-width', '2');
        path.setAttribute('stroke-linejoin', 'round');
        svg.append(path);
      });
    });
  };
  if (document.querySelector('.twilight-panel-dialogue')) {
    drawBalloonTails();
    window.addEventListener('resize', drawBalloonTails, { passive: true });
    document.fonts?.ready.then(drawBalloonTails);
  }
})();
