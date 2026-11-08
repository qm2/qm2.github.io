(() => {
 'use strict';
 // Shared lightbox displays an upright/full-size derivative; retain the unchanged JPEG link.
 document.querySelectorAll('a[data-photo]').forEach(a=>a.addEventListener('click',()=>{
  if(document.querySelector('#art-lightbox')?.open) document.querySelector('#original-photo').href=a.dataset.original;
 }));
 const dialog=document.querySelector('#art-lightbox');
 // When arrows change the active image, resolve its original from the shared viewer's image URL.
 if(dialog){const large=dialog.querySelector('#large-photo');new MutationObserver(()=>{
  const link=[...document.querySelectorAll('a[data-photo]')].find(a=>a.href===large.src);
  if(link)dialog.querySelector('#original-photo').href=link.dataset.original;
 }).observe(large,{attributes:true,attributeFilter:['src']});}
 document.querySelectorAll('[data-rs-gallery]').forEach(g=>{
  const slides=[...g.querySelectorAll('.rs-slide')],controls=g.querySelector('.rs-gallery-controls');let index=0,all=false;
  const update=()=>{slides.forEach((s,i)=>s.hidden=!all&&i!==index);g.querySelector('[data-count]').textContent=all?`全部 ${slides.length} 张`:`${index+1} / ${slides.length}`;g.querySelector('[data-prev]').disabled=all||!index;g.querySelector('[data-next]').disabled=all||index===slides.length-1;const b=g.querySelector('[data-all]');b.setAttribute('aria-pressed',String(all));b.textContent=all?'收起图组':'展开全部';};
  g.querySelector('[data-prev]').onclick=()=>{index--;update();};g.querySelector('[data-next]').onclick=()=>{index++;update();};g.querySelector('[data-all]').onclick=()=>{all=!all;update();};
  controls.hidden=slides.length<2;update();
 });
 const search=document.querySelector('#rs-search');
 if(search){
  const museum=document.querySelector('#rs-museum'),theme=document.querySelector('#rs-theme'),cards=[...document.querySelectorAll('[data-record]')];
  const restore=()=>{const p=new URLSearchParams(location.search);search.value=p.get('q')||'';museum.value=p.get('museum')||'all';theme.value=p.get('theme')||'all';if(!museum.value)museum.value='all';if(!theme.value)theme.value='all';update(false);};
  const update=(push=true)=>{let count=0;const terms=search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
   cards.forEach(c=>{c.hidden=!(terms.every(t=>c.dataset.search.toLowerCase().includes(t))&&(museum.value==='all'||c.dataset.museum===museum.value)&&(theme.value==='all'||c.dataset.theme===theme.value));if(!c.hidden)count++;document.querySelector(`[data-time-record="${c.dataset.record}"]`).hidden=c.hidden;});
   document.querySelector('#rs-results').textContent=`${count} / ${cards.length} 条作品记录`;document.querySelector('#rs-empty').hidden=!!count;
   document.querySelectorAll('[data-map-museum]').forEach(a=>a.setAttribute('aria-current',String(a.dataset.mapMuseum===museum.value)));
   if(push){const u=new URL(location.href);for(const k of ['q','museum','theme'])u.searchParams.delete(k);if(search.value)u.searchParams.set('q',search.value);if(museum.value!=='all')u.searchParams.set('museum',museum.value);if(theme.value!=='all')u.searchParams.set('theme',theme.value);history.pushState(null,'',u);}
  };
  search.addEventListener('input',()=>update());museum.addEventListener('change',()=>update());theme.addEventListener('change',()=>update());
  document.querySelector('#rs-clear').onclick=()=>{search.value='';museum.value=theme.value='all';update();};
  document.querySelectorAll('[data-map-museum]').forEach(a=>a.addEventListener('click',event=>{if(event.metaKey||event.ctrlKey||event.shiftKey)return;event.preventDefault();museum.value=a.dataset.mapMuseum;update();document.querySelector('.rs-atlas-controls').scrollIntoView({block:'start'});}));
  window.addEventListener('popstate',restore);restore();
  const reveal=()=>{const c=cards.find(c=>'#'+c.id===location.hash);if(c?.hidden){search.value='';museum.value=theme.value='all';update();}if(c)c.scrollIntoView({block:'start'});};window.addEventListener('hashchange',reveal);if(location.hash)reveal();
 }
 const revealDetails=()=>{const id=decodeURIComponent(location.hash.slice(1));if(!id)return;const target=document.getElementById(id);if(!target)return;let node=target,expanded=false;while(node){if(node.tagName==='DETAILS'&&!node.open){node.open=true;expanded=true;}node=node.parentElement;}if(expanded)requestAnimationFrame(()=>target.scrollIntoView({block:'start',behavior:'instant'}));};
 revealDetails();window.addEventListener('hashchange',revealDetails);
})();
