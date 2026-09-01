from pathlib import Path


def insert_once(path: str, marker: str, anchor: str, addition: str):
    p = Path(path)
    s = p.read_text('utf-8')
    count = s.count(marker)
    if count == 1:
        print(f'{path}: marker already present; no-op')
        return
    assert count == 0, (path, marker, count)
    assert s.count(anchor) == 1, (path, anchor, s.count(anchor))
    p.write_text(s.replace(anchor, addition + anchor, 1), 'utf-8')
    s2 = p.read_text('utf-8')
    assert s2.count(marker) == 1, (path, marker, s2.count(marker))


rt_addition = '''<h3 id="data-claim-contract">4.7 · Data → Estimator → Evidence → Claim：先知道 n 在哪一层</h3>
<p>一条研究结论不是从 raw file 直接跳到 paper sentence。中间至少有四层：<b>data object</b> 是记录到的东西；<b>estimator</b> 把它压成一个可比较的量；<b>evidence unit</b> 决定不确定度和独立样本数；最后才是 <b>claim</b>。最常见的伪精确，来自把这四层混在一起。</p>
<div class="flow"><div><b>Data</b><p>trajectory、field row、frame、endpoint、event、run status。</p></div><div><b>Estimator</b><p>f<sub>c</sub><sup>(i)</sup>、v、β<sub>eff</sub>、ζ、work、event-size statistics。</p></div><div><b>Evidence</b><p>哪些 realization / device / size 真正提供独立信息。</p></div><div><b>Sensitivity</b><p>window、threshold、detector、topology、exposure 改动后是否 survive。</p></div><div><b>Claim</b><p>从 phenomenology 到 candidate criticality，再到 universality。</p></div></div>

<h3>4.7.1 · 同一个文件里有很多 rows，不代表 n 很大</h3>
<table class="matrix"><thead><tr><th>数据对象</th><th>它适合估计什么</th><th>通常的独立层级</th><th>不能偷换成</th></tr></thead><tbody>
<tr><td>time-series rows / field rows</td><td>单个 run 的 trajectory、steady window、crossing / switching time</td><td>属于同一个 run / source 的 repeated observations</td><td>几千个独立 samples</td></tr>
<tr><td>cycles / endpoints</td><td>protocol 内重复性、cycle-level derived observable</td><td>默认 nested in task / device，除非实验设计另有独立随机化</td><td>自动独立的 n</td></tr>
<tr><td>frames / pixels</td><td>morphology、interface geometry、field map</td><td>同一 realization 的空间/时间采样</td><td>独立 disorder realizations</td></tr>
<tr><td>thermal seeds</td><td>给定 quenched landscape 下的 thermal expectation / stochastic spread</td><td>inner repeats nested under one disorder realization</td><td>新的 quenched samples</td></tr>
<tr><td>disorder realizations / devices</td><td>disorder-population inference</td><td>通常是最关键的 independent unit</td><td>由内部 rows 数量放大的 n</td></tr>
<tr><td>system sizes L</td><td>finite-size trend / collapse</td><td>design strata；每个 L 仍需独立 realizations</td><td>“9 个 L = n=9” 的全部统计依据</td></tr>
<tr><td>bootstrap draws</td><td>传播 estimator uncertainty</td><td>计算重采样</td><td>新的物理数据</td></tr>
</tbody></table>
<div class="warn"><b>层级规则：</b>trajectory rows、cycles、frames、pixels、events、endpoints 与 bootstrap draws 都可能非常多，但是否能进入独立 n 取决于生成它们的随机化层级。先画出 <b>realization → run/condition → repeated observation</b> 的树，再决定 CI / test / bootstrap 怎么做。</div>

<h3>4.7.2 · threshold 结果必须保留 failure semantics</h3>
<table class="matrix"><thead><tr><th>run / search 状态</th><th>允许进入的 estimator</th><th>正确解释</th></tr></thead><tbody>
<tr><td>valid pinned + valid moving bracket</td><td>sample-specific f<sub>c</sub><sup>(i)</sup> interval / estimate</td><td>在注册 criterion 与 exposure 下定位了 threshold</td></tr>
<tr><td>valid pinned up to E<sub>max</sub>，仍未见 moving</td><td>lower bound：f<sub>c</sub><sup>(i)</sup> &gt; E<sub>max</sub>（在该 protocol 下）</td><td>right-censored / exposure-limited，不是 infinite threshold</td></tr>
<tr><td>observation time 不足以区分 late motion</td><td>unresolved / censored status</td><td>缺少 exposure，不应硬塞进 pinned 或 moving</td></tr>
<tr><td>solver / certificate / numerical QC 失败</td><td>不进入 physical threshold estimator</td><td>numerical invalid ≠ physical pinned</td></tr>
</tbody></table>
<div class="q"><b>绝不做的事：</b>把 unresolved 样本删掉直到图变漂亮；把未 bracket 的 sample 随便赋成 E<sub>max</sub>；或者把 numerical failure 解释成“墙被钉住”。这些都会直接偏置 population f<sub>c</sub> 与后续 β。</div>

<h3>4.7.3 · estimator 的 authority 要单向传递</h3>
<table class="matrix"><thead><tr><th>目标</th><th>上游 authority</th><th>当前层只允许调什么</th><th>红灯</th></tr></thead><tbody>
<tr><td>β</td><td>独立 T=0 threshold authority</td><td>预注册的 reduced-force / transient window family</td><td>为了让 β 更直而回调 f<sub>c</sub></td></tr>
<tr><td>ζ</td><td>通过 topology / single-valuedness gate 的 wall extraction</td><td>预注册 scale masks + contour sensitivity</td><td>只挑 W、B、S(q) 中最漂亮的一种</td></tr>
<tr><td>ν / collapse</td><td>多 L threshold / velocity estimates</td><td>fixed objective + leave-one-size-out sensitivity</td><td>每次 collapse 都重新自由挑 L 和 f<sub>c</sub></td></tr>
<tr><td>thermal rounding</td><td>冻结的 T=0 f<sub>c</sub> / f<sub>c</sub><sup>(i)</sup></td><td>thermal seeds、T window、rounding observable</td><td>用 finite-T 曲线事后重定 threshold</td></tr>
<tr><td>avalanche statistics</td><td>冻结的 event detector / size definition</td><td>cutoff、alternative-distribution tests、shape checks</td><td>看到 exponent 后再改 merge/dead-time rule</td></tr>
</tbody></table>
<div class="bridge"><b>这叫 authority chain：</b>下游分析可以对上游 uncertainty 做 sensitivity propagation，但不能把上游 estimator 当成隐藏自由参数重新优化。否则同一批数据会被多次“用来证明自己”。</div>

<h3>4.7.4 · claim ladder：失败时知道该退到哪一级</h3>
<table class="matrix"><thead><tr><th>证据层级</th><th>最低要求</th><th>允许的写法</th></tr></thead><tbody>
<tr><td>E0 · raw integrity</td><td>provenance、config、status、units、重复/别名检查</td><td>dataset / run set is auditable</td></tr>
<tr><td>E1 · estimator stability</td><td>criterion / window / detector / extraction sensitivity</td><td>robust threshold-like / morphology / dynamic observable</td></tr>
<tr><td>E2 · population / size evidence</td><td>正确 independent unit、censoring accounting、多 realizations / L</td><td>population separation / finite-size trend / effective exponent</td></tr>
<tr><td>E3 · cross-observable critical evidence</td><td>f<sub>c</sub>、β、ζ、ν/z 中多个独立 observable 相互兼容</td><td>candidate depinning critical regime</td></tr>
<tr><td>E4 · universality / breakdown</td><td>scaling relations、collapse、topology gate、corrections 与替代解释一起 survive</td><td>candidate universality class；或明确 mapping breakdown</td></tr>
</tbody></table>
<div class="warn"><b>Breakdown 不是“没做成”。</b> 如果 β/ζ/ν 无法在同一 authority chain 下相容，或 topology gate 系统失败，正确结果可能就是：该 sliding-FE regime 只能称为 depinning-like / effective-interface crossover，而不是强行给它套 universality label。</div>
<div class="bridge"><b>公开边界：</b>这里给的是可复用的 analysis contract，不展示项目未发表数值、内部 campaign label 或当前 gate 状态。真正分析时再把每个 dataset 映射到这张表。</div>

'''

