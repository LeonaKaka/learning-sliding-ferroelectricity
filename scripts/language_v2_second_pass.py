from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "modules/pinning-creep.html",
    ROOT / "modules/depinning.html",
    ROOT / "modules/disorder-rfim.html",
    ROOT / "modules/numerical-modeling.html",
    ROOT / "modules/research-track.html",
]

REPLACEMENTS = {
    "dx refinement": "dx 加密",
    "dt refinement": "dt 加密",
    "fit window": "拟合区间",
    "fit windows": "拟合区间",
    "finite-size effects": "有限尺寸效应",
    "finite-size effect": "有限尺寸效应",
    "held-out size": "留出尺寸",
    "cross-check": "交叉核验",
    "post-hoc diagnostic": "事后诊断",
    "analysis contract": "分析约定",
    "Research recipe": "研究方法",
    "baseline": "基准",
    "dirty working tree": "有未提交改动的工作树",
    "dirty flag": "未提交改动标记",
    "run set": "运行集合",
    "row count": "数据行数",
    "clustering": "聚类结构",
    "paper sentence": "论文结论句",
    "有效 粗糙度指数 over the tested 区间": "在已测试尺度区间得到的有效粗糙度指数",
    "整体 tilt": "整体倾斜",
    "去趋势 order": "去趋势阶数",
    "高阶 polynomial": "高阶多项式",
    "long-wavelength": "长波",
    "原始 u(y) 与 detrended u(y)": "原始 u(y) 与去趋势后的 u(y)",
    "detrended u(y)": "去趋势后的 u(y)",
    "generic anomalous-标度 分类": "一般异常标度分类",
    "缺陷-structure information": "缺陷结构信息",
    "r-bin": "r 分箱",
    "Fourier modes": "Fourier 模式",
    "轨迹 帧": "轨迹帧",
    "外层 n": "外层独立样本数 n",
    "分层 summary": "分层汇总",
    "supported over tested scales": "在已测试尺度内得到支持",
    "ensemble/统计 可观测量": "集合统计可观测量",
    "PFM snapshots": "PFM 快照",
    "normalized switched 区域": "归一化翻转面积",
    "PFM phase 图像": "PFM 相位图",
    "Research recipe": "研究方法",
    "有限-T": "有限温度",
    "PZT nanocapacitor": "PZT 纳米电容",
    "nonuniversal scales": "非普适尺度",
    "near-阈值": "近阈值",
    "logarithmic 修正": "对数修正",
    "qEW-类别": "qEW 类别",
    "热-圆滑 标度": "热圆滑标度",
    "Arrhenius activation": "Arrhenius 激活",
    "supported over tested range": "在已测试范围内得到支持",
    "留出尺寸 lands without retuning + independent 可观测量 交叉核验": "留出尺寸无需重新调参即可落入预期位置，并由独立可观测量交叉核验",
    "强 普适性 证据, subject to 映射 validity": "较强的普适性证据，但仍受映射有效性约束",
    "intersection count": "交点数量",
    "data-integrity QC": "数据完整性检查",
    "adaptive / binary search": "自适应 / 二分搜索",
    "adaptive 场 probes pooled": "自适应搜索得到的场点全部合并",
    "relative tolerance": "相对容差",
    "冻结 or propagate": "冻结或传播",
    "有效 nonlinear onset 指数": "有效非线性起始指数",
    "driven RFIM": "受驱 RFIM",
    "无效 in the middle": "中间区间无效",
    "log-binned histogram": "对数分箱直方图",
    "likelihood-based 指数 estimate": "基于似然的指数估计",
    "plausible alternatives": "合理的替代分布",
    "尺寸–持续时间 relation": "尺寸–持续时间关系",
    "upper 截止": "上截止",
    "maximum likelihood": "最大似然",
    "模型 比较": "模型比较",
    "multivariable 标度 函数": "多变量标度函数",
    "dP/dt peaks": "dP/dt 峰",
    "active 像素": "活跃像素",
    "事件 事件检测器": "事件检测器",
    "事件检测器 敏感性": "事件检测器敏感性",
    "项目 驱动": "项目 Drive",
    "短时 畴壁 study": "短时畴壁研究",
    "local、gradient、electrostatic、elastic": "局域、梯度、静电、弹性",
    "local bias": "局域偏置",
    "diffuse-wall cost": "弥散畴壁代价",
    "extracted 界面": "提取出的界面",
    "彩色 surface": "彩色曲面",
    "tanh-like profile": "类 tanh 剖面",
    "soliton profile": "孤子剖面",
    "wall profile": "畴壁剖面",
    "wall width": "畴壁宽度",
    "bulk field": "体场",
    "single-harmonic sector": "单谐波扇区",
    "洁净 sector": "洁净扇区",
    "minima": "极小值",
    "sine-Gordon kink": "sine-Gordon kink（孤子）",
    "harmonic content": "谐波成分",
    "correlation effects": "关联效应",
    "coupling type": "耦合类型",
    "extended/clustered landscape": "延展/成簇的无序景观",
    "continuum-field": "连续场",
    "continuum field": "连续场",
    "grid cell average": "网格单元平均",
    "field value": "场值",
    "random numbers": "随机数",
    "heat bath": "热浴",
    "white-噪声 idealization": "白噪声理想化",
    "additive-噪声": "加性噪声",
    "multiplicative / colored": "乘性 / 有色",
    "random calculus": "随机微积分",
    "简单可控 case": "简单可控情形",
    "hard 判据": "硬判据",
    "nonsteady 交叉区": "非稳态交叉区",
    "稳态-v route": "稳态速度路线",
    "nonsteady-松弛 route": "非稳态弛豫路线",
    "transient cut": "瞬态截断",
    "regression": "回归",
    "ordinary 最小二乘 pointwise error": "普通最小二乘逐点误差",
    "候选-区间 slopes": "候选区间斜率",
    "final 区间": "最终区间",
    "已解析-钉扎态 under registered 观测时长": "在登记观测时长内可判定的钉扎态",
    "区域-based 交叉核验": "基于区域的交叉核验",
    "本征 异常标度": "本征异常标度",
    "repository / 提交": "代码仓库 / 提交",
    "dated snapshot": "带日期的快照",
    "defaults": "默认值",
    "CLI override": "命令行覆盖参数",
    "precision": "数值精度",
    "backend": "计算后端",
    "dependency / environment identity": "依赖项 / 环境标识",
    "library change": "程序库变化",
    "converged": "已收敛",
    "hit 观测时长 limit": "达到观测时长上限",
    "上限 steps": "最大步数",
    "manual abort": "人工终止",
    "residual": "残差",
    "对象 id": "对象 ID",
    "sampling cadence": "采样间隔",
    "checksum": "校验和",
    "derived CSV / PNG": "派生 CSV / PNG",
    "原始 parent": "原始数据",
    "recovery / context": "恢复 / 上下文",
    "triangular 回线": "三角波回线",
    "level set / separator": "等值集 / 分隔面",
    "single-valuedness": "单值性",
    "driven 问题": "受驱动问题",
    "nonuniversal shift": "非普适偏移",
    "mapping failure": "映射失效",
    "cell-average": "网格单元平均",
    "δ-correlated continuum-field convention": "δ 相关连续场约定",
    "RNG / stream split": "随机数生成器 / 随机流拆分",
    "翻转 system": "翻转体系",
    "周期 堆垛 景观": "周期堆垛能量景观",
    "equivalent minima": "等价极小值",
    "off-diagonal BEC tensor": "非对角 BEC 张量",
    "二维 cell-average white disorder": "二维网格单元平均白噪声无序",
    "空间 碎裂 / coalescence context": "空间碎裂 / 合并背景",
    "L subset": "L 子集",
    "粗糙度 range": "粗糙度范围",
    "事件统计约定：突发事件 ≠ 雪崩 by naming": "事件统计约定：不能因为把突发事件叫作 avalanche 就把它当成雪崩",
    "integrated 畴壁 advance": "畴壁累计前进量",
    "integrated 活动度": "累计活动度",
    "electrical pulse 区域": "电脉冲面积",
    "普适 形状 or 函数 where applicable": "适用时还要检查普适形状或标度函数",
    "循环-level derived 可观测量": "循环层级派生可观测量",
    "默认 嵌套 in task / 器件": "默认嵌套在任务 / 器件内",
    "内层 重复 嵌套 under one 无序样本": "内层重复嵌套在同一个无序样本内",
    "数据集 / 运行 set is 可审计": "数据集 / 运行集合可审计",
    "Same nuisance 样本": "相同干扰因素样本",
    "机制 被证伪": "机制被证伪",
    "研究结论不是从 原始文件": "研究结论不是从原始文件",
    "有效 钉扎态 up to E": "直到 E 仍可判定为钉扎态",
    "A vs B": "A 与 B",
    "真正 运动态 对象": "真正运动的对象",
    "总体-level": "总体层级",
    "拟合 windows": "拟合区间",
    "原始/unwrapped X(t)": "原始/展开后的 X(t)",
    "detached island": "脱离小畴",
    "extra-畴壁": "额外畴壁",
    "projected u(y)": "投影得到的 u(y)",
    "dirty working 树": "有未提交改动的工作树",
    "patch / 树 哈希": "补丁 / 树哈希",
    "删失 ≠ no transition exists": "删失 ≠ ‘不存在转变’",
    "environment variable": "环境变量",
    "已解析 values + exact command": "解析后的参数值 + 完整命令",
    "exploratory script": "探索性脚本",
}

