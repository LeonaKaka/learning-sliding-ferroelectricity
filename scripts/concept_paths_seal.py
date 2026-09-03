from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'modules/concept-paths.html'
INDEX = ROOT / 'index.html'

PATH_IDS = ('threshold', 'roughness', 'disorder', 'creep', 'closure')
INDEX_HREFS = tuple(f'modules/concept-paths.html#{x}' for x in PATH_IDS)

SCIENCE_STOP_ANCHORS = (
    '只看到 P–E 的 Ec、一次跳变或“速度开始非零”，都不能自动把它命名为热力学退钉扎',
    '单一尺寸、单一拟合区间里的一条漂亮双对数直线不够',
    '“某缺陷会钉扎畴壁”只说明它可能进入有效无序',
    '“阈值下速度非零”不是蠕变律拟合许可证',
    '已知答案测试通过与普适性结论通过是两个不同层级',
)

FORBIDDEN_VISIBLE = (
    '单样本 bracket',
    'synthetic gold test',
    'gold test PASS',
    'universal claim PASS',
    'creep law',
    'creep-law',
    'Thermal Noise（热噪声）',
    'Finite-T',
    'super-rough（超粗糙）',
    '合成已知答案测试 只能',
    '普适性结论通过 是两个不同层级',
)


def soup(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')


def visible_text(doc: BeautifulSoup) -> str:
    clone = BeautifulSoup(str(doc), 'html.parser')
    for selector in ('script', 'style', 'pre', 'code', '.source-text'):
        for node in clone.select(selector):
            node.decompose()
    return ' '.join(clone.stripped_strings)


def assert_local_links(source: Path, doc: BeautifulSoup) -> int:
    checked = 0
    repo_root = ROOT.resolve()
    for a in doc.find_all('a'):
        href = (a.get('href') or '').strip()
        if not href or href.startswith(('mailto:', 'javascript:', 'data:')):
            continue
        parts = urlsplit(href)
        if parts.scheme or parts.netloc:
            continue

        if parts.path:
            target = (source.parent / unquote(parts.path)).resolve()
        else:
            target = source.resolve()

        if target != repo_root and repo_root not in target.parents:
            raise RuntimeError(f'{source.name}: local link escapes repository root: {href}')
        if not target.exists():
            raise RuntimeError(f'{source.name}: missing local target: {href}')

        if parts.fragment:
            if target.suffix.lower() != '.html':
                raise RuntimeError(f'{source.name}: fragment points to non-HTML target: {href}')
            target_doc = soup(target)
            fragment = unquote(parts.fragment)
            if target_doc.find(id=fragment) is None:
                raise RuntimeError(f'{source.name}: missing target fragment #{fragment} in {target.relative_to(ROOT)} for href={href}')
        checked += 1
    return checked


def main() -> None:
    for path in (PAGE, INDEX):
        if not path.exists():
            raise RuntimeError(f'missing Concept Paths dependency: {path.relative_to(ROOT)}')

    page_doc = soup(PAGE)
    index_doc = soup(INDEX)
    page_raw = PAGE.read_text(encoding='utf-8')
    index_raw = INDEX.read_text(encoding='utf-8')

    sections = page_doc.select('section.path[id]')
    ids = tuple(section.get('id') for section in sections)
    if ids != PATH_IDS:
        raise RuntimeError(f'Concept Paths section order/count drifted: {ids}')

    for section in sections:
        pid = section.get('id')
        steps = section.select(':scope > .chain > .step')
        stops = section.select(':scope > .stop')
        if len(steps) != 5:
            raise RuntimeError(f'Concept Path {pid}: expected exactly 5 learning steps, found {len(steps)}')
        if len(stops) != 1:
            raise RuntimeError(f'Concept Path {pid}: expected exactly 1 stop condition, found {len(stops)}')

    for anchor in SCIENCE_STOP_ANCHORS:
        if anchor not in page_raw:
            raise RuntimeError(f'Concept Paths scientific stop condition drifted: {anchor}')

    visible = visible_text(page_doc)
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f'Concept Paths visible prose residue: {token}')

    home = index_doc.find('section', id='concept-paths')
    if home is None:
        raise RuntimeError('index.html: missing #concept-paths entry section')
    cards = home.select('article.paper')
    if len(cards) != 5:
        raise RuntimeError(f'index.html: expected exactly 5 Concept Paths cards, found {len(cards)}')
    hrefs = tuple(card.find('a').get('href') for card in cards if card.find('a'))
    if hrefs != INDEX_HREFS:
        raise RuntimeError(f'index.html: Concept Paths card hrefs/order drifted: {hrefs}')

    if page_raw.count('class="stop"') != 5:
        raise RuntimeError('Concept Paths stop-condition count drifted')
    if index_raw.count('modules/concept-paths.html#') != 5:
        raise RuntimeError('index.html Concept Paths link count drifted')

    checked = assert_local_links(PAGE, page_doc) + assert_local_links(INDEX, home)
    print(f'CONCEPT PATHS SEAL PASS: 5 paths / 25 learning steps / 5 stop conditions / {checked} local links checked including HTML fragments.')


if __name__ == '__main__':
    main()
