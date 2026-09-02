from __future__ import annotations

import re
from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

# Second, page-scoped Language V2 audit for Module 05.  This is intentionally
# not a bulk site pass: later pages must be reviewed in sequence.
TARGET = ROOT / "modules/depinning.html"

REPLACEMENTS = {
    # Reader-facing editorial / provenance language.
    "APS official record": "APS 官方记录",
    "Figure 为对应 PDF 派生的无损 PNG": "论文图为对应 PDF 派生的无损 PNG",
    "elastic-energy 模型": "弹性能模型",
    "inset 检查": "插图检查",
    "滑移铁电 simulation": "滑移铁电模拟",
    "nonuniversal 尺度": "非普适尺度",
    "1D elastic-string / uncorrelated-无序模型": "一维弹性线 / 无关联无序模型",
    "joint 速度标度函数": "联合速度标度函数",
    "sharp 退钉扎": "尖锐的退钉扎临界点",
    "threshold-distribution broadening": "阈值分布展宽",
    "activated 动力学": "热激活动力学",

    # Collapse / finite-size audit prose.
    "各 size 有共同支持的 rescaled-x 区间": "各尺寸共同覆盖的重标度 x 区间",
    "sampling 不确定性": "抽样不确定性",
    "允许估计的 scaling 参数": "允许估计的标度参数",
    "endpoint leverage": "端点影响",
    "prediction 残差": "预测残差",
    "剩余 sizes": "剩余尺寸",
    "重新 rescale 后": "重新重标度后",
    "master-curve 不确定性 band": "主曲线不确定性带",
    "当前 size 区间": "当前尺寸区间",
    "有限尺寸 effects": "有限尺寸效应",
    "留出尺寸 prediction": "留出尺寸预测",
    "challenge size": "挑战尺寸",
    "core sizes": "核心尺寸",
    "指数 ratios": "指数比值",
    "master-curve rule": "主曲线规则",
    "交叉区 length": "交叉区长度",
    "几何 dependence": "几何依赖",
    "最小 correction": "最小标度修正",
    "correction 模型": "修正模型",
    "correction 参数": "修正参数",
    "同一批 sizes / 无序样本": "同一批尺寸 / 无序样本",
    "三张 panel": "三张分图",
    "C0 · visual": "C0 · 目视",
    "手工 rescale 后看似重合": "手工重标度后看似重合",
    "illustrative 坍缩 only": "仅为示意性坍缩",
    "quantitative scaling 候选": "定量标度候选",
    "endpoint/区间敏感性通过": "端点 / 区间敏感性通过",
    "有限尺寸标度 supported over tested 区间": "已测试区间内支持有限尺寸标度",
    "C3 · predictive": "C3 · 预测",
    "留出尺寸 lands without retuning + independent 可观测量交叉核验": "留出尺寸无需重新调参即可落在主曲线上 + 独立可观测量交叉核验",
    "strong 普适性证据, subject to 映射 validity": "较强的普适性证据，但仍受映射有效性约束",
    "scaling illustration": "标度示意",
    "普适性 closure": "普适性闭合",

    # Threshold inference ladder / numerical QC prose.
    "阈值 inference ladder": "阈值推断阶梯",
    "diffuse-界面模型": "弥散界面模型",
    "阈值区间或 bound": "阈值区间或边界",
    "convex 弹性流形": "凸弹性流形",
    "“exact 阈值”": "“精确阈值”",
    "Initial-态 stability": "初态稳定性",
    "零场 relax 后": "零场弛豫后",
    "Numerical 数值证明": "数值有效性",
    "NaN / divergence": "NaN / 发散",
    "求解器-specific": "求解器特定的",
    "detached 畴": "脱离主体的畴",
    "场-onset": "加场初期",
    "Go / no-go": "通过 / 不通过",
    "扩大场 grid": "加密场网格",
    "resolved-运动态": "已解析运动态",
    "velocity / displacement 判据": "速度 / 位移判据",
    "upper 阈值区间": "阈值上界",
    "resolved-钉扎态 under 观测时长": "给定观测时长内的已解析钉扎态",
    "lower 阈值区间": "阈值下界",
    "场 probes": "场探针点",
    "区间 / bound 信息": "区间 / 边界信息",
    "总体 distribution / 配对差值": "总体分布 / 配对差值",
    "censored 来源": "删失来源",
    "自助法 resamples": "自助法重采样",
    "新增的无序无序样本": "新增的无序样本",

    # Exponent / roughness audit prose.
    "rough 畴壁图": "粗糙畴壁图",
    "全局 width": "全局宽度",
    "谱 scaling": "谱标度",
    "UV/grid 截止": "UV / 网格截止",
    "finite size": "有限尺寸",
    "畴壁 extraction": "畴壁提取",
    "失效 anchor": "失效对照",
    "overhang study": "悬垂研究",
    "spatial 多重标度": "空间多重标度",

    # Ordinary workflow English still left by the first pass.
    " force 的原始松弛曲线": "驱动力的原始松弛曲线",
    " finite v 与 0": "有限速度与 0",
    "scaling": "标度",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    # Source quotations and displayed formulas are authority content: neither
    # may be rewritten by Language V2 cleanup.
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    before_sources = source_blocks(soup)
    before_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]

    # Normalize visible navigation labels without changing anchor ids.
    nav = soup.select("header .bar span a")
    nav_labels = ["知识图谱", "临界几何", "非稳态松弛", "标度关系", "阈值推断"]
    for link, label in zip(nav, nav_labels):
        link.string = label

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for a, b in sorted(REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
            new = new.replace(a, b)
        # Repair legacy spacing only in prose, never in source quotations or equations.
        new = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", new)
        new = re.sub(r"\s+([，。；：！？、）])", r"\1", new)
        if new != old:
            node.replace_with(new)

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 05 source-text changed during second Language V2 audit")
    after_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]
    if after_equations != before_equations:
        raise RuntimeError("Module 05 displayed equation changed during Language V2 audit")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
