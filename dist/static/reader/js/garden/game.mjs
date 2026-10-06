import {LEVELS, cellKey, createLevel, step} from './core.mjs';

const root = document.querySelector('[data-garden-game]');
const canvas = root?.querySelector('[data-garden-canvas]');
const context = canvas?.getContext('2d');
const overlay = root?.querySelector('[data-garden-overlay]');
const levelName = root?.querySelector('[data-garden-level]');
const levelNumber = root?.querySelector('[data-garden-number]');
const flowerCount = root?.querySelector('[data-garden-flowers]');
const seedStatus = root?.querySelector('[data-garden-seed]');
const message = root?.querySelector('[data-garden-message]');
const soundButton = root?.querySelector('[data-garden-sound]');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const storageKey = 'voidwielder-mila-unlocked-v1';
const board = {left: 104, top: 83, cell: 88};

let state = createLevel(0);
let playing = false;
let unlocked = 0;
let soundOn = true;
let audioContext = null;
let moveFrom = {...state.player};
let moveStarted = 0;
let particles = [];
let pointerStart = null;
let completionTimer = null;

try {
  unlocked = Math.min(LEVELS.length - 1, Math.max(0, Number(localStorage.getItem(storageKey)) || 0));
} catch { /* Progress can stay in memory. */ }

function speak(text) {
  if (message) message.textContent = text;
}

function playNotes(notes) {
  if (!soundOn) return;
  try {
    audioContext ||= new (window.AudioContext || window.webkitAudioContext)();
    const start = audioContext.currentTime;
    notes.forEach(([frequency, delay, duration]) => {
      const oscillator = audioContext.createOscillator();
      const gain = audioContext.createGain();
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(frequency, start + delay);
      gain.gain.setValueAtTime(0.0001, start + delay);
      gain.gain.exponentialRampToValueAtTime(0.12, start + delay + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.0001, start + delay + duration);
      oscillator.connect(gain).connect(audioContext.destination);
      oscillator.start(start + delay);
      oscillator.stop(start + delay + duration + 0.02);
    });
  } catch { /* The garden is playable without audio. */ }
}

function updateHud() {
  levelName.textContent = LEVELS[state.index].name;
  levelNumber.textContent = `${String(state.index + 1).padStart(2, '0')} / 03`;
  flowerCount.textContent = `${state.bloomed.size} / ${state.buds.size} flores`;
  seedStatus.textContent = state.carrying ? '✦ Uma sementinha no bolso' : 'Encontre uma sementinha ✦';
}

function button(label, action, secondary = false) {
  const item = document.createElement('button');
  item.type = 'button';
  item.textContent = label;
  if (secondary) item.className = 'secondary';
  item.addEventListener('click', action);
  return item;
}

function showOverlay(kicker, title, copy, actions, chooseLevel = false) {
  overlay.hidden = false;
  overlay.querySelector('[data-overlay-kicker]').textContent = kicker;
  overlay.querySelector('[data-overlay-title]').textContent = title;
  overlay.querySelector('[data-overlay-copy]').textContent = copy;
  const actionRow = overlay.querySelector('[data-overlay-actions]');
  actionRow.replaceChildren(...actions);
  const choices = overlay.querySelector('[data-level-choices]');
  choices.replaceChildren();
  choices.hidden = !chooseLevel;
  if (chooseLevel) {
    LEVELS.forEach((level, index) => {
      const choice = button(`${index + 1} · ${level.name}`, () => startLevel(index));
      choice.disabled = index > unlocked;
      choice.setAttribute('aria-label', index > unlocked ? `Fase ${index + 1} bloqueada` : `Jogar fase ${index + 1}: ${level.name}`);
      choices.append(choice);
    });
  }
  actionRow.querySelector('button')?.focus();
}

function showWelcome() {
  playing = false;
  state = createLevel(unlocked);
  updateHud();
  speak('Mila espera você no jardim. Pegue uma sementinha e leve até uma flor.');
  showOverlay(
    'UMA AVENTURA SEM PRESSA',
    'Um jardim precisa de você!',
    'Ajude Mila, a coelhinha das nuvens, a levar sementes brilhantes até os botões de flor. Não há relógio nem vidas para perder.',
    [button('Começar a brincar →', () => startLevel(unlocked)), button('Como jogar', showHelp, true)],
    true,
  );
}

function showHelp() {
  showOverlay(
    'COMO JOGAR',
    'Pegue, plante e veja florescer',
    'Use as setas ou WASD no teclado. No celular, toque nas setas ou deslize sobre o jardim. Mila carrega uma sementinha por vez; encoste em uma flor fechada para plantá-la.',
    [button('Entendi, vamos brincar!', () => startLevel(state.index)), button('Escolher fase', showWelcome, true)],
  );
}

