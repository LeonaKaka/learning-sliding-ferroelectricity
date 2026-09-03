from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/domain-walls.html"

REPLACEMENTS = (
    ('<a href="../index.html#map">Map</a> · <a href="#force">Force</a> · <a href="#experiment">Experiment</a>', '<a href="../index.html#map">知识地图</a> · <a href="#force">驱动力</a> · <a href="#experiment">实验</a>'),
    ('这里只保留科学 Figure，不再使用段落截图。', '这里只保留科学图，不再使用段落截图。'),
    ('Phys. Rev. B 111, L201406 · Drive PDF', 'Phys. Rev. B 111, L201406 · 项目 Drive 正式 PDF'),
    ('Phys. Rev. Lett. 135, 046201 · Drive PDF', 'Phys. Rev. Lett. 135, 046201 · 项目 Drive 正式 PDF'),
    ('Phys. Rev. X 16, 011066 · Drive PDF', 'Phys. Rev. X 16, 011066 · 项目 Drive 正式 PDF'),
    ('Phys. Rev. Lett. 136, 206202 · Drive PDF', 'Phys. Rev. Lett. 136, 206202 · 项目 Drive 正式 PDF'),
    ('2026 issue；online first 2025-10-28', '2026 年卷期；2025-10-28 在线首发'),
    ('不复制 Figure，也不伪造“Drive 原文”', '不复制论文图，也不伪造“Drive 原文”'),
    ('它也给 Module 04 / 05 一个明确的实验接口', '它也给模块 04 / 05 一个明确的实验接口'),
)

REQUIRED = (
    '知识地图', '驱动力', '实验',
    '这里只保留科学图，不再使用段落截图',
    'Phys. Rev. B 111, L201406 · 项目 Drive 正式 PDF',
    'Phys. Rev. Lett. 135, 046201 · 项目 Drive 正式 PDF',
    'Phys. Rev. X 16, 011066 · 项目 Drive 正式 PDF',
    'Phys. Rev. Lett. 136, 206202 · 项目 Drive 正式 PDF',
    '2026 年卷期；2025-10-28 在线首发',
    '不复制论文图，也不伪造“Drive 原文”',
    '模块 04 / 05 一个明确的实验接口',
)

FORBIDDEN_OUTSIDE_SOURCE = (
    '>Map</a>', '>Force</a>', '>Experiment</a>',
    '科学 Figure',
    ' · Drive PDF',
    '2026 issue', 'online first',
    '不复制 Figure',
    'Module 04 / 05',
)

LOCKED_SCIENCE = (
    'sliding barrier（滑移势垒）',
    'domain wall（畴壁）',
    'Born effective charge tensor（Born 有效电荷张量）',
    'homogeneous coherent sliding（均匀整体相干滑移）',
    'symmetry-broken region（对称性破缺区域）',
    'microscopic driving mechanism（微观驱动机制）',
    'fully commensurate single-domain（完全共格单畴）',
    'DW-free switching（无畴壁翻转）',
    'critical depinning transition（临界退钉扎转变）',
    'universality class（普适类）',
    'Shear-mode Raman（剪切模 Raman）',
    'apparent critical field（表观临界场）',
    'pinning landscape（钉扎景观）',
    'clean / superlubric mobility（洁净体系 / 近超润滑迁移率）',
    '不应该自动升级成“所有滑移铁电、所有场强和所有缺陷条件下都绝不可能 nucleate（成核）”的数学定理',
    '不能把它升级成所有滑移铁电的必要条件',
    '距离真正的 critical depinning transition（临界退钉扎转变）还差时间分辨的 v(E)、统计量和有限尺寸标度',
)


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    before = BeautifulSoup(raw, 'html.parser')
    source_before = [str(x) for x in before.select('.source-text')]
    eq_before = [str(x) for x in before.select('.eq')]
    imgs_before = [(x.get('src'), x.get('alt')) for x in before.find_all('img')]
    hrefs_before = [x.get('href') for x in before.find_all('a')]
    science_counts = {token: raw.count(token) for token in LOCKED_SCIENCE}

    out = raw
    for old, new in REPLACEMENTS:
        if old not in out:
            raise RuntimeError(f'Domain Walls expected editorial fragment missing: {old}')
        out = out.replace(old, new, 1)

    after = BeautifulSoup(out, 'html.parser')
    if source_before != [str(x) for x in after.select('.source-text')]:
        raise RuntimeError('Domain Walls paper-original source text changed')
    if eq_before != [str(x) for x in after.select('.eq')]:
        raise RuntimeError('Domain Walls equation changed')
    if imgs_before != [(x.get('src'), x.get('alt')) for x in after.find_all('img')]:
        raise RuntimeError('Domain Walls Figure wiring changed')
    if hrefs_before != [x.get('href') for x in after.find_all('a')]:
        raise RuntimeError('Domain Walls href wiring changed')
    for token, count in science_counts.items():
        if out.count(token) != count:
            raise RuntimeError(f'Domain Walls scientific term/claim drifted: {token}')

    audit = BeautifulSoup(out, 'html.parser')
    for node in audit.select('.source-text'):
        node.decompose()
    visible_outside_source = str(audit)
    visible_text = after.get_text(' ', strip=True)

    for token in REQUIRED:
        if token not in visible_text:
            raise RuntimeError(f'Domain Walls required Language V2 text missing: {token}')
    for token in FORBIDDEN_OUTSIDE_SOURCE:
        if token in visible_outside_source:
            raise RuntimeError(f'Domain Walls editorial English remains outside source text: {token}')

    TARGET.write_text(out, encoding='utf-8')
    print('Domain Walls final editorial Language V2 repair complete; source text/equations/Figures/links/science unchanged.')


if __name__ == '__main__':
    main()
