(() => {
  const selectors = [
    ['[data-book-spread], [data-linux-spread], [data-python-spread], [data-web-spread]', null],
    ['.twilight-page-stage', '.twilight-page-scroll'],
    ['.twilight-comic', null],
    ['.manga-page', null],
    ['.arc-book', null],
  ];
  let target = null;
  let viewport = null;
  for (const [selector, viewportSelector] of selectors) {
    target = document.querySelector(selector);
    if (!target) continue;
    viewport = viewportSelector ? target.closest(viewportSelector) : target.parentElement;
    break;
  }
  if (!target || !viewport) return;

  const longReader = target.matches('.arc-book');
  if (!target.matches('[data-book-spread], [data-linux-spread], [data-python-spread], [data-web-spread], .twilight-page-stage')) {
    const wrapper = document.createElement('div');
    wrapper.className = 'reader-zoom-viewport';
    target.before(wrapper);
    wrapper.append(target);
    viewport = wrapper;
  }
  viewport.classList.add('reader-zoom-viewport');
  if (longReader) viewport.classList.add('reader-zoom-long');
  target.classList.add('reader-zoom-target');

  const clamp = (value) => Math.max(.4, Math.min(3, Math.round(value * 20) / 20));
  const key = `voidwielder-reader-zoom:${location.pathname.replace(/\/ler\/\d+\/$/, '/ler/')}`;
  let scale = 1;
  try { scale = clamp(Number(sessionStorage.getItem(key)) || 1); } catch { /* Storage is optional. */ }
  let baseWidth = 0;
  let pinch = null;
  let suppressSwipe = false;
  let resizeFrame = 0;

  function measure() {
    target.style.zoom = '1';
    target.style.width = '';
    baseWidth = target.getBoundingClientRect().width;
    target.style.width = `${baseWidth}px`;
    target.style.zoom = String(scale);
  }
  function notifyLayout() {
    if (!target.matches('.twilight-page-stage, .twilight-comic')) return;
    cancelAnimationFrame(resizeFrame);
    resizeFrame = requestAnimationFrame(() => window.dispatchEvent(new Event('resize')));
  }
  function setScale(value, anchor) {
    const old = scale;
    scale = clamp(value);
    if (!baseWidth) measure();
    target.style.zoom = String(scale);
    viewport.classList.toggle('is-zoomed', scale > 1);
    viewport.classList.toggle('is-zoomed-out', scale < 1);
    if (anchor && old !== scale) {
      const rect = viewport.getBoundingClientRect();
      const x = anchor.x - rect.left + viewport.scrollLeft;
      const y = anchor.y - rect.top + viewport.scrollTop;
      const ratio = scale / old;
      viewport.scrollLeft = x * ratio - (anchor.x - rect.left);
      viewport.scrollTop = y * ratio - (anchor.y - rect.top);
    }
    try { sessionStorage.setItem(key, String(scale)); } catch { /* Storage is optional. */ }
    notifyLayout();
  }
  measure();
  setScale(scale);
  window.addEventListener('keydown', (event) => {
    if (event.ctrlKey || event.metaKey || event.altKey || event.repeat) return;
    if (event.target.closest('input, select, textarea, [contenteditable="true"], dialog[open]')) return;
    if (event.key === '+' || event.code === 'NumpadAdd' || (event.key === '=' && !event.shiftKey)) {
      event.preventDefault(); setScale(scale + .25);
    } else if (event.key === '-' || event.key === '_' || event.code === 'NumpadSubtract') {
      event.preventDefault(); setScale(scale - .25);
    } else if (event.key === '0' || event.code === 'Numpad0') {
      event.preventDefault(); setScale(1);
    }
  });
  window.addEventListener('resize', () => {
    // An unchanged layout does not need a second measurement or a resize event.
    const available = viewport.clientWidth;
    if (Math.abs(available - (viewport._zoomAvailable || 0)) < 2) return;
    viewport._zoomAvailable = available;
    measure();
  });
  viewport._zoomAvailable = viewport.clientWidth;

  const distance = (a, b) => Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
  viewport.addEventListener('touchstart', (event) => {
    if (event.touches.length !== 2) return;
    pinch = { distance: distance(event.touches[0], event.touches[1]), scale };
    suppressSwipe = true;
  }, { capture: true, passive: true });
  viewport.addEventListener('touchmove', (event) => {
    if (!pinch || event.touches.length !== 2) return;
    event.preventDefault();
    const a = event.touches[0], b = event.touches[1];
    setScale(pinch.scale * distance(a, b) / Math.max(1, pinch.distance), {
      x: (a.clientX + b.clientX) / 2, y: (a.clientY + b.clientY) / 2,
    });
  }, { capture: true, passive: false });
  viewport.addEventListener('touchend', (event) => {
    if (pinch || suppressSwipe || scale > 1) event.stopPropagation();
    if (event.touches.length < 2) pinch = null;
    if (!event.touches.length) suppressSwipe = false;
  }, { capture: true, passive: true });
})();
