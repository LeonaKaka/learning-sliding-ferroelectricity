from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/switching-pathways.html"

REPLACEMENTS = (
    ('<a href="../index.html#map">Map</a> · <a href="#atomic">Atomic path</a> · <a href="#trilayer">Trilayer</a>', '<a href="../index.html#map">知识地图</a> · <a href="#atomic">原子路径</a> · <a href="#trilayer">三层体系</a>'),
    ('保留完整 panel、坐标轴、color bar、箭头和标签', '保留完整分图、坐标轴、色标、箭头和标签'),
    ('Nature Communications · main text · published PDF p.4 · 原文未改', 'Nature Communications · 正文 · 已发表 PDF 第 4 页 · 原文未改'),
    ('Nature Communications · “Atomic-level polarization switching dynamics” · published PDF pp.5–6 · 原文未改', 'Nature Communications · “Atomic-level polarization switching dynamics” · 已发表 PDF 第 5–6 页 · 原文未改'),
    ('Nature Nanotechnology · “Influence of pinning centres on the polarization switching pathway” · published PDF p.5 · 原文未改', 'Nature Nanotechnology · “Influence of pinning centres on the polarization switching pathway” · 已发表 PDF 第 5 页 · 原文未改'),
)

REQUIRED = (
    '知识地图', '原子路径', '三层体系',
    '保留完整分图、坐标轴、色标、箭头和标签',
    'Nature Communications · 正文 · 已发表 PDF 第 4 页',
    '“Atomic-level polarization switching dynamics” · 已发表 PDF 第 5–6 页',
    '“Influence of pinning centres on the polarization switching pathway” · 已发表 PDF 第 5 页',
)

FORBIDDEN_OUTSIDE_SOURCE = (
    '>Map</a>', '>Atomic path</a>', '>Trilayer</a>',
    '完整 panel', 'color bar',
    'main text · published PDF',
    '” · published PDF',
)

LOCKED_SCIENCE = (
    'metastable stacking（亚稳堆垛）',
    'switching pathway（翻转路径）',
    'pre-existing DW（预存畴壁）',
    'depin / release（解钉 / 释放）',
    'Stark shift（Stark 位移）',
    'local pinning potential（局域钉扎势）',
    'sliding-induced reversal（滑移诱导的极化反转）',
    'pinning hierarchy（钉扎层级）',
    'E<sub>c</sub> 直接当作普适的退钉扎临界场',
)


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    before = BeautifulSoup(raw, 'html.parser')
    source_before = [str(x) for x in before.select('.source-text')]
    imgs_before = [(x.get('src'), x.get('alt')) for x in before.find_all('img')]
    hrefs_before = [x.get('href') for x in before.find_all('a')]
    science_counts = {token: raw.count(token) for token in LOCKED_SCIENCE}

    out = raw
    for old, new in REPLACEMENTS:
        if old not in out:
            raise RuntimeError(f'Switching Pathways expected editorial fragment missing: {old}')
        out = out.replace(old, new, 1)

    after = BeautifulSoup(out, 'html.parser')
    if source_before != [str(x) for x in after.select('.source-text')]:
        raise RuntimeError('Switching Pathways paper-original source text changed')
    if imgs_before != [(x.get('src'), x.get('alt')) for x in after.find_all('img')]:
        raise RuntimeError('Switching Pathways Figure wiring changed')
    if hrefs_before != [x.get('href') for x in after.find_all('a')]:
        raise RuntimeError('Switching Pathways href wiring changed')
    for token, count in science_counts.items():
        if out.count(token) != count:
            raise RuntimeError(f'Switching Pathways scientific term/claim drifted: {token}')

    audit = BeautifulSoup(out, 'html.parser')
    for node in audit.select('.source-text'):
        node.decompose()
    visible_outside_source = str(audit)
    visible_text = after.get_text(' ', strip=True)

    for token in REQUIRED:
        if token not in visible_text:
            raise RuntimeError(f'Switching Pathways required Language V2 text missing: {token}')
    for token in FORBIDDEN_OUTSIDE_SOURCE:
        if token in visible_outside_source:
            raise RuntimeError(f'Switching Pathways editorial English remains outside source text: {token}')

    TARGET.write_text(out, encoding='utf-8')
    print('Switching Pathways final editorial Language V2 repair complete; source text/Figures/links/science unchanged.')


if __name__ == '__main__':
    main()
