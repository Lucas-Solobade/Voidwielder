import { drawScene } from './art.mjs';

const root = document.querySelector('[data-novel-reader]');
const resume = document.querySelector('[data-novel-resume]');
const siteBase = document.documentElement.dataset.siteBase || '';
const bookRoot = `${siteBase}/livros/as-estradas-do-crepusculo/`;
const path = `${bookRoot}ler/`;
const storageKey = 'voidwielder-estradas-novel-page';

if (resume) {
  try {
    const saved = Number(localStorage.getItem(storageKey));
    if (saved > 1) {
      resume.hidden = false;
      resume.href = `${path}${saved}/`;
      resume.textContent = `Retomar na página ${saved} →`;
    }
  } catch { /* Reading progress is optional. */ }
}

if (root) {
  const total = Number(root.dataset.total);
  const complete = root.dataset.complete === 'true';
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
  const safe = (number) => Math.max(1, Math.min(total, number));
  const step = () => mobile.matches ? 1 : 2;

  function fill(container, page) {
    container.replaceChildren();
    if (!page) return;
    if (page.chapter_start) {
      const eyebrow = document.createElement('span');
      eyebrow.className = 'book-chapter-number';
      eyebrow.textContent = `CAPÍTULO ${String(page.chapter_number).padStart(2, '0')}`;
      const heading = document.createElement('h1');
      heading.textContent = page.chapter_title;
      container.append(eyebrow, heading);
    }
    if (page.illustration) {
      const art = document.createElement('canvas');
      art.className = 'novel-illustration';
      art.width = 600; art.height = 200;
      art.dataset.novelArt = 'scene'; art.dataset.scene = page.illustration;
      art.setAttribute('role', 'img');
      art.setAttribute('aria-label', `Gravura em preto e branco: cena do capítulo ${page.chapter_number}`);
      container.append(art);
      drawScene(art);
    }
    page.paragraphs.forEach((value) => {
      const paragraph = document.createElement('p'); paragraph.textContent = value; container.append(paragraph);
    });
    if (page.number === total) {
      const end = document.createElement('p'); end.className = 'book-endmark';
      end.textContent = complete ? 'FIM' : `FIM DO ATO ${root.dataset.arc} · O ROMANCE CONTINUA`;
      container.append(end);
    }
    const number = document.createElement('span');
    number.className = 'book-page-number'; number.textContent = page.number;
    container.append(number);
  }

  function render(number) {
    current = safe(number); root.dataset.page = String(current);
    fill(left, pages[current - 1]); fill(right, pages[current]);
    rightSheet.hidden = current >= total;
    leftSheet.setAttribute('aria-label', `Página ${current}`);
    rightSheet.setAttribute('aria-label', `Página ${Math.min(total, current + 1)}`);
    chapterLabel.textContent = pages[current - 1].chapter_title;
    position.textContent = `Página ${current} de ${total}`;
    jump.value = String(current);
    chapters.value = String((pages[current - 1].chapter_number - 1) * 20 + 1);
    progress.setAttribute('aria-valuenow', String(current));
    progress.querySelector('span').style.width = `${current / total * 100}%`;
    prev.href = `${path}${safe(current - step())}/`; prev.hidden = current === 1;
    next.href = `${path}${safe(current + step())}/`; next.hidden = current >= total - (mobile.matches ? 0 : 1);
    finish.hidden = current < total - (mobile.matches ? 0 : 1);
    try { localStorage.setItem(storageKey, String(current)); } catch { /* Optional. */ }
    document.title = `Página ${current} · As Estradas do Crepúsculo · Voidwielder`;
  }

  async function turn(target, direction = 'next') {
    if (!pages || turning || target < 1 || target > total || target === current) return;
    turning = true;
    if (!reduced.matches) {
      spread.classList.add(`is-turning-${direction}`);
      await new Promise((resolve) => setTimeout(resolve, 220));
    }
    render(target);
    history.pushState({ page: target }, '', `${path}${target}/`);
    if (!reduced.matches) await new Promise((resolve) => setTimeout(resolve, 240));
    spread.classList.remove('is-turning-next', 'is-turning-prev');
    turning = false;
  }

  fetch(`${siteBase}/static/reader/book/estradas-crepusculo/pages.json?v=${total}`)
    .then((response) => { if (!response.ok) throw Error('pages'); return response.json(); })
    .then((data) => {
      if (!Array.isArray(data) || data.length !== total) throw Error('pages');
      pages = data; render(current);
      prev.addEventListener('click', (event) => { event.preventDefault(); turn(current - step(), 'prev'); });
      next.addEventListener('click', (event) => { event.preventDefault(); turn(current + step()); });
      chapters.addEventListener('change', () => {
        const target = Number(chapters.value); turn(target, target < current ? 'prev' : 'next');
      });
      jump.addEventListener('change', () => {
        const target = safe(Number(jump.value) || current); turn(target, target < current ? 'prev' : 'next');
      });
      document.addEventListener('keydown', (event) => {
        if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
        if (event.key === 'ArrowRight') { event.preventDefault(); turn(current + step()); }
        if (event.key === 'ArrowLeft') { event.preventDefault(); turn(current - step(), 'prev'); }
      });
      spread.addEventListener('touchstart', (event) => { touchX = event.changedTouches[0].screenX; }, { passive: true });
      spread.addEventListener('touchend', (event) => {
        const dx = event.changedTouches[0].screenX - touchX;
        if (Math.abs(dx) > 55) turn(current + (dx < 0 ? 1 : -1), dx < 0 ? 'next' : 'prev');
      }, { passive: true });
      window.addEventListener('popstate', () => {
        const number = Number(location.pathname.match(/ler\/(\d+)\/$/)?.[1]);
        if (number) render(number);
      });
      mobile.addEventListener('change', () => render(current));
    })
    .catch(() => { /* Server-rendered pages and links remain readable. */ });
}
