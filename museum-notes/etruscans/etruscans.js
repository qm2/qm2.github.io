(() => {
 'use strict';
 const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 // Regional selector is usable as ordinary links without JavaScript.
 const selectors=$$('[data-map-place]'),previews=$$('[data-place-preview]');
 let activePlace='';
 function selectPlace(id){activePlace=id;selectors.forEach(el=>{el.setAttribute(el.tagName.toLowerCase()==='button'?'aria-expanded':'aria-current',String(el.dataset.mapPlace===id));});previews.forEach(p=>p.hidden=p.dataset.placePreview!==id);}
 $('[data-map-zoom]')?.addEventListener('click',e=>{const on=$('.et-map-scroll').classList.toggle('is-zoomed');e.currentTarget.setAttribute('aria-pressed',String(on));e.currentTarget.textContent=on?'恢复地图大小':'放大地图';});
 $('[data-map-more]')?.addEventListener('click',e=>{const on=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(on));e.currentTarget.textContent=on?'收起更多地点':'更多地点';$$('[data-tier="2"]').forEach(n=>{n.toggleAttribute('hidden',!on);});});
 const cards=$$('[data-record]'),search=$('#et-search'),filters=$$('[data-filter]'),sort=$('#et-sort');
 function update(push=false){
  if(!search)return;
  const terms=search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean),values=Object.fromEntries(filters.map(f=>[f.dataset.filter,f.value]));
  let start=values.start===''?-Infinity:Number(values.start),end=values.end===''?Infinity:Number(values.end);const valid=start<=end;
  let count=0;
  cards.forEach(c=>{const d=c.dataset,show=valid&&terms.every(t=>(d.search.toLocaleLowerCase().includes(t)||d.search.toLocaleLowerCase().replace(/[\s.,–—-]/g,'').includes(t.replace(/[\s.,–—-]/g,''))))&&filters.every(f=>['start','end'].includes(f.dataset.filter)||f.value==='all'||(f.dataset.filter==='function'?d.function.split(' ').includes(f.value):d[f.dataset.filter]===f.value))&&Number(d.end)>=start&&Number(d.start)<=end;c.hidden=!show;const row=$(`[data-time-record="${d.record}"]`);if(row)row.hidden=!show;if(show)count++;});
  $('#et-results').textContent=valid?`${count} / ${cards.length} 条记录`:'起始年代应早于结束年代。';$('#et-empty').hidden=!!count||!valid;
  const grid=$('.et-record-grid');[...cards].sort((a,b)=>sort.value==='date'?Number(a.dataset.start)-Number(b.dataset.start):sort.value==='collection'?a.dataset.collection.localeCompare(b.dataset.collection):a.dataset.record.localeCompare(b.dataset.record)).forEach(c=>grid.append(c));
  if(values.place!=='all')selectPlace(values.place);else selectPlace('');
  if(push){const u=new URL(location.href);u.search='';if(search.value)u.searchParams.set('q',search.value);filters.forEach(f=>{if(f.value&&f.value!=='all')u.searchParams.set(f.dataset.filter,f.value);});if(sort.value!=='chapter')u.searchParams.set('sort',sort.value);history.pushState(null,'',u);}
 }
 function restore(){if(!search)return;const q=new URLSearchParams(location.search);search.value=q.get('q')||'';filters.forEach(f=>{f.value=q.get(f.dataset.filter)||(f.tagName==='SELECT'?'all':'');if(f.tagName==='SELECT'&&!f.value)f.value='all';});sort.value=q.get('sort')||'chapter';if(!sort.value)sort.value='chapter';update();}
 if(search){let timer;search.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>update(true),180);});filters.forEach(f=>f.addEventListener('change',()=>update(true)));sort.addEventListener('change',()=>update(true));$('#et-reset').onclick=()=>{search.value='';filters.forEach(f=>f.value=f.tagName==='SELECT'?'all':'');sort.value='chapter';update(true);};window.addEventListener('popstate',restore);restore();}
 selectors.forEach(el=>el.addEventListener('click',e=>{if(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;e.preventDefault();const id=el.dataset.mapPlace;if(search){$('[data-filter="place"]').value=id;update(true);}else selectPlace(activePlace===id?'':id);}));
 const lookup=$('#et-lookup');lookup?.addEventListener('input',()=>{const terms=lookup.value.trim().toLowerCase().split(/\s+/).filter(Boolean);$$('[data-lookup]').forEach(d=>{d.hidden=!terms.every(t=>d.dataset.lookup.toLowerCase().includes(t));});});
 const photoKind=$('#et-photo-kind');function filterPhotos(push=false){if(!photoKind)return;let n=0;$$('[data-photo-kind]').forEach(d=>{d.hidden=photoKind.value!=='all'&&photoKind.value!==d.dataset.photoKind;if(!d.hidden)n++;});$('#et-photo-count').textContent=`${n} / ${$$('[data-photo-kind]').length} 张照片`;if(push){const u=new URL(location.href);u.searchParams.delete('kind');if(photoKind.value!=='all')u.searchParams.set('kind',photoKind.value);history.pushState(null,'',u);}}
 if(photoKind){const init=()=>{photoKind.value=new URLSearchParams(location.search).get('kind')||'all';if(!photoKind.value)photoKind.value='all';filterPhotos();};init();photoKind.onchange=()=>filterPhotos(true);window.addEventListener('popstate',init);}
 function reveal(){const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(!target)return;
  if(target.matches('[data-record]')&&target.hidden){search.value='';filters.forEach(f=>f.value=f.tagName==='SELECT'?'all':'');update(false);}
  if(target.matches('[data-photo-kind]')&&target.hidden){photoKind.value='all';filterPhotos();}
  let n=target;while(n){if(n.tagName==='DETAILS')n.open=true;if(n.hidden)n.hidden=false;n=n.parentElement;}
  requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
 }
 window.addEventListener('hashchange',reveal);if(location.hash)reveal();
})();
