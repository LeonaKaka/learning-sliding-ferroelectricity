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


section = r'''<h2 id="identifiability">4.5 · Nondimensionalization & identifiability：参数多，不等于信息多</h2>
<p>一套 continuum model 可以同时写 κ、V<sub>0</sub>、P<sub>0</sub>、Γ、disorder amplitude、correlation length 和 temperature；但一条实验曲线通常不能把它们全部独立决定。真正应该先问的是：<b>某个 observable 约束的是哪个参数，还是只约束某个参数组合？</b> 如果这个问题没回答，所谓“参数拟合得很好”可能只是 non-identifiability。</p>
<div class="q">最重要的校准顺序：<b>先定自由度与 symmetry → 再定 clean statics → 再定 clean dynamics → 再加 disorder → 最后才拿没参与校准的 observable 做验证。</b></div>

<h3>4.5.1 · 先用 clean single-harmonic sector 看清“参数组合”</h3>
<p>对 Research Track 里采用的 periodic stacking 模型，先暂时关掉 drive 与 disorder，并只保留一维、单谐波 clean sector：</p>
<div class="eq">F = ∫ dx [ κ/2 (∂<sub>x</sub>φ)² + V<sub>0</sub>(1 − cos(nφ)) ]</div>
<p>在<b>这个明确 normalization</b> 下，相邻 minima 之间的 sine-Gordon kink 有特征宽度与壁张力：</p>
<div class="eq">ℓ<sub>w</sub> = √[ κ / (n²V<sub>0</sub>) ]　；　γ<sub>w</sub> = 8√(κV<sub>0</sub>) / n</div>
<div class="warn"><b>公式边界：</b>这两式只属于这里写出的 clean、单谐波、local-gradient 模型。真实 sliding-FE stacking landscape 若有方向各向异性、多谐波、非局域 elasticity 或多个 coupled interfaces，应重新对实际 energy landscape 做数值 wall calibration，不能把这两个 prefactor 当材料定律。</div>
<p>这两式立刻暴露 identifiability：只知道 wall width 时，只约束 <b>κ/V<sub>0</sub></b> 的组合；如果还能独立知道 wall tension / wall energy，才有机会在这个简化模型里拆开：</p>
<div class="eq">V<sub>0</sub> = γ<sub>w</sub> / (8ℓ<sub>w</sub>)　；　κ = n²ℓ<sub>w</sub>γ<sub>w</sub> / 8</div>

<h3>4.5.2 · 哪个 observable 能约束什么？</h3>
<table class="matrix"><thead><tr><th>observable / prior</th><th>主要约束</th><th>单独做不到什么</th></tr></thead><tbody>
<tr><td>stacking symmetry / minima 数</td><td>periodicity、允许的 n、order-parameter topology</td><td>不能靠 hysteresis fit 把 symmetry 当自由参数随便调</td></tr>
<tr><td>clean wall width ℓ<sub>w</sub></td><td>gradient stiffness / local barrier 的长度组合</td><td>通常不能单独拆出 κ 与 V<sub>0</sub></td></tr>
<tr><td>clean wall energy / tension γ<sub>w</sub></td><td>√(κV<sub>0</sub>) 类型的能量组合</td><td>没有宽度信息时仍不能唯一决定 κ、V<sub>0</sub></td></tr>
<tr><td>stacking energy landscape / barrier</td><td>local potential 的能量尺度与 harmonic content</td><td>不决定 gradient stiffness κ</td></tr>
<tr><td>polarization amplitude / electrostatic coupling convention</td><td>P<sub>0</sub> 与 electric-drive energy scale</td><td>不能从 coercive field 单独反推出 P<sub>0</sub></td></tr>
<tr><td>clean-wall mobility / relaxation time</td><td>在 statics 已冻结后的 Γ / kinetic scale</td><td>若 κ、V<sub>0</sub> 还漂着，Γ 会与能量尺度互相补偿</td></tr>
<tr><td>P–E loop / coercive scale</td><td>protocol 下多个机制的综合 response</td><td>不能唯一同时识别 κ、V<sub>0</sub>、Γ、σ、ξ<sub>d</sub></td></tr>
<tr><td>disorder morphology + threshold statistics</td><td>在 clean baseline 冻结后的 coupling law、strength、correlation effects</td><td>不能用来补偿一个本来就错误的 clean wall</td></tr>
</tbody></table>

<h3>4.5.3 · 无量纲化的价值，是看见真正控制问题的 ratios</h3>
<p>在上面的单谐波 clean model 中，可以用 ℓ<sub>w</sub> 作为自然长度。于是很多“参数扫描”其实更应该写成 dimensionless ratio：</p>
<table class="matrix"><thead><tr><th>ratio</th><th>物理含义</th><th>数值上要问什么</th></tr></thead><tbody>
<tr><td>dx / ℓ<sub>w</sub></td><td>网格相对 wall core 的解析度</td><td>wall 是否被足够多 grid points 解析</td></tr>
<tr><td>L / ℓ<sub>w</sub></td><td>system size 相对 microscopic wall scale</td><td>finite-size scaling 是否真的离开 wall-core 尺度</td></tr>
<tr><td>ξ<sub>d</sub> / ℓ<sub>w</sub></td><td>disorder correlation length 相对 wall width</td><td>wall 看到的是近白噪声、有限相关 defect，还是 smooth landscape</td></tr>
<tr><td>E P<sub>0</sub> / V<sub>0</sub></td><td>drive coupling 相对 local periodic energy scale</td><td>它只是自然 drive ratio，不自动等于 coercive / depinning field</td></tr>
<tr><td>σ<sub>RF</sub> / V<sub>0</sub> 或 σ<sub>RB</sub> / V<sub>0</sub></td><td>disorder energy scale 相对 clean barrier</td><td>不同 coupling form 仍需 fair matching，不能只比同一个数字 σ</td></tr>
</tbody></table>
<div class="bridge">这正好把两处旧知识接起来：<a href="#grid">Grid sanity</a> 负责“dx 改变时 physical disorder 是否保持不变”；<a href="research-track.html#fair">Research Track fair matching</a> 负责“RF 与 RB 是否在明确物理尺度上可比”。这里补的是更上游的一步：<b>先把 clean energy / length scales 冻结。</b></div>

<h3>4.5.4 · Γ 最好在 statics 冻结以后再校准</h3>
<p>若采用 overdamped TDGL 形式 <span class="eq" style="display:inline-block;padding:2px 7px;margin:0">∂<sub>t</sub>φ = −Γ δF/δφ</span>，那么在这个 normalization 下，clean minimum 附近 local curvature 是 n²V<sub>0</sub>，小扰动的自然局域 relaxation time 满足：</p>
<div class="eq">τ<sub>0</sub> ∼ 1 / (Γ n²V<sub>0</sub>)</div>
<p>这里的重点不是把这个 prefactor 当普适常数，而是说明 <b>Γ 只有在能量尺度冻结后才有独立动力学意义</b>。实际 calibration 更稳妥的做法，是先用 statics 决定 wall profile / energy，再用 clean-wall mobility 或独立 relaxation observable 约束 kinetic scale。</p>

<h3>4.5.5 · calibration 与 validation 必须分开</h3>
<div class="steps"><div class="step"><b>① Structural prior</b><p>由 stacking symmetry / microscopic landscape 决定 order parameter 与 periodicity。</p></div><div class="step"><b>② Clean statics</b><p>用 wall width、wall energy、stacking barrier 等冻结 κ / V<sub>0</sub> 相关组合。</p></div><div class="step"><b>③ Clean dynamics</b><p>再用 mobility / relaxation 约束 Γ，不让 kinetic 参数替 statics 擦屁股。</p></div></div>
<div class="steps"><div class="step"><b>④ Disorder</b><p>在 clean baseline 不动以后，定义 RF/RB coupling、physical amplitude 与 ξ<sub>d</sub>。</p></div><div class="step"><b>⑤ Calibration set</b><p>明确哪些 observables 被用来定参数。</p></div><div class="step"><b>⑥ Holdout validation</b><p>用没参与校准的 morphology、threshold、size/temperature response 检查 model 是否真的预测到新东西。</p></div></div>
<div class="warn"><b>一个常见自欺路径：</b>同时调 κ、V<sub>0</sub>、Γ、σ 让同一条 P–E loop 很像实验，然后再把“loop 拟合得好”当成模型验证。那只是 calibration closure，不是 independent validation。</div>
<div class="q"><b>模型声明至少要补一句：</b>“哪些参数由外部 structural / static / dynamic observable 约束；哪些只在 dimensionless ratio 中可识别；哪些仍是 phenomenological control parameter；最后用什么 holdout observable 验证。”</div>

'''

