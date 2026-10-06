import {LEVELS, createLevel, key, move, placeBubble, ready, tick, point} from './core.mjs';

const root = document.querySelector('[data-bubble-game]');
const canvas = root.querySelector('[data-bubble-canvas]');
const ctx = canvas.getContext('2d');
const overlay = root.querySelector('[data-bubble-overlay]');
const status = root.querySelector('[data-bubble-status]');
const levelLabel = root.querySelector('[data-bubble-level]');
const countLabel = root.querySelector('[data-bubble-count]');
const bossLabel = root.querySelector('[data-bubble-boss]');
const soundButton = root.querySelector('[data-bubble-sound]');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const storeKey = 'voidwielder-lilo-unlocked-v1';
const board = {x: 108, y: 106, size: 70};

let state = createLevel(0), unlocked = 0, playing = false, soundOn = true;
let audio = null, light = new Set(), lightUntil = 0, pointer = null, lastMove = 0;
let lastBreeze = 0;
try { unlocked = Math.min(LEVELS.length - 1, Math.max(0, Number(localStorage.getItem(storeKey)) || 0)); } catch { /* Optional save. */ }

function say(text) { status.textContent = text; }
function chime(frequency = 620) {
  if (!soundOn) return;
  try {
    audio ||= new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audio.createOscillator(), gain = audio.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(frequency, audio.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(frequency * 1.35, audio.currentTime + .13);
    gain.gain.setValueAtTime(.08, audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(.001, audio.currentTime + .24);
    oscillator.connect(gain).connect(audio.destination);
    oscillator.start(); oscillator.stop(audio.currentTime + .25);
  } catch { /* The game stays silent and playable. */ }
}
function hud() {
  levelLabel.textContent = `${String(state.index + 1).padStart(2, '0')} / 06 · ${LEVELS[state.index].name}`;
  countLabel.textContent = `✦ ${state.stars.size} estrela${state.stars.size === 1 ? '' : 's'} · ☁ ${state.shadows.size} nuven${state.shadows.size === 1 ? 'zinha' : 'zinhas'}`;
  bossLabel.textContent = state.boss ? `Rainha Névoa ${'♥'.repeat(state.bossHearts)}${'♡'.repeat(3 - state.bossHearts)}` : 'Bolhas de luz disponíveis: ∞';
  bossLabel.classList.toggle('is-boss', Boolean(state.boss));
}
function action(text, fn, secondary = false) {
  const button = document.createElement('button');
  button.type = 'button'; button.textContent = text;
  if (secondary) button.className = 'secondary';
  button.addEventListener('click', fn);
  return button;
}
function show(kicker, title, copy, buttons, levels = false) {
  overlay.hidden = false;
  overlay.querySelector('[data-bubble-kicker]').textContent = kicker;
  overlay.querySelector('[data-bubble-title]').textContent = title;
  overlay.querySelector('[data-bubble-copy]').textContent = copy;
  overlay.querySelector('[data-bubble-actions]').replaceChildren(...buttons);
  const choices = overlay.querySelector('[data-bubble-choices]');
  choices.replaceChildren(); choices.hidden = !levels;
  if (levels) LEVELS.forEach((level, index) => {
    const button = action(`${index + 1} · ${level.name}`, () => start(index));
    button.disabled = index > unlocked;
    button.setAttribute('aria-label', index > unlocked ? `Fase ${index + 1} bloqueada` : `Jogar fase ${index + 1}: ${level.name}`);
    choices.append(button);
  });
  overlay.querySelector('[data-bubble-actions] button')?.focus();
}
function welcome() {
  playing = false; state = createLevel(unlocked); hud();
  say('Lilo espera uma ajudinha para acender o festival.');
  show('UM FESTIVAL FEITO DE LUZ', 'Olá! Eu sou o Lilo ✦',
    'Solte bolhas de luz para abrir nuvens fofas e acordar as nuvenzinhas cinzas. Recolha as estrelas e entre no portal. Se a luz encostar em você, Lilo volta ao início da fase: sem perder vidas.',
    [action('Vamos brincar →', () => start(unlocked)), action('Como jogar', help, true)], true);
}
function help() {
  show('COMO JOGAR', 'Luz, bolhas e confete!',
    'Setas ou WASD movem Lilo. Espaço coloca uma bolha, que brilha depois de três batidas. Afaste-se da luz! Pedras seguram o brilho; nuvens macias somem. No celular, use os botões abaixo ou deslize no tabuleiro.',
    [action('Entendi!', () => start(state.index)), action('Voltar', welcome, true)]);
}
function start(index) {
  if (index > unlocked || index < 0) return;
  state = createLevel(index); playing = true; light = new Set(); lightUntil = 0;
  overlay.hidden = true; hud(); say(LEVELS[index].hint);
  canvas.focus();
}
function won() {
  playing = false; chime(800);
  const next = state.index + 1, finale = next >= LEVELS.length;
  if (!finale) {
    unlocked = Math.max(unlocked, next);
    try { localStorage.setItem(storeKey, String(unlocked)); } catch { /* Optional save. */ }
  }
  show(finale ? 'FESTIVAL COMPLETO' : `FASE ${state.index + 1} COMPLETA`,
    finale ? 'O céu ganhou todas as cores!' : 'Mais um cantinho iluminado!',
    finale ? 'A Rainha Névoa descobriu que podia brincar junto. Lilo e você fizeram um festival para todo mundo.'
      : 'As nuvenzinhas acordaram e as estrelas estão em casa. O próximo lugar já está esperando por Lilo.',
    [action(finale ? 'Brincar de novo' : 'Próxima fase →', () => start(finale ? 0 : next)),
      action('Escolher fase', welcome, true)]);
}
function walk(dx, dy) {
  if (!playing || performance.now() - lastMove < 115) return;
  const result = move(state, dx, dy); state = result.state; lastMove = performance.now();
  if (result.event === 'blocked') say('Uma pedra, nuvem ou visitante está no caminho. Tente outra direção.');
  else if (result.event === 'star') { say('Uma estrelinha resgatada! ✦'); chime(690); }
  else if (result.event === 'locked') say('O portal acorda quando todas as estrelas e nuvenzinhas forem libertadas.');
  else if (result.event === 'finished') { hud(); won(); return; }
  else if (ready(state)) say('Tudo brilhando! Vá até o portal colorido.');
  hud();
}
function bubble() {
  if (!playing) return;
  const result = placeBubble(state); state = result.state;
  say(result.event === 'placed' ? 'Bolha acesa! Saia do caminho antes de três batidas.' : 'Lilo pode cuidar de duas bolhas por vez.');
  if (result.event === 'placed') chime(430);
}
function beat() {
  if (!playing) return;
  const result = tick(state); state = result.state; light = result.light;
  if (light.size) lightUntil = performance.now() + (reduced.matches ? 180 : 480);
  if (result.event === 'respawn') { say('Ops! A luz trouxe Lilo de volta ao começo. Tudo continua no lugar.'); chime(230); }
  else if (result.event === 'bossHit') { say('O escudo apagou! A Rainha Névoa levou uma bolha de alegria.'); chime(850); }
  else if (result.event === 'bossCleared') { say('A Rainha Névoa virou amiga! Pegue a estrela e vá ao portal.'); chime(980); }
  else if (result.event === 'pop') { say(ready(state) ? 'Tudo brilhando! Vá até o portal colorido.' : 'Puf! Um pouco mais de luz no festival.'); chime(570); }
  if (state.bossHearts && state.beat % 6 === 5 && lastBreeze !== state.beat) {
    say('Atenção: o vento lilás vai passar pela fileira da Rainha!'); lastBreeze = state.beat;
  }
  hud();
}
setInterval(beat, 650);

const directions = {ArrowUp:[0,-1],KeyW:[0,-1],ArrowDown:[0,1],KeyS:[0,1],ArrowLeft:[-1,0],KeyA:[-1,0],ArrowRight:[1,0],KeyD:[1,0]};
document.addEventListener('keydown', (event) => {
  if (!playing || ['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName)) return;
  if (directions[event.code]) {event.preventDefault(); walk(...directions[event.code]);}
  else if (event.code === 'Space') {event.preventDefault(); bubble();}
  else if (event.code === 'Escape') {event.preventDefault(); playing = false; show('UMA PAUSA MERECIDA', 'Respire uma nuvem', 'O festival espera você. Seu progresso nesta fase fica no tabuleiro enquanto descansa.', [action('Continuar →', () => {overlay.hidden = true; playing = true; canvas.focus();}), action('Recomeçar fase', () => start(state.index), true)]);}
});
root.querySelectorAll('[data-bubble-direction]').forEach((button) => button.addEventListener('click', () => walk(...directions[button.dataset.bubbleDirection])));
root.querySelector('[data-bubble-place]').addEventListener('click', bubble);
root.querySelector('[data-bubble-restart]').addEventListener('click', () => start(state.index));
soundButton.addEventListener('click', () => {soundOn = !soundOn; soundButton.textContent = soundOn ? '♫ Som ligado' : '♫ Som desligado'; soundButton.setAttribute('aria-pressed', String(soundOn)); if (soundOn) chime();});
canvas.addEventListener('pointerdown', (event) => {pointer = [event.clientX, event.clientY];});
canvas.addEventListener('pointerup', (event) => {
  if (!pointer || !playing) return;
  const dx = event.clientX - pointer[0], dy = event.clientY - pointer[1]; pointer = null;
  if (Math.max(Math.abs(dx), Math.abs(dy)) < 25) return;
  Math.abs(dx) > Math.abs(dy) ? walk(Math.sign(dx), 0) : walk(0, Math.sign(dy));
});

function ellipse(x,y,rx,ry,color) {ctx.fillStyle=color;ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);ctx.fill();}
function box(x,y,w,h,r,color) {ctx.fillStyle=color;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();}
function star(x,y,r,color) {
  ctx.fillStyle=color;ctx.beginPath();
  for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5, q=i%2?r*.48:r;const px=x+Math.cos(a)*q,py=y+Math.sin(a)*q;i?ctx.lineTo(px,py):ctx.moveTo(px,py);}
  ctx.closePath();ctx.fill();
}
function cloud(x,y,tint) {ellipse(x-13,y+8,17,13,tint);ellipse(x+2,y-1,24,20,tint);ellipse(x+20,y+9,17,13,tint);box(x-27,y+6,55,19,10,tint);}
function face(x,y) {ellipse(x-8,y-2,2.5,3.5,'#313153');ellipse(x+8,y-2,2.5,3.5,'#313153');ellipse(x-16,y+6,5,3,'#ed8db1');ellipse(x+16,y+6,5,3,'#ed8db1');ctx.strokeStyle='#313153';ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y+4,5,0,Math.PI);ctx.stroke();}
function scene(time) {
  const grad=ctx.createLinearGradient(0,0,990,720);grad.addColorStop(0,LEVELS[state.index].sky);grad.addColorStop(1,'#fff1e1');ctx.fillStyle=grad;ctx.fillRect(0,0,990,720);
  for(let i=0;i<16;i++){const x=35+(i*127)%920,y=30+(i*97)%640;star(x,y,2.5,i%2?'#fff9d9':'#ffffffbb');}
  cloud(61,65,'#ffffff8c');cloud(919,610,'#ffffff8c');
  box(board.x-15,board.y-15,800,520,28,'#ffffffcf');box(board.x-6,board.y-6,782,502,20,'#71adba');
  for(let y=0;y<state.height;y++)for(let x=0;x<state.width;x++){
    const px=board.x+x*board.size,py=board.y+y*board.size,k=key(x,y);
    box(px+2,py+2,66,66,10,(x+y)%2?'#e9f6e8':'#f5fae9');
    if(state.walls.has(k)){box(px+5,py+5,60,60,11,'#9186b8');box(px+10,py+9,50,41,9,'#aaa0ca');star(px+48,py+21,4,'#f8d8fa');}
    if(state.clouds.has(k)){cloud(px+34,py+31,'#f7aac1');ellipse(px+23,py+26,3,3,'#fff6');}
    if(state.stars.has(k)){const bob=reduced.matches?0:Math.sin(time/350+x)*3;ellipse(px+35,py+37,22,20,'#ffe8a366');star(px+35,py+34+bob,18,'#ffcd66');star(px+35,py+34+bob,8,'#fff4c2');}
    if(state.shadows.has(k)){cloud(px+34,py+31,'#a5a4c2');face(px+34,py+34);star(px+13,py+15,4,'#f7e5b4');}
    if(state.exit===k){const open=ready(state);box(px+9,py+9,52,53,25,open?'#ffb9cf':'#b7afce');box(px+15,py+15,40,47,20,open?'#fce69c':'#ebe6f1');star(px+35,py+35,11,open?'#f6a162':'#aca1c5');}
    if(state.boss===k&&state.bossHearts){cloud(px+34,py+30,'#846fa9');face(px+34,py+33);star(px+35,py-2,11,'#ffcf75');if(state.beat%4<2)ctx.strokeStyle='#ffffffb9';else ctx.strokeStyle='#ffe49e';ctx.lineWidth=3;ctx.beginPath();ctx.arc(px+35,py+35,31,0,Math.PI*2);ctx.stroke();}
  }
  for(const bomb of state.bubbles){const x=board.x+(bomb.x+.5)*board.size,y=board.y+(bomb.y+.5)*board.size;ellipse(x,y,23,23,'#b4eafb9c');ctx.strokeStyle='#fff';ctx.lineWidth=4;ctx.beginPath();ctx.arc(x,y,23,0,Math.PI*2);ctx.stroke();star(x,y,12,'#fff5b5');}
  if(state.bossHearts&&state.beat%6===5){box(board.x+3,board.y+4*board.size+3,764,64,8,'#d0a5f077');}
  if(performance.now()<lightUntil)for(const lit of light){const[x,y]=point(lit);const px=board.x+x*board.size,py=board.y+y*board.size;box(px+4,py+4,62,62,15,'#fff1a6c8');star(px+35,py+35,23,'#ffffff');}
  const px=board.x+(state.player.x+.5)*board.size,py=board.y+(state.player.y+.5)*board.size;
  const bob=reduced.matches?0:Math.sin(time/270)*2;
  ellipse(px,py+24,22,6,'#647e7955');star(px,py-4+bob,29,'#ffe37d');ellipse(px,py+2+bob,24,22,'#ffe37d');face(px,py-1+bob);box(px-13,py+17+bob,26,6,4,'#8dd6cc');
  ctx.fillStyle='#496777';ctx.font='800 15px system-ui';ctx.textAlign='center';ctx.fillText(LEVELS[state.index].name,495,675);
}
function frame(time){scene(time);requestAnimationFrame(frame);} requestAnimationFrame(frame);
welcome();
