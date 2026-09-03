from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

PAGES = [
    ROOT / 'modules/foundations.html',
    ROOT / 'modules/switching-pathways.html',
    ROOT / 'modules/domain-walls.html',
    ROOT / 'modules/pinning-creep.html',
    ROOT / 'modules/depinning.html',
    ROOT / 'modules/disorder-rfim.html',
    ROOT / 'modules/numerical-modeling.html',
    ROOT / 'modules/current-frontiers.html',
    ROOT / 'modules/research-track.html',
    ROOT / 'modules/reproduction-lab.html',
    *[ROOT / f'modules/reproduction-lab-{i:02d}.html' for i in range(2, 13)],
]

FORBIDDEN_VISIBLE = (
    '热圆滑',
    'elastic-界面 language',
    '一维 elastic string',
    '阈值-distribution broadening',
    'Numerical 模型ing',
    '普适ity',
    'De钉扎',
    '项目项目',
    '封闭封闭',
    '无序无序样本',
    'main text · published PDF',
    'published PDF',
    'RF-like',
    'Se-vacancy',
    'spatial 多重标度',
    'lattice 模型',
    'late 运动',
    '畴壁 extraction',
    'size 定义',
    'CI / 自助法',
    'cycle 等内层重复',
    '跨 stage',
    ' up to E',
)

FORBIDDEN_VISIBLE_LOWER = (
    ' gate ',
    ' authority ',
    ' fit window',
    ' workflow ',
    ' checkpoint ',
    ' sample-specific',
    ' held-out',
    ' source-level',
    ' estimator ',
    ' benchmark ',
    ' raw data',
    ' steady velocity',
)

CRITICAL_ANCHORS = {
    'pinning-creep.html': (
        '第一次读这一章：',
        'Tybell 看“速度为什么高度非线性”',
        'Paruch 看“粗糙度怎样被定义和测量”',
        'Kim 看“统计钉扎如何落回单个局域事件”',
        '进阶研究方法 · 粗糙度验收判据',
        '局域退钉扎与临界退钉扎不是同一个概念',
    ),
    'depinning.html': (
        '第一次读本章，先走四步：',
        '进阶研究方法 A · 坍缩验收判据',
        '进阶研究方法 B · 阈值推断阶梯',
        '进阶研究方法 C · 指数提取纪律',
        '下一章必须把无序本身拆开',
        '“有阈值 + 一条幂律”不等于退钉扎普适性',
    ),
    'disorder-rfim.html': (
        '第一次读本章，先把问题分成四层：',
        '不要从“样品有缺陷”直接跳到“它就是 RFIM”',
        '弹性流形的 “随机场类别” ≠ “用了 RFIM”',
        '研究桥接 · 真实滑移铁电里的无序到底是什么？',
        '实验里看见无序，不等于已经知道它属于哪个统计无序类别',
        'RFIM 是一个体相序参量模型',
    ),
    'current-frontiers.html': (
        '机制证据已经很强，普适性证据还没闭合',
        '预存畴壁不是无条件必要条件',
        '在孤立畴壁条件下能否进入受驱无序界面的普适性框架',
    ),
    'research-track.html': (
        '失效不是“没做成”',
        '候选普适类；或明确映射失效',
        '不展示项目未发表数值',
    ),
    'reproduction-lab-09.html': (
        '拟合区间稳定性：未通过',
        '普适 β 结论：不授权',
        '回归分析已知答案测试：通过',
    ),
    'reproduction-lab-10.html': (
        '小尺寸 QEW 超粗糙特征：通过',
        '热力学 ζ 闭合：未通过',
        '不能挑出 1.316 或 1.201 中的任何一个',
    ),
    'reproduction-lab-11.html': (
        '尺寸区间稳定性：未通过',
        '普适 ν 结论：不授权',
        'ν=1.318867',
    ),
    'reproduction-lab-12.html': (
        '热圆整拟合区间稳定性：未通过',
        '普适 ψ 结论：不授权',
        '低温蠕变渐近区：尚未解析',
        '蠕变律 / μ 结论：不授权',
        'Brownian（布朗）噪声归一化测试',
    ),
}

