// Pure game rules. The browser advances one beat every 620 ms.
export const LEVELS = [
  {name:'Praça dos Sorrisos',hint:'Abra as nuvens e conheça o primeiro visitante.',sky:'#c6eeec',map:[
    '###########','#p..c.s..e#','#..c...m..#','#...c.....#','#.........#','#..c......#','###########',
  ]},
  {name:'Ponte de Marshmallow',hint:'Encontre passagens entre pedras, pontes e nuvens.',sky:'#dce9fb',map:[
    '###########','#p..c.c..e#','#..c#...c.#','#s..#..w..#','#...c..c..#','#..m...s..#','###########',
  ]},
  {name:'Trilha das Estrelinhas',hint:'O vento muda de direção: observe os visitantes.',sky:'#e8ddfb',map:[
    '###########','#p.cc..s.e#','#.#.#c#.#.#','#..wm..c..#','#.#.#.#c#.#','#s..c..m..#','###########',
  ]},
  {name:'Bosque do Algodão',hint:'Use as pedras como abrigo e encontre itens surpresa.',sky:'#f9e1eb',map:[
    '###########','#p.c.c.s.e#','#..c.c.c..#','#m...#..w.#','#..s.#.c..#','#.c..m.c..#','###########',
  ]},
  {name:'Festa dos Confetes',hint:'Os convidados correm depressa; prepare uma fuga.',sky:'#ffe9cf',map:[
    '###########','#p..c.s..e#','#c#c..#c..#','#w..c...w.#','#..c#c..#.#','#s..c.m.s.#','###########',
  ]},
  {name:'Castelo da Neblina',hint:'A Rainha anuncia seu Vórtice de Espelhos. Espere o escudo abrir.',sky:'#d9d5fa',map:[
    '###########','#p..cs...e#','#.c.#..c..#','#....cbb..#','#.c...bb..#','#..m.c...s#','###########',
  ]},
];

export const ITEM_INFO = {
  skates:{name:'Patins de vento',icon:'➜',description:'Lilo corre mais rápido.'},
  wings:{name:'Asas de algodão',icon:'⌁',description:'Shift ou Asas avança duas casas.'},
  prism:{name:'Prisma de luz',icon:'✧',description:'As bolhas brilham mais longe.'},
  shield:{name:'Guarda-chuva',icon:'◒',description:'Protege de uma trombada.'},
};
const DIRECTIONS = [[1,0],[-1,0],[0,1],[0,-1]];
export const key = (x,y) => `${x},${y}`;
export const point = (cell) => cell.split(',').map(Number);
const same = (a,b) => a.x === b.x && a.y === b.y;
function random(state) {state.rng=(Math.imul(state.rng,1664525)+1013904223)>>>0;return state.rng/4294967296;}
function copy(state) {
  return {...state,player:{...state.player},clouds:new Set(state.clouds),stars:new Set(state.stars),
    items:new Map(state.items),enemies:state.enemies.map((enemy)=>({...enemy})),
    bubbles:state.bubbles.map((bubble)=>({...bubble})),stats:{...state.stats},
    boss:state.boss?{...state.boss,cells:new Set(state.boss.cells),target:state.boss.target&&{...state.boss.target}}:null};
}

