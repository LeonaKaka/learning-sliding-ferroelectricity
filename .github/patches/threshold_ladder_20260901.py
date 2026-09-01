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


section = r'''<h2 id="threshold-ladder">6.8 · Threshold inference ladder：先证明 run 有资格，再给 f<sub>c</sub></h2>
<p>在一般 phase-field / diffuse-interface 模型里，threshold 不是“找一个让曲线最直的数”。它是一条逐级建立的证据链：<b>零场初态稳定 → 每个受驱 run 的数值状态有效 → pinned / moving / unresolved 判读有注册标准 → 单个 quenched source 得到 bracket 或 bound → 跨独立 source 做 population inference → 最后才把 threshold authority 交给 β。</b></p>
<div class="bridge"><b>先区分两类问题：</b>对满足特殊数学条件的 convex elastic-manifold Hamiltonian，可以有直接定位有限样本 critical manifold 的专门算法；一般 phase-field 伴随 diffuse wall、可能的 nucleation / overhang / topology change 时，不应借用这种“exact threshold”口吻。这里讨论的是后一类更常见的数值证据链。</div>

<h3>6.8.1 · Gate 0：E=0 自己都站不住，就不要开始 threshold search</h3>
<div class="checks"><div class="check"><b>Initial-state stability</b><p>预先构造的 wall 在零场 relax 后不能继续发生系统性漂移、湮灭或额外成核。否则后面的“低场运动”可能只是初态制备松弛。</p></div><div class="check"><b>Numerical certificate</b><p>残差、NaN / divergence、能量或 solver-specific convergence 指标必须满足预注册 QC。数值上没站稳不能解释成“物理上 pinned”。</p></div><div class="check"><b>Topology sanity</b><p>如果目标 observable 假设一堵单值 wall，零场时就先检查 wall 数量、intersection count 与 detached domains。</p></div><div class="check"><b>Exposure baseline</b><p>零场基线本身要跑到足够长，使后面 field-onset 的 transient window 有可比较的时间尺度。</p></div></div>
<div class="warn"><b>Go / no-go：</b>Gate 0 不过时，最短路线是先修初态、solver 或 wall definition，而不是扩大 field grid。否则二分搜索只会更快地把一个无效问题“收敛”到错误答案。</div>

<h3>6.8.2 · 每个 field run 先分类，再参与搜索</h3>
<table class="matrix"><thead><tr><th>run 状态</th><th>最低证据</th><th>threshold search 中怎么用</th></tr></thead><tbody>
<tr><td><b>resolved-moving</b></td><td>排除 transient 后仍有持续推进；velocity / displacement 判据对合理 window 改动稳定</td><td>可作为 moving upper bracket</td></tr>
<tr><td><b>resolved-pinned under exposure</b></td><td>在注册 observation window 内无持续推进，且数值与 topology QC 均通过</td><td>可作为 pinned lower bracket；措辞仍应带 protocol / exposure 条件</td></tr>
<tr><td><b>unresolved / exposure-limited</b></td><td>late motion 与真正长期静止无法区分</td><td>不能替代 pinned；延长 exposure 或保留 censoring</td></tr>
<tr><td><b>numerical-invalid</b></td><td>solver / certificate / data-integrity QC 失败</td><td>不提供物理方向信息；不能据此缩 bracket</td></tr>
<tr><td><b>topology-breakdown</b></td><td>single-wall mapping 失效，但二维动力学本身可能有效</td><td>不能继续作为 elastic-line threshold sample；转入 breakdown evidence</td></tr>
</tbody></table>
<div class="q"><b>关键措辞：</b>有限时间模拟通常只能支持“在注册 exposure 下 resolved-pinned”，而不是数学意义上的“永远不会动”。越接近临界点，相关时间越长，这个区别越重要。</div>

<h3>6.8.3 · bracket 是区间证据，不是一个神奇小数</h3>
<div class="eq">f<sub>−,i</sub> : valid pinned　&lt;　f<sub>c</sub><sup>(i)</sup>　≤　f<sub>+,i</sub> : valid moving</div>
<p>对独立 quenched source <b>i</b>，最诚实的第一产物通常是一个 bracket。adaptive / binary search 只是决定下一次把算力放在哪里；它不会把中间试过的 field points 变成新的独立样本。</p>
<div class="checks"><div class="check"><b>Bracket invariant</b><p>只有 valid pinned 才能更新下界，只有 valid moving 才能更新上界。unresolved / invalid 不改变 bracket 方向。</p></div><div class="check"><b>Registered tolerance</b><p>搜索停止条件应由预先定义的 bracket width、relative tolerance 或资源上限决定，而不是“看到一个顺眼的 f<sub>c</sub> 就停”。</p></div><div class="check"><b>E<sub>max</sub> still pinned</b><p>若最高注册驱动仍是 valid pinned，只得到 f<sub>c</sub><sup>(i)</sup> &gt; E<sub>max</sub> 的 lower bound；这是 right-censored，不是 infinite threshold。</p></div><div class="check"><b>Invalid in the middle</b><p>中间 field 数值失败时，不应用“更高场应该更容易动”的直觉替代实际 run certificate；先修 numerical validity。</p></div></div>

<h3>6.8.4 · sample-specific threshold 与 population threshold 不是一回事</h3>
<p>quenched disorder 下，每个 realization 都可以有自己的 f<sub>c</sub><sup>(i)</sup> 或 bracket。论文里的 population inference 应来自跨独立 realizations 的分布，而不是把一个 source 内的几十个 field probes 当成 n。</p>
<table class="matrix"><thead><tr><th>对象</th><th>它是什么</th><th>不是什么</th></tr></thead><tbody>
<tr><td>一个 source 的 bracket</td><td>f<sub>c</sub><sup>(i)</sup> 的区间 / bound 信息</td><td>整个 disorder ensemble 的唯一 f<sub>c</sub></td></tr>
<tr><td>多个 source 的 f<sub>c</sub><sup>(i)</sup></td><td>population distribution / paired contrast 的基础</td><td>把所有 adaptive field probes pooled 后的普通回归样本</td></tr>
<tr><td>censored source</td><td>部分 threshold 信息</td><td>应静默删除的“坏样本”</td></tr>
<tr><td>bootstrap resamples</td><td>传播 source-level uncertainty</td><td>新增的 disorder realizations</td></tr>
</tbody></table>
<div class="bridge">如果 A/B 两种 coupling 在同一 latent source 下形成 paired threshold comparison，就继续遵守 <a href="research-track.html#paired-hierarchy">Research Track 的 pairing / censoring hierarchy</a>：先形成 source-level contrast 或 bound，再跨 source 推断。</div>

<h3>6.8.5 · β 只能消费冻结的 threshold authority，不能反过来优化它</h3>
<p>一旦 threshold search / finite-size authority 冻结，下游 velocity analysis 才能定义 reduced drive，例如 <span class="eq">ε = (f − f<sub>c</sub>) / f<sub>c</sub></span>，并检查 <span class="eq">v ∼ ε<sup>β</sup></span> 的稳定 window。最危险的做法是同时自由调整 f<sub>c</sub>、fit window 与 β，直到 log–log 图最直。</p>
<div class="checks"><div class="check"><b>Freeze or propagate</b><p>要么固定独立 threshold estimate，要么把 bracket / f<sub>c</sub> uncertainty 显式传播到 β；不要把 f<sub>c</sub> 当隐藏 fit knob。</p></div><div class="check"><b>Transient gate</b><p>近临界 velocity 的 steady window 必须与早期 transient 分开。长期 crossover 会制造看似稳定的 effective exponent。</p></div><div class="check"><b>Window family</b><p>在预先定义的 reduced-force family 上检查 β 对 fit range 的漂移；报告 corrections / crossover，而不是只留最漂亮窗口。</p></div><div class="check"><b>Cross-observable gate</b><p>β 通过只是 E2/E3 的一部分；ζ、finite-size、ν/z、topology 与 scaling relations 仍需独立闭合。</p></div></div>
<div class="warn"><b>最短科学路线：</b>先让 threshold classifier 可审计，再增加 threshold sources；只有 population threshold 稳定后，才值得把算力投入更密的 near-critical velocity grid。反过来先跑大矩阵，往往只是把 classifier / exposure 的系统误差复制很多遍。</div>

'''

