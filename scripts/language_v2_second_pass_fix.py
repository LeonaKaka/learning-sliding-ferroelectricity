from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/current-frontiers.html"

REQUIRED = (
    '08 Current Frontiers（当前前沿）',
    '机制证据已经很强，普适性证据还没闭合',
    '证据评分',
    '缺失证据',
    '预存畴壁不是无条件必要条件',
    '为什么这仍然是一个研究空档',
)

FORBIDDEN_OUTSIDE_SOURCE = (
    '热圆滑', 'published PDF', 'source-level', 'held-out', 'sample-specific',
    ' gate ', ' authority ', 'fit window', ' workflow ', ' checkpoint ',
    'Numerical 模型ing', '普适ity', 'De钉扎',
)

LOCKED_BOUNDARIES = (
    '未给连续恒场 v(E) 临界曲线',
    '速度–场动力学，但不是淬火无序退钉扎标度',
    '无畴壁翻转：提醒“畴壁必要性”有结构条件',
    '前沿问题因此不再是“畴壁到底重不重要”',
    '在孤立畴壁条件下能否进入受驱无序界面的普适性框架',
)


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')

    if not soup.find_all('img'):
        raise RuntimeError('Module 08 Figures unexpectedly missing')
    if not soup.find_all('a'):
        raise RuntimeError('Module 08 links unexpectedly missing')

    visible = soup.get_text(' ', strip=True)
    for token in REQUIRED:
        if token not in visible:
            raise RuntimeError(f'Module 08 final-audit required text missing: {token}')
    for token in LOCKED_BOUNDARIES:
        if token not in raw:
            raise RuntimeError(f'Module 08 scientific boundary drifted: {token}')

    audit = BeautifulSoup(raw, 'html.parser')
    for node in audit.select('.source-text'):
        node.decompose()
    outside = str(audit)
    for token in FORBIDDEN_OUTSIDE_SOURCE:
        if token in outside:
            raise RuntimeError(f'Module 08 final-audit residue found: {token}')

    if TARGET.read_text(encoding='utf-8') != raw:
        raise RuntimeError('Module 08 read-only seal unexpectedly changed the page')
    print('Module 08 final Language V2 audit sealed read-only; evidence boundaries and wiring present.')


if __name__ == '__main__':
    main()
