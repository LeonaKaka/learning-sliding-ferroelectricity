from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/pinning-creep.html"

OLD = '靠近 f<sub>c</sub> 会进入交叉区 / 热圆滑物理，不能把整个阈值以下区域强行用一个 μ 吃掉。'
NEW = '靠近 f<sub>c</sub> 会进入交叉区 / 热圆整物理，不能把整个阈值以下区域强行用一个 μ 吃掉。'

REQUIRED = (
    '04 Pinning（钉扎）、Creep（蠕变）与 Roughness（粗糙度）',
    '知识图谱',
    '为什么真实畴壁不会匀速、笔直地走？',
    '有限温蠕变不是“给 T=0 方程加噪声”就结束',
    '热噪声平均是在',
    '固定淬火无序景观',
    '交叉区 / 热圆整物理',
    '先隔离畴壁传播 → 测速度 → 加独立几何 → 扩动力学区间 → 检查瞬态 / 有限尺寸 → 最后才谈普适坍缩',
)

FORBIDDEN_OUTSIDE_SOURCE = (
    'De钉扎', '普适ity', '无序无序样本',
    'published PDF', ' gate ', ' authority ', 'fit window',
    'sample-specific', 'held-out', 'source-level',
    'Numerical 模型ing', '热圆滑',
)

LOCKED_CLAIMS = (
    '文中的 “退钉扎” 是越过具体局域势垒的描述，并未建立热力学临界阈值、β/ζ/ν、有限尺寸标度或普适类',
    '真正适合拟合 μ 的是<b>低场、低温、可测的热激活区间</b>，不是所有 f&lt;f<sub>c</sub> 点',
    '如果一个无序样本跑了 6 个热随机种子，它不是“6 个独立无序样本”',
)


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    before = BeautifulSoup(raw, 'html.parser')
    source_before = [str(x) for x in before.select('.source-text')]
    eq_before = [str(x) for x in before.select('.eq')]
    images_before = [(x.get('src'), x.get('alt')) for x in before.find_all('img')]
    hrefs_before = [x.get('href') for x in before.find_all('a')]

    if raw.count(OLD) != 1:
        raise RuntimeError(f'Module 04 expected exactly one thermal-rounding residue, found {raw.count(OLD)}')
    out = raw.replace(OLD, NEW, 1)

    after = BeautifulSoup(out, 'html.parser')
    if source_before != [str(x) for x in after.select('.source-text')]:
        raise RuntimeError('Module 04 source text changed')
    if eq_before != [str(x) for x in after.select('.eq')]:
        raise RuntimeError('Module 04 equations changed')
    if images_before != [(x.get('src'), x.get('alt')) for x in after.find_all('img')]:
        raise RuntimeError('Module 04 Figure wiring changed')
    if hrefs_before != [x.get('href') for x in after.find_all('a')]:
        raise RuntimeError('Module 04 href wiring changed')
    for token in LOCKED_CLAIMS:
        if token not in out:
            raise RuntimeError(f'Module 04 scientific boundary drifted: {token}')

    visible = after.get_text(' ', strip=True)
    for token in REQUIRED:
        if token not in visible:
            raise RuntimeError(f'Module 04 final-audit required text missing: {token}')

    audit = BeautifulSoup(out, 'html.parser')
    for node in audit.select('.source-text'):
        node.decompose()
    outside = str(audit)
    for token in FORBIDDEN_OUTSIDE_SOURCE:
        if token in outside:
            raise RuntimeError(f'Module 04 final-audit residue found: {token}')

    TARGET.write_text(out, encoding='utf-8')
    print('Module 04 thermal-rounding terminology fixed; source text/equations/Figures/links/scientific boundaries unchanged.')


if __name__ == '__main__':
    main()
