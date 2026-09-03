from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'modules/depinning.html'


def protected(raw: str) -> dict[str, list[str | None]]:
    doc = BeautifulSoup(raw, 'html.parser')
    return {
        'sources': [str(x) for x in doc.select('.source-text')],
        'equations': [str(x) for x in doc.select('.eq')],
        'figures': [str(x) for x in doc.find_all('figure')],
        'hrefs': [x.get('href') for x in doc.find_all('a')],
        'srcs': [x.get('src') for x in doc.find_all('img')],
        'pre': [str(x) for x in doc.find_all('pre')],
        'code': [str(x) for x in doc.find_all('code')],
    }


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    before = protected(raw)
    old = '看完整的完整翻转 vs 孤立畴壁流程对照 →'
    new = '看完整翻转与孤立畴壁流程对照 →'
    if raw.count(old) != 1:
        raise RuntimeError(f'expected exactly one bridge residue, found {raw.count(old)}')
    out = raw.replace(old, new, 1)
    if protected(out) != before:
        raise RuntimeError('bridge polish changed protected evidence/link wiring')

    doc = BeautifulSoup(out, 'html.parser')
    checks = doc.find('section', id='claim-check')
    if checks is None or len(checks.find_all('details', recursive=False)) != 4:
        raise RuntimeError('depinning claim-check structure drifted during bridge polish')
    if old in out or '完整翻转与孤立畴壁' not in out:
        raise RuntimeError('bridge polish did not converge')

    TARGET.write_text(out, encoding='utf-8')
    print('TEACHING V2 BRIDGE POLISH PASS: duplicate/mixed-language bridge fixed; evidence and claim checks unchanged.')


if __name__ == '__main__':
    main()
