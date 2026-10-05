function drawCover(canvas) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const { width: w, height: h } = canvas;
  ctx.fillStyle = '#e9e4d7'; ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = '#17171b'; ctx.fillRect(19, 19, w - 38, h - 38);
  ctx.strokeStyle = '#a7a293'; ctx.lineWidth = 1;
  for (let i = 0; i < 60; i++) {
    const x = 36 + ((i * 73) % (w - 72));
    const y = 38 + ((i * 127) % (h - 76));
    ctx.globalAlpha = .08 + (i % 3) * .02;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 35, y - 7); ctx.stroke();
  }
  ctx.globalAlpha = 1;
  ctx.strokeStyle = '#d5d0c0'; ctx.lineWidth = 2;
  ctx.strokeRect(48, 51, w - 96, h - 102);
  ctx.fillStyle = '#eae5d8'; ctx.font = 'bold 13px Arial'; ctx.letterSpacing = '4px';
  ctx.textAlign = 'center'; ctx.fillText('HELENA BASTOS', w / 2, 95);
  ctx.font = '46px Georgia'; ctx.letterSpacing = '-1px';
  ctx.fillText('A CASA', w / 2, 172); ctx.fillText('DAS', w / 2, 227); ctx.fillText('MEDIDAS', w / 2, 282);
  ctx.strokeStyle = '#f0eadb'; ctx.lineWidth = 2;
  const bx = 101, by = 352, bw = 278, bh = 226;
  ctx.strokeRect(bx, by, bw, bh);
  ctx.beginPath(); ctx.moveTo(bx + 102, by); ctx.lineTo(bx + 102, by + 60); ctx.moveTo(bx + 102, by + 95); ctx.lineTo(bx + 102, by + bh); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(bx + 102, by + 111); ctx.lineTo(bx + 208, by + 111); ctx.lineTo(bx + 208, by + 54); ctx.moveTo(bx + 208, by + 26); ctx.lineTo(bx + 208, by); ctx.stroke();
  ctx.fillStyle = '#070709'; ctx.fillRect(bx + 145, by + 148, 78, 78);
  ctx.strokeStyle = '#fffaf0'; ctx.lineWidth = 1;
  for (let j = 0; j < 7; j++) { const y = by + 157 + j * 9; ctx.beginPath(); ctx.moveTo(bx + 154, y); ctx.lineTo(bx + 213, y); ctx.stroke(); }
  ctx.beginPath(); ctx.moveTo(66, 612); ctx.lineTo(414, 612); ctx.stroke();
  ctx.fillStyle = '#eae5d8'; ctx.font = '15px Georgia'; ctx.letterSpacing = '2px'; ctx.fillText('UM ROMANCE DE TERROR', w / 2, 650);
  ctx.font = 'bold 11px Arial'; ctx.letterSpacing = '4px'; ctx.fillText('VOIDWIELDER', w / 2, 685);
}

export function drawScene(canvas) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const w = canvas.width, h = canvas.height, scene = Number(canvas.dataset.scene);
  ctx.fillStyle = '#eee9dc'; ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = '#171516'; ctx.strokeStyle = '#171516';
  if (scene === 1) {
    // The sealed municipal facade, with the measuring tape leading into it.
    ctx.fillRect(145, 44, 285, 111);
    ctx.fillStyle = '#eee9dc'; ctx.fillRect(267, 85, 43, 70);
    ctx.fillRect(185, 69, 34, 46); ctx.fillRect(357, 69, 34, 46);
    ctx.fillStyle = '#171516';
    for (let i = 0; i < 19; i++) { const x = 147 + i * 15; ctx.fillRect(x, 43 - (i % 4), 8, 4); }
    ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(20, 154); ctx.bezierCurveTo(130, 124, 228, 153, 286, 150); ctx.bezierCurveTo(410, 151, 486, 127, 560, 148); ctx.stroke();
    for (let i = 0; i < 23; i++) { const x = 40 + i * 22; ctx.beginPath(); ctx.moveTo(x, 143 + i % 3); ctx.lineTo(x + 3, 151 + i % 3); ctx.stroke(); }
  } else if (scene === 7) {
    // A dry-plate portrait of the witness's hand holding the altered plan.
    ctx.lineWidth = 3; ctx.strokeRect(153, 13, 278, 135);
    ctx.beginPath(); ctx.moveTo(188, 39); ctx.lineTo(387, 39); ctx.moveTo(188, 68); ctx.lineTo(365, 68); ctx.moveTo(188, 95); ctx.lineTo(322, 95); ctx.stroke();
    ctx.fillRect(322, 68, 21, 70);
    ctx.beginPath(); ctx.ellipse(335, 146, 83, 18, -.1, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#eee9dc'; ctx.lineWidth = 2;
    for (let i = 0; i < 9; i++) { ctx.beginPath(); ctx.moveTo(260 + i * 17, 137); ctx.lineTo(241 + i * 17, 164); ctx.stroke(); }
  } else {
    // Seven damp steps discovered behind a bricked doorway.
    ctx.fillRect(103, 8, 374, 153); ctx.fillStyle = '#eee9dc';
    ctx.beginPath(); ctx.moveTo(179, 152); ctx.lineTo(401, 152); ctx.lineTo(355, 31); ctx.lineTo(223, 31); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#171516';
    for (let i = 0; i < 7; i++) { const y = 48 + i * 16; const span = 55 + i * 14; ctx.fillRect(290 - span, y, span * 2, 3 + i / 3); }
    for (let i = 0; i < 28; i++) { const x = 105 + (i * 37) % 370, y = 11 + (i * 53) % 145; ctx.fillRect(x, y, 15 + i % 11, 1); }
  }
  ctx.strokeStyle = '#171516'; ctx.lineWidth = .7;
  for (let i = 0; i < 75; i++) { const x = (i * 47) % w, y = (i * 73) % h; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 11, y - 3); ctx.stroke(); }
}

function decorateSearch() {
  document.querySelectorAll('[data-static-search-results] a[href="/livros/a-casa-das-medidas/"], [data-django-search-results] a[href="/livros/a-casa-das-medidas/"]').forEach((link) => {
    if (link.querySelector('canvas')) return;
    link.classList.add('book-card');
    const canvas = document.createElement('canvas');
    canvas.className = 'book-cover'; canvas.width = 480; canvas.height = 720;
    canvas.setAttribute('role', 'img'); canvas.setAttribute('aria-label', 'Capa de A Casa das Medidas');
    link.prepend(canvas); drawCover(canvas);
  });
}
document.querySelectorAll('canvas[data-book-art="cover"]').forEach(drawCover);
document.querySelectorAll('canvas[data-book-art="scene"]').forEach(drawScene);
decorateSearch();
const search = document.querySelector('[data-static-search-results]');
if (search) new MutationObserver(decorateSearch).observe(search, { childList: true, subtree: true });
