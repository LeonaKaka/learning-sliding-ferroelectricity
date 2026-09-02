from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-08.html"
LOCKED_RESULTS = (
    "3.47%–4.93%",
    "0.0010%",
    "0.5%",
    "0.001387%",
    "dt=.1",
    "dt=.025",
    "dt=.0125",
    "L=32",
)
EXPECTED_SRCS = (
    "../assets/reproduction-lab/source-ferrero2013-review-fig1-full.png",
    "../assets/reproduction-lab/lesson08_vf.png",
    "../assets/reproduction-lab/lesson08_transient_periods.png",
    "../assets/reproduction-lab/lesson08_dt_error.png",
    "../assets/reproduction-lab/lesson08_particle_velocity_gold.png",
)
REPLACEMENTS = (
    ("<title>Reproduction Lab 08 · Steady velocity</title>", "<title>Reproduction Lab（复现实验室）08 · 稳态速度</title>"),
    ("<b>Reproduction Lab <small>· Lesson 08 · Paper2 Method Track</small></b>", "<b>Reproduction Lab（复现实验室） <small>· 第 08 课 · 第二篇工作方法线</small></b>"),
    ("<a href=\"../index.html\">Learning Sliding Ferroelectricity</a> / Reproduction Lab / Lesson 08", "<a href=\"../index.html\">Learning Sliding Ferroelectricity</a> / 复现实验室 / 第 08 课"),
    ("<span class=\"tag\">steady v(f)</span><span class=\"tag\">transient removal</span><span class=\"tag\">dt convergence</span>", "<span class=\"tag\">稳态 v(f)</span><span class=\"tag\">瞬态剔除</span><span class=\"tag\">dt 收敛</span>"),
    ("<p class=\"lead\">L07 只找 threshold。L08 的任务是把 <b>center-of-mass steady velocity v</b> 测准。页面先给论文完整 transport map，再给我们的真实 v(f) 数据；transient 与 dt 检查只是用来回答“这些 v 点能不能信”。</p>", "<p class=\"lead\">L07 只确定了单样本阈值区间。L08 的任务是把 <b>steady velocity（稳态速度）v</b> 测准，这里具体指 center-of-mass velocity（质心速度）。页面先给论文完整的速度–驱动力图，再给我们的真实 v(f) 数据；瞬态剔除与 dt 收敛检查只回答一个问题：这些速度点能不能作为后续临界分析的输入。</p>"),
    ("<div class=\"read-order\"><div><b>1 · 论文 panel b</b><span>velocity–force regime map。</span></div><div><b>2 · 我们的 v(f)</b><span>同样横轴 f、纵轴 steady v。</span></div><div><b>3 · 去 transient</b><span>第 1 个 traversal 不能算 steady。</span></div><div><b>4 · dt 收敛</b><span>production dt 必须过 gate。</span></div></div>", "<div class=\"read-order\"><div><b>1 · 论文子图 b</b><span>先读速度–驱动力上的动力学区间。</span></div><div><b>2 · 我们的 v(f)</b><span>同样以 f 为横轴、稳态 v 为纵轴。</span></div><div><b>3 · 去除瞬态</b><span>第 1 个无序周期不能计入稳态平均。</span></div><div><b>4 · dt 收敛</b><span>正式计算的 dt 必须通过预设判据。</span></div></div>"),
    ("<h2>0 · 论文总图：v–f 上有哪些 regime？</h2>", "<h2>0 · 论文总图：v–f 上有哪些动力学区间？</h2>"),
    ("alt=\"Ferrero 2013 review Figure 1 full\"", "alt=\"Ferrero 2013 综述图 1 完整原图区域\""),
    ("完整保留四个 panels 和原始 caption。本课只读 panel (b)：T=0 depinning、T&gt;0 thermal rounding、creep 与 fast flow 都放在 velocity–force 坐标系。", "完整保留四个子图和论文原始图注。本课只读子图 (b)：T=0 的 depinning（退钉扎）、T&gt;0 的 thermal rounding（热圆整）、creep（蠕变）与 fast flow（快速流动）都被放在速度–驱动力坐标系中。"),
    ("<h2>1 · 我们实际测到的 steady v(f)</h2>", "<h2>1 · 我们实际测到的稳态 v(f)</h2>"),
    ("alt=\"Steady velocity versus force from simulation\"", "alt=\"模拟得到的稳态速度随驱动力变化\""),
    ("<b>Our simulation output。</b> 横轴和论文 panel (b) 一样是 drive f，纵轴一样是 center-of-mass velocity v。四个点全部在 L07 sample threshold 上方；production dt=.025 与更细 reference dt=.0125 几乎重合。", "<b>本课模拟输出。</b> 横轴与论文子图 (b) 一样是驱动力 f，纵轴是质心稳态速度 v。四个点全部位于 L07 的单样本阈值区间上方；正式计算 dt=.025 与更细的参考 dt=.0125 几乎重合。"),
    ("<div class=\"grid3\"><div class=\"card\"><b>同一个 observable</b><p>steady COM velocity v versus drive f。</p></div><div class=\"card\"><b>不同 normalization</b><p>所以不能比较曲线绝对高度或 fc 数值。</p></div><div class=\"card\"><b>L08 不拟 β</b><p>先保证 v estimator 稳定，critical window 留给 L09。</p></div></div>", "<div class=\"grid3\"><div class=\"card\"><b>同一观测量</b><p>质心稳态速度 v 随驱动力 f 的变化。</p></div><div class=\"card\"><b>归一化不同</b><p>所以不能比较曲线绝对高度或 fc 数值。</p></div><div class=\"card\"><b>L08 不拟合 β</b><p>先保证速度估计量稳定，临界拟合区间留给 L09。</p></div></div>"),
    ("<h2>2 · 为什么第一个 traversal 必须丢掉？</h2>", "<h2>2 · 为什么第一个无序周期必须丢掉？</h2>"),
    ("alt=\"Period averaged velocity by traversal\"", "alt=\"逐个无序周期的平均速度\""),
    ("<b>Our simulation output。</b> 每条线对应一个 Δf。第 1 个 disorder-period traversal 从 last-pinned state 解锁，速度系统性偏低；第 2–4 个 traversal 才形成稳定 measurement window。", "<b>本课模拟输出。</b> 每条线对应一个 Δf。第 1 个无序周期从最后钉扎态解锁，速度系统性偏低；第 2–4 个周期才形成稳定的测量区间。"),
    ("第 1 period 相比 steady mean 低约 <b>3.47%–4.93%</b>，而后 3 period 的内部 spread 最大只有 <b>0.0010%</b>。所以“从 t=0 总位移 / 总时间”会把 depinning transient 混进 steady v。", "第 1 个周期相对稳态平均值低约 <b>3.47%–4.93%</b>，而后 3 个周期的内部离散最大只有 <b>0.0010%</b>。所以“从 t=0 起用总位移除以总时间”会把退钉扎瞬态混入稳态速度。"),
    ("<h2>3 · dt convergence 是实际数据，不是口头保证</h2>", "<h2>3 · dt 收敛是实际数据，不是口头保证</h2>"),
    ("alt=\"Velocity relative error versus time step\"", "alt=\"速度相对误差随积分步长变化\""),
    ("<b>Our simulation output。</b> y 轴是相对 dt=.0125 reference 的真实 velocity error。注册 gate 是 0.5%；dt=.1 失败，dt=.025 通过，因此 production 选择 .025，而不是事后放宽 gate。", "<b>本课模拟输出。</b> y 轴是相对 dt=.0125 参考值的真实速度误差。预先登记的判据是 0.5%；dt=.1 未通过，dt=.025 通过，因此正式计算选择 .025，而不是事后放宽判据。"),
    ("alt=\"Analytic velocity estimator gold test\"", "alt=\"速度估计量的解析已知答案测试\""),
    ("<b>Code gold test。</b> 在 tilted washboard moving regime，numerical mean velocity 与解析 √(f²−1) 重合，最大 relative error 0.001387%。", "<b>代码已知答案测试。</b> 在 tilted washboard（倾斜搓衣板势）的运动态中，数值平均速度与解析结果 √(f²−1) 重合，最大相对误差为 0.001387%。"),
    ("<h2 id=\"result\">4 · 本课结论</h2><div class=\"ok\"><b>STEADY VELOCITY ESTIMATOR + DT CONVERGENCE PASS。</b> 可以把这些 v(f) measurement 交给下一课做 critical-window audit。</div><div class=\"warn\"><b>NO BETA FIT IN LESSON 08。</b> 单 sample、L=32、四个 Δf 点只够验证 estimator，不够证明 critical scaling。</div>", "<h2 id=\"result\">4 · 本课结论</h2><div class=\"ok\"><b>稳态速度估计量 + dt 收敛：通过。</b> 可以把这些 v(f) 测量交给下一课做临界拟合区间审计。</div><div class=\"warn\"><b>本课不拟合 β。</b> 单个样本、L=32、四个 Δf 点只够验证速度估计量，不足以证明临界标度。</div>"),
    (">run receipt</a>", ">运行回执</a>"),
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
            raise RuntimeError(f"Lab 08 expected source fragment missing: {src}")
        out = out.replace(src, dst, 1)

    after = BeautifulSoup(out, "html.parser")
    if before_hrefs != [x.get("href") for x in after.find_all("a")]:
        raise RuntimeError("Lab 08 href wiring changed")
    if before_srcs != [x.get("src") for x in after.find_all("img")]:
        raise RuntimeError("Lab 08 Figure wiring changed")
    if tuple(x.get("src") for x in after.find_all("img")) != EXPECTED_SRCS:
        raise RuntimeError("Lab 08 expected evidence Figure set changed")
    for token, count in before_results.items():
        if out.count(token) != count:
            raise RuntimeError(f"Lab 08 locked result changed: {token}")

    visible = after.get_text(" ", strip=True)
    required = (
        "steady velocity（稳态速度）",
        "center-of-mass velocity（质心速度）",
        "depinning（退钉扎）",
        "thermal rounding（热圆整）",
        "creep（蠕变）",
        "fast flow（快速流动）",
        "稳态速度估计量 + dt 收敛：通过",
        "本课不拟合 β",
        "3.47%–4.93%",
        "0.0010%",
        "0.001387%",
    )
    for token in required:
        if token not in visible:
            raise RuntimeError(f"Lab 08 required teaching text missing: {token}")
    forbidden = (
        "transient removal", "dt convergence", "production dt", "reference dt",
        "measurement window", "run receipt", "Our simulation output", "Code gold test",
        "sample threshold", "critical-window audit", "velocity error", "normalization",
        "observable", "NO BETA FIT IN LESSON 08", "STEADY VELOCITY ESTIMATOR + DT CONVERGENCE PASS",
    )
    for token in forbidden:
        if token in visible:
            raise RuntimeError(f"Lab 08 ordinary workflow English remains visible: {token}")

    TARGET.write_text(out, encoding="utf-8")
    print("Lab 08 targeted Language V2 audit complete; science/results/Figure wiring unchanged.")


if __name__ == "__main__":
    main()
