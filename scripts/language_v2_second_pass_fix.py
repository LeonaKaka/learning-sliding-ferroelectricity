from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-06.html"
LOCKED_RESULTS = (
    "1.227%",
    "6.122%",
    "0.538906",
    "0.509213",
    "0.694308",
    "0.664796",
    "0.982981",
    "1.371256",
    "0.077925",
)

REPLACEMENTS = (
    ("Reproduction Lab 06 · Disordered GL ↔ EW Geometry", "Reproduction Lab（复现实验室）06 · 含无序 GL ↔ EW 几何"),
    ("Reproduction Lab ", "Reproduction Lab（复现实验室） "),
    ("Lesson 06 · Geometry Before Universality", "第 06 课 · 先验证几何，再讨论普适性"),
    ("Paper vs Ours", "论文对照"),
    (" / Reproduction Lab / Lesson 06", " / 复现实验室 / 第 06 课"),
    ("random-bond problem", "random-bond（随机键）问题"),
    ("2D Ginzburg–Landau bulk", "二维 Ginzburg–Landau（GL）体场"),
    ("1D Edwards–Wilkinson line", "一维 Edwards–Wilkinson（EW）界面"),
    ("real-space roughness", "real-space roughness（实空间粗糙度）"),
    ("Fourier-space structure factor", "structure factor（傅里叶空间结构因子）"),
    ("两个 observable", "两个观测量"),
    ("cross-model geometry mapping pass", "跨模型几何映射通过"),
    ("B-derived 与 S-derived effective exponent", "由 B 与 S 得到的有效指数"),
    ("原论文 Fig.5 vs 我们的 t=1000 checkpoint", "原论文 Fig.5 与我们的 t=1000 阶段验证"),
    ("从 flat wall 出发，平均 10 realizations", "从平直畴壁出发，平均 10 个独立无序样本"),
    ("large-time regime", "长时间区间"),
    ("random-bond roughness", "随机键粗糙度"),
    ("Our CPU-fast checkpoint", "本课小系统阶段验证"),
    ("EW length 128，8 realizations", "EW 长度 128，8 个独立无序样本"),
    ("effective ζ", "有效 ζ"),
    ("estimator", "估计量"),
    ("GL 与 EW geometry", "GL 与 EW 几何统计"),
    ("cross-model mapping pass", "跨模型映射通过"),
    ("random-bond universality", "随机键普适性"),
    ("命题 A · model reduction", "命题 A · 模型降维"),
    ("bulk disorder physics", "体场无序物理"),
    ("提取出的 wall", "提取出的畴壁"),
    ("cross-model agreement", "跨模型一致性"),
    ("命题 B · asymptotic scaling", "命题 B · 渐近标度"),
    ("roughness exponent", "粗糙指数"),
    ("random-bond equilibrium value", "随机键平衡值"),
    ("estimator consistency", "估计量一致性"),
    ("size/time convergence", "尺寸/时间收敛"),
    ("universality 成立", "普适性成立"),
    ("同一份 interface", "同一条界面"),
    ("Fourier window", "傅里叶尺度区间"),
    ("paper physics", "论文物理设定"),
    ("本课 checkpoint", "本课阶段验证"),
    ("bulk coupling", "体场耦合"),
    ("initial condition", "初始条件"),
    ("flat interface", "平直界面"),
    ("GL wall estimator", "GL 畴壁估计量"),
    ("finite-T soliton fit", "有限温孤子拟合"),
    ("Lesson04 已验证的 {A,w,u} fit", "第 04 课已验证的 {A,w,u} 拟合"),
    ("GL size", "GL 尺寸"),
    ("EW length", "EW 长度"),
    ("realizations", "独立无序样本"),
    ("time range", "时间范围"),
    ("t=1000 checkpoint", "t=1000 阶段验证"),
    ("protocol-identical Fig.5 reproduction", "与 Fig.5 完全同协议的复现"),
    ("小系统 checkpoint", "小系统阶段验证"),
    ("GL→EW mapping", "GL→EW 映射"),
    ("long-time / large-size exponent closure", "长时间/大尺寸下的指数闭合"),
    ("disorder lineage", "无序传递链"),
    ("random-bond coupling", "随机键耦合"),
    ("random force", "随机力"),
    ("wall-level pinning statistics", "畴壁层钉扎统计"),
    ("EW thermal dynamics", "EW 热噪声动力学"),
    ("finite-T bulk→wall estimator", "有限温体场→畴壁估计量"),
    ("bulk RB→pinning correlator", "体场 RB→钉扎力相关函数"),
    ("disordered dynamics", "含无序动力学"),
    ("finite size/time", "有限尺寸/有限时间"),
    ("mapping assumptions", "映射假设"),
    ("B(r) 的 cross-model geometry", "B(r) 的跨模型几何对照"),
    ("symmetric relative difference", "对称相对差"),
    ("CI 保存的最终结果", "自动化测试保存的最终结果"),
    ("B median relative difference =", "B 中位相对差 ="),
    ("cross-model agreement", "跨模型一致性"),
    ("bulk GL", "体场 GL"),
    ("reduced EW", "降维后的 EW"),
    ("real-space wall geometry", "实空间畴壁几何"),
    ("Fourier space", "傅里叶空间"),
    ("small-scale / large-scale crossover", "小尺度/大尺度过渡"),
    ("log bins", "对数分箱"),
    ("bin center", "分箱中心"),
    ("high q 密集 modes", "高 q 密集模式"),
    ("S(q) log-bin median relative difference =", "S(q) 对数分箱中位相对差 ="),
    ("10% gate", "10% 判据"),
    ("Fourier observable", "傅里叶观测量"),
    ("新的 n", "新的 n"),
    ("estimator weight", "估计量权重"),
    ("Fourier modes", "傅里叶模式"),
    ("也不是 bins", "也不是分箱"),
    ("然后才看 exponent", "然后才看指数"),
    ("paper asymptotic guide", "论文渐近参考"),
    ("ζ from B(r)", "由 B(r) 得到 ζ"),
    ("ζ from S(q)", "由 S(q) 得到 ζ"),
    ("crossover / finite-size / finite-time structure", "跨尺度过渡、有限尺寸和有限时间效应"),
    ("渐近 universality", "渐近普适性"),
    ("ASYMPTOTIC ζ GATE NOT PASSED。", "渐近 ζ 判据：未通过。"),
    ("同一 observable", "同一观测量"),
    ("model reduction", "模型降维"),
    ("B-derived 与 S-derived exponent", "由 B 与 S 得到的指数"),
    ("scaling regime", "标度区间"),
    ("paper target / slope guide", "论文目标值/斜率参考"),
    ("measured asymptotic exponent", "测得的渐近指数"),
    ("GL↔EW agreement", "GL↔EW 一致性"),
    ("geometry pipeline", "几何分析流程"),
    ("暴露 crossover", "暴露跨尺度过渡"),
    ("fit window", "拟合区间"),
    ("asymptotic regime", "渐近区间"),
    ("cheaper EW", "计算更省的 EW"),
    ("time/size ladder", "时间/尺寸阶梯"),
    ("exponent convergence", "指数收敛"),
    ("sanity check", "合理性检查"),
    ("bulk wall profile", "体场畴壁剖面"),
    ("disorder 已把 wall 撕成 bubbles / multiple-valued geometry", "无序已把畴壁撕成气泡或多值几何"),
    ("single-line mapping", "单值界面映射"),
    ("finite-T soliton fit", "有限温孤子拟合"),
    ("mean fitted amplitude A", "平均拟合振幅 A"),
    ("mean fitted width w", "平均拟合宽度 w"),
    ("mean profile-fit RMSE", "平均剖面拟合 RMSE"),
    ("clean low-T profile", "干净低温剖面"),
    ("当前 checkpoint", "当前阶段验证"),
    ("成 interface 的 regime", "成单值界面的区间"),
    ("topology/profile QC", "拓扑/剖面质量检查"),
    ("ζ fit", "ζ 拟合"),
    ("机器生成的 benchmark receipt", "机器生成的基准测试回执"),
    ("打开 Lesson 06 Python 脚本", "打开第 06 课 Python 脚本"),
    ("打开 CI 保存的 benchmark log", "打开自动化测试保存的基准测试日志"),
    ("Paper1 方法链在这里收口；下一步切到 Paper2 depinning", "第一篇工作的方法链在这里收口；下一步切到第二篇工作的 depinning（退钉扎）"),
    ("Paper1 boundary", "第一篇工作边界"),
    ("clean wall", "干净畴壁"),
    ("field-to-line mapping", "外场到界面驱动力映射"),
    ("EW roughness benchmark", "EW 粗糙度基准测试"),
    ("finite-T mapping boundary", "有限温映射边界"),
    ("RB disorder projection", "RB 无序投影"),
    ("disordered GL/EW geometry checkpoint", "含无序 GL/EW 几何阶段验证"),
    ("Paper1 的 switching / disorder comparison", "第一篇工作的翻转/无序比较"),
    ("asymptotic ζ gate", "渐近 ζ 判据"),
    ("universality 已证明", "普适性已证明"),
    ("time/size ladder", "时间/尺寸阶梯"),
    ("roughness 精修", "粗糙度精修"),
    ("正式主线现在进入 Paper2", "正式主线现在进入第二篇工作"),
    ("isolated wall", "孤立畴壁"),
    ("constant drive", "恒定驱动"),
    ("sample-dependent depinning threshold", "样本依赖的退钉扎阈值"),
    ("Paper1 的 hysteresis / switching coercive scale", "第一篇工作的滞回/翻转矫顽尺度"),
    ("nucleation", "成核"),
    ("protocol-rate effects", "协议速率效应"),
    ("Paper2 的 depinning threshold", "第二篇工作的退钉扎阈值"),
    ("constant drive 下 pinned ↔ moving", "恒定驱动下钉扎 ↔ 运动"),
    ("← Lesson05 · disorder projection", "← 第 05 课 · 无序投影"),
    ("Lesson07 · threshold search →", "第 07 课 · 阈值搜索 →"),
)


