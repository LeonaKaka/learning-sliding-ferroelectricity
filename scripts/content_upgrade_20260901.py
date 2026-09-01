from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def replace_once(path, old, new):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise RuntimeError(f'anchor missing in {path}: {old[:100]}')
    if s.count(old) != 1:
        raise RuntimeError(f'anchor not unique in {path}: {s.count(old)}')
    p.write_text(s.replace(old, new, 1), encoding='utf-8')

# Module 02: multilayer coupled-interface boundary from Dai 2026.
replace_once(
    'modules/switching-pathways.html',
    '<h2>把三篇压成一张物理图</h2>',
    '''<h2>4 · Dai 2026：trilayer 不只是“两个独立 interface”，DW 之间还会互相作用</h2>\n<p>Liang 已经告诉我们两个 interface 的解钉顺序会生成不同 intermediate state。Dai 等在 trilayer γ-InSe 上把这个问题继续推进到 atomistic dynamics：相邻层的 DW 可以出现在不同位置，中间夹着 nonpolar domain；外场下 switching 分成不同 kinetic stages，而且多个 DW 的 collective motion 显示显著的 inter-DW interaction。</p>\n<div class="src"><div class="head"><b>最新补充 · Dai et al. 2026</b>　<span class="rule">npj Computational Materials · published 2026-08-29 · open-access publisher text</span></div><div class="note"><b>来源层级：</b>项目 Drive 当前未检索到这篇刚发表论文，因此这里只使用 Nature Portfolio 正式页面的摘要级事实，不复制尚未进入项目文献库的 Figure。核心结果是：multiple sliding interfaces → distinct-location DWs + nonpolar intermediate domains + staged switching + inter-DW interaction。</div></div>\n<div style="font-family:Georgia,'Times New Roman',serif;font-size:18px;text-align:center;padding:15px;margin:20px 0;background:#faf7f0;border:1px solid var(--l);border-radius:10px">bilayer-like:　u(y,t)<br><b>trilayer minimal extension:</b>　u<sub>1</sub>(y,t), u<sub>2</sub>(y,t) + F<sub>int</sub>[u<sub>1</sub>−u<sub>2</sub>]</div>\n<div class="claims"><div class="claim"><h3>为什么这对 pathway 很重要</h3><p>intermediate state 不再只是“某个 interface 先动”的静态标签；两个 wall 的相对位置与相互作用本身会进入动力学，阶段式 switching 可以是 coupled-interface system 的自然结果。</p></div><div class="claim"><h3>为什么这对后面的模型很重要</h3><p>单一 elastic line u(y) 是刻意选择的 minimal problem，不是 multilayer sliding FE 的终极 coarse graining。若目标转向 trilayer/multilayer，至少要检查 coupled-interface degrees of freedom 是否不可忽略。</p></div></div>\n\n<h2>把四篇压成一张物理图</h2>''')
replace_once(
    'modules/switching-pathways.html',
    '<div class="paths"><div class="pathbox"><b>Yang 2024</b><p>单界面器件：已有 DW 被局域 pinning centre 困住；超过局域阈值后 release，并扫过大区域。</p></div><div class="pathbox"><b>Sui 2024</b><p>原子尺度：相邻层真的发生有限位移；不同 metastable stacking 使多条结构路径竞争。</p></div><div class="pathbox"><b>Liang 2025</b><p>多界面器件：每个 interface 有自己的 DW/pinning；解钉顺序直接生成不同 intermediate state。</p></div></div>',
    '<div class="paths"><div class="pathbox"><b>Yang 2024</b><p>单界面器件：已有 DW 被局域 pinning centre 困住；超过局域阈值后 release，并扫过大区域。</p></div><div class="pathbox"><b>Sui 2024</b><p>原子尺度：相邻层真的发生有限位移；不同 metastable stacking 使多条结构路径竞争。</p></div><div class="pathbox"><b>Liang 2025</b><p>多界面器件：每个 interface 有自己的 DW/pinning；解钉顺序直接生成不同 intermediate state。</p></div><div class="pathbox"><b>Dai 2026</b><p>多界面动力学：DW 可位于不同位置并相互作用；nonpolar intermediate region 与 staged switching 成为真正的 dynamic degrees of freedom。</p></div></div>')
