from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/foundations.html"

REPLACEMENTS = (
    ('<a href="../index.html#map">Map</a> · <a href="#multi">Multilayer</a> · <a href="#sym">Symmetry</a>', '<a href="../index.html#map">知识地图</a> · <a href="#multi">多层体系</a> · <a href="#sym">对称性</a>'),
    ('PNAS · Theoretical Model · published PDF p.2 · 跨栏拼接，原文未改', 'PNAS · 理论模型 · 已发表 PDF 第 2 页 · 跨栏拼接，原文未改'),
    ('Science · main text · published PDF p.1 · 跨栏拼接，原文未改', 'Science · 正文 · 已发表 PDF 第 1 页 · 跨栏拼接，原文未改'),
    ('Science · main text · published PDF p.2 · 原文未改', 'Science · 正文 · 已发表 PDF 第 2 页 · 原文未改'),
    ('Nature Communications · main text · published PDF pp.3–4 · 跨栏/跨页拼接，原文未改', 'Nature Communications · 正文 · 已发表 PDF 第 3–4 页 · 跨栏/跨页拼接，原文未改'),
    ('PRL · main text · published PDF p.2 · 原文未改', 'PRL · 正文 · 已发表 PDF 第 2 页 · 原文未改'),
)

REQUIRED = (
    '知识地图', '多层体系', '对称性',
    'PNAS · 理论模型 · 已发表 PDF 第 2 页',
    'Science · 正文 · 已发表 PDF 第 1 页',
    'Science · 正文 · 已发表 PDF 第 2 页',
    'Nature Communications · 正文 · 已发表 PDF 第 3–4 页',
    'PRL · 正文 · 已发表 PDF 第 2 页',
)
FORBIDDEN_OUTSIDE_SOURCE = (
    '>Map</a>', '>Multilayer</a>', '>Symmetry</a>',
    'Theoretical Model · published PDF',
    'main text · published PDF',
)
LOCKED_RAW = (
    'sliding ferroelectricity（滑移铁电）',
    'stacking registry（堆垛注册）',
    'interlayer charge transfer（层间电荷转移）',
    'coherent sliding（整体相干滑移）',
    'domain wall（畴壁）',
    'inversion symmetry（反演对称性）',
    'KPFM（开尔文探针力显微镜）',
    'surface potential（表面电势）',
    'interfacial polarization（界面极化）',
    'bilayer（双层）',
    'trilayer（三层）',
    'intermediate state（中间态）',
    'layer group（层群）',
    'symmetry criterion（对称性判据）',
    'coercive field（矫顽场）',
)


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    before = BeautifulSoup(raw, "html.parser")
    source_before = [str(x) for x in before.select('.source-text')]
    img_before = [(x.get('src'), x.get('alt')) for x in before.find_all('img')]
    href_before = [x.get('href') for x in before.find_all('a')]
    locked_counts = {x: raw.count(x) for x in LOCKED_RAW}

    out = raw
    for old, new in REPLACEMENTS:
        if old not in out:
            raise RuntimeError(f"Foundations expected editorial fragment missing: {old}")
        out = out.replace(old, new, 1)

    after = BeautifulSoup(out, "html.parser")
    if source_before != [str(x) for x in after.select('.source-text')]:
        raise RuntimeError('Foundations paper-original source text changed')
    if img_before != [(x.get('src'), x.get('alt')) for x in after.find_all('img')]:
        raise RuntimeError('Foundations Figure wiring changed')
    if href_before != [x.get('href') for x in after.find_all('a')]:
        raise RuntimeError('Foundations href wiring changed')
    for token, count in locked_counts.items():
        if out.count(token) != count:
            raise RuntimeError(f'Foundations scientific term/claim drifted: {token}')

    # Audit only visible text outside frozen paper-original blocks.
    audit = BeautifulSoup(out, "html.parser")
    for node in audit.select('.source-text'):
        node.decompose()
    visible_outside_source = str(audit)
    visible_text = after.get_text(' ', strip=True)
    for token in REQUIRED:
        if token not in visible_text:
            raise RuntimeError(f'Foundations required Language V2 text missing: {token}')
    for token in FORBIDDEN_OUTSIDE_SOURCE:
        if token in visible_outside_source:
            raise RuntimeError(f'Foundations editorial English remains outside source text: {token}')

    TARGET.write_text(out, encoding='utf-8')
    print('Foundations final editorial Language V2 repair complete; source text/Figures/links/science unchanged.')


if __name__ == '__main__':
    main()
