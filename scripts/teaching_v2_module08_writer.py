from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'modules/current-frontiers.html'

FIRST = '''
<style>
.frontier-read{margin:24px 0 28px;border:1px solid var(--l);border-radius:13px;background:var(--p);padding:17px 18px}.frontier-read>p{margin:0 0 12px;color:#4f4b45}.frontier-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.frontier-card{border:1px solid var(--l);border-radius:10px;padding:12px;background:#faf7f0}.frontier-card b{display:block;font-family:Georgia,"Songti SC",serif;margin-bottom:4px}.frontier-card small{display:block;color:var(--m);line-height:1.5}.frontier-read .route{margin-top:11px;font-size:12.5px;color:#65615a}.frontier-read .route a{color:#504c46}.claim-check{margin:54px 0 30px;padding-top:28px;border-top:1px solid var(--l)}.claim-check h2{margin:0 0 8px}.claim-check .quiz-intro{margin:0 0 15px;color:#666}.claim-check details{margin:9px 0;border:1px solid var(--l);border-radius:10px;background:var(--p);padding:12px 14px}.claim-check summary{cursor:pointer;font-weight:650}.claim-check details p{margin:10px 0 2px}.claim-check .answer{font-weight:700}@media(max-width:760px){.frontier-grid{grid-template-columns:1fr}}
</style>
<section class="frontier-read" id="first-read">
<p><b>第一次读前沿论文，固定问四个问题：</b>不要按年份背文献，而是判断证据现在停在哪一级。</p>
<div class="frontier-grid">
<div class="frontier-card"><b>① 直接观察了什么？</b><small>先区分空间成像、路径、局域钉扎事件、速度与真正的临界标度；“看见畴壁”不是“测出普适类”。</small></div>
<div class="frontier-card"><b>② 哪部分仍是机制解释？</b><small>作者把现象解释成钉扎、对称性破缺或类雪崩时，要继续问有没有独立可观测量支撑这一层解释。</small></div>
<div class="frontier-card"><b>③ 哪个结果限制了外推？</b><small>Baek 的无预存畴壁翻转、Dai 的耦合多畴壁都提醒：单畴壁最小模型有明确结构边界。</small></div>
<div class="frontier-card"><b>④ 离普适性还缺什么？</b><small>恒场 v(E)、B(r)/S(q)、多个 L、无序定义与跨估计量闭合，缺一串时就不要把机制成熟度写成普适性成熟度。</small></div>
</div>
<div class="route">建议顺序：先读 <a href="#score">证据评分矩阵</a>，再看各篇论文为什么被放在这个层级，最后用 <a href="#missing">缺失证据清单</a> 反推下一步实验 / 数值设计。</div>
</section>
'''

QUIZ = '''
<section class="claim-check" id="claim-check">
<h2>判断自测 · 前沿结果能不能再往前多说一步？</h2>
<p class="quiz-intro">先判断“对 / 错”，再展开答案。四题都训练同一件事：不要把机制证据自动升级成普适性结论。</p>
<details><summary>1 · Chen 2026 在 KPFM 中直接看到畴壁被封闭小畴 / 粗糙边缘钉扎并在更高偏置下越过，因此已经足够提取退钉扎临界指数 β。</summary><p><span class="answer">答案：错。</span> 这组图可以强有力地支持局域钉扎 / 退钉扎事件，但它没有连续恒场下的稳态 v(E)、独立阈值定义、多尺寸和无序样本，所以不能从离散偏置后的空间状态直接升级到 β。</p></details>
<details><summary>2 · Ke 2025 的洁净畴壁超润滑 / 极低运动势垒，与“淬火无序下存在临界退钉扎”是同一个物理命题。</summary><p><span class="answer">答案：错。</span> 前者主要约束洁净畴壁受力与迁移率上限，后者要求随机钉扎景观、阈值与临界标度。洁净极限非常重要，但不能替代无序退钉扎证据。</p></details>
<details><summary>3 · Baek 的完全公度单畴样品可以在没有预存畴壁 / AA 网络时翻转，因此“畴壁介导翻转”在所有滑移铁电结构中都被否定了。</summary><p><span class="answer">答案：错。</span> 它否定的是“预存畴壁无条件必要”这种过强外推，并给出明确的结构边界；它并不抹去多畴 / 含畴壁样品里已经直接观察到的畴壁介导路径。</p></details>
<details><summary>4 · Liang、Chen、Liu 等结果合在一起，已经很有力地说明真实滑移铁电动力学对畴壁与钉扎景观敏感；但在 v(E)、ζ、β、ν 和有限尺寸标度尚未闭合前，仍不应宣布一个确定的退钉扎普适类。</summary><p><span class="answer">答案：对。</span> 这正是本章的证据成熟度结论：机制链已经很强，普适性链仍缺关键可观测量。下一步不是再找一句“有钉扎”，而是把同一系统中的动力学、几何和有限尺寸标度闭合起来。</p></details>
</section>
'''