function startLevel(index) {
  if (index < 0 || index > unlocked) return;
  window.clearTimeout(completionTimer);
  state = createLevel(index);
  moveFrom = {...state.player};
  moveStarted = 0;
  particles = [];
  playing = true;
  overlay.hidden = true;
  updateHud();
  speak(`Fase ${index + 1}: ${LEVELS[index].note}`);
  canvas.focus({preventScroll: true});
}

function sprinkle(col, row, color, count = 14) {
  const x = board.left + (col + 0.5) * board.cell;
  const y = board.top + (row + 0.5) * board.cell;
  for (let i = 0; i < count; i += 1) {
    const angle = (Math.PI * 2 * i) / count;
    particles.push({
      x, y, color,
      vx: Math.cos(angle) * (1.2 + Math.random() * 1.4),
      vy: Math.sin(angle) * (1.2 + Math.random() * 1.4) - 0.5,
      born: performance.now(),
    });
  }
}

function finishLevel() {
  playing = false;
  const next = state.index + 1;
  if (next < LEVELS.length) {
    unlocked = Math.max(unlocked, next);
    try { localStorage.setItem(storageKey, String(unlocked)); } catch { /* Optional progress. */ }
  }
  playNotes([[523, 0, .22], [659, .12, .22], [784, .24, .3], [1047, .38, .45]]);
  const final = next === LEVELS.length;
  completionTimer = window.setTimeout(() => showOverlay(
    final ? 'TODOS OS JARDINS FLORESCERAM' : `JARDIM ${state.index + 1} COMPLETO`,
    final ? 'Você coloriu o céu inteiro!' : 'Que jardim mais bonito!',
    final
      ? 'Mila guardou cada flor no coração. Obrigada por brincar com calma, carinho e um pouquinho de magia.'
      : `Você acordou todas as flores do ${LEVELS[state.index].name}. O próximo jardim já está esperando!`,
    [button(final ? 'Brincar de novo' : 'Próximo jardim →', () => startLevel(final ? 0 : next)),
      button('Escolher fase', showWelcome, true)],
  ), reducedMotion.matches ? 0 : 700);
}

function move(dx, dy) {
  if (!playing || performance.now() - moveStarted < 110) return;
  const before = state.player;
  const result = step(state, dx, dy);
  if (result.event === 'blocked') {
    speak('Por aqui há um lago ou um arbusto. Tente outro caminho.');
    playNotes([[220, 0, .09]]);
    return;
  }
  state = result.state;
  moveFrom = before;
  moveStarted = performance.now();
  if (result.event === 'pickup') {
    sprinkle(state.player.col, state.player.row, '#ffd86b', 10);
    speak('Uma sementinha brilhante! Leve-a até uma flor fechada.');
    playNotes([[660, 0, .13], [880, .08, .17]]);
  } else if (result.event === 'planted' || result.event === 'finished') {
    sprinkle(state.player.col, state.player.row, '#ff8bb7', 20);
    speak(result.event === 'finished' ? 'Todas as flores acordaram! Que alegria!' : 'Uma flor acordou! Procure outra sementinha.');
    playNotes([[440, 0, .17], [660, .1, .2]]);
    if (result.event === 'finished') finishLevel();
  } else if (result.event === 'needsSeed') {
    speak('Essa flor ainda dorme. Traga uma sementinha para acordá-la.');
  } else if (result.event === 'handsFull') {
    speak('Mila já está levando uma sementinha. Plante-a primeiro!');
  }
  updateHud();
}

const directions = {
  ArrowUp: [0, -1], KeyW: [0, -1],
  ArrowDown: [0, 1], KeyS: [0, 1],
  ArrowLeft: [-1, 0], KeyA: [-1, 0],
  ArrowRight: [1, 0], KeyD: [1, 0],
};

document.addEventListener('keydown', (event) => {
  if (!playing || !directions[event.code] || document.querySelector('dialog[open]')) return;
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;
  event.preventDefault();
  move(...directions[event.code]);
});

root?.querySelectorAll('[data-garden-direction]').forEach((control) => {
  const direction = directions[control.dataset.gardenDirection];
  control.addEventListener('click', () => move(...direction));
});

root?.querySelector('[data-garden-restart]')?.addEventListener('click', () => startLevel(state.index));
soundButton?.addEventListener('click', () => {
  soundOn = !soundOn;
  soundButton.textContent = soundOn ? '♫ Som ligado' : '♫ Som desligado';
  soundButton.setAttribute('aria-pressed', String(soundOn));
  if (soundOn) playNotes([[660, 0, .12]]);
});

