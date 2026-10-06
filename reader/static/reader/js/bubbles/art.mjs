import {ITEM_INFO, LEVELS, bossHazardCells, key, point, ready} from './core.mjs';

export const BOARD = {x:108,y:106,size:70};
const fill = (ctx,x,y,rx,ry,color) => {
  ctx.fillStyle=color;ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);ctx.fill();
};
const round = (ctx,x,y,w,h,r,color) => {
  ctx.fillStyle=color;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();
};
function star(ctx,x,y,r,color){
  ctx.fillStyle=color;ctx.beginPath();
  for(let i=0;i<10;i++){
    const a=-Math.PI/2+i*Math.PI/5,radius=i%2?r*.47:r;
    const px=x+Math.cos(a)*radius,py=y+Math.sin(a)*radius;
    i?ctx.lineTo(px,py):ctx.moveTo(px,py);
  }
  ctx.closePath();ctx.fill();
}
function cloud(ctx,x,y,color,scale=1){
  ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);
  fill(ctx,-15,8,20,16,color);fill(ctx,3,-1,27,23,color);fill(ctx,22,8,20,16,color);
  round(ctx,-34,7,68,22,11,color);ctx.restore();
}
function face(ctx,x,y,angry=false){
  fill(ctx,x-9,y-2,3,4,'#30334d');fill(ctx,x+9,y-2,3,4,'#30334d');
  fill(ctx,x-19,y+7,6,3,'#f3a3bd');fill(ctx,x+19,y+7,6,3,'#f3a3bd');
  ctx.strokeStyle='#30334d';ctx.lineWidth=2;ctx.beginPath();
  ctx.arc(x,y+5,angry?4:6,angry?Math.PI:0,angry?2*Math.PI:Math.PI);ctx.stroke();
}
function lerp(from,to,progress){return from+(to-from)*progress;}
function tileCenter(x,y){return [BOARD.x+(x+.5)*BOARD.size,BOARD.y+(y+.5)*BOARD.size];}

function drawTile(ctx,state,x,y,time,reduced){
  const px=BOARD.x+x*BOARD.size,py=BOARD.y+y*BOARD.size,cell=key(x,y);
  round(ctx,px+2,py+2,66,66,10,(x+y)%2?'#eaf7e9':'#f8f9e9');
  if(state.walls.has(cell)){
    round(ctx,px+5,py+5,60,60,11,'#8984b3');
    round(ctx,px+10,py+9,50,42,9,'#aaa5cb');star(ctx,px+46,py+20,4,'#f8e0fb');
  }
  if(state.clouds.has(cell)){
    cloud(ctx,px+35,py+31,'#f2abc3',.82);fill(ctx,px+24,py+27,3,3,'#ffffffa6');
  }
  if(state.exit===cell){
    const open=ready(state);
    round(ctx,px+9,py+8,52,54,26,open?'#ffaec6':'#bab3d1');
    round(ctx,px+15,py+14,40,47,20,open?'#ffe79f':'#eae5f3');
    star(ctx,px+35,py+34,11,open?'#eb976d':'#aaa1c8');
  }
  if(state.stars.has(cell)){
    const bob=reduced?0:Math.sin(time/350+x)*3;
    fill(ctx,px+35,py+35,24,22,'#ffe5a770');star(ctx,px+35,py+33+bob,18,'#ffcc68');
    star(ctx,px+35,py+33+bob,8,'#fff7c9');
  }
  const item=state.items.get(cell);
  if(item){
    const bob=reduced?0:Math.sin(time/320+x+y)*3;
    fill(ctx,px+35,py+37,22,8,'#6e79804d');fill(ctx,px+35,py+31+bob,23,23,'#ffffffeb');
    ctx.strokeStyle='#7ccdcc';ctx.lineWidth=3;ctx.beginPath();ctx.arc(px+35,py+31+bob,22,0,Math.PI*2);ctx.stroke();
    ctx.fillStyle='#7b5c95';ctx.font='900 28px system-ui';ctx.textAlign='center';
    ctx.fillText(ITEM_INFO[item].icon,px+35,py+40+bob);
  }
}

function drawEnemy(ctx,enemy,from,time,reduced){
  const duration=210,progress=reduced?1:Math.min(1,(time-from.started)/duration);
  const x=lerp(from.x,enemy.x,progress),y=lerp(from.y,enemy.y,progress);
  const [cx,cy]=tileCenter(x,y),bob=reduced?0:Math.sin(time/240+enemy.id)*3;
  fill(ctx,cx,cy+23,23,7,'#4a5f6a55');
  cloud(ctx,cx,cy-4+bob,enemy.kind==='hunter'?'#8d88b7':'#a7a8c4',.68);
  face(ctx,cx,cy-3+bob,enemy.kind==='hunter');
  if(enemy.kind==='hunter'){
    ctx.strokeStyle='#ffe2a2';ctx.lineWidth=3;ctx.beginPath();
    ctx.moveTo(cx-19,cy-18+bob);ctx.lineTo(cx-25,cy-25+bob);
    ctx.moveTo(cx+19,cy-18+bob);ctx.lineTo(cx+25,cy-25+bob);ctx.stroke();
  }
}