replace_once('modules/switching-pathways.html', '.paths{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:28px 0}', '.paths{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:28px 0}')

# Module 07: make the single-interface model boundary explicit.
replace_once(
    'modules/numerical-modeling.html',
    '<h2>4 · Fedeli 2019：disorder 要进入“物理项”，而不是只给结果图加噪声</h2>',
    '''<h2>4 · Dai 2026：什么时候单一 u(y) 不是“近似得粗”，而是自由度真的少了？</h2>\n<p>Caballero 的约化问题默认只有一堵主要 interface。multilayer sliding FE 会出现更直接的失效模式：不是 wall 变得有一点 overhang，而是体系本来就有多个 sliding interfaces。Dai 2026 的 trilayer γ-InSe 计算显示，相邻层的 DW 位于不同位置，中间可以形成 nonpolar domain，外场下又出现 staged motion 与显著 inter-DW interaction。</p>\n<div class="eq">u(y,t)　→　{u<sub>1</sub>(y,t), u<sub>2</sub>(y,t), …}<small>若多个 interface 的相对位移会改变能量和动力学，就还需要 interaction term，例如 F<sub>int</sub>[u<sub>1</sub>−u<sub>2</sub>]；这只是 coarse-grained 结构示意，不是 Dai 论文直接给出的 Hamiltonian。</small></div>\n<div class="twocol"><div class="card"><h3>仍可做 single-wall minimal problem</h3><p>当研究问题明确限定在 bilayer-like、一堵预存 wall、其它界面自由度被冻结时，单一 u(y) 仍是最干净的 universality test。</p></div><div class="card"><h3>不能无条件外推</h3><p>trilayer/multilayer 的 intermediate states、coupled DWs 与 inter-DW interaction 可能引入新的长度和时间尺度；单壁 β/ζ/ν 不能自动描述整个 multilayer switching。</p></div></div>\n<div class="warn"><b>模型边界不是缺点。</b>真正严谨的说法是：先用 single-wall problem 测试最小 driven-interface framework；如果未来扩到 multilayer，就显式增加 interface index，而不是把所有额外自由度藏进一个更大的“noise”。</div>\n\n<h2>5 · Fedeli 2019：disorder 要进入“物理项”，而不是只给结果图加噪声</h2>''')
replace_once('modules/numerical-modeling.html', '<h2 id="grid">5 · 最容易把数值结果做假的地方：dx 改了，disorder 也跟着变</h2>', '<h2 id="grid">6 · 最容易把数值结果做假的地方：dx 改了，disorder 也跟着变</h2>')
replace_once('modules/numerical-modeling.html', '<h2>6 · 一套不会自欺的 depinning 数值实验</h2>', '<h2>7 · 一套不会自欺的 depinning 数值实验</h2>')

# Module 04: method genealogy.
replace_once(
    'modules/pinning-creep.html',
    '.kicker{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);font-weight:700}',
    '.kicker{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);font-weight:700}.genealogy{display:grid;gap:9px;margin:24px 0}.gene{display:grid;grid-template-columns:120px 1fr;gap:16px;background:#fff;border:1px solid var(--l);border-radius:10px;padding:13px 15px}.gene b{font:16px/1.4 Georgia,serif}.gene p{font-size:13px;margin:0}.gene small{display:block;color:var(--m);margin-top:4px}')
replace_once(
    'modules/pinning-creep.html',
    '@media(max-width:760px){.terms,.claims,.readgrid{grid-template-columns:1fr}',
    '@media(max-width:760px){.terms,.claims,.readgrid{grid-template-columns:1fr}.gene{grid-template-columns:1fr}')
