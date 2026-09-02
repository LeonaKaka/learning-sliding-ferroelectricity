from __future__ import annotations

import re
from copy import copy
from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

# Language V2 is reviewed one page at a time. Keep this pass scoped to Module 07.
TARGET = ROOT / "modules/numerical-modeling.html"

REPLACEMENTS = {
    # Page framing / provenance.
    "From Theory to Numerical Modeling": "07 从理论到数值建模",
    "phase-field 文献集": "相场文献集",
    "Drive PDF": "项目 Drive PDF",
    "Figure 均来自": "论文图均来自",
    "Caballero Figure": "Caballero 论文图",
    "原始 Figure": "原论文图",
    "Module 05": "模块 05",
    "Module 08": "模块 08",

    # General prose and model reduction.
    "畴壁、elastic 与 静电 能量": "畴壁、弹性与静电能量",
    "完整 tensor 极化": "完整张量极化",
    "静电 / elastic 非局域性": "静电 / 弹性非局域性",
    "多个 sliding 界面": "多个滑移界面",
    "staged 运动": "分阶段运动",
    "多个 interface 的相对位移": "多个界面的相对位移",
    "interaction term": "相互作用项",
    "coarse-grained 结构示意": "粗粒化结构示意",
    "Hamiltonian": "Hamiltonian（哈密顿量）",
    "single-畴壁 最小问题": "单畴壁最小问题",
    "三层/多层 的 intermediate 态": "三层 / 多层的中间态",
    "单壁 β/ζ/ν": "单畴壁 β/ζ/ν",
    "single-畴壁 problem": "单畴壁问题",
    "界面 index": "界面索引",

    # Identifiability / calibration.
    "无量纲化 & 可辨识性": "无量纲化与可辨识性",
    "连续体 模型": "连续体模型",
    "无序 amplitude": "无序幅度",
    "non-可辨识性": "不可辨识性",
    "无无序": "无序为零",
    "Research Track 里采用的 periodic 堆垛 模型": "Research Track 中采用的周期性堆垛模型",
    "关掉 drive 与 无序": "关掉驱动与无序",
    "单谐波 无序为零 sector": "无序为零的单谐波扇区",
    "单谐波 无无序 sector": "无序为零的单谐波扇区",
    "明确 normalization": "明确归一化",
    "sine-Gordon kink": "sine-Gordon kink（孤子）",
    "局域-gradient 模型": "局域梯度模型",
    "多个 coupled 界面": "多个耦合界面",
    "actual energy 景观": "实际能量景观",
    "实际 energy 景观": "实际能量景观",
    "prefactor": "前因子",
    "畴壁 width": "畴壁宽度",
    "畴壁 tension": "畴壁张力",
    "畴壁 energy": "畴壁能量",
    "可观测量 / prior": "可观测量 / 先验",
    "periodicity": "周期性",
    "order-参数": "序参量",
    "堆垛 energy 景观": "堆垛能量景观",
    "无序 morphology + 阈值 statistics": "无序形貌 + 阈值统计",
    "关联 effects": "关联效应",
    "dimensionless ratio": "无量纲比",
    "<th>ratio</th>": "<th>比值</th>",
    "畴壁 core": "畴壁核心区",
    "grid points": "网格点",
    "体系 size": "体系尺寸",
    "畴壁-core": "畴壁核心区",
    "smooth 景观": "平滑景观",
    "drive 耦合": "驱动耦合",
    "drive ratio": "驱动力比",
    "coercive / 退钉扎 场": "矫顽场 / 退钉扎场",
    "无序 energy 尺度": "无序能量尺度",
    "fair 匹配": "公平匹配",
    "same 无序 强度": "相同无序强度",
    "Research Track fair matching": "Research Track 的公平匹配",
    "无无序 energy / length 尺度": "无序为零时的能量 / 长度尺度",
    "local relaxation time": "局域弛豫时间",
    "自然局域 relaxation time": "自然局域弛豫时间",
    "无无序 minimum": "无序为零时的极小值",
    "实际 校准": "实际校准",
    "无无序-畴壁 迁移率": "无序为零时的畴壁迁移率",
    "独立 relaxation 可观测量": "独立弛豫可观测量",
    "kinetic 尺度": "动力学尺度",
    "Calibration set": "校准集",
    "Holdout 验证": "留出验证",
    "holdout 可观测量": "留出可观测量",
    "independent 验证": "独立验证",
    "calibration closure": "校准闭合",
    "structural / static / dynamic 可观测量": "结构 / 静态 / 动态可观测量",
    "phenomenological control 参数": "现象学控制参数",

    # Disorder couplings and correlation length.
    "翻转 cost": "翻转代价",
    "order-参数 的某个符号": "序参量的某个符号",
    "frozen region": "固定区域",
    "RMS 强度": "RMS（均方根）强度",
    "disorder 在空间上": "无序在空间上",
    "finite-关联 无序": "有限相关长度无序",
    "δ-correlated limit": "δ 相关极限",
    "连续体 white 噪声": "连续体白噪声",
    "cell volume": "网格单元体积",
    "连续 correlated 场": "连续相关场",
    "white-噪声": "白噪声",
    "correlated-RF 稳健性": "相关随机场稳健性",
    "apparent 指数": "表观指数",
    "same 无序强度": "相同无序强度",

    # Grid / discretization.
    "Grid sanity": "网格检验",
    "continuum Δ": "连续体 Δ",
    "cell/node": "网格单元 / 节点",
    "cell 已积分": "网格单元上已积分",
    "场 value": "场值",
    "dx dependence": "dx 依赖",
    "像素 的标准差": "网格点的标准差",
    "δ-correlated 噪声": "δ 相关噪声",

    # Thermal noise / FDT.
    "quenched 场": "淬火场",
    "热噪声 随时间刷新": "热噪声随时间刷新",
    "空间 cell measure": "空间网格单元测度",
    "timestep": "时间步长",
    "涨落–耗散 convention": "涨落–耗散约定",
    "frozen 景观": "固定无序景观",
    "cell measure": "网格单元测度",
    "temporal δ-函数": "时间 δ 函数",
    "space 与 time 上 δ-correlated": "空间和时间上均为 δ 相关",
    "constant-迁移率": "常迁移率",
    "模型-A convention": "模型 A 约定",
    "dimensionless energy": "无量纲能量",
    "热 bath": "热浴",
    "dissipative 迁移率": "耗散迁移率",
    "update amplitude": "每步增量幅度",
    "derivative amplitude": "导数项幅度",
    "increment amplitude": "增量幅度",
    "噪声-rate": "噪声率",
    "energy convention": "能量约定",
    "热-噪声 rule": "热噪声规则",
    "T convention": "温度约定",
    "free energy": "自由能",
    "equilibrium 合理性": "平衡态合理性",
    "distribution": "分布",
    "受驱 problem": "受驱问题",
    "equilibrium": "平衡态",
    "thermostat": "恒温器",
    "rounding 曲线": "热圆滑曲线",
    "white 热噪声": "白热噪声",
    "粗粒化 theory": "粗粒化理论",
    "bare 参数": "裸参数",
    "thermal seeds": "热噪声随机种子",
    "finite-T protocol / outer-vs-inner statistics": "有限温流程 / 外层与内层统计",
    "thermal rounding measurement logic": "热圆滑测量逻辑",

    # Reproduction Lab bridge.
    "只读 checklist": "只读检查清单",
    "解析 kink": "解析 kink（孤子）",
    "EW 粗糙度 vs Eq.19": "EW 粗糙度与 Eq. 19 对照",
    "validity boundary": "有效性边界",
    "有效 钉扎 correlator": "有效钉扎相关函数",
    "disordered B/S cross-模型 阶段验证": "含无序 B/S 跨模型阶段验证",
    "硬判据": "硬判据",

    # Steady-velocity estimator.
    "稳态-畴壁 velocity contract": "稳态畴壁速度估计约定",
    "有限 观测 time": "有限观测时长",
    "畴壁-拓扑变化": "畴壁拓扑变化",
    "nonsteady-relaxation route": "非稳态弛豫路线",
    "可 unwarp 的 畴壁 坐标": "可周期展开的畴壁坐标",
    "畴壁 extraction 判据": "畴壁提取判据",
    "center-of-mass 坐标": "质心坐标",
    "periodic boundary": "周期边界",
    "畴壁 separation": "畴壁间距",
    "体相 relaxation": "体相弛豫",
    "局域 局域呼吸模": "局域呼吸模",
    "constant-E 运行": "恒定 E 运行",
    "候选 区间s": "候选区间",
    "区间 stability": "区间稳定性",
    "late-区间 split": "后段分割",
    "局部 slope": "局部斜率",
    "aging": "老化",
    "late 突发事件": "晚时突发事件",
    "net displacement": "净位移",
    "extraction jitter": "提取抖动",
    "extra 畴壁": "额外畴壁",
    "一次性 escape": "一次性逃逸",
    "boundary": "边界",
    "time points": "时间点",
    "用 slope": "用斜率",
    "回归 slope": "回归斜率",
    "endpoint 估计量": "端点估计量",
    "time 样本": "时间样本",
    "ordinary least-squares pointwise error": "普通最小二乘逐点误差",
    "无序 uncertainty": "无序不确定性",
    "场 point": "场点",
    "β inference": "β 推断",
    "场 points": "场点",
    "来源-对应的速度曲线": "样本对应的速度曲线",
    "raw/unwrapped X(t)": "原始 / 周期展开后的 X(t)",
    "畴壁-valid mask": "畴壁有效掩码",
    "endpoint velocity": "端点速度",
    "summary/CI": "汇总 / 置信区间",
    "reduced-force 区间": "约化驱动力区间",
    "运行 outcome": "运行结果",
    "velocity 估计量": "速度估计量",
    "resolved-运动态": "已解析运动态",
    "稳态-区间 pass": "稳态区间通过",
    "resolved-钉扎态 under registered 观测时长": "预注册观测时长内的已解析钉扎态",
    "阈值/bracket": "阈值 / 夹定区间",
    "log-v 幂律 点": "对数速度幂律点",
    "late 运动 / 观测时长-limited": "晚时运动 / 受观测时长限制",
    "censored": "删失",
    "velocity estimate": "速度估计",
    "resolved-钉扎态-under-观测时长": "预注册观测时长内的已解析钉扎态",
    "数值 numerical 数值证明": "数值有效性证明",
    "E=0 stability": "E=0 稳定性",
    "threshold inference ladder": "阈值推断层级",
    "exponent robustness": "指数稳健性",

    # Run receipts / provenance.
    "运行 记录 / 来源追踪": "运行记录 / 来源追踪",
    "figure / 估计量": "图 / 估计量",
    "raw output": "原始输出",
    "raw bytes": "原始字节",
    "一个 simulation 运行": "一次模拟运行",
    "Code 依据": "代码依据",
    "repository / commit": "仓库 / 提交",
    "来源-tree hash": "源码树哈希",
    "无序为零 / dirty": "无序为零 / 有未提交改动",
    "patch / tree hash": "补丁 / 源码树哈希",
    "干净 commit": "干净提交",
    "Resolved configuration": "最终生效配置",
    "include": "引用文件",
    "Random identity": "随机源身份",
    "quenched-无序": "淬火无序",
    "stochastic 随机种子": "随机过程种子",
    "RNG 族 / stream convention": "RNG（随机数生成器）族 / 随机流约定",
    "Execution environment": "执行环境",
    "integrator": "积分器",
    "关键 依赖项": "关键依赖项",
    "Stop & QC 记录": "停止原因与质检记录",
    "max steps": "最大步数",
    "NaN/divergence": "NaN / 发散",
    "畴壁-拓扑": "畴壁拓扑",
    "Raw-output 记录": "原始输出记录",
    "阶段验证 的路径": "阶段验证路径",
    "object id": "对象 ID",
    "dtype": "数据类型",
    "raw parent": "原始父数据",
    "analysis code/version": "分析代码 / 版本",
    "运行 IDs": "运行 ID",
    "畴壁-extraction rule": "畴壁提取规则",
    "删失 rule": "删失规则",
    "execution_状态": "执行状态",
    "completed / aborted": "完成 / 中止",
    "physically 钉扎态": "物理钉扎态",
    "物理_assessment": "物理判定",
    "bracketed": "已夹定",
    "no transition exists": "不存在转变",
    "analysis_role": "分析角色",
    "holdout": "留出验证",
    "事后 diagnostic": "事后诊断",
    "excluded-with-reason": "有理由排除",
    "preregistered 主 证据": "预注册主证据",
    "一个 task": "一个任务",
    "敏感性 analysis": "敏感性分析",
    "PASS / FAIL": "通过 / 失败",
    "总体 statistics": "总体统计",
    "fully 最终生效配置": "完整的最终生效配置",
    "配置 lineage": "配置继承链",
    "CLI command": "命令行命令",
    "resolved values": "最终取值",
    "随机种子 role": "随机种子角色",
    "RNG convention": "RNG（随机数生成器）约定",
    "无序-array hash": "无序数组哈希",
    "commit SHA": "提交 SHA",
    "运行 completed": "运行完成",
    "hit max-time": "达到最大时长",
    "stop_reason": "停止原因",
    "registered stopping thresholds": "预注册停止阈值",
    "final diagnostics": "最终诊断量",
    "raw hashes": "原始数据哈希",
    "用什么 rule / 区间": "用什么规则 / 区间",
    "Figure / 结论 map": "图 / 结论映射",
    "panel 指向": "图中分区指向",
    "independent 证据单元": "独立证据单元",
    "候选 figure": "候选图",
    "Data → Estimator → Evidence → Claim contract": "数据 → 估计量 → 证据 → 结论契约",

    # Final experimental checklist / closing prose.
    "无 drive": "无驱动",
    "strong 缺陷": "强缺陷",
    "像素 amplitude": "网格点幅度",
    "constant drive": "恒定驱动",
    "grid points": "网格点",
    "size 收敛": "尺寸收敛",
    "随机种子 statistics": "随机种子统计",
    "畴壁 extraction": "畴壁提取",
    "目标 basin": "目标吸引域",
    "层级 set / separator": "水平集 / 分隔线",
    "numerical 模型": "数值模型",
    "generic 相场": "通用相场",
    "periodic 堆垛 坐标": "周期性堆垛坐标",
    "fair 匹配": "公平匹配",
    "进入 Research Track": "进入 Research Track →",
    "06 Disorder & RFIM": "06 Disorder（无序）与 RFIM",
    "08 Current Frontiers": "08 Current Frontiers（当前前沿）",
}


