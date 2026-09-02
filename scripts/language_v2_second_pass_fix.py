from __future__ import annotations

import re
from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

TARGET = ROOT / "modules/depinning.html"

REPLACEMENTS = {
    "Short-time-dynamics 标度": "短时动力学标度",
    "diffuse 畴壁": "弥散畴壁",
    "速度 / displacement 判据": "速度 / 位移判据",
    "预注册 QC": "预注册质检标准",
    "数值与拓扑 QC": "数值与拓扑质检",
    "观测时长-limited": "受观测时长限制",
    "late 运动": "晚时运动",
    "数据-integrity QC": "数据完整性质检",
    "single-畴壁映射": "单畴壁映射",
    "resolved-钉扎态": "已解析钉扎态",
    "Bracket invariant": "阈值区间不变量",
    "Registered tolerance": "预注册容差",
    "阈值区间 width": "阈值区间宽度",
    "E<sub>max</sub> still 钉扎态": "E<sub>max</sub> 仍为钉扎态",
    "infinite 阈值": "无限大阈值",
    "Invalid in the middle": "中间点无效",
    "numerical validity": "数值有效性",
    "当前 sizes": "当前尺寸",
    "f<sub>c</sub>(L) shift": "f<sub>c</sub>(L) 漂移",
    "full 坍缩": "完整坍缩",
    "nonsteady 动力学": "非稳态动力学",
    "带带系统偏置": "带系统偏置",
    "quenched 无序样本": "淬火无序样本",
    "交叉区 / correction": "交叉区 / 标度修正",
    "尺度窗与 extraction 敏感性": "尺度区间与提取敏感性",
    "尺度-dependent / anomalous 粗糙度": "尺度依赖 / 异常粗糙度",
    "fixed analysis rule": "固定分析规则",
    "有限尺寸交叉区, no 普适性结论": "有限尺寸交叉区，不支持普适性结论",
    "退钉扎-like / 有效界面区间 only": "类退钉扎 / 仅限有效界面区间",
    "size 与畴壁-extraction rules": "尺寸与畴壁提取规则",
    "Data → Estimator → Evidence → Claim contract": "数据 → 估计量 → 证据 → 结论契约",
    "界面 height /": "界面高度 /",
    "elastic kernel": "elastic kernel（弹性核）",
    "triangle-回线": "三角波回线",
    "coercive 阈值": "矫顽阈值",
    "full-switching vs isolated-wall protocol": "完整翻转 vs 孤立畴壁流程",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
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

    next_links = soup.select(".next a")
    if len(next_links) >= 2:
        next_links[0].string = "← 04 Pinning（钉扎）、Creep（蠕变）与 Roughness（粗糙度）"
        next_links[1].string = "06 Disorder（无序）与 RFIM →"

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 05 source-text changed during final Language V2 cleanup")
    after_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]
    if after_equations != before_equations:
        raise RuntimeError("Module 05 displayed equation changed during final Language V2 cleanup")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
