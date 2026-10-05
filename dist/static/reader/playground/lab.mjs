import { LEVELS, OPERATIONS, runProgram } from './engine.mjs';

const $ = (selector) => document.querySelector(selector);
const board = $('#board');
const programList = $('#program');
const status = $('#lab-status');
const signalCount = $('#signal-count');
const commandCount = $('#command-count');
const successPanel = $('#success');
const runButton = $('#run-button');
const undoButton = $('#undo-button');
const clearButton = $('#clear-button');
const nextButton = $('#next-button');
const hintButton = $('#hint-button');
const hint = $('#hint');
const levelButtons = [...document.querySelectorAll('[data-level]')];
const commandButtons = [...document.querySelectorAll('[data-op]')];
const STORAGE_KEY = 'voidwielder-playground-sinal-zero-v1';
const ANGLES = { N: '0deg', E: '90deg', S: '180deg', W: '270deg' };
let unlocked = 0;
try {
  unlocked = Math.min(2, Math.max(0, Number(JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}').unlocked) || 0));
} catch { /* The playground works without local storage. */ }
let currentLevel = 0;
let program = [];
let running = false;
let generation = 0;
let lastSuccess = null;
let pathElement;

function announce(message) { status.textContent = message; }

function updateControls() {
  runButton.disabled = running || program.length === 0;
  undoButton.disabled = running || program.length === 0;
  clearButton.disabled = running || program.length === 0;
  commandButtons.forEach((button) => { button.disabled = running || program.length >= 20; });
  levelButtons.forEach((button) => {
    const index = Number(button.dataset.level);
    button.disabled = running || index > unlocked;
    if (index === currentLevel) button.setAttribute('aria-current', 'step');
    else button.removeAttribute('aria-current');
  });
  commandCount.textContent = `${program.length} / 20`;
}

function renderProgram(active = -1, done = -1) {
  programList.replaceChildren();
  if (!program.length) {
    const empty = document.createElement('li');
    empty.className = 'program-empty';
    empty.textContent = 'Seus comandos vão aparecer aqui.';
    programList.append(empty);
  }
  program.forEach((operation, index) => {
    const item = document.createElement('li');
    item.classList.toggle('active', index === active);
    item.classList.toggle('done', index < done);
    const label = document.createElement('span');
    label.textContent = `${String(index + 1).padStart(2, '0')} ${OPERATIONS[operation]}`;
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.dataset.remove = String(index);
    remove.setAttribute('aria-label', `Remover comando ${index + 1}: ${OPERATIONS[operation]}`);
    remove.textContent = '×';
    remove.disabled = running;
    item.append(label, remove);
    programList.append(item);
  });
  updateControls();
}

function makeCell(x, y, level) {
  const cell = document.createElement('div');
  cell.className = 'cell';
  cell.dataset.point = `${x},${y}`;
  cell.setAttribute('role', 'gridcell');
  const rock = level.rocks.some(([rx, ry]) => rx === x && ry === y);
  const signal = level.signals.some(([sx, sy]) => sx === x && sy === y);
  const goal = level.goal[0] === x && level.goal[1] === y;
  if (rock) cell.classList.add('rock');
  if (signal) cell.classList.add('signal');
  if (goal) cell.classList.add('goal');
  cell.setAttribute('aria-label', `Coluna ${x + 1}, linha ${y + 1}${rock ? ', meteoro' : ''}${signal ? ', sinal' : ''}${goal ? ', farol' : ''}`);
  return cell;
}

function buildBoard(level) {
  board.style.setProperty('--size', level.size);
  board.setAttribute('aria-label', `Mapa ${level.size} por ${level.size} da missão ${currentLevel + 1}`);
  const cells = [];
  for (let y = 0; y < level.size; y += 1) {
    for (let x = 0; x < level.size; x += 1) cells.push(makeCell(x, y, level));
  }
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.classList.add('route');
  svg.setAttribute('viewBox', `0 0 ${level.size} ${level.size}`);
  svg.setAttribute('aria-hidden', 'true');
  pathElement = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  svg.append(pathElement);
  board.replaceChildren(...cells, svg);
}

function paintFrame(frame, trail) {
  const level = LEVELS[currentLevel];
  const seen = new Set(trail.map(({ x, y }) => `${x},${y}`));
  board.querySelectorAll('.cell').forEach((cell) => {
    cell.classList.toggle('visited', seen.has(cell.dataset.point));
    const [x, y] = cell.dataset.point.split(',').map(Number);
    const signalIndex = level.signals.findIndex(([sx, sy]) => sx === x && sy === y);
    cell.classList.toggle('collected', signalIndex >= 0 && frame.collected.includes(signalIndex));
    cell.querySelector('.ship')?.remove();
    if (x === frame.x && y === frame.y) {
      const ship = document.createElement('span');
      ship.className = 'ship';
      ship.style.setProperty('--angle', ANGLES[frame.direction]);
      ship.setAttribute('aria-label', `Centelha olhando para ${frame.direction}`);
      cell.append(ship);
    }
  });
  pathElement.setAttribute('d', trail.map(({ x, y }, index) => `${index ? 'L' : 'M'} ${x + .5} ${y + .5}`).join(' '));
  signalCount.textContent = `${frame.collected.length} / ${level.signals.length} ${level.signals.length === 1 ? 'sinal' : 'sinais'}`;
}

function setLevel(index) {
  if (index < 0 || index >= LEVELS.length || index > unlocked) return;
  generation += 1;
  running = false;
  currentLevel = index;
  program = [];
  lastSuccess = null;
  const level = LEVELS[index];
  $('#mission-number').textContent = `${String(index + 1).padStart(2, '0')} / 03`;
  $('#mission-title').textContent = level.title;
  $('#mission-story').textContent = level.story;
  $('#mission-concept').textContent = level.concept;
  hint.textContent = level.hint;
  hint.hidden = true;
  hintButton.setAttribute('aria-expanded', 'false');
  successPanel.hidden = true;
  buildBoard(level);
  const start = { x: level.start[0], y: level.start[1], direction: level.start[2], collected: [] };
  paintFrame(start, [start]);
  renderProgram();
  announce('Monte um programa e toque em Executar. A centelha precisa dos sinais antes de chegar ao farol.');
}

const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

async function execute() {
  if (running || !program.length) return;
  const level = LEVELS[currentLevel];
  const result = runProgram(level, program);
  running = true;
  successPanel.hidden = true;
  updateControls();
  const runId = ++generation;
  const trail = [result.frames[0]];
  paintFrame(result.frames[0], trail);
  announce('Executando seu algoritmo…');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  for (const frame of result.frames.slice(1)) {
    await wait(reduceMotion ? 80 : 320);
    if (runId !== generation) return;
    renderProgram(frame.command, frame.command);
    if (frame.action === 'forward') trail.push(frame);
    paintFrame(frame, trail);
    if (frame.action === 'collision') break;
  }
  if (runId !== generation) return;
  running = false;
  renderProgram(-1, program.length);
  if (result.status === 'collision') {
    announce('Ops! A centelha encontrou um meteoro ou saiu do mapa. Ajuste os comandos e tente de novo.');
  } else if (result.status === 'incomplete') {
    announce(`Ainda falta algo: ${result.collected} de ${level.signals.length} sinais. Termine no farol com todos eles.`);
  } else {
    lastSuccess = { level, frames: result.frames };
    unlocked = Math.max(unlocked, Math.min(LEVELS.length - 1, currentLevel + 1));
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ unlocked })); } catch { /* Progress is optional. */ }
    nextButton.textContent = currentLevel === LEVELS.length - 1 ? 'Voltar à missão 1 ↺' : 'Próxima missão →';
    successPanel.hidden = false;
    announce(`Conseguiu! ${result.collected} ${result.collected === 1 ? 'sinal acendeu' : 'sinais acenderam'} sua constelação. O caminho foi seu algoritmo.`);
  }
  updateControls();
}