def source_formula_blocks(soup: BeautifulSoup) -> list[str]:
    """Capture equation content while excluding explanatory <small> prose."""
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
    if "eq" in parent.get("class", []):
        return True
    return parent.find_parent(class_="eq") is not None


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
    # Preserve the displayed mathematical expression itself. Explanatory small
    # text inside an equation card remains editable prose.
    if inside_eq(node) and not inside_eq_small(node):
        return True
    return False


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    before_sources = source_blocks(soup)
    before_formulae = source_formula_blocks(soup)
    before_images = [(img.get("src"), img.get("alt")) for img in soup.find_all("img")]
    before_figure_links = [a.get("href") for a in soup.select("figure a")]

    if soup.title:
        soup.title.string = "Numerical Modeling（数值建模） · Learning Sliding Ferroelectricity"
    header_small = soup.select_one("header .bar b small")
    if header_small:
        header_small.string = "· 07 Numerical Modeling（数值建模）"
    nav = soup.select("header .bar span a")
    labels = ["知识图谱", "TDGL", "模型约化", "尺度与可辨识性", "网格检验", "热噪声", "运行记录"]
    for link, label in zip(nav, labels):
        link.string = label

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for a, b in sorted(REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
            new = new.replace(a, b)
        # Repair historical spacing damage, but never touch quotations or formulae.
        new = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", new)
        new = re.sub(r"\s+([，。；：！？、）])", r"\1", new)
        new = re.sub(r"（\s+", "（", new)
        if new != old:
            node.replace_with(new)

    # One first-use teaching term that is useful to recognize in English.
    h_reduction = soup.find("h2", id="reduction")
    if h_reduction:
        next_p = h_reduction.find_next_sibling("p")
        if next_p and "弹性线模型" in next_p.get_text():
            for node in list(next_p.find_all(string=True)):
                old = str(node)
                if "弹性线模型" in old:
                    node.replace_with(old.replace("弹性线模型", "elastic-line model（弹性线模型）", 1))
                    break

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 07 source-text changed during Language V2 repair")
    if source_formula_blocks(soup) != before_formulae:
        raise RuntimeError("Module 07 displayed formula changed during Language V2 repair")
    if [(img.get("src"), img.get("alt")) for img in soup.find_all("img")] != before_images:
        raise RuntimeError("Module 07 image src/alt changed during Language V2 repair")
    if [a.get("href") for a in soup.select("figure a")] != before_figure_links:
        raise RuntimeError("Module 07 figure link changed during Language V2 repair")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
