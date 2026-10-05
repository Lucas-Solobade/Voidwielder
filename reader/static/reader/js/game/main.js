import { createLevel, LEVELS } from './levels.js';
import { renderGame } from './art.js';

const root = document.querySelector('[data-game]');
const canvas = root?.querySelector('[data-canvas]');
const ctx = canvas?.getContext('2d');

if (root && ctx) {
  const screen = root.querySelector('[data-screen]');
  const screenContent = root.querySelector('[data-screen-content]');
  const levelLabel = root.querySelector('[data-level-label]');
  const healthLabel = root.querySelector('[data-health-label]');
  const scoreLabel = root.querySelector('[data-score-label]');
  const pauseButton = root.querySelector('[data-pause]');
  const SAVE_KEY = 'voidwielder-pipo-progress-v1';
  const keys = { left: false, right: false, jump: false };
  const playerSize = { w: 30, h: 42 };
  let audioContext = null;
  let muted = false;
  let unlocked = 0;
  try { unlocked = Math.min(2, Math.max(0, Number(JSON.parse(localStorage.getItem(SAVE_KEY) || '{}').unlocked) || 0)); } catch { /* Optional local progress. */ }

  const game = {
    state: 'MENU', levelIndex: 0, level: createLevel(0),
    player: null, score: 0, collected: 0, camera: 0, time: 0,
    particles: [], burstTime: 0, shake: 0,
  };

  function makePlayer(x, y) {
    return {
      x, y, w: playerSize.w, h: playerSize.h, vx: 0, vy: 0, facing: 1,
      grounded: false, coyote: 0, jumpBuffer: 0, specialRequested: false,
      specialCooldown: 0, health: 3, invulnerable: 0, hurtTime: 0,
      landSquash: 0, checkpointX: x, checkpointY: y,
    };
  }
  game.player = makePlayer(game.level.spawn.x, game.level.spawn.y);

  function sound(frequency, duration = .12, type = 'sine', slide = 0) {
    if (muted) return;
    try {
      audioContext ||= new (window.AudioContext || window.webkitAudioContext)();
      if (audioContext.state === 'suspended') audioContext.resume();
      const oscillator = audioContext.createOscillator();
      const gain = audioContext.createGain();
      const now = audioContext.currentTime;
      oscillator.type = type;
      oscillator.frequency.setValueAtTime(frequency, now);
      oscillator.frequency.linearRampToValueAtTime(Math.max(80, frequency + slide), now + duration);
      gain.gain.setValueAtTime(.045, now);
      gain.gain.exponentialRampToValueAtTime(.001, now + duration);
      oscillator.connect(gain).connect(audioContext.destination);
      oscillator.start(now);
      oscillator.stop(now + duration);
    } catch { /* Sound is optional. */ }
  }

  function particles(x, y, count, color, speed = 130) {
    for (let i = 0; i < count && game.particles.length < 110; i += 1) {
      const angle = Math.PI * 2 * i / count + Math.random() * .45;
      const velocity = speed * (.35 + Math.random() * .65);
      game.particles.push({ x, y, vx: Math.cos(angle) * velocity, vy: Math.sin(angle) * velocity - 35,
        life: .45 + Math.random() * .3, maxLife: .75, size: 2 + Math.random() * 3, color });
    }
  }

  function updateHud() {
    levelLabel.textContent = `Fase ${game.levelIndex + 1} · ${game.level.name}`;
    healthLabel.textContent = `${'♥ '.repeat(game.player.health)}${'♡ '.repeat(3 - game.player.health)}`.trim();
    healthLabel.setAttribute('aria-label', `${game.player.health} de 3 corações`);
    scoreLabel.textContent = `✉ ${game.collected} · ${game.score} pts`;
    pauseButton.disabled = game.state !== 'PLAYING' && game.state !== 'PAUSED';
    pauseButton.textContent = game.state === 'PAUSED' ? 'Continuar' : 'Pausar';
  }

  function showScreen(title, body, buttons, symbol = '✦') {
    screen.hidden = false;
    screenContent.replaceChildren();
    const mascot = document.createElement('div');
    mascot.className = 'game-mascot';
    mascot.setAttribute('aria-hidden', 'true');
    mascot.textContent = symbol;
    const heading = document.createElement('h2');
    heading.textContent = title;
    const paragraph = document.createElement('p');
    paragraph.textContent = body;
    const actions = document.createElement('div');
    actions.className = 'game-screen-actions';
    buttons.forEach(({ label, action, secondary }) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.dataset.action = action;
      button.textContent = label;
      if (secondary) button.className = 'secondary';
      actions.append(button);
    });
    screenContent.append(mascot, heading, paragraph, actions);
    actions.querySelector('button')?.focus({ preventScroll: true });
    updateHud();
  }

  function menu() {
    game.state = 'MENU';
    keys.left = false; keys.right = false; keys.jump = false;
    const options = [{ label: 'Jogar desde o início', action: 'start' }];
    if (unlocked > 0) options.push({ label: `Continuar da fase ${unlocked + 1}`, action: 'continue', secondary: true });
    options.push({ label: 'Como jogar', action: 'how', secondary: true });
    options.push({ label: muted ? 'Som: desligado' : 'Som: ligado', action: 'sound', secondary: true });
    showScreen('Uma entrega fora deste mundo!', 'Pipo recebeu cartas para as estrelas. Atravesse três lugares esquisitos, junte envelopes e ajude o Rabugão das Nuvens a sorrir de novo.', options, '✉');
  }

  function loadLevel(index, keepScore = false) {
    game.levelIndex = index;
    game.level = createLevel(index);
    game.player = makePlayer(game.level.spawn.x, game.level.spawn.y);
    game.camera = 0;
    game.particles = [];
    game.burstTime = 0;
    if (!keepScore) { game.score = 0; game.collected = 0; }
    game.state = 'PLAYING';
    screen.hidden = true;
    updateHud();
    sound(460, .18, 'sine', 230);
    canvas.focus?.({ preventScroll: true });
  }

  function pause() {
    if (game.state === 'PLAYING') {
      game.state = 'PAUSED';
      showScreen('Pausa para respirar', 'As estrelas esperam por você. Pipo também aproveita para ajeitar o cachecol.', [
        { label: 'Continuar', action: 'resume' }, { label: 'Reiniciar fase', action: 'retry', secondary: true }, { label: 'Menu', action: 'menu', secondary: true },
      ], '☾');
    } else if (game.state === 'PAUSED') {
      game.state = 'PLAYING'; screen.hidden = true; updateHud();
    }
  }

  function finishLevel() {
    particles(game.level.goal.x, 365, 30, '#fff0a3', 210);
    sound(650, .42, 'triangle', 420);
    game.score += 100;
    if (game.levelIndex < 2) {
      unlocked = Math.max(unlocked, game.levelIndex + 1);
      try { localStorage.setItem(SAVE_KEY, JSON.stringify({ unlocked })); } catch { /* Optional local progress. */ }
      game.state = 'LEVEL_COMPLETE';
      showScreen('Entrega feita!', `Pipo concluiu ${game.level.name}. As estrelas já estão mandando a próxima encomenda.`, [
        { label: 'Próxima fase', action: 'next' }, { label: 'Menu', action: 'menu', secondary: true },
      ], '✉');
    } else {
      game.state = 'VICTORY';
      showScreen('O céu voltou a sorrir!', `Pipo entregou ${game.collected} cartas e fez ${game.score} pontos. Até o Rabugão pediu um abraço. Fim!`, [
        { label: 'Jogar de novo', action: 'start' }, { label: 'Menu', action: 'menu', secondary: true },
      ], '★');
    }
    updateHud();
  }

  function damage(force = 0) {
    const p = game.player;
    if (p.invulnerable > 0 || game.state !== 'PLAYING') return;
    p.health -= 1;
    p.invulnerable = 1.45;
    p.hurtTime = .42;
    p.vx = force || (p.facing > 0 ? -230 : 230);
    p.vy = -260;
    particles(p.x + 15, p.y + 18, 12, '#ff8da6');
    sound(250, .24, 'sawtooth', -130);
    if (p.health <= 0) {
      game.state = 'GAME_OVER';
      showScreen('As cartas vão esperar', 'Pipo ficou sem fôlego, mas uma boa soneca resolve tudo. Tente esta fase de novo!', [
        { label: 'Tentar novamente', action: 'retry' }, { label: 'Menu', action: 'menu', secondary: true },
      ], '♡');
    }
    updateHud();
  }

  function special() {
    const p = game.player;
    if (p.specialCooldown > 0) return;
    p.specialCooldown = 1.7;
    game.burstTime = .35;
    particles(p.x + 15, p.y + 20, 24, '#bff7ff', 210);
    sound(390, .25, 'triangle', 390);
    for (const foe of game.level.enemies) {
      if (!foe.alive) continue;
      if (Math.hypot(foe.x - (p.x + 15), foe.y - (p.y + 20)) < 130) {
        foe.stunned = 2.4;
        foe.x = Math.max(foe.min, Math.min(foe.max, foe.x + (foe.x > p.x ? 35 : -35)));
        particles(foe.x, foe.y, 8, '#e5faff');
      }
    }
    const boss = game.level.boss;
    if (boss && !boss.defeated && boss.mode === 'exposed' && Math.abs(boss.x - p.x) < 170) {
      boss.hp -= 1;
      boss.hitFlash = .4;
      boss.mode = 'recoil';
      boss.timer = 1.1;
      boss.waves = [];
      game.score += 50;
      particles(boss.x, boss.y, 24, '#ffe993', 220);
      sound(720, .35, 'triangle', -250);
      if (boss.hp <= 0) { boss.defeated = true; boss.waves = []; game.score += 150; }
      updateHud();
    }
  }

  const overlaps = (a, b) => a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
  const approach = (current, target, step) => current < target ? Math.min(target, current + step) : Math.max(target, current - step);

  function updateEnemies(dt) {
    const p = game.player;
    for (const foe of game.level.enemies) {
      if (!foe.alive) continue;
      foe.timer += dt;
      if (foe.stunned > 0) foe.stunned = Math.max(0, foe.stunned - dt);
      else if (foe.type === 'roller') foe.x += foe.direction * 65 * dt;
      else if (foe.type === 'hopper') {
        foe.x += foe.direction * 43 * dt;
        foe.y = foe.originY - Math.max(0, Math.sin(foe.timer * 3.4)) * 68;
      } else {
        foe.x += foe.direction * 52 * dt;
        foe.y = foe.originY + Math.sin(foe.timer * 2.5) * 20;
      }
      if (foe.x < foe.min) { foe.x = foe.min; foe.direction = 1; }
      if (foe.x > foe.max) { foe.x = foe.max; foe.direction = -1; }
      const box = { x: foe.x - 16, y: foe.y - 15, w: 32, h: 30 };
      if (overlaps(p, box) && foe.stunned <= 0) {
        if (p.vy > 90 && p.y + p.h - p.vy * dt <= box.y + 12) {
          foe.alive = false;
          p.vy = -390;
          p.grounded = false;
          game.score += 20;
          particles(foe.x, foe.y, 14, '#fff0ae');
          sound(570, .14, 'triangle', 200);
          updateHud();
        } else damage(p.x < foe.x ? -220 : 220);
      }
    }
  }

  function updateBoss(dt) {
    const boss = game.level.boss;
    if (!boss || boss.defeated) return;
    if (game.player.x >= 2160) boss.awake = true;
    if (!boss.awake) return;
    boss.timer -= dt;
    boss.hitFlash = Math.max(0, boss.hitFlash - dt);
    if (boss.mode === 'warning' && boss.timer <= 0) {
      boss.mode = 'attack'; boss.timer = boss.hp <= 2 ? 2.1 : 1.55;
      boss.waves.push({ x: boss.x - 62, y: 436 });
      boss.secondWave = boss.hp <= 2 ? .7 : -1;
      sound(220, .3, 'sawtooth', -100);
    } else if (boss.mode === 'attack') {
      if (boss.secondWave > 0) {
        boss.secondWave -= dt;
        if (boss.secondWave <= 0) boss.waves.push({ x: boss.x - 62, y: 436 });
      }
      for (const wave of boss.waves) {
        wave.x -= 260 * dt;
        if (overlaps(game.player, { x: wave.x - 15, y: wave.y - 15, w: 30, h: 30 })) damage(-210);
      }
      boss.waves = boss.waves.filter((wave) => wave.x > boss.x - 680);
      if (boss.timer <= 0) { boss.mode = 'exposed'; boss.timer = 3.1; }
    } else if (boss.timer <= 0) {
      boss.mode = 'warning'; boss.timer = boss.hp <= 2 ? 1.15 : 1.6;
      boss.waves = [];
    }
    if (overlaps(game.player, { x: boss.x - 43, y: boss.y - 28, w: 86, h: 75 })) {
      damage(game.player.x < boss.x ? -210 : 210);
    }
  }

  function update(dt) {
    const p = game.player;
    game.time += dt;
    game.burstTime = Math.max(0, game.burstTime - dt);
    p.invulnerable = Math.max(0, p.invulnerable - dt);
    p.hurtTime = Math.max(0, p.hurtTime - dt);
    p.landSquash = Math.max(0, p.landSquash - dt * 4);
    p.specialCooldown = Math.max(0, p.specialCooldown - dt);
    p.jumpBuffer = Math.max(0, p.jumpBuffer - dt);
    if (p.specialRequested) { p.specialRequested = false; special(); }

    const direction = Number(keys.right) - Number(keys.left);
    p.vx = approach(p.vx, direction * 285, (direction ? (p.grounded ? 1900 : 1150) : (p.grounded ? 2200 : 450)) * dt);
    if (direction) p.facing = direction;
    if (p.grounded) p.coyote = .11;
    else p.coyote = Math.max(0, p.coyote - dt);
    if (p.jumpBuffer > 0 && p.coyote > 0) {
      p.vy = -620; p.grounded = false; p.coyote = 0; p.jumpBuffer = 0;
      particles(p.x + 15, p.y + p.h, 9, '#e8f6d5');
      sound(440, .13, 'sine', 230);
    }
    p.vy = Math.min(820, p.vy + 1450 * dt);
    const solids = [...game.level.ground, ...game.level.platforms];
    const previousBottom = p.y + p.h;
    p.x += p.vx * dt;
    p.x = Math.max(0, Math.min(game.level.width - p.w, p.x));
    for (const solid of solids) {
      if (solid.h > 50 || !overlaps(p, solid)) continue;
      if (p.y + p.h > solid.y + 8 && p.y < solid.y + solid.h && p.vy > 0) {
        if (p.vx > 0 && p.x < solid.x) p.x = solid.x - p.w;
        if (p.vx < 0 && p.x > solid.x) p.x = solid.x + solid.w;
      }
    }
    p.y += p.vy * dt;
    p.grounded = false;
    if (p.vy >= 0) {
      for (const solid of solids) {
        if (p.x + p.w > solid.x + 3 && p.x < solid.x + solid.w - 3 && previousBottom <= solid.y + 7 && p.y + p.h >= solid.y) {
          p.y = solid.y - p.h;
          if (p.vy > 280) { p.landSquash = 1; particles(p.x + 15, p.y + p.h, 6, '#e7f7d5', 70); }
          p.vy = 0; p.grounded = true;
          break;
        }
      }
    }
    if (p.grounded && p.x > p.checkpointX + 90 && p.x < game.level.width - 220) {
      p.checkpointX = p.x; p.checkpointY = p.y;
    }
    if (p.y > 560) {
      damage();
      if (game.state === 'PLAYING') { p.x = p.checkpointX; p.y = p.checkpointY; p.vx = 0; p.vy = 0; }
    }
    for (const hazard of game.level.hazards) if (overlaps(p, hazard)) damage(p.x < hazard.x ? -190 : 190);
    for (const item of game.level.letters) {
      if (!item.taken && Math.hypot(item.x - p.x - 15, item.y - p.y - 20) < 30) {
        item.taken = true; game.collected += 1; game.score += 10;
        particles(item.x, item.y, 12, '#ffec9b');
        sound(650, .15, 'sine', 280);
        updateHud();
      }
    }
    updateEnemies(dt);
    updateBoss(dt);
    if (game.state === 'PLAYING' && p.x + p.w > game.level.goal.x - 22 && (!game.level.boss || game.level.boss.defeated)) finishLevel();
    game.camera = approach(game.camera, Math.max(0, Math.min(game.level.width - 960, p.x - 360)), 1550 * dt);
    for (const part of game.particles) {
      part.x += part.vx * dt; part.y += part.vy * dt;
      part.vy += 180 * dt; part.life -= dt;
    }
    game.particles = game.particles.filter((part) => part.life > 0);
  }

  function action(name) {
    switch (name) {
      case 'start': loadLevel(0); break;
      case 'continue': loadLevel(unlocked); break;
      case 'next': loadLevel(game.levelIndex + 1, true); break;
      case 'retry': loadLevel(game.levelIndex, true); break;
      case 'resume': pause(); break;
      case 'menu': menu(); break;
      case 'sound': muted = !muted; menu(); break;
      case 'how':
        game.state = 'HOW';
        showScreen('Como jogar', 'Mova com A/D ou setas, pule com Espaço e aperte X para um sopro que atordoa criaturas. Pule por cima dos perigos. No último mundo, desvie das estrelas do Rabugão e use X quando ele ficar cansado. No celular, use os botões na tela.', [{ label: 'Entendi!', action: 'menu' }], '✧');
        break;
      default: break;
    }
  }

  screen.addEventListener('click', (event) => {
    const button = event.target.closest('[data-action]');
    if (button) action(button.dataset.action);
  });
  pauseButton.addEventListener('click', pause);
  document.addEventListener('keydown', (event) => {
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;
    const key = event.key.toLowerCase();
    if (['arrowleft', 'arrowright', 'arrowup', ' ', 'a', 'd', 'x', 'escape'].includes(key)) event.preventDefault();
    if (key === 'escape') { if (['PLAYING', 'PAUSED'].includes(game.state)) pause(); return; }
    if (key === 'enter' && game.state !== 'PLAYING') { event.preventDefault(); screen.querySelector('[data-action]')?.click(); return; }
    if (game.state !== 'PLAYING') return;
    if (key === 'a' || key === 'arrowleft') keys.left = true;
    if (key === 'd' || key === 'arrowright') keys.right = true;
    if (key === ' ' || key === 'arrowup') { if (!keys.jump) game.player.jumpBuffer = .14; keys.jump = true; }
    if (key === 'x' && !event.repeat) game.player.specialRequested = true;
  });
  document.addEventListener('keyup', (event) => {
    const key = event.key.toLowerCase();
    if (key === 'a' || key === 'arrowleft') keys.left = false;
    if (key === 'd' || key === 'arrowright') keys.right = false;
    if (key === ' ' || key === 'arrowup') {
      keys.jump = false;
      if (game.player.vy < -200) game.player.vy *= .52;
    }
  });
  window.addEventListener('blur', () => { keys.left = false; keys.right = false; keys.jump = false; if (game.state === 'PLAYING') pause(); });
  root.querySelectorAll('[data-touch]').forEach((button) => {
    const control = button.dataset.touch;
    const release = (event) => {
      event.preventDefault();
      button.classList.remove('pressed');
      if (control === 'left' || control === 'right') keys[control] = false;
      if (control === 'jump') keys.jump = false;
    };
    button.addEventListener('pointerdown', (event) => {
      event.preventDefault();
      button.setPointerCapture(event.pointerId);
      button.classList.add('pressed');
      if (game.state !== 'PLAYING') return;
      if (control === 'left' || control === 'right') keys[control] = true;
      if (control === 'jump') { if (!keys.jump) game.player.jumpBuffer = .14; keys.jump = true; }
      if (control === 'special') game.player.specialRequested = true;
    });
    button.addEventListener('pointerup', release);
    button.addEventListener('pointercancel', release);
    button.addEventListener('lostpointercapture', release);
  });

  let previous = performance.now();
  let accumulator = 0;
  function frame(now) {
    const elapsed = Math.min((now - previous) / 1000, .05);
    previous = now;
    if (game.state === 'PLAYING') {
      accumulator += elapsed;
      let steps = 0;
      while (accumulator >= 1 / 120 && steps < 6 && game.state === 'PLAYING') {
        update(1 / 120);
        accumulator -= 1 / 120;
        steps += 1;
      }
      if (steps === 6) accumulator = 0;
    } else {
      game.time += elapsed * .35;
      accumulator = 0;
    }
    renderGame(ctx, game);
    requestAnimationFrame(frame);
  }
  menu();
  requestAnimationFrame(frame);
}
