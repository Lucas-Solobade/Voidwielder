import {drawWebArt} from './art.mjs';

const base=document.documentElement.dataset.siteBase||'';
const bookPath=`${base}/livros/desenvolvimento-web-do-zero-ao-avancado/`;
const pagePath=`${bookPath}ler/`;
const progressKey='voidwielder-web-page';
const resume=document.querySelector('[data-web-resume]');
if(resume){
  try{
    const saved=Number(localStorage.getItem(progressKey));
    if(saved>1){resume.hidden=false;resume.href=`${pagePath}${saved}/`;resume.textContent=`Retomar na página ${saved} →`;}
  }catch{/* Reading does not require local storage. */}
}

const root=document.querySelector('[data-web-reader]');
if(root){
  const total=Number(root.dataset.total),spread=root.querySelector('[data-web-spread]');
  const left=root.querySelector('[data-web-content="left"]'),right=root.querySelector('[data-web-content="right"]');
  const leftSheet=root.querySelector('[data-web-left]'),rightSheet=root.querySelector('[data-web-right]');
  const prev=root.querySelector('[data-web-prev]'),next=root.querySelector('[data-web-next]');
  const jump=root.querySelector('[data-web-jump]'),select=root.querySelector('[data-web-section-select]');
  const part=root.querySelector('[data-web-part]'),chapter=root.querySelector('[data-web-chapter]');
  const progress=root.querySelector('[data-web-progress]');
  const mobile=matchMedia('(max-width:780px)'),reduced=matchMedia('(prefers-reduced-motion:reduce)');
  const sectionStarts=[...select.options].map((option)=>Number(option.value));
  let current=Number(root.dataset.page),pages=null,turning=false,touchX=null,queued=null;
  const clamp=(number)=>Math.max(1,Math.min(total,number));
  const step=()=>mobile.matches?1:2;

  function fill(container,page){
    container.replaceChildren();
    if(!page)return;
    const kicker=document.createElement('span');kicker.className='web-page-kicker';
    kicker.textContent=`${page.part_title.toLocaleUpperCase('pt-BR')}${page.chapter_number?` · CAPÍTULO ${String(page.chapter_number).padStart(2,'0')}`:''}`;
    const heading=document.createElement('h1');heading.textContent=page.section_title;
    container.append(kicker,heading);
    if(page.diagram){
      const canvas=document.createElement('canvas');canvas.width=680;canvas.height=185;
      canvas.className='web-diagram';canvas.dataset.webArt=page.diagram;
      canvas.setAttribute('role','img');canvas.setAttribute('aria-label',`Diagrama do capítulo ${page.chapter_number}; os conceitos são explicados no texto`);
      container.append(canvas);drawWebArt(canvas);
    }
    const body=document.createElement('div');body.className='web-page-body';body.innerHTML=page.body_html;
    const number=document.createElement('span');number.className='web-page-number';number.textContent=page.number;
    container.append(body,number);
  }
  function render(number){
    current=clamp(number);root.dataset.page=current;
    const page=pages[current-1];fill(left,page);fill(right,pages[current]);
    leftSheet.setAttribute('aria-label',`Página ${current}`);
    rightSheet.setAttribute('aria-label',current<total?`Página ${current+1}`:'');
    rightSheet.hidden=current===total;
    part.textContent=`${page.part_title}${page.chapter_number?` · capítulo ${page.chapter_number}`:''}`;
    chapter.textContent=page.chapter_title;
    select.value=String(sectionStarts.filter((start)=>start<=current).at(-1)||1);
    jump.value=current;
    progress.setAttribute('aria-valuenow',String(current));
    progress.querySelector('span').style.width=`${current/total*100}%`;
    prev.hidden=current===1;prev.href=`${pagePath}${clamp(current-step())}/`;
    next.href=current+step()>total?bookPath:`${pagePath}${current+step()}/`;
    next.textContent=current+step()>total?'Voltar ao sumário →':'Próxima →';
    try{localStorage.setItem(progressKey,String(current));}catch{/* Optional progress. */}
    document.title=`Página ${current} · Desenvolvimento web · Voidwielder`;
  }
  async function turn(target,direction='next'){
    if(!pages||target<1||target>total||target===current)return;
    if(turning){queued={target,direction};return;}
    turning=true;
    if(!reduced.matches){spread.classList.add(`is-turning-${direction}`);await new Promise((resolve)=>setTimeout(resolve,210));}
    render(target);history.pushState({page:target},'',`${pagePath}${target}/`);
    if(!reduced.matches)await new Promise((resolve)=>setTimeout(resolve,230));
    spread.classList.remove('is-turning-next','is-turning-prev');turning=false;
    if(queued){const pending=queued;queued=null;turn(pending.target,pending.direction);}
  }
  fetch(`${base}/static/reader/book/web/pages.json`).then((response)=>{
    if(!response.ok)throw Error('Páginas indisponíveis');return response.json();
  }).then((data)=>{
    if(!Array.isArray(data)||data.length!==total)throw Error('Livro incompleto');
    pages=data;render(current);
    prev.addEventListener('click',(event)=>{event.preventDefault();turn(current-step(),'prev');});
    next.addEventListener('click',(event)=>{if(current+step()>total)return;event.preventDefault();turn(current+step());});
    jump.addEventListener('change',()=>turn(clamp(Number(jump.value)||current),Number(jump.value)<current?'prev':'next'));
    select.addEventListener('change',()=>turn(Number(select.value),Number(select.value)<current?'prev':'next'));
    document.addEventListener('keydown',(event)=>{
      if(event.target.closest('input,select,textarea,button,summary,a,pre'))return;
      if(event.key==='ArrowRight'){event.preventDefault();turn(current+step());}
      if(event.key==='ArrowLeft'){event.preventDefault();turn(current-step(),'prev');}
    });
    spread.addEventListener('touchstart',(event)=>{touchX=event.target.closest('pre')?null:event.changedTouches[0].screenX;},{passive:true});
    spread.addEventListener('touchend',(event)=>{
      if(touchX===null)return;
      const dx=event.changedTouches[0].screenX-touchX;touchX=null;
      if(Math.abs(dx)>55)turn(current+(dx<0?step():-step()),dx<0?'next':'prev');
    },{passive:true});
    window.addEventListener('popstate',()=>{const number=Number(location.pathname.match(/ler\/(\d+)\/$/)?.[1]);if(number)render(number);});
    mobile.addEventListener('change',()=>render(current));
  }).catch(()=>{/* Server-rendered pages and links remain available. */});
}
