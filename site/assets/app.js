/* Enhancements only: the full reading content is present in the HTML. */
'use strict';
(() => {
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const data = window.SITE_DATA;
  if (!data) return;
  const normalize = (s) => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const setText = (s, value) => { const el = $(s); if (el) el.textContent = value; };
  const menu = $('#main-nav'), menuToggle = $('.menu-toggle');
  const closeMenu = () => { menu?.classList.remove('open'); menuToggle?.setAttribute('aria-expanded', 'false'); menuToggle?.setAttribute('aria-label', 'Ouvrir le menu'); };
  menuToggle?.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
  });
  $$('.nav a').forEach(a => a.addEventListener('click', closeMenu));
  $$('.dialog').forEach(dialog => {
    $('.dialog-close', dialog)?.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', ev => {
      const rect = dialog.getBoundingClientRect();
      if (ev.target === dialog && (ev.clientX < rect.left || ev.clientX > rect.right || ev.clientY < rect.top || ev.clientY > rect.bottom)) dialog.close();
    });
  });
  const searchDialog = $('#search-dialog'), searchInput = $('#site-search');
  const searchable = data.search.map(item => ({...item, normalTitle:normalize(item.title), normalText:normalize(item.text)}));
  function search() {
    const query = normalize(searchInput.value.trim());
    const terms = query.split(/\s+/).filter(Boolean);
    const results = terms.length ? searchable.filter(item => terms.every(t => item.normalText.includes(t) || item.normalTitle.includes(t)))
      .sort((a,b) => Number(b.normalTitle.includes(query)) - Number(a.normalTitle.includes(query))) : searchable.filter(item => item.kind !== 'Définition');
    const container = $('#search-results'); container.replaceChildren();
    setText('#search-status', terms.length ? `${results.length} résultat${results.length === 1 ? '' : 's'}` : 'Les chapitres de l’ouvrage');
    if (!results.length) {
      const p = document.createElement('p'); p.className='empty-state'; p.textContent='Aucun résultat. Essayez un terme plus simple ou consultez le lexique.'; container.append(p);
    }
    results.slice(0,30).forEach(item => {
      const a=document.createElement('a'); a.href=item.url;
      const label=document.createElement('span'); label.className='eyebrow'; label.textContent=item.kind;
      const title=document.createElement('strong'); title.textContent=item.title;
      const snippet=document.createElement('small'); snippet.textContent=item.excerpt;
      a.append(label,title,snippet); container.append(a);
    });
    if(results.length>30) {
      const p=document.createElement('p');p.className='small muted';p.textContent='Les 30 premiers résultats sont affichés. Précisez votre recherche pour les affiner.';container.append(p);
    }
  }
  function openSearch() { closeMenu(); search(); searchDialog.showModal(); searchInput.focus(); }
  $$('.search-trigger').forEach(b=>b.addEventListener('click',openSearch));
  searchInput?.addEventListener('input',search);
  document.addEventListener('keydown',ev=>{
    if((ev.ctrlKey||ev.metaKey)&&ev.key.toLowerCase()==='k') {
      ev.preventDefault(); $$('.dialog[open]').forEach(d=>d.close());openSearch();
    }
    if(ev.key==='Escape')closeMenu();
  });
  const terms = new Map(data.glossary.map(g=>[g.id,g]));
  $$('[data-term]').forEach(a=>a.addEventListener('click',ev=>{
    const g=terms.get(a.dataset.term);if(!g)return;
    ev.preventDefault();setText('#term-title',g.term);setText('#term-definition',g.definition);
    $('#term-link').href='lexique.html#'+g.id;
    $('#term-dialog').showModal();
  }));
  const glossaryInput = $('#glossary-search');
  function filterGlossary() {
    const query=normalize(glossaryInput.value.trim());let count=0;
    $$('.definition').forEach(item=>{const show=normalize(item.textContent).includes(query);item.hidden=!show;if(show)count++;});
    setText('#glossary-count',`${count} notion${count===1?'':'s'}`);$('#glossary-empty').hidden=count!==0;
  }
  glossaryInput?.addEventListener('input',filterGlossary);
  if(glossaryInput) window.addEventListener('hashchange',()=>{glossaryInput.value='';filterGlossary();document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView();});
  const storageKey='classer-la-folie:read:v1';
  function getRead(){try{const value=JSON.parse(localStorage.getItem(storageKey)||'[]');return new Set(Array.isArray(value)?value.filter(x=>data.lessons.some(l=>l.slug===x)):[]);}catch{return new Set();}}
  let read=getRead();
  function updateRead(){
    $$('[data-complete]').forEach(b=>{const done=read.has(b.dataset.complete);b.classList.toggle('done',done);b.setAttribute('aria-pressed',String(done));b.textContent=done?'Section lue · annuler':'Marquer cette section comme lue';});
    $$('[data-lesson-row]').forEach(row=>{$('.read-mark',row).hidden=!read.has(row.dataset.lessonRow);});
    setText('#reading-counter',`${read.size} section${read.size===1?'':'s'} lue${read.size===1?'':'s'} sur ${data.lessons.length} · information enregistrée sur cet appareil`);
  }
  function saveRead(){try{localStorage.setItem(storageKey,JSON.stringify([...read]));}catch{/* Reading still works when storage is disabled. */}updateRead();}
  $$('[data-complete]').forEach(b=>b.addEventListener('click',()=>{read.has(b.dataset.complete)?read.delete(b.dataset.complete):read.add(b.dataset.complete);saveRead();}));
  $('#reset-progress')?.addEventListener('click',()=>{read.clear();saveRead();});
  window.addEventListener('storage',ev=>{if(ev.key===storageKey){read=getRead();updateRead();}});updateRead();
  const progress=$('#reading-progress'), article=$('article.reading');
  if(progress&&article){
    let queued=false;
    const update=()=>{const rect=article.getBoundingClientRect();const available=Math.max(1,rect.height-innerHeight+100);progress.style.width=Math.max(0,Math.min(100,(100-rect.top)/available*100))+'%';queued=false;};
    addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(update);}},{passive:true});addEventListener('resize',update);update();
  }
})();
