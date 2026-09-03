from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'modules/numerical-modeling.html'
FIRST = ('#tdgl', '#reduction', '#disorder-axes', '#grid')
SECOND = ('#identifiability', '#velocity-estimator', '#run-receipt')

ANCHORS = (
    '第一次读这一章，只抓四个支点',
    '第二遍再读',
    '真实缺陷不能只压成一个 σ',
    'dx / dt 不能偷偷改物理',
    '“能产生一堵墙”不等于“已经是滑移铁电”',
    '固定的是 Δ，而不是数组里每个网格点的标准差',
    '热噪声 / FDT：温度不是再加一张随机场',
    '可复现不等于可作为当前依据',
)


def main() -> None:
    raw = PAGE.read_text(encoding='utf-8')
    doc = BeautifulSoup(raw, 'html.parser')
    sections = doc.select('section#first-read')
    if len(sections) != 1:
        raise RuntimeError(f'Module 07: expected one #first-read, found {len(sections)}')
    section = sections[0]

    cards = section.select('.first-read-grid > a')
    if len(cards) != 4:
        raise RuntimeError(f'Module 07: expected 4 first-read cards, found {len(cards)}')
    first_hrefs = tuple(a.get('href') for a in cards)
    if first_hrefs != FIRST:
        raise RuntimeError(f'Module 07: first-read hrefs/order drifted: {first_hrefs}')

    second = section.select_one('.second-read')
    if second is None:
        raise RuntimeError('Module 07: second-read layer missing')
    second_hrefs = tuple(a.get('href') for a in second.find_all('a'))
    if second_hrefs != SECOND:
        raise RuntimeError(f'Module 07: second-read hrefs/order drifted: {second_hrefs}')

    ids = {node.get('id') for node in doc.find_all(id=True)}
    for href in FIRST + SECOND:
        if href[1:] not in ids:
            raise RuntimeError(f'Module 07: first/second-read target missing: {href}')

    for anchor in ANCHORS:
        if anchor not in raw:
            raise RuntimeError(f'Module 07 Teaching/science anchor missing: {anchor}')

    pos_first = raw.index('id="first-read"')
    pos_source = raw.index('<p class="rule">核心来源：')
    pos_tdgl = raw.index('<h2 id="tdgl">')
    if not (pos_first < pos_source < pos_tdgl):
        raise RuntimeError('Module 07 first-read placement regressed')

    if raw.count('class="first-read-grid"') != 1 or raw.count('class="second-read"') != 1:
        raise RuntimeError('Module 07 first/second-read structure duplicated')

    print('MODULE 07 TEACHING SEAL PASS: 4 first-read pillars + 3 second-read research links, all target ids and scientific boundaries locked.')


if __name__ == '__main__':
    main()
