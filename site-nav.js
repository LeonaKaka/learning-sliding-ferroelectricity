(()=>{
  const path=location.pathname.replace(/\/+$/,'');
  const inModules=/\/modules\//.test(path);
  const prefix=inModules?'../':'';
  const pages=[
    ['首页','index.html'],
    ['01 · What is Sliding FE?','modules/foundations.html'],
    ['02 · Switching Pathways','modules/switching-pathways.html'],
    ['03 · Domain Walls','modules/domain-walls.html'],
    ['04 · Pinning & Creep','modules/pinning-creep.html'],
    ['05 · Depinning','modules/depinning.html'],
    ['06 · Disorder & RFIM','modules/disorder-rfim.html'],
    ['07 · Numerical Modeling','modules/numerical-modeling.html'],
    ['08 · Current Frontiers','modules/current-frontiers.html'],
    ['Research Track','modules/research-track.html'],
  ];
  const labs=[
    ['L01 · TDGL wall','modules/reproduction-lab.html'],
    ['L02 · 2D wall extraction','modules/reproduction-lab-02.html'],
    ['L03 · EW roughening','modules/reproduction-lab-03.html'],
    ['L04 · GL → EW boundary','modules/reproduction-lab-04.html'],
    ['L05 · Disorder projection','modules/reproduction-lab-05.html'],
    ['L06 · Disordered geometry','modules/reproduction-lab-06.html'],
    ['L07 · Threshold search','modules/reproduction-lab-07.html'],
    ['L08 · Steady velocity','modules/reproduction-lab-08.html'],
    ['L09 · β stability','modules/reproduction-lab-09.html'],
    ['L10 · Super-rough ζ','modules/reproduction-lab-10.html'],
    ['L11 · FSS / ν','modules/reproduction-lab-11.html'],
    ['L12 · Thermal rounding','modules/reproduction-lab-12.html'],
  ];
  const hrefFor=f=>prefix+f.replace(/^modules\//,inModules?'':'modules/');
  const currentFile=(path.split('/').pop()||'index.html');
  const isActive=f=>currentFile===f.split('/').pop();

  const left=document.createElement('aside'); left.className='site-sidebar'; left.id='siteSidebar';
  left.innerHTML='<div class="site-nav-title">All pages</div>'+
    pages.map(([t,f],i)=>`<a class="${i===0?'site-nav-home ':''}${isActive(f)?'active':''}" href="${hrefFor(f)}">${t}</a>`).join('')+
    '<div class="site-nav-section">Reproduction Lab · Paper2 methods</div>'+
    `<a class="site-nav-lab ${isActive('modules/reproduction-lab.html')?'active':''}" href="${hrefFor('modules/reproduction-lab.html')}">Open Reproduction Lab →</a>`+
    labs.map(([t,f])=>`<a class="site-nav-sub ${isActive(f)?'active':''}" href="${hrefFor(f)}">${t}</a>`).join('');
  document.body.appendChild(left);

  if(currentFile==='index.html'){
    const hero=document.querySelector('main .hero');
    if(hero && !document.getElementById('reproduction-lab-entry')){
      const section=document.createElement('section');
      section.className='wrap'; section.id='reproduction-lab-entry';
      section.style.cssText='padding-top:8px;padding-bottom:10px';
      section.innerHTML=`<div style="display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:center;background:#1f201e;color:#f8f3e8;border-radius:16px;padding:22px 24px;box-shadow:0 12px 30px #00000012"><div><div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.68;margin-bottom:5px">Reproduction Lab · 12 lessons</div><b style="font:700 22px/1.25 Georgia,serif">从论文公式走到可复跑的数值证据链</b><p style="margin:8px 0 0;color:#ddd6ca">L01–L06：Paper1 方法基础；L07–L12：threshold → steady velocity → β → ζ → finite-size scaling → thermal rounding / creep boundary。</p></div><a href="modules/reproduction-lab.html" style="text-decoration:none;color:#1f201e;background:#fffdf8;border-radius:10px;padding:12px 16px;font-weight:750;white-space:nowrap">打开 Reproduction Lab →</a></div>`;
      hero.insertAdjacentElement('afterend',section);
    }
    const topNav=document.querySelector('.top .nav');
    if(topNav && !topNav.querySelector('[data-lab-link]')){
      const a=document.createElement('a'); a.href='modules/reproduction-lab.html'; a.textContent='Reproduction Lab'; a.dataset.labLink='1'; a.style.fontWeight='750'; topNav.appendChild(a);
    }
  }

  const ensureId=(el,i)=>{if(el.id)return el.id; const base=(el.textContent||'section').trim().toLowerCase().replace(/[^a-z0-9\u4e00-\u9fff]+/g,'-').replace(/^-|-$/g,'').slice(0,48)||`section-${i+1}`; let id=base,n=2; while(document.getElementById(id))id=`${base}-${n++}`; el.id=id; return id};
  const headings=[...document.querySelectorAll('main h2')].filter(h=>!h.closest('.site-sidebar,.page-toc'));
  const right=document.createElement('aside'); right.className='page-toc'; right.id='pageToc';
  right.innerHTML='<div class="page-toc-title">On this page</div>'+(headings.length?headings.map((h,i)=>`<a class="toc-h2" href="#${ensureId(h,i)}">${h.textContent.trim().replace(/\s+/g,' ')}</a>`).join(''):'<div style="padding:4px 8px;color:#807a70">本页暂无分节</div>');
  document.body.appendChild(right);

  const mkBtn=(side,label,target)=>{const b=document.createElement('button');b.className=`nav-drawer-btn ${side}`;b.type='button';b.setAttribute('aria-label',label);b.textContent=side==='left'?'☰':'≡';b.onclick=()=>{document.getElementById(target).classList.toggle('open');document.body.classList.toggle('nav-drawer-open',document.querySelector('.site-sidebar.open,.page-toc.open'))};document.body.appendChild(b)};
  mkBtn('left','打开全站导航','siteSidebar'); mkBtn('right','打开本页目录','pageToc');
  document.addEventListener('click',e=>{if(innerWidth>=1280)return; const a=e.target.closest('.site-sidebar a,.page-toc a'); if(a){left.classList.remove('open');right.classList.remove('open');document.body.classList.remove('nav-drawer-open')}});

  if('IntersectionObserver' in window && headings.length){
    const links=new Map([...right.querySelectorAll('a')].map(a=>[a.getAttribute('href').slice(1),a]));
    const io=new IntersectionObserver(es=>{for(const e of es)if(e.isIntersecting){right.querySelectorAll('a.active').forEach(a=>a.classList.remove('active'));links.get(e.target.id)?.classList.add('active')}},{rootMargin:'-18% 0px -70% 0px'});
    headings.forEach(h=>io.observe(h));
  }
})();
