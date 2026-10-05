const menuButton = document.querySelector('[data-menu-button]');
const menu = document.querySelector('[data-menu]');
const backdrop = document.querySelector('[data-backdrop]');
const closeButton = document.querySelector('[data-menu-close]');

function setMenu(open) {
  if (!menuButton || !menu || !backdrop) return;
  menu.hidden = !open;
  backdrop.hidden = !open;
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.querySelector('.sr-only').textContent = open ? 'Fechar menu' : 'Abrir menu';
  document.body.classList.toggle('menu-open', open);
  (open ? closeButton : menuButton)?.focus();
}

menuButton?.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
closeButton?.addEventListener('click', () => setMenu(false));
backdrop?.addEventListener('click', () => setMenu(false));
menu?.addEventListener('click', (event) => {
  if (event.target.closest('a')) setMenu(false);
});

const dialog = document.querySelector('[data-search-dialog]');
document.querySelector('[data-search-open]')?.addEventListener('click', () => dialog?.showModal());
document.querySelector('[data-search-close]')?.addEventListener('click', () => dialog?.close());

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') setMenu(false);
  if (!document.querySelector('[data-reader]') || ['INPUT', 'SELECT'].includes(document.activeElement?.tagName)) return;
  const link = event.key === 'ArrowLeft' ? document.querySelector('[rel="prev"]') : event.key === 'ArrowRight' ? document.querySelector('[rel="next"]') : null;
  if (link) window.location.assign(link.href);
});

const reader = document.querySelector('[data-reader]');
if (reader) {
  localStorage.setItem('homus-bananus-progress', JSON.stringify({ page: Number(reader.dataset.page), arc: reader.dataset.arc }));
  document.querySelector('[data-page-select]')?.addEventListener('change', (event) => window.location.assign(event.target.value));
  document.querySelector('[data-fit-button]')?.addEventListener('click', () => document.body.classList.toggle('wide-reader'));
}

const staticSearch = document.querySelector('[data-static-search-results]');
if (document.documentElement.hasAttribute('data-static-export') && staticSearch) {
  const form = document.querySelector('.search-form-page');
  const input = document.querySelector('#page-search');
  const query = new URLSearchParams(window.location.search).get('q')?.trim() || '';
  const requestedCategory = new URLSearchParams(window.location.search).get('tipo') || 'todos';
  const category = ['todos', 'livros', 'hq', 'jogos', 'estudos'].includes(requestedCategory) ? requestedCategory : 'todos';
  document.querySelector('.search-page')?.toggleAttribute('data-hq-browse', category === 'hq' && !query);
  const categoryTitle = document.querySelector('[data-category-title]');
  if (categoryTitle) categoryTitle.textContent = {
    todos: 'Explore o catálogo', livros: 'Livros', hq: 'HQs', jogos: 'Jogos', estudos: 'Estudos',
  }[category];
  if (input) input.value = query;
  document.querySelectorAll('.category-tabs a').forEach((link) => {
    const linkCategory = new URL(link.href).searchParams.get('tipo') || 'todos';
    if (linkCategory === category) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
    if (query) {
      const url = new URL(link.href);
      url.searchParams.set('q', query);
      link.href = url.toString();
    }
  });
  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    const params = new URLSearchParams({ q: input?.value.trim() || '', tipo: category });
    window.location.assign(`/buscar/?${params}`);
  });
  fetch('/catalog.json')
      .then((response) => {
        if (!response.ok) throw new Error('Falha ao carregar catálogo');
        return response.json();
      })
      .then((records) => {
        const needle = query.toLocaleLowerCase('pt-BR');
        const results = records.filter((record) => (
          (category === 'todos' || record.category === category)
          && (query || !['Arco', 'Capítulo'].includes(record.kind))
          && `${record.title} ${record.detail} ${record.topics || ''} ${record.number || ''}`.toLocaleLowerCase('pt-BR').includes(needle)
        ));
        const heading = document.createElement('h2');
        heading.textContent = `${results.length} resultado${results.length === 1 ? '' : 's'}${query ? ` para “${query}”` : ''}`;
        staticSearch.append(heading);
        const list = document.createElement('div');
        list.className = 'results';
        if (results.length) {
          results.forEach((result) => {
            const link = document.createElement('a');
            link.href = result.url;
            if (result.kind === 'Jogo') link.className = 'game-card';
            if (result.cover) {
              link.className = 'series-card';
              const cover = document.createElement('img');
              cover.src = `/static/${result.cover}`;
              cover.alt = `Capa da HQ ${result.title}`;
              cover.loading = 'lazy';
              cover.width = 1672;
              cover.height = 941;
              link.append(cover);
            }
            const copy = document.createElement('span');
            copy.className = 'result-copy';
            const kind = document.createElement('span');
            kind.textContent = result.kind;
            const title = document.createElement('strong');
            title.textContent = result.title;
            const detail = document.createElement('span');
            detail.className = 'result-detail';
            detail.textContent = result.detail;
            copy.append(kind, title, detail);
            if (result.cover) {
              const action = document.createElement('span');
              action.className = 'result-action';
              action.textContent = 'Explorar HQ →';
              copy.append(action);
            }
            link.append(copy);
            list.append(link);
          });
        } else {
          const empty = document.createElement('p');
          empty.className = 'empty-state';
          empty.textContent = category === 'livros' ? 'Ainda não há títulos nesta categoria.' : 'Nada encontrado. Tente outro título ou assunto.';
          list.append(empty);
        }
        staticSearch.append(list);
      })
      .catch(() => { staticSearch.textContent = 'Não foi possível carregar o catálogo. Tente novamente.'; });
}

const studySteps = [...document.querySelectorAll('[data-study-step]')];
if (studySteps.length) {
  const storageKey = 'voidwielder-study-progress-v1';
  let completed = [];
  try {
    const stored = JSON.parse(localStorage.getItem(storageKey) || localStorage.getItem('homus-bananus-study-progress-v1') || '[]');
    if (Array.isArray(stored)) completed = stored.filter((step) => studySteps.some((input) => input.dataset.studyStep === step));
  } catch { /* Reading progress is optional. */ }
  const progressText = document.querySelector('[data-study-progress]');
  const progressBar = document.querySelector('[data-study-progress-bar]');
  const updateProgress = () => {
    const count = studySteps.filter((input) => input.checked).length;
    if (progressText) progressText.textContent = `${count} de ${studySteps.length} etapas concluídas`;
    if (progressBar) {
      progressBar.setAttribute('aria-valuenow', String(count));
      progressBar.querySelector('span').style.width = `${(count / studySteps.length) * 100}%`;
    }
  };
  studySteps.forEach((input) => {
    input.checked = completed.includes(input.dataset.studyStep);
    input.addEventListener('change', () => {
      completed = studySteps.filter((step) => step.checked).map((step) => step.dataset.studyStep);
      try { localStorage.setItem(storageKey, JSON.stringify(completed)); } catch { /* Keep checkboxes usable without storage. */ }
      updateProgress();
    });
  });
  updateProgress();
}
