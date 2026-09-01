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


section = r'''<h2 id="thermal-noise">6.2 · Thermal noise / FDT：温度不是再加一张随机场</h2>
<p>quenched disorder 与 thermal noise 都会在代码里出现 random numbers，但物理角色完全不同：<b>quenched field 在一次 run 内固定；thermal noise 随时间刷新，并且其幅度必须与 mobility、temperature、空间 cell measure 和 timestep 一起满足 fluctuation–dissipation convention。</b></p>
<div class="twocol"><div class="card"><h3>Quenched disorder</h3><p>描述 frozen landscape。一个 realization 生成后整条 trajectory 都使用同一 h(r) / δV(r)。白噪声空间归一化涉及 cell measure，但没有 temporal δ-function。</p></div><div class="card"><h3>Thermal noise</h3><p>描述与 heat bath 相连的快速随机力。white-noise idealization 同时在 space 与 time 上 δ-correlated；改变 dx 或 dt 都会改变离散采样幅度。</p></div></div>

<h3>6.2.1 · 先声明连续方程，再写离散随机数</h3>
<p>对 constant-mobility、additive-noise 的 overdamped TDGL / Model-A convention：</p>
<div class="eq">∂<sub>t</sub>φ(r,t) = −Γ δF/δφ + ξ(r,t)</div>
<div class="eq">⟨ξ(r,t)⟩ = 0　；　⟨ξ(r,t)ξ(r′,t′)⟩ = 2Γ k<sub>B</sub>T δ<sup>(d)</sup>(r−r′) δ(t−t′)</div>
<p>这一定义把 thermal bath 的噪声强度和 dissipative mobility Γ 绑在一起。若模型使用 dimensionless energy / temperature，或 Γ 的定义放在方程另一侧，prefactor 必须跟着该 normalization 重新推导；不要从别人的代码里抄一个 <code>sqrt(T)</code>。</p>
<div class="warn"><b>适用边界：</b>这里讨论 constant Γ + additive Gaussian white noise。若 mobility 依赖 φ、噪声是 multiplicative / colored，或使用不同 stochastic calculus，漂移项与 FDT 关系会改变，不能机械套下面的离散式。</div>

<h3>6.2.2 · derivative noise 与 update noise 的 dt 标度正好相反</h3>
<p>设一个离散 cell 的 measure 为 ΔV（二维有效模型可对应 ΔA，但必须和 F 的积分单位一致），时间步为 Δt。若代码每一步先生成“方程右端的 noise rate” ξ<sub>i</sub><sup>m</sup>：</p>
<div class="eq">Var(ξ<sub>i</sub><sup>m</sup>) = 2Γ k<sub>B</sub>T / (ΔV Δt)</div>
<p>所以 rate amplitude 随 <b>Δt<sup>−1/2</sup></b> 增大；但 Euler update 真正加到 φ 上的是 ξΔt，因此随机 increment 满足：</p>
<div class="eq">Δφ<sub>thermal</sub> = √[2Γ k<sub>B</sub>T Δt / ΔV] · N(0,1)</div>
<p>也就是说 update amplitude 随 <b>Δt<sup>+1/2</sup></b>。这两个写法等价，但不能混用。很多“dt convergence 一改温度就变”的 bug，就是把 derivative amplitude 当 increment amplitude。</p>
<table class="matrix"><thead><tr><th>代码里随机数加在哪里</th><th>正确 white-noise 尺度</th><th>常见错误</th></tr></thead><tbody>
<tr><td>加到 dφ/dt 右端</td><td>std ∝ [ΓT/(ΔVΔt)]<sup>1/2</sup></td><td>dt 改了仍固定同一个 noise-rate std</td></tr>
<tr><td>直接加到每步 Δφ</td><td>std ∝ [ΓTΔt/ΔV]<sup>1/2</sup></td><td>又额外乘一次 dt，或完全不随 dt 变</td></tr>
<tr><td>二维 cell-average</td><td>ΔV → ΔA = dx²（按你的 2D energy convention）</td><td>把 quenched RF 的 1/dx 规则直接当完整 thermal-noise rule</td></tr>
</tbody></table>

<h3>6.2.3 · dx convergence 与 dt convergence 都要保持同一个 T convention</h3>
<div class="check"><div><b>dx test：</b>若 physical coarse-grained free energy 与 temperature convention 固定，cell 变小后 thermal noise rate 的方差会随 1/ΔV 增大；不能固定每格 random amplitude。</div><div><b>dt test：</b>减小 dt 时，noise rate std 应按 dt<sup>−1/2</sup> 调整，或 update std 按 dt<sup>+1/2</sup> 调整；两种实现只选一种。</div><div><b>equilibrium sanity：</b>在 E=0、无 quenched disorder 的简单可控 case 下，先检查 steady fluctuations / distribution 是否随 dt refinement 稳定，再进入 driven problem。</div><div><b>driven sanity：</b>有外场时系统不是 equilibrium，但 thermostat 的 noise–dissipation convention 仍要固定；不能为拟合 creep / rounding 曲线事后改 noise amplitude。</div></div>
<div class="warn"><b>更深一层：</b>continuum white thermal noise 本身含有任意短波 fluctuation，phase-field 又是 coarse-grained theory。因此极端 dx→0 不一定意味着所有 bare parameters 都能原封不动保持；网格 cutoff 与 coarse-graining convention 要写清。这里的首要目标不是追求“随机场逐点收敛”，而是保证目标 observables 在声明的 coarse-grained model 下稳定。</div>

<h3>6.2.4 · thermal seed 仍然只是 inner repeat</h3>
<p>同一个 quenched landscape 下换 20 个 Langevin seeds，可以更精确估计该 landscape 的 finite-T conditional response；它不会自动变成 20 个新的 disorder realizations。统计层级继续沿用 Research Track：</p>
<div class="eq">quenched source i → thermal seeds j → trajectory frames t</div>
<div class="bridge"><a href="research-track.html#temperature">Research Track：finite-T protocol / outer-vs-inner statistics</a>　·　<a href="depinning.html#thermal-rounding">Module 05：thermal rounding measurement logic</a></div>
<div class="q"><b>代码验收一句话：</b>改 dx 或 dt 后，如果你不能明确说明“为了保持同一个 physical T，随机项到底按什么公式重标了”，finite-T exponent 暂时没有解释资格。</div>

'''

