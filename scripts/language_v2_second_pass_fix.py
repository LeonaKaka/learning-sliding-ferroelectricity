from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-03.html"
LOCKED_RESULTS = (
    "0.91%", "1.36%", "3.04%",
    "1.39%", "1.86%", "3.40%",
    "1.02%", "1.33%", "2.46%",
    "0.9592",
)

TEXT_REPLACEMENTS = {
    "Reproduction Lab ": "复现实验室 ",
    "· Lesson 03 · First Paper-Curve Thumbnail": "· 第 03 课 · 首次论文曲线缩略复现",
    "Paper vs Ours": "论文对照",
    "Code": "代码",
    " / Reproduction Lab / Lesson 03": " / 复现实验室 / 第 03 课",
    "thermal roughness 为什么从 0 长出来？": "thermal roughness（热粗糙度）为什么从 0 长出来？",
    "gold test": "已知答案测试",
    "wall profile": "畴壁剖面",
    "wall extractor": "畴壁提取器",
    "flat interface": "平直界面",
    "thermal noise": "thermal noise（热噪声）",
    "exact analytic benchmark": "精确解析基准",
    "paper protocol": "论文方案",
    "analytic Eq.19": "解析 Eq.19",
    "our simulation": "我们的数值模拟",
    "comparison window": "比较区间",
    "relative error": "相对误差",
    "0 · 原论文 Fig.2 vs 我们的 thumbnail": "0 · 原论文 Fig.2 与我们的缩略复现",
    "long-time thermal roughness": "长时热粗糙度",
    "Our thumbnail reproduction。": "本课缩略复现。",
    "右上直接画 relative error": "右上直接画相对误差",
    "同一 thermal realization 随时间逐渐 roughen": "同一独立热噪声样本随时间逐渐粗糙化",
    "论文曲线的 thumbnail reproduction": "论文曲线的缩略复现",
    "observable": "可观测量",
    "time dependence": "时间演化",
    "analytic benchmark": "解析基准",
    "full reproduction": "完整复现",
    "系统长度、dt、时间范围和 realization 数": "系统长度、dt、时间范围和独立样本数",
    "1 · 先把 paper protocol 写下来，防止偷偷改题": "1 · 先把论文方案写下来，防止偷偷改题",
    "line length": "线长",
    "CPU-fast thumbnail": "CPU 快速缩略复现",
    "time step": "时间步长",
    "Eq.19 error gate": "Eq.19 误差验收条件",
    "times": "时刻",
    "realizations": "独立样本数",
    "Monte Carlo noise": "Monte Carlo（蒙特卡洛）采样噪声",
    "protocol-identical": "方案参数完全一致",
    "我们 realizations 更多": "我们的独立样本更多",
    "system size": "系统尺寸",
    "time horizon": "时间跨度",
    "thumbnail": "缩略复现",
    "bulk-to-line projection": "bulk-to-line projection（体场到界面线投影）",
    "EW equation": "EW 方程",
    "diffusion ratio": "扩散比",
    "thermal increment": "热噪声增量",
    "2D quenched disorder": "二维 quenched disorder（冻结无序）",
    "thermal white noise": "thermal white noise（热白噪声）",
    "spatial + temporal delta correlation": "空间与时间 δ 相关",
    "cell size": "网格尺寸",
    "quenched RF": "冻结 RF",
    "flat initial condition": "平直初态",
    "finite-time crossover": "finite-time crossover（有限时间交叉）",
    "late-time short-scale thermal regime": "长时短尺度热区间",
    "periodic Laplacian": "periodic Laplacian（周期拉普拉斯算子）",
    "line elasticity": "界面线弹性",
    "deterministic relaxation": "确定性弛豫",
    "FDT noise": "FDT noise（涨落耗散噪声）",
    "independent thermal realizations": "独立热噪声样本",
    "statistical unit": "统计单位",
    "realization": "独立样本",
    "r-bins": "r 分箱",
    "interfaces": "界面样本",
    "correlation function": "correlation function（相关函数）",
    "separation": "间距",
    "6 · Hard gate：先冻结窗口，再算误差": "6 · 硬性验收：先冻结比较区间，再算误差",
    "lattice scale": "晶格尺度",
    "finite-size / periodicity": "有限尺寸 / 周期边界效应",
    "median relative error": "相对误差中位数",
    "RMS relative error": "相对误差 RMS",
    "max relative error": "最大相对误差",
    "gate": "判定",
    "PASS": "通过",
    "long-time thermal slope": "长时热斜率",
    "Eq.19 relative error": "Eq.19 相对误差",
    "打开 Lesson 03 Python 脚本": "打开第 03 课 Python 脚本",
    "先验 estimator": "先验估计量",
    "B(r,t) implementation": "B(r,t) 实现",
    "再测 reduction": "再测模型约化",
    "mapped parameters": "映射参数",
    "bulk→line mapping": "体场→界面线映射",
    "solver/noise": "求解器/噪声",
    "finite wall width / bulk fluctuation": "有限畴壁宽度 / 体场涨落",
    "Lesson 04 才是 Caballero 这篇的核心跨模型复现": "第 04 课才是 Caballero 这篇的核心跨模型复现",
    "1D EW theory": "一维 EW 理论",
    "1D EW simulation": "一维 EW 数值模拟",
    "2D GL extracted wall": "二维 GL 提取畴壁",
    "line prediction": "界面线预测",
    "extractor/B(r)/S(q)": "提取器/B(r)/S(q)",
    "sliding-FE periodic model": "滑移铁电周期模型",
    "← Lesson 02": "← 第 02 课",
    "Lesson 04": "第 04 课",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    return False


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [eq.get_text(" ", strip=False) for eq in soup.select(".eq")]
    before_pre = [pre.get_text() for pre in soup.select("pre")]
    before_code = [code.get_text() for code in soup.select("code")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]
    before_src = [img.get("src") for img in soup.find_all("img")]
    before_sources = [node.get_text() for node in soup.select(".source-text")]
    before_results = {token: raw.count(token) for token in LOCKED_RESULTS}

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in TEXT_REPLACEMENTS.items():
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    # This is a workflow label embedded in an equation-style box; only localize the label.
    for eq in soup.select(".eq"):
        if eq.get_text(strip=True) == "comparison window: 4 ≤ r ≤ 64":
            eq.string = "比较区间：4 ≤ r ≤ 64"

    if soup.title:
        soup.title.string = "Reproduction Lab（复现实验室）03 · EW 热粗糙化缩略复现"

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 03 expected 2 Figures, found {len(figures)}")
    figures[0]["alt"] = "Caballero 2020 图 2：界面粗糙度随时间演化"
    figures[1]["alt"] = "本课 EW 数值模拟与 Caballero Eq.19 的粗糙度对照"

    after_eq = [eq.get_text(" ", strip=False) for eq in soup.select(".eq")]
    if len(after_eq) != len(before_eq):
        raise RuntimeError("Lab 03 equation count changed")
    for old, new in zip(before_eq, after_eq):
        old_s = " ".join(old.split())
        new_s = " ".join(new.split())
        if old_s == "comparison window: 4 ≤ r ≤ 64":
            if new_s != "比较区间：4 ≤ r ≤ 64":
                raise RuntimeError("Lab 03 comparison-window label changed unexpectedly")
        elif old != new:
            raise RuntimeError(f"Lab 03 equation body changed: {old!r} -> {new!r}")
    if [pre.get_text() for pre in soup.select("pre")] != before_pre:
        raise RuntimeError("Lab 03 code/output block changed")
    if [code.get_text() for code in soup.select("code")] != before_code:
        raise RuntimeError("Lab 03 inline code changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Lab 03 links changed")
    if [img.get("src") for img in soup.find_all("img")] != before_src:
        raise RuntimeError("Lab 03 Figure wiring changed")
    if [node.get_text() for node in soup.select(".source-text")] != before_sources:
        raise RuntimeError("Lab 03 paper source text changed")

    rendered = str(soup)
    after_results = {token: rendered.count(token) for token in LOCKED_RESULTS}
    if after_results != before_results:
        raise RuntimeError(f"Lab 03 locked results changed: {before_results} -> {after_results}")
    TARGET.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