def blocked(node: NavigableString) -> bool:
    p = node.parent
    if p is None or p.name in {"script", "style", "pre", "code", "math"}:
        return True
    return bool(p.find_parent(class_="eq") or "eq" in p.get("class", []))


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [x.get_text(" ", strip=False) for x in soup.select(".eq")]
    before_pre = [x.get_text() for x in soup.select("pre")]
    before_hrefs = [x.get("href") for x in soup.find_all("a")]
    before_srcs = [x.get("src") for x in soup.find_all("img")]
    before_results = {x: raw.count(x) for x in LOCKED_RESULTS}

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in REPLACEMENTS:
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    after = str(soup)
    if before_eq != [x.get_text(" ", strip=False) for x in soup.select(".eq")]:
        raise RuntimeError("Lab 06 equations changed")
    if before_pre != [x.get_text() for x in soup.select("pre")]:
        raise RuntimeError("Lab 06 machine/code blocks changed")
    if before_hrefs != [x.get("href") for x in soup.find_all("a")]:
        raise RuntimeError("Lab 06 href wiring changed")
    if before_srcs != [x.get("src") for x in soup.find_all("img")]:
        raise RuntimeError("Lab 06 Figure wiring changed")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 06 locked result changed: {token}")
    if "渐近 ζ 判据：未通过。" not in after:
        raise RuntimeError("Lab 06 asymptotic-zeta failure boundary missing")
    if "CROSS-MODEL GEOMETRY PASS; ASYMPTOTIC ZETA GATE NOT PASSED" not in "\n".join(before_pre):
        raise RuntimeError("Lab 06 machine verdict marker changed")

    TARGET.write_text(after, encoding="utf-8")
    print("Lab 06 Language V2 first pass complete; equations/results/Figure wiring unchanged.")


if __name__ == "__main__":
    main()