function saveCard() {
  if (!lastSuccess) return;
  const { level, frames } = lastSuccess;
  const canvas = document.createElement('canvas');
  canvas.width = 1200;
  canvas.height = 675;
  const ctx = canvas.getContext('2d');
  const background = ctx.createLinearGradient(0, 0, 1200, 675);
  background.addColorStop(0, '#101b3b');
  background.addColorStop(1, '#3b315d');
  ctx.fillStyle = background;
  ctx.fillRect(0, 0, 1200, 675);
  for (let index = 0; index < 95; index += 1) {
    const x = (index * 173 + 73) % 1170;
    const y = (index * 101 + 41) % 640;
    ctx.fillStyle = index % 4 ? '#ffffff77' : '#ffe6a3';
    ctx.beginPath(); ctx.arc(x, y, index % 9 ? 1.5 : 3, 0, Math.PI * 2); ctx.fill();
  }
  const unique = [];
  for (const frame of frames) if (frame.action === 'start' || frame.action === 'forward') unique.push([frame.x, frame.y]);
  const step = 72;
  const originX = 650 - (level.size - 1) * step / 2;
  const originY = 342 - (level.size - 1) * step / 2;
  ctx.strokeStyle = '#a6f3ed';
  ctx.lineWidth = 5;
  ctx.lineCap = 'round';
  ctx.shadowColor = '#a6f3ed';
  ctx.shadowBlur = 18;
  ctx.beginPath();
  unique.forEach(([x, y], index) => index ? ctx.lineTo(originX + x * step, originY + y * step) : ctx.moveTo(originX + x * step, originY + y * step));
  ctx.stroke();
  unique.forEach(([x, y]) => {
    ctx.fillStyle = '#fff4bd';
    ctx.beginPath(); ctx.arc(originX + x * step, originY + y * step, 8, 0, Math.PI * 2); ctx.fill();
  });
  ctx.shadowBlur = 0;
  ctx.fillStyle = '#ffda70';
  ctx.font = 'bold 30px system-ui';
  ctx.fillText('VOIDWIELDER / LABORATÓRIO DO VAZIO', 68, 77);
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 56px system-ui';
  ctx.fillText('Minha constelação', 68, 161);
  ctx.font = '26px system-ui';
  ctx.fillStyle = '#d2e8e8';
  ctx.fillText(level.title, 70, 210);
  ctx.font = '22px system-ui';
  ctx.fillText(`Criada com ${program.length} comandos · Experimento ${String(currentLevel + 1).padStart(2, '0')}`, 70, 620);
  canvas.toBlob((blob) => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `voidwielder-constelacao-${currentLevel + 1}.png`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }, 'image/png');
}

