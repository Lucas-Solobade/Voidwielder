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
      const art = panel.querySelector('.twilight-panel-art') || panel;
      const svg = art.querySelector('.twilight-balloon-tails');
      if (!svg || !art) return;
      const artBox = art.getBoundingClientRect();
      svg.setAttribute('viewBox', `0 0 ${artBox.width} ${artBox.height}`);
      svg.replaceChildren();
      art.querySelectorAll('.twilight-speech').forEach((balloon) => {
        if (balloon.dataset.offPanel === 'true') return;
        const box = balloon.getBoundingClientRect();
        const targetX = artBox.width * Number(balloon.dataset.targetX) / 100;
        const targetY = artBox.height * Number(balloon.dataset.targetY) / 100;
        const left = box.left - artBox.left;
        const right = box.right - artBox.left;
        const bottom = box.bottom - artBox.top;
        const top = box.top - artBox.top;
        if (![left, right, top, bottom, targetX, targetY].every(Number.isFinite)) return;
        if (targetX >= left && targetX <= right && targetY >= top && targetY <= bottom) return;

        // Keep the pointer close to its balloon. A long tail can cut across
        // another panel or the speaker's face when the page is resized.
        const clamp = (value, low, high) => Math.min(high, Math.max(low, value));
        let startX;
        let startY;
        if (targetY >= bottom && (targetX >= left || targetY - bottom > left - targetX) && (targetX <= right || targetY - bottom > targetX - right)) {
          startX = clamp(targetX, left + 18, right - 18);
          startY = bottom - 1;
        } else if (targetY <= top && (targetX >= left || top - targetY > left - targetX) && (targetX <= right || top - targetY > targetX - right)) {
          startX = clamp(targetX, left + 18, right - 18);
          startY = top + 1;
        } else {
          startX = targetX < left ? left + 1 : right - 1;
          startY = clamp(targetY, top + 15, bottom - 15);
        }
        const deltaX = targetX - startX;
        const deltaY = targetY - startY;
        const distance = Math.hypot(deltaX, deltaY);
        if (distance < 3) return;
        const length = Math.min(distance, clamp(artBox.width * .035, 18, 34));
        const tipX = startX + deltaX / distance * length;
        const tipY = startY + deltaY / distance * length;
        const sideX = -deltaY / distance * 6;
        const sideY = deltaX / distance * 6;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M ${startX - sideX} ${startY - sideY} Q ${startX + deltaX / distance * length * .55 - sideX * .45} ${startY + deltaY / distance * length * .55 - sideY * .45} ${tipX} ${tipY} Q ${startX + deltaX / distance * length * .55 + sideX * .45} ${startY + deltaY / distance * length * .55 + sideY * .45} ${startX + sideX} ${startY + sideY} Z`);
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