function drawBoss(ctx,state,time,reduced){
  if(!state.boss)return;
  const cells=[...state.boss.cells].map(point),minX=Math.min(...cells.map(([x])=>x)),minY=Math.min(...cells.map(([,y])=>y));
  const cx=BOARD.x+(minX+1)*BOARD.size,cy=BOARD.y+(minY+1)*BOARD.size;
  if(!state.boss.hearts){
    cloud(ctx,cx,cy+8,'#d6b9df',1.4);star(ctx,cx,cy-33,18,'#ffd875');face(ctx,cx,cy+11);return;
  }
  const bob=reduced?0:Math.sin(time/460)*5;
  fill(ctx,cx,cy+54,60,12,'#4c4c7355');
  fill(ctx,cx,cy+bob,76,67,state.boss.mode==='open'?'#ffe7c5':'#aba2d7');
  cloud(ctx,cx-38,cy+24+bob,'#9289c1',1.2);
  cloud(ctx,cx+38,cy+24+bob,'#9289c1',1.2);
  fill(ctx,cx,cy-14+bob,55,47,'#b5a9d9');
  star(ctx,cx,cy-68+bob,24,'#ffcf82');
  face(ctx,cx,cy-5+bob,state.boss.hearts<=2);
  if(state.boss.mode==='open'){
    fill(ctx,cx,cy+33+bob,25,22,'#fff4bc');star(ctx,cx,cy+33+bob,13,'#ffad90');
  }else{
    ctx.strokeStyle=state.boss.mode==='warning'?'#fbc3e0':'#edf0ff';ctx.lineWidth=5;
    ctx.beginPath();ctx.arc(cx,cy+bob,76,0,Math.PI*2);ctx.stroke();
  }
}

function drawPlayer(ctx,state,from,time,reduced){
  const progress=reduced?1:Math.min(1,(time-from.started)/150);
  const x=lerp(from.x,state.player.x,progress),y=lerp(from.y,state.player.y,progress);
  const [cx,cy]=tileCenter(x,y),hop=reduced?0:Math.sin(progress*Math.PI)*9;
  const idle=reduced?0:Math.sin(time/330)*2;
  ctx.save();ctx.translate(cx,cy-hop+idle);
  if(state.invulnerable&&!reduced&&Math.floor(time/100)%2===0)ctx.globalAlpha=.45;
  fill(ctx,0,25+hop,23,7,'#667f8055');
  ctx.rotate(reduced?0:Math.sin(progress*Math.PI)*from.direction*.13);
  star(ctx,0,-5,31,'#ffe07b');fill(ctx,0,2,24,22,'#ffe07b');face(ctx,0,-1);
  round(ctx,-14,17,27,7,4,'#81d4c7');
  if(state.stats.wings){fill(ctx,-29,10,12,7,'#fffaf0');fill(ctx,29,10,12,7,'#fffaf0');}
  if(state.stats.skates){round(ctx,-17,24,12,4,2,'#ef9bc1');round(ctx,5,24,12,4,2,'#ef9bc1');}
  ctx.restore();
}

export function drawScene(ctx,state,animation){
  const {time,reduced,playerFrom,enemyFrom,light,lightUntil,attack,attackUntil}=animation;
  const gradient=ctx.createLinearGradient(0,0,990,720);
  gradient.addColorStop(0,LEVELS[state.index].sky);gradient.addColorStop(1,'#fff0df');
  ctx.fillStyle=gradient;ctx.fillRect(0,0,990,720);
  for(let i=0;i<17;i++){const x=35+(i*127)%920,y=25+(i*93)%630;star(ctx,x,y,3,i%2?'#fff5d0':'#ffffffc4');}
  cloud(ctx,59,69,'#ffffff8d',.9);cloud(ctx,930,610,'#ffffff90',1.1);
  round(ctx,BOARD.x-15,BOARD.y-15,800,520,27,'#ffffffd5');
  round(ctx,BOARD.x-6,BOARD.y-6,782,502,20,'#73aeb8');
  for(let y=0;y<state.height;y++)for(let x=0;x<state.width;x++)drawTile(ctx,state,x,y,time,reduced);
  if(state.boss?.mode==='warning')for(const cell of bossHazardCells(state)){
    const [x,y]=point(cell),[cx,cy]=tileCenter(x,y);
    round(ctx,cx-31,cy-31,62,62,10,'#d28ac05c');
  }
  if(time<attackUntil)for(const cell of attack){
    const [x,y]=point(cell),[cx,cy]=tileCenter(x,y);
    round(ctx,cx-31,cy-31,62,62,10,'#e391c9aa');star(ctx,cx,cy,18,'#fff6db');
  }
  for(const bubble of state.bubbles){
    const [cx,cy]=tileCenter(bubble.x,bubble.y),pulse=reduced?0:Math.sin(time/160)*2;
    fill(ctx,cx,cy,23+pulse,23+pulse,'#b7eff3ac');
    ctx.strokeStyle='#fff';ctx.lineWidth=4;ctx.beginPath();ctx.arc(cx,cy,23+pulse,0,Math.PI*2);ctx.stroke();
    star(ctx,cx,cy,12,'#fff1a7');
  }
  state.enemies.forEach((enemy)=>drawEnemy(ctx,enemy,enemyFrom.get(enemy.id)??{...enemy,started:time},time,reduced));
  drawBoss(ctx,state,time,reduced);
  if(time<lightUntil)for(const cell of light){
    const [x,y]=point(cell),[cx,cy]=tileCenter(x,y);
    round(ctx,cx-31,cy-31,62,62,13,'#fff0a9c9');star(ctx,cx,cy,23,'#ffffff');
  }
  drawPlayer(ctx,state,playerFrom,time,reduced);
  ctx.fillStyle='#4c6275';ctx.font='800 15px system-ui';ctx.textAlign='center';
  ctx.fillText(LEVELS[state.index].name,495,675);
}
