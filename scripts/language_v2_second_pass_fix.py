from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/numerical-modeling.html"

REPLACEMENTS = (
    ('不能为拟合蠕变 / 热圆滑曲线事后改噪声幅度。', '不能为拟合蠕变 / 热圆整曲线事后改噪声幅度。'),
    ('模块 05：热圆滑测量逻辑', '模块 05：热圆整测量逻辑'),
)

LOCKED_SCIENCE = (
    'std(h<sub>cell</sub>) ∝ dx<sup>−d/2</sup>',
    '二维 d=2：std(h<sub>cell</sub>) ∝ 1/dx',
    'std(δV<sub>cell</sub>) ∝ 1/dx',
    'std(ξ<sub>cell</sub>) ∝ [ΓT/(ΔVΔt)]<sup>1/2</sup>',
    '同一个淬火无序景观下换 20 个 Langevin 随机种子',
    '不能把淬火 RF 的 1/dx 规则直接当完整热噪声规则',
    '墙还能画出来”不等于“墙仍属于单值弹性流形',
    '有效钉扎态 / 运动态才能缩小夹定区间',
)

REQUIRED = (
    '07 Numerical Modeling（数值建模）',
    '知识图谱',
    '热噪声',
    '运行记录',
    '热圆整曲线',
    '模块 05：热圆整测量逻辑',
)

FORBIDDEN_OUTSIDE_SOURCE = (
    '热圆滑', 'Numerical 模型ing',
    ' gate ', ' authority ', 'fit window',
    'sample-specific', 'held-out', 'source-level',
    ' workflow ', ' checkpoint ', ' realization ',
)


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    before = BeautifulSoup(raw, 'html.parser')
    sources_before = [str(x) for x in before.select('.source-text')]
    eq_before = [str(x) for x in before.select('.eq')]
    images_before = [(x.get('src'), x.get('alt')) for x in before.find_all('img')]
    hrefs_before = [x.get('href') for x in before.find_all('a')]
    science_counts = {token: raw.count(token) for token in LOCKED_SCIENCE}

    if raw.count('热圆滑') != 2:
        raise RuntimeError(f'Module 07 expected exactly two visible 热圆滑 residues, found {raw.count("热圆滑")}')

    out = raw
    for old, new in REPLACEMENTS:
        if out.count(old) != 1:
            raise RuntimeError(f'Module 07 expected exactly one cleanup fragment: {old}')
        out = out.replace(old, new, 1)

    after = BeautifulSoup(out, 'html.parser')
    if sources_before != [str(x) for x in after.select('.source-text')]:
        raise RuntimeError('Module 07 paper-original source text changed')
    if eq_before != [str(x) for x in after.select('.eq')]:
        raise RuntimeError('Module 07 equations changed')
    if images_before != [(x.get('src'), x.get('alt')) for x in after.find_all('img')]:
        raise RuntimeError('Module 07 Figure wiring changed')
    if hrefs_before != [x.get('href') for x in after.find_all('a')]:
        raise RuntimeError('Module 07 href wiring changed')
    for token, count in science_counts.items():
        if out.count(token) != count:
            raise RuntimeError(f'Module 07 scientific statement drifted: {token}')

    visible = after.get_text(' ', strip=True)
    for token in REQUIRED:
        if token not in visible:
            raise RuntimeError(f'Module 07 final-audit required text missing: {token}')

    audit = BeautifulSoup(out, 'html.parser')
    for node in audit.select('.source-text'):
        node.decompose()
    outside = str(audit)
    for token in FORBIDDEN_OUTSIDE_SOURCE:
        if token in outside:
            raise RuntimeError(f'Module 07 final-audit residue found: {token}')

    TARGET.write_text(out, encoding='utf-8')
    print('Module 07 thermal-rounding terminology fixed; source text/equations/Figures/links/science unchanged.')


if __name__ == '__main__':
    main()