replace_once(
    'modules/pinning-creep.html',
    '<div class="q">本章最小判断框架：',
    '''<h2>方法谱系 · 为什么后来不能只拟合一条 creep 直线？</h2>\n<p>把这一章放回历史里，会发现“受驱无序畴壁”的证据标准是逐步长出来的。下面不是把磁畴壁和铁电畴壁说成同一种材料，而是看每一代工作给方法链补了哪一块。</p>\n<div class="genealogy">\n<div class="gene"><b>Lemerle 1998</b><p>磁畴壁实验把低场 <i>v(H)</i> 的 creep 与 wall wandering 放在同一个研究对象上：动力学和几何开始互相约束。<small>PRL 80, 849 · APS official record；当前项目 Drive 未检索到该 PDF。</small></p></div>\n<div class="gene"><b>Tybell 2002</b><p>把 creep 语言带入 ferroelectric DW，而且先用 real-space domain growth 论证后续速度主要对应 lateral wall propagation，而不是持续随机成核。<small>本章 Drive PDF + 原 Figure。</small></p></div>\n<div class="gene"><b>Paruch 2005</b><p>进一步把 creep exponent 与独立 roughness observable 放在一起，尝试用“动力学 + 几何”区分 disorder picture，而不是让一个 μ 独自承担机制判断。<small>本章 Drive PDF + 原 Figure。</small></p></div>\n<div class="gene"><b>Metaxas 2007</b><p>把测量从低场 creep 扩展到完整 velocity–field characteristic，明确区分 creep、过渡区和高场 flow：单一工作点的幂律被放回完整 dynamic regimes。<small>项目 Drive 已有正式 PDF。</small></p></div>\n<div class="gene"><b>Ferrero 2013</b><p>数值层面强调临界附近的长 transient 与 corrections to scaling：effective exponent 可以在有限时间窗口里看起来非常稳定，却不是 asymptotic exponent。<small>下一章用原论文展开。</small></p></div>\n<div class="gene"><b>Jeudy 2016</b><p>再向前一步，比较不同磁性薄膜和宽温区，把 creep 写成跨材料可缩放的 pinning-energy barrier function。真正的“universal”开始要求跨条件 collapse，而不只是某个样品里出现一条直线。<small>PRL 117, 057201 · APS official record。</small></p></div>\n</div>\n<div class="q"><b>方法史留下的规则：</b>先隔离 wall propagation → 测 velocity → 加独立 geometry → 扩 dynamic regime → 检查 transient / finite-size → 最后才谈 universal collapse。你后面设计 sliding-FE depinning 实验，其实是在继承这条证据链。</div>\n\n<div class="q">本章最小判断框架：''')

# Module 05: connect the genealogy and add the Jeudy universality standard.
replace_once(
    'modules/depinning.html',
    '<h2>1 · Chauve 2000：先把 creep、depinning、flow 放进同一张相图</h2>',
    '<div class="bridge"><b>方法谱系接力：</b>Module 04 已经把 Lemerle → Tybell → Paruch → Metaxas 串起来：先把 wall motion 从完整 switching 中隔离，再从 creep 扩到完整 velocity–field regimes。本章继续补上 <b>critical threshold、finite-size、transient corrections 与 scaling relations</b>，而不是重新从一条幂律开始。<a href="pinning-creep.html">回看方法谱系 →</a></div>\n<h2>1 · Chauve 2000：先把 creep、depinning、flow 放进同一张相图</h2>')
replace_once(
    'modules/depinning.html',
    '<div class="bridge">到这里，问题已经从“墙会不会动”变成“哪一种无序与哪一种有效界面理论控制它怎么动”。下一章必须把 disorder 本身拆开：random-bond、random-field 与 RFIM 到底各自意味着什么。</div>',
    '''<h2>5 · Jeudy 2016：比“指数像不像”更强的测试，是跨材料 barrier collapse</h2>\n<p>Jeudy 等比较多种磁性薄膜、宽磁场和温度范围，在 depinning threshold 以下研究完整 thermally activated creep。关键教学点不是把磁性材料的参数搬给 sliding FE，而是看 universality claim 如何升级：先用每个体系自己的 nonuniversal scales 做归一化，再问不同材料是否落到同一个 pinning-energy barrier function。</p>\n<div class="src"><div class="head"><b>补充方法锚点 · Jeudy et al. 2016</b>　<span class="rule">Phys. Rev. Lett. 117, 057201 · APS official record</span></div><div class="note">APS 摘要报告：不同磁性薄膜在宽 field / temperature 区间的 creep motion，可以由一个统一的 energy-barrier function 描述，并指出这一框架应与其它可由 disordered elastic interface 描述的体系相关。这里使用的是官方发表记录的摘要级信息，不把它伪装成本站 Drive 原文块。</div></div>\n<div class="claims"><div class="claim"><h3>为什么它比单个 μ 更强</h3><p>一个 exponent 在有限窗口里相似，可能来自 crossover；跨材料、跨温度、跨 field 的归一化 collapse 同时约束曲线形状和非普适尺度，证据要求更高。</p></div><div class="claim"><h3>对 sliding FE 的正确用法</h3><p>先证明自己的 wall / disorder / temperature regime 足以支持 elastic-interface language，再把 barrier/scaling collapse 当作待检验假说；不能因为 Jeudy 得到 universal function，就预设 sliding FE 必须服从。</p></div></div>\n<div class="bridge">到这里，问题已经从“墙会不会动”变成“哪一种无序与哪一种有效界面理论控制它怎么动”。下一章必须把 disorder 本身拆开：random-bond、random-field 与 RFIM 到底各自意味着什么。</div>''')

