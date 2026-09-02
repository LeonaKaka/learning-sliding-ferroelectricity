from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-09.html"
LOCKED_RESULTS = (
    "0.267993", "0.229890", "0.195041", "0.165810",
    "0.102183", "0.030", "0.001004", "0.245", "L=32",
)
EXPECTED_SRCS = (
    "../assets/reproduction-lab/source-ferrero2013-pre-fig5-full.png",
    "../assets/reproduction-lab/lesson09_mean_v_loglog.png",
    "../assets/reproduction-lab/lesson09_beta_vs_window.png",
    "../assets/reproduction-lab/lesson09_threshold_sensitivity.png",
    "../assets/reproduction-lab/lesson09_bootstrap_beta.png",
)
REPLACEMENTS = (
    ("<title>Reproduction Lab 09 · Beta window stability</title>", "<title>Reproduction Lab（复现实验室）09 · β 拟合区间稳定性</title>"),
    ("<b>Reproduction Lab <small>· Lesson 09 · Paper2 Method Track</small></b>", "<b>Reproduction Lab（复现实验室） <small>· 第 09 课 · 第二篇工作方法线</small></b>"),
    ("<a href=\"../index.html\">Learning Sliding Ferroelectricity</a> / Reproduction Lab / Lesson 09", "<a href=\"../index.html\">Learning Sliding Ferroelectricity</a> / 复现实验室 / 第 09 课"),
    ("<span class=\"tag\">β window audit</span><span class=\"tag\">8 disorder realizations</span><span class=\"tag\">no post-hoc tuning</span>", "<span class=\"tag\">β 拟合区间审计</span><span class=\"tag\">8 个独立无序样本</span><span class=\"tag\">禁止事后挑点</span>"),
    ("<h1>一条漂亮的 log–log 直线，不等于 universal β</h1>", "<h1>一条漂亮的双对数直线，不等于普适 β</h1>"),
    ("<p class=\"lead\">Ferrero 的关键提醒不是“正确答案等于 0.245”，而是 <b>mesoscopic corrections 会制造 biased effective exponents</b>。因此 L09 只问：当我们按预注册规则逐步缩小 Δf window，β 有没有形成稳定 plateau？</p>", "<p class=\"lead\">Ferrero 的关键提醒不是“正确答案等于 0.245”，而是 <b>mesoscopic corrections（介观修正）会制造有偏的 effective exponent（有效指数）</b>。因此 L09 只问：按照预先登记的规则逐步缩小 Δf 拟合区间时，β 是否形成稳定平台。</p>"),
    ("<div class=\"read-order\"><div><b>1 · 论文 Fig.5</b><span>同一 critical relaxation 出现不同 effective slopes。</span></div><div><b>2 · 我们的 v(Δf)</b><span>8 个 realization 的 mean velocity。</span></div><div><b>3 · β vs window</b><span>真正的授权 gate。</span></div><div><b>4 · 排除替代解释</b><span>fc bracket 与 bootstrap 都不能救 window drift。</span></div></div>", "<div class=\"read-order\"><div><b>1 · 论文 Fig.5</b><span>同一次临界弛豫在不同尺度上出现不同有效斜率。</span></div><div><b>2 · 我们的 v(Δf)</b><span>对 8 个独立无序样本取算术平均。</span></div><div><b>3 · β 随拟合区间变化</b><span>这是决定是否授权 β 的核心判据。</span></div><div><b>4 · 排除替代解释</b><span>阈值区间与 bootstrap（自助法）都不能消除拟合区间漂移。</span></div></div>"),
    ("<h2>0 · 论文原图：corrections-to-scaling 是看得见的</h2>", "<h2>0 · 论文原图：corrections-to-scaling（标度修正）是看得见的</h2>"),
    ("alt=\"Ferrero PRE 2013 Figure 5 full crop\"", "alt=\"Ferrero PRE 2013 图 5 完整原图区域\""),
    ("完整保留 velocity panel (a)、width panel (b)、两段 power-law guide 与原始 caption。panel (a) 在不同时间区间给出约 0.16 与 0.13 的 effective decay slope，正是“一个局部 power law 不代表 asymptotic exponent”的直观例子。", "完整保留速度子图 (a)、宽度子图 (b)、两段幂律参考线和论文原始图注。子图 (a) 在不同时间区间给出约 0.16 与 0.13 的有效衰减斜率，直观说明：局部幂律并不等于 asymptotic exponent（渐近指数）。"),
    ("<div class=\"bridge\"><b>我们不是拿 Fig.5 的 time slope 去直接比较 β。</b> 它提供的是方法论证据：临界附近存在 crossover / corrections-to-scaling，所以 steady v(f) 的 β 也必须做 scale-window stability，而不能只挑一个最像 benchmark 的窗口。</div>", "<div class=\"bridge\"><b>我们不是拿 Fig.5 的时间斜率直接比较 β。</b> 它提供的是方法论证据：临界附近存在 crossover（交叉）与标度修正，因此稳态 v(f) 的 β 也必须检查拟合区间稳定性，不能只挑一个最接近文献基准值的区间。</div>"),
    ("alt=\"Disorder mean velocity versus delta f on log log axes\"", "alt=\"无序平均速度随 Δf 的双对数图\""),
    ("<b>Our simulation output。</b> 六个 Δf 点是 8 个独立 quenched realizations 的 arithmetic mean；每个 realization 先自己找 fc。图上只示范最宽和最窄两个 registered window 的 fit：同一批数据的 slope 明显不同。", "<b>本课模拟输出。</b> 六个 Δf 点来自 8 个独立 quenched disorder（淬火无序）样本的算术平均；每个样本都先独立确定自己的 fc。图中只展示预先登记的最宽与最窄两个拟合区间：同一批数据得到的斜率明显不同。"),
    ("<h2>2 · 核心结果：β 没有 plateau</h2>", "<h2>2 · 核心结果：β 没有形成稳定平台</h2>"),
    ("alt=\"Effective beta versus fit window\"", "alt=\"有效 β 随拟合区间上界变化\""),
    ("<b>Our simulation output · central gate。</b> 横轴越往右表示 max Δf 越小、越靠近 sample threshold；β 从 0.268 持续滑到 0.166。虚线 0.245 只作为 Ferrero QEW benchmark，不是拟合目标。", "<b>本课模拟输出 · 核心判据。</b> 横轴越往右表示最大 Δf 越小、越靠近单样本阈值；β 从 0.268 持续滑到 0.166。虚线 0.245 只作为 Ferrero QEW 的文献基准值，不是拟合目标。"),
    ("<div class=\"hold\"><b>WINDOW-STABILITY GATE NOT PASSED。</b> drift=0.102183，远高于预注册 0.030。</div>", "<div class=\"hold\"><b>拟合区间稳定性：未通过。</b> β 漂移为 0.102183，远高于预先登记的 0.030 判据。</div>"),
    ("<h2>3 · 是不是 L07 的 fc 不够准？不是主要问题</h2>", "<h2>3 · 是不是 L07 的 fc 不够准？不是主要问题</h2>"),
    ("alt=\"Beta sensitivity to threshold bracket edge\"", "alt=\"β 对单样本阈值区间边缘的敏感性\""),
    ("<b>Our simulation output。</b> 把每个 sample 的 fc 从 bracket midpoint 推到 low/high edge，all-six β 只变化约 0.001004；这比 0.102 的 window drift 小两个数量级。", "<b>本课模拟输出。</b> 把每个样本的 fc 从阈值区间中点分别移到下沿和上沿，六点拟合的 β 只变化约 0.001004；这比 0.102 的拟合区间漂移小两个数量级。"),
    ("<h2>4 · bootstrap CI 为什么也不能救？</h2>", "<h2>4 · bootstrap（自助法）置信区间为什么也不能救？</h2>"),
    ("alt=\"Bootstrap distribution of beta\"", "alt=\"β 的样本自助法分布\""),
    ("<b>Our simulation output。</b> sample bootstrap 回答“换一批 disorder realization，当前 estimator 会抖多少”；它不回答“是否已经进入 asymptotic critical window”。所以 CI 覆盖 0.245 不能覆盖掉系统性 window drift。", "<b>本课模拟输出。</b> 样本自助法回答的是“重新抽取独立无序样本时，当前 β 估计量会波动多少”；它并不回答“数据是否已经进入渐近临界区间”。因此置信区间覆盖 0.245，并不能抵消系统性的拟合区间漂移。"),
    ("<h2 id=\"result\">5 · 本课结论</h2><div class=\"ok\"><b>Regression pipeline gold test PASS。</b> tilted washboard 的 β=1/2 被同一套 log-fit pipeline 正确恢复。</div><div class=\"hold\"><b>UNIVERSAL BETA CLAIM = NOT AUTHORIZED。</b> 当前 L=32 / periodic-u geometry 只给出 window-dependent effective β。</div>", "<h2 id=\"result\">5 · 本课结论</h2><div class=\"ok\"><b>回归分析已知答案测试：通过。</b> 同一套双对数拟合流程在 tilted washboard（倾斜搓衣板势）模型中正确恢复 β=1/2。</div><div class=\"hold\"><b>普适 β 结论：不授权。</b> 当前 L=32、u 方向周期边界的几何设置只给出随拟合区间变化的有效 β。</div>"),
    (">run receipt</a>", ">运行回执</a>"),
    (">8-realization CSV</a>", ">8 个无序样本 CSV</a>"),
    (">论文截图 receipt</a>", ">论文原图来源回执</a>"),
)


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    before = BeautifulSoup(raw, "html.parser")
    before_hrefs = [x.get("href") for x in before.find_all("a")]
    before_srcs = [x.get("src") for x in before.find_all("img")]
    before_results = {x: raw.count(x) for x in LOCKED_RESULTS}

    out = raw
    for src, dst in REPLACEMENTS:
        if src not in out:
            raise RuntimeError(f"Lab 09 expected source fragment missing: {src}")
        out = out.replace(src, dst, 1)

    after = BeautifulSoup(out, "html.parser")
    if before_hrefs != [x.get("href") for x in after.find_all("a")]:
        raise RuntimeError("Lab 09 href wiring changed")
    if before_srcs != [x.get("src") for x in after.find_all("img")]:
        raise RuntimeError("Lab 09 Figure wiring changed")
    if tuple(x.get("src") for x in after.find_all("img")) != EXPECTED_SRCS:
        raise RuntimeError("Lab 09 expected evidence Figure set changed")
    for token, count in before_results.items():
        if out.count(token) != count:
            raise RuntimeError(f"Lab 09 locked result changed: {token}")

    visible = after.get_text(" ", strip=True)
    required = (
        "mesoscopic corrections（介观修正）",
        "effective exponent（有效指数）",
        "corrections-to-scaling（标度修正）",
        "asymptotic exponent（渐近指数）",
        "crossover（交叉）",
        "quenched disorder（淬火无序）",
        "bootstrap（自助法）",
        "拟合区间稳定性：未通过",
        "普适 β 结论：不授权",
        "0.102183",
        "0.001004",
    )
    for token in required:
        if token not in visible:
            raise RuntimeError(f"Lab 09 required teaching text missing: {token}")
    forbidden = (
        "β window audit", "disorder realizations", "post-hoc tuning", "effective slopes",
        "mean velocity", "β vs window", "authorization gate", "window drift", "panel (a)",
        "power-law guide", "registered window", "sample threshold", "central gate",
        "QEW benchmark", "bracket midpoint", "low/high edge", "all-six", "sample bootstrap",
        "current estimator", "asymptotic critical window", "Our simulation output",
        "Regression pipeline gold test PASS", "UNIVERSAL BETA CLAIM = NOT AUTHORIZED",
        "WINDOW-STABILITY GATE NOT PASSED", "run receipt",
    )
    for token in forbidden:
        if token in visible:
            raise RuntimeError(f"Lab 09 ordinary workflow English remains visible: {token}")

    TARGET.write_text(out, encoding="utf-8")
    print("Lab 09 targeted Language V2 audit complete; beta failure boundary/results/Figure wiring unchanged.")


if __name__ == "__main__":
    main()