FIGURE_READING_V2 = {
    'pinning-creep.html': {
        'Tybell Fig.3': 'tybell2002-fig3-creep.png',
        'Paruch Fig.3': 'paruch2005-fig3-roughness.png',
        'Kim Fig.1': 'kim2014-fig1-pinning-display.webp',
    },
    'depinning.html': {
        'Rosso Fig.2': 'rosso2003-fig2-critical-roughness.png',
        'Ferrero Fig.3': 'ferrero2013-fig3-nonsteady-velocity.png',
        'Wiese Fig.22': 'wiese2022-fig22-depinning-phenomenology.png',
    },
    'disorder-rfim.html': {
        'Drossel Fig.3(a)': 'drossel1998-fig3a-percolative-wall.png',
        'Zhou Fig.2': 'zhou2012-fig2-anomalous-roughness.png',
        'Paul Fig.4': 'paul2026-fig4-multidomain-disorder.webp',
    },
}


def visible_text(raw: str) -> str:
    soup = BeautifulSoup(raw, 'html.parser')
    for selector in ('.source-text', 'pre', 'code', 'script', 'style'):
        for node in soup.select(selector):
            node.decompose()
    return ' '.join(soup.stripped_strings)


def resolve_local(page: Path, value: str) -> Path | None:
    if not value or value.startswith(('#', 'mailto:', 'javascript:', 'data:')):
        return None
    parts = urlsplit(value)
    if parts.scheme or parts.netloc:
        return None
    rel = parts.path
    if not rel:
        return None
    return (page.parent / rel).resolve()


def assert_wiring(page: Path, raw: str) -> None:
    soup = BeautifulSoup(raw, 'html.parser')
    if soup.find('h1') is None:
        raise RuntimeError(f'{page.name}: missing h1')
    if not soup.find_all('a'):
        raise RuntimeError(f'{page.name}: no links found')

    root_resolved = ROOT.resolve()
    for img in soup.find_all('img'):
        target = resolve_local(page, img.get('src', ''))
        if target is None:
            continue
        if root_resolved not in target.parents and target != root_resolved:
            raise RuntimeError(f'{page.name}: image escapes repository root: {img.get("src")}')
        if not target.exists():
            raise RuntimeError(f'{page.name}: missing image asset: {img.get("src")}')

    for a in soup.find_all('a'):
        href = a.get('href', '')
        target = resolve_local(page, href)
        if target is None or target.suffix.lower() != '.html':
            continue
        if root_resolved not in target.parents and target != root_resolved:
            raise RuntimeError(f'{page.name}: link escapes repository root: {href}')
        if not target.exists():
            raise RuntimeError(f'{page.name}: missing local HTML target: {href}')


def assert_teaching_v2_order(page: Path, raw: str) -> None:
    if page.name == 'pinning-creep.html':
        order = (
            '第一次读这一章：',
            '1 · Tybell 2002',
            '2 · Paruch 2005',
            '进阶研究方法 · 粗糙度验收判据',
            '3 · Kim 2014',
            '下一章的问题因此非常明确',
        )
        positions = [raw.index(x) for x in order]
        if positions != sorted(positions):
            raise RuntimeError('Module 04 Teaching V2 order regressed')

    if page.name == 'depinning.html':
        order = (
            '第一次读本章，先走四步：',
            '1 · Chauve 2000',
            '2 · Rosso 2003',
            '3 · Ferrero 2013',
            '4 · Wiese 2022',
            '进阶研究方法 A · 坍缩验收判据',
            '进阶研究方法 B · 阈值推断阶梯',
            '进阶研究方法 C · 指数提取纪律',
            '下一章必须把无序本身拆开',
            '<div class="next">',
        )
        positions = [raw.index(x) for x in order]
        if positions != sorted(positions):
            raise RuntimeError('Module 05 Teaching V2 order regressed')

    if page.name == 'disorder-rfim.html':
        order = (
            '第一次读本章，先把问题分成四层：',
            '0 · 先拆掉最容易混淆的三个词',
            '1 · Dahmen &amp; Sethna 1996',
            '2 · Drossel &amp; Dahmen 1998',
            '3 · Zhou, Zheng &amp; He',
            '研究桥接 · 真实滑移铁电里的无序到底是什么？',
            '回到滑移铁电：什么时候该用哪一级模型？',
        )
        positions = [raw.index(x) for x in order]
        if positions != sorted(positions):
            raise RuntimeError('Module 06 Teaching V2 order regressed')
        if raw.count('Paul et al. 2026') != 1:
            raise RuntimeError('Module 06 Paul 2026 evidence block duplicated or missing')