insert_once(
    'modules/numerical-modeling.html',
    'id="thermal-noise"',
    '<h2 id="wall-extraction">6.5 · 从 diffuse phase field 提取 u(y)：先证明“这是一堵线”</h2>',
    section,
)

replace_once(
    'modules/numerical-modeling.html',
    '<a href="#grid">Grid sanity</a> · <a href="#run-receipt">Receipts</a>',
    '<a href="#grid">Grid sanity</a> · <a href="#thermal-noise">Thermal</a> · <a href="#run-receipt">Receipts</a>',
)

# Add finite-T numerical bridge to Research Track.
rt_old = '<div class="bridge"><a href="pinning-creep.html#finite-temperature">Module 04：怎么找可测 creep window</a>　·　<a href="depinning.html#thermal-rounding">Module 05：怎么测 thermal rounding / ψ</a></div>'
rt_new = '<div class="bridge"><a href="pinning-creep.html#finite-temperature">Module 04：怎么找可测 creep window</a>　·　<a href="depinning.html#thermal-rounding">Module 05：怎么测 thermal rounding / ψ</a>　·　<a href="numerical-modeling.html#thermal-noise">Module 07：thermal noise / FDT 怎样随 dx、dt 离散</a></div>'
replace_once('modules/research-track.html', rt_old, rt_new)

nm = Path('modules/numerical-modeling.html').read_text('utf-8')
rt = Path('modules/research-track.html').read_text('utf-8')
assert nm.count('id="thermal-noise"') == 1
assert nm.count('href="#thermal-noise"') == 1
assert '2Γ k<sub>B</sub>T / (ΔV Δt)' in nm
assert '2Γ k<sub>B</sub>T Δt / ΔV' in nm
assert 'thermal seed 仍然只是 inner repeat' in nm
assert 'numerical-modeling.html#thermal-noise' in rt
for page in (nm, rt):
    assert not any(ord(ch) < 32 and ch not in '\n\r\t' for ch in page)
print('Thermal noise / FDT patch validated.')