canvas?.addEventListener('pointerdown', (event) => {
  pointerStart = {x: event.clientX, y: event.clientY};
});
canvas?.addEventListener('pointerup', (event) => {
  if (!pointerStart || !playing) return;
  const dx = event.clientX - pointerStart.x;
  const dy = event.clientY - pointerStart.y;
  pointerStart = null;
  if (Math.max(Math.abs(dx), Math.abs(dy)) < 22) return;
  if (Math.abs(dx) > Math.abs(dy)) move(Math.sign(dx), 0);
  else move(0, Math.sign(dy));
});

function roundRect(x, y, width, height, radius, color) {
  context.fillStyle = color;
  context.beginPath();
  context.roundRect(x, y, width, height, radius);
  context.fill();
}

function ellipse(x, y, radiusX, radiusY, color) {
  context.fillStyle = color;
  context.beginPath();
  context.ellipse(x, y, radiusX, radiusY, 0, 0, Math.PI * 2);
  context.fill();
}

function cloud(x, y, scale = 1) {
  context.save();
  context.translate(x, y);
  context.scale(scale, scale);
  ellipse(0, 12, 47, 16, '#ffffffb8');
  ellipse(-25, 3, 25, 19, '#ffffffc9');
  ellipse(4, -8, 33, 28, '#ffffffde');
  ellipse(31, 4, 23, 18, '#ffffffc9');
  context.restore();
}

function star(x, y, size, color) {
  context.fillStyle = color;
  context.beginPath();
  context.moveTo(x, y - size);
  context.quadraticCurveTo(x + size * .18, y - size * .18, x + size, y);
  context.quadraticCurveTo(x + size * .18, y + size * .18, x, y + size);
  context.quadraticCurveTo(x - size * .18, y + size * .18, x - size, y);
  context.quadraticCurveTo(x - size * .18, y - size * .18, x, y - size);
  context.fill();
}

function drawHedge(x, y) {
  roundRect(x + 8, y + 15, 72, 64, 22, '#7bb884');
  ellipse(x + 28, y + 43, 23, 25, '#89c991');
  ellipse(x + 55, y + 36, 26, 29, '#68ad7b');
  ellipse(x + 70, y + 55, 14, 19, '#80be8a');
  star(x + 40, y + 30, 4, '#f7e8a0');
  star(x + 67, y + 55, 3, '#fff5c7');
}

function drawPond(x, y, time) {
  roundRect(x + 7, y + 7, 74, 74, 26, '#78bbd1');
  ellipse(x + 44, y + 48, 28, 15, '#a5dce3');
  context.strokeStyle = '#e3f8f5';
  context.lineWidth = 3;
  context.beginPath();
  context.arc(x + 43, y + 46, 13 + Math.sin(time / 500) * 2, .2, 2.7);
  context.stroke();
  ellipse(x + 25, y + 24, 5, 3, '#e6f9e4');
}

function drawSeed(x, y, time) {
  const bob = reducedMotion.matches ? 0 : Math.sin(time / 340 + x) * 3;
  ellipse(x, y + 17, 18, 6, '#87977e44');
  const glow = context.createRadialGradient(x, y + bob, 2, x, y + bob, 32);
  glow.addColorStop(0, '#fff9be');
  glow.addColorStop(1, '#fff9be00');
  ellipse(x, y + bob, 32, 32, glow);
  star(x, y + bob, 17, '#fff0a2');
  star(x, y + bob, 10, '#ffcf57');
  ellipse(x - 2, y - 2 + bob, 2, 2, '#fff');
}

function drawFlower(x, y, opened, time) {
  context.strokeStyle = '#518a63';
  context.lineWidth = 6;
  context.lineCap = 'round';
  context.beginPath();
  context.moveTo(x, y + 25);
  context.quadraticCurveTo(x + 5, y + 5, x, y - 9);
  context.stroke();
  ellipse(x - 13, y + 13, 13, 6, '#6bac72');
  ellipse(x + 12, y + 8, 13, 6, '#78ba79');
  if (opened) {
    const sway = reducedMotion.matches ? 0 : Math.sin(time / 520 + x) * 2;
    for (let petal = 0; petal < 6; petal += 1) {
      const angle = Math.PI * 2 * petal / 6;
      ellipse(x + Math.cos(angle) * 15, y - 15 + sway + Math.sin(angle) * 15,
        10, 14, petal % 2 ? '#ff86ad' : '#ffa8c7');
    }
    ellipse(x, y - 15 + sway, 12, 12, '#ffe688');
    ellipse(x - 4, y - 17 + sway, 1.8, 2, '#6b5262');
    ellipse(x + 4, y - 17 + sway, 1.8, 2, '#6b5262');
    context.strokeStyle = '#6b5262';
    context.lineWidth = 1.5;
    context.beginPath(); context.arc(x, y - 12 + sway, 3, 0, Math.PI); context.stroke();
  } else {
    ellipse(x - 7, y - 17, 9, 17, '#e48caf');
    ellipse(x + 7, y - 17, 9, 17, '#efa7c1');
    ellipse(x, y - 14, 9, 15, '#f3b8c9');
    star(x + 22, y - 28, 4, '#fff2c4');
  }
}

