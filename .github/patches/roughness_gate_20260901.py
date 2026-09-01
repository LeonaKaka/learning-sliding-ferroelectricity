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


section = r'''<h2 id="roughness-gate">2.7 · Roughness acceptance gate：ζ 不是从任意 log–log 直线里读出来</h2>
<p>Paruch 的关键动作是先限定 short-scale random-manifold window，再拟合 B(L)。把这个方法搬到 phase-field / depinning simulation 时还要再严格一步：<b>先证明 wall extraction 有效，再区分 UV cutoff、scaling window 与 IR cutoff，并用 real-space、Fourier-space、global-width 三类 estimator 互相检查。</b></p>
<div class="bridge"><b>为什么一个 ζ 不够：</b>generic roughening theory 允许 local、global 与 spectral scaling 分裂；QEW depinning 本身就是重要提醒——其 global depinning roughness 可大于 1，因此不能把同一个 ζ 无条件塞进所有 local correlation functions。若 estimator 分裂，先问 anomalous / super-rough scaling 或 mapping breakdown，而不是先平均成一个数。</div>

<h3>2.7.1 · 三个常用 observable 回答的是不同尺度问题</h3>
<div class="eq">B(r)=⟨[u(y+r)−u(y)]²⟩ ∼ r<sup>2ζ<sub>loc</sub></sup></div>
<div class="eq">S(q)=⟨|u<sub>q</sub>|²⟩ ∼ q<sup>−(1+2ζ<sub>spec</sub>)</sup></div>
<div class="eq">W(L)=√⟨[u(y)−ū]²⟩ ∼ L<sup>ζ<sub>glob</sub></sup></div>
<p>对普通 monoaffine self-affine interface，这些指数在适当 scaling regime 中可以相容；但这是一条<b>待检验的结果</b>，不是定义。尤其当 ζ<sub>glob</sub>&gt;1、存在 anomalous scaling、multiaffinity 或大 overhang 时，local/global/spectral exponent 可能不再相同。</p>
<div class="warn"><b>super-rough 特别警告：</b>短程弹性 QEW depinning 的经典数值结果给出 global ζ≈1.25。此时 local real-space roughness 不应机械拟合成 r<sup>2×1.25</sup>；super-rough scaling 中 local exponent 可受上界/系统尺度影响。先比较 B、S 与 W 的 scaling form，再决定该报告 ζ<sub>loc</sub>、ζ<sub>spec</sub> 还是 ζ<sub>glob</sub>。</div>

<h3>2.7.2 · 先画 scale mask：wall core 以下和 system size 附近都不是免费数据</h3>
<table style="width:100%;border-collapse:collapse;margin:22px 0;background:#fff;border:1px solid var(--l)"><thead><tr><th style="padding:10px;text-align:left;background:#f0ece3">尺度区</th><th style="padding:10px;text-align:left;background:#f0ece3">主要污染</th><th style="padding:10px;text-align:left;background:#f0ece3">处理原则</th></tr></thead><tbody>
<tr><td style="padding:10px;border-top:1px solid var(--l)">UV · r≈dx / wall width</td><td style="padding:10px;border-top:1px solid var(--l)">grid、diffuse-core、contour jitter、插值</td><td style="padding:10px;border-top:1px solid var(--l)">预先屏蔽；dx refinement 后物理下限应稳定</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">candidate scaling window</td><td style="padding:10px;border-top:1px solid var(--l)">可能仍有 crossover</td><td style="padding:10px;border-top:1px solid var(--l)">看 effective slope plateau + estimator cross-check</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">IR · r≈L / few q modes</td><td style="padding:10px;border-top:1px solid var(--l)">finite size、periodicity、detrending、低模数不足</td><td style="padding:10px;border-top:1px solid var(--l)">不把 saturation / lowest modes 强行纳入幂律</td></tr>
</tbody></table>
<p>因此“用了更多点”不一定更可靠。一个跨越 UV crossover、真正 scaling window 与 IR saturation 的长直线，可能只是在 log–log 图上把三种偏差平均了。</p>

<h3>2.7.3 · 用 local effective slope 找 plateau，不用肉眼挑直线</h3>
<div class="eq">ζ<sub>eff</sub><sup>B</sup>(r)=½ d ln B / d ln r　；　ζ<sub>eff</sub><sup>S</sup>(q)=−½[d ln S/d ln q + 1]</div>
<p>primary window 应由预注册 scale mask + effective-slope stability 共同决定。窗口向内/向外移动一档时，ζ 若系统漂移而没有 plateau，就先报告 <b>effective roughness exponent over the tested window</b>，不要升级为 asymptotic ζ。</p>
<div class="readgrid"><div class="readbox"><b>Window sensitivity</b><p>预先定义 nested windows；每个 source 都用同一规则，不按单条曲线挑最好看的区间。</p></div><div class="readbox"><b>Estimator sensitivity</b><p>B(r)、S(q)、W(L) 的适用尺度不同，但应检查它们是否支持同一种 scaling taxonomy。</p></div><div class="readbox"><b>Extraction sensitivity</b><p>轻微改变 contour threshold / interpolation 后 ζ 不应显著跳变；否则还在测 wall core / extraction method。</p></div></div>

<h3>2.7.4 · Detrending 是物理选择，不是“预处理一下”</h3>
<p>若 u(y) 含整体 tilt，可先减去注册好的低阶趋势；但 detrending order 必须固定。过高阶 polynomial 会直接吸收真实 long-wavelength roughness，让 S(q) 的低 q 与 W(L) 人为变平。推荐同时保存 raw u(y) 与 detrended u(y)，并把 detrending rule 写进 estimator receipt。</p>
<div class="warn"><b>不要双重筛选：</b>如果先用 roughness 结果挑 contour / detrending / window，再用同一个 ζ 去“独立验证”β 或 disorder class，这个几何证据已经不再独立。roughness analysis contract 应在看到最终 β / collapse outcome 前冻结。</div>

<h3>2.7.5 · 指数分裂不一定是失败，可能是新的 scaling regime</h3>
<p>出现 ζ<sub>loc</sub>≠ζ<sub>glob</sub>≠ζ<sub>spec</sub> 时，先按 generic anomalous-scaling taxonomy 检查，而不是把三个数平均。若不同阶位移结构函数</p>
<div class="eq">C<sub>n</sub>(r)=⟨|u(y+r)−u(y)|<sup>n</sup>⟩<sup>1/n</sup> ∼ r<sup>ζ<sub>n</sub></sup></div>
<p>还给出系统性的 ζ<sub>n</sub> 分裂，则可能进入 multiaffine / multiscaling 情形。Guyonnet 2012 在 ferroelectric DW 中就观察到：较短尺度可以近似 monoaffine，而更大尺度因局域 disorder variations 出现更复杂的 multiscaling。这个结果应该被当作<b>crossover / defect-structure information</b>，不是“粗糙度拟合坏了”。</p>

<h3>2.7.6 · 统计单元仍然是 quenched source，不是 r-bin、q-mode 或 frame</h3>
<div class="eq">quenched source i → valid wall snapshot / steady ensemble → B<sub>i</sub>(r), S<sub>i</sub>(q), W<sub>i</sub>(L) → ζ<sub>i</sub></div>
<p>同一堵 wall 的很多 r-bin、Fourier modes、trajectory frames 高度相关。它们提高单个 source 的曲线分辨率，却不增加 disorder population 的 outer n。跨 source uncertainty 应在 source level 做 bootstrap / hierarchical summary；若一个 source 在多个 field 或 time 上重复，也应保留配对结构。</p>

<h3>2.7.7 · topology gate 优先于 exponent gate</h3>
<p>如果 contour 出现 persistent overhang、bubble、multiple intersections 或 wall splitting，首先触发的是 <b>single-valued-interface mapping failure</b>。可以研究 hull、cluster morphology、interface density 或 multivalued contour geometry，但不能继续把一个任意投影后的 u(y) exponent 称作 elastic-line ζ。</p>
<table style="width:100%;border-collapse:collapse;margin:22px 0;background:#fff;border:1px solid var(--l)"><thead><tr><th style="padding:10px;text-align:left;background:#f0ece3">等级</th><th style="padding:10px;text-align:left;background:#f0ece3">最低要求</th><th style="padding:10px;text-align:left;background:#f0ece3">允许措辞</th></tr></thead><tbody>
<tr><td style="padding:10px;border-top:1px solid var(--l)">R0 · visual</td><td style="padding:10px;border-top:1px solid var(--l)">一段 log–log 近似直线</td><td style="padding:10px;border-top:1px solid var(--l)">apparent / illustrative roughness</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">R1 · stable window</td><td style="padding:10px;border-top:1px solid var(--l)">UV/IR mask + effective-slope plateau + window sensitivity</td><td style="padding:10px;border-top:1px solid var(--l)">roughness exponent candidate</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">R2 · cross-estimator</td><td style="padding:10px;border-top:1px solid var(--l)">B/S/W 与 extraction/detrending sensitivity 支持同一 scaling taxonomy</td><td style="padding:10px;border-top:1px solid var(--l)">roughness scaling supported over tested scales</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">R3 · cross-observable</td><td style="padding:10px;border-top:1px solid var(--l)">source-level uncertainty + roughness 与独立 v(E)/finite-size evidence 相容，且 mapping gate 存活</td><td style="padding:10px;border-top:1px solid var(--l)">strong universality evidence, not exponent matching alone</td></tr>
</tbody></table>
<div class="q"><b>roughness 验收一句话：</b>如果 ζ 依赖 contour、detrending、UV/IR cutoff 或 fit window，或者 B/S/W 指向不同 scaling taxonomy，就先解释 crossover / anomalous scaling / mapping failure；不要用一条平均直线把差异抹掉。</div>

'''

