const GOLD = '#fcd75f';
const BLUE = '#75c4ee';
const INK = '#152137';

function rounded(ctx, x, y, w, h, r, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.roundRect(x, y, w, h, r);
  ctx.fill();
}

function cover(canvas) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const { width: w, height: h } = canvas;
  const bg = ctx.createLinearGradient(0, 0, w, h);
  bg.addColorStop(0, '#132441'); bg.addColorStop(.55, '#101829'); bg.addColorStop(1, '#070b16');
  ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = '#95c8ef23'; ctx.lineWidth = 1;
  for (let x = 50; x < w; x += 42) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
  for (let y = 50; y < h; y += 42) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }
  ctx.fillStyle = '#9dbbd3'; ctx.font = 'bold 18px Arial'; ctx.fillText('VOIDWIELDER  /  GUIAS', 48, 67);
  ctx.fillStyle = '#f6f1e5'; ctx.font = 'bold 76px Arial'; ctx.fillText('PYTHON', 42, 172);
  ctx.fillStyle = GOLD; ctx.font = 'bold 31px Arial'; ctx.fillText('DO ZERO AO', 46, 216); ctx.fillText('AVANÇADO', 46, 252);
  ctx.fillStyle = '#b9c9d9'; ctx.font = '21px Arial'; ctx.fillText('Pense · programe · descubra', 47, 298);
  const nodes = [
    [96, 420, 'IDEIA', GOLD], [280, 392, 'CÓDIGO', BLUE], [366, 520, 'TESTE', GOLD],
    [168, 568, 'DADOS', BLUE], [354, 636, 'MUNDO', GOLD],
  ];
  ctx.strokeStyle = '#b7e4f3a5'; ctx.lineWidth = 4;
  for (const [a, b] of [[0,1],[1,2],[2,3],[3,4],[0,3]]) { ctx.beginPath(); ctx.moveTo(nodes[a][0], nodes[a][1]); ctx.lineTo(nodes[b][0], nodes[b][1]); ctx.stroke(); }
  nodes.forEach(([x, y, label, color]) => {
    ctx.shadowColor = color; ctx.shadowBlur = 22;
    ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, 29, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0;
    ctx.fillStyle = INK; ctx.font = 'bold 11px Arial'; ctx.textAlign = 'center'; ctx.fillText(label, x, y + 4);
  });
  ctx.textAlign = 'left'; ctx.fillStyle = '#e3d7b3'; ctx.font = 'bold 17px Arial'; ctx.fillText('13 PARTES   ·   39 DESAFIOS', 46, 686);
}

const charts = {
  algoritmo: ['ENTRADA', 'PASSOS', 'SAÍDA'],
  condicao: ['CONDIÇÃO', 'SIM / NÃO', 'AÇÃO'],
  objeto: ['CLASSE', 'OBJETO', 'MÉTODO'],
  array: ['DADOS', 'ARRAY', 'OPERAÇÃO'],
  bot: ['EVENTO', 'BOT', 'RESPOSTA'],
  ml: ['TREINO', 'MODELO', 'PREVISÃO'],
};

function diagram(canvas, type) {
  const ctx = canvas.getContext('2d'); if (!ctx) return;
  const {width: w, height: h} = canvas;
  ctx.fillStyle = '#eaf0ef'; ctx.fillRect(0, 0, w, h);
  const labels = charts[type] || charts.algoritmo;
  const centers = [105, 310, 515];
  ctx.strokeStyle = '#356c83'; ctx.lineWidth = 3;
  for (let i = 0; i < 2; i++) {
    ctx.beginPath(); ctx.moveTo(centers[i] + 68, 92); ctx.lineTo(centers[i + 1] - 71, 92); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(centers[i + 1] - 79, 86); ctx.lineTo(centers[i + 1] - 70, 92); ctx.lineTo(centers[i + 1] - 79, 98); ctx.stroke();
  }
  labels.forEach((label, index) => {
    rounded(ctx, centers[index] - 76, 53, 152, 76, 12, index === 1 ? '#ffe39a' : '#d0e8ee');
    ctx.fillStyle = '#183b52'; ctx.font = 'bold 19px Arial'; ctx.textAlign = 'center'; ctx.fillText(label, centers[index], 99);
  });
}

export function drawPythonArt(canvas) {
  if (canvas.dataset.pythonArt === 'cover') cover(canvas);
  else diagram(canvas, canvas.dataset.pythonArt);
}
document.querySelectorAll('canvas[data-python-art]').forEach(drawPythonArt);
