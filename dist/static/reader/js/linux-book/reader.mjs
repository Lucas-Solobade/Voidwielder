import { drawLinuxArt } from './art.mjs';

const path = '/livros/linux-do-zero-ao-avancado/ler/';
const storageKey = 'voidwielder-linux-page';
const resume = document.querySelector('[data-linux-resume]');
if (resume) {
  try {
    const saved = Number(localStorage.getItem(storageKey));
    if (saved > 1 && saved <= 554) { resume.hidden = false; resume.href = `${path}${saved}/`; resume.textContent = `Retomar na página ${saved} →`; }
  } catch { /* Reading still works without local storage. */ }
}

const root = document.querySelector('[data-linux-reader]');
if (root) {
  const total = Number(root.dataset.total);
  const spread = root.querySelector('[data-linux-spread]');
  const left = root.querySelector('[data-linux-content="left"]');
  const right = root.querySelector('[data-linux-content="right"]');
  const rightSheet = root.querySelector('[data-linux-right]');
  const prev = root.querySelector('[data-linux-prev]');
  const next = root.querySelector('[data-linux-next]');
  const jump = root.querySelector('[data-linux-jump]');
  const select = root.querySelector('[data-linux-lesson-select]');
  const part = root.querySelector('[data-linux-part]');
  const lesson = root.querySelector('[data-linux-lesson]');
  const progress = root.querySelector('[data-linux-progress]');
  const mobile = matchMedia('(max-width: 780px)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let current = Number(root.dataset.page);
  let pages = null;
  let turning = false;
  let touchX = 0;
  const clamp = (n) => Math.max(1, Math.min(total, n));
  function fill(container, page) {
    container.replaceChildren();
    if (!page) return;
    const kicker = document.createElement('span'); kicker.className = 'linux-page-kicker';
    kicker.textContent = page.part_number ? `PARTE ${String(page.part_number).padStart(2, '0')} · LIÇÃO ${String(page.lesson_number).padStart(2, '0')}` : 'ANTES DE COMEÇAR';
    const heading = document.createElement('h1'); heading.textContent = page.section_title;
    container.append(kicker, heading);
    if (page.diagram) {
      const canvas = document.createElement('canvas'); canvas.width = 620; canvas.height = 180; canvas.className = 'linux-diagram';
      canvas.dataset.linuxArt = page.diagram; canvas.setAttribute('role', 'img');
      canvas.setAttribute('aria-label', `Diagrama de ${page.diagram}; o texto da página explica as etapas`);
      container.append(canvas); drawLinuxArt(canvas);
    }
    const body = document.createElement('p'); body.innerHTML = page.body_html; container.append(body);
    const number = document.createElement('span'); number.className = 'linux-page-number'; number.textContent = page.number; container.append(number);
  }
  function render(n) {
    current = clamp(n); root.dataset.page = current;
    const page = pages[current - 1]; fill(left, page); fill(right, pages[current]);
    rightSheet.hidden = current === total;
    part.textContent = page.part_number ? `Parte ${String(page.part_number).padStart(2, '0')} · ${page.part_title}` : 'Abertura';
    lesson.textContent = page.lesson_title;
    select.value = String(page.lesson_number ? 9 + (page.lesson_number - 1) * 7 : 1);
    jump.value = current;
    progress.setAttribute('aria-valuenow', String(current));
    progress.querySelector('span').style.width = `${current / total * 100}%`;
    const step = mobile.matches ? 1 : 2;
    prev.hidden = current === 1; prev.href = `${path}${clamp(current - step)}/`;
    const atEnd = current + step > total;
    next.href = atEnd ? '/livros/linux-do-zero-ao-avancado/' : `${path}${current + step}/`;
    next.textContent = atEnd ? 'Voltar ao sumário →' : 'Próxima →';
    try { localStorage.setItem(storageKey, String(current)); } catch { /* Optional progress. */ }
    document.title = `Página ${current} · Linux: do zero ao avançado · Voidwielder`;
  }
  async function turn(target, direction = 'next', replace = false) {
    if (!pages || turning || target < 1 || target > total || target === current) return;
    turning = true;
    if (!reduced.matches) { spread.classList.add(`is-turning-${direction}`); await new Promise((resolve) => setTimeout(resolve, 210)); }
    render(target);
    history[replace ? 'replaceState' : 'pushState']({ page: target }, '', `${path}${target}/`);
    if (!reduced.matches) await new Promise((resolve) => setTimeout(resolve, 240));
    spread.classList.remove('is-turning-next', 'is-turning-prev'); turning = false;
  }
  fetch('/static/reader/book/linux/pages.json').then((response) => {
    if (!response.ok) throw Error('Páginas indisponíveis'); return response.json();
  }).then((data) => {
    if (!Array.isArray(data) || data.length !== total) throw Error('Livro incompleto');
    pages = data; render(current);
    prev.addEventListener('click', (event) => { event.preventDefault(); turn(current - (mobile.matches ? 1 : 2), 'prev'); });
    next.addEventListener('click', (event) => { if (next.href.endsWith('/livros/linux-do-zero-ao-avancado/')) return; event.preventDefault(); turn(current + (mobile.matches ? 1 : 2)); });
    jump.addEventListener('change', () => turn(clamp(Number(jump.value) || current), Number(jump.value) < current ? 'prev' : 'next'));
    select.addEventListener('change', () => turn(Number(select.value), Number(select.value) < current ? 'prev' : 'next'));
    document.addEventListener('keydown', (event) => {
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
      if (event.key === 'ArrowRight') { event.preventDefault(); turn(current + (mobile.matches ? 1 : 2)); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); turn(current - (mobile.matches ? 1 : 2), 'prev'); }
    });
    spread.addEventListener('touchstart', (event) => { touchX = event.changedTouches[0].screenX; }, { passive: true });
    spread.addEventListener('touchend', (event) => { const dx = event.changedTouches[0].screenX - touchX; if (Math.abs(dx) > 55) turn(current + (dx < 0 ? 1 : -1), dx < 0 ? 'next' : 'prev'); }, { passive: true });
    window.addEventListener('popstate', () => { const n = Number(location.pathname.match(/ler\/(\d+)\/$/)?.[1]); if (n) render(n); });
    mobile.addEventListener('change', () => render(current));
  }).catch(() => { /* Server-rendered text and links remain available. */ });
}