commandButtons.forEach((button) => button.addEventListener('click', () => {
  if (running || program.length >= 20) return;
  program.push(button.dataset.op);
  successPanel.hidden = true;
  renderProgram();
  announce(`${OPERATIONS[button.dataset.op]} adicionado. Agora você tem ${program.length} comando${program.length === 1 ? '' : 's'}.`);
}));
programList.addEventListener('click', (event) => {
  const remove = event.target.closest('[data-remove]');
  if (!remove || running) return;
  program.splice(Number(remove.dataset.remove), 1);
  successPanel.hidden = true;
  renderProgram();
  announce('Comando removido.');
});
undoButton.addEventListener('click', () => { if (!running) { program.pop(); successPanel.hidden = true; renderProgram(); announce('Último comando desfeito.'); } });
clearButton.addEventListener('click', () => { if (!running) { program = []; successPanel.hidden = true; renderProgram(); announce('Programa limpo. Tente um caminho novo.'); } });
runButton.addEventListener('click', execute);
levelButtons.forEach((button) => button.addEventListener('click', () => setLevel(Number(button.dataset.level))));
nextButton.addEventListener('click', () => setLevel(currentLevel === LEVELS.length - 1 ? 0 : currentLevel + 1));
$('#save-button').addEventListener('click', saveCard);
hintButton.addEventListener('click', () => {
  hint.hidden = !hint.hidden;
  hintButton.setAttribute('aria-expanded', String(!hint.hidden));
});

setLevel(0);