insert_once(
    'modules/research-track.html',
    'id="data-claim-contract"',
    '<h2>5 · Mechanism falsification：先排掉简单解释，再谈“真正机制”</h2>',
    rt_addition,
)

# Add top-nav anchor once.
p = Path('modules/research-track.html')
s = p.read_text('utf-8')
if 'href="#data-claim-contract"' not in s:
    old = '<a href="#observables">Observables</a></span>'
    assert s.count(old) == 1, s.count(old)
    s = s.replace(old, '<a href="#observables">Observables</a> · <a href="#data-claim-contract">Evidence</a></span>', 1)
    p.write_text(s, 'utf-8')

# M05: one concise bridge into the full contract.
dep_anchor = '<h2>把它变成一个靠谱的数值实验</h2>'
dep_add = '''<div id="data-claim-bridge" class="bridge"><b>在拟合 exponent 之前先冻结数据层级：</b>field rows / frames 不是新的 disorder samples，thermal seeds 要嵌套在 quenched realization 下，未 bracket 的 threshold 要保留为 censored / unresolved，numerical invalid 不能冒充 pinned。<a href="research-track.html#data-claim-contract">看完整 Data → Estimator → Evidence → Claim contract →</a></div>\n'''
insert_once('modules/depinning.html', 'id="data-claim-bridge"', dep_anchor, dep_add)

# Homepage research-track sentence: idempotent editorial update.
p = Path('index.html')
s = p.read_text('utf-8')
new_phrase = 'observable anatomy → analysis/event statistics → data-to-claim contract → mechanism falsification'
if new_phrase not in s:
    old_phrase = 'observable anatomy → mechanism falsification'
    assert s.count(old_phrase) == 1, s.count(old_phrase)
    s = s.replace(old_phrase, new_phrase, 1)
    p.write_text(s, 'utf-8')

# Final idempotency / integrity assertions.
assert Path('modules/research-track.html').read_text('utf-8').count('id="data-claim-contract"') == 1
assert Path('modules/depinning.html').read_text('utf-8').count('id="data-claim-bridge"') == 1
assert Path('index.html').read_text('utf-8').count(new_phrase) == 1
print('Data-to-claim contract patch validated.')
