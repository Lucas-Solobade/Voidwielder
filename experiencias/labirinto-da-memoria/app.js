const HELP={fifo:"FIFO remove a página que está há mais tempo na memória, sem considerar quando ela foi usada pela última vez.",lru:"LRU remove a página usada há mais tempo. Cada acesso recente protege temporariamente uma página.",optimal:"O algoritmo Ótimo olha o futuro e remove a página cujo próximo uso está mais distante — ou que nunca será usada novamente."};
const LABELS={fifo:"FIFO",lru:"LRU",optimal:"ÓTIMO"};

export function parseReferences(value){
  const parts=String(value).split(/[\s,;]+/).filter(Boolean).map(Number);
  if(!parts.length||parts.some((item)=>!Number.isInteger(item)||item<0||item>99)) throw new Error("Use páginas inteiras entre 0 e 99.");
  return parts.slice(0,24);
}

function victimFIFO(loadedAt){let index=0;for(let i=1;i<loadedAt.length;i+=1)if(loadedAt[i]<loadedAt[index])index=i;return index}
function victimLRU(lastUsed){let index=0;for(let i=1;i<lastUsed.length;i+=1)if(lastUsed[i]<lastUsed[index])index=i;return index}
function victimOptimal(frames,references,position){let victim=0;let distance=-1;frames.forEach((page,index)=>{const next=references.indexOf(page,position+1);const score=next===-1?Infinity:next;if(score>distance){distance=score;victim=index}});return victim}

export function simulate(references,frameCount=3,algorithm="fifo"){
  const count=Math.max(2,Math.min(6,Number(frameCount)||3));
  const frames=Array(count).fill(null),loadedAt=Array(count).fill(-1),lastUsed=Array(count).fill(-1);
  let hits=0,faults=0;
  return references.map((page,position)=>{
    const existing=frames.indexOf(page);let changed=-1,evicted=null,hit=existing!==-1;
    if(hit){hits+=1;lastUsed[existing]=position;changed=existing}
    else{
      faults+=1;let target=frames.indexOf(null);
      if(target===-1){target=algorithm==="lru"?victimLRU(lastUsed):algorithm==="optimal"?victimOptimal(frames,references,position):victimFIFO(loadedAt);evicted=frames[target]}
      frames[target]=page;loadedAt[target]=position;lastUsed[target]=position;changed=target;
    }
    return{page,frames:[...frames],hit,fault:!hit,changed,evicted,hits,faults};
  });
}

const root=typeof document==="undefined"?null:document.querySelector("#simulador");
if(root){
  const $=(selector)=>document.querySelector(selector);
  const state={algorithm:"fifo",references:[],steps:[],index:0,timer:null,error:""};

  function build(reset=true){
    try{state.references=parseReferences($("#references").value);state.error=""}catch(error){state.error=error.message;state.references=[0]}
    const count=Math.max(2,Math.min(6,Number($("#frameCount").value)||3));$("#frameCount").value=count;
    state.steps=simulate(state.references,count,state.algorithm);if(reset)state.index=0;state.index=Math.min(state.index,state.steps.length-1);stop();render();
  }
  function render(){
    const step=state.steps[state.index],previous=state.index?state.steps[state.index-1].frames:Array(step.frames.length).fill(null);
    $("#algorithmBadge").textContent=LABELS[state.algorithm];$("#algorithmHelp").textContent=HELP[state.algorithm];$("#currentPage").textContent=step.page;
    $("#eventLabel").textContent=state.error?"ERRO":step.hit?"ACERTO":"FALTA";$("#eventLabel").className=step.hit?"hit":"";
    $("#eventDetail").textContent=state.error|| (step.hit?"A página já estava carregada.":step.evicted===null?"Havia um quadro livre.":`Página ${step.evicted} removida.`);
    $("#hits").textContent=step.hits;$("#faults").textContent=step.faults;$("#faultRate").textContent=`${Math.round(step.faults/(state.index+1)*100)}%`;
    $("#stepNow").textContent=state.index+1;$("#stepTotal").textContent=state.steps.length;$("#previous").disabled=state.index===0;$("#next").disabled=state.index===state.steps.length-1;
    $("#memoryFrames").innerHTML=step.frames.map((page,index)=>`<div class="memory-frame ${page===null?"empty":""} ${index===step.changed?(step.hit?"hit":"changed"):""}"><span>QUADRO ${index+1}</span><strong>${page===null?"—":page}</strong><small>${index===step.changed?(step.hit?"acessado":previous[index]===null?"carregado":`substituiu ${previous[index]}`):"mantido"}</small></div>`).join("");
    $("#historyGrid").innerHTML=state.steps.map((item,column)=>`<div class="history-column ${item.hit?"hit":"fault"} ${column===state.index?"current":column>state.index?"future":""}"><span class="history-reference">${item.page}</span>${item.frames.map((page,row)=>`<span class="history-cell ${row===item.changed&&!item.hit?"changed":""}">${page===null?"—":page}</span>`).join("")}<span class="history-status">${item.hit?"HIT":"FALTA"}</span></div>`).join("");
    $("#historyGrid").children[state.index]?.scrollIntoView({behavior:"smooth",block:"nearest",inline:"center"});
  }
  function stop(){clearInterval(state.timer);state.timer=null;$("#play").innerHTML="▶ <span>Reproduzir</span>";$("#play").setAttribute("aria-label","Reproduzir")}
  function play(){if(state.timer){stop();return}if(state.index===state.steps.length-1)state.index=0;$("#play").innerHTML="Ⅱ <span>Pausar</span>";$("#play").setAttribute("aria-label","Pausar");state.timer=setInterval(()=>{if(state.index>=state.steps.length-1){stop();return}state.index+=1;render()},850);render()}
  $("#references").addEventListener("change",()=>build());$("#frameCount").addEventListener("change",()=>build());
  document.querySelectorAll('[name="algorithm"]').forEach((input)=>input.addEventListener("change",()=>{state.algorithm=input.value;build()}));
  $("#previous").addEventListener("click",()=>{stop();state.index=Math.max(0,state.index-1);render()});$("#next").addEventListener("click",()=>{stop();state.index=Math.min(state.steps.length-1,state.index+1);render()});$("#play").addEventListener("click",play);
  build();
}
