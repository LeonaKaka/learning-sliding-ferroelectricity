from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-04.html"
LOCKED_RESULTS = (
    "7.67%", "7.57%", "4.49%", "4.36%",
    "0.9879", "1.3738", "0.9870", "1.3740",
    "26.52%", "1.6664", "0.9806", "5.47%",
    "40.51%", "1.7018", "0.9760", "7.23%",
)

TEXT_REPLACEMENTS = {
    "· Lesson 04 · Model Reduction Boundary": "· 第 04 课 · 模型约化适用边界",
    "Paper vs Ours": "论文对照",
    "Code": "代码",
    " / Reproduction Lab / Lesson 04": " / 复现实验室 / 第 04 课",
    "最重要的不只是“映射成功”：还要知道什么时候该停止把 bulk wall 当 elastic line": "最重要的不只是“映射成功”：还要知道什么时候该停止把体场畴壁当作弹性线",
    "Caballero 2020 的真正价值，不只是证明 2D Ginzburg–Landau 可以降成 1D Edwards–Wilkinson。论文还明确测试了这个 reduction 的适用边界：低温时两种描述吻合；温度升高、bulk fluctuation 变强后，soliton ansatz 与 single-valued interface picture 会逐渐失效。这一课就复现“通过 + 失败”两边。": "Caballero 2020 的真正价值，不只是证明二维 Ginzburg–Landau（GL）可以约化成一维 Edwards–Wilkinson（EW）。论文还明确测试了这种 model reduction（模型约化）的适用边界：低温时两种描述吻合；温度升高、体场涨落增强后，soliton ansatz（孤子假设）与 single-valued interface（单值界面）描述会逐渐失效。这一课就同时复现“通过”和“失效”两侧。",
    "低温要通过 Eq.19 hard gate；高温则不允许为了“复现成功”继续调参数。只要 bulk→line mapping 的诊断一起恶化，就应该把结果标成 mapping breakdown，而不是硬塞一个 ζ。": "低温必须通过 Eq.19 的硬性验收条件；高温则不允许为了“复现成功”继续调参数。只要体场到弹性线映射的多项诊断一起恶化，就应该明确标成映射失效，而不是硬塞一个 ζ。",
    "0 · 原论文 Fig.3 vs 我们的 boundary thumbnail": "0 · 原论文 Fig.3 与我们的适用边界缩略复现",
    "Our CPU-fast boundary thumbnail。": "本课的 CPU 快速适用边界缩略复现。",
    "只取 T=0.05 与 T=0.30、t=10 与 100。左上：低温 GL extracted-wall roughness 对 EW Eq.19；右上：高温偏离；下排同时看 fitted wall width 与多 crossing / error diagnostics。": "只取 T=0.05 与 T=0.30、t=10 与 100。左上：低温 GL 提取畴壁的粗糙度对照 EW Eq.19；右上：高温偏离；下排同时检查拟合畴壁宽度、多重零点交叉与误差诊断。",
    "这不是 Fig.3 的 protocol-identical reproduction。": "这不是 Fig.3 的同协议复现。",
    "12 realizations 的快速 boundary test。它的作用是先验证“低 T 通过、高 T 失败”这个方法结构，再决定值不值得跑大尺寸。": "12 个独立热噪声样本的快速适用边界测试。它的作用是先验证“低温通过、高温失效”这个方法结构，再决定是否值得跑大尺寸。",
    "1 · 先修正 Lesson 02 的一个教学简化：finite T 不能只找 zero crossing": "1 · 先修正第 02 课的一个教学简化：有限温度不能只找零点交叉",
    "Lesson 02 在 T=0 的 clean wall 上用 φ=0 crossing 很合适，因为每一列只有一个干净 crossing。但论文在 finite T 下采用更严格的 estimator：对固定 y,t 的整个 transverse profile φ(x,y,t) 拟合 soliton，并把 {φ₀,w,u(y)} 都作为 fitting parameters。": "第 02 课在 T=0 的无序为零畴壁上用 φ=0 零点交叉很合适，因为每一列只有一个干净的交叉点。但论文在有限温度下采用更严格的 estimator（估计量）：对固定 y,t 的整个横向剖面 φ(x,y,t) 拟合孤子，并把 {φ₀,w,u(y)} 都作为拟合参数。",
    "zero crossing 只做初始化，不做最终 estimator": "零点交叉只用于初始化，不作为最终估计量",
    "thermal fluctuation 会同时扰动 domain interior、wall amplitude、wall width 和 apparent crossing。只用一格之间的符号变化，容易把 bulk noise 当作 wall displacement；拟合整段 profile 则利用了 wall 的完整形状信息。": "热涨落会同时扰动畴内部、畴壁幅度、畴壁宽度和表观零点交叉。只用相邻格点间的符号变化，容易把体场噪声误当成畴壁位移；拟合整段剖面则利用了畴壁的完整形状信息。",
    "2 · 论文 protocol 与我们哪里相同、哪里缩小？": "2 · 论文协议与我们哪里相同、哪里缩小？",
    "boundary": "边界条件",
    "y periodic；x Dirichlet": "y 方向周期边界；x 方向 Dirichlet（狄利克雷）边界",
    "锁住单一 domain wall": "锁住单一畴壁",
    "mesh": "网格",
    "time step": "时间步",
    "semi-implicit Euler，Δt=0.1": "semi-implicit Euler（半隐式欧拉），Δt=0.1",
    "Δt=0.1；linear Laplacian implicit": "Δt=0.1；线性 Laplacian（拉普拉斯算子）隐式处理",
    "保持同一量级；实现细节不是逐行复制论文代码": "保持同一量级；实现细节不是逐行复制论文代码",
    "system size": "系统尺寸",
    "快速 thumbnail": "快速缩略复现",
    "temperature": "温度",
    "先取两端测试 validity boundary": "先取两端测试适用边界",
    "time": "时间",
    "先做即时可验收版": "先做可快速验收的版本",
    "wall estimator": "畴壁估计量",
    "zero crossing 只初始化 fit": "零点交叉只用于初始化拟合",
    "3 · 2D thermal noise：这次真的回到 bulk FDT": "3 · 二维 thermal noise（热噪声）：这次真的回到体场 FDT",
    "因此二维 cell 面积 ΔxΔy、时间步 Δt 下，直接加到 φ update 的 stochastic increment 是：": "因此在二维网格单元面积 ΔxΔy、时间步 Δt 下，直接加到 φ 更新中的随机增量是：",
    "这一行不能从 Lesson 03 的 1D EW 代码直接复制。": "这一行不能从第 03 课的一维 EW 代码直接复制。",
    "1D line 的 noise normalization 用 dy；2D bulk 用 dx·dy。模型降维以后 friction/noise 也通过论文 Eq.13–16 被重新投影，不能靠“同一个 seed 同一个 sigma”代替推导。": "一维弹性线的噪声归一化使用 dy；二维体场使用 dx·dy。模型降维以后，摩擦项与噪声也通过论文 Eq.13–16 被重新投影，不能靠“同一个随机种子、同一个 σ”代替推导。",
    "4 · 低温 T=0.05：mapping 必须先过": "4 · 低温 T=0.05：映射必须先通过",
    "Eq.19 median error": "Eq.19 中位相对误差",
    "RMS error": "RMS 相对误差",
    "mean fitted φ₀": "拟合 φ₀ 均值",
    "mean fitted w": "拟合 w 均值",
    "论文在 T=0.05 的 fit diagnostics 报告 mean φ₀≈0.99、mean w≈1.38，而 clean equilibrium 值是 φ₀=1、w=√2≈1.414。我们的 thumbnail 均值已经落在同一位置；但我们没有声称复现论文的标准差，因为系统尺寸、realization 数与 integrator implementation 都不同。": "论文在 T=0.05 的拟合诊断中报告 φ₀ 均值约 0.99、w 均值约 1.38，而无序为零的平衡值是 φ₀=1、w=√2≈1.414。我们的缩略复现均值已经落在同一位置；但我们没有声称复现论文的标准差，因为系统尺寸、独立样本数和积分器实现都不同。",
    "LOW-T MAPPING PASS。": "低温映射：通过。",
    "在预先固定的 4≤r≤32 窗口内，低温 GL roughness 能在约 5–8% 内跟随 EW Eq.19，同时 fitted profile 仍接近 clean soliton。这时把 bulk wall 压成 u(y) 是有证据支撑的。": "在预先固定的 4≤r≤32 尺度区间内，低温 GL 粗糙度能在约 5–8% 误差内跟随 EW Eq.19，同时拟合剖面仍接近无序为零的孤子。这时把体场畴壁压成 u(y) 是有证据支撑的。",
    "5 · 高温 T=0.30：这次“失败”才是应该出现的答案": "5 · 高温 T=0.30：这次“失效”才是应该出现的答案",
    "mean fitted w": "拟合 w 均值",
    "width std": "宽度标准差",
    "multi-cross columns": "多重交叉列占比",
    "HIGH-T BREAKDOWN DETECTED。": "高温映射失效：已检测到。",
    "roughness 不再跟 Eq.19，wall-width distribution 急剧变宽，还开始出现同一 y-column 的 multiple crossings。这里如果继续只提一条 u(y)、再拟合 ζ，得到的“漂亮 exponent”反而会掩盖 estimator 已失效。": "粗糙度不再跟随 Eq.19，畴壁宽度分布急剧变宽，还开始出现同一 y 列中的多重零点交叉。这里如果继续只提一条 u(y)、再拟合 ζ，得到的“漂亮指数”反而会掩盖估计量已经失效。",
    "GL→EW reduction 建立在 low-noise / solitonic ansatz 上；对于 α=δ=γ=η=1，特征温度 T*≈1，随着 T 增大，bulk fluctuations 增强；论文 Fig.3 中 T>0.15 已观察到系统性偏离。": "GL→EW 模型约化建立在低噪声与孤子假设上；对于 α=δ=γ=η=1，特征温度 T*≈1，随着 T 增大，体场涨落增强；论文 Fig.3 中 T>0.15 已观察到系统性偏离。",
    "6 · 这节真正教给你的不是 Caballero，而是一个 universality gate": "6 · 这节真正教给你的不是 Caballero，而是一个普适性判据",
    "先验 mapping": "先验证映射",
    "先证明 bulk field 能稳定压成单值 u(y)，再调用 elastic-interface theory。": "先证明体场能稳定压成单值 u(y)，再调用 elastic interface（弹性界面）理论。",
    "同时验 geometry": "同时验证几何结构",
    "B(r) 对上还不够；profile width、fit residual、crossing topology 也要一起正常。": "B(r) 对上还不够；剖面宽度、拟合残差和零点交叉拓扑也要一起正常。",
    "失败要降级 claim": "失效时要降低结论强度",
    "mapping gate 失败时，正确语言是 crossover / bulk-interface breakdown，而不是强给 universality label。": "映射判据失败时，正确语言是 crossover（交叉）或体场—界面描述失效，而不是强行给出普适性标签。",
    "直接对应你的 sliding-FE Paper2：": "直接对应你的滑移铁电第二篇研究：",
    "你后面从 phase field 提取 wall contour、算 B(r)/S(q)、再拟合 ζ/β/ν 时，也应该先做这套 gate。尤其 sliding-FE 的 wall profile 不是 φ⁴ tanh；应使用你的 periodic stacking landscape 对应的 clean wall template / contour rule，而不是把 Caballero 的 tanh 生搬过去。": "你后面从 phase-field（相场）提取畴壁轮廓、计算 B(r)/S(q)、再拟合 ζ/β/ν 时，也应该先做这套判据。尤其滑移铁电的畴壁剖面不是 φ⁴ tanh；应使用周期性堆垛势能面对应的无序为零畴壁模板或轮廓判据，而不是把 Caballero 的 tanh 生搬过去。",
    "7 · 完整脚本与 hard gates": "7 · 完整脚本与硬性验收条件",
    "打开 Lesson 04 Python 脚本 →": "打开第 04 课 Python 脚本 →",
    "这类“必须失败”的测试非常重要。一个 reproduction suite 如果所有 gate 都只接受“越来越像理论”，它就无法发现理论适用边界。": "这类“必须失效”的测试非常重要。如果一套复现测试只接受“越来越像理论”，它就无法发现理论适用边界。",
    "8 · 下一课：disorder 不只是“往方程里加随机数”": "8 · 下一课：无序不只是“往方程里加随机数”",
    "Caballero 的 Sec.IV 从 bulk random-bond disorder 出发，推导出 interface 看到的是一个具有有限 u-correlation length 的 pinning force。下一课最适合先复现论文 Fig.4：从理论 Γ(u) 生成很多 Fp(u,y)，直接检查 sample correlator 是否回到 Γ(u)。这一步算力很小，却是进入 quenched-disorder / depinning 前非常强的 gold test。": "Caballero 的 Sec. IV 从 bulk random-bond disorder（体场随机键无序）出发，推导出界面看到的是具有有限 u-correlation length（u 方向相关长度）的 pinning force（钉扎力）。下一课先复现论文 Fig.4：从理论 Γ(u) 生成许多 Fp(u,y)，直接检查样本相关函数是否回到 Γ(u)。这一步算力很小，却是进入 quenched disorder（冻结无序）与 depinning（退钉扎）之前很强的已知答案测试。",
    "← Lesson 03 · EW roughness": "← 第 03 课 · EW 粗糙度",
    "Lesson 05 · bulk RB → pinning correlator →": "第 05 课 · 体场 RB → 钉扎相关函数 →",
}


def equation_body_text(eq) -> str:
    clone = BeautifulSoup(str(eq), "html.parser").select_one(".eq")
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

    soup.title.string = "Reproduction Lab（复现实验室）04 · GL → EW 适用边界"
    bar_b = soup.select_one(".bar b")
    if bar_b is None or not bar_b.contents:
        raise RuntimeError("Lab 04 header missing")
    if isinstance(bar_b.contents[0], NavigableString):
        bar_b.contents[0].replace_with("Reproduction Lab（复现实验室） ")

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
        raise RuntimeError(f"Lab 04 expected 2 Figures, found {len(figures)}")
    figures[0]["alt"] = "Caballero 2020 图 3：温度升高时 GL 到 EW 映射逐渐失效"
    figures[1]["alt"] = "本课低温 GL→EW 映射通过与高温映射失效对照"

    after = str(soup)
    after_eq = [equation_body_text(eq) for eq in soup.select(".eq")]
    after_pre = [pre.get_text() for pre in soup.select("pre")]
    after_code = [code.get_text() for code in soup.select("code")]
    after_hrefs = [a.get("href") for a in soup.find_all("a")]
    after_src = [img.get("src") for img in soup.find_all("img")]

    if before_eq != after_eq:
        raise RuntimeError("Lab 04 equation bodies changed during Language V2 pass")
    if before_pre != after_pre or before_code != after_code:
        raise RuntimeError("Lab 04 code/machine receipt text changed during Language V2 pass")
    if before_hrefs != after_hrefs or before_src != after_src:
        raise RuntimeError("Lab 04 link/Figure wiring changed during Language V2 pass")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 04 locked numerical result changed: {token}")

    TARGET.write_text(after, encoding="utf-8")
    print(
        f"Updated {TARGET.relative_to(ROOT)}; locked {len(before_eq)} equations, "
        f"{len(before_pre)} pre blocks, {len(before_hrefs)} links, {len(LOCKED_RESULTS)} numerical results."
    )


if __name__ == "__main__":
    main()
