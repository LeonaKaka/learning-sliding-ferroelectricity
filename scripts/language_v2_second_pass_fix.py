from __future__ import annotations

import re
from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

# Language V2 is reviewed page by page. Keep this pass scoped to Module 08.
TARGET = ROOT / "modules/current-frontiers.html"

REPLACEMENTS = {
    # Page framing / provenance.
    "Current Frontiers · Learning Sliding Ferroelectricity": "Current Frontiers（当前前沿） · Learning Sliding Ferroelectricity",
    "· 08 Current Frontiers": "· 08 Current Frontiers（当前前沿）",
    "Map": "知识图谱",
    "Evidence score": "证据评分",
    "What is missing?": "缺失证据",
    " / Current Frontiers": " / 08 Current Frontiers（当前前沿）",
    "原 Figure": "原论文图",
    "HTML text": "HTML 真文本",
    "Drive PDF": "项目 Drive PDF",
    "Module 02": "模块 02",
    "Module 03": "模块 03",
    "07 Numerical Modeling": "07 Numerical Modeling（数值建模）",

    # Opening synthesis and evidence matrix.
    "滑移铁电 畴壁故事": "滑移铁电畴壁故事",
    "关键 可观测量": "关键可观测量",
    "审一篇 前沿论文": "审一篇前沿论文",
    "畴壁 主导": "畴壁主导",
    "不同界面 钉扎 中心": "不同界面钉扎中心",
    "光学 堆垛 图": "光学堆垛图",
    "机制指向 畴壁": "机制指向畴壁",
    "讨论 外在 对称性破缺": "讨论外在对称性破缺",
    "非 无序 v(E)": "无序为零时的 v(E)",
    "只有 畴壁 附近受横向力": "只有畴壁附近受横向力",
    "洁净/超润滑 畴壁": "洁净 / 超润滑畴壁",
    "MD 空间轨迹": "MD 空间轨迹",
    "淬火-无序": "淬火无序",
    "封闭小畴 / 粗糙边缘 钉扎-退钉扎": "封闭小畴 / 粗糙边缘的钉扎–退钉扎",
    "连续 恒场 v(E) 临界 曲线": "连续恒场 v(E) 临界曲线",
    "停留时间 / 表观 临界-场 变化": "停留时间 / 表观临界场变化",
    "器件尺度 拉曼图": "器件尺度拉曼图",
    "FC 单畴 3R-TMD": "FC（完全公度）单畴 3R-TMD",
    "无畴壁 翻转": "无畴壁翻转",
    "畴壁 必要性": "畴壁必要性",
    "多畴 畴壁/AA 钉扎": "多畴畴壁 / AA 钉扎",
    "结构 验证": "结构验证",
    "耦合 多个 畴壁": "耦合多个畴壁",
    "分阶段 路径": "分阶段路径",
    "原子级 模拟 轨迹": "原子级模拟轨迹",
    "位移–时间 / 速度 动力学": "位移–时间 / 速度动力学",
    "临界退钉扎 曲线": "临界退钉扎曲线",

    # Frontier verdict and structural boundaries.
    "前沿 verdict": "前沿判断",
    "畴壁-containing 滑移铁电": "含畴壁的滑移铁电",
    "堆垛-已解析": "堆垛分辨",
    "完全公度 单畴": "完全公度单畴",
    "预存 畴壁": "预存畴壁",
    "多个界面 与 耦合畴壁": "多个界面与耦合畴壁",
    "翻转通道": "翻转通道",
    "孤立畴壁 条件": "孤立畴壁条件",
    "无预存 畴壁/AA 网络": "无预存畴壁 / AA 网络",
    "nonpolar 中间畴": "非极性中间畴",
    "自动 粗粒化": "自动粗粒化",

    # Liang section.
    "无序-敏感 可观测量": "对无序敏感的可观测量",
    "同样净 极化": "相同净极化",
    "不同 堆垛": "不同堆垛",
    "翻转路径 本身": "翻转路径本身",
    "界面的 畴壁": "界面的畴壁",
    "中间 堆垛 态": "中间堆垛态",
    "循环-dependent 路径": "循环依赖的路径",
    "不同 界面 的 俘获 competition": "不同界面的钉扎竞争",
    "畴壁 速度": "畴壁速度",
    "尺寸 标度": "尺寸标度",
    "界面-已解析 路径 图": "界面分辨路径图",
    "钉扎景观 的 readout": "钉扎景观的读出量",

    # Wang / Ke mechanism section.
    "雪崩/超润滑": "雪崩 / 超润滑",
    "基态畴 内": "基态畴内",
    "横向滑移": "横向滑移",
    "畴壁 提供": "畴壁提供",
    "面内力": "面内力",
    "现实 翻转": "现实翻转",
    "微观 翻转-力 图像": "微观翻转–力图像",
    "雪崩-尺寸 指数": "雪崩尺寸指数",
    "wavelike 畴壁": "波状畴壁",
    "高速 超润滑 动力学": "高速超润滑动力学",
    "洁净-畴壁 迁移率": "洁净畴壁迁移率",
    "淬火无序 下的 临界退钉扎": "淬火无序下的临界退钉扎",
    "基态畴 与 对称性破缺构型 的 力 差值": "基态畴与对称性破缺构型的力差值",
    "畴壁驱动 的 微观 来源": "畴壁驱动的微观来源",
    "无序 指数": "无序指数",

    # Chen / Liu sections.
    "真实看到 钉扎 → 退钉扎": "真实看到钉扎 → 退钉扎",
    "KPFM 里 畴壁": "KPFM 里畴壁",
    "偏置 测试": "偏置测试",
    "单畴 区域": "单畴区域",
    "预存畴壁控制翻转": "预存畴壁控制翻转",
    "钉扎/退钉扎 事件": "钉扎 / 退钉扎事件",
    "阈值 定义": "阈值定义",
    "无序 无序样本": "无序样本",
    "rough-edge 钉扎": "粗糙边缘钉扎",
    "真实 滑移铁电 缺陷 景观 上的 畴壁 退钉扎": "真实滑移铁电缺陷景观上的畴壁退钉扎",
    "离散 偏置": "离散偏置",
    "临界 动力学": "临界动力学",
    "器件尺度 空间 图": "器件尺度空间图",
    "Raman 成像": "Raman（拉曼）成像",
    "器件 分成": "器件分成",
    "不同区域独立 翻转": "不同区域独立翻转",
    "不同 循环": "不同循环",
    "表观 临界场": "表观临界场",
    "电输运 滞回": "电输运滞回",
    "空间 图": "空间图",
    "局域 景观": "局域景观",
    "器件-level 矫顽场": "器件层级矫顽场",
    "局域 阈值 / waiting 时间 / 区域 尺寸 / 畴壁 几何": "局域阈值 / 等待时间 / 区域尺寸 / 畴壁几何",
    "区域依赖 翻转": "区域依赖翻转",
    "stepwise / 区域依赖 翻转": "分步 / 区域依赖翻转",
    "无序-敏感 动力学": "对无序敏感的动力学",

    # Missing-observable checklist.
    "一组恒定 E": "一组恒定 E",
    "position(t)": "畴壁位置 x(t)",
    "同一批 畴壁 轨迹": "同一批畴壁轨迹",
    "提取 规则": "提取规则",
    "有限 尺寸": "有限尺寸",
    "横向 尺寸": "横向尺寸",
    "速度 坍缩": "速度坍缩",
    "粗糙度 截止": "粗糙度截止",
    "无序 定义": "无序定义",
    "缺陷 type": "缺陷类型",
    "连续体 无序 强度": "连续体无序强度",
    "独立 可观测量": "独立可观测量",
    "[DW / pinning / threshold / geometry / scaling]": "[畴壁 / 钉扎 / 阈值 / 几何 / 标度]",
    "洁净 迁移率": "洁净迁移率",
    "钉扎 事件": "钉扎事件",

    # Closing experiment / numerical loop.
    "预置单墙": "预置单畴壁",
    "成核 变量": "成核变量",
    "已有 畴壁": "已有畴壁",
    "重复 无序样本 / 器件 区域": "重复无序样本 / 器件区域",
    "E<sub>c</sub> 分布": "E<sub>c</sub> 分布",
    "循环间 variability": "循环间变异性",
    "多个 L 做 坍缩": "多个 L 做标度坍缩",
    "翻转 自由度": "翻转自由度",
    "整层协同滑移": "整层协同滑移",
    "畴壁 运动": "畴壁运动",
    "多种 3R-MoS₂ 空间实验": "多种 3R-MoS₂ 空间实验",
    "钉扎 / 翻转 observations": "钉扎 / 翻转观测",
    "跨 无序": "跨无序",
    "退钉扎 可观测量": "退钉扎可观测量",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "math"}:
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    soup = BeautifulSoup(TARGET.read_text(encoding="utf-8"), "html.parser")
    before_sources = source_blocks(soup)
    before_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]
    before_images = [(img.get("src"), img.get("alt")) for img in soup.find_all("img")]
    before_figure_links = [a.get("href") for a in soup.select("figure a")]

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for a, b in sorted(REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
            new = new.replace(a, b)
        new = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", new)
        new = re.sub(r"\s+([，。；：！？、）])", r"\1", new)
        new = re.sub(r"（\s+", "（", new)
        if new != old:
            node.replace_with(new)

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 08 source-text changed during Language V2 repair")
    if [el.get_text(" ", strip=False) for el in soup.select(".eq")] != before_equations:
        raise RuntimeError("Module 08 equation card changed during Language V2 repair")
    if [(img.get("src"), img.get("alt")) for img in soup.find_all("img")] != before_images:
        raise RuntimeError("Module 08 image wiring changed during Language V2 repair")
    if [a.get("href") for a in soup.select("figure a")] != before_figure_links:
        raise RuntimeError("Module 08 figure link changed during Language V2 repair")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
