import { drawScene } from './art.mjs';
const root = document.querySelector('[data-book-reader]');
const resume = document.querySelector('[data-book-resume]');
const storageKey = 'voidwielder-casa-medidas-page';
const path = '/livros/a-casa-das-medidas/ler/';
if (resume) {
  const saved = Number(localStorage.getItem(storageKey));
  if (saved > 1 && saved <= 150) { resume.hidden = false; resume.href = `${path}${saved}/`; resume.textContent = `Retomar na página ${saved} →`; }
}
if (root) {
  const total = Number(root.dataset.total);
  const spread = root.querySelector('[data-book-spread]');
  const left = root.querySelector('[data-page-content="left"]');
  const right = root.querySelector('[data-page-content="right"]');
  const rightSheet = root.querySelector('[data-sheet-right]');
  const leftSheet = root.querySelector('[data-sheet-left]');
  const prev = root.querySelector('[data-book-prev]');
  const next = root.querySelector('[data-book-next]');
  const finish = root.querySelector('[data-book-finish]');
  const jump = root.querySelector('[data-page-jump]');
  const chapters = root.querySelector('[data-chapter-select]');
  const chapterLabel = root.querySelector('[data-reader-chapter]');
  const position = root.querySelector('[data-reader-position]');
  const progress = root.querySelector('[data-book-progress]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = matchMedia('(max-width: 740px)');
  let current = Number(root.dataset.page);
  let pages = null;
  let turning = false;
  let touchX = 0;
  const safe = (n) => Math.max(1, Math.min(total, n));
  function fill(container, page) {
    container.replaceChildren();
    if (!page) return;
    if (page.chapter_start) {
      const eyebrow = document.createElement('span'); eyebrow.className = 'book-chapter-number'; eyebrow.textContent = `CAPÍTULO ${String(page.chapter_number).padStart(2, '0')}`;
      const heading = document.createElement('h1'); heading.textContent = page.chapter_title;
      container.append(eyebrow, heading);
      if ([1, 7, 13].includes(page.chapter_number)) {
        const art = document.createElement('canvas'); art.className = 'book-illustration'; art.width = 580; art.height = 170;
        art.dataset.bookArt = 'scene'; art.dataset.scene = String(page.chapter_number);
        art.setAttribute('role', 'img'); art.setAttribute('aria-label', 'Ilustração em nanquim do capítulo');
        container.append(art); drawScene(art);
      }
    }
    page.paragraphs.forEach((text) => { const p = document.createElement('p'); p.textContent = text; container.append(p); });
    if (page.number === total) { const end = document.createElement('p'); end.className = 'book-endmark'; end.textContent = 'FIM'; container.append(end); }
    const number = document.createElement('span'); number.className = 'book-page-number'; number.textContent = page.number; container.append(number);
  }
  function render(n) {
    current = safe(n); root.dataset.page = current;
    fill(left, pages[current - 1]); fill(right, pages[current]);
    rightSheet.hidden = current >= total;
    leftSheet.setAttribute('aria-label', `Página ${current}`);
    rightSheet.setAttribute('aria-label', `Página ${Math.min(total, current + 1)}`);
    chapterLabel.textContent = pages[current - 1].chapter_title;
    position.textContent = `Página ${current} de ${total}`;
    jump.value = current;
    const chapter = pages[current - 1].chapter_number;
    chapters.value = String((chapter - 1) * 10 + 1);
    progress.setAttribute('aria-valuenow', String(current));
    progress.querySelector('span').style.width = `${current / total * 100}%`;
    if (prev) { prev.href = `${path}${safe(current - (mobile.matches ? 1 : 2))}/`; prev.hidden = current === 1; }
    if (next) { next.href = `${path}${safe(current + (mobile.matches ? 1 : 2))}/`; next.hidden = current >= total - (mobile.matches ? 0 : 1); }
    finish.hidden = current < total - (mobile.matches ? 0 : 1);
    try { localStorage.setItem(storageKey, String(current)); } catch { /* Optional progress. */ }
    document.title = `Página ${current} · A Casa das Medidas · Voidwielder`;
  }
  async function turn(target, direction = 'next', replace = false) {
    if (!pages || turning || target < 1 || target > total || target === current) return;
    turning = true;
    if (!reduced.matches) { spread.classList.add(`is-turning-${direction}`); await new Promise((resolve) => setTimeout(resolve, 220)); }
    render(target);
    history[replace ? 'replaceState' : 'pushState']({ page: target }, '', `${path}${target}/`);
    if (!reduced.matches) await new Promise((resolve) => setTimeout(resolve, 240));
    spread.classList.remove('is-turning-next', 'is-turning-prev'); turning = false;
  }
  fetch('/static/reader/book/casa-medidas/pages.json').then((r) => { if (!r.ok) throw Error('pages'); return r.json(); }).then((data) => {
    if (!Array.isArray(data) || data.length !== total) throw Error('pages');
    pages = data; render(current);
    prev?.addEventListener('click', (event) => { event.preventDefault(); turn(current - (mobile.matches ? 1 : 2), 'prev'); });
    next?.addEventListener('click', (event) => { event.preventDefault(); turn(current + (mobile.matches ? 1 : 2)); });
    chapters.addEventListener('change', () => turn(Number(chapters.value), Number(chapters.value) < current ? 'prev' : 'next'));
    jump.addEventListener('change', () => turn(safe(Number(jump.value) || current), Number(jump.value) < current ? 'prev' : 'next'));
    document.addEventListener('keydown', (event) => {
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
      if (event.key === 'ArrowRight') { event.preventDefault(); turn(current + (mobile.matches ? 1 : 2)); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); turn(current - (mobile.matches ? 1 : 2), 'prev'); }
    });
    spread.addEventListener('touchstart', (event) => { touchX = event.changedTouches[0].screenX; }, { passive: true });
    spread.addEventListener('touchend', (event) => { const dx = event.changedTouches[0].screenX - touchX; if (Math.abs(dx) > 55) turn(current + (dx < 0 ? 1 : -1), dx < 0 ? 'next' : 'prev'); }, { passive: true });
    window.addEventListener('popstate', () => { const n = Number(location.pathname.match(/ler\/(\d+)\/$/)?.[1]); if (n) render(n); });
    mobile.addEventListener('change', () => render(current));
  }).catch(() => { /* Server-rendered pages and links remain usable. */ });
}
