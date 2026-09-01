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


section = r'''<h2 id="collapse-gate">6.6 · Collapse acceptance gate：把“看起来叠上了”变成可否证的检验</h2>
<p>finite-size collapse 很有说服力，也因此特别容易被 analysis freedom 滥用。横轴可以移动 f<sub>c</sub>，纵轴可以调 β/ν，横轴尺度还能调 1/ν；如果再自由挑 L、field window 与插值曲线，几乎总能得到一张“更顺”的图。真正的任务不是追求视觉重合，而是<b>提前限制这些自由度，并让没参与优化的数据有机会把 scaling ansatz 否掉。</b></p>
<div class="bridge"><b>方法上的最低共识：</b>data collapse 可以被定义成一个可量化的 optimization / goodness-of-collapse 问题，而不只靠肉眼。对本项目更重要的是在这个思想上再加 held-out size、source-level uncertainty 与 correction-to-scaling 纪律。</div>

<h3>6.6.1 · 先冻结 scaling object，再谈 objective</h3>
<p>例如测试</p>
<div class="eq">v(f,L)L<sup>β/ν</sup> = G[(f−f<sub>c</sub>)L<sup>1/ν</sup>]</div>
<p>在看最终 collapse 前至少冻结：<b>observable 定义、eligible size set、field/reduced-force window family、f<sub>c</sub> authority、interpolation / reference-curve rule、weighting 与 objective</b>。不能先看图，再删掉“最不听话”的 L 或 field points。</p>
<table style="width:100%;border-collapse:collapse;margin:22px 0;background:#fff;border:1px solid var(--l)"><thead><tr><th style="padding:10px;text-align:left;background:#f0ece3">自由度</th><th style="padding:10px;text-align:left;background:#f0ece3">应该怎样约束</th><th style="padding:10px;text-align:left;background:#f0ece3">危险做法</th></tr></thead><tbody>
<tr><td style="padding:10px;border-top:1px solid var(--l)">f<sub>c</sub></td><td style="padding:10px;border-top:1px solid var(--l)">继承独立 threshold authority / uncertainty</td><td style="padding:10px;border-top:1px solid var(--l)">为了 collapse 更漂亮反向调 f<sub>c</sub></td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">size set</td><td style="padding:10px;border-top:1px solid var(--l)">预先定义 core / challenge sizes</td><td style="padding:10px;border-top:1px solid var(--l)">看残差后逐个删 L</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">x-window</td><td style="padding:10px;border-top:1px solid var(--l)">预定 family，并报告 sensitivity</td><td style="padding:10px;border-top:1px solid var(--l)">只保留自然重叠最好的窄区间</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">master curve G</td><td style="padding:10px;border-top:1px solid var(--l)">固定插值/平滑复杂度</td><td style="padding:10px;border-top:1px solid var(--l)">用任意高自由度曲线吸收 size-dependent drift</td></tr>
</tbody></table>

<h3>6.6.2 · objective 必须惩罚“不同 L 在重叠区不一致”</h3>
<p>具体 objective 可以有多种实现；最低要求是它只在各 size 有共同支持的 rescaled-x 区间比较，并按 source-level uncertainty / sampling uncertainty 合理加权。记为 Q<sub>collapse</sub> 即可：</p>
<div class="eq">Q<sub>collapse</sub>(f<sub>c</sub>,β/ν,1/ν) = weighted mismatch of rescaled curves in common support</div>
<p>这里不要把 Q 的数值本身神化。重要的是：<b>同一 objective</b> 必须用于 primary fit、leave-one-size-out、window sensitivity 与 held-out prediction；不能每次换一套“最有利”的评分标准。</p>
<div class="warn"><b>误差传播：</b>如果 f<sub>c</sub> 本身有 source-to-source variation 或 bracket uncertainty，collapse 不能把它当精确常数。至少要在 resampling / sensitivity 中一起传播 f<sub>c</sub> authority；否则 β/ν 与 1/ν 的 CI 会虚假变窄。</div>

<h3>6.6.3 · Leave-one-size-out 的正确问题不是“图还像不像”</h3>
<p>每删掉一个 L，都应<b>重新估计</b>允许估计的 scaling parameters 与 Q<sub>collapse</sub>，再记录：</p>
<div class="check"><div><b>parameter drift：</b>f<sub>c</sub>、β/ν、1/ν 是否在 uncertainty 内稳定？</div><div><b>endpoint leverage：</b>删最小 L 或最大 L 是否造成远大于删中间 L 的跳变？</div><div><b>prediction residual：</b>被删掉的 L 用剩余 sizes 得到的参数重新 rescale 后，是否落在同一 master-curve uncertainty band？</div><div><b>window drift：</b>扩大/收缩 primary reduced-force window 后，结论是否只小幅变化，而不是 exponent 系统漂移？</div></div>
<div class="warn"><b>特别警惕最大尺寸。</b>如果“普适指数”只有加上最大 L 才出现，可能是小尺寸 crossover；如果删掉最大 L 后完全崩溃，也说明当前 size range 还不足以证明 asymptotic regime。两种情况都不是靠一句“finite-size effects”带过。</div>

<h3>6.6.4 · Held-out size prediction 比全数据 collapse 更难作弊</h3>
<p>一个更强的设计是预先留出至少一个 challenge size L<sub>hold</sub>：用 core sizes 冻结 f<sub>c</sub> / exponent ratios / master-curve rule，然后才打开 L<sub>hold</sub>。它不是再做一次 fit，而是问：</p>
<div class="eq">Does L<sub>hold</sub> land on the frozen scaling curve without retuning?</div>
<p>若 held-out size 失败，最有信息量的处理不是立刻重调参数，而是诊断：它显示 correction-to-scaling、crossover length、geometry dependence，还是原 scaling ansatz 本身不适用。</p>

<h3>6.6.5 · Correction-to-scaling 是诊断，不是无限自由度</h3>
<p>若残差随 L 呈系统趋势，可以测试最小 correction，例如</p>
<div class="eq">O(L,f) = L<sup>−x</sup>[G(y) + L<sup>−ω</sup>G<sub>1</sub>(y) + …]　，y=(f−f<sub>c</sub>)L<sup>1/ν</sup></div>
<p>但加入 ω / G<sub>1</sub> 后必须看到<b>可复现的系统改善</b>，并报告主指数对 correction model 的敏感性。若每加一个 correction 参数 exponent 都大幅移动，合理结论是“当前 sizes 仍在 crossover”，不是“终于拟合出了精确 universality class”。</p>

<h3>6.6.6 · 两张图共享数据，就不是两次独立确认</h3>
<p>f<sub>c</sub>(L) shift、critical velocity scaling、full collapse 往往使用同一批 sizes / sources。它们可以形成很强的<b>内部一致性</b>，但不能因为画成三张 panel 就当成三份统计独立证据。真正更独立的 cross-check 来自不同 observable：例如 roughness / structure factor、nonsteady dynamics 或 thermal rounding。</p>
<table style="width:100%;border-collapse:collapse;margin:22px 0;background:#fff;border:1px solid var(--l)"><thead><tr><th style="padding:10px;text-align:left;background:#f0ece3">证据等级</th><th style="padding:10px;text-align:left;background:#f0ece3">最低要求</th><th style="padding:10px;text-align:left;background:#f0ece3">允许的措辞</th></tr></thead><tbody>
<tr><td style="padding:10px;border-top:1px solid var(--l)">C0 · visual</td><td style="padding:10px;border-top:1px solid var(--l)">手工 rescale 后看似重合</td><td style="padding:10px;border-top:1px solid var(--l)">illustrative collapse only</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">C1 · objective</td><td style="padding:10px;border-top:1px solid var(--l)">冻结 objective + uncertainty propagation</td><td style="padding:10px;border-top:1px solid var(--l)">quantitative scaling candidate</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">C2 · robust</td><td style="padding:10px;border-top:1px solid var(--l)">leave-one-size-out + endpoint/window sensitivity survive</td><td style="padding:10px;border-top:1px solid var(--l)">finite-size scaling supported over tested range</td></tr>
<tr><td style="padding:10px;border-top:1px solid var(--l)">C3 · predictive</td><td style="padding:10px;border-top:1px solid var(--l)">held-out size lands without retuning + independent observable cross-check</td><td style="padding:10px;border-top:1px solid var(--l)">strong universality evidence, subject to mapping validity</td></tr>
</tbody></table>
<div class="q"><b>collapse 验收一句话：</b>如果删掉一个尺寸、换一个预注册 window、传播 f<sub>c</sub> uncertainty 或打开 held-out size 后就需要重新“调漂亮”，那张图暂时是 scaling illustration，不是 universality closure。</div>

'''

