(() => {
 'use strict';
 document.querySelectorAll('.iv-gallery').forEach(gallery => {
  const slides=[...gallery.querySelectorAll('.iv-slides>.iv-figure')];
  const controls=gallery.querySelector('.iv-gallery-controls'),tabs=gallery.querySelector('.iv-gallery-tabs');
  let index=0,all=false;
  const update=()=>{
   gallery.classList.toggle('is-single',!all);
   slides.forEach((s,i)=>s.hidden=!all&&i!==index);
   [...tabs.children].forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
   gallery.querySelector('.iv-gallery-count').textContent=`${index+1} / ${slides.length}`;
   gallery.querySelector('[data-prev]').disabled=all||index===0;
   gallery.querySelector('[data-next]').disabled=all||index===slides.length-1;
   const b=gallery.querySelector('[data-all]');b.setAttribute('aria-expanded',String(all));b.textContent=all?'收起为单张':'展开全部照片';
  };
  slides.forEach((slide,i)=>{
   const b=document.createElement('button');b.type='button';b.textContent=slide.dataset.view;b.setAttribute('aria-controls',slide.id);
   b.addEventListener('click',()=>{index=i;all=false;update();});tabs.append(b);
  });
  gallery.querySelector('[data-prev]').addEventListener('click',()=>{index=Math.max(0,index-1);update();});
  gallery.querySelector('[data-next]').addEventListener('click',()=>{index=Math.min(slides.length-1,index+1);update();});
  gallery.querySelector('[data-all]').addEventListener('click',()=>{all=!all;update();});
  gallery.revealPhoto=id=>{const i=slides.findIndex(s=>s.id===id);if(i>=0){index=i;all=false;update();}};
  if(slides.length>1){controls.hidden=false;tabs.hidden=false;}update();
 });
 const reveal=()=>{
  let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
  const target=document.getElementById(id);if(!target)return;
  target.closest('.iv-gallery')?.revealPhoto?.(id);
  for(let p=target;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;
  requestAnimationFrame(()=>target.scrollIntoView({block:'start',behavior:'instant'}));
 };
 window.addEventListener('hashchange',reveal);
 const form=document.querySelector('.iv-filters');
 if(form){
  const search=document.getElementById('iv-search'),region=document.getElementById('iv-region'),text=document.getElementById('iv-text'),rows=[...document.querySelectorAll('.iv-catalogue li')];
  const update=()=>{
   const terms=search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);let count=0;
   rows.forEach(row=>{row.hidden=!terms.every(t=>row.dataset.search.toLocaleLowerCase().includes(t))||(region.value&&region.value!==row.dataset.region)||(text.value&&text.value!==row.dataset.text);if(!row.hidden)count++;});
   document.getElementById('iv-count').textContent=`${count} / ${rows.length}件`;document.querySelector('.iv-empty').hidden=count!==0;
  };
  form.hidden=false;form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('input',update);form.addEventListener('change',update);form.addEventListener('reset',()=>setTimeout(update,0));update();
 }
 if(location.hash)reveal();
})();
