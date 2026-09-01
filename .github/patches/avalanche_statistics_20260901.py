from pathlib import Path


def rep(path, old, new):
    p=Path(path); s=p.read_text('utf-8'); n=s.count(old)
    if n != 1:
        raise RuntimeError((path,n,old[:120]))
    p.write_text(s.replace(old,new,1),'utf-8')

# Module 06: distinguish physical avalanche, detected burst, and statistical evidence.
anchor='<div class="bridge">宏观 hysteresis 告诉你 disorder 能制造 criticality，但它还没有回答“墙”本身长什么样。下一篇把 RFIM 初态改成一堵明确的 domain wall，只允许它向前侵入。</div>'
block='''<h2 id="avalanche-statistics">1.5 · Avalanche statistics：先定义 event，再问 power law</h2>
<p>Dahmen–Sethna 的 RFIM 里，avalanche 是准静态增加驱动后，从一个 metastable state 到下一个 metastable state 的集体响应；实验或连续时间模拟里，我们却常从一条 noisy activity trace 用 amplitude threshold、dead time 或 bandwidth “切”出 bursts。<b>这两种 event definition 不是自动等价。</b></p>
<div class="compare"><div class="model"><div class="model-title">Physics-defined avalanche</div><p>驱动 protocol 本身定义 event 边界：一次 infinitesimal / quasistatic drive increment 触发的完整 collective relaxation。适合理论 depinning / RFIM。</p></div><div class="model"><div class="model-title">Detector-defined burst</div><p>从 dP/dt、velocity、current 或 image activity 中按 threshold / gap rule 分段。event 数量、size、duration 都可能随 detector 改变。</p></div></div>
<div class="warn"><b>检测阈值不是无害参数。</b> Ferrero 2021 综述指出，在 depinning avalanche 的实验分析中，有限 detection threshold 甚至可以制造看似存在的 temporal correlations。一个 detector rule 如果能拆分或合并事件，就必须做 threshold / bandwidth sensitivity，而不是只报告最漂亮的一组分布。</div>

<h3>Power law 是 candidate，不是结论</h3>
<div style="font:18px Georgia,serif;text-align:center;padding:14px;background:#faf7f0;border:1px solid var(--l);border-radius:10px;margin:16px 0">P(S) ∼ S<sup>−τ</sup> 𝒢(S/S<sub>c</sub>)</div>
<p>Dahmen &amp; Sethna 1996 的关键提醒是：其模型中真正的 all-size critical power law 出现在 critical disorder；但 critical region 可以很宽，所以离临界点并不很近的数据也可能在有限动态范围里“像”幂律。<b>因此几 decade 的直线本身不能定位 critical point。</b></p>
<div class="claims"><div class="claim"><h3>最低统计要求</h3><p>不要对 log-binned histogram 做普通 least-squares 就宣布 τ。至少明确 lower cutoff、finite-size / detection upper cutoff，用 likelihood-based exponent estimate 与 goodness-of-fit，并比较 plausible alternatives。</p></div><div class="claim"><h3>更强的 universality test</h3><p>如果事件量足够，除了 size / duration exponents，还可测试 size–duration relation、cutoff scaling 与固定 duration 下的 average avalanche shape / scaling function。Papanikolaou 2011 的方法论价值就在于“beyond power laws”。</p></div></div>
<div class="src"><div class="head"><b>统计方法锚点</b>　<span class="rule">Clauset–Shalizi–Newman 2009 · SIAM Review；Papanikolaou et al. 2011 · Nature Physics</span></div><div class="note">Clauset 等强调 least-squares power-law fitting 会产生严重偏差，并推荐 maximum likelihood + goodness-of-fit + model comparison。Papanikolaou 等则用平均 avalanche temporal shape 与 multivariable scaling function，把 universality test 推到单个 exponent 之外。本项目 Drive 当前未检索到这两篇正式 PDF，因此这里使用出版社正式记录的摘要级方法信息。</div></div>

<h3>真正的 n 是什么？先画统计层级</h3>
<div style="overflow-x:auto"><table style="width:100%;min-width:720px;border-collapse:collapse;margin:22px 0;background:#fff;border:1px solid var(--l)"><thead><tr><th style="padding:10px;text-align:left;background:#f0ece3">层级</th><th style="padding:10px;text-align:left;background:#f0ece3">是什么</th><th style="padding:10px;text-align:left;background:#f0ece3">能不能直接当独立 n</th></tr></thead><tbody>
<tr><td style="padding:10px;border-top:1px solid var(--l)">quenched realization / device</td><td style="padding:10px;border-top:1px solid var(--l)">独立 disorder landscape、device 或独立空间 realization</td><td style="padding:10px;border-top:1px solid var(--l)">通常是跨样本 uncertainty 的 outer unit</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">avalanche events</td><td style="padding:10px;border-top:1px solid var(--l)">同一 realization 内按固定 protocol 定义的 events</td><td style="padding:10px;border-top:1px solid var(--l)">可估 conditional event distribution；跨样本推断前先检查相关性/分层</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">time bins / frames / pixels</td><td style="padding:10px;border-top:1px solid var(--l)">一个 event 或 trajectory 的测量采样</td><td style="padding:10px;border-top:1px solid var(--l)"><b>不是</b>新的 avalanche，也不是新的 disorder sample</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">bootstrap draws</td><td style="padding:10px;border-top:1px solid var(--l)">uncertainty 计算产生的 resamples</td><td style="padding:10px;border-top:1px solid var(--l)"><b>绝不是</b>物理 n</td></tr>
</tbody></table></div>
<div class="warn"><b>稳健做法：</b>先在每个 realization 内得到 event-level summary / distribution，再做 leave-one-realization-out 或 block / hierarchical resampling。只有在模型与数据都支持事件近似独立时，才可以把大量 avalanches 直接当 iid event sample；这个假设要写出来。</div>

<div class="q"><b>回到 sliding FE：</b>一条 P–E loop 里的多个 dP/dt peaks、同一次 switching 的多个 frames、或一张图里的多个 active pixels，都不能自动升级成“很多 avalanches”。先固定 event detector，再验证 detector sensitivity、size/duration scaling、finite-size cutoff 和跨 realization 稳健性，最后才谈 avalanche universality。</div>
'''+anchor
rep('modules/disorder-rfim.html',anchor,block)

