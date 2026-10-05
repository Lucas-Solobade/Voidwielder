const gold = '#ffd84d';
const blue = '#6fd3ef';
function roundRect(ctx, x, y, w, h, r, fill, stroke) {
  ctx.beginPath(); ctx.roundRect(x, y, w, h, r);
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.stroke(); }
}
function line(ctx, points, color, width = 2) {
  ctx.beginPath(); ctx.moveTo(...points[0]); points.slice(1).forEach((point) => ctx.lineTo(...point));
  ctx.strokeStyle = color; ctx.lineWidth = width; ctx.stroke();
}
function cover(canvas) {
  const ctx = canvas.getContext('2d'); if (!ctx) return;
  const { width: w, height: h } = canvas;
  const bg = ctx.createLinearGradient(0, 0, w, h); bg.addColorStop(0, '#101627'); bg.addColorStop(.55, '#142e49'); bg.addColorStop(1, '#060b18');
  ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);
  for (let i = 0; i < 76; i++) {
    const x = (i * 197 + 37) % w; const y = (i * 137 + 63) % h;
    ctx.fillStyle = i % 8 === 0 ? '#ffe59e' : '#7eb3cc77'; ctx.beginPath(); ctx.arc(x, y, i % 8 === 0 ? 2.2 : 1.1, 0, Math.PI * 2); ctx.fill();
  }
  ctx.strokeStyle = '#74d3ed55'; ctx.lineWidth = 1;
  for (let i = 0; i < 6; i++) { ctx.beginPath(); ctx.ellipse(w / 2, 375, 160 + i * 30, 80 + i * 18, -.35, 0, Math.PI * 2); ctx.stroke(); }
  roundRect(ctx, 84, 236, 372, 278, 17, '#101b2af0', '#6ad6e8');
  roundRect(ctx, 84, 236, 372, 43, [17, 17, 0, 0], '#24394b');
  for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(109 + 19 * i, 258, 4, 0, Math.PI * 2); ctx.fillStyle = ['#ff876f', '#ffd84d', '#63c9a9'][i]; ctx.fill(); }
  ctx.font = '700 24px Consolas, monospace'; ctx.fillStyle = '#a9e8e5'; ctx.fillText('$', 113, 336); ctx.fillStyle = gold; ctx.fillText('hello, Linux_', 145, 336);
  ctx.font = '16px Consolas, monospace'; ctx.fillStyle = '#a5bbce'; ctx.fillText('kernel → processos → mundo', 115, 376); ctx.fillText('aprenda | pratique | entenda', 115, 405);
  ctx.strokeStyle = gold; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(145, 460); ctx.lineTo(230, 478); ctx.lineTo(325, 451); ctx.lineTo(410, 475); ctx.stroke();
  [145, 230, 325, 410].forEach((x, i) => { ctx.fillStyle = i % 2 ? blue : gold; ctx.beginPath(); ctx.arc(x, [460, 478, 451, 475][i], 6, 0, Math.PI * 2); ctx.fill(); });
  ctx.fillStyle = '#f8f3e6'; ctx.font = '800 84px Arial, sans-serif'; ctx.fillText('LINUX', 76, 146);
  ctx.fillStyle = gold; ctx.font = '700 31px Arial, sans-serif'; ctx.fillText('DO ZERO AO AVANÇADO', 79, 193);
  ctx.fillStyle = '#cbd4df'; ctx.font = '20px Arial, sans-serif'; ctx.fillText('78 lições  •  554 páginas  •  prática real', 82, 583);
  line(ctx, [[81, 623], [456, 623]], '#ffd84d88', 1);
  ctx.font = '700 24px Arial, sans-serif'; ctx.fillStyle = gold; ctx.fillText('VOIDWIELDER', 81, 669);
}
function diagram(canvas, kind) {
  const ctx = canvas.getContext('2d'); if (!ctx) return;
  const w = canvas.width, h = canvas.height;
  ctx.fillStyle = '#e3eced'; ctx.fillRect(0, 0, w, h);
  const items = {
    rede: [['APLICAÇÃO', 'dados'], ['TRANSPORTE', 'TCP / UDP'], ['REDE', 'IP / rotas'], ['LIGAÇÃO', 'quadros']],
    boot: [['FIRMWARE', 'UEFI'], ['BOOTLOADER', 'entrada'], ['KERNEL', 'núcleo'], ['SERVIÇOS', 'login']],
    container: [['APLICAÇÃO', 'processo'], ['ISOLAMENTO', 'namespaces'], ['CONTROLE', 'cgroups'], ['HOST', 'kernel']],
  }[kind];
  if (!items) return;
  ctx.font = '700 13px Arial, sans-serif'; ctx.fillStyle = '#254051';
  ctx.fillText(kind === 'rede' ? 'O CAMINHO DE UM PACOTE' : kind === 'boot' ? 'O CAMINHO DA INICIALIZAÇÃO' : 'O QUE UM CONTÊINER COMPARTILHA', 22, 26);
  items.forEach(([title, sub], i) => {
    const x = 22 + 151 * i; roundRect(ctx, x, 52, 131, 91, 8, i % 2 ? '#d5e5e8' : '#d5dde7', '#799cad');
    ctx.fillStyle = '#153449'; ctx.font = '700 12px Arial, sans-serif'; ctx.fillText(title, x + 10, 87);
    ctx.fillStyle = '#476278'; ctx.font = '12px Arial, sans-serif'; ctx.fillText(sub, x + 10, 112);
    if (i < 3) { line(ctx, [[x + 133, 96], [x + 150, 96]], '#ac8422', 2); line(ctx, [[x + 145, 91], [x + 150, 96], [x + 145, 101]], '#ac8422', 2); }
  });
  ctx.fillStyle = '#52687b'; ctx.font = '12px Arial, sans-serif'; ctx.fillText('Cada camada tem uma tarefa. Use o texto para investigar o que acontece entre elas.', 22, 167);
}
export function drawLinuxArt(canvas) { if (canvas?.dataset.linuxArt === 'cover') cover(canvas); else if (canvas) diagram(canvas, canvas.dataset.linuxArt); }
document.querySelectorAll('[data-linux-art]').forEach(drawLinuxArt);
