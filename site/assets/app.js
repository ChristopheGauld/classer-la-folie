/* Enhancements only: the full reading content is present in the HTML. */
'use strict';
(() => {
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const data = window.SITE_DATA;
  if (!data) return;
  const normalize = (s) => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const setText = (s, value) => { const el = $(s); if (el) el.textContent = value; };
  const setPressed = (selector, selected) => $$(selector).forEach(b => b.setAttribute('aria-pressed', String(b === selected)));
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
      .sort((a,b) => Number(b.normalTitle.includes(query)) - Number(a.normalTitle.includes(query))) : searchable.filter(item => item.kind.startsWith('Étape'));
    const container = $('#search-results'); container.replaceChildren();
    setText('#search-status', terms.length ? `${results.length} résultat${results.length === 1 ? '' : 's'}` : 'Les neuf étapes de la traversée');
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
    $$('[data-complete]').forEach(b=>{const done=read.has(b.dataset.complete);b.classList.toggle('done',done);b.setAttribute('aria-pressed',String(done));b.textContent=done?'✓ Étape lue · annuler':'Marquer cette étape comme lue';});
    $$('[data-lesson-row]').forEach(row=>{$('.read-mark',row).hidden=!read.has(row.dataset.lessonRow);});
    setText('#reading-counter',`${read.size} étape${read.size===1?'':'s'} lue${read.size===1?'':'s'} sur ${data.lessons.length} · progression enregistrée sur cet appareil`);
  }
  function saveRead(){try{localStorage.setItem(storageKey,JSON.stringify([...read]));}catch{/* Reading still works when storage is disabled. */}updateRead();}
  $$('[data-complete]').forEach(b=>b.addEventListener('click',()=>{read.has(b.dataset.complete)?read.delete(b.dataset.complete):read.add(b.dataset.complete);saveRead();}));
  $('#reset-progress')?.addEventListener('click',()=>{read.clear();saveRead();});
  window.addEventListener('storage',ev=>{if(ev.key===storageKey){read=getRead();updateRead();}});updateRead();
  $$('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
    setPressed('[data-filter]',button);$$('[data-lesson-row]').forEach(row=>row.hidden=button.dataset.filter!=='all'&&row.dataset.group!==button.dataset.filter);
  }));
  const progress=$('#reading-progress'), article=$('article.reading');
  if(progress&&article){
    let queued=false;
    const update=()=>{const rect=article.getBoundingClientRect();const available=Math.max(1,rect.height-innerHeight+100);progress.style.width=Math.max(0,Math.min(100,(100-rect.top)/available*100))+'%';queued=false;};
    addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(update);}},{passive:true});addEventListener('resize',update);update();
  }
  // Classification comparison: distinct questions and distinct uses.
  const classes={
    categories:['Quel ensemble de manifestations reconnaît-on ?','Les classifications diagnostiques organisent des manifestations en catégories, avec des critères communs. Elles soutiennent la communication, la recherche et l’organisation des soins.','Un nom diagnostique ne décrit pas toute une histoire et n’établit pas à lui seul une cause.'],
    stades:['Comment la situation évolue-t-elle dans le temps ?','La stadification distingue des étapes possibles dans l’évolution d’un trouble. Elle s’intéresse aux premiers signes, aux épisodes et aux transformations ultérieures.','Les étapes ne dessinent pas une aggravation inévitable. Un facteur de risque n’est pas nécessairement le début d’un trouble.'],
    hitop:['À quel niveau décrire les régularités ?','HiTOP regroupe les manifestations selon leurs relations statistiques, à des niveaux plus ou moins larges. On peut passer de dimensions générales à des descriptions plus fines.','Une hiérarchie de regroupements statistiques n’est ni une hiérarchie des personnes ni une preuve de causalité.'],
    rdoc:['Quelles fonctions étudier, et à quelles échelles ?','RDoC étudie des dimensions du fonctionnement, comme l’attention, à plusieurs échelles : comportement, fonctionnement cérébral ou génétique.','RDoC est un cadre de recherche. Il n’est pas un guide pour poser un diagnostic en consultation.']
  };
  $$('[data-classification]').forEach(b=>b.addEventListener('click',()=>{setPressed('[data-classification]',b);const [title,body,limit]=classes[b.dataset.classification];setText('#class-title',title);setText('#class-text',body);setText('#class-limit',limit);}));
  // Fictitious overdamped double-well system, x'=x-x^3.
  if($('#landscape')){
    const point=x=>[300+x*165,155-360*(x**4/4-x*x/2)];
    const points=Array.from({length:121},(_,i)=>point(-1.6+i*3.2/120));
    const path=points.map((p,i)=>(i?'L':'M')+p.map(v=>v.toFixed(2)).join(' ')).join(' ');
    $('#landscape-line').setAttribute('d',path);$('#landscape-fill').setAttribute('d',path+'L564 267L36 267Z');
    let start='valley',x=-1,raf=0;
    const move=$('#move-ball');
    const draw=()=>{const [cx,cy]=point(x);$('#landscape-ball').setAttribute('cx',cx);$('#landscape-ball').setAttribute('cy',cy-9);};
    const reset=()=>{cancelAnimationFrame(raf);x=start==='valley'?-1:-.12;move.disabled=false;draw();setText('#dynamic-result',start==='valley'?'La bille part au fond de la vallée A. Une configuration stable n’est pas nécessairement un état souhaitable.':'La bille part du côté A, tout près de la crête. Le même déplacement peut la faire passer dans l’autre bassin d’attraction.');};
    $$('[data-start]').forEach(b=>b.addEventListener('click',()=>{start=b.dataset.start;setPressed('[data-start]',b);reset();}));
    $('#reset-ball').addEventListener('click',reset);
    move.addEventListener('click',()=>{
      move.disabled=true;x+=.28;draw();let steps=0;
      const finish=()=>{x=x<0?-1:1;draw();setText('#dynamic-result',x<0?'Avec ce départ, le déplacement ne franchit pas la crête : la bille revient vers la configuration A.':'Avec ce départ, le même déplacement franchit la crête : la bille rejoint la configuration B. Ce résultat appartient au modèle fictif.');};
      if(matchMedia('(prefers-reduced-motion: reduce)').matches){finish();return;}
      setText('#dynamic-result','La bille suit la pente après le déplacement…');
      const step=()=>{for(let k=0;k<4;k++){x+=.025*(x-x**3);steps++;}draw();if(steps<520)raf=requestAnimationFrame(step);else finish();};
      raf=requestAnimationFrame(step);
    });reset();
  }
  const networkModes={
    association:['VARIENT ENSEMBLE','Une association indique que les mesures varient ensemble. Elle ne dit pas, à elle seule, si l’une cause l’autre.',''],
    hypothesis:['INFLUENCE SUPPOSÉE','La flèche exprime ici une hypothèse : le sommeil perturbé contribuerait à la fatigue. Le sens de la flèche est posé dans le schéma ; il ne démontre pas cette influence.','7 5'],
    perceived:['RELATION DÉCRITE','Dans cet exemple inventé, une personne décrit le lien ainsi : « Après une mauvaise nuit, je me sens épuisée. » Cette relation perçue compte pour comprendre son expérience ; elle ne constitue pas seule une preuve causale.','2 5']
  };
  $$('[data-network]').forEach(b=>b.addEventListener('click',()=>{
    const mode=b.dataset.network,[label,description,dash]=networkModes[mode];setPressed('[data-network]',b);setText('#edge-label',label);setText('#network-result',description);
    const edge=$('#network-edge');edge.setAttribute('stroke-dasharray',dash);if(mode==='association')edge.removeAttribute('marker-end');else edge.setAttribute('marker-end','url(#arrow)');
  }));
  $('#toggle-context')?.addEventListener('click',ev=>{const b=ev.currentTarget,on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',String(on));$('#context-edges').toggleAttribute('hidden',!on);$('#context-result').hidden=!on;b.textContent=on?'Masquer le facteur commun':'Ajouter un facteur commun possible';});
  if($('#prior')){
    function updatePrediction(){const prior=Number($('#prior').value),q=Number($('#reliability').value),p=prior/100,r=q/100;const result=100*p*r/(p*r+(1-p)*(1-r));const value=new Intl.NumberFormat('fr-FR',{maximumFractionDigits:1}).format(result);
      setText('#prior-value',prior+' %');setText('#reliability-value',q+' %');setText('#prior-output',prior+' %');setText('#posterior',value+' %');$('#round-bar').style.width=result+'%';$('#square-bar').style.width=(100-result)+'%';
      setText('#prediction-result',q===50?`Un indice fiable à 50 % n’apporte aucune information dans ce modèle : la probabilité reste à ${prior} %.`:`Avec une attente initiale de ${prior} % et un indice fiable à ${q} %, la probabilité révisée est de ${value} %. Ce résultat dépend des hypothèses choisies.`);
    }$('#prior').addEventListener('input',updatePrediction);$('#reliability').addEventListener('input',updatePrediction);updatePrediction();
  }
  const reasoning={
    artisan:['Ajuster la description à cette rencontre','Que veut dire « ne plus dormir comme avant » pour cette personne ? Quand les difficultés surviennent-elles, que ressent-elle et qu’est-ce qu’elles changent dans sa vie ? La phrase seule ne permet pas de le savoir.'],
    anthropologue:['Situer les mots dans un monde','Quels horaires de travail, quelles conditions de logement et quelles obligations familiales entourent le sommeil ? Comment cette personne comprend-elle ce qu’elle traverse ? Ces questions élargissent le contexte sans supposer leurs réponses.'],
    cartographe:['Se repérer parmi les hypothèses','Quelles informations sont observées, racontées ou encore manquantes ? Quelles approches aideraient à les comprendre ? Comparer des cartes permet de préciser les questions sans prendre l’une d’elles pour la totalité de la situation.']
  };
  $$('[data-reasoning]').forEach(b=>b.addEventListener('click',()=>{setPressed('[data-reasoning]',b);const [title,description]=reasoning[b.dataset.reasoning],box=$('#reasoning-result');box.replaceChildren();const strong=document.createElement('strong');strong.textContent=title;const p=document.createElement('p');p.textContent=description;box.append(strong,p);}));
})();