# Module 08: keep the frontier audit current with Baek and Dai.
replace_once(
    'modules/current-frontiers.html',
    '<tr><td><b>Liu et al. 2026</b><br>3R-MoS₂ PRL</td><td class="yes">✓</td><td class="yes">✓ dwell time / apparent critical-field variation</td><td class="yes">✓ device-scale Raman maps</td><td class="no">—</td><td class="no">—</td><td class="no">—</td></tr>',
    '<tr><td><b>Liu et al. 2026</b><br>3R-MoS₂ PRL</td><td class="yes">✓</td><td class="yes">✓ dwell time / apparent critical-field variation</td><td class="yes">✓ device-scale Raman maps</td><td class="no">—</td><td class="no">—</td><td class="no">—</td></tr>\n<tr><td><b>Baek et al.</b><br>FC single-domain 3R-TMD</td><td class="partial">DW-free switching：提醒“DW 必要性”有结构条件</td><td class="yes">与 poly-domain DW/AA pinning 作直接结构对照</td><td class="yes">✓ DF-TEM / HAADF-STEM structural verification</td><td class="no">未给 quenched-disorder wall v(E)</td><td class="no">—</td><td class="no">—</td></tr>\n<tr><td><b>Dai et al. 2026</b><br>trilayer γ-InSe theory/MLMD</td><td class="yes">✓ coupled multiple DWs</td><td class="partial">inter-DW interaction / staged pathway，不是 quenched pinning 主线</td><td class="partial">atomistic simulation trajectory</td><td class="partial">displacement–time / velocity dynamics，但不是 critical depinning curve</td><td class="no">—</td><td class="no">—</td></tr>')
replace_once(
    'modules/current-frontiers.html',
    '<div class="verdict"><b>Frontier verdict：</b>“DW-mediated switching + pinning landscape” 已经不是一个松散猜想；它现在有 stacking-resolved、KPFM、Raman imaging、DFT/BEC 与 MD 多条独立证据链。但从“有 pinning / 有临界样 switching”到“属于某个 depinning universality class”，中间仍缺整套定量标度。</div>',
    '<div class="verdict"><b>Frontier verdict：</b>“DW-mediated switching + pinning landscape” 在 poly-domain / wall-containing sliding FE 中已经有 stacking-resolved、KPFM、Raman、DFT/BEC 与 MD 多条证据链；但 Baek 的 fully commensurate single-domain 结果同时说明 <b>pre-existing DW 不是无条件必要条件</b>。Dai 又进一步显示 multilayer 中会出现 multiple interfaces 与 coupled DWs。前沿问题因此不再是“DW 到底重不重要”，而是：<b>哪种结构走哪种 switching channel，以及在 isolated-wall 条件下能否进入受驱无序界面的 universality framework。</b></div>\n<div class="open"><div class="card"><h3>Baek boundary</h3><p>fully commensurate single-domain 3R-TMD 可以在无预存 DW/AA network 的结构里保持 ferroelectric switching；这把 Chen 的 “no DW, no reversal” 从口号改写成需要注明样品结构与条件的机制命题。</p></div><div class="card"><h3>Dai boundary</h3><p>trilayer γ-InSe 的 multiple sliding interfaces 产生 distinct-location DWs、nonpolar intermediate domains 与 inter-DW interaction；单一 u(y) 因此应被理解为最小模型，而不是 multilayer 的自动 coarse graining。</p></div></div>')

print('content upgrade anchors applied successfully')
