from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'modules/current-frontiers.html'

FIRST_HEADINGS = (
    '① 直接观察了什么？',
    '② 哪部分仍是机制解释？',
    '③ 哪个结果限制了外推？',
    '④ 离普适性还缺什么？',
)

ANCHORS = (
    '第一次读前沿论文，固定问四个问题',
    '“看见畴壁”不是“测出普适类”',
    '单畴壁最小模型有明确结构边界',
    '不要把机制成熟度写成普适性成熟度',
    '机制证据已经很强，普适性证据还没闭合',
    '预存畴壁不是无条件必要条件',
    '真正缺的不是“再来一篇钉扎论文”，而是同一套标度可观测量',
)


def main() -> None:
    raw = PAGE.read_text(encoding='utf-8')
    doc = BeautifulSoup(raw, 'html.parser')
    sections = doc.select('section#first-read')
    if len(sections) != 1:
        raise RuntimeError(f'Module 08: expected one #first-read, found {len(sections)}')
    section = sections[0]

    cards = section.select('.frontier-grid > .frontier-card')
    if len(cards) != 4:
        raise RuntimeError(f'Module 08: expected 4 first-read cards, found {len(cards)}')
    headings = tuple(card.find('b').get_text(' ', strip=True) for card in cards)
    if headings != FIRST_HEADINGS:
        raise RuntimeError(f'Module 08 first-read headings/order drifted: {headings}')

    route = section.select_one('.route')
    if route is None:
        raise RuntimeError('Module 08: first-read route missing')
    hrefs = tuple(a.get('href') for a in route.find_all('a'))
    if hrefs != ('#score', '#missing'):
        raise RuntimeError(f'Module 08 first-read route hrefs drifted: {hrefs}')
    ids = {node.get('id') for node in doc.find_all(id=True)}
    for href in hrefs:
        if href[1:] not in ids:
            raise RuntimeError(f'Module 08 first-read target missing: {href}')

    for anchor in ANCHORS:
        if anchor not in raw:
            raise RuntimeError(f'Module 08 Teaching/science anchor missing: {anchor}')

    pos_first = raw.index('id="first-read"')
    pos_rule = raw.index('<p class="rule">本章只使用项目 Drive 中的 2025–2026 主线论文')
    pos_score = raw.index('<h2 id="score">')
    if not (pos_first < pos_rule < pos_score):
        raise RuntimeError('Module 08 first-read placement regressed')

    print('MODULE 08 TEACHING SEAL PASS: four-question evidence-maturity reading frame and score/missing navigation locked.')


if __name__ == '__main__':
    main()
