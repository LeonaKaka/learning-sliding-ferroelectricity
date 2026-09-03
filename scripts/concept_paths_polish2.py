from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'modules/concept-paths.html'
INDEX = ROOT / 'index.html'

PAGE_REPL = {
    'super-rough（超粗糙）': '超粗糙',
    'creep、depinning 与 flow': '蠕变、退钉扎与流动',
    '05 Creep → Depinning →': '05 蠕变 → 退钉扎 →',
    '07 Thermal Noise（热噪声） →': '07 热噪声 →',
    ' creep law 或 μ': '蠕变律或 μ',
    ' creep-law 拟合许可证': '蠕变律拟合许可证',
    'L12 Finite-T →': 'L12 有限温 →',
    '合成已知答案测试 只能': '合成已知答案测试只能',
    '普适性结论通过 是两个不同层级': '普适性结论通过是两个不同层级',
}
INDEX_REPL = {
    'L10 super-roughness': 'L10 超粗糙',
    'creep/depinning 相图': '蠕变/退钉扎相图',
}


def wiring(raw: str) -> tuple[list[str | None], list[str | None]]:
    soup = BeautifulSoup(raw, 'html.parser')
    return [a.get('href') for a in soup.find_all('a')], [x.get('id') for x in soup.find_all(id=True)]


def exact(raw: str, repl: dict[str, str], label: str) -> str:
    out = raw
    for old, new in repl.items():
        if out.count(old) != 1:
            raise RuntimeError(f'{label}: expected exactly one {old!r}, found {out.count(old)}')
        out = out.replace(old, new, 1)
    return out


def main() -> None:
    page = PAGE.read_text(encoding='utf-8')
    index = INDEX.read_text(encoding='utf-8')
    pw = wiring(page)
    iw = wiring(index)

    page_out = exact(page, PAGE_REPL, 'concept page')
    index_out = exact(index, INDEX_REPL, 'index')

    if wiring(page_out) != pw or wiring(index_out) != iw:
        raise RuntimeError('Concept Paths polish2 changed href/id wiring')

    for anchor in (
        '不能自动把它命名为热力学退钉扎',
        '单一尺寸、单一拟合区间里的一条漂亮双对数直线不够',
        '“某缺陷会钉扎畴壁”只说明它可能进入有效无序',
        '“阈值下速度非零”不是蠕变律拟合许可证',
        '已知答案测试通过与普适性结论通过是两个不同层级',
    ):
        if anchor not in page_out:
            raise RuntimeError(f'Concept Paths boundary missing: {anchor}')

    for bad in ('creep law', 'creep-law', 'Thermal Noise（热噪声）', 'Finite-T', 'super-rough（超粗糙）'):
        if bad in page_out:
            raise RuntimeError(f'Concept Paths visible residue remains: {bad}')

    PAGE.write_text(page_out, encoding='utf-8')
    INDEX.write_text(index_out, encoding='utf-8')
    print('CONCEPT PATHS POLISH2 PASS: teaching prose normalized; links/ids/scientific stop conditions unchanged.')


if __name__ == '__main__':
    main()