function drawBunny(x, y, time) {
  const bob = reducedMotion.matches ? 0 : Math.sin(time / 220) * 1.5;
  context.save();
  context.translate(x, y + bob);
  ellipse(0, 26, 30, 8, '#685b7040');
  ellipse(-16, 19, 17, 10, '#fff3e8');
  ellipse(15, 19, 17, 10, '#fff3e8');
  ellipse(0, 7, 29, 30, '#fff7ec');
  ellipse(-15, -35, 12, 34, '#fff7ec');
  ellipse(15, -35, 12, 34, '#fff7ec');
  ellipse(-15, -37, 6, 23, '#f5b8c8');
  ellipse(15, -37, 6, 23, '#f5b8c8');
  ellipse(0, -7, 31, 29, '#fffdf5');
  ellipse(-11, -8, 3.2, 4, '#38364c');
  ellipse(11, -8, 3.2, 4, '#38364c');
  ellipse(-18, 1, 7, 4, '#ffc4cf');
  ellipse(18, 1, 7, 4, '#ffc4cf');
  ellipse(0, 0, 4.5, 3.5, '#e68eaa');
  context.strokeStyle = '#514657';
  context.lineWidth = 1.8;
  context.beginPath(); context.arc(0, 1, 6, .12, Math.PI - .12); context.stroke();
  roundRect(-22, 14, 44, 8, 4, '#8ac7ba');
  ellipse(-15, 17, 9, 6, '#6aaea0');
  if (state.carrying) drawSeed(0, -74, time);
  context.restore();
}

function render(time) {
  if (!context) return;
  const {width, height} = canvas;
  const sky = context.createLinearGradient(0, 0, width, height);
  LEVELS[state.index].sky.forEach((color, index) => sky.addColorStop(index, color));
  context.fillStyle = sky;
  context.fillRect(0, 0, width, height);
  ellipse(825, 55, 115, 58, '#ffffff5c');
  cloud(120, 42, .8);
  cloud(835, 635, 1.1);
  cloud(925, 90, .45);
  for (let i = 0; i < 9; i += 1) {
    const x = 60 + i * 110;
    const y = 27 + i % 3 * 10;
    star(x, y, i % 2 ? 3 : 5, '#fffbea');
  }

  roundRect(board.left - 19, board.top - 19, board.cell * state.width + 38,
    board.cell * state.height + 38, 38, '#ffffffa8');
  roundRect(board.left - 7, board.top - 7, board.cell * state.width + 14,
    board.cell * state.height + 14, 26, '#8cc0a4');
  for (let row = 0; row < state.height; row += 1) {
    for (let col = 0; col < state.width; col += 1) {
      const x = board.left + col * board.cell;
      const y = board.top + row * board.cell;
      roundRect(x + 2, y + 2, board.cell - 4, board.cell - 4, 15,
        (row + col) % 2 ? '#e6eecf' : '#edf2d9');
      const key = cellKey(col, row);
      if (state.water.has(key)) drawPond(x, y, time);
      else if (state.walls.has(key)) drawHedge(x, y);
      else {
        ellipse(x + 18, y + 21, 2, 3, '#b6d79d');
        ellipse(x + 69, y + 65, 2, 3, '#b6d79d');
        if (state.buds.has(key)) drawFlower(x + 44, y + 47, state.bloomed.has(key), time);
        if (state.seeds.has(key)) drawSeed(x + 44, y + 43, time);
      }
    }
  }

  const progress = Math.min(1, Math.max(0, (time - moveStarted) / 150));
  const ease = progress * progress * (3 - 2 * progress);
  const col = moveFrom.col + (state.player.col - moveFrom.col) * ease;
  const row = moveFrom.row + (state.player.row - moveFrom.row) * ease;
  drawBunny(board.left + (col + .5) * board.cell, board.top + (row + .54) * board.cell, time);

  particles = particles.filter((particle) => time - particle.born < 650);
  particles.forEach((particle) => {
    const age = (time - particle.born) / 16;
    context.globalAlpha = Math.max(0, 1 - age / 40);
    star(particle.x + particle.vx * age * 3, particle.y + particle.vy * age * 3, 4, particle.color);
  });
  context.globalAlpha = 1;
  requestAnimationFrame(render);
}

if (root && context) {
  updateHud();
  showWelcome();
  requestAnimationFrame(render);
}
