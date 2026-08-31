(() => {
  'use strict';
  const pairs = [
    ['Evidence score','证据评分'], ['What is missing','缺失证据'],
    ['distribution','分布'], ['islands','岛状畴'], ['depin','解钉'],
    ['soliton profile','孤子剖面'], ['continuum','连续介质'], ['trajectory','轨迹'],
    ['pulse width','脉冲宽度'], ['saturation','饱和'], ['switched-area plateau','翻转面积平台'],
    ['pause','停滞'], ['panel','子图'], ['hierarchy','层级'], ['variability','波动'],
    ['spatial trajectory','空间轨迹'], ['curve','曲线'], ['variation','变化'], ['verdict','结论'],
    ['trapping competition','俘获竞争'], ['readout','读出'], ['statistics','统计'],
    ['ground-state domains','基态畴'], ['ground-state domain','基态畴'],
    ['broken configurations','对称性破缺构型'], ['contrast','对比'], ['origin','起源'],
    ['device-scale','器件尺度'], ['mechanically segmented regions','机械分区'],
    ['mechanically segmented region','机械分区'], ['stepwise','分步'],
    ['extraction rule','提取规则'], ['finite size','有限尺寸'], ['lateral size','横向尺寸'],
    ['cutoff','截断'], ['definition','定义'], ['event','事件'], ['triangular P–E','三角波 P–E'],
    ['observations','观测'], ['finite-size dependence','有限尺寸依赖'], ['regimes','状态区间'],
    ['inset','插图'], ['dimensionality','维数'], ['moving criterion','运动判据'],
    ['height','高度'], ['description','描述'], ['spins','自旋'], ['charge trap','电荷陷阱'],
    ['self-similar','自相似'], ['invaded area','侵入区域'], ['scaling arguments','标度论证'],
    ['arguments','论证'], ['study','研究'], ['correlation','关联'], ['background','背景'],
    ['dynamic roughening','动态粗化'], ['comparison','对比'], ['conjecture','猜想'],
    ['lattice anisotropy','晶格各向异性'], ['lower critical dimension','下临界维度'],
    ['bounded','有界'], ['Monte Carlo','蒙特卡洛'], ['short-time dynamics','短时动力学'],
    ['short-time depinning','短时退钉扎'], ['force–velocity','力–速度'], ['force-velocity','力–速度'],
    ['constant-field','恒定外场'], ['region-dependent','区域依赖'],
    ['continuum disorder strength','连续介质无序强度'], ['unit-cell','单胞'],
    ['Stark shift','斯塔克位移'], ['PL','光致发光'], ['e-beam','电子束'],
    ['first-principles','第一性原理'], ['interface-resolved','界面分辨'],
    ['top-interface','上界面'], ['bottom-interface','下界面'], ['scan','扫描'],
    ['intermediate optical response','中间态光学响应'], ['release schematic','解钉示意'],
    ['vdW interface','范德华界面'], ['out-of-plane field','面外电场'],
    ['wall-based driving','基于畴壁的驱动'], ['microscopic origin','微观起源'],
    ['optical response','光学响应'], ['color bar','色标'], ['panel label','子图标签'],
    ['device-level','器件尺度'], ['region size','区域尺寸'],
    ['disorder-sensitive dynamics','无序敏感动力学'], ['velocity collapse','速度标度坍缩'],
    ['critical curve','临界曲线'], ['force contrast','力对比'], ['finite v','有限速度']
  ];

  pairs.sort((a,b) => b[0].length - a[0].length);
  const map = new Map(pairs.map(([term,zh]) => [term.toLowerCase(), zh]));
  const escaped = pairs.map(([term]) => term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const reTerm = new RegExp(`(^|[^A-Za-z0-9])(${escaped.join('|')})(?![A-Za-z0-9]|（)`, 'gi');

  function skip(node) {
    const el = node.parentElement;
    if (!el) return true;
    if (el.closest('script,style,pre,code,.source-text')) return true;
    if (el.matches('.paper h3,.authors,.supporting li,.core-row') || el.closest('.paper h3,.authors,.supporting li,.core-row')) return true;
    return false;
  }

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const node of nodes) {
    if (skip(node) || !/[A-Za-z]/.test(node.nodeValue)) continue;
    node.nodeValue = node.nodeValue.replace(reTerm, (match,prefix,term) => {
      const zh = map.get(term.toLowerCase());
      return zh ? `${prefix}${term}（${zh}）` : match;
    });
  }
})();