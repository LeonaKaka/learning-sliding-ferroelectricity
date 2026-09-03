from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / 'modules/depinning.html'

REPLACEMENTS = (
    ('elastic-界面 language', '弹性界面描述'),
    ('一维 elastic string', '一维弹性线'),
    ('阈值-distribution broadening', '阈值分布展宽'),
)

LOCKED_SCIENCE = (
    'v(f<sub>c</sub>,T) ∼ T<sup>ψ</sup>',
    'v(f,T) = T<sup>ψ</sup> G[(f−f<sub>c</sub>) T<sup>−ψ/β</sup>]',
    '这个数值不是滑移铁电的先验目标',
    'T=0 阈值应先独立闭合',
    '不能从同一批有限温速度数据事后给每个随机种子找最有利的 f<sub>c</sub><sup>(i)</sup>',
    '坍缩应该是待检验结果，不是数据预处理步骤',
    '真正的任务不是追求视觉重合，而是<b>提前限制这些自由度，并让没参与优化的数据有机会把标度假设否掉。</b>',
    '较强的普适性证据，但仍受映射有效性约束',
)

FORBIDDEN_VISIBLE = (
    '热圆滑',
    'elastic-界面 language',
    '一维 elastic string',
    '阈值-distribution broadening',
    'Numerical 模型ing',
    '普适ity',
    'De钉扎',
    ' gate ',
    ' authority ',
    'fit window',
    'sample-specific',
    'held-out',
    'source-level',
)


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    before = BeautifulSoup(raw, 'html.parser')
    sources_before = [str(x) for x in before.select('.source-text')]
    eq_before = [str(x) for x in before.select('.eq')]
    images_before = [(x.get('src'), x.get('alt')) for x in before.find_all('img')]
    hrefs_before = [x.get('href') for x in before.find_all('a')]
    science_counts = {token: raw.count(token) for token in LOCKED_SCIENCE}

    if '热圆滑' not in raw:
        raise RuntimeError('Module 05 expected thermal-rounding residue missing')

    out = raw.replace('热圆滑', '热圆整')
    for old, new in REPLACEMENTS:
        if old not in out:
            raise RuntimeError(f'Module 05 expected mixed-language fragment missing: {old}')
        out = out.replace(old, new, 1)

    after = BeautifulSoup(out, 'html.parser')
    if sources_before != [str(x) for x in after.select('.source-text')]:
        raise RuntimeError('Module 05 paper-original source text changed')
    if eq_before != [str(x) for x in after.select('.eq')]:
        raise RuntimeError('Module 05 equations changed')
    if images_before != [(x.get('src'), x.get('alt')) for x in after.find_all('img')]:
        raise RuntimeError('Module 05 Figure wiring changed')
    if hrefs_before != [x.get('href') for x in after.find_all('a')]:
        raise RuntimeError('Module 05 href wiring changed')
    for token, count in science_counts.items():
        if out.count(token) != count:
            raise RuntimeError(f'Module 05 scientific statement drifted: {token}')

    audit = BeautifulSoup(out, 'html.parser')
    for node in audit.select('.source-text'):
        node.decompose()
    visible = ' '.join(audit.stripped_strings)
    padded = f' {visible} '
    for token in FORBIDDEN_VISIBLE:
        if token in padded or token in visible:
            raise RuntimeError(f'Module 05 final-audit residue remains: {token}')

    required = (
        '6 · 热圆整：',
        '一维弹性线的数值研究',
        '阈值分布展宽',
        '足以支持弹性界面描述',
        'f≈f<sub>c</sub> 测热圆整',
        '这里负责 f≈f<sub>c</sub> 的热圆整',
    )
    for token in required:
        if token not in out:
            raise RuntimeError(f'Module 05 repaired Language V2 text missing: {token}')

    TARGET.write_text(out, encoding='utf-8')
    print('Module 05 thermal-rounding Language V2 repair complete; source text/equations/Figures/links/scientific boundaries unchanged.')


if __name__ == '__main__':
    main()
