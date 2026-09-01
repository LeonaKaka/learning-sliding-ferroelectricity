from pathlib import Path

p = Path('modules/depinning.html')
s = p.read_text('utf-8')
marker = 'id="roughness-gate"'
anchor = '<h3>7.3 · finite-size scaling 要做“删尺寸复核”</h3>'

section = r'''<h3 id="roughness-gate">7.2A · Roughness acceptance gate：先分清 global / local / spectral，再谈 ζ</h3>
<p>roughness 最容易出现一种“数值看起来很漂亮、物理却没有闭合”的假成功：在一段 log–log 区间拟合出斜率，就把它命名成 ζ。真正要检验的是<b>同一堵可定义的 wall，在受控尺度窗内，global、local 与 spectral 几何是否遵守同一种 scaling scenario</b>。尤其当 global ζ 接近或超过 1 时，local correlation 的斜率不能机械地当成同一个 ζ。</p>
<div class="bridge"><b>方法学背景：</b>anomalous-roughening 文献区分 standard self-affine、super-rough 与 intrinsic anomalous scaling；ferroic wall 实验也已经显示，小尺度 monoaffine 并不保证跨更大尺度仍保持单一 ζ。这里因此把“测一个 exponent”升级成“判定 scaling scenario”。</div>

<h4>7.2A.1 · Gate 0：先证明 u(y) 仍然是合法对象</h4>
<p>roughness analysis 继承 Module 07 的 wall-extraction contract。每个被纳入分析的 snapshot / source 都要先通过 single-valued-interface gate：无持续 bubble、额外 wall、无法消解的 overhang 或 contour branching；periodic boundary 下还要保证 wall coordinate 已正确 unwrap。</p>
<div class="warn"><b>topology failure 不是“坏数据”。</b>如果 overhang / bubble 在接近 depinning 时系统出现，它可能正是 elastic-line mapping 的 breakdown evidence。正确处理是停止把这些帧塞进单值 u(y) 的 ζ fit，并单独报告 breakdown fraction / morphology，而不是强行投影成一条线。</div>

<h4>7.2A.2 · 三个 observable 回答不同问题</h4>
<table style="width:100%;border-collapse:collapse;margin:22px 0;background:#fff;border:1px solid var(--l)"><thead><tr><th style="padding:10px;text-align:left;background:#f0ece3">observable</th><th style="padding:10px;text-align:left;background:#f0ece3">定义 / scaling</th><th style="padding:10px;text-align:left;background:#f0ece3">主要风险</th></tr></thead><tbody>
<tr><td style="padding:10px;border-top:1px solid var(--l)"><b>global width</b></td><td style="padding:10px;border-top:1px solid var(--l)">W²(L)=⟨[u(y)−ū]²⟩，跨多个 L 测 W∼L<sup>ζ</sup></td><td style="padding:10px;border-top:1px solid var(--l)">size range 太窄；残余 tilt / curvature；只有一个 L 时根本不能给 global ζ</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)"><b>local correlation</b></td><td style="padding:10px;border-top:1px solid var(--l)">B(r)=⟨[u(y+r)−u(y)]²⟩</td><td style="padding:10px;border-top:1px solid var(--l)">UV contour noise、wall width、IR finite-size；super-rough 时 local slope 可与 global ζ 不同</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)"><b>structure factor</b></td><td style="padding:10px;border-top:1px solid var(--l)">S(q)=⟨|ũ(q)|²⟩，1D interface 中常写 S(q)∼q<sup>−(1+2ζ<sub>s</sub>)</sup></td><td style="padding:10px;border-top:1px solid var(--l)">最低 q 被 finite size 控制；最高 q 被 grid / wall-core / extraction filter 控制</td></tr>
</tbody></table>
<div class="warn"><b>关键边界：</b>只有在 standard self-affine scenario 下，global ζ、local ζ<sub>loc</sub> 与 spectral ζ<sub>s</sub> 才应在同一可用尺度范围内相容。若 global ζ&gt;1，常见 super-rough 情形会出现 ζ<sub>loc</sub>≈1，而 global / spectral exponent 仍可大于 1；这时不能把 B(r) 的 local slope 直接报告成 global ζ。</div>

<h4>7.2A.3 · fit window 必须来自物理 cutoff，不是来自“哪段最直”</h4>
<p>对 real-space 与 Fourier-space analysis 都先登记 exclusion rules，再看 exponent：</p>
<div class="checks"><div class="check"><b>UV cutoff</b><p>r 必须明显大于 grid spacing、wall-core width 与 contour-extraction jitter scale；q 必须低于相应的 grid / core cutoff。</p></div><div class="check"><b>IR cutoff</b><p>r 不能逼近 L/2 后才开始“变直”；最低几个 q mode 往往受 finite size、center-of-mass 与 detrending 强烈影响。</p></div><div class="check"><b>effective slope</b><p>画 ζ<sub>eff</sub>(r) 或 spectral local slope。没有跨一段尺度的 plateau，就先报告 crossover / effective exponent。</p></div><div class="check"><b>window family</b><p>用预注册的相邻尺度窗重复拟合；ζ 对端点持续单向漂移时，不把某一个最顺窗口挑成主结果。</p></div></div>

<h4>7.2A.4 · detrending 是必要步骤，但不能偷偷抹掉长波物理</h4>
<p>至少移除整体平移 ū；若几何或 boundary condition 允许全局 tilt，则 tilt-removal rule 要在看 disorder realization 前固定。更高阶 polynomial detrending 会同时删除真实长波 roughness，因此只能作为 sensitivity test，不能为了延长 power-law window 临时提高多项式阶数。</p>
<div class="eq">raw u(y) → registered detrend → W(L), B(r), S(q) → effective-slope / window sensitivity</div>

<h4>7.2A.5 · monoaffine 还是 multiaffine？不要只看二阶相关</h4>
<p>若少数尖锐 kink / localized defects 主导高阶涨落，可以进一步计算</p>
<div class="eq">C<sub>n</sub>(r)=⟨|u(y+r)−u(y)|<sup>n</sup>⟩<sup>1/n</sup> ∼ r<sup>ζ<sub>n</sub></sup></div>
<p>简单 monoaffine interface 期望不同 n 得到相容的 ζ<sub>n</sub>（在误差与同一尺度窗内）；ζ<sub>n</sub> 随 n 系统变化、或 normalized displacement distributions 不 collapse，则应标记 multiscaling / localized-defect contamination candidate。ferroic domain-wall 实验已经说明，这种“大尺度变复杂”可以是真实的 disorder physics，而不只是拟合失败。</p>

<h4>7.2A.6 · independent unit 仍然是 quenched source，不是 q-mode 或 r-bin</h4>
<p>一条 wall 可以产生几十个 r bins 或 Fourier modes，但它们高度相关。推荐保留 source-level curves，再以 quenched source 为 outer resampling unit：bootstrap / jackknife 时整条 source curve 一起重采样；如果同一 source 在多个 field、time 或 size 上被重复使用，相关结构也要保留。</p>
<div class="warn"><b>不要把 mode count 当 n。</b>“S(q) 有 50 个点”不等于 n=50；同理，一个 B(r) curve 的 100 个 r bins 也不是 100 个独立 roughness measurements。</div>

<h4>7.2A.7 · roughness claim ladder</h4>
<table style="width:100%;border-collapse:collapse;margin:22px 0;background:#fff;border:1px solid var(--l)"><thead><tr><th style="padding:10px;text-align:left;background:#f0ece3">等级</th><th style="padding:10px;text-align:left;background:#f0ece3">最低要求</th><th style="padding:10px;text-align:left;background:#f0ece3">允许措辞</th></tr></thead><tbody>
<tr><td style="padding:10px;border-top:1px solid var(--l)">R0 · visual</td><td style="padding:10px;border-top:1px solid var(--l)">wall 看起来粗糙 / 单一 log–log 直线</td><td style="padding:10px;border-top:1px solid var(--l)">rough morphology / illustrative scaling</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">R1 · scale candidate</td><td style="padding:10px;border-top:1px solid var(--l)">合法 u(y) + 物理 cutoff + stable effective-slope window</td><td style="padding:10px;border-top:1px solid var(--l)">effective roughness exponent over tested window</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">R2 · scenario identified</td><td style="padding:10px;border-top:1px solid var(--l)">多个 L；global/local/spectral consistency；source-level uncertainty；window/detrend sensitivity survive</td><td style="padding:10px;border-top:1px solid var(--l)">self-affine / super-rough / anomalous scaling supported over tested scales</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">R3 · universality cross-check</td><td style="padding:10px;border-top:1px solid var(--l)">R2 + independent dynamic scaling / finite-size evidence + mapping validity</td><td style="padding:10px;border-top:1px solid var(--l)">roughness independently supports the proposed depinning universality scenario</td></tr>
</tbody></table>
<div class="q"><b>roughness 验收一句话：</b>如果 ζ 会随着 local/global/spectral estimator、UV/IR cutoff、detrending 或是否保留几个极端 source 而改变物理解释，就先报告 crossover / anomalous candidate；不要平均成一个“最终 ζ”。</div>

'''

if marker in s:
    print('roughness gate already present; no-op')
else:
    assert s.count(anchor) == 1, s.count(anchor)
    p.write_text(s.replace(anchor, section + anchor, 1), 'utf-8')

# Semantic / integrity checks.
s = p.read_text('utf-8')
assert s.count(marker) == 1
for phrase in (
    'super-rough 与 intrinsic anomalous scaling',
    'global ζ、local ζ<sub>loc</sub> 与 spectral ζ<sub>s</sub>',
    '不要把 mode count 当 n',
    'R3 · universality cross-check',
    'roughness 验收一句话',
):
    assert phrase in s, phrase
assert not any(ord(ch) < 32 and ch not in '\n\r\t' for ch in s)
print('Roughness acceptance gate validated.')