# Research Track: compact event-analysis contract next to other analysis freedoms.
anchor2='<div class="bridge"><b>预注册不等于僵化。</b>发现新 crossover 后可以升级模型或新增 secondary analysis，但要把它标成 post-hoc，并保留原 primary result。这样“breakdown”才不会被分析自由度悄悄洗掉。</div>'
block2=anchor2+'''\n<h3 id="event-contract">4.6 · Event-statistics contract：burst ≠ avalanche by naming</h3>
<div class="three"><div class="card"><b>Freeze detector</b><p>primary threshold、dead-time / merge rule、bandwidth / sampling rate 在看 exponent 前固定；另外做一组 detector-sensitivity sweep。</p></div><div class="card"><b>Freeze size definition</b><p>明确 S 是 switched area、integrated wall advance、integrated activity 还是 electrical pulse area；不同定义不能混在同一 τ 里。</p></div><div class="card"><b>Preserve hierarchy</b><p>realization → event → frame/bin/pixel。bootstrap draws 只是计算工具，永远不是新的物理样本。</p></div></div>
<table class="matrix"><thead><tr><th>看到的现象</th><th>允许的最低措辞</th><th>升级前还缺什么</th></tr></thead><tbody>
<tr><td>intermittent peaks</td><td>bursty / intermittent switching</td><td>固定 event definition + detector robustness</td></tr>
<tr><td>broad event-size distribution</td><td>broad / heavy-tailed events</td><td>power-law goodness-of-fit + alternatives</td></tr>
<tr><td>candidate power law</td><td>power-law-consistent window</td><td>cutoff / size dependence + duration relation + realization robustness</td></tr>
<tr><td>multiple scaling observables</td><td>candidate avalanche criticality</td><td>critical control parameter / scaling relations / universal shape or function where applicable</td></tr>
</tbody></table>
<div class="warn"><b>Paper-writing rule：</b>“burst concentration” 或 “multiple resistance jumps” 可以是很有价值的 phenomenology；在没有 event-level critical analysis 前，不把它们改名成 RFIM avalanches。<a href="disorder-rfim.html#avalanche-statistics">去 Module 06 看完整统计边界 →</a></div>
'''
rep('modules/research-track.html',anchor2,block2)
