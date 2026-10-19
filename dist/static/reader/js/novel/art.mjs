// One complete monochrome plate opens each illustrated chapter.
const ink = '#181716';
const paper = '#f5f1e8';
const plates = new Map();

function plate(name) {
  if (!plates.has(name)) {
    plates.set(name, new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = reject;
      image.src = new URL(`../../images/novel/${name}`, import.meta.url).href;
    }));
  }
  return plates.get(name);
}

function monochrome(ctx, image, target) {
  ctx.save();
  ctx.filter = 'grayscale(1) contrast(1.12)';
  ctx.drawImage(image, ...target);
  ctx.restore();
}

function border(ctx, width, height) {
  ctx.strokeStyle = ink;
  ctx.lineWidth = 2;
  ctx.strokeRect(3, 3, width - 6, height - 6);
  ctx.lineWidth = .5;
  ctx.strokeRect(9, 9, width - 18, height - 18);
}

export function drawScene(canvas) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const { width, height } = canvas;
  const id = canvas.dataset.scene || '01-1';
  const chapter = Number(id.split('-')[0]);
  ctx.fillStyle = paper;
  ctx.fillRect(0, 0, width, height);
  const filename = id.startsWith('v2-')
    ? `volume-2-chapter-${id.slice(3, 5)}.webp`
    : `chapter-${String(chapter).padStart(2, '0')}.webp`;
  plate(filename).then((image) => {
    ctx.fillStyle = paper;
    ctx.fillRect(0, 0, width, height);
    const scale = Math.min((width - 16) / image.width, (height - 16) / image.height);
    const drawnWidth = image.width * scale;
    const drawnHeight = image.height * scale;
    monochrome(ctx, image, [(width - drawnWidth) / 2, (height - drawnHeight) / 2, drawnWidth, drawnHeight]);
    border(ctx, width, height);
  }).catch(() => {
    ctx.fillStyle = ink;
    ctx.font = 'italic 22px Georgia, serif';
    ctx.textAlign = 'center';
    ctx.fillText('As Estradas do Crepúsculo', width / 2, height / 2);
    border(ctx, width, height);
  });
}

export function drawCover(canvas) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const { width, height } = canvas;
  ctx.fillStyle = paper;
  ctx.fillRect(0, 0, width, height);
  const secondVolume = canvas.dataset.volume === '2';
  plate(secondVolume ? 'volume-2-cover.webp' : 'cover.webp').then((image) => {
    monochrome(ctx, image, [0, 0, width, height]);
    const sky = ctx.createLinearGradient(0, 0, 0, height * .39);
    sky.addColorStop(0, 'rgba(0,0,0,.42)');
    sky.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, width, height * .39);
    ctx.textAlign = 'center';
    ctx.fillStyle = '#fffaf0';
    ctx.font = '700 13px Georgia, serif';
    ctx.letterSpacing = '3px';
    ctx.fillText('VOIDWIELDER', width / 2, height * .09);
    ctx.font = '700 37px Georgia, serif';
    ctx.letterSpacing = '-1px';
    ctx.fillText('AS ESTRADAS', width / 2, height * .16);
    ctx.fillText('DO CREPÚSCULO', width / 2, height * .23);
    ctx.font = '600 15px Georgia, serif';
    ctx.letterSpacing = '3px';
    ctx.fillText(secondVolume ? 'O AVESSO DAS ÁGUAS · VOLUME II' : 'O FERRO QUE ESCUTA', width / 2, height * .285);
    ctx.fillStyle = 'rgba(245,241,232,.96)';
    ctx.fillRect(24, height - 60, width - 48, 37);
    ctx.fillStyle = ink;
    ctx.font = 'italic 16px Georgia, serif';
    ctx.letterSpacing = '0px';
    ctx.fillText(secondVolume ? 'Há caminhos que correm sob a água.' : 'Toda estrada começa com alguém que decide escutar.', width / 2, height - 36);
    border(ctx, width, height);
  }).catch(() => {
    ctx.fillStyle = ink;
    ctx.font = '700 32px Georgia, serif';
    ctx.textAlign = 'center';
    ctx.fillText('As Estradas do Crepúsculo', width / 2, height / 2);
    border(ctx, width, height);
  });
}

document.querySelectorAll('[data-novel-art="cover"]').forEach(drawCover);
document.querySelectorAll('[data-novel-art="scene"]').forEach(drawScene);

function decorateSearch() {
  document.querySelectorAll('[data-static-search-results] a[href$="/livros/as-estradas-do-crepusculo/"], [data-django-search-results] a[href$="/livros/as-estradas-do-crepusculo/"], [data-static-search-results] a[href$="/livros/as-estradas-do-crepusculo-volume-ii/"], [data-django-search-results] a[href$="/livros/as-estradas-do-crepusculo-volume-ii/"]').forEach((link) => {
    if (link.querySelector('canvas')) return;
    link.classList.add('book-card');
    const canvas = document.createElement('canvas');
    canvas.className = 'book-cover';
    canvas.width = 480;
    canvas.height = 720;
    canvas.dataset.volume = link.pathname.includes('volume-ii') ? '2' : '1';
    canvas.setAttribute('role', 'img');
    canvas.setAttribute('aria-label', 'Capa de As Estradas do Crepúsculo');
    link.prepend(canvas);
    drawCover(canvas);
  });
}
decorateSearch();
const search = document.querySelector('[data-static-search-results]');
if (search) new MutationObserver(decorateSearch).observe(search, { childList: true, subtree: true });
