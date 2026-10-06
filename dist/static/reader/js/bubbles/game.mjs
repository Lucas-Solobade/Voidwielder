import {ITEM_INFO, LEVELS, createLevel, dash, move, placeBubble, ready, tick} from './core.mjs';
import {drawScene} from './art.mjs';

const root=document.querySelector('[data-bubble-game]');
const canvas=root.querySelector('[data-bubble-canvas]'),ctx=canvas.getContext('2d');
const overlay=root.querySelector('[data-bubble-overlay]');
const status=root.querySelector('[data-bubble-status]');
const levelLabel=root.querySelector('[data-bubble-level]');
const countLabel=root.querySelector('[data-bubble-count]');
const bossLabel=root.querySelector('[data-bubble-boss]');
const inventory=root.querySelector('[data-bubble-powerups]');
const soundButton=root.querySelector('[data-bubble-sound]');
const dashButton=root.querySelector('[data-bubble-dash]');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const storeKey='voidwielder-lilo-unlocked-v1';

let unlocked=0,state=createLevel(0),playing=false,started=false,menuPaused=false,soundOn=true,audio=null;
let pointer=null,lastMove=0,lastDirection=[1,0],playerFrom={...state.player,started:0,direction:1};
let enemyFrom=new Map(),light=new Set(),lightUntil=0,attack=new Set(),attackUntil=0;
try {unlocked=Math.min(LEVELS.length-1,Math.max(0,Number(localStorage.getItem(storeKey))||0));}
catch {/* Progress can remain in memory. */}

const STORY=[
  {kicker:'ERA UMA VEZ, NO CÉU DE LUMINÁRIA',title:'A noite perdeu suas cores',
    copy:'Toda estrela acendia uma canção para o Festival das Bolhas. Um dia, a Rainha Névoa guardou as cores em nuvens de algodão e o céu ficou silencioso.'},
  {kicker:'UMA PEQUENA ESTRELA, UMA GRANDE IDEIA',title:'Lilo encontrou a luz',
    copy:'Lilo descobriu que suas bolhas iluminam caminhos escondidos. Quando uma nuvem se abre, um presente pode aparecer. Alguns ajudam a correr, outros a voar por duas casas.'},
  {kicker:'O FESTIVAL PODE VOLTAR',title:'Vamos convidar todo mundo?',
    copy:'Os visitantes cinzas só precisam acordar. A Rainha Névoa é grandona e tem um Vórtice de Espelhos, mas talvez ela também queira fazer parte da festa.'},
];

