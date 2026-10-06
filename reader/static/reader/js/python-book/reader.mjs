import {drawPythonArt} from './art.mjs';

const siteBase = document.documentElement.dataset.siteBase || '';
const bookPath = `${siteBase}/livros/python-do-zero-ao-avancado/`;
const pagePath = `${bookPath}ler/`;
const progressKey = 'voidwielder-python-page';
const resume = document.querySelector('[data-python-resume]');
if (resume) {
  try {
    const saved = Number(localStorage.getItem(progressKey));
    if (saved > 1 && saved <= 281) {
      resume.hidden = false; resume.href = `${pagePath}${saved}/`; resume.textContent = `Retomar na página ${saved} →`;
    }
  } catch { /* Leitura sem armazenamento local. */ }
}

const root = document.querySelector('[data-python-reader]');
if (root) {
  const total = Number(root.dataset.total);
  const spread = root.querySelector('[data-python-spread]');
  const left = root.querySelector('[data-python-content="left"]');
  const right = root.querySelector('[data-python-content="right"]');
  const rightSheet = root.querySelector('[data-python-right]');
  const prev = root.querySelector('[data-python-prev]');
  const next = root.querySelector('[data-python-next]');
  const jump = root.querySelector('[data-python-jump]');
  const select = root.querySelector('[data-python-lesson-select]');
  const part = root.querySelector('[data-python-part]');
  const lesson = root.querySelector('[data-python-lesson]');
  const progress = root.querySelector('[data-python-progress]');
  const panel = root.querySelector('[data-exercise-panel]');
  const editor = root.querySelector('[data-python-code]');
  const prompt = root.querySelector('[data-exercise-prompt]');
  const exerciseNumber = root.querySelector('[data-exercise-number]');
  const status = root.querySelector('[data-python-status]');
  const output = root.querySelector('[data-python-output]');
  const testsList = root.querySelector('[data-python-tests]');
  const solution = root.querySelector('[data-python-solution]');
  const solutionToggle = root.querySelector('[data-python-solution-toggle]');
  const mobile = matchMedia('(max-width: 780px)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let current = Number(root.dataset.page);
  let pages = null;
  let exercises = null;
  let activeExercise = null;
  let turning = false;
  let touchX = 0;
  let worker = null;
  let ready = null;
  let requestId = 0;
  const clamp = (number) => Math.max(1, Math.min(total, number));
  const draftKey = (number) => `voidwielder-python-exercise-${number}`;

  function fill(container, page) {
    container.replaceChildren();
    if (!page) return;
    const kicker = document.createElement('span'); kicker.className = 'python-page-kicker';
    kicker.textContent = page.part_number ? `PARTE ${String(page.part_number).padStart(2, '0')} · LIÇÃO ${String(page.lesson_number).padStart(2, '0')}` : 'ANTES DE COMEÇAR';
    const heading = document.createElement('h1'); heading.textContent = page.section_title;
    container.append(kicker, heading);
    if (page.diagram) {
      const canvas = document.createElement('canvas'); canvas.width = 620; canvas.height = 180;
      canvas.className = 'python-diagram'; canvas.dataset.pythonArt = page.diagram;
      canvas.setAttribute('role', 'img'); canvas.setAttribute('aria-label', `Diagrama de ${page.diagram}; o texto da página explica as etapas`);
      container.append(canvas); drawPythonArt(canvas);
    }
    const body = document.createElement('div'); body.className = 'python-page-body';
    body.innerHTML = page.body_html; container.append(body);
    const number = document.createElement('span'); number.className = 'python-page-number'; number.textContent = page.number;
    container.append(number);
  }

  function showExercise(number) {
    const exercise = exercises?.[number - 1];
    if (!exercise) { panel.hidden = true; prompt.textContent = 'Avance até a primeira lição para começar a programar.'; activeExercise = null; return; }
    panel.hidden = false;
    if (activeExercise?.lesson === number) return;
    activeExercise = exercise;
    exerciseNumber.textContent = String(number).padStart(2, '0');
    prompt.textContent = exercise.prompt;
    try { editor.value = localStorage.getItem(draftKey(number)) ?? exercise.starter; }
    catch { editor.value = exercise.starter; }
    status.textContent = 'Pronto para tentar.';
    output.textContent = '';
    testsList.replaceChildren();
    solution.hidden = true; solutionToggle.setAttribute('aria-expanded', 'false');
    solutionToggle.textContent = 'Ver solução explicada';
    root.querySelector('[data-python-solution-code]').textContent = exercise.solution;
    root.querySelector('[data-python-explanation]').textContent = exercise.explanation;
  }

  function render(number) {
    current = clamp(number); root.dataset.page = current;
    const page = pages[current - 1]; fill(left, page); fill(right, pages[current]);
    rightSheet.hidden = current === total;
    part.textContent = page.part_number ? `Parte ${String(page.part_number).padStart(2, '0')} · ${page.part_title}` : 'Abertura';
    lesson.textContent = page.lesson_title;
    select.value = String(page.lesson_number ? 9 + (page.lesson_number - 1) * 7 : 1);
    jump.value = current;
    progress.setAttribute('aria-valuenow', String(current));
    progress.querySelector('span').style.width = `${current / total * 100}%`;
    const step = mobile.matches ? 1 : 2;
    prev.hidden = current === 1; prev.href = `${pagePath}${clamp(current - step)}/`;
    const atEnd = current + step > total;
    next.href = atEnd ? bookPath : `${pagePath}${current + step}/`;
    next.textContent = atEnd ? 'Voltar ao sumário →' : 'Próxima →';
    showExercise(page.lesson_number);
    try { localStorage.setItem(progressKey, String(current)); } catch { /* Progresso opcional. */ }
    document.title = `Página ${current} · Python: do zero ao avançado · Voidwielder`;
  }

  async function turn(target, direction = 'next', replace = false) {
    if (!pages || turning || target < 1 || target > total || target === current) return;
    turning = true;
    if (!reduced.matches) { spread.classList.add(`is-turning-${direction}`); await new Promise((resolve) => setTimeout(resolve, 180)); }
    render(target);
    history[replace ? 'replaceState' : 'pushState']({page: target}, '', `${pagePath}${target}/`);
    if (!reduced.matches) await new Promise((resolve) => setTimeout(resolve, 200));
    spread.classList.remove('is-turning-next', 'is-turning-prev'); turning = false;
  }

  function createWorker() {
    worker?.terminate();
    worker = new Worker(new URL('./worker.mjs', import.meta.url), {type: 'module'});
    ready = new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(Error('O interpretador demorou a carregar. Confira a conexão e tente novamente.')), 60000);
      const onMessage = ({data}) => {
        if (data.type !== 'ready' && data.type !== 'init-error') return;
        clearTimeout(timer); worker.removeEventListener('message', onMessage);
        if (data.type === 'ready') resolve(); else reject(Error('Não foi possível carregar Python neste navegador.'));
      };
      worker.addEventListener('message', onMessage);
      worker.addEventListener('error', () => { clearTimeout(timer); reject(Error('Falha ao iniciar o interpretador.')); }, {once: true});
    });
    return ready;
  }

  async function execute(grade) {
    if (!activeExercise) return;
    const buttons = [...root.querySelectorAll('[data-python-run], [data-python-grade]')];
    buttons.forEach((button) => { button.disabled = true; });
    status.textContent = ready ? 'Executando…' : 'Carregando Python pela primeira vez…';
    output.textContent = ''; testsList.replaceChildren();
    try {
      await (ready || createWorker());
      const id = ++requestId;
      const payload = {code: editor.value, grade, tests: grade ? activeExercise.tests : []};
      const result = await new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          worker.terminate(); worker = null; ready = null;
          reject(Error('Tempo esgotado. Verifique se há um laço infinito e tente novamente.'));
        }, 6000);
        const onMessage = ({data}) => {
          if (data.type !== 'result' || data.id !== id) return;
          clearTimeout(timer); worker.removeEventListener('message', onMessage); resolve(data.payload);
        };
        worker.addEventListener('message', onMessage);
        worker.postMessage({type: 'execute', id, payload});
      });
      output.textContent = result.output || (result.error ? result.error : 'Sem saída impressa.');
      if (result.error) { status.textContent = 'O código apresentou um erro. Leia a mensagem abaixo e tente novamente.'; output.textContent = result.error; }
      else if (!grade) status.textContent = 'Executado sem erros. Clique em Corrigir para conferir os casos de teste.';
      else {
        const passed = result.results.filter((item) => item.passed).length;
        status.textContent = passed === result.results.length ? `Muito bem! ${passed} de ${passed} testes passaram.` : `${passed} de ${result.results.length} testes passaram. Revise os casos abaixo.`;
        result.results.forEach((item) => {
          const li = document.createElement('li'); li.className = item.passed ? 'is-pass' : 'is-fail';
          li.textContent = `${item.passed ? '✓' : '×'} ${item.label}${item.error ? ` — ${item.error}` : ''}`;
          testsList.append(li);
        });
      }
    } catch (error) {
      status.textContent = error.message;
    } finally { buttons.forEach((button) => { button.disabled = false; }); }
  }

  editor.addEventListener('input', () => { if (activeExercise) { try { localStorage.setItem(draftKey(activeExercise.lesson), editor.value); } catch { /* Rascunho opcional. */ } } });
  editor.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    event.preventDefault(); const start = editor.selectionStart;
    editor.setRangeText('    ', start, editor.selectionEnd, 'end'); editor.dispatchEvent(new Event('input'));
  });
  root.querySelector('[data-python-run]').addEventListener('click', () => execute(false));
  root.querySelector('[data-python-grade]').addEventListener('click', () => execute(true));
  root.querySelector('[data-python-reset]').addEventListener('click', () => {
    if (!activeExercise) return; editor.value = activeExercise.starter; editor.dispatchEvent(new Event('input'));
    status.textContent = 'Rascunho reiniciado.'; output.textContent = ''; testsList.replaceChildren();
  });
  solutionToggle.addEventListener('click', () => {
    solution.hidden = !solution.hidden;
    solutionToggle.setAttribute('aria-expanded', String(!solution.hidden));
    solutionToggle.textContent = solution.hidden ? 'Ver solução explicada' : 'Ocultar solução';
  });

  Promise.all([
    fetch(`${siteBase}/static/reader/book/python/pages.json`).then((response) => { if (!response.ok) throw Error('Páginas indisponíveis'); return response.json(); }),
    fetch(`${siteBase}/static/reader/book/python/exercises.json`).then((response) => { if (!response.ok) throw Error('Exercícios indisponíveis'); return response.json(); }),
  ]).then(([bookPages, tasks]) => {
    if (bookPages.length !== total || tasks.length !== 39) throw Error('Livro incompleto');
    pages = bookPages; exercises = tasks; render(current);
    prev.addEventListener('click', (event) => { event.preventDefault(); turn(current - (mobile.matches ? 1 : 2), 'prev'); });
    next.addEventListener('click', (event) => { if (next.href.endsWith(bookPath)) return; event.preventDefault(); turn(current + (mobile.matches ? 1 : 2)); });
    jump.addEventListener('change', () => turn(clamp(Number(jump.value) || current), Number(jump.value) < current ? 'prev' : 'next'));
    select.addEventListener('change', () => turn(Number(select.value), Number(select.value) < current ? 'prev' : 'next'));
    document.addEventListener('keydown', (event) => {
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
      if (event.key === 'ArrowRight') { event.preventDefault(); turn(current + (mobile.matches ? 1 : 2)); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); turn(current - (mobile.matches ? 1 : 2), 'prev'); }
    });
    spread.addEventListener('touchstart', (event) => { touchX = event.changedTouches[0].screenX; }, {passive: true});
    spread.addEventListener('touchend', (event) => { const dx = event.changedTouches[0].screenX - touchX; if (Math.abs(dx) > 55) turn(current + (dx < 0 ? 1 : -1), dx < 0 ? 'next' : 'prev'); }, {passive: true});
    window.addEventListener('popstate', () => { const page = Number(location.pathname.match(/ler\/(\d+)\/$/)?.[1]); if (page) render(page); });
    mobile.addEventListener('change', () => render(current));
  }).catch(() => { status.textContent = 'O modo interativo não carregou. As páginas e os links do livro continuam disponíveis.'; });
}
