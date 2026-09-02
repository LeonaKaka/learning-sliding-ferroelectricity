from __future__ import annotations

import re
from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

# Final page-scoped Language V2 audit for Module 07.  This pass is intentionally
# small and idempotent: it repairs residual prose from earlier passes without
# reopening the scientific formulas, quotations, or figure wiring.
TARGET = ROOT / "modules/numerical-modeling.html"

REPLACEMENTS = {
    "项目项目 Drive PDF": "项目 Drive PDF",
    "elastic-line model（elastic-line model（弹性线模型））": "elastic-line model（弹性线模型）",
    "解析 kink（孤子）（孤子）": "解析 kink（孤子）",
    "比值s": "比值",
    "gradient 刚度": "梯度刚度",
    "畴壁能量 / tension": "畴壁能量 / 张力",
    "极化 amplitude / 静电耦合 convention": "极化幅度 / 静电耦合约定",
    "electric-drive energy": "电驱动能量",
    "relaxation time": "弛豫时间",
    "P–E 回线 / coercive 尺度": "P–E 回线 / 矫顽尺度",
    "综合 response": "综合响应",
    "在这个 normalization 下": "在这个归一化下",
    "畴壁 profile / energy": "畴壁剖面 / 能量",
    "① Structural prior": "① 结构先验",
    "② Clean 静态性质": "② 无序为零的静态性质",
    "③ Clean 动力学": "③ 无序为零的动力学",
    "迁移率 / relaxation": "迁移率 / 弛豫",
    "kinetic 参数": "动力学参数",
    "物理 amplitude": "物理幅度",
    "morphology、阈值、size/温度 response": "形貌、阈值、尺寸 / 温度响应",
    "校准 closure": "校准闭合",

    "overdamped TDGL": "overdamped（过阻尼）TDGL",
    "过阻尼（过阻尼）TDGL": "过阻尼 TDGL",
    "该 normalization": "该归一化",
    "constant Γ + additive Gaussian white 噪声": "常数 Γ + 加性高斯白噪声",
    "stochastic calculus": "随机微积分",
    "derivative 噪声": "导数项噪声",
    "update 噪声": "每步增量噪声",
    "离散 cell 的 measure": "离散网格单元的测度",
    "噪声 rate": "噪声率",
    "rate amplitude": "噪声率幅度",
    "Euler update": "Euler（欧拉）更新",
    "随机 increment": "随机增量",
    "quenched RF": "淬火 RF",
    "温度 convention": "温度约定",
    "cell 变小后热噪声 rate": "网格单元变小后热噪声率",
    "每格 random amplitude": "每个网格单元的随机幅度",
    "热噪声 rate": "热噪声率",
    "update 标准差": "每步增量标准差",
    "噪声–耗散 convention": "噪声–耗散约定",
    "噪声 amplitude": "噪声幅度",
    "粗粒化 convention": "粗粒化约定",
    "同一个 quenched 景观": "同一个淬火无序景观",
    "有限温条件 response": "有限温条件响应",
    "无序无序样本": "无序样本",

    "原来的 single-畴壁 v 定义失效": "原来的单畴壁 v 定义失效",
    "失效 analysis": "失效分析",
    "是否 unwrap": "是否完成周期展开",
    "换 late 区间后 slope 是否稳定": "更换后段区间后斜率是否稳定",
    "从 diffuse 相场提取": "从弥散相场提取",
    "模型 reduction": "模型约化",
    "指定 separator": "指定分隔线",
    "层级-set 敏感性": "水平集敏感性",
    "等值线 thresholds": "等值线阈值",
    "均值 velocity": "平均速度",
    "粗糙度 scaling": "粗糙度标度",
    "diffuse-core": "弥散畴壁核心区",
    "悬垂/multiple-畴壁候选": "悬垂 / 多畴壁候选",
    "area-based 交叉核验": "基于面积的交叉核验",
    "畴-area change": "畴面积变化",
    "粗糙度 triple": "三种粗糙度估计",
    "grid-尺度、畴壁-width 与体系-size": "网格尺度、畴壁宽度与体系尺寸",
    "单值 elastic 流形": "单值弹性流形",
    "numerical 数值证明": "数值有效性证明",
    "缩 bracket": "缩小夹定区间",

    "commit + 未提交改动标记 + patch/tree hash": "提交 + 未提交改动标记 + 补丁 / 源码树哈希",
    "在 raw 运行处断掉": "在原始运行处断掉",
    "正文结论再指向 panel": "正文结论再指向图中分区",
    "进入 Research Track → →": "进入 Research Track →",
    "08 Current Frontiers（当前前沿）（当前前沿） →": "08 Current Frontiers（当前前沿） →",
}


def formula_blocks(soup: BeautifulSoup) -> list[str]:
    """Capture mathematical expression text, excluding explanatory <small>."""
    out: list[str] = []
    for el in soup.select(".eq"):
        clone = BeautifulSoup(str(el), "html.parser").select_one(".eq")
        if clone is None:
            continue
        for small in clone.find_all("small"):
            small.decompose()
        out.append(clone.get_text(" ", strip=False))
    return out


def inside_eq(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None:
        return False
    return "eq" in parent.get("class", []) or parent.find_parent(class_="eq") is not None


def inside_eq_small(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None:
        return False
    small = parent if parent.name == "small" else parent.find_parent("small")
    return small is not None and small.find_parent(class_="eq") is not None


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    if inside_eq(node) and not inside_eq_small(node):
        return True
    return False


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    before_sources = source_blocks(soup)
    before_images = [(img.get("src"), img.get("alt")) for img in soup.find_all("img")]
    before_figure_links = [a.get("href") for a in soup.select("figure a")]

    # This .eq card is a statistics hierarchy, not a scientific formula. Translate
    # its teaching labels explicitly, then freeze every actual equation below.
    hierarchy_old = "独立淬火无序样本 i → thermal seeds j → 轨迹 frames t"
    hierarchy_new = "独立淬火无序样本 i → 热噪声随机种子 j → 轨迹帧 t"
    for el in soup.select(".eq"):
        if el.get_text(" ", strip=True) == hierarchy_old:
            el.string = hierarchy_new
            break

    before_formulae = formula_blocks(soup)

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for a, b in sorted(REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
            new = new.replace(a, b)
        new = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", new)
        new = re.sub(r"\s+([，。；：！？、）])", r"\1", new)
        if new != old:
            node.replace_with(new)

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 07 source-text changed during final Language V2 cleanup")
    if formula_blocks(soup) != before_formulae:
        raise RuntimeError("Module 07 mathematical formula changed during final Language V2 cleanup")
    if [(img.get("src"), img.get("alt")) for img in soup.find_all("img")] != before_images:
        raise RuntimeError("Module 07 image src/alt changed during final Language V2 cleanup")
    if [a.get("href") for a in soup.select("figure a")] != before_figure_links:
        raise RuntimeError("Module 07 figure link changed during final Language V2 cleanup")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