function say(text){status.textContent=text;}
function chime(frequency=620){
  if(!soundOn)return;
  try {
    audio||=new (window.AudioContext||window.webkitAudioContext)();
    const oscillator=audio.createOscillator(),gain=audio.createGain();
    oscillator.type='sine';
    oscillator.frequency.setValueAtTime(frequency,audio.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(frequency*1.3,audio.currentTime+.13);
    gain.gain.setValueAtTime(.075,audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(.001,audio.currentTime+.23);
    oscillator.connect(gain).connect(audio.destination);
    oscillator.start();oscillator.stop(audio.currentTime+.24);
  }catch {/* Audio is optional. */}
}
function hud(){
  levelLabel.textContent=`${String(state.index+1).padStart(2,'0')} / 06 · ${LEVELS[state.index].name}`;
  countLabel.textContent=`✦ ${state.stars.size} estrela${state.stars.size===1?'':'s'} · ☁ ${state.enemies.length} visitante${state.enemies.length===1?'':'s'}`;
  const bossMode={shield:'Escudo aceso',warning:'Vórtice anunciado',attack:'Vórtice!',open:'Coração exposto'};
  bossLabel.textContent=state.boss?`Rainha Névoa ${'♥'.repeat(state.boss.hearts)}${'♡'.repeat(state.boss.maxHearts-state.boss.hearts)} · ${state.boss.hearts?bossMode[state.boss.mode]:'Amiga da festa'}`:'Bolhas de luz: ∞';
  bossLabel.classList.toggle('is-boss',Boolean(state.boss));
  const equipped=[];
  if(state.stats.skates)equipped.push('➜ Patins');
  if(state.stats.wings)equipped.push('⌁ Asas');
  if(state.stats.range>2)equipped.push(`✧ Alcance ${state.stats.range}`);
  if(state.stats.shield)equipped.push(`◒ Proteção ${state.stats.shield}`);
  inventory.textContent=equipped.length?equipped.join(' · '):'Itens surpresa nas nuvens rosadas';
  dashButton.disabled=!state.stats.wings;
}
function action(text,fn,secondary=false){
  const button=document.createElement('button');button.type='button';button.textContent=text;
  if(secondary)button.className='secondary';
  button.addEventListener('click',fn);return button;
}
function show(mode,kicker,title,copy,buttons,levels=false){
  overlay.hidden=false;overlay.dataset.mode=mode;
  overlay.querySelector('[data-bubble-kicker]').textContent=kicker;
  overlay.querySelector('[data-bubble-title]').textContent=title;
  overlay.querySelector('[data-bubble-copy]').textContent=copy;
  overlay.querySelector('[data-bubble-actions]').replaceChildren(...buttons);
  const choices=overlay.querySelector('[data-bubble-choices]');
  choices.replaceChildren();choices.hidden=!levels;
  if(levels)LEVELS.forEach((level,index)=>{
    const button=action(`${index+1} · ${level.name}`,()=>start(index));
    button.disabled=index>unlocked;
    button.setAttribute('aria-label',index>unlocked?`Fase ${index+1} bloqueada`:`Jogar fase ${index+1}: ${level.name}`);
    choices.append(button);
  });
  overlay.querySelector('[data-bubble-actions] button')?.focus({preventScroll:true});
  const dialog=overlay.querySelector('.bubble-dialog');
  const align=()=>{
    const top=Math.max(82,(window.innerHeight-dialog.offsetHeight)/2);
    window.scrollTo({top:window.scrollY+dialog.getBoundingClientRect().top-top,behavior:'auto'});
  };
  align();
  requestAnimationFrame(()=>requestAnimationFrame(align));
}
function intro(index=0){
  playing=false;if(!started)state=createLevel(unlocked);hud();
  const scene=STORY[index];
  say('Uma pequena história começou no céu de Luminária.');
  show('intro',scene.kicker,scene.title,scene.copy,[
    action(index===STORY.length-1?'Abrir o menu →':'Próxima cena →',()=>index===STORY.length-1?menu(menuPaused):intro(index+1)),
    action('Pular abertura',()=>menu(menuPaused),true),
  ]);
}
function menu(paused=false){
  playing=false;menuPaused=paused;
  if(!paused)state=createLevel(unlocked);
  hud();
  show('menu','LILO E O FESTIVAL DAS BOLHAS','O festival espera você',
    'Explore seis lugares, use bolhas de luz para abrir caminhos e encontre presentes nas nuvens. A última visita é ao castelo da Rainha Névoa.',
    [paused?action('Continuar →',resume):action(started?'Continuar aventura →':'Começar aventura →',()=>start(unlocked)),
      action('Escolher fase',levelMenu,true),action('Como jogar',help,true),action('Ver história',()=>intro(),true)]);
}
function levelMenu(){
  show('menu','SELEÇÃO DE FASES','Escolha um lugar',
    'Fases concluídas ficam disponíveis para visitar de novo. As próximas se abrem durante a aventura.',
    [action('Voltar ao menu',()=>menu(menuPaused),true)],true);
}
function help(){
  show('help','COMO JOGAR','Bolhas, luz e movimento',
    'Setas ou WASD movem Lilo; Espaço solta uma bolha que brilha após três batidas. Desvie do brilho e dos visitantes. Asas liberam o avanço de duas casas com Shift. No celular, use os botões ou deslize no tabuleiro. A Rainha anuncia o vórtice: saia da faixa rosada e acerte o coração quando o escudo abrir.',
    [menuPaused?action('Voltar ao jogo →',resume):action('Vamos brincar →',()=>start(state.index)),
      action('Voltar ao menu',()=>menu(menuPaused),true)]);
}
function start(index){
  if(index<0||index>unlocked)return;
  state=createLevel(index);playing=true;started=true;
  light=new Set();attack=new Set();lightUntil=0;attackUntil=0;
  playerFrom={...state.player,started:0,direction:1};enemyFrom=new Map();lastMove=0;
  overlay.hidden=true;hud();say(LEVELS[index].hint);canvas.focus({preventScroll:true});
  const shell=root.querySelector('.bubble-shell');
  window.scrollTo({top:window.scrollY+shell.getBoundingClientRect().top-82,behavior:'auto'});
}
function resume(){playing=true;overlay.hidden=true;canvas.focus({preventScroll:true});}
function won(){
  playing=false;chime(880);
  const next=state.index+1,finale=next>=LEVELS.length;
  if(!finale){unlocked=Math.max(unlocked,next);try{localStorage.setItem(storeKey,String(unlocked));}catch{/* Optional save. */}}
  show('complete',finale?'O FESTIVAL VOLTOU':'UM CANTINHO ACESO',
    finale?'A Rainha veio dançar!':'Mais luz para Luminária!',
    finale?'Lilo mostrou à Rainha Névoa que dividir as cores era mais divertido. As nuvens cinzas viraram confetes e o céu inteiro cantou junto.':
      'Os visitantes acordaram e as estrelas encontraram suas canções. O próximo lugar já espera por Lilo.',
    [action(finale?'Brincar de novo':'Próxima fase →',()=>start(finale?0:next)),action('Ir ao menu',()=>menu(),true)]);
}
function travel(dx,dy,fast=false){
  if(!playing||performance.now()-lastMove<(state.stats.skates?65:135))return;
  const before={...state.player},result=fast?dash(state,dx,dy):move(state,dx,dy);
  state=result.state;lastMove=performance.now();lastDirection=[dx,dy];
  if(before.x!==state.player.x||before.y!==state.player.y){
    playerFrom={...before,started:performance.now(),direction:dx||dy};
  }
  if(result.event==='blocked')say('Há uma pedra ou nuvem no caminho. Procure outra passagem.');
  else if(result.event==='noWings')say('Encontre Asas de algodão nas nuvens para avançar duas casas.');
  else if(result.event==='star'){say('Uma estrelinha resgatada! ✦');chime(700);}
  else if(result.event==='item'){say(`${ITEM_INFO[result.item].name}! ${ITEM_INFO[result.item].description}`);chime(760);}
  else if(result.event==='shield'||result.event==='respawn'){say('Lilo voltou ao começo, mas seu progresso ficou no mapa.');chime(250);}
  else if(result.event==='locked')say('O portal abre quando as estrelas e os visitantes forem libertados.');
  else if(result.event==='finished'){hud();won();return;}
  else if(ready(state))say('Tudo brilhando! Vá ao portal colorido.');
  hud();
}
function bubble(){
  if(!playing)return;
  const result=placeBubble(state);state=result.state;
  say(result.event==='placed'?'Bolha acesa! Saia do brilho antes de três batidas.':'Lilo só pode soltar duas bolhas por vez.');
  if(result.event==='placed')chime(430);
}
function beat(){
  if(!playing)return;
  const before={...state.player},oldEnemies=new Map(state.enemies.map((enemy)=>[enemy.id,{x:enemy.x,y:enemy.y}]));
  const result=tick(state);state=result.state;light=result.light;attack=result.attack;
  if(light.size)lightUntil=performance.now()+(reduced.matches?170:440);
  if(attack.size)attackUntil=performance.now()+(reduced.matches?170:490);
  const now=performance.now();
  enemyFrom=new Map(state.enemies.map((enemy)=>[enemy.id,{...(oldEnemies.get(enemy.id)??enemy),started:now}]));
  if(before.x!==state.player.x||before.y!==state.player.y)playerFrom={...before,started:now,direction:1};
  if(result.events.includes('respawn')){say('Puf! Lilo voltou ao início. Os caminhos abertos continuam abertos.');chime(230);}
  else if(result.events.includes('shield')){say('O guarda-chuva protegeu Lilo!');chime(580);}
  else if(result.events.includes('bossCleared')){say('A Rainha Névoa aceitou o convite! Recolha as estrelas e encontre o portal.');chime(980);}
  else if(result.events.includes('bossHit')){say('O coração da Rainha brilhou! Ela chamou um ajudante de névoa.');chime(840);}
  else if(result.events.includes('bossWarning'))say('Vórtice de Espelhos! Saia da linha rosada antes do sopro.');
  else if(result.events.includes('bossAttack'))say('O vórtice passou! O coração da Rainha ficará exposto por duas batidas.');
  else if(result.events.includes('itemDrop')){say('Uma nuvem revelou um presente! Encoste nele para pegar.');chime(650);}
  else if(result.events.includes('enemyCleared')){say('Um visitante acordou. O festival está mais perto!');chime(720);}
  else if(result.events.includes('pop'))say(ready(state)?'Tudo brilhando! Vá ao portal.':'Bolha de luz! Veja se apareceu um presente.');
  hud();
}
setInterval(beat,620);
const directions={ArrowUp:[0,-1],KeyW:[0,-1],ArrowDown:[0,1],KeyS:[0,1],ArrowLeft:[-1,0],KeyA:[-1,0],ArrowRight:[1,0],KeyD:[1,0]};
document.addEventListener('keydown',(event)=>{
  if(['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName))return;
  if(!playing){if(event.code==='Escape'&&overlay.dataset.mode!=='menu')menu();return;}
  if(directions[event.code]){event.preventDefault();travel(...directions[event.code]);}
  else if(event.code==='Space'){event.preventDefault();bubble();}
  else if(event.code==='ShiftLeft'||event.code==='ShiftRight'){event.preventDefault();travel(...lastDirection,true);}
  else if(event.code==='Escape'){event.preventDefault();menu(true);}
});
root.querySelectorAll('[data-bubble-direction]').forEach((button)=>button.addEventListener('click',()=>travel(...directions[button.dataset.bubbleDirection])));
root.querySelector('[data-bubble-place]').addEventListener('click',bubble);
dashButton.addEventListener('click',()=>travel(...lastDirection,true));
root.querySelector('[data-bubble-menu]').addEventListener('click',()=>menu(playing));
root.querySelector('[data-bubble-restart]').addEventListener('click',()=>start(state.index));
soundButton.addEventListener('click',()=>{soundOn=!soundOn;soundButton.textContent=soundOn?'♫ Som ligado':'♫ Som desligado';soundButton.setAttribute('aria-pressed',String(soundOn));if(soundOn)chime();});
canvas.addEventListener('pointerdown',(event)=>{pointer=[event.clientX,event.clientY];});
canvas.addEventListener('pointerup',(event)=>{
  if(!pointer||!playing)return;
  const dx=event.clientX-pointer[0],dy=event.clientY-pointer[1];pointer=null;
  if(Math.max(Math.abs(dx),Math.abs(dy))<24){bubble();return;}
  Math.abs(dx)>Math.abs(dy)?travel(Math.sign(dx),0):travel(0,Math.sign(dy));
});
function frame(time){drawScene(ctx,state,{time,reduced:reduced.matches,playerFrom,enemyFrom,light,lightUntil,attack,attackUntil});requestAnimationFrame(frame);}
requestAnimationFrame(frame);
intro();
