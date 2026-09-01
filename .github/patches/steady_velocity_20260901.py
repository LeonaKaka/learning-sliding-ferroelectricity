from pathlib import Path


def insert_once(path: str, marker: str, anchor: str, addition: str):
    p = Path(path)
    s = p.read_text('utf-8')
    n = s.count(marker)
    if n == 1:
        print(f'{path}: {marker} already present; no-op')
        return
    assert n == 0, (path, marker, n)
    assert s.count(anchor) == 1, (path, anchor, s.count(anchor))
    p.write_text(s.replace(anchor, addition + anchor, 1), 'utf-8')


def replace_once(path: str, old: str, new: str):
    p = Path(path)
    s = p.read_text('utf-8')
    if new in s:
        print(f'{path}: replacement already present; no-op')
        return
    assert s.count(old) == 1, (path, old, s.count(old))
    p.write_text(s.replace(old, new, 1), 'utf-8')


section = r'''<h2 id="velocity-estimator">6.3 · Steady-wall velocity contract：一个 v(E) 点到底怎样才算“测到了”？</h2>
<p>depinning 最常见的下一步是画 <i>v</i>(E)，但“trajectory 最后动了一点”并不等于得到 steady velocity。尤其靠近 E<sub>c</sub> 时，长 transient、intermittent bursts、有限 observation time 与 wall-topology change 都会把一个单点速度变成分析自由度。这里把 <b>run 是否有效、wall 怎样位移、什么时候进入 steady window、单条 trajectory 的误差和跨 disorder source 的误差</b> 分开。</p>
<div class="bridge"><b>为什么要这么严格：</b>Module 05 的 Ferrero 2013 已经显示，depinning 附近可以存在很长的 nonsteady crossover；过早把 transient 当 asymptotic regime，会系统性偏置 effective exponent。steady-v route 与 nonsteady-relaxation route 都可以研究 criticality，但不能把两套 estimator 混在同一条 β fit 里。</div>

<h3>6.3.1 · 先定义一个可 unwarp 的 wall coordinate</h3>
<p>如果 wall extraction gate 已经通过，可以先把单值 wall 写成 u(y,t)，再定义 center-of-mass coordinate：</p>
<div class="eq">X(t) = ⟨u(y,t)⟩<sub>y</sub>　；　v = dX/dt</div>
<p>若驱动方向使用 periodic boundary，X(t) 必须先做 <b>unwrapping</b>；否则 wall 穿过边界时，坐标会从 L 跳回 0，一条真实匀速轨迹会被错误地拟合成巨大反向速度。若体系包含两堵对称 wall，则必须预先规定测哪一堵、还是测 wall separation；不能在分析时按“哪条更漂亮”选择。</p>
<div class="warn"><b>不要用错误的 surrogate：</b>平均 |∂φ/∂t|、总 switching activity、dP/dt 可以很有用，但它们不是自动等于 wall center-of-mass velocity。bulk relaxation、局域 breathing、nucleation 都可能贡献这些量。</div>

<h3>6.3.2 · steady window 必须由稳定性判据产生，不是肉眼裁一段直线</h3>
<p>对每个 constant-E run，先保留完整 X(t)，再注册一族 nested candidate windows。例如固定终点 t<sub>2</sub>，逐步增加 transient cut t<sub>1</sub>，对每个窗口拟合：</p>
<div class="eq">X(t) = X<sub>0</sub> + v t　，t ∈ [t<sub>1</sub>, t<sub>2</sub>]</div>
<table class="matrix"><thead><tr><th>检查</th><th>通过意味着什么</th><th>失败时怎么处理</th></tr></thead><tbody>
<tr><td>window stability</td><td>继续向后移动 t<sub>1</sub> 时 v 不再系统漂移</td><td>标记 transient / unresolved，不挑一个最顺的窗口</td></tr>
<tr><td>late-window split</td><td>后半段拆成两个或多个子窗口，局部 slope 相容</td><td>可能有 aging、late burst 或尚未稳态</td></tr>
<tr><td>net displacement</td><td>累计位移明显大于 wall-core / extraction jitter scale</td><td>不能用极小净位移制造“非零速度”</td></tr>
<tr><td>topology gate</td><td>整个测量窗口仍是一堵可追踪的 wall</td><td>bubble / extra wall / persistent overhang 出现时停止 elastic-line velocity claim</td></tr>
</tbody></table>
<div class="warn"><b>窗口长度不是越长越自动正确。</b>靠近 threshold，长等待后突然移动可能是有限温度激活、有限系统一次性 escape，或真正 steady intermittent motion；必须结合 T、boundary、exposure 与重复 source 判断。一个长 run 的很多 time points 仍然只是一个 run，不会把 outer n 变大。</div>

<h3>6.3.3 · 用 slope，还是用总位移 / 总时间？两者要互相复核</h3>
<p>在真正 steady 的长期窗口里，线性回归 slope 与 endpoint estimator</p>
<div class="eq">v<sub>end</sub> = [X(t<sub>2</sub>) − X(t<sub>1</sub>)] / (t<sub>2</sub> − t<sub>1</sub>)</div>
<p>应给出相容结果。二者明显分裂时，通常意味着窗口内仍有 curvature、长停滞或单次 burst 主导。此时不要把 regression 的很小标准误当成“v 很精确”：time samples 强相关，ordinary least-squares pointwise error 不是 disorder uncertainty。</p>

<h3>6.3.4 · 一个 field point 的统计层级</h3>
<div class="eq">quenched source i → constant field E → trajectory X<sub>i,E</sub>(t) → source-level v<sub>i</sub>(E)</div>
<p>如果同一个 quenched source 在多个 E 上重复，得到的是一条 <b>source-specific velocity curve</b>，这些 field points 在统计上相关。真正做 population-level v(E) 或 β inference 时，outer independent unit 仍然是 quenched source；trajectory frames、多个 fit windows、同一 source 的多个 E 都不能各自冒充新的 n。</p>
<div class="twocol"><div class="card"><h3>推荐保存</h3><p>raw/unwrapped X(t)、wall-valid mask、transient cut、candidate-window slopes、final window、endpoint velocity、topology/QC status 与 exposure。</p></div><div class="card"><h3>推荐报告</h3><p>每个 source 的 v<sub>i</sub>(E)，再跨 source 给 summary/CI；β fit 继承冻结的 E<sub>c</sub> authority 与预注册 reduced-force window。</p></div></div>

<h3>6.3.5 · pinned、moving、unresolved 与“v≈0”不是同义词</h3>
<table class="matrix"><thead><tr><th>run outcome</th><th>velocity estimator</th><th>能否进入 β fit</th></tr></thead><tbody>
<tr><td>resolved-moving + steady-window pass</td><td>有资格给 source-level steady v</td><td>满足冻结 fit window 时可以</td></tr>
<tr><td>resolved-pinned under registered exposure</td><td>不是“测得一个精确 v=0”</td><td>用于 threshold/bracket，不作为 log-v power-law 点</td></tr>
<tr><td>late motion / exposure-limited</td><td>unresolved / censored</td><td>不能硬塞成 0 或删掉不提</td></tr>
<tr><td>numerical-invalid</td><td>无物理 velocity estimate</td><td>绝不能当 pinned</td></tr>
<tr><td>topology-breakdown</td><td>原来的 single-wall v 定义失效</td><td>转向 bulk/multidomain observable 或单独 breakdown analysis</td></tr>
</tbody></table>
<div class="bridge"><a href="depinning.html#threshold-ladder">先看 Module 05 的 threshold inference ladder</a>：它负责判定每个 run 有没有资格进入 threshold authority；本节负责 threshold 以上的 run 怎样获得可审计的 steady v。两条链闭合后，β 才真正有输入数据。</div>
<div class="q"><b>steady-v 验收一句话：</b>如果一个 v 点不能回答“wall coordinate 怎么定义、是否 unwrap、丢了多少 transient、换 late window 后 slope 是否稳定、wall topology 是否仍有效、outer independent unit 是谁”，它暂时不该进入 universality fit。</div>

'''

