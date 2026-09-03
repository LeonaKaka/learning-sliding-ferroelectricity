from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/pinning-creep.html"

REQUIRED = (
    '04 Pinning（钉扎）、Creep（蠕变）与 Roughness（粗糙度）',
    '知识图谱',
    '为什么真实畴壁不会匀速、笔直地走？',
    '钉扎', '蠕变', '粗糙度', '退钉扎',
    '有限温蠕变不是“给 T=0 方程加噪声”就结束',
    '热噪声平均是在',
    '固定淬火无序景观',
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
    soup = BeautifulSoup(raw, 'html.parser')

    source_snapshot = [str(x) for x in soup.select('.source-text')]
    image_snapshot = [(x.get('src'), x.get('alt')) for x in soup.find_all('img')]
    href_snapshot = [x.get('href') for x in soup.find_all('a')]
    if not source_snapshot:
        raise RuntimeError('Module 04 source-text blocks unexpectedly missing')
    if not image_snapshot:
        raise RuntimeError('Module 04 Figures unexpectedly missing')
    if not href_snapshot:
        raise RuntimeError('Module 04 links unexpectedly missing')

    visible = soup.get_text(' ', strip=True)
    for token in REQUIRED:
        if token not in visible:
            raise RuntimeError(f'Module 04 final-audit required text missing: {token}')
    for token in LOCKED_CLAIMS:
        if token not in raw:
            raise RuntimeError(f'Module 04 scientific boundary drifted: {token}')

    audit = BeautifulSoup(raw, 'html.parser')
    for node in audit.select('.source-text'):
        node.decompose()
    outside = str(audit)
    for token in FORBIDDEN_OUTSIDE_SOURCE:
        if token in outside:
            raise RuntimeError(f'Module 04 final-audit residue found: {token}')

    # Read-only seal: never rewrite the page.
    if TARGET.read_text(encoding='utf-8') != raw:
        raise RuntimeError('Module 04 read-only seal unexpectedly changed the page')
    print('Module 04 final Language V2 audit sealed read-only; source text/Figures/links/scientific boundaries present.')


if __name__ == '__main__':
    main()
