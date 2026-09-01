from pathlib import Path


def insert_once(path: str, marker: str, anchor: str, addition: str):
    p=Path(path); s=p.read_text('utf-8')
    n=s.count(marker)
    if n==1:
        print(f'{path}: {marker} already present; no-op')
        return
    assert n==0,(path,marker,n)
    assert s.count(anchor)==1,(path,anchor,s.count(anchor))
    p.write_text(s.replace(anchor,addition+anchor,1),'utf-8')

addition='''<h3 id="paired-hierarchy">4.8 · Pairing & hierarchical uncertainty：同一 source 内做差，跨 source 才谈 population</h3>
<p>“matched comparison” 不只是在横轴上把两个参数调到同一个数。若 A/B 两个 coupling 能由同一个预先定义的 latent source 生成，<b>paired design</b> 可以先消掉 realization-to-realization 的大波动，再问 coupling law 本身改变了多少。但 pairing 是实验设计，不是事后统计技巧：必须在看 outcome 前定义，而且不能跨本来就不可交换的 evidence strata 强行配对。</p>
<div class="eq">Δ<sub>i</sub> = y<sub>A,i</sub> − y<sub>B,i</sub>　；　\bar{Δ} = N<sup>−1</sup> Σ<sub>i=1</sub><sup>N</sup> Δ<sub>i</sub></div>
<p>这里真正进入 population inference 的基本对象是独立 source <b>i</b> 的 paired contrast Δ<sub>i</sub>，不是 A/B 两边所有 time rows 的总和。</p>

<h3>4.8.1 · pairing 什么时候是公平的？</h3>
<div class="three"><div class="card"><b>Same nuisance source</b><p>两条 condition 共享的是你想消掉的 nuisance variation，例如同一独立 disorder source / device，而不是为了让结果相似才事后挑最接近的 pair。</p></div><div class="card"><b>Frozen mapping</b><p>从 latent source 到 A/B disorder realization 的变换必须预先定义，并保持各自目标 marginal distribution / matching contract；“同 seed”本身不自动等于公平。</p></div><div class="card"><b>Same evidence stratum</b><p>production、holdout、successor、legacy 或不同 protocol 若 authority 不同，就不能只因为能找到共同标签而塞进一张 paired table。</p></div></div>
<div class="warn"><b>common random numbers 是 variance-reduction device，不是物理等价证明。</b> pairing 能让 within-source contrast 更精确，但不能抹掉 A/B coupling 的不同数学结构，也不能替代 fair physical matching。</div>

<h3>4.8.2 · outer sample 与 inner repeat 要分开</h3>
<table class="matrix"><thead><tr><th>层级</th><th>典型对象</th><th>主要用途</th><th>不确定度怎么处理</th></tr></thead><tbody>
<tr><td><b>outer independent unit</b></td><td>独立 disorder realization / independent device</td><td>population inference</td><td>CI / bootstrap / model 的最外层 resampling unit</td></tr>
<tr><td><b>paired condition</b></td><td>同一 source 下 A vs B coupling / protocol</td><td>within-source contrast</td><td>先在 source 内形成 Δ<sub>i</sub>，再跨 i 汇总</td></tr>
<tr><td><b>inner stochastic repeat</b></td><td>固定 quenched landscape 下的 thermal seeds</td><td>估计 conditional thermal expectation / stochastic spread</td><td>先在 i 内平均或做 nested model；不能冒充新 disorder samples</td></tr>
<tr><td><b>repeated observation</b></td><td>time rows、cycles、frames、events</td><td>估计 trajectory / event distribution / morphology</td><td>保留 clustering；不能用 row count 放大 population n</td></tr>
<tr><td><b>bootstrap draw</b></td><td>resampled index sets</td><td>传播 estimator uncertainty</td><td>draw 数量只控制 Monte Carlo precision，不增加物理样本</td></tr>
</tbody></table>

<h3>4.8.3 · finite-T：先在 quenched source 内平均，再跨 source 推断</h3>
<div class="eq">\bar y<sub>i,c</sub> = M<sub>i,c</sub><sup>−1</sup> Σ<sub>j</sub> y<sub>i,c,j</sub>　；　Δ<sub>i</sub> = \bar y<sub>i,A</sub> − \bar y<sub>i,B</sub></div>
<p>其中 i 是 quenched realization，j 是 thermal seed，c 是 condition。若研究问题是“平均 thermal response 在不同 coupling 间是否不同”，最简单的 authority 是先得到每个 i,c 的 conditional estimator，再对 Δ<sub>i</sub> 做 outer-level inference。若 inner stochastic variance 本身也是科学问题，可用 hierarchical / nested bootstrap，但外层独立单位仍然是 i。</p>
<div class="warn"><b>不要把更多 thermal seeds 当成更多 disorder。</b> 增加 inner repeats 会降低给定 landscape 下 thermal mean 的 Monte Carlo noise，却不能凭空增加对 disorder population 的覆盖。</div>

<h3>4.8.4 · missing / censored pair 不能靠“补一个数”恢复完整</h3>
<table class="matrix"><thead><tr><th>情况</th><th>错误处理</th><th>正确方向</th></tr></thead><tbody>
<tr><td>A 有 valid estimate，B 只有 lower bound</td><td>把 B=E<sub>max</sub> 后直接算 Δ</td><td>保留 paired censoring / bound 信息；若主 estimator 不支持，降级为 partial-information analysis</td></tr>
<tr><td>A numerical-invalid，B valid</td><td>把 A 当 pinned 或从 paired sample 静默删除</td><td>记录失配原因；区分 technical missingness 与 physical censoring</td></tr>
<tr><td>某 source 只有一侧通过 topology gate</td><td>只保留“好看”的另一侧 geometry exponent</td><td>该 paired geometry contrast 不成立；保留 breakdown / missingness 本身</td></tr>
<tr><td>多个 outcomes 同时显著</td><td>把每个 contrast 当独立发现</td><td>预定义 primary family，必要时 multiplicity control；同时报告 effect / CI</td></tr>
</tbody></table>

<h3>4.8.5 · finite-size 也有 pairing 陷阱</h3>
<p>为了降噪，有时会让不同 L 使用相关的 disorder construction，例如从同一个大 field crop / restrict 出较小系统。这样做不是禁止的，但会让不同 L 的 estimator 相关；此时“每个 L 一点”不能被当成互相独立的样本。若目标是最简单透明的 finite-size inference，优先让每个 L 有独立 disorder realizations；若有意使用 common-random-number / nested-size design，就把 correlation structure 写进 receipt 和统计模型。</p>
<div class="q"><b>最实用的统计顺序：</b>先决定 independent unit → 再决定哪些 condition 在 unit 内 paired → 再处理 thermal/event/cycle 等 inner repeats → 最后才选择 bootstrap / hierarchical model。反过来先把 CSV 全部堆进统计包，几乎一定会把 n 算错。</div>
<div class="bridge">这节与 <a href="#data-claim-contract">Data → Estimator → Evidence → Claim</a> 是同一件事的统计版本；而每个 outer / inner 身份怎样被保存，则回到 <a href="numerical-modeling.html#run-receipt">Module 07 的 run receipt</a>。</div>

'''
insert_once(
    'modules/research-track.html',
    'id="paired-hierarchy"',
    '<h2>5 · Mechanism falsification：先排掉简单解释，再谈“真正机制”</h2>',
    addition
)

s=Path('modules/research-track.html').read_text('utf-8')
assert s.count('id="paired-hierarchy"')==1
assert 'outer independent unit' in s
assert 'common random numbers 是 variance-reduction device' in s
assert 'paired censoring / bound 信息' in s
assert 'bootstrap draw' in s
print('Paired/hierarchical uncertainty patch validated.')