anchor = '<div class="bridge">Tybell 与 Paruch 把 disorder 变成了<b>统计势景</b>：它能控制 v(E) 和 B(L)。但真实纳米器件里，“pinning centre”到底是不是一个看得见的局域事件？Kim 把统计语言重新落回单个器件。</div>'
insert_once('modules/pinning-creep.html', 'id="roughness-gate"', anchor, section)

# Research Track bridge in the existing zeta analysis-contract row.
rt = Path('modules/research-track.html')
s = rt.read_text('utf-8')
marker = 'id="roughness-gate-bridge"'
if marker not in s:
    old = '<tr><td>ζ</td><td>预定 wall-extraction + scale mask</td><td>contour threshold、W/B/S(q)、detrending</td><td>overhang fraction 高或 local/global/spectral exponent 分裂</td></tr>'
    assert s.count(old) == 1, s.count(old)
    new = old + '\n<tr id="roughness-gate-bridge"><td colspan="4"><b>完整验收链：</b><a href="pinning-creep.html#roughness-gate">Module 04 · UV/IR mask → effective slope → B/S/W → anomalous/multiscaling → source-level uncertainty</a></td></tr>'
    s = s.replace(old, new, 1)
    rt.write_text(s, 'utf-8')

pc = Path('modules/pinning-creep.html').read_text('utf-8')
rtx = Path('modules/research-track.html').read_text('utf-8')
assert pc.count('id="roughness-gate"') == 1
assert rtx.count('id="roughness-gate-bridge"') == 1
assert 'ζ<sub>eff</sub><sup>B</sup>' in pc
assert 'super-rough 特别警告' in pc
assert 'R3 · cross-observable' in pc
assert 'single-valued-interface mapping failure' in pc
assert 'r-bin、Fourier modes、trajectory frames' in pc
for page in (pc, rtx):
    assert not any(ord(ch) < 32 and ch not in '\n\r\t' for ch in page)
print('Roughness acceptance gate validated.')
