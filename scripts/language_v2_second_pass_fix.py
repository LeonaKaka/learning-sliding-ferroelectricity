from __future__ import annotations

import re
from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

# Language V2 is reviewed page by page.  Keep this pass scoped to Module 06.
TARGET = ROOT / "modules/disorder-rfim.html"

REPLACEMENTS = {
    # Page framing / provenance.
    "Figure 只取 Drive PDF 自身": "论文图只取项目 Drive PDF 自身",
    "Drive published PDF": "项目 Drive 正式发表 PDF",
    "Drive PDF": "项目 Drive PDF",
    "原 Figure 裁取": "原论文图裁取",
    "原 Figure 对象": "原论文图对象",

    # Real-material disorder bridge.
    "growth-induced structural 无序": "生长诱导的结构无序",
    "Se-vacancy-related 陷阱动力学": "与 Se 空位相关的陷阱动力学",
    "矫顽场 spread": "矫顽场分散",
    "slow-sweep 畴松弛": "慢扫场下的畴松弛",
    "structural 缺陷": "结构缺陷",
    "多畴 relaxation": "多畴弛豫",
    "trapped charge / charged 缺陷": "陷阱电荷 / 带电缺陷",
    "time-dependent trapping / 迁移率": "随时间变化的电荷俘获 / 迁移率",
    "strain / structural 缺陷 / 封闭小畴 / edge": "应变 / 结构缺陷 / 封闭小畴 / 边缘",
    "畴壁 energy": "畴壁能量",
    "多畴 initial structure": "多畴初始结构",
    "initial 拓扑": "初始拓扑",
    "阈值 distribution": "阈值分布",
    "relaxation 路径": "弛豫路径",
    "extended / clustered 缺陷": "扩展 / 团簇缺陷",
    "finite 关联长度": "有限相关长度",
    "anisotropy": "各向异性",
    "rare strong pins": "稀有强钉扎中心",
    "δ-correlated white 噪声": "δ 相关白噪声",
    "microscopy / electrostatics / 缺陷 energetics": "显微表征 / 静电学 / 缺陷能量学",

    # RFIM introduction / model language.
    "quenched 随机场": "淬火随机场",
    "无序-induced 临界点": "无序诱导临界点",
    "无序-induced 临界性": "无序诱导临界性",
    "雪崩 scaling": "雪崩标度",
    "charge trap": "电荷陷阱",
    "均值-场": "均值场",

    # Avalanche event definitions and statistics.
    "noisy 活动度 trace": "含噪活动度时间序列",
    "amplitude 阈值": "幅度阈值",
    "dead time": "dead time（死时间）",
    "物理-defined 雪崩": "物理定义的雪崩",
    "infinitesimal / quasistatic drive increment": "无穷小 / 准静态驱动增量",
    "collective relaxation": "集体弛豫",
    "事件检测器-defined 突发事件": "事件检测器定义的突发事件",
    "velocity、current 或 image 活动度": "速度、电流或图像活动度",
    "gap rule": "间隔规则",
    "事件 数量、size、duration": "事件数量、大小、持续时间",
    "detection 阈值": "检测阈值",
    "temporal correlations": "时间关联",
    "事件检测器 rule": "事件检测规则",
    "all-size 临界 幂律": "全尺度临界幂律",
    "临界 region": "临界区",
    "几 decade": "数个数量级",
    "least-squares": "普通最小二乘",
    "lower 截止": "下截止",
    "detection 上截止": "检测上截止",
    "基于似然的指数估计": "基于似然的指数估计",
    "goodness-of-拟合": "拟合优度",
    "plausible 替代分布": "合理的替代分布",
    "size / duration 指数": "事件大小 / 持续时间指数",
    "size–duration relation": "事件大小–持续时间关系",
    "截止 scaling": "截止尺度标度",
    "固定 duration 下的 average 雪崩 形状 / scaling 函数": "固定持续时间下的平均雪崩形状 / 标度函数",
    "least-squares 幂律 fitting": "最小二乘幂律拟合",
    "模型 comparison": "模型比较",
    "平均 雪崩 temporal 形状": "平均雪崩时间形状",
    "multivariable scaling 函数": "多变量标度函数",
    "time bins / 帧 / 像素": "时间分箱 / 帧 / 像素",
    "自助法 draws": "自助法抽样",
    "uncertainty 计算产生的 resamples": "不确定性计算产生的重采样",
    "事件-层级 summary / distribution": "事件层级汇总量 / 分布",
    "leave-one-无序样本-out": "逐一留出无序样本",
    "iid 事件 样本": "iid（独立同分布）事件样本",
    "size/duration scaling": "事件大小 / 持续时间标度",

    # Drossel / geometry.
    "percolation-like invasion": "percolation-like（类渗流）推进",
    "self-similar 行为": "self-similar（自相似）行为",
    "invaded area near 退钉扎": "退钉扎附近的侵入区域",
    "invaded area": "侵入区域",
    "multiply-connected 几何": "多连通几何",
    "数值与 scaling arguments": "数值结果与标度论证",
    "Gaussian 无序": "高斯无序",
    "percolation-like behavior": "类渗流行为",
    "percolation 普适性": "渗流普适性",
    "lower 临界 维数": "lower critical dimension（下临界维数）",
    "无序 distribution": "无序分布",
    "做 height/粗糙度 统计": "做高度 / 粗糙度统计",
    "time scaling": "时间标度",

    # Zhou / anomalous roughening.
    "short-time 畴壁 study": "短时畴壁研究",
    "QEW 的简单 superrough scaling": "QEW 的简单 super-rough scaling（超粗糙标度）",
    "本征异常标度 / spatial 多重标度": "intrinsic anomalous scaling（本征异常标度）/ spatial multiscaling（空间多重标度）",
    "RFIM 与 QEW 的 scaling 差异": "RFIM 与 QEW 的标度差异",
    "全局 粗糙度": "全局粗糙度",
    "局域 粗糙度": "局域粗糙度",
    "无序-induced 粗糙度": "无序诱导粗糙度",
    "无 无序 background": "无序为零时的背景",
    "short-time 退钉扎 scaling": "短时退钉扎标度",
    "dynamic roughening": "动态粗糙化",
    "QEW comparison": "QEW 对比",
    "bounded 随机场": "有界随机场",
    "lattice anisotropy": "晶格各向异性",

    # Closing model-choice prose.
    "sliding ferroelectricity": "sliding ferroelectricity（滑移铁电）",
    "体相 order-参数 模型": "体相序参量模型",
    "elastic 畴壁": "弹性畴壁",
    "滑移铁电 simulation": "滑移铁电模拟",
    "无序/drive": "无序 / 驱动力",
    "Module 07": "模块 07",
    "畴壁 extraction": "畴壁提取",
    "07 From Theory to Numerical Modeling": "07 从理论到数值建模",
    "05 Depinning as a Critical Phenomenon": "05 Depinning（退钉扎）· 临界现象",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    # Displayed model equations are scientific content, not prose.
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    before_sources = source_blocks(soup)
    before_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]

    if soup.title:
        soup.title.string = "Disorder（无序）与 RFIM · Learning Sliding Ferroelectricity"
    header_small = soup.select_one("header .bar b small")
    if header_small:
        header_small.string = "· 06 Disorder（无序）与 RFIM"
    nav = soup.select("header .bar span a")
    nav_labels = ["知识图谱", "RFIM", "单畴壁", "Overhangs（悬垂）"]
    for link, label in zip(nav, nav_labels):
        link.string = label
    crumb = soup.select_one("main > .rule")
    if crumb:
        for node in list(crumb.find_all(string=True)):
            if "Disorder & RFIM" in str(node):
                node.replace_with(str(node).replace("Disorder & RFIM", "06 Disorder（无序）与 RFIM"))

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for a, b in sorted(REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
            new = new.replace(a, b)
        # Repair spacing damage left by the historical mechanical pass. Source
        # quotations and equations are excluded above.
        new = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", new)
        new = re.sub(r"\s+([，。；：！？、）])", r"\1", new)
        new = re.sub(r"（\s+", "（", new)
        if new != old:
            node.replace_with(new)

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 06 source-text changed during Language V2 repair")
    after_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]
    if after_equations != before_equations:
        raise RuntimeError("Module 06 displayed equation changed during Language V2 repair")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
