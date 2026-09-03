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

        for anchor in CRITICAL_ANCHORS.get(page.name, ()):
            if anchor not in raw:
                raise RuntimeError(f'{page.name}: critical scientific boundary missing: {anchor}')

        if page.name == 'reproduction-lab.html':
            if '剖面 RMSE =' not in raw:
                raise RuntimeError('Lab 01: visible Chinese RMSE label missing')
            if '<pre' not in raw or 'profile RMSE' not in raw:
                raise RuntimeError('Lab 01: machine-output profile RMSE label unexpectedly missing')

        if page.read_text(encoding='utf-8') != before:
            raise RuntimeError(f'{page.name}: read-only final seal changed page bytes')

    print(f'FULL-SITE LANGUAGE V2 FINAL SEAL PASS: {len(PAGES)} teaching pages checked read-only.')
    print('Scientific figures may retain original English labels; source/code/machine-output text is excluded from prose-language checks.')


if __name__ == '__main__':
    main()
