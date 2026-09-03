from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'modules/concept-paths.html'
INDEX = ROOT / 'index.html'

PAGE_REPL = {
    '这里不做 glossary（术语表）': '这里不做术语表',
    '先找单样本 bracket': '先找单样本阈值区间',
    'L10 Super-roughness →': 'L10 超粗糙 →',
    'synthetic gold test': '合成已知答案测试',
    'L09 β Gold Test →': 'L09 β 已知答案测试 →',
    'gold test PASS 与 universal claim PASS': '已知答案测试通过与普适性结论通过',
}
INDEX_REPL = {
    '单样本 bracket': '单样本阈值区间',
}

LOCKED_PAGE_ANCHORS = (
    'id="threshold"', 'id="roughness"', 'id="disorder"', 'id="creep"', 'id="closure"',
    '不能自动把它命名为热力学退钉扎',
    '单一尺寸、单一拟合区间里的一条漂亮双对数直线不够',
    '“某缺陷会钉扎畴壁”只说明它可能进入有效无序',
    '“阈值下速度非零”不是 creep-law 拟合许可证',
    '只要 β / ζ / ν / ψ 的真实数据尺度区间没有闭合',
)


def hrefs(raw: str) -> list[str | None]:
    soup = BeautifulSoup(raw, 'html.parser')
    return [a.get('href') for a in soup.find_all('a')]


def ids(raw: str) -> list[str | None]:
    soup = BeautifulSoup(raw, 'html.parser')
    return [x.get('id') for x in soup.find_all(id=True)]


def apply_exact(raw: str, repl: dict[str, str], label: str) -> str:
    out = raw
    for old, new in repl.items():
        count = out.count(old)
        if count != 1:
            raise RuntimeError(f'{label}: expected exactly one occurrence of {old!r}, found {count}')
        out = out.replace(old, new, 1)
    return out


def main() -> None:
    page_raw = PAGE.read_text(encoding='utf-8')
    index_raw = INDEX.read_text(encoding='utf-8')
    page_hrefs = hrefs(page_raw)
    page_ids = ids(page_raw)
    index_hrefs = hrefs(index_raw)
    index_ids = ids(index_raw)

    page_out = apply_exact(page_raw, PAGE_REPL, 'concept page')
    index_out = apply_exact(index_raw, INDEX_REPL, 'index')

    if hrefs(page_out) != page_hrefs or ids(page_out) != page_ids:
        raise RuntimeError('Concept page href/id wiring changed')
    if hrefs(index_out) != index_hrefs or ids(index_out) != index_ids:
        raise RuntimeError('Index href/id wiring changed')

    for anchor in LOCKED_PAGE_ANCHORS:
        if anchor not in page_out:
            raise RuntimeError(f'Concept page scientific boundary drifted: {anchor}')

    for bad in ('glossary（术语表）', '单样本 bracket', 'synthetic gold test', 'L09 β Gold Test', 'gold test PASS', 'universal claim PASS'):
        if bad in page_out:
            raise RuntimeError(f'Concept page residue remains: {bad}')
    if '单样本 bracket' in index_out:
        raise RuntimeError('Index bracket residue remains')

    PAGE.write_text(page_out, encoding='utf-8')
    INDEX.write_text(index_out, encoding='utf-8')
    print('CONCEPT PATHS POLISH PASS: ordinary workflow-English removed; paths, links, ids and scientific stop conditions unchanged.')


if __name__ == '__main__':
    main()
