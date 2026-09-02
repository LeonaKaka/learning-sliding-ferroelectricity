from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-05.html"
LOCKED_RESULTS = (
    "0.071833070",
    "0.0000002%",
    "0.0000012%",
    "0.995554",
    "0.222%",
    "0.445%",
    "0.104%",
    "1.039429",
    "1.039472",
    "0.099555",
)

REPLACEMENTS = (
    ("· Lesson 05 · Disorder Projection", "· 第 05 课 · 无序投影"),
    ("Paper vs Ours", "论文对照"),
    ("Code", "代码"),
    (" / Reproduction Lab / Lesson 05", " / 复现实验室 / 第 05 课"),
    ("bulk 里是白噪声 RB，interface 为什么看到的是有相关长度的 pinning force？", "体场里是白噪声 RB，界面为什么看到有相关长度的钉扎力？"),
    ("bulk Ginzburg–Landau 势垒高度里加入 delta-correlated random-bond disorder", "体场 Ginzburg–Landau（GL）势垒高度里加入 delta-correlated random-bond disorder（δ 相关随机键无序）"),
    ("然后把它投影到 domain wall", "然后把它投影到 domain wall（畴壁）"),
    ("经过有限宽度 wall profile 的投影以后，interface 实际感受到的 pinning force 在位移 u 方向变成短程相关，其 correlation length 是 wall width 的量级。", "经过有限宽度畴壁剖面的投影以后，界面实际感受到的 pinning force（钉扎力）在位移 u 方向变成短程相关，其 correlation length（相关长度）与畴壁宽度同量级。"),
    ("Eq.25 的 projection-kernel autocorrelation", "Eq.25 的投影核自相关函数"),
    ("从 bulk disorder 得到的", "从体场无序得到的"),
    ("sample correlator", "样本相关函数"),
    ("continuum white noise", "continuum white noise（连续白噪声）"),
    ("网格幅度必须随", "离散幅度必须随"),
    ("0 · 原论文 Fig.4 vs 我们的 bulk-projection reproduction", "0 · 原论文 Fig.4 与我们的体场投影复现"),
    ("256 个独立 pinning-force realizations 的相关函数", "256 个独立钉扎力样本的相关函数"),
    ("Inset 展示 4 条", "插图展示 4 条"),
    ("disordered-interface dynamics", "disordered interface（无序界面）动力学"),
    ("correlator gold test", "相关函数已知答案测试"),
    ("Our reproduction。", "本课复现。"),
    ("统计仍用 256 realizations", "统计仍用 256 个独立无序样本"),
    ("continuum-normalized bulk", "按连续极限归一化的体场"),
    ("bulk→interface", "体场→界面"),
    ("这次比 Lesson04 还便宜", "这次比第 04 课还便宜"),
    ("paper-size 的", "论文同规模的"),
    ("bulk random-bond disorder 到底加在哪里？", "体场 random-bond disorder（随机键无序）到底加在哪里？"),
    ("直接给 interface 一个随机力", "直接给界面一个随机力"),
    ("bulk double-well barrier", "体场 double-well barrier（双阱势垒）"),
    ("zero-mean、delta-correlated Gaussian field", "零均值、δ 相关 Gaussian field（高斯场）"),
    ("barrier-amplitude / random-bond-like coupling", "barrier-amplitude coupling（势垒幅度耦合）/ 类随机键耦合"),
    ("直接 local bias", "直接的局域偏置"),
    ("和你的 sliding-FE 项目怎么接？", "和你的滑移铁电项目怎么接？"),
    ("barrier-amplitude disorder", "势垒幅度无序"),
    ("coupling 思路", "耦合思路"),
    ("periodic stacking potential", "periodic stacking potential（周期性堆垛势）"),
    ("coupling → generalized force → interface projection → effective correlator", "耦合 → generalized force（广义力）→ 界面投影 → effective correlator（有效相关函数）"),
    ("wall 本身就是一个空间滤波器", "畴壁本身就是一个空间滤波器"),
    ("clean soliton ansatz", "无序为零的 soliton ansatz（孤子假设）"),
    ("bulk ζ", "体场 ζ"),
    ("它先被 kernel", "它先被 kernel（核函数）"),
    ("wall 附近显著，wall width w 自然成为 effective disorder correlation length 的来源。", "畴壁附近显著，畴壁宽度 w 自然成为 effective disorder correlation length（有效无序相关长度）的来源。"),
    ("代码里它就是一次 cross-correlation", "代码里它就是一次 cross-correlation（互相关）"),
    ("先让两个 theory route 自己闭合", "先让两条理论路线自行闭合"),
    ("projection kernel", "投影核"),
    ("soliton profile", "孤子剖面"),
    ("两条路线完全分开实现", "两条理论路线完全分开实现"),
    ("离散 kernel autocorrelation", "离散核自相关函数"),
    ("解析双曲函数表达式", "解析双曲函数表达式"),
    ("0/0 cancellation 区域", "0/0 数值消减区域"),
    ("Taylor 展开", "Taylor（泰勒）展开"),
    ("先要求 Eq.25 与 Eq.26 自己通过 hard gate", "先要求 Eq.25 与 Eq.26 自己通过硬性验收条件"),
    ("wall width", "畴壁宽度"),
    ("Γ first zero", "Γ 首零点"),
    ("correlation scale 与 Γ amplitude 都由 bulk coupling + soliton profile 决定。", "相关尺度与 Γ 幅度都由体场耦合和孤子剖面决定。"),
    ("continuum white noise 不是“每格 std=1”", "连续白噪声不是“每格 std=1”"),
    ("正确 vs 故意错误", "正确归一化与故意错误对照"),
    ("正确 continuum 目标", "正确的连续极限目标"),
    ("二维 delta-correlated field 对应的 amplitude scaling", "二维 δ 相关场对应的幅度缩放"),
    ("我们尽量贴论文 protocol，但不伪装成完全相同", "我们尽量贴近论文协议，但不伪装成完全相同"),
    ("realizations", "独立无序样本"),
    ("grid spacing", "网格间距"),
    ("Eq.27 Fourier synthesis", "Eq.27 Fourier synthesis（傅里叶合成）"),
    ("bulk ζ → Eq.23 projection", "体场 ζ → Eq.23 投影"),
    ("theory target", "理论目标"),
    ("Eq.25 numerical + independent analytic Eq.26", "Eq.25 数值投影 + 独立解析 Eq.26"),
    ("model reduction", "model reduction（模型约化）"),
    ("Hard gates：相关函数必须定量对上", "硬性验收条件：相关函数必须定量对上"),
    ("quantity", "量"),
    ("result", "结果"),
    ("gate", "验收条件"),
    ("analytic Eq.26", "解析 Eq.26"),
    ("reference", "参考值"),
    ("sample RMSE", "样本 RMSE"),
    ("sample max", "样本最大误差"),
    ("normalized-shape RMSE", "归一化形状 RMSE"),
    ("diagnostic", "诊断量"),
    ("first zero: theory", "首零点：理论"),
    ("first zero: empirical", "首零点：经验"),
    ("difference", "差值"),
    ("theory amplitude", "理论幅度"),
    ("normalization error", "归一化错误"),
    ("ALL DISORDER-PROJECTION GATES PASS。", "无序投影全部验收条件：通过。"),
    ("analytic Eq.26、Eq.25 projection、sample amplitude/shape/zero crossing", "解析 Eq.26、Eq.25 投影、样本幅度/形状/零点交叉"),
    ("打开 Lesson 05 Python 脚本", "打开第 05 课 Python 脚本"),
    ("time integration", "时间积分"),
    ("paper-size correlation test", "论文同规模的相关函数测试"),
    ("查看本次 run receipt", "查看本次运行回执"),
    ("RB bulk coupling", "RB 体场耦合"),
    ("soliton 投影后产生短程相关 pinning force", "孤子投影后产生短程相关钉扎力"),
    ("Eq.25 numerical projection 与 analytic Eq.26", "Eq.25 数值投影与解析 Eq.26"),
    ("continuum white-noise normalization", "连续白噪声归一化"),
    ("depinning exponent", "退钉扎指数"),
    ("RF 与 RB 同 universality", "RF 与 RB 属于同一 universality（普适类）"),
    ("sliding-FE 的真实 defect", "滑移铁电中的真实缺陷"),
    ("φ⁴ RB model", "φ⁴ RB 模型"),
    ("RF term", "RF 项"),
    ("barrier-amplitude term", "势垒幅度项"),
    ("φ-dependence", "φ 依赖"),
    ("投影到 wall", "投影到畴壁"),
    ("effective force correlator", "effective force correlator（有效力相关函数）"),
    ("amplitude", "幅度"),
    ("RF↔RB isolated-wall universality comparison", "RF↔RB 孤立畴壁普适性比较"),
    ("effective wall-level disorder statistics", "effective wall-level disorder statistics（有效畴壁层级无序统计）"),
    ("Lesson 06：从 correlator gold test 进入真正的 disordered wall geometry", "第 06 课：从相关函数已知答案测试进入真正的无序畴壁几何"),
    ("large-scale roughness", "大尺度粗糙度"),
    ("thermal regime", "thermal regime（热涨落区间）"),
    ("random-bond roughness", "random-bond roughness（随机键粗糙度）"),
    ("正确的 disorder correlator 是否产生正确的 interface geometry", "正确的无序相关函数是否产生正确的界面几何"),
    ("← Lesson 04 · GL→EW validity boundary", "← 第 04 课 · GL→EW 适用边界"),
    ("Lesson 06 · disordered GL↔EW geometry →", "第 06 课 · 无序 GL↔EW 几何 →"),
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
    before_code = [x.get_text() for x in soup.select("code")]
    before_hrefs = [x.get("href") for x in soup.find_all("a")]
    before_srcs = [x.get("src") for x in soup.find_all("img")]
    before_results = {x: raw.count(x) for x in LOCKED_RESULTS}

    soup.title.string = "Reproduction Lab（复现实验室）05 · 体场 RB → 钉扎力"
    bar_b = soup.select_one(".bar b")
    if bar_b is None or not bar_b.contents:
        raise RuntimeError("Lab 05 header missing")
    if isinstance(bar_b.contents[0], NavigableString):
        bar_b.contents[0].replace_with("Reproduction Lab（复现实验室） ")

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in REPLACEMENTS:
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 05 expected 2 Figures, found {len(figures)}")
    figures[0]["alt"] = "Caballero 2020 图 4：钉扎力相关函数"
    figures[1]["alt"] = "本课体场随机键无序投影与钉扎力相关函数"

    after = str(soup)
    if before_eq != [x.get_text(" ", strip=False) for x in soup.select(".eq")]:
        raise RuntimeError("Lab 05 equations changed")
    if before_pre != [x.get_text() for x in soup.select("pre")]:
        raise RuntimeError("Lab 05 machine/code pre blocks changed")
    if before_code != [x.get_text() for x in soup.select("code")]:
        raise RuntimeError("Lab 05 inline code changed")
    if before_hrefs != [x.get("href") for x in soup.find_all("a")]:
        raise RuntimeError("Lab 05 href wiring changed")
    if before_srcs != [x.get("src") for x in soup.find_all("img")]:
        raise RuntimeError("Lab 05 Figure wiring changed")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 05 locked result changed: {token}")

    TARGET.write_text(after, encoding="utf-8")
    print("Lab 05 Language V2 first pass complete; equations/code/results/wiring unchanged.")


if __name__ == "__main__":
    main()
