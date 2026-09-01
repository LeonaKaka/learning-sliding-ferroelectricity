(() => {
  'use strict';

  // Keep the glossary intentionally compact. Longest phrases win, and each
  // concept is annotated only once per page. Paper quotations and equations
  // are never touched.
  const termPairs = [
    ['depinning universality class','退钉扎普适类'],
    ['off-diagonal Born effective charge','非对角 Born 有效电荷'],
    ['pre-existing domain-wall motion','预存畴壁运动'],
    ['random-field disorder','随机场无序'],
    ['random-bond disorder','随机键无序'],
    ['disordered elastic interface','无序弹性界面'],
    ['finite-size scaling','有限尺寸标度'],
    ['system-size scaling','系统尺寸标度'],
    ['scaling collapse','标度坍缩'],
    ['corrections to scaling','标度修正'],
    ['roughness correlation function','粗糙度关联函数'],
    ['free-energy functional','自由能泛函'],
    ['bulk order-parameter model','体相序参量模型'],
    ['domain-wall motion','畴壁运动'],
    ['switching pathway','极化翻转路径'],
    ['multiple polarization states','多极化态'],
    ['free-carrier screening','自由载流子屏蔽'],
    ['Born effective charge','Born 有效电荷'],
    ['out-of-plane polarization','面外极化'],
    ['in-plane force','面内力'],
    ['critical depinning','临界退钉扎'],
    ['depinning criticality','退钉扎临界性'],
    ['depinning threshold','退钉扎阈值'],
    ['critical manifold','临界流形'],
    ['critical geometry','临界几何'],
    ['critical exponents','临界指数'],
    ['critical exponent','临界指数'],
    ['critical force','临界力'],
    ['critical field','临界场'],
    ['correlation length','关联长度'],
    ['velocity exponent','速度指数'],
    ['roughness exponent','粗糙指数'],
    ['universality class','普适类'],
    ['universality test','普适性检验'],
    ['quenched disorder','淬火无序'],
    ['pinning landscape','钉扎景观'],
    ['disorder landscape','无序景观'],
    ['random pinning potential','随机钉扎势'],
    ['elastic interface','弹性界面'],
    ['elastic line','弹性线'],
    ['order parameter','序参量'],
    ['Landau free energy','朗道自由能'],
    ['gradient energy','梯度能'],
    ['phase-field','相场'],
    ['phase field','相场'],
    ['coarse-graining','粗粒化'],
    ['coarse graining','粗粒化'],
    ['diffuse interface','弥散界面'],
    ['emergent interface','涌现界面'],
    ['structure factor','结构因子'],
    ['stacking registry','堆垛构型'],
    ['stacking configuration','堆垛构型'],
    ['intermediate state','中间态'],
    ['domain pattern','畴图样'],
    ['white disorder','白噪声无序'],
    ['disorder strength','无序强度'],
    ['creep law','蠕变定律'],
    ['power-law','幂律'],
    ['domain walls','畴壁'],
    ['domain wall','畴壁'],
    ['depinning','退钉扎'],
    ['pinning','钉扎'],
    ['creep','蠕变'],
    ['roughness','粗糙度'],
    ['universality','普适性'],
    ['criticality','临界性'],
    ['threshold','阈值'],
    ['random-field','随机场'],
    ['random field','随机场'],
    ['random-bond','随机键'],
    ['random bond','随机键'],
    ['RFIM','随机场伊辛模型'],
    ['QEW','淬火 Edwards–Wilkinson 模型'],
    ['TDGL','含时金兹堡–朗道方程'],
    ['KPFM','开尔文探针力显微镜'],
    ['polarization','极化'],
    ['screening','屏蔽'],
    ['hysteresis','滞回'],
    ['avalanche','雪崩'],
    ['metastability','亚稳性'],
    ['observables','可观测量'],
    ['observable','可观测量'],
  ];

  const glossary = new Map(termPairs.map(([en, zh]) => [en.toLowerCase(), zh]));
  const orderedTerms = [...glossary.keys()].sort((a, b) => b.length - a.length);
  const escapeRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const termRe = new RegExp(`(^|[^A-Za-z0-9])(${orderedTerms.map(escapeRe).join('|')})(?=$|[^A-Za-z0-9])`, 'gi');
  const seen = new Set();

  function blocked(el) {
    return !el || !!el.closest('script,style,pre,code,kbd,samp,math,.source-text,.eq,h1,h2,h3,a,.brand,.bar');
  }

  function annotateConceptChips() {
    document.querySelectorAll('.concept').forEach(el => {
      const raw = el.textContent.trim();
      const zh = glossary.get(raw.toLowerCase());
      if (!zh || raw.includes('（')) return;
      el.textContent = `${raw}（${zh}）`;
      seen.add(raw.toLowerCase());
    });
  }

  function annotateText() {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      const el = node.parentElement;
      if (blocked(el) || !/[A-Za-z]/.test(node.nodeValue || '')) continue;
      let usedHere = 0;
      node.nodeValue = node.nodeValue.replace(termRe, (whole, lead, raw, offset, full) => {
        const key = raw.toLowerCase();
        const after = full.slice(offset + whole.length);
        if (after.startsWith('（')) {
          seen.add(key);
          return whole;
        }
        if (seen.has(key) || usedHere >= 2) return whole;
        seen.add(key);
        usedHere += 1;
        return `${lead}${raw}（${glossary.get(key)}）`;
      });
    }
  }

  function applyPageSpecificReadingFixes() {
    const matrix = document.querySelector('table.matrix');
    if (matrix && !matrix.parentElement.classList.contains('matrix-scroll')) {
      const wrap = document.createElement('div');
      wrap.className = 'matrix-scroll';
      wrap.setAttribute('role', 'region');
      wrap.setAttribute('aria-label', 'Frontier evidence matrix');
      wrap.tabIndex = 0;
      matrix.parentNode.insertBefore(wrap, matrix);
      wrap.appendChild(matrix);
      const style = document.createElement('style');
      style.textContent = '.matrix-scroll{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:24px 0}.matrix-scroll .matrix{display:table!important;min-width:820px;margin:0}.matrix-scroll .matrix th{position:static}@media(max-width:760px){.matrix-scroll{margin-left:0;margin-right:0}}';
      document.head.appendChild(style);
    }

    document.querySelectorAll('p.rule').forEach(el => {
      if (!el.textContent.includes('Chauve 2000 当前不在该项目 Drive 文件夹')) return;
      el.textContent = '素材来源：Chauve 2000、Rosso 2003、Ferrero 2013、Wiese 2022 均已由项目 Google Drive · 03 Depinning, elastic-interface, RFIM theory 中的论文 PDF 核验。作者原文均为可选择、可复制 HTML 真文本；Figure 为对应论文 PDF 派生的无损 PNG，点击可查看原尺寸。';
    });
  }

  function addMobileToc() {
    const source = document.querySelector('.bar span');
    const header = document.querySelector('header.top');
    if (!source || !header || document.querySelector('.mobile-toc')) return;
    const links = [...source.querySelectorAll('a')];
    if (!links.length) return;

    const details = document.createElement('details');
    details.className = 'mobile-toc';
    const summary = document.createElement('summary');
    summary.textContent = '本章导航';
    const nav = document.createElement('nav');
    for (const link of links) {
      const clone = link.cloneNode(true);
      clone.addEventListener('click', () => details.removeAttribute('open'));
      nav.appendChild(clone);
    }
    details.append(summary, nav);
    header.insertAdjacentElement('afterend', details);

    const style = document.createElement('style');
    style.textContent = `
      .mobile-toc{display:none}
      @media(max-width:760px){
        .mobile-toc{display:block;position:sticky;top:62px;z-index:2;margin:0;background:rgba(243,240,232,.97);border-bottom:1px solid #d8d1c3;padding:0 16px}
        .mobile-toc summary{cursor:pointer;list-style:none;padding:9px 0;font-size:12px;color:#5f5b54;font-weight:600}
        .mobile-toc summary::-webkit-details-marker{display:none}
        .mobile-toc summary:after{content:'＋';float:right;font-weight:400}
        .mobile-toc[open] summary:after{content:'−'}
        .mobile-toc nav{display:flex;gap:8px;overflow-x:auto;padding:0 0 10px;scrollbar-width:none}
        .mobile-toc nav::-webkit-scrollbar{display:none}
        .mobile-toc a{flex:0 0 auto;text-decoration:none;border:1px solid #d8d1c3;border-radius:999px;padding:5px 9px;background:#fffdf8;color:#504c46;font-size:11px}
      }`;
    document.head.appendChild(style);
  }

  applyPageSpecificReadingFixes();
  annotateConceptChips();
  annotateText();
  addMobileToc();
})();