insert_once(
    'modules/depinning.html',
    'id="threshold-ladder"',
    '<h2 id="fit-discipline">7 · Exponent extraction discipline：漂亮直线最容易骗人</h2>',
    section,
)

replace_once(
    'modules/depinning.html',
    '<a href="#scaling">Scaling</a></span>',
    '<a href="#scaling">Scaling</a> · <a href="#threshold-ladder">Threshold</a></span>',
)

# Numerical Modeling: add one direct bridge before run receipts.
nm_bridge = r'''<div id="threshold-authority-bridge" class="bridge"><b>Threshold 不从一张 v(E) 图里“读出来”：</b>先做 E=0 stability / numerical certificate，再把每个 field run 分类为 resolved-moving、resolved-pinned-under-exposure、unresolved、numerical-invalid 或 topology-breakdown；只有有效 pinned / moving 才能缩 bracket。<a href="depinning.html#threshold-ladder">去 Module 05 看完整 threshold inference ladder →</a></div>
'''
insert_once(
    'modules/numerical-modeling.html',
    'id="threshold-authority-bridge"',
    '<h2 id="run-receipt">6.6 · Run receipt / provenance：一张图能不能成为证据，先看它能不能追到 run</h2>',
    nm_bridge,
)

# Final assertions.
dep = Path('modules/depinning.html').read_text('utf-8')
nm = Path('modules/numerical-modeling.html').read_text('utf-8')
assert dep.count('id="threshold-ladder"') == 1
assert dep.count('href="#threshold-ladder"') == 1
assert 'right-censored，不是 infinite threshold' in dep
assert 'numerical-invalid' in dep and '不能据此缩 bracket' in dep
assert 'β 只能消费冻结的 threshold authority' in dep
assert nm.count('id="threshold-authority-bridge"') == 1
assert 'depinning.html#threshold-ladder' in nm
print('Threshold inference ladder patch validated.')
