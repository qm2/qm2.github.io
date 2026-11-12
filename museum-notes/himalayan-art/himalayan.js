(() => {
 'use strict';
 const $ = q => document.querySelector(q), $$ = q => [...document.querySelectorAll(q)];
 // Stable period links open the relevant native disclosure, including on Back.
 const revealPeriod = () => {
  let id; try { id=decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const period=document.getElementById(id);
  if(period && (period.classList.contains('ha-period') || period.classList.contains('ha-guide-entry') || period.classList.contains('ha-revisit-prompt'))){
   period.open=true;
   requestAnimationFrame(()=>period.scrollIntoView({block:'start'}));
  }
 };
 revealPeriod(); window.addEventListener('hashchange',revealPeriod);
 // Plates remain all visible without JavaScript; one-button return to the full mandala.
 $$('.ha-detail-view').forEach(view => {
  const tabs=view.querySelector('.ha-tabs'), panels=[...view.querySelectorAll('[data-plate-panel]')];
  if(!tabs)return; tabs.hidden=false;
  const show=i=>{panels.forEach((p,j)=>p.hidden=j!==i);tabs.querySelectorAll('button').forEach((b,j)=>b.setAttribute('aria-pressed',String(j===i)));};
  tabs.addEventListener('click',ev=>{const b=ev.target.closest('[data-plate]');if(b)show(Number(b.dataset.plate));}); show(0);
 });
 // Local learning search: shareable queries, native disclosures and Back support.
 const learningInput=$('#learning-query');
 if(learningInput){
  const items=$$('[data-learning-search]'), index=$('#learning-index');
  const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase().trim();
  const records=items.map((item,order)=>({item,order,fields:JSON.parse(item.dataset.learningSearch).map(xs=>xs.map(normalize))}));
  const labels=['名称／异名','辨认特征','正文／比较提及'];
  const apply=()=>{
   const query=normalize(learningInput.value), words=learningInput.value.trim().split(/\s+/).filter(Boolean), terms=words.map(normalize);
   let count=0;
   const ranked=records.map(record=>{
    const hits=terms.map(t=>record.fields.findIndex(xs=>xs.some(x=>x.includes(t))));
    const visible=hits.every(t=>t>=0), reason=record.item.querySelector('.ha-search-reason');
    record.item.hidden=!visible;
    reason.hidden=!query||!visible;
    reason.textContent=visible&&query ? labels.map((label,tier)=>{
     const matched=words.filter((_,i)=>hits[i]===tier);
     return matched.length ? label+'：'+matched.slice(0,2).join('、')+(matched.length>2?'…':'') : '';
    }).filter(Boolean).join('；') : '';
    if(visible)count++;
    // All query terms must match. Prefer names, then identification clues,
    // then mentions in prose/comparisons; ties retain the editorial order.
    return {...record,worst:visible?Math.max(-1,...hits):3,total:hits.reduce((a,b)=>a+b,0),exact:query&&record.fields[0].includes(query)?1:0};
   }).sort((a,b)=>a.worst-b.worst||a.total-b.total||b.exact-a.exact||a.order-b.order);
   $('.ha-search-results').append(...ranked.map(r=>r.item));
   $('#learning-count').textContent=count+' / '+items.length+' 条';
   $('#learning-empty').hidden=count!==0;
   if(query)index.open=true;
  };
  const fromURL=()=>{learningInput.value=new URLSearchParams(location.search).get('q')||'';apply();};
  const save=()=>{const url=new URL(location.href);const q=learningInput.value.trim();if(q)url.searchParams.set('q',q);else url.searchParams.delete('q');if(url.href!==location.href)history.pushState({},'',url);apply();};
  let timer;
  learningInput.addEventListener('input',()=>{clearTimeout(timer);apply();timer=setTimeout(save,300);});
  learningInput.form.addEventListener('submit',ev=>{ev.preventDefault();clearTimeout(timer);save();index.open=true;});
  $('#learning-clear').hidden=false;
  $('#learning-clear').addEventListener('click',()=>{clearTimeout(timer);learningInput.value='';save();learningInput.focus();});
  window.addEventListener('popstate',()=>{clearTimeout(timer);fromURL();});fromURL();
 }
 if(!$('#places'))return;
 const script=document.currentScript || [...document.scripts].find(s=>s.src&&new URL(s.src).pathname.endsWith('/himalayan.js'));
 const dataURL=new URL('data/navigation.json',script.src);
 dataURL.search=new URL(script.src).search;
 fetch(dataURL).then(r=>{if(!r.ok)throw new Error('navigation');return r.json();}).then(start).catch(()=>{
  const p=document.createElement('p');p.className='ha-note';p.textContent='地图筛选暂时无法载入，下方章节与完整目录仍可阅读。';$('#ha-map-status').replaceWith(p);
 });
 function start(data){
  const externalWork=new URLSearchParams(location.search).get('work')||location.hash.slice(1);
  if(data.external_works?.[externalWork]){location.replace(data.external_works[externalWork]);return;}
  const ws=data.works, groups=data.groups, places=data.places, wb=new Map(ws.map(w=>[w.work_id,w]));
  const groupsBy=new Map(groups.map(g=>[g.id,g]));
  const parentGroup=id=>groupsBy.get(id) || groups.find(g=>g.members.includes(id));
  const placeName=id=>{const p=places.find(p=>p.place_id===id);return p?.filter_label || p?.label_zh || id;};
  const regionName=id=>groupsBy.get(id)?.label || places.find(p=>p.place_id===id)?.label_zh || id;
  const names=new Map(data.museums.map(m=>[m.museum_id,m.label_zh]));
  const es=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let state={}, timer;
  const fromURL=()=>{
   const q=new URLSearchParams(location.search);state=Object.fromEntries(q);
   if(!['regions','museums','collections'].includes(state.view))state.view=state.museum?'museums':state.collection?'collections':'regions';
   if(state.work&&!wb.has(state.work))delete state.work;
   if(state.work){const w=wb.get(state.work);if(groups.some(g=>g.extension&&g.members.some(p=>w.region_ids.includes(p))))state.ext='1';}
   if(parentGroup(state.region)?.extension)state.ext='1';
  };
  const related=(w,id)=>!id || (groupsBy.get(id)?.members || [id]).some(p=>w.region_ids.includes(p));
  const matches=(w,ignoreRegion=false)=>{
   if(state.work && w.work_id!==state.work)return false;
   if(!ignoreRegion && !related(w,state.region))return false;
   if(state.museum && (w.display_museum_id || 'unknown')!==state.museum)return false;
   if(state.collection && (w.collection_museum_id || 'unknown')!==state.collection)return false;
   if(state.material && state.material!==w.material)return false;
   if(state.theme && state.theme!==w.theme)return false;
   if(state.q && !state.q.toLocaleLowerCase().trim().split(/\s+/).every(t=>w.search.toLocaleLowerCase().includes(t)))return false;
   const unknown=w.date_start===null||w.date_end===null;
   if(state.period==='unknown')return unknown;
   if(unknown)return state.unknown!=='0';
   if(state.period){const [a,b]=state.period.split(',').map(Number);if(w.date_end<a||w.date_start>b)return false;}
   return true;
  };
  const writeURL=()=>{const q=new URLSearchParams();Object.entries(state).forEach(([k,v])=>{if(v&&!(k==='view'&&v==='regions'))q.set(k,v);});const dest=location.pathname+(q.size?'?'+q:'')+location.hash;if(dest!==location.pathname+location.search+location.hash)history.pushState({},'',dest);};
  const change=patch=>{state={...state,...patch};if(patch.region&&parentGroup(patch.region)?.extension)state.ext='1';writeURL();render();};
  const mini=w=>`<a class="ha-mini" href="${es(w.work_id)}/"><img src="${es(w.thumbnail_path || `images/${w.primary_photo}-400.webp`)}" width="70" height="100" loading="lazy" alt="${es(w.title_zh)}"><span>${es(w.title_zh)}<small>${es(w.date_label)}</small></span></a>`;
  function render(){
   const selected=ws.filter(w=>matches(w)), ids=new Set(selected.map(w=>w.work_id));
   for(const [k,id] of [['q','search'],['museum','museum'],['period','period'],['material','material'],['theme','theme']])$('#ha-'+id).value=state[k]||'';
   const group=parentGroup(state.region), child=$('#ha-place');
   $('#ha-region').value=group?.id || '';
   child.replaceChildren(new Option('全部关联地点',''));
   if(group&&group.members.length>1)group.members.forEach(id=>child.add(new Option(placeName(id),id)));
   child.value=group&&state.region!==group.id ? state.region : '';
   $('#ha-place-label').hidden=!(group&&group.members.length>1);
   $('#ha-unknown').checked=state.unknown!=='0';$('#ha-extended').checked=state.ext==='1';
   $$('[data-map]').forEach(el=>el.hidden=el.dataset.map!==(state.view==='museums'?'museums':state.ext==='1'?'extended':'regions')||state.view==='collections');
   $('.ha-map-fold').hidden=state.view==='collections';
   $$('[data-list]').forEach(el=>el.hidden=el.dataset.list!==state.view);
   $$('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===state.view)));
   $$('[data-extension]').forEach(el=>el.hidden=state.ext!=='1');
   $$('[data-region]').forEach(el=>{
    const active=state.region===el.dataset.region || group?.id===el.dataset.region || (state.work&&wb.get(state.work).map_enabled&&related(wb.get(state.work),el.dataset.region));
    if(active)el.setAttribute('aria-current','true');else el.removeAttribute('aria-current');
   });
   $$('[data-museum]').forEach(el=>{const active=el.dataset.museum===state.museum||(state.work&&wb.get(state.work).display_museum_id===el.dataset.museum);if(active)el.setAttribute('aria-current','true');else el.removeAttribute('aria-current');});
   $$('[data-collection]').forEach(el=>{if(el.dataset.collection===state.collection)el.setAttribute('aria-current','true');else el.removeAttribute('aria-current');});
   $$('[data-count-region]').forEach(el=>el.textContent=ws.filter(w=>w.map_enabled&&related(w,el.dataset.countRegion)&&matches(w,true)).length);
   if(state.work){const w=wb.get(state.work);$('#ha-map-status').textContent=w.title_zh+' · '+(w.map_enabled?w.map_associations.map(a=>regionName(a.place_id)+(a.relationship.includes('candidate')?'（候选／风格联系）':'')).join('；'):w.display_museum_id?'实际观看：'+names.get(w.display_museum_id)+'；组合陈设中的作品各有来处。':'具体地点尚未确认，暂不在地图落点。');}
   else $('#ha-map-status').textContent=state.view==='museums'?'按已识别的拍摄展馆定位；借展作品仍标出收藏者。':state.view==='collections'?'收藏机构与实际观看地点分别记录。':state.region?'已选：'+regionName(state.region):'圆点表示大致区域，不表示原寺院、工坊或出土地。';
   const active=Object.entries(state).some(([k,v])=>v&&!['view','ext'].includes(k));
   $('#ha-map-result').hidden=!active;
   $('#ha-count').textContent=selected.length+' / '+ws.length+' 条记录'+(selected.length===0?' · 没有符合条件的作品':'');
   $('#ha-matches').innerHTML=selected.slice(0,8).map(mini).join('');
   const readings=data.units.filter(u=>u.works.some(k=>ids.has(k)));
   $('#ha-readings-result').innerHTML=readings.length?'<p>相关细读</p>'+readings.map(u=>`<a href="${es(u.id)}/">${es(u.title)} →</a>`).join(''):'';
   $$('.ha-record').forEach(el=>el.hidden=!ids.has(el.dataset.work));$('#ha-empty').hidden=selected.length!==0;
   $$('.ha-reading').forEach(el=>el.classList.toggle('ha-associated',active&&readings.some(u=>u.id===el.dataset.reading)));
  }
  $$('.ha-controls,.ha-filters,.ha-map-work').forEach(el=>el.hidden=false);
  document.addEventListener('click',ev=>{
   const target=ev.target.closest('[data-region],[data-museum],[data-collection],[data-focus],[data-view],[data-reset]');if(!target)return;
   ev.preventDefault();
   if(target.hasAttribute('data-reset')){clearTimeout(timer);state={view:'regions'};writeURL();render();return;}
   if(target.dataset.view){change({view:target.dataset.view});return;}
   if(target.dataset.focus){state={view:'regions',work:target.dataset.focus};if(groups.some(g=>g.extension&&g.members.some(p=>wb.get(state.work).region_ids.includes(p))))state.ext='1';writeURL();render();$('#places').scrollIntoView();return;}
   if(target.dataset.region){change({region:target.dataset.region,work:'',view:'regions'});return;}
   if(target.dataset.museum){change({museum:target.dataset.museum,collection:'',work:'',view:'museums'});return;}
   if(target.dataset.collection)change({collection:target.dataset.collection,museum:'',work:'',view:'collections'});
  });
  $('#ha-extended').addEventListener('change',ev=>change({ext:ev.target.checked?'1':'',...(!ev.target.checked&&parentGroup(state.region)?.extension?{region:''}:{})}));
  $('#ha-unknown').addEventListener('change',ev=>change({unknown:ev.target.checked?'':'0',work:''}));
  $('#ha-region').addEventListener('change',ev=>change({region:ev.target.value,work:'',view:'regions'}));
  $('#ha-place').addEventListener('change',ev=>change({region:ev.target.value || parentGroup(state.region)?.id || '',work:'',view:'regions'}));
  for(const k of ['museum','period','material','theme'])$('#ha-'+k).addEventListener('change',ev=>change({[k]:ev.target.value,work:''}));
  $('#ha-search').addEventListener('input',ev=>{clearTimeout(timer);const q=ev.target.value;timer=setTimeout(()=>change({q,work:''}),180);});
  $('#ha-open-catalogue').addEventListener('click',()=>$('#ha-catalogue').open=true);
  const revealHash=()=>{if(location.hash&&$(location.hash)?.classList.contains('ha-record'))$('#ha-catalogue').open=true;};
  window.addEventListener('popstate',()=>{clearTimeout(timer);fromURL();render();revealHash();});window.addEventListener('hashchange',revealHash);
  fromURL();render();revealHash();
 }
})();
