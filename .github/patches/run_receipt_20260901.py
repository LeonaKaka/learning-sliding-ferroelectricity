from pathlib import Path


def replace_once(path: str, old: str, new: str):
    p=Path(path); s=p.read_text('utf-8')
    if new in s:
        print(f'{path}: replacement already present; no-op')
        return
    assert s.count(old)==1,(path,old,s.count(old))
    p.write_text(s.replace(old,new,1),'utf-8')


def insert_once(path: str, marker: str, anchor: str, addition: str):
    p=Path(path); s=p.read_text('utf-8')
    n=s.count(marker)
    if n==1:
        print(f'{path}: {marker} already present; no-op')
        return
    assert n==0,(path,marker,n)
    assert s.count(anchor)==1,(path,anchor,s.count(anchor))
    p.write_text(s.replace(anchor,addition+anchor,1),'utf-8')

# Repair stable fair-matching anchor in Research Track.
replace_once(
    'modules/research-track.html',
    '<h3>1.1 · 一个适合 sliding-FE 的有效比较语言</h3>',
    '<h3 id="fair">1.1 · 一个适合 sliding-FE 的有效比较语言</h3>'
)

# Add a direct provenance bridge to the Data→Claim contract.
rt_anchor='<div class="bridge"><b>公开边界：</b>这里给的是可复用的 analysis contract，不展示项目未发表数值、内部 campaign label 或当前 gate 状态。真正分析时再把每个 dataset 映射到这张表。</div>'
rt_new='''<div class="bridge"><b>公开边界：</b>这里给的是可复用的 analysis contract，不展示项目未发表数值、内部 campaign label 或当前 gate 状态。真正分析时再把每个 dataset 映射到这张表。上游每个 simulation run 还必须能回答“它到底由哪版代码、哪份 resolved config、哪组随机源与哪种停止状态生成”；<a href="numerical-modeling.html#run-receipt">去 Module 07 看 run receipt / provenance contract →</a></div>'''
replace_once('modules/research-track.html',rt_anchor,rt_new)

# Numerical Modeling: run-level provenance / receipt contract.
receipt='''<h2 id="run-receipt">6.6 · Run receipt / provenance：一张图能不能成为证据，先看它能不能追到 run</h2>
<p>只保存一个 <code>.npz</code>、一张 PNG 或最终 CSV，并不等于结果可复现。真正可审计的链条应该能从 figure / estimator 一路反查到：<b>哪版代码、哪份实际生效的配置、哪组随机源、怎样结束、保存了什么 raw output、又由哪版分析规则压成当前数字。</b> 这份绑定记录就是 run receipt。</p>
<div class="q">最小原则：<b>raw bytes 可恢复 ≠ run 可重算；run 可重算 ≠ estimator 可复核；全部可复核 ≠ 它自动拥有当前 claim authority。</b></div>

<h3>6.6.1 · 一个 simulation run 至少要冻结七层信息</h3>
<div class="check">
<div><b>Code authority</b>：repository / commit 或 source-tree hash；明确 clean / dirty。若运行来自 dirty working tree，应保存 patch / tree hash，并把它标成 dated snapshot，而不是假装属于某个干净 commit。</div>
<div><b>Resolved configuration</b>：保存 defaults、include、CLI override 全部展开后的最终配置。至少包含 geometry、boundary condition、L / N、dx、dt、T、drive protocol、disorder law / strength / correlation、initial condition 与 units。</div>
<div><b>Random identity</b>：把 quenched-disorder seed 与 thermal / stochastic seed 分开记录；需要时同时保存 RNG family / stream convention。一个整数 seed 只有在随机流定义也固定时才真正可复现。</div>
<div><b>Execution environment</b>：solver / integrator、precision、backend、关键 dependency / environment identity。硬件型号通常不是 physics parameter，但 precision、backend 或 library change 若会改变数值路径，就必须可追踪。</div>
<div><b>Stop & QC receipt</b>：为什么停止——converged、hit exposure limit、max steps、numerical failure、manual abort？同时保存 NaN/divergence、residual、wall-topology 等与物理判读直接相关的 QC。</div>
<div><b>Raw-output receipt</b>：原始数组 / trajectory / checkpoint 的路径或 object id、sampling cadence、shape、dtype、units 与 checksum。derived CSV / PNG 应指回 raw parent，而不是成为孤儿证据。</div>
<div><b>Estimator receipt</b>：analysis code/version、输入 run IDs、transient cut、fit window、wall-extraction rule、threshold criterion、censoring rule、bootstrap / resampling unit。最终一个 β 或 ζ 必须能反查这些选择。</div>
</div>

<h3>6.6.2 · 不要用一个 status 字段装下三种完全不同的问题</h3>
<table class="matrix"><thead><tr><th>状态轴</th><th>它回答什么</th><th>例子</th><th>绝不能偷换</th></tr></thead><tbody>
<tr><td><b>execution_status</b></td><td>数值任务是否按实现要求完成</td><td>completed / aborted / numerical-invalid</td><td>numerical-invalid ≠ physically pinned</td></tr>
<tr><td><b>physical_assessment</b></td><td>在注册 protocol 下物理状态能判到哪一级</td><td>resolved-pinned / resolved-moving / bracketed / censored / unresolved / topology-breakdown</td><td>censored ≠ no transition exists</td></tr>
<tr><td><b>analysis_role</b></td><td>这条 run 在推断里扮演什么角色</td><td>primary / sensitivity / holdout / post-hoc diagnostic / excluded-with-reason</td><td>post-hoc diagnostic ≠ preregistered primary evidence</td></tr>
</tbody></table>
<div class="warn"><b>为什么要拆三轴：</b>一个 task 可以数值上完全成功，却因为 observation time 不够而在物理上 unresolved；也可以物理上很清楚，但只属于 sensitivity analysis。把它们都压成 PASS / FAIL，会在后续 population statistics 里把“没有证据”误写成“负证据”。</div>

<h3>6.6.3 · resolved config 比“我记得当时参数是这些”更重要</h3>
<table class="matrix"><thead><tr><th>只保存输入模板</th><th>还不够的原因</th><th>receipt 应保存</th></tr></thead><tbody>
<tr><td><code>base.yaml</code></td><td>可能又 include 其他文件</td><td>fully resolved config + source config lineage</td></tr>
<tr><td>CLI command</td><td>defaults / environment variable 可能隐式改变参数</td><td>resolved values + exact command</td></tr>
<tr><td>seed=17</td><td>不同 RNG / stream split 可产生不同 field</td><td>seed role + RNG convention；必要时保存 disorder-array hash</td></tr>
<tr><td>commit SHA</td><td>运行时可能有未提交修改</td><td>commit + dirty flag + patch/tree hash</td></tr>
<tr><td>“run completed”</td><td>无法知道是 convergence 还是 hit max-time</td><td>stop_reason + registered stopping thresholds + final diagnostics</td></tr>
</tbody></table>

<h3>6.6.4 · receipt 应该沿着分析链继续传递，而不是在 raw run 处断掉</h3>
<div class="steps"><div class="step"><b>Run receipt</b><p>代码、resolved config、RNG、status、raw hashes。</p></div><div class="step"><b>Estimator receipt</b><p>从哪些 runs、用什么 rule / window 得到一个 observable。</p></div><div class="step"><b>Figure / claim map</b><p>panel 指向 estimator 与 independent evidence unit；正文 claim 再指向 panel。</p></div></div>
<div class="eq">source authority → resolved run receipt → raw data → estimator receipt → figure source map → claim</div>
<p>这条链有一个重要但常被忽略的结论：<b>reproducible 不等于 authoritative。</b> 历史 run、exploratory script 或 candidate figure 可以保存得非常完整，但如果它没有通过当前 analysis contract，就应该被保留用于 recovery / context，而不是悄悄升级成当前主结论。</p>
<div class="bridge">这和 Research Track 的 <a href="research-track.html#data-claim-contract">Data → Estimator → Evidence → Claim contract</a> 正好闭合：那里规定“什么能支持什么 claim”，这里规定“每一级证据怎样留下可追溯 receipt”。</div>

'''
insert_once(
    'modules/numerical-modeling.html',
    'id="run-receipt"',
    '<h2>7 · 一套不会自欺的 depinning 数值实验</h2>',
    receipt
)