WHOLE_REPLACEMENTS = {
    "无序 至少有三条独立轴：耦合 × 强度 × 关联长度": "无序至少有三条独立轴：耦合方式 × 强度 × 关联长度",
    "coupling type 决定 h 怎样进入自由能；Δ/σ 决定幅度；ξ": "耦合方式决定 h 怎样进入自由能；Δ/σ 决定幅度；ξ",
    "淬火无序 与 热噪声 都会在代码里出现 random numbers，但物理角色完全不同：": "淬火无序与热噪声都会在代码里出现随机数，但物理角色完全不同：",
    "一条 P–E 回线 里的多个 dP/dt peaks、同一次 翻转 的多个 帧、或一张图里的多个 active 像素，都不能自动升级成‘很多 雪崩’。": "一条 P–E 回线里的多个 dP/dt 峰、同一次翻转的多个帧，或一张图里的多个活跃像素，都不能自动升级成‘很多雪崩’。",
}

BAD_TOKENS = [
    "普适ity", "无序ed", "over流", "de-钉扎", "short-尺度", "全局-width", "类别=",
    "data-integrity", "总体-level", "拟合 windows", "瞬态 cut", "dirty working", "exact command",
    "exploratory script",
]


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None:
        return True
    if parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    if parent.find_parent("header"):
        return True
    if parent.find_parent(class_="next") or "next" in parent.get("class", []):
        return True
    if "rule" in parent.get("class", []) or "eq" in parent.get("class", []):
        return True
    if parent.name == "a":
        return True
    return False


def source_blocks(soup: BeautifulSoup) -> list[str]:
    return [node.decode_contents() for node in soup.select(".source-text")]


def main() -> None:
    for path in FILES:
        before_text = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(before_text, "html.parser")
        before_sources = source_blocks(soup)
        title = soup.title.string if soup.title else None
        changed = 0
        for node in list(soup.find_all(string=True)):
            if not isinstance(node, NavigableString) or blocked(node):
                continue
            old = str(node)
            new = old
            for a, b in WHOLE_REPLACEMENTS.items():
                new = new.replace(a, b)
            for a, b in sorted(REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
                new = new.replace(a, b)
            if new != old:
                node.replace_with(new)
                changed += 1
        if soup.title and title is not None:
            soup.title.string = title
        after_sources = source_blocks(soup)
        if after_sources != before_sources:
            raise RuntimeError(f"source-text changed in {path}")
        out = str(soup)
        for token in BAD_TOKENS:
            if token in out:
                raise RuntimeError(f"bad token {token!r} remains in {path}")
        path.write_text(out, encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: changed {changed} visible text nodes; source blocks preserved={len(before_sources)}")


if __name__ == "__main__":
    main()