def assert_figure_reading_v2(page: Path, raw: str) -> None:
    expected = FIGURE_READING_V2.get(page.name)
    if expected is None:
        return

    soup = BeautifulSoup(raw, 'html.parser')
    guides = soup.select('.fig-read[data-figure-read]')
    if len(guides) != len(expected):
        raise RuntimeError(f'{page.name}: expected {len(expected)} Figure Reading V2 guides, found {len(guides)}')

    names = [g.get('data-figure-read') for g in guides]
    if set(names) != set(expected):
        raise RuntimeError(f'{page.name}: Figure Reading V2 guide names drifted: {names}')

    for guide in guides:
        name = guide.get('data-figure-read')
        text = ' '.join(guide.stripped_strings)
        for heading in ('先看哪里', '看到什么', '能证明 / 不能证明'):
            if heading not in text:
                raise RuntimeError(f'{page.name}: {name} missing Figure Reading heading: {heading}')

        figure = guide.find_previous_sibling('figure')
        if figure is None:
            raise RuntimeError(f'{page.name}: {name} is not immediately preceded by a figure')
        img = figure.find('img')
        src = img.get('src', '') if img else ''
        if expected[name] not in src:
            raise RuntimeError(f'{page.name}: {name} guide attached to wrong figure: {src}')

    if '.fig-read{' not in raw or '@media(max-width:760px){.fig-read{grid-template-columns:1fr}}' not in raw:
        raise RuntimeError(f'{page.name}: Figure Reading V2 responsive CSS missing')


def main() -> None:
    missing = [str(p.relative_to(ROOT)) for p in PAGES if not p.exists()]
    if missing:
        raise RuntimeError(f'Final-audit pages missing: {missing}')

    for page in PAGES:
        raw = page.read_text(encoding='utf-8')
        before = raw
        visible = visible_text(raw)
        padded_lower = f' {visible.lower()} '

        for token in FORBIDDEN_VISIBLE:
            if token in visible:
                raise RuntimeError(f'{page.name}: visible Language V2 residue: {token}')
        for token in FORBIDDEN_VISIBLE_LOWER:
            if token in padded_lower:
                raise RuntimeError(f'{page.name}: visible workflow-English residue: {token.strip()}')

        assert_wiring(page, raw)
        assert_teaching_v2_order(page, raw)
        assert_figure_reading_v2(page, raw)

        for anchor in CRITICAL_ANCHORS.get(page.name, ()):
            if anchor not in raw:
                raise RuntimeError(f'{page.name}: critical scientific/teaching boundary missing: {anchor}')

        if page.name == 'depinning.html':
            for anchor in (
                '6 · 热圆整：',
                '一维弹性线的数值研究',
                '阈值分布展宽',
                'T=0 阈值应先独立闭合',
                '坍缩应该是待检验结果，不是数据预处理步骤',
            ):
                if anchor not in raw:
                    raise RuntimeError(f'Module 05 final wording/science anchor missing: {anchor}')

        if page.name == 'reproduction-lab.html':
            if '剖面 RMSE =' not in raw:
                raise RuntimeError('Lab 01: visible Chinese RMSE label missing')
            if '<pre' not in raw or 'profile RMSE' not in raw:
                raise RuntimeError('Lab 01: machine-output profile RMSE label unexpectedly missing')

        if page.name == 'reproduction-lab-08.html':
            for anchor in ('<b>稳态速度 v</b>', '本课不拟合 β', '不足以证明临界标度'):
                if anchor not in raw:
                    raise RuntimeError(f'Lab 08 final wording/science anchor missing: {anchor}')

        if page.read_text(encoding='utf-8') != before:
            raise RuntimeError(f'{page.name}: read-only final seal changed page bytes')

    print(f'FULL-SITE LANGUAGE + TEACHING + FIGURE READING V2 FINAL SEAL PASS: {len(PAGES)} teaching pages checked read-only.')
    print('Teaching V2 order and Figure Reading V2 phase 1 are locked for modules 04–06; scientific figures may retain original English labels.')


if __name__ == '__main__':
    main()
