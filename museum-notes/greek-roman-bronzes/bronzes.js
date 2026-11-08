/* Museum previews follow the existing, URL-backed atlas controls. */
(() => {
 const field=document.querySelector('#rs-museum');if(!field)return;
 const update=()=>document.querySelectorAll('[data-museum-preview]').forEach(p=>p.hidden=p.dataset.museumPreview!==field.value);
 const results=document.querySelector('#rs-results');new MutationObserver(update).observe(results,{childList:true});
 field.addEventListener('change',update);window.addEventListener('popstate',update);update();
})();