export function createLevel(index,seed=Math.floor(Math.random()*4294967296)) {
  const level=LEVELS[index];if(!level)throw new RangeError('Fase inexistente');
  const width=level.map[0].length,height=level.map.length;
  const walls=new Set(),clouds=new Set(),stars=new Set(),enemies=[],bossCells=new Set();
  let player,exit;
  level.map.forEach((line,y)=>{
    if(line.length!==width)throw new Error('Mapa irregular');
    [...line].forEach((tile,x)=>{
      const cell=key(x,y);
      if(tile==='#')walls.add(cell);
      else if(tile==='c')clouds.add(cell);
      else if(tile==='s')stars.add(cell);
      else if(tile==='m'||tile==='w')enemies.push({id:enemies.length+1,x,y,kind:tile==='w'?'hunter':'drifter'});
      else if(tile==='p')player={x,y};
      else if(tile==='e')exit=cell;
      else if(tile==='b')bossCells.add(cell);
      else if(tile!=='.')throw new Error(`Peça desconhecida: ${tile}`);
    });
  });
  if(!player||!exit||(index===LEVELS.length-1?bossCells.size!==4:bossCells.size!==0))throw new Error('Mapa incompleto');
  return {index,width,height,spawn:{...player},player,exit,walls,clouds,stars,enemies,
    items:new Map(),bubbles:[],beat:0,rng:seed>>>0,brokenSinceItem:0,
    stats:{skates:0,wings:0,range:2,capacity:2,shield:0},
    boss:bossCells.size?{cells:bossCells,hearts:4,maxHearts:4,mode:'shield',target:null}:null,
    collected:0,invulnerable:0,complete:false};
}
export function ready(state) {return !state.stars.size&&!state.enemies.length&&(!state.boss||!state.boss.hearts);}
function blocked(state,x,y) {
  const cell=key(x,y);
  return x<0||y<0||x>=state.width||y>=state.height||state.walls.has(cell)||state.clouds.has(cell)||
    (state.boss?.hearts&&state.boss.cells.has(cell));
}
function collectItem(state,cell) {
  const item=state.items.get(cell);if(!item)return null;
  state.items.delete(cell);
  if(item==='skates')state.stats.skates=1;
  else if(item==='wings')state.stats.wings=1;
  else if(item==='prism')state.stats.range=Math.min(4,state.stats.range+1);
  else state.stats.shield=Math.min(2,state.stats.shield+1);
  return item;
}
function bump(state) {
  if(state.invulnerable)return 'safe';
  const shielded=state.stats.shield>0;
  if(shielded)state.stats.shield-=1;
  state.player={...state.spawn};state.invulnerable=3;
  return shielded?'shield':'respawn';
}
export function move(state,dx,dy) {
  if(!Number.isInteger(dx)||!Number.isInteger(dy)||Math.abs(dx)+Math.abs(dy)!==1)throw new TypeError('Direção inválida');
  if(state.complete)return {state,event:'complete'};
  const x=state.player.x+dx,y=state.player.y+dy,cell=key(x,y);
  if(blocked(state,x,y)||state.bubbles.some((bubble)=>bubble.x===x&&bubble.y===y))return {state,event:'blocked'};
  const next=copy(state);next.player={x,y};
  if(next.enemies.some((enemy)=>same(enemy,next.player)))return {state:next,event:bump(next)};
  let event='move';
  if(next.stars.delete(cell)){next.collected+=1;event='star';}
  const item=collectItem(next,cell);if(item)event='item';
  if(cell===next.exit){if(ready(next)){next.complete=true;event='finished';}else event='locked';}
  return {state:next,event,item};
}
export function dash(state,dx,dy) {
  if(!state.stats.wings)return {state,event:'noWings'};
  const first=move(state,dx,dy);
  if(['blocked','finished','respawn'].includes(first.event))return first;
  const second=move(first.state,dx,dy);
  if(second.event==='blocked')return first;
  return second.event==='move'&&first.event!=='move'?{...second,event:first.event,item:first.item}:second;
}
export function placeBubble(state) {
  if(state.complete||state.bubbles.length>=state.stats.capacity||state.bubbles.some((bubble)=>same(bubble,state.player)))return {state,event:'limit'};
  const next=copy(state);next.bubbles.push({...next.player,fuse:3,range:next.stats.range});
  return {state:next,event:'placed'};
}
export function lightPath(state,bubble) {
  const cells=[key(bubble.x,bubble.y)];
  for(const [dx,dy] of DIRECTIONS)for(let distance=1;distance<=bubble.range;distance+=1){
    const x=bubble.x+dx*distance,y=bubble.y+dy*distance,cell=key(x,y);
    if(x<0||y<0||x>=state.width||y>=state.height||state.walls.has(cell))break;
    cells.push(cell);if(state.clouds.has(cell))break;
  }
  return cells;
}
export function bossHazardCells(state) {
  if(!state.boss?.target||!state.boss.hearts)return new Set();
  const {x,y}=state.boss.target,cells=new Set();
  for(let col=1;col<state.width-1;col+=1)cells.add(key(col,y));
  for(let row=1;row<state.height-1;row+=1)cells.add(key(x,row));
  if(state.boss.hearts<=2){
    const extraRow=y===state.height-2?y-1:y+1;
    for(let col=1;col<state.width-1;col+=1)cells.add(key(col,extraRow));
  }
  return cells;
}
function distances(state) {
  const start=key(state.player.x,state.player.y),result=new Map([[start,0]]),queue=[state.player];
  for(const position of queue)for(const [dx,dy] of DIRECTIONS){
    const x=position.x+dx,y=position.y+dy,cell=key(x,y);
    if(blocked(state,x,y)||result.has(cell)||state.bubbles.some((bubble)=>bubble.x===x&&bubble.y===y))continue;
    result.set(cell,result.get(key(position.x,position.y))+1);queue.push({x,y});
  }
  return result;
}
function moveEnemies(state) {
  const danger=new Set(state.bubbles.filter((bubble)=>bubble.fuse<=1).flatMap((bubble)=>lightPath(state,bubble)));
  if(state.boss?.mode==='warning')for(const cell of bossHazardCells(state))danger.add(cell);
  const path=distances(state),occupied=new Set(state.enemies.map((enemy)=>key(enemy.x,enemy.y)));
  for(const enemy of state.enemies){
    const here=key(enemy.x,enemy.y),cadence=enemy.kind==='hunter'?2:3;
    if(state.beat%cadence!==0&&!(enemy.kind==='hunter'&&danger.has(here)))continue;
    occupied.delete(here);
    const choices=[[0,0],...DIRECTIONS].map(([dx,dy])=>({x:enemy.x+dx,y:enemy.y+dy,stay:!dx&&!dy})).filter(({x,y})=>{
      const cell=key(x,y);
      return !blocked(state,x,y)&&!occupied.has(cell)&&!state.bubbles.some((bubble)=>bubble.x===x&&bubble.y===y);
    });
    const score=(candidate)=>{
      const cell=key(candidate.x,candidate.y);
      return (danger.has(cell)?1000:0)+(path.get(cell)??80)+(candidate.stay?.6:0);
    };
    choices.sort((a,b)=>score(a)-score(b));
    if(choices.length)Object.assign(enemy,choices[0]);
    occupied.add(key(enemy.x,enemy.y));
  }
}
function spawnHelper(state) {
  if(!state.boss?.hearts||state.enemies.length>=3)return;
  for(const [x,y] of [[8,5],[2,5],[8,2]]){
    const cell=key(x,y);
    if(blocked(state,x,y)||state.enemies.some((enemy)=>key(enemy.x,enemy.y)===cell)||
       state.bubbles.some((bubble)=>key(bubble.x,bubble.y)===cell)||cell===key(state.player.x,state.player.y))continue;
    state.enemies.push({id:100+state.beat,x,y,kind:'hunter'});break;
  }
}
export function tick(state) {
  if(state.complete)return {state,event:'complete',events:[],light:new Set(),attack:new Set()};
  const next=copy(state),events=[],light=new Set(),attack=new Set();
  next.beat+=1;next.invulnerable=Math.max(0,next.invulnerable-1);
  if(next.boss?.hearts){
    const phase=next.beat%8;
    next.boss.mode=phase===3?'warning':phase===4?'attack':phase===5||phase===6?'open':'shield';
    if(phase===3){next.boss.target={...next.player};events.push('bossWarning');}
    if(phase===4){for(const cell of bossHazardCells(next))attack.add(cell);events.push('bossAttack');}
  }
  for(const bubble of next.bubbles)bubble.fuse-=1;
  const pending=next.bubbles.filter((bubble)=>bubble.fuse<=0),exploded=new Set();
  while(pending.length){
    const bubble=pending.shift(),origin=key(bubble.x,bubble.y);
    if(exploded.has(origin))continue;
    exploded.add(origin);
    for(const cell of lightPath(next,bubble)){
      light.add(cell);
      if(next.clouds.delete(cell)){
        next.brokenSinceItem+=1;
        if(random(next)<.48||next.brokenSinceItem>=3){
          const roll=random(next),item=roll<.38?'skates':roll<.68?'wings':roll<.88?'prism':'shield';
          next.items.set(cell,item);next.brokenSinceItem=0;events.push('itemDrop');
        }
      }
      for(const other of next.bubbles)if(key(other.x,other.y)===cell&&!exploded.has(cell))pending.push(other);
    }
  }
  next.bubbles=next.bubbles.filter((bubble)=>!exploded.has(key(bubble.x,bubble.y)));
  if(light.size){
    const before=next.enemies.length;
    next.enemies=next.enemies.filter((enemy)=>!light.has(key(enemy.x,enemy.y)));
    if(before!==next.enemies.length)events.push('enemyCleared');
    events.push('pop');
  }
  if(next.boss?.hearts&&next.boss.mode==='open'&&[...next.boss.cells].some((cell)=>light.has(cell))){
    next.boss.hearts-=1;events.push(next.boss.hearts?'bossHit':'bossCleared');
    if(next.boss.hearts===3||next.boss.hearts===1)spawnHelper(next);
  }
  moveEnemies(next);
  const playerCell=key(next.player.x,next.player.y);
  if(light.has(playerCell)||attack.has(playerCell)||next.enemies.some((enemy)=>key(enemy.x,enemy.y)===playerCell))events.push(bump(next));
  const event=events.includes('respawn')?'respawn':events.includes('shield')?'shield':events.at(-1)??'tick';
  return {state:next,event,events,light,attack};
}
