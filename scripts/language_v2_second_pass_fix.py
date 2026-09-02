from __future__ import annotations

import re
from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

# Page-by-page Language V2 repair.  Keep this pass scoped to Module 05.
TARGET = ROOT / "modules/depinning.html"

REPLACEMENTS = {
    "Module 04": "模块 04",
    "Module 05": "模块 05",
    "published PDF": "正式发表 PDF",
    "点击 Figure 看": "点击图片查看",
    "force–速度": "驱动力–速度",
    "freeze T=0 依据": "冻结 T=0 依据",
    "小 热 pilot": "小规模有限温预检",
    "stochastic integrator": "随机积分器",
    "速度 floor": "速度下限",
    "观测 time": "观测时间",
    "来源层级 uncertainty": "来源层级不确定性",
    "uncertainty": "不确定性",
    "quenched 样本": "淬火无序样本",
    "deep 阈值以下 区间": "深阈值下区间",
    "multiple walls": "多畴壁",
    "速度 scaling": "速度标度",
    "characteristic length": "特征长度",
    "failure 也要保留": "失效结果也要保留",
    "finite T": "有限温",
    "finite-T": "有限温",
    "finite-size": "有限尺寸",
    "creep recipe": "蠕变测量方案",
    "activated 区间": "热激活区间",
    "scaling ansatz": "标度假设",
    "optimization / goodness-of-坍缩": "优化 / 坍缩优度",
    "eligible size set": "可用尺寸集合",
    "reference-curve rule": "参考曲线规则",
    "weighting": "权重方案",
    "场 points": "场点",
    "Cross-可观测量 判据": "跨可观测量判据",
    "Cross-可观测量": "跨可观测量",
    "threshold classifier": "阈值分类器",
    "classifier": "分类器",
    "无序样本s": "无序样本",
    "near-临界 速度 grid": "近临界速度网格",
    "指数 extraction discipline": "指数提取纪律",
    "systematic 偏置 的 有效指数s": "带系统偏置的有效指数",
    "systematic 偏置": "系统偏置",
    "nonsteady 判据": "非稳态判据",
    "censored / 未解析": "删失或未解析",
    "场 rows": "场点",
    "pairing / censoring hierarchy": "配对 / 删失层级",
    "配对 阈值 comparison": "配对阈值比较",
    "速度 analysis": "速度分析",
    "reduced drive": "约化驱动力",
    "reduced-force": "约化驱动力",
    "bracket / f": "阈值区间 / f",
    "bracket": "阈值区间",
    "scaling object": "标度对象",
    "finite T 触发": "有限温触发",
    "scaling 对窗口": "标度对区间",
    "scaling 有候选": "标度存在候选关系",
    "数据 坍缩": "数据坍缩",
    "有限尺寸 坍缩": "有限尺寸坍缩",
    "坍缩 验收 判据": "坍缩验收判据",
    "goodness-of-坍缩": "坍缩优度",
    "场/reduced-force 区间 族": "场 / 约化驱动力区间族",
    "场/reduced-force": "场 / 约化驱动力",
    "插值 / reference-curve rule": "插值 / 参考曲线规则",
    "optimization": "优化",
    "pilot": "预检",
    "thermal rounding": "thermal rounding（热圆滑）",
    "热-rounding": "热圆滑",
    "rounding": "热圆滑",
    "effective exponent": "有效指数",
    "effective 指数": "有效指数",
    "effective slopes": "有效斜率",
    "effective slope": "有效斜率",
    "effective": "有效",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    return bool(parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []))


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    before_sources = source_blocks(soup)

    # Browser title and visible page framing were damaged by the previous
    # mechanical pass.  Paper titles/source quotations are not touched.
    if soup.title:
        soup.title.string = "Depinning（退钉扎）· 临界现象 · Learning Sliding Ferroelectricity"
    header_small = soup.select_one("header .bar b small")
    if header_small:
        header_small.string = "· 05 Depinning（退钉扎）"
    crumb = soup.select_one("main > .rule")
    if crumb:
        # Preserve the home link, only normalize the trailing label.
        for node in list(crumb.find_all(string=True)):
            if "Depinning as a Critical Phenomenon" in str(node):
                node.replace_with(str(node).replace("Depinning as a Critical Phenomenon", "05 Depinning（退钉扎）· 临界现象"))

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for a, b in sorted(REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
            new = new.replace(a, b)
        # Historical bulk replacement inserted spaces between Chinese words.
        new = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", new)
        new = re.sub(r"\s+([，。；：！？、）])", r"\1", new)
        new = re.sub(r"（\s+", "（", new)
        if new != old:
            node.replace_with(new)

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 05 source-text changed during Language V2 repair")
    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
