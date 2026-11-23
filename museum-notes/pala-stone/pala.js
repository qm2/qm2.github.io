(() => {
  'use strict';
  const root='/museum-notes/pala-stone/';
  function openHash(){let el;try{el=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch{return;}if(!el)return;for(let p=el;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;requestAnimationFrame(()=>el.scrollIntoView({block:'start'}));}
  addEventListener('hashchange',openHash);if(location.hash)setTimeout(openHash,100);
  const svg=document.getElementById('ps-map');if(!svg)return;
  const form=document.getElementById('ps-filters');const fields=['search','museum','religion','group','sort'];const controls=Object.fromEntries(fields.map(k=>[k,document.getElementById('ps-'+k)]));
  const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let records=[],museums=[],land=null,region='mainland',selected='',visible=[];
  const bounds={mainland:[-126,-66,23,50],east:[-97,-70,24,45],hawaii:[-161,-154,18,23]};
  const filter=()=>{const q=(controls.search?.value||'').trim().toLowerCase();return records.filter(w=>(!q||w.search.toLowerCase().includes(q))&&['museum','religion','group'].every(k=>!controls[k]?.value||w[k==='museum'?'viewing_museum_id':k]===controls[k].value));};
  function readState(){if(!form)return;const qs=new URLSearchParams(location.search);fields.forEach(k=>{const c=controls[k];c.value=qs.get(k)|| (k==='sort'?'catalogue':'');if(c.tagName==='SELECT'&&c.selectedIndex<0)c.selectedIndex=0;});}
  function writeState(){if(!form)return;const qs=new URLSearchParams(location.search);fields.forEach(k=>{const v=controls[k].value;if(v&&!(k==='sort'&&v==='catalogue'))qs.set(k,v);else qs.delete(k);});const u=location.pathname+(qs.size?'?'+qs:'')+location.hash;if(u!==location.pathname+location.search+location.hash)history.pushState({},'',u);}
  function card(w){return `<a class="ps-card" href="${w.url}"><img src="${w.image}" alt="${esc(w.title)}" width="400" height="533" loading="lazy"><h3>${esc(w.title)}</h3><p>${esc(w.date)}</p></a>`;}
  function selection(){const box=document.getElementById('ps-map-selection');if(!selected){box.innerHTML='';return;}const m=museums.find(m=>m.museum_id===selected),ws=visible.filter(w=>w.viewing_museum_id===selected);if(!ws.length){box.innerHTML='';return;}box.innerHTML=`<h3>${esc(m.label_zh)}</h3><p>${esc(m.city)} · 当前${ws.length}件作品 · <a href="${root}atlas/?museum=${m.museum_id}#catalogue">打开该馆完整图录</a></p><div class="ps-grid">${ws.map(card).join('')}</div>`;}
  function choose(id){selected=id;if(form){controls.museum.value=id;writeState();update();svg.querySelector(`[data-museum="${id}"]`)?.focus({preventScroll:true});}else selection();}
  let customBounds=null;
  function draw(){
    if(!land)return;
    const b=customBounds||bounds[region],W=Math.max(320,svg.clientWidth||1000),H=W<650?330:470;
    svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
    const cos=Math.cos((b[2]+b[3])/2*Math.PI/180),scale=Math.min((W-50)/((b[1]-b[0])*cos),(H-55)/(b[3]-b[2])),dx=(W-(b[1]-b[0])*cos*scale)/2,dy=(H-(b[3]-b[2])*scale)/2;
    const xy=([lon,lat])=>[dx+(lon-b[0])*cos*scale,H-dy-(lat-b[2])*scale];
    const polygons=land.features.flatMap(f=>f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates);
    const paths=polygons.map(poly=>poly.map(r=>r.map((p,i)=>{const q=xy(p);return(i?'L':'M')+q[0].toFixed(1)+','+q[1].toFixed(1);}).join('')+'Z').join('')).join('');
    const active=museums.filter(m=>visible.some(w=>w.viewing_museum_id===m.museum_id)&&m.longitude>=b[0]&&m.longitude<=b[1]&&m.latitude>=b[2]&&m.latitude<=b[3]);
    const clusters=[];
    active.forEach(m=>{const [x,y]=xy([m.longitude,m.latitude]);let c=clusters.find(c=>c.items.some(v=>Math.hypot(v.x-x,v.y-y)<42));if(!c){c={items:[]};clusters.push(c);}c.items.push({m,x,y});});
    svg.innerHTML=`<defs><clipPath id="ps-map-clip"><rect width="${W}" height="${H}"/></clipPath></defs><g clip-path="url(#ps-map-clip)"><path class="ps-land" d="${paths}"/></g>`+clusters.map((c,i)=>{
      const x=c.items.reduce((a,p)=>a+p.x,0)/c.items.length,y=c.items.reduce((a,p)=>a+p.y,0)/c.items.length,group=c.items.length>1,m=c.items[0].m,n=visible.filter(w=>w.viewing_museum_id===m.museum_id).length;
      const label=group?'':m.city,name=group?c.items.map(p=>p.m.label_zh).join('、')+'，点击放大':m.label_zh+'，'+n+'件作品';
      const right=x<W*.65,ox=right?19:-19,oy=group?-20:-16;
      return `<g class="ps-marker" tabindex="0" role="button" data-cluster="${i}" ${group?'':`data-museum="${m.museum_id}"`} aria-label="${esc(name)}" transform="translate(${x.toFixed(1)} ${y.toFixed(1)})"><title>${esc(name)}</title><circle r="22" fill="transparent"/><circle class="ps-dot" r="${group?17:13}"/><text class="ps-number" y="4">${group?c.items.length+'馆':n}</text><text class="ps-marker-label" x="${ox}" y="${oy}" text-anchor="${right?'start':'end'}">${esc(label)}</text></g>`;
    }).join('');
    svg.querySelectorAll('[data-cluster]').forEach(el=>{
      const activate=()=>{const c=clusters[Number(el.dataset.cluster)];if(c.items.length===1){choose(c.items[0].m.museum_id);return;}
        const xs=c.items.map(p=>p.m.longitude),ys=c.items.map(p=>p.m.latitude);customBounds=[Math.min(...xs)-.6,Math.max(...xs)+.6,Math.min(...ys)-.6,Math.max(...ys)+.6];draw();svg.querySelector('[data-cluster]')?.focus();};
      el.addEventListener('click',activate);el.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();activate();}});
    });
  }
  function update(){visible=filter();if(form){const ids=new Set(visible.map(w=>w.id));document.querySelectorAll('[data-record-id]').forEach(el=>el.hidden=!ids.has(el.dataset.recordId));document.getElementById('ps-result-count').textContent=`当前${visible.length}件 / 全部${records.length}件`;document.getElementById('ps-empty').hidden=visible.length>0;const sorted=[...records];if(controls.sort.value==='date')sorted.sort((a,b)=>a.date_start-b.date_start);if(controls.sort.value==='museum')sorted.sort((a,b)=>a.viewing_museum_id.localeCompare(b.viewing_museum_id));const grid=document.querySelector('.ps-catalogue');sorted.forEach(w=>grid.append(document.querySelector(`[data-record-id="${w.id}"]`)));if(controls.museum.value)selected=controls.museum.value;}draw();selection();}
  Promise.all([fetch(root+'data/atlas-index.json').then(r=>{if(!r.ok)throw Error();return r.json();}),fetch(root+'data/museums.json').then(r=>{if(!r.ok)throw Error();return r.json();})]).then(([rs,ms])=>{records=rs;museums=ms;readState();if(form){form.hidden=false;form.addEventListener('submit',ev=>ev.preventDefault());let timer;controls.search.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>{writeState();update();},220);});fields.filter(k=>k!=='search').forEach(k=>controls[k].addEventListener('change',()=>{writeState();update();}));form.addEventListener('reset',()=>{selected='';setTimeout(()=>{writeState();update();},0);});addEventListener('popstate',()=>{selected='';readState();update();});}update();return fetch('/museum-notes/homer/data/ne_110m_land.geojson').then(r=>{if(!r.ok)throw Error();return r.json();});}).then(data=>{land=data;document.querySelector('[data-map-box]').hidden=false;document.querySelectorAll('[data-map]').forEach(b=>b.addEventListener('click',()=>{region=b.dataset.map;customBounds=null;document.querySelectorAll('[data-map]').forEach(a=>a.setAttribute('aria-pressed',String(a===b)));draw();}));draw();let resize;addEventListener('resize',()=>{clearTimeout(resize);resize=setTimeout(draw,120);});}).catch(()=>{/* Static museum links and complete catalogue remain available. */});
})();
// Progressive timeline filter; static cards and place links remain usable without JS.
(()=>{const tools=document.getElementById('ps-time-filters');if(!tools)return;tools.hidden=false;const records=[...document.querySelectorAll('[data-time-work]')];const apply=()=>{const faith=new URL(location.href).searchParams.get('faith')||'';let n=0;for(const r of records){r.hidden=!!faith&&r.dataset.faith!==faith;if(!r.hidden)n++;}for(const b of tools.querySelectorAll('button'))b.setAttribute('aria-pressed',String(b.dataset.time===faith));document.getElementById('ps-time-count').textContent=`当前${n}件作品`;};tools.addEventListener('click',e=>{const b=e.target.closest('[data-time]');if(!b)return;const u=new URL(location.href);if(b.dataset.time)u.searchParams.set('faith',b.dataset.time);else u.searchParams.delete('faith');history.pushState({},'',u);apply();});window.addEventListener('popstate',apply);apply();})();

// Keep horizontal navigation within reach while reading the long century columns.
(()=>{
 const track=document.getElementById('ps-time-track');if(!track)return;
 const nav=document.querySelector('.ps-time-navigation'),prev=document.getElementById('ps-time-prev'),next=document.getElementById('ps-time-next'),period=document.getElementById('ps-time-period');
 const columns=[...track.querySelectorAll('.ps-century')];
 const update=()=>{prev.disabled=track.scrollLeft<=2;next.disabled=track.scrollLeft>=track.scrollWidth-track.clientWidth-2;};
 const move=left=>track.scrollTo({left,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
 prev.addEventListener('click',()=>move(track.scrollLeft-Math.max(245,track.clientWidth*.8)));
 next.addEventListener('click',()=>move(track.scrollLeft+Math.max(245,track.clientWidth*.8)));
 period.addEventListener('change',()=>{
  if(period.value==='')return;
  const column=columns[Number(period.value)];
  move(track.scrollLeft+column.getBoundingClientRect().left-track.getBoundingClientRect().left);
 });
 track.addEventListener('scroll',update,{passive:true});
 new ResizeObserver(update).observe(track);nav.hidden=false;update();
})();