anchor = '<h2 id="threshold-ladder">6.8 · Threshold inference ladder：先证明 run 有资格，再给 f<sub>c</sub></h2>'
insert_once('modules/depinning.html', 'id="collapse-gate"', anchor, section)

# Add a small Research Track bridge next to its existing collapse analysis contract.
rt = Path('modules/research-track.html')
s = rt.read_text('utf-8')
marker = 'id="collapse-gate-bridge"'
if marker not in s:
    old = '<tr><td>ν / collapse</td><td>固定 size set 与 objective</td><td>leave-one-size-out、端点 L 删除</td><td>collapse 只靠一个 L 或一个自由参数支撑</td></tr>'
    assert s.count(old) == 1
    new = old + '\n<tr id="collapse-gate-bridge"><td colspan="4"><b>完整验收链：</b><a href="depinning.html#collapse-gate">Module 05 · objective → leave-one-size-out → held-out size → correction-to-scaling gate</a></td></tr>'
    s = s.replace(old, new, 1)
    rt.write_text(s, 'utf-8')

# Semantics/integrity.
dep = Path('modules/depinning.html').read_text('utf-8')
rtx = Path('modules/research-track.html').read_text('utf-8')
assert dep.count('id="collapse-gate"') == 1
assert rtx.count('id="collapse-gate-bridge"') == 1
assert 'Does L<sub>hold</sub> land on the frozen scaling curve without retuning?' in dep
assert '两张图共享数据，就不是两次独立确认' in dep
assert 'C3 · predictive' in dep
assert 'f<sub>c</sub> uncertainty' in dep
for page in (dep, rtx):
    assert not any(ord(ch) < 32 and ch not in '\n\r\t' for ch in page)
print('Finite-size collapse acceptance gate validated.')
