const palettes={
  request:['NAVEGADOR','REQUISIÇÃO','SERVIDOR','RESPOSTA'],
  semantic:['HEADER','NAV','MAIN','FOOTER'],
  layout:['CONTEÚDO','FLEX / GRID','TELA MENOR','REORGANIZAR'],
  dom:['HTML','CSS','DOM','JAVASCRIPT'],
  api:['INTERFACE','HTTP / JSON','API','DADOS'],
  database:['MODELO','CONSULTA','ÍNDICE','RESULTADO'],
  security:['IDENTIDADE','SESSÃO','PERMISSÃO','RECURSO'],
  deploy:['CÓDIGO','TESTES','BUILD','PUBLICAR'],
};
function round(ctx,x,y,w,h,r=15){ctx.beginPath();ctx.roundRect(x,y,w,h,r);}
function label(ctx,text,x,y,color,size=16){ctx.fillStyle=color;ctx.font=`800 ${size}px system-ui`;ctx.textAlign='center';ctx.fillText(text,x,y);}

function cover(canvas){
  const ctx=canvas.getContext('2d'),w=canvas.width,h=canvas.height;
  const sky=ctx.createLinearGradient(0,0,w,h);sky.addColorStop(0,'#101a35');sky.addColorStop(.6,'#172c44');sky.addColorStop(1,'#322450');
  ctx.fillStyle=sky;ctx.fillRect(0,0,w,h);
  ctx.strokeStyle='#86e5e04d';ctx.lineWidth=1;
  for(let x=20;x<w;x+=40){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}
  for(let y=20;y<h;y+=40){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
  ctx.fillStyle='#90f5de';ctx.fillRect(45,58,105,5);
  ctx.fillStyle='#eefbf5';ctx.textAlign='left';ctx.font='800 18px system-ui';ctx.fillText('VOIDWIELDER · LIVROS',45,94);
  ctx.fillStyle='#f8f5ec';ctx.font='900 49px system-ui';ctx.fillText('DESENVOLVIMENTO',44,180);
  ctx.fillText('WEB',44,238);
  ctx.fillStyle='#bcece9';ctx.font='600 23px system-ui';ctx.fillText('do primeiro arquivo à produção',46,278);
  ctx.save();ctx.shadowColor='#64e5d8';ctx.shadowBlur=40;
  round(ctx,65,340,410,255,23);ctx.fillStyle='#e8fdf8';ctx.fill();ctx.restore();
  round(ctx,65,340,410,255,23);ctx.strokeStyle='#76c6d0';ctx.lineWidth=4;ctx.stroke();
  round(ctx,65,340,410,48,22);ctx.fillStyle='#9bdccf';ctx.fill();
  ['#f47796','#ffd684','#70b4ce'].forEach((color,index)=>{ctx.beginPath();ctx.fillStyle=color;ctx.arc(92+25*index,364,7,0,Math.PI*2);ctx.fill();});
  ctx.fillStyle='#21354e';ctx.font='700 16px ui-monospace,monospace';ctx.fillText('<main>',94,428);
  ctx.fillStyle='#4e728b';ctx.fillText('  <h1>Olá, web!</h1>',94,462);
  ctx.fillStyle='#6e658f';ctx.fillText('  display: grid;',94,496);
  ctx.fillStyle='#a1668b';ctx.fillText('  fetch("/api/tarefas")',94,530);
  ctx.fillStyle='#21354e';ctx.fillText('</main>',94,564);
  ctx.fillStyle='#ffdc91';ctx.font='800 19px system-ui';ctx.fillText('HTML  →  CSS  →  JS  →  API',45,652);
  ctx.fillStyle='#d1d9e5';ctx.font='600 15px system-ui';ctx.fillText('Iniciante · Intermediário · Avançado',45,681);
}

function diagram(canvas,name){
  const ctx=canvas.getContext('2d'),labels=palettes[name]||palettes.request;
  const w=canvas.width,h=canvas.height;
  const background=ctx.createLinearGradient(0,0,w,h);background.addColorStop(0,'#e5f5f1');background.addColorStop(1,'#ecedfa');
  round(ctx,0,0,w,h,20);ctx.fillStyle=background;ctx.fill();
  ctx.setLineDash([7,7]);ctx.strokeStyle='#79adb2';ctx.lineWidth=3;
  ctx.beginPath();ctx.moveTo(82,90);ctx.lineTo(w-82,90);ctx.stroke();ctx.setLineDash([]);
  labels.forEach((item,index)=>{
    const x=95+index*163,y=90;
    ctx.save();ctx.shadowColor='#5f719455';ctx.shadowBlur=13;
    round(ctx,x-71,y-40,142,80,15);ctx.fillStyle=index%2?'#f6e6ec':'#ffffff';ctx.fill();ctx.restore();
    ctx.strokeStyle=index%2?'#d2a2b8':'#8dc7c0';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.arc(x,y-51,11,0,Math.PI*2);ctx.fillStyle=index%2?'#d38bac':'#4ca99e';ctx.fill();
    label(ctx,item,x,y+5,'#30425b',item.length>13?12:14);
    if(index<3)label(ctx,'→',x+81,y+6,'#629da7',24);
  });
}

export function drawWebArt(canvas){
  if(!canvas?.getContext)return;
  canvas.dataset.webArt==='cover'?cover(canvas):diagram(canvas,canvas.dataset.webArt);
}
document.querySelectorAll('[data-web-art]').forEach(drawWebArt);