anchor = '<h2>5 · Fedeli 2019：disorder 要进入“物理项”，而不是只给结果图加噪声</h2>'
insert_once('modules/numerical-modeling.html', 'id="identifiability"', anchor, section)

replace_once(
    'modules/numerical-modeling.html',
    '<a href="#reduction">Model reduction</a> · <a href="#grid">Grid sanity</a>',
    '<a href="#reduction">Model reduction</a> · <a href="#identifiability">Scale</a> · <a href="#grid">Grid sanity</a>',
)

# Research Track bridge from the exact current model-boundary sentence.
rt_anchor = '<div class="warn"><b>建模边界：</b>这个模型的价值是把 “periodic stacking + diffuse wall + quenched disorder + drive” 放在同一最小框架里，用于比较机制与 universality。若结论依赖特定 3R lattice direction、层间 shear tensor、off-diagonal Born effective charge、multilayer interface coupling，就必须回到更细的自由度。</div>'
rt_new = rt_anchor + '\n<div id="identifiability-bridge" class="bridge"><b>参数不是越多越真实：</b>这个 periodic model 写出 κ、V<sub>0</sub>、P<sub>0</sub>、Γ 与 disorder 后，下一步不是一起拟合，而是先问哪些 observable 能独立约束哪些参数组合。<a href="numerical-modeling.html#identifiability">去 Module 07 看 nondimensionalization / identifiability →</a></div>'
replace_once('modules/research-track.html', rt_anchor, rt_new)

# Integrity checks.
nm = Path('modules/numerical-modeling.html').read_text('utf-8')
rt = Path('modules/research-track.html').read_text('utf-8')
assert nm.count('id="identifiability"') == 1
assert nm.count('href="#identifiability"') == 1
assert rt.count('id="identifiability-bridge"') == 1
assert 'ℓ<sub>w</sub> = √[ κ / (n²V<sub>0</sub>) ]' in nm
assert 'γ<sub>w</sub> = 8√(κV<sub>0</sub>) / n' in nm
assert 'wall width 时，只约束 <b>κ/V<sub>0</sub></b>' in nm
assert 'calibration closure，不是 independent validation' in nm
for page in (nm, rt):
    assert not any(ord(ch) < 32 and ch not in '\n\r\t' for ch in page)
print('Parameter identifiability patch validated.')