def protected(raw: str) -> dict[str, list[str | None]]:
    doc = BeautifulSoup(raw, 'html.parser')
    return {
        'source': [str(x) for x in doc.select('.source-text')],
        'fig': [str(x) for x in doc.find_all('figure')],
        'src': [x.get('src') for x in doc.find_all('img')],
        'pre': [str(x) for x in doc.find_all('pre')],
        'code': [str(x) for x in doc.find_all('code')],
    }


def main() -> None:
    raw = PAGE.read_text(encoding='utf-8')
    if 'id="first-read"' in raw or 'id="claim-check"' in raw:
        raise RuntimeError('Module 08 Teaching V2 layer already exists')
    before = protected(raw)

    first_marker = '<p class="rule">本章只使用项目 Drive 中的 2025–2026 主线论文'
    first_pos = raw.find(first_marker)
    if first_pos < 0:
        raise RuntimeError('Module 08 core-source rule marker missing')
    out = raw[:first_pos] + FIRST + '\n' + raw[first_pos:]

    nav_marker = '<div class="next">'
    nav_pos = out.rfind(nav_marker)
    if nav_pos < 0:
        raise RuntimeError('Module 08 final navigation marker missing')
    out = out[:nav_pos] + QUIZ + '\n' + out[nav_pos:]

    if protected(out) != before:
        raise RuntimeError('Module 08 Teaching V2 insertion changed protected source/figure/code content')

    doc = BeautifulSoup(out, 'html.parser')
    first = doc.find('section', id='first-read')
    quiz = doc.find('section', id='claim-check')
    if first is None or len(first.select('.frontier-card')) != 4:
        raise RuntimeError('Module 08 first-read structure invalid')
    if quiz is None or len(quiz.find_all('details', recursive=False)) != 4:
        raise RuntimeError('Module 08 claim-check structure invalid')
    if quiz.find_next_sibling('div', class_='next') is None:
        raise RuntimeError('Module 08 claim-check not immediately before final navigation')

    ids = {x.get('id') for x in doc.find_all(id=True)}
    for href in ('#score', '#missing'):
        if href[1:] not in ids:
            raise RuntimeError(f'Module 08 first-read target missing: {href}')

    for anchor in (
        '“看见畴壁”不是“测出普适类”',
        '机制成熟度写成普适性成熟度',
        '不能从离散偏置后的空间状态直接升级到 β',
        '不能替代无序退钉扎证据',
        '否定的是“预存畴壁无条件必要”这种过强外推',
        '机制链已经很强，普适性链仍缺关键可观测量',
    ):
        if anchor not in out:
            raise RuntimeError(f'Module 08 Teaching V2 boundary missing: {anchor}')

    PAGE.write_text(out, encoding='utf-8')
    print('MODULE 08 TEACHING V2 PASS: 4-question first-read frame + 4 evidence-maturity claim checks inserted; paper evidence unchanged.')


if __name__ == '__main__':
    main()
