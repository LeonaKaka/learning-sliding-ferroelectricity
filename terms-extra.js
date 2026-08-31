(() => {
  'use strict';
  const pairs = [
    ['Evidence score','证据评分'], ['What is missing','缺失证据'], ['literature-first field guide','文献优先学习指南'],
    ['device-scale spatial mapping','器件尺度空间映射'], ['device-scale spatial map','器件尺度空间图'],
    ['wall-based driving','基于畴壁的驱动'], ['region-dependent switching','区域依赖翻转'],
    ['continuum disorder strength','连续介质无序强度'], ['disorder-sensitive dynamics','无序敏感动力学'],
    ['symmetry-broken displacement configurations','对称性破缺位移构型'],
    ['intrinsic material constant','内禀材料常数'], ['mechanically segmented regions','机械分区'],
    ['mechanically segmented region','机械分区'], ['ground-state domains','基态畴'], ['ground-state domain','基态畴'],
    ['intermediate optical response','中间态光学响应'], ['collective coordinate','集体坐标'],
    ['continuous and univalued interfaces','连续且单值界面'], ['layer-number dependence','层数依赖'],
    ['lower critical dimension','下临界维度'], ['intrinsic anomalous scaling','内禀反常标度'],
    ['dynamic roughening','动态粗化'], ['short-time dynamics','短时动力学'], ['short-time depinning','短时退钉扎'],
    ['spatial trajectory','空间轨迹'], ['trapping competition','俘获竞争'], ['switched-area plateau','翻转面积平台'],
    ['soliton profile','孤子剖面'], ['pulse width','脉冲宽度'], ['moving criterion','运动判据'],
    ['finite-size dependence','有限尺寸依赖'], ['scaling arguments','标度论证'], ['lattice anisotropy','晶格各向异性'],
    ['charge trap','电荷陷阱'], ['self-similar','自相似'], ['invaded area','侵入区域'],
    ['force–velocity','力–速度'], ['force-velocity','力–速度'], ['constant-field','恒定外场'],
    ['random-bond-like','类随机键'], ['triangular P–E','三角波 P–E'], ['velocity collapse','速度标度坍缩'],
    ['critical curve','临界曲线'], ['force contrast','力对比'], ['finite v','有限速度'],
    ['extraction rule','提取规则'], ['lateral size','横向尺寸'], ['finite size','有限尺寸'],
    ['region size','区域尺寸'], ['device-level','器件尺度'], ['out-of-plane field','面外电场'],
    ['microscopic origin','微观起源'], ['release schematic','解钉示意'], ['vdW interface','范德华界面'],
    ['interface-resolved','界面分辨'], ['top-interface','上界面'], ['bottom-interface','下界面'],
    ['Stark shift','斯塔克位移'], ['first-principles','第一性原理'], ['e-beam','电子束'],
    ['color bar','色标'], ['panel label','子图标签'], ['optical response','光学响应'],
    ['degree of freedom','自由度'], ['potential profile','电势剖面'], ['endpoint criterion','端点判据'],
    ['Peierls potential','佩尔斯势'], ['shear coordinate','剪切坐标'], ['gradient descent','梯度下降'],
    ['time axis','时间轴'], ['vdW assembly','范德华组装'], ['I–E loop','I–E 回线'],
    ['map','图谱'], ['distribution','分布'], ['islands','岛状畴'], ['depin','解钉'], ['continuum','连续介质'],
    ['trajectory','轨迹'], ['saturation','饱和'], ['pause','停滞'], ['panel','子图'], ['hierarchy','层级'],
    ['variability','波动'], ['curve','曲线'], ['variation','变化'], ['verdict','结论'], ['readout','读出'],
    ['statistics','统计'], ['broken configurations','对称性破缺构型'], ['contrast','对比'], ['origin','起源'],
    ['device-scale','器件尺度'], ['stepwise','分步'], ['cutoff','截断'], ['definition','定义'], ['event','事件'],
    ['observations','观测'], ['regimes','状态区间'], ['inset','插图'], ['dimensionality','维数'], ['height','高度'],
    ['description','描述'], ['spins','自旋'], ['arguments','论证'], ['study','研究'], ['correlation','关联'],
    ['background','背景'], ['comparison','对比'], ['conjecture','猜想'], ['bounded','有界'], ['Monte Carlo','蒙特卡洛'],
    ['unit-cell','单胞'], ['PL','光致发光'], ['scan','扫描'], ['tensor','张量'], ['layer','层'], ['object','对象'],
    ['displacement','位移'], ['nucleate','成核'], ['transition','转变'], ['flake','薄片'], ['history','历史依赖'],
    ['segmentation','分区'], ['sites','位点'], ['conversion','转换'], ['reversed P','反向极化'], ['twist','扭转'],
    ['layer-number','层数'], ['initial','初始态'], ['final','终态'], ['rotation','旋转'], ['kinetics','动力学'],
    ['ferroelectricity','铁电性'], ['state','状态'], ['physics','物理'], ['gradient','梯度'], ['raster','栅格图'],
    ['surface','曲面'], ['tests','检验'], ['rule','规则'], ['regions','区域'], ['size','尺寸'], ['like','类似']
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