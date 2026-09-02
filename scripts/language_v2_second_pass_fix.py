from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-02.html"
LOCKED_RESULTS = (
    "48/48",
    "2.629×10<sup>−3</sup>",
    "2.764×10<sup>−5</sup>",
    "4.020×10<sup>−4</sup>",
    "0.870339",
)

TEXT_REPLACEMENTS = {
    "Reproduction Lab 02 · 2D Wall Extraction Gold Test": "Reproduction Lab（复现实验室）02 · 二维畴壁提取已知答案测试",
    "Reproduction Lab": "复现实验室",
    "· Lesson 02 · Bulk → Interface": "· 第 02 课 · 体场 → 界面",
    "M07": "模块 07",
    "Paper vs Ours": "论文对照",
    "Code": "代码",
    " / Reproduction Lab / Lesson 02": " / 复现实验室 / 第 02 课",
    "Lesson 01 只证明 1D TDGL 能回到正确的 tanh kink。现在进入 Caballero 2020 真正关键的 model-reduction 步骤：先跑 2D Ginzburg–Landau field，再从每一条 y-column 里提取 φ=0 crossing，把 diffuse wall 压成单值 interface u(y)，最后验证 clean flat wall 应满足 B(r)≈0。": "第 01 课只证明一维 TDGL 能回到正确的 tanh kink（双曲正切扭结）。现在进入 Caballero 2020 真正关键的 model reduction（模型约化）步骤：先跑二维 Ginzburg–Landau（GL）场，再从每一条 y 列中提取 φ=0 零点交叉，把 diffuse wall（弥散畴壁）压成单值界面 u(y)，最后验证无序为零的平直畴壁应满足 B(r)≈0。",
    "只有当每个 y 都恰好有一个 crossing、横截面仍符合 tanh、u(y) 真的变平、B(r) 真的降到接近 0，这个 wall extractor 才算通过。": "只有当每个 y 都恰好有一个零点交叉、横截面仍符合 tanh、u(y) 真的变平、B(r) 真的降到接近 0，这个畴壁提取器才算通过。",
    "0 · 这次开始真的和论文 Figure 并排比": "0 · 这次开始真的和论文 Figure 并排比",
    "2D GL field φ(x,y)、从 bulk field 抽出的 interface，以及横穿 domain wall 的 tanh-like soliton profile。论文 caption 的示例参数": "二维 GL 场 φ(x,y)、从体场抽出的界面，以及横穿畴壁的类 tanh 孤子剖面。论文图注的示例参数",
    "Our small-system gold test。": "本课小系统已知答案测试。",
    "同一个 φ⁴ / Model-A clean framework，但取 T=0，并故意从一条 sinusoidal wavy wall 出发，让 2D TDGL 自己把它拉平；然后用 φ=0 crossing 提取 u(y)。": "同一个 φ⁴ / Model A（A 型模型）无序为零框架，但取 T=0，并故意从一条正弦起伏畴壁出发，让二维 TDGL 自己把它拉平；然后用 φ=0 零点交叉提取 u(y)。",
    "bulk φ(x,y) → wall crossing → u(y) → transverse tanh profile": "体场 φ(x,y) → 畴壁零点交叉 → u(y) → 横向 tanh 剖面",
    "Lesson 03/04 才会开始对论文的 roughness / structure-factor 曲线做定量 thumbnail reproduction。": "第 03/04 课才会开始对论文的 roughness（粗糙度）/ structure factor（结构因子）曲线做定量缩略复现。",
    "如果直接初始化一个完全平的 wall": "如果直接初始化一堵完全平直的畴壁",
    "你的 y-Laplacian 写错了": "你的 y 方向 Laplacian（拉普拉斯算子）写错了",
    "clean T=0、h=0 下，gradient energy 会惩罚弯曲。正确的二维 TDGL 应该让这条墙逐步变平，而不是凭边界条件把它瞬间钉死。": "在无序为零且 T=0、h=0 时，gradient energy（梯度能）会惩罚弯曲。正确的二维 TDGL 应该让这堵畴壁逐步变平，而不是凭边界条件把它瞬间钉死。",
    "每个横截面的 wall profile 仍应接近解析 tanh。": "每个横截面的畴壁剖面仍应接近解析 tanh。",
    "sinusoidal u(y) 应因 line tension 衰减。": "正弦 u(y) 应因 line tension（线张力）衰减。",
    "free energy 应单调下降，而不是靠 extractor “伪造”平墙。": "自由能应单调下降，而不是靠畴壁提取器“伪造”平墙。",
    "2 · 从 diffuse field 提取 u(y)": "2 · 从弥散场提取 u(y)",
    "的 column，寻找唯一一对相邻格点满足": "这一列中，寻找唯一一对相邻格点满足",
    "Extractor 的真正 hard gate": "畴壁提取器的真正硬性验收条件",
    "如果出现 bubble、overhang 或多重 crossing，就不应该继续默默算一个 u(y)。这正是网站前面一直强调的 topology gate：elastic-line observable 只有在 single-valued mapping 成立时才合法。": "如果出现 bubble（气泡畴）、overhang（悬垂）或多重零点交叉，就不应该继续默默计算一个 u(y)。这正是网站前面一直强调的 topology gate（拓扑判据）：elastic line（弹性线）可观测量只有在 single-valued mapping（单值映射）成立时才合法。",
    "3 · 为什么 flat wall 的 B(r) 是另一个独立验收？": "3 · 为什么平直畴壁的 B(r) 是另一个独立验收？",
    "如果最终 wall 真正变成平直单墙": "如果最终畴壁真正变成平直单墙",
    "这里不是拟合 ζ，也不是追求 power law；它只是检验“wall extraction + y 方向动力学”是否自洽。": "这里不是拟合 ζ，也不是追求幂律；它只是检验“畴壁提取 + y 方向动力学”是否自洽。",
    "Lesson 01 验的是 solver 的横向 wall profile；Lesson 02 新增的是 wall geometry estimator。": "第 01 课验证的是求解器的横向畴壁剖面；第 02 课新增的是畴壁几何估计量。",
    "Lesson 03 给它加 thermal noise，再去看真实的 roughness growth。": "第 03 课给它加热噪声，再去看真实的粗糙度增长。",
    "4 · 实际运行结果：四个 gate 一起过": "4 · 实际运行结果：全部验收条件一起通过",
    "Hard gate": "硬性验收条件",
    "single crossing": "单一零点交叉",
    "columns 合法": "列合法",
    "PASS": "通过",
    "final wall RMS": "最终畴壁 RMS",
    "max B(r)": "最大 B(r)",
    "tanh profile RMSE": "tanh 剖面 RMSE",
    "free energy": "自由能",
    "sampled F(t) 单调不增": "采样的 F(t) 单调不增",
    "原论文 Figure 告诉我们应该复现怎样的模型结构；解析 tanh、single-crossing topology、B(r)≈0 和 energy descent 则分别从不同方向检查代码。": "原论文 Figure 告诉我们应该复现怎样的模型结构；解析 tanh、单一零点交叉拓扑、B(r)≈0 和自由能下降则分别从不同方向检查代码。",
    "① 2D Laplacian": "① 二维 Laplacian（拉普拉斯算子）",
    "x 用固定边界，y 用 periodic boundary。": "x 用固定边界，y 用 periodic boundary（周期边界）。",
    "② Wavy initial wall": "② 起伏初始畴壁",
    "让 line tension 有真实工作要做。": "让线张力真正参与弛豫。",
    "③ Zero crossing": "③ 零点交叉",
    "把 diffuse φ(x,y) 压成 u(y)。": "把弥散 φ(x,y) 压成 u(y)。",
    "从几何线计算最基础 roughness observable。": "从几何线计算最基础的粗糙度可观测量。",
    "脚本会生成上面的 4-panel 结果图，并自动执行全部 hard gates。": "脚本会生成上面的四面板结果图，并自动执行全部硬性验收条件。",
    "7 · 这一步在你的 sliding-FE 项目里对应什么？": "7 · 这一步在你的滑移铁电项目里对应什么？",
    "φ=0 crossing": "φ=0 零点交叉",
    "从 phase field 提取 wall contour": "从 phase field（相场）提取畴壁轮廓",
    "single-crossing gate": "单一零点交叉判据",
    "overhang / bubble / multiple-wall diagnostic": "悬垂 / 气泡畴 / 多畴壁诊断",
    "mapping 失败时不能硬套 elastic-line universality": "映射失败时不能硬套弹性线普适性",
    "B(r)≈0 clean test": "B(r)≈0 无序为零测试",
    "roughness estimator regression test": "粗糙度估计量回归测试",
    "避免以后 disorder roughness 其实来自 extractor bias": "避免以后无序粗糙度其实来自提取器偏差",
    "wavy-wall relaxation": "起伏畴壁弛豫",
    "clean E=0 wall stability": "无序为零、E=0 的畴壁稳定性",
    "先确认 wall 自己稳定，再讨论 driven depinning": "先确认畴壁自身稳定，再讨论受驱退钉扎",
    "8 · Lesson 03：开始第一次真正的论文曲线复现": "8 · 第 03 课：开始第一次真正的论文曲线复现",
    "下一课不再只是 gold test。": "下一课不再只是已知答案测试。",
    "保留同一个 2D clean wall，加 Caballero Eq. (4) 的 thermal white noise；同时跑 1D Edwards–Wilkinson line。": "保留同一个二维无序为零畴壁，加 Caballero Eq. (4) 的 thermal white noise（热白噪声）；同时跑一维 Edwards–Wilkinson（EW）线。",
    "B(r,t) scaling curve 与我们的 small-system curve 并排，做真正的 thumbnail reproduction，并用解析 EW prediction 检查有限尺寸偏差。": "B(r,t) 标度曲线与我们的小系统曲线并排，做真正的缩略复现，并用解析 EW 预测检查有限尺寸偏差。",
    "← Lesson 01 · 1D kink gold test": "← 第 01 课 · 一维扭结已知答案测试",
    "Lesson 03 · EW roughness thumbnail →": "第 03 课 · EW 粗糙度缩略复现 →",
}


def equation_body_text(eq) -> str:
    clone = BeautifulSoup(str(eq), "html.parser").select_one(".eq")
    for small in clone.select("small"):
        small.decompose()
    return clone.get_text(" ", strip=False)


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [equation_body_text(eq) for eq in soup.select(".eq")]
    before_pre = [pre.get_text() for pre in soup.select("pre")]
    before_code = [code.get_text() for code in soup.select("code")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]
    before_src = [img.get("src") for img in soup.find_all("img")]
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

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 02 expected 2 Figures, found {len(figures)}")
    figures[0]["alt"] = "Caballero 2020 Figure 1：二维 GL 体场与提取界面"
    figures[1]["alt"] = "本课二维 GL 场、提取畴壁、B(r) 与解析剖面对照"

    if [equation_body_text(eq) for eq in soup.select(".eq")] != before_eq:
        raise RuntimeError("Lab 02 equation body changed")
    if [pre.get_text() for pre in soup.select("pre")] != before_pre:
        raise RuntimeError("Lab 02 preformatted code/output changed")
    if [code.get_text() for code in soup.select("code")] != before_code:
        raise RuntimeError("Lab 02 inline code changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Lab 02 links changed")
    if [img.get("src") for img in soup.find_all("img")] != before_src:
        raise RuntimeError("Lab 02 Figure wiring changed")

    rendered = str(soup)
    after_results = {token: rendered.count(token) for token in LOCKED_RESULTS}
    if after_results != before_results:
        raise RuntimeError(f"Lab 02 locked results changed: {before_results} -> {after_results}")

    TARGET.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
