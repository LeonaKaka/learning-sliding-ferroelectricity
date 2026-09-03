from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'modules/numerical-modeling.html'

BLOCK = '''
<style>
.claim-check{margin:54px 0 30px;padding-top:28px;border-top:1px solid var(--l)}.claim-check h2{margin:0 0 8px}.claim-check .quiz-intro{margin:0 0 15px;color:#666}.claim-check details{margin:9px 0;border:1px solid var(--l);border-radius:10px;background:var(--p);padding:12px 14px}.claim-check summary{cursor:pointer;font-weight:650}.claim-check details p{margin:10px 0 2px}.claim-check .answer{font-weight:700}
</style>
<section class="claim-check" id="claim-check">
<h2>判断自测 · 数值代码“能跑”以后，物理还对吗？</h2>
<p class="quiz-intro">先判断“对 / 错”，再展开答案。四题都来自本章最容易造成假收敛或假证据的地方。</p>
<details><summary>1 · 二维 δ 相关淬火无序里，把 dx 从 1 改到 0.5，同时保持代码中的每格 σ 不变，仍然是在模拟同一个连续体无序强度 Δ。</summary><p><span class="answer">答案：错。</span> 对这里声明的网格单元平均约定，固定连续体 Δ 时应有 σ<sub>grid</sub> ∝ dx<sup>−1</sup>。若 dx 加密却固定每格 σ，你同时改变了物理无序强度，不能把差异只解释为“网格收敛”。</p></details>
<details><summary>2 · 在常迁移率、加性白热噪声的 TDGL 中，减小 dt 时，方程右端“噪声率”的标准差与每步真正加入 φ 的随机增量标准差具有相反的 dt 标度。</summary><p><span class="answer">答案：对。</span> 噪声率标准差随 dt<sup>−1/2</sup>，每步随机增量随 dt<sup>+1/2</sup>。两种写法等价，但必须选清楚代码里的随机数究竟加在哪里；混用会让所谓温度随 dt 漂移。</p></details>
<details><summary>3 · 固定同一个淬火无序景观，只更换 20 个热噪声随机种子，就得到 20 个独立无序样本，可以直接把它们当作外层统计单元。</summary><p><span class="answer">答案：错。</span> 这些只是同一淬火景观下的热噪声内层重复。它们能更精确估计该景观的有限温响应，却不会自动增加独立无序样本数。</p></details>
<details><summary>4 · 若平均 dP/dt 很稳定，而且一套参数能很好拟合用于校准的 P–E 回线，就已经同时验证了“稳态畴壁速度”和模型的独立预测能力。</summary><p><span class="answer">答案：错。</span> dP/dt 还可能包含体相弛豫、成核和局域呼吸模，并不自动等于畴壁质心速度；而用来调参的 P–E 回线只能说明校准闭合。稳态 v 要从定义清楚的畴壁坐标与稳定时间区间得到，模型验证还需要没参与校准的留出可观测量。</p></details>
</section>
'''


def protected(raw: str) -> dict[str, list[str | None]]:
    doc = BeautifulSoup(raw, 'html.parser')
    return {
        'source': [str(x) for x in doc.select('.source-text')],
        'eq': [str(x) for x in doc.select('.eq')],
        'fig': [str(x) for x in doc.find_all('figure')],
        'hrefs': [x.get('href') for x in doc.find_all('a')],
        'srcs': [x.get('src') for x in doc.find_all('img')],
        'pre': [str(x) for x in doc.find_all('pre')],
        'code': [str(x) for x in doc.find_all('code')],
    }


def main() -> None:
    raw = PAGE.read_text(encoding='utf-8')
    if 'id="claim-check"' in raw:
        raise RuntimeError('Module 07 claim-check already exists')
    before = protected(raw)
    marker = '<div class="next">'
    pos = raw.rfind(marker)
    if pos < 0:
        raise RuntimeError('Module 07 final navigation marker missing')
    out = raw[:pos] + BLOCK + '\n' + raw[pos:]
    if protected(out) != before:
        raise RuntimeError('Module 07 claim-check insertion changed protected evidence/link wiring')

    doc = BeautifulSoup(out, 'html.parser')
    section = doc.find('section', id='claim-check')
    if section is None or len(section.find_all('details', recursive=False)) != 4:
        raise RuntimeError('Module 07 claim-check structure invalid')
    if section.find_next_sibling('div', class_='next') is None:
        raise RuntimeError('Module 07 claim-check not immediately before final navigation')
    for anchor in (
        'σ<sub>grid</sub> ∝ dx<sup>−1</sup>',
        '噪声率标准差随 dt<sup>−1/2</sup>',
        '热噪声内层重复',
        '并不自动等于畴壁质心速度',
        '没参与校准的留出可观测量',
    ):
        if anchor not in out:
            raise RuntimeError(f'Module 07 claim boundary missing: {anchor}')

    PAGE.write_text(out, encoding='utf-8')
    print('MODULE 07 CLAIM CHECK PASS: 4 numerical evidence-to-claim judgments inserted; protected science unchanged.')


if __name__ == '__main__':
    main()
