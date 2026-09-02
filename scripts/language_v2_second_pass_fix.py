from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/research-track.html"

REPLACEMENTS = (
    (
        '<meta content="Research bridge from sliding-ferroelectric switching to disorder coupling, isolated-wall depinning and universality tests." name="description"/>',
        '<meta content="从滑移铁电翻转、无序耦合到孤立畴壁退钉扎与普适性检验的研究路线。" name="description"/>',
    ),
    (
        '公式中的 periodic scalar model（周期标量模型） 是教学 / 研究用有效模型',
        '公式中的周期标量模型是教学 / 研究用有效模型',
    ),
    (
        'RMS、能量方差、局域力 RMS 等不同定义并不自动等价。',
        'RMS（均方根）、能量方差、局域力 RMS 等不同定义并不自动等价。',
    ),
    ('临近阈值 · 热圆滑', '临近阈值 · 热圆整'),
    ('<b>最重要的防过拟合规则：</b>热圆滑必须继承独立 T=0 阈值。', '<b>最重要的防过拟合规则：</b>热圆整必须继承独立 T=0 阈值。'),
    ('模块 05：怎么测热圆滑 / ψ', '模块 05：怎么测热圆整 / ψ'),
    ('<td>热圆滑</td>', '<td>热圆整</td>'),
    ('有效钉扎态 up to E<sub>max</sub>，仍未见运动态', '有效钉扎态直到 E<sub>max</sub>，仍未见运动态'),
    ('观测时间不足以区分 late 运动', '观测时间不足以区分迟发运动'),
    ('通过拓扑 / 单值性判据的畴壁 extraction', '通过拓扑 / 单值性判据的畴壁提取'),
    ('判据 / 区间 / 事件检测器 / extraction 敏感性', '判据 / 区间 / 事件检测器 / 提取敏感性'),
    ('冻结的事件检测器 / size 定义', '冻结的事件检测器 / 事件大小定义'),
    ('CI / 自助法 / 模型的最外层重采样单元', '置信区间 / 自助法 / 模型的最外层重采样单元'),
    ('热/事件/cycle 等内层重复', '热噪声 / 事件 / 循环等内层重复'),
    ('跨 stage 一致的碎裂排序', '跨翻转阶段一致的碎裂排序'),
    ('← 回到 07 Numerical 模型ing（数值建模）', '← 回到 07 数值建模'),
)

REQUIRED = (
    'Research Track（研究路线）',
    '周期标量模型是教学 / 研究用有效模型',
    'RMS（均方根）',
    'Gaussian white random field（高斯白噪声随机场）',
    'stacking registry（堆垛配位）',
    'Langevin（朗之万）',
    '临近阈值 · 热圆整',
    '热圆整必须继承独立 T=0 阈值',
    '有效钉扎态直到 E',
    '迟发运动',
    '畴壁提取',
    '事件大小定义',
    '置信区间 / 自助法 / 模型的最外层重采样单元',
    '热噪声 / 事件 / 循环等内层重复',
    '跨翻转阶段一致的碎裂排序',
    '失效不是“没做成”',
    '候选普适类；或明确映射失效',
    '← 回到 07 数值建模',
)

FORBIDDEN = (
    'periodic scalar model（周期标量模型）',
    'RMS、能量方差、局域力 RMS',
    '热圆滑',
    ' up to E',
    'late 运动',
    '畴壁 extraction',
    'extraction 敏感性',
    'size 定义',
    'CI / 自助法',
    'cycle 等内层重复',
    '跨 stage',
    'Numerical 模型ing',
)

LOCKED_SCIENCE = (
    'F<sub>RF</sub> = −h(r) cos[φ−α(r)]',
    'F<sub>RB</sub> = δV(r)[1−cos(nφ)]',
    'v∼(E−E<sub>c</sub>)<sup>β</sup>',
    'v(f<sub>c</sub>,T)∼T<sup>ψ</sup>',
    'P(φ)=P<sub>0</sub> sinφ',
    'std(h<sub>cell</sub>)∝dx<sup>−d/2</sup>',
    'β<sub>eff</sub> 持续漂移',
    '不能因为数值上“像一个阈值”就重命名成退钉扎临界场',
    '不展示项目未发表数值',
)


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    before = BeautifulSoup(raw, "html.parser")
    before_hrefs = [x.get("href") for x in before.find_all("a")]
    before_eq = [x.get_text(" ", strip=True) for x in before.select(".eq")]
    before_sources = [x.get_text(" ", strip=True) for x in before.select(".source-text")]
    before_science = {token: raw.count(token) for token in LOCKED_SCIENCE}

    out = raw
    for old, new in REPLACEMENTS:
        if old not in out:
            raise RuntimeError(f"Research Track expected cleanup fragment missing: {old}")
        out = out.replace(old, new, 1)

    after = BeautifulSoup(out, "html.parser")
    if before_hrefs != [x.get("href") for x in after.find_all("a")]:
        raise RuntimeError("Research Track href wiring changed")
    if before_eq != [x.get_text(" ", strip=True) for x in after.select(".eq")]:
        raise RuntimeError("Research Track equations changed")
    if before_sources != [x.get_text(" ", strip=True) for x in after.select(".source-text")]:
        raise RuntimeError("Research Track paper-original source text changed")
    for token, count in before_science.items():
        if out.count(token) != count:
            raise RuntimeError(f"Research Track locked scientific statement changed: {token}")

    visible = after.get_text(" ", strip=True)
    for token in REQUIRED:
        if token not in visible:
            raise RuntimeError(f"Research Track required Language V2 text missing: {token}")
    for token in FORBIDDEN:
        if token in visible:
            raise RuntimeError(f"Research Track ordinary workflow English remains visible: {token}")

    TARGET.write_text(out, encoding="utf-8")
    print("Research Track Language V2 repair complete; equations, links and scientific claim boundaries unchanged.")


if __name__ == "__main__":
    main()