# Stable top navigation link for the new section.
replace_once(
    'modules/numerical-modeling.html',
    '<a href="#grid">Grid sanity</a></span>',
    '<a href="#grid">Grid sanity</a> · <a href="#run-receipt">Receipts</a></span>'
)

# Strengthen static-site validator: legacy runtimes must be physically absent and new contracts unique.
p=Path('.github/workflows/pages.yml'); s=p.read_text('utf-8')
old="""          if Path('scripts').exists():
              raise SystemExit('legacy evidence-regeneration scripts must not remain in static V1')
          if Path('_bilingual_noop.txt').exists():
              raise SystemExit('temporary bilingual staging marker must not remain')
          print('Static evidence + conservative terminology validation passed.')
"""
new="""          if Path('scripts').exists():
              raise SystemExit('legacy evidence-regeneration scripts must not remain in static V1')
          for legacy_runtime in ('terms-extra.js', 'terms-cleanup.js'):
              if Path(legacy_runtime).exists():
                  raise SystemExit(f'unused legacy terminology runtime must be removed: {legacy_runtime}')
          if Path('_bilingual_noop.txt').exists():
              raise SystemExit('temporary bilingual staging marker must not remain')

          contracts = {
              Path('modules/research-track.html'): ('id=\"fair\"', 'id=\"data-claim-contract\"', 'id=\"event-contract\"'),
              Path('modules/numerical-modeling.html'): ('id=\"run-receipt\"', 'research-track.html#fair'),
              Path('modules/depinning.html'): ('id=\"data-claim-bridge\"',),
          }
          for page, markers in contracts.items():
              text = page.read_text(encoding='utf-8')
              for marker in markers:
                  if text.count(marker) != 1:
                      raise SystemExit(f'{page}: expected exactly one contract marker: {marker}')
          print('Static evidence + conservative terminology validation passed.')
"""
if new not in s:
    assert s.count(old)==1,s.count(old)
    p.write_text(s.replace(old,new,1),'utf-8')

# Final assertions, including the previously broken fragment.
rt=Path('modules/research-track.html').read_text('utf-8')
nm=Path('modules/numerical-modeling.html').read_text('utf-8')
assert rt.count('id="fair"')==1
assert rt.count('id="data-claim-contract"')==1
assert nm.count('id="run-receipt"')==1
assert nm.count('research-track.html#fair')==1
assert 'numerical-invalid ≠ physically pinned' in nm
assert 'reproducible 不等于 authoritative' in nm
print('Run receipt + anchor repair patch validated.')
