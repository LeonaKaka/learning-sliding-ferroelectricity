from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/current-frontiers.html"

REQUIRED = (
    '08 Current Frontiers（当前前沿）',
    '当前真正的前沿，不是“滑移铁电存不存在”，而是“翻转到底怎样发生”',
    '机制证据',
    '普适性证据',
    '证据还没有闭合',
    '为什么这仍然是研究空档',
)

FORBIDDEN_OUTSIDE_SOURCE = (
    '热圆滑', 'published PDF', 'source-level', 'held-out', 'sample-specific',
    ' gate ', ' authority ', 'fit window', ' workflow ', ' checkpoint ',
    'Numerical 模型ing', '普适ity', 'De钉扎',
)

LOCKED_BOUNDARIES = (
    '目前没有一套滑移铁电实验同时完成受控 f<sub>c</sub>、稳态 v(E)、β、独立 ζ、有限尺寸 ν / 坍缩、热圆整与雪崩统计。',
    '它证明“畴壁传播主导”在这类多畴器件中非常重要，但不是所有几何与初态的唯一机制。',
    'Baek 2025 给出了 fully commensurate single-domain（完全共格单畴）条件下的 DW-free switching（无畴壁翻转）证据。',
    '因此“畴壁主导”应被写成有条件的机制结论，而不是滑移铁电的普适定理。',
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
