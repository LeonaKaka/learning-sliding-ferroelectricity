from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / 'modules/reproduction-lab-08.html'

LOCKED_RESULTS = (
    '3.47%–4.93%',
    '0.0010%',
    '0.5%',
    'dt=.025',
    'dt=.0125',
    '0.001387%',
    'L=32',
    '本课不拟合 β',
    '不足以证明临界标度',
)


def visible_text(raw: str) -> str:
    soup = BeautifulSoup(raw, 'html.parser')
    for selector in ('pre', 'code', 'script', 'style'):
        for node in soup.select(selector):
            node.decompose()
    return ' '.join(soup.stripped_strings)


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    before = BeautifulSoup(raw, 'html.parser')
    images_before = [(x.get('src'), x.get('alt')) for x in before.find_all('img')]
    hrefs_before = [x.get('href') for x in before.find_all('a')]
    result_counts = {token: raw.count(token) for token in LOCKED_RESULTS}

    old = '<b>steady velocity（稳态速度）v</b>'
    new = '<b>稳态速度 v</b>'
    if raw.count(old) != 1:
        raise RuntimeError(f'Lab 08 expected exactly one visible steady-velocity phrase, found {raw.count(old)}')
    out = raw.replace(old, new, 1)

    after = BeautifulSoup(out, 'html.parser')
    if images_before != [(x.get('src'), x.get('alt')) for x in after.find_all('img')]:
        raise RuntimeError('Lab 08 Figure wiring changed')
    if hrefs_before != [x.get('href') for x in after.find_all('a')]:
        raise RuntimeError('Lab 08 href wiring changed')
    for token, count in result_counts.items():
        if out.count(token) != count:
            raise RuntimeError(f'Lab 08 numerical/scientific result drifted: {token}')

    visible = visible_text(out)
    if 'steady velocity' in visible.lower():
        raise RuntimeError('Lab 08 visible steady velocity residue remains')
    if '稳态速度 v' not in out:
        raise RuntimeError('Lab 08 Chinese steady-velocity wording missing')
    if 'center-of-mass velocity（质心速度）' not in out:
        raise RuntimeError('Lab 08 center-of-mass velocity first-use explanation drifted')

    TARGET.write_text(out, encoding='utf-8')
    print('Lab 08 visible steady-velocity wording normalized; Figures/links/numerical results/scientific boundaries unchanged.')


if __name__ == '__main__':
    main()
