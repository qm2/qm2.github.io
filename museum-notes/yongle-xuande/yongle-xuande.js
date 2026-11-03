(() => {
 'use strict';
 const reveal=()=>{
  let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
  if(id==='w1514'){location.replace('#w1486');return;}
  const node=document.getElementById(id);if(!node)return;
  for(let p=node;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;
  requestAnimationFrame(()=>node.scrollIntoView({block:'start'}));
 };
 reveal();window.addEventListener('hashchange',reveal);
})();