anchor = '<h2 id="wall-extraction">6.5 · 从 diffuse phase field 提取 u(y)：先证明“这是一堵线”</h2>'
insert_once('modules/numerical-modeling.html', 'id="velocity-estimator"', anchor, section)

# Make the Foundations return link statically resolvable without creating a duplicate runtime id.
replace_once(
    'index.html',
    '<div id="moduleList"></div></section>',
    '<div id="foundations" style="scroll-margin-top:76px"></div><div id="moduleList"></div></section>',
)
replace_once(
    'index.html',
    "el.className='module';el.id=m.id;el.innerHTML=",
    "el.className='module';if(m.id!=='foundations')el.id=m.id;el.innerHTML=",
)

# Integrity / semantics checks. Workflow validation is updated separately via the connector.
nm = Path('modules/numerical-modeling.html').read_text('utf-8')
idx = Path('index.html').read_text('utf-8')
assert nm.count('id="velocity-estimator"') == 1
assert 'X(t) = ⟨u(y,t)⟩<sub>y</sub>' in nm
assert 'ordinary least-squares pointwise error 不是 disorder uncertainty' in nm
assert 'resolved-pinned under registered exposure' in nm
assert 'numerical-invalid' in nm and '绝不能当 pinned' in nm
assert idx.count('id="foundations"') == 1
assert "if(m.id!=='foundations')el.id=m.id" in idx
for page in (nm, idx):
    assert not any(ord(ch) < 32 and ch not in '\n\r\t' for ch in page)
print('Steady-velocity + static Foundations anchor patch validated.')
