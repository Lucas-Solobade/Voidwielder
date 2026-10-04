const menuButton = document.querySelector('[data-menu-button]');
const menu = document.querySelector('[data-menu]');
const backdrop = document.querySelector('[data-backdrop]');
const closeButton = document.querySelector('[data-menu-close]');

function setMenu(open) {
  if (!menuButton || !menu || !backdrop) return;
  menu.hidden = !open;
  backdrop.hidden = !open;
  menuButton.setAttribute('aria-expanded', String(open));
  document.body.classList.toggle('menu-open', open);
  (open ? closeButton : menuButton)?.focus();
}

menuButton?.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
closeButton?.addEventListener('click', () => setMenu(false));
backdrop?.addEventListener('click', () => setMenu(false));

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
  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    window.location.assign(`/buscar/?q=${encodeURIComponent(input?.value.trim() || '')}`);
  });
  if (query) {
    fetch('/catalog.json')
      .then((response) => response.json())
      .then((records) => {
        const needle = query.toLocaleLowerCase('pt-BR');
        const results = records.filter((record) => `${record.title} ${record.detail} ${record.number || ''}`.toLocaleLowerCase('pt-BR').includes(needle));
        const heading = document.createElement('h2');
        heading.textContent = `${results.length} resultado${results.length === 1 ? '' : 's'} para “${query}”`;
        staticSearch.append(heading);
        const list = document.createElement('div');
        list.className = 'results';
        list.innerHTML = results.length
          ? results.map((result) => `<a href="${result.url}"><span>${result.kind}</span><strong>${result.title}</strong><p>${result.detail}</p></a>`).join('')
          : '<p class="empty-state">Nada encontrado. Tente o nome de um arco ou capítulo.</p>';
        staticSearch.append(list);
      });
  }
}
