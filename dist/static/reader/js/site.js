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
  const category = new URLSearchParams(window.location.search).get('tipo') || 'todos';
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
        const results = records.filter((record) => (category === 'todos' || record.category === category) && `${record.title} ${record.detail} ${record.number || ''}`.toLocaleLowerCase('pt-BR').includes(needle));
        const heading = document.createElement('h2');
        heading.textContent = `${results.length} resultado${results.length === 1 ? '' : 's'}${query ? ` para “${query}”` : ''}`;
        staticSearch.append(heading);
        const list = document.createElement('div');
        list.className = 'results';
        if (results.length) {
          results.forEach((result) => {
            const link = document.createElement('a');
            link.href = result.url;
            const kind = document.createElement('span');
            kind.textContent = result.kind;
            const title = document.createElement('strong');
            title.textContent = result.title;
            const detail = document.createElement('p');
            detail.textContent = result.detail;
            link.append(kind, title, detail);
            list.append(link);
          });
        } else {
          const empty = document.createElement('p');
          empty.className = 'empty-state';
          empty.textContent = ['livros', 'jogos', 'estudos'].includes(category) ? 'Ainda não há títulos nesta categoria.' : 'Nada encontrado. Tente outro título, arco ou capítulo.';
          list.append(empty);
        }
        staticSearch.append(list);
      })
      .catch(() => { staticSearch.textContent = 'Não foi possível carregar o catálogo. Tente novamente.'; });
}
