from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-07.html"
LOCKED_RESULTS = (
    "[0.777636719, 0.777783203]",
    "1.465×10<sup>−4</sup>",
    "f<sub>c</sub> = 1",
    "0.7777",
    "1.916",
)
EXPECTED_SRCS = (
    "../assets/reproduction-lab/source-ferrero2013-pre-fig3-full.png",
    "../assets/reproduction-lab/lesson07_bisection.png",
    "../assets/reproduction-lab/lesson07_last_pinned_profile.png",
    "../assets/reproduction-lab/lesson07_particle_gold.png",
    "../assets/reproduction-lab/lesson07_dt_threshold.png",
)

REPLACEMENTS = (
    ("<title>Reproduction Lab 07 · Threshold search</title>",
     "<title>Reproduction Lab（复现实验室）07 · 退钉扎阈值搜索</title>"),
    ("<header class=\"top\"><div class=\"bar\"><b>Reproduction Lab <small>· Lesson 07 · Paper2 Method Track</small></b><span><a href=\"reproduction-lab-06.html\">上一课</a> · <a href=\"../index.html\">首页</a> · <a href=\"#result\">结论</a></span></div></header>",
     "<header class=\"top\"><div class=\"bar\"><b>Reproduction Lab（复现实验室） <small>· 第 07 课 · 第二篇工作方法线</small></b><span><a href=\"reproduction-lab-06.html\">上一课</a> · <a href=\"../index.html\">首页</a> · <a href=\"#result\">结论</a></span></div></header>"),
    ("<div class=\"crumb\"><a href=\"../index.html\">Learning Sliding Ferroelectricity</a> / Reproduction Lab / Lesson 07</div><div><span class=\"tag\">T=0</span><span class=\"tag\">threshold classifier</span><span class=\"tag\">真实 code plot</span></div>",
     "<div class=\"crumb\"><a href=\"../index.html\">Learning Sliding Ferroelectricity</a> / 复现实验室 / 第 07 课</div><div><span class=\"tag\">T=0</span><span class=\"tag\">阈值分类判据</span><span class=\"tag\">真实代码图</span></div>"),
    ("<h1>先判断 pinned 还是 moving，再二分 f<sub>c</sub></h1>",
     "<h1>先判断钉扎态还是运动态，再二分搜索 f<sub>c</sub></h1>"),
    ("<p class=\"lead\">L07 不再用“critical structure + finite-size threshold”两张无关图凑在一起。这里只回答一个问题：<b>固定 disorder sample、固定 drive 后，长时间是停住还是持续运动？</b> 把这个二分类做稳，才能谈 sample-specific threshold bracket。</p>",
     "<p class=\"lead\">L07 不再用两张无关的临界结构与有限尺寸阈值图拼出一个结论。这里只回答一个问题：<b>固定 quenched disorder（淬火无序）样本、固定驱动力后，长时间究竟停住还是持续运动？</b> 先把这个二分类做稳，才有资格讨论单样本阈值区间。</p>"),
    ("<div class=\"read-order\"><div><b>1 · 论文原图</b><span>Fig.3 展示 threshold 两侧 v(t) 的不同命运。</span></div><div><b>2 · 我们的算法</b><span>last pinned / first moving 两侧做二分。</span></div><div><b>3 · 数值稳定性</b><span>dt 降低后 bracket 不移动。</span></div><div><b>4 · 权限边界</b><span>这里只得到 finite-sample bracket。</span></div></div>",
     "<div class=\"read-order\"><div><b>1 · 论文原图</b><span>Fig.3 展示阈值两侧 v(t) 的长期命运如何分开。</span></div><div><b>2 · 我们的算法</b><span>在最后一个钉扎点与第一个运动点之间做二分搜索。</span></div><div><b>3 · 数值稳定性</b><span>减小 dt 后，阈值区间不应漂移。</span></div><div><b>4 · 结论边界</b><span>这里只得到有限样本的阈值区间。</span></div></div>"),
    ("<h2>0 · 论文原图：阈值两侧真正不同的是 long-time fate</h2>",
     "<h2>0 · 论文原图：阈值两侧真正不同的是长期命运</h2>"),
    ("<figure class=\"figure source\"><img src=\"../assets/reproduction-lab/source-ferrero2013-pre-fig3-full.png\" alt=\"Ferrero PRE 2013 Figure 3 full crop\"><figcaption class=\"caption\"><b>Ferrero, Bustingorry & Kolton, PRE 87, 032122 (2013), Fig.3。</b> 完整保留 (a) raw v(t)、(b) rescaled data、legend 和原始 caption。我们这里只借用 panel (a) 的物理判据：f&lt;f<sub>c</sub> 的曲线最终 blocked、v→0；f&gt;f<sub>c</sub> 的曲线长时间趋向 finite velocity。</figcaption></figure>",
     "<figure class=\"figure source\"><img src=\"../assets/reproduction-lab/source-ferrero2013-pre-fig3-full.png\" alt=\"Ferrero PRE 2013 图 3 完整原图区域\"><figcaption class=\"caption\"><b>Ferrero, Bustingorry & Kolton, PRE 87, 032122 (2013), Fig.3。</b> 完整保留 (a) 原始 v(t)、(b) 重标度数据、图例和论文原始图注。我们这里只借用 panel (a) 的物理判据：f&lt;f<sub>c</sub> 时曲线最终被钉住、v→0；f&gt;f<sub>c</sub> 时长时间速度趋向有限值。</figcaption></figure>"),
    ("<div class=\"bridge\"><b>注意：</b>Ferrero 用的是 thermodynamic critical force 附近的 disorder-averaged non-steady relaxation；我们用 direct relaxation 去分类一个有限 periodic disorder sample。两者不是同一个算法，但“pinned ↔ moving”的物理分界是同一件事。</div>",
     "<div class=\"bridge\"><b>注意：</b>Ferrero 研究的是 thermodynamic critical force（热力学临界力）附近的无序平均非稳态弛豫；我们则用直接弛豫去分类一个有限、周期性无序样本。两者不是同一个数值算法，但“钉扎态 ↔ 运动态”的物理分界指向同一个退钉扎问题。</div>"),
    ("<h2>1 · 我们如何把它变成 bracket？</h2>",
     "<h2>1 · 我们如何把它变成阈值区间？</h2>"),
    ("<figure class=\"figure\"><img src=\"../assets/reproduction-lab/lesson07_bisection.png\" alt=\"Threshold bisection history\"><figcaption class=\"caption\"><b>Our simulation output。</b> 每一步都保留两个有证据的端点：last pinned f<sub>−</sub> 和 first moving f<sub>+</sub>。灰带不是画出来的“误差条”，而是二分尚未消除的 threshold bracket。</figcaption></figure>",
     "<figure class=\"figure\"><img src=\"../assets/reproduction-lab/lesson07_bisection.png\" alt=\"单个无序样本的阈值二分历史\"><figcaption class=\"caption\"><b>本课模拟输出。</b> 每一步都保留两个有动力学证据的端点：最后一个钉扎点 f<sub>−</sub> 与第一个运动点 f<sub>+</sub>。灰带不是人为添加的“误差条”，而是二分搜索尚未消除的阈值区间。</figcaption></figure>"),
    ("<figure class=\"figure\"><img src=\"../assets/reproduction-lab/lesson07_last_pinned_profile.png\" alt=\"Last pinned QEW profile\"><figcaption class=\"caption\"><b>Our simulation output。</b> 这是最终 bracket 下沿的 last-pinned wall profile。它说明 classifier 面对的不是一个单自由度，而是一条在 quenched landscape 中变形的 elastic line。</figcaption></figure>",
     "<figure class=\"figure\"><img src=\"../assets/reproduction-lab/lesson07_last_pinned_profile.png\" alt=\"最终阈值区间下沿的 QEW 钉扎畴壁剖面\"><figcaption class=\"caption\"><b>本课模拟输出。</b> 这是最终阈值区间下沿的最后一个钉扎畴壁剖面。分类判据面对的不是单自由度粒子，而是一条会在 quenched landscape（淬火无序势景观）中变形的 elastic line（弹性界面）。</figcaption></figure>"),
    ("<table class=\"table\"><thead><tr><th>sample</th><th>final bracket</th><th>width</th></tr></thead><tbody><tr><td>L=32, seed=20260902</td><td>[0.777636719, 0.777783203]</td><td>1.465×10<sup>−4</sup></td></tr></tbody></table>",
     "<table class=\"table\"><thead><tr><th>样本</th><th>最终阈值区间</th><th>区间宽度</th></tr></thead><tbody><tr><td>L=32, seed=20260902</td><td>[0.777636719, 0.777783203]</td><td>1.465×10<sup>−4</sup></td></tr></tbody></table>"),
    ("<h2>2 · 先在答案已知的问题上验 classifier</h2>",
     "<h2>2 · 先在答案已知的问题上验证分类判据</h2>"),
    ("<figure class=\"figure medium\"><img src=\"../assets/reproduction-lab/lesson07_particle_gold.png\" alt=\"Analytic threshold gold test\"><figcaption class=\"caption\"><b>Code gold test。</b> 同一套二分逻辑在 tilted washboard 上恢复 exact f<sub>c</sub>=1；不同 dt 的 bracket 都落在解析答案上。</figcaption></figure>",
     "<figure class=\"figure medium\"><img src=\"../assets/reproduction-lab/lesson07_particle_gold.png\" alt=\"解析阈值已知答案测试\"><figcaption class=\"caption\"><b>代码已知答案测试。</b> 同一套二分逻辑在 tilted washboard（倾斜搓衣板势）上恢复解析值 f<sub>c</sub>=1；不同 dt 得到的阈值区间都覆盖解析答案。</figcaption></figure>"),
    ("<h2>3 · 再看 dt：不是积分步长制造出来的 threshold</h2>",
     "<h2>3 · 再看 dt：确认阈值不是积分步长制造出来的</h2>"),
    ("<figure class=\"figure medium\"><img src=\"../assets/reproduction-lab/lesson07_dt_threshold.png\" alt=\"Threshold bracket versus time step\"><figcaption class=\"caption\"><b>Our simulation output。</b> dt=0.10、0.05、0.025 的 midpoint 在打印精度内不变，error bar 是各自 bracket 的 half-width。</figcaption></figure>",
     "<figure class=\"figure medium\"><img src=\"../assets/reproduction-lab/lesson07_dt_threshold.png\" alt=\"阈值区间随积分步长的稳定性\"><figcaption class=\"caption\"><b>本课模拟输出。</b> dt=0.10、0.05、0.025 的区间中点在打印精度内完全不变；误差棒表示各自阈值区间的半宽。</figcaption></figure>"),
    ("<div class=\"ok\"><b>THRESHOLD GOLD TEST + SMALL-LINE BRACKET PASS。</b> threshold classifier 和 bisection contract 可以交给 L08 使用。</div>",
     "<div class=\"ok\"><b>阈值已知答案测试 + 小尺寸界面阈值区间：通过。</b> 阈值分类判据与二分搜索流程已经具备交给 L08 使用的数值资格。</div>"),
    ("<div class=\"warn\"><b>没有证明：</b>这不是 Ferrero exact metastable-state algorithm；没有 thermodynamic f<sub>c</sub>；0.7777 也不能和论文约 1.916 或材料电场阈值比较绝对数值。</div>",
     "<div class=\"warn\"><b>没有证明：</b>这不是 Ferrero 的 exact metastable-state algorithm（精确亚稳态算法）；这里没有得到热力学极限 f<sub>c</sub>。因此 0.7777 不能与论文约 1.916 或真实材料的电场阈值直接比较绝对数值。</div>"),
    ("<h2>5 · 可复查</h2><div class=\"code-links\"><a href=\"../examples/reproduction-lab/lesson07_threshold_search.py\">Python 脚本</a><a href=\"../assets/reproduction-lab/lesson07_threshold_search.txt\">run receipt</a><a href=\"../assets/reproduction-lab/source-figure-receipt.json\">论文截图 receipt</a></div>",
     "<h2>5 · 可复查</h2><div class=\"code-links\"><a href=\"../examples/reproduction-lab/lesson07_threshold_search.py\">Python 脚本</a><a href=\"../assets/reproduction-lab/lesson07_threshold_search.txt\">运行回执</a><a href=\"../assets/reproduction-lab/source-figure-receipt.json\">论文原图来源回执</a></div>"),
)


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    before = BeautifulSoup(raw, "html.parser")
    before_eq = [x.decode_contents() for x in before.select(".eq")]
    before_hrefs = [x.get("href") for x in before.find_all("a")]
    before_srcs = [x.get("src") for x in before.find_all("img")]
    before_results = {x: raw.count(x) for x in LOCKED_RESULTS}

    out = raw
    for src, dst in REPLACEMENTS:
        if src not in out:
            raise RuntimeError(f"Lab 07 expected source fragment missing: {src[:80]}")
        out = out.replace(src, dst, 1)

    after = BeautifulSoup(out, "html.parser")
    if before_eq != [x.decode_contents() for x in after.select(".eq")]:
        raise RuntimeError("Lab 07 equation changed")
    if before_hrefs != [x.get("href") for x in after.find_all("a")]:
        raise RuntimeError("Lab 07 href wiring changed")
    if before_srcs != [x.get("src") for x in after.find_all("img")]:
        raise RuntimeError("Lab 07 Figure wiring changed")
    if tuple(x.get("src") for x in after.find_all("img")) != EXPECTED_SRCS:
        raise RuntimeError("Lab 07 expected evidence Figure set changed")
    for token, count in before_results.items():
        if out.count(token) != count:
            raise RuntimeError(f"Lab 07 locked result changed: {token}")
    visible = after.get_text(" ", strip=True)
    if "这里没有得到热力学极限" not in visible:
        raise RuntimeError("Lab 07 thermodynamic-fc claim boundary missing")
    if "阈值已知答案测试 + 小尺寸界面阈值区间：通过" not in visible:
        raise RuntimeError("Lab 07 finite-sample pass statement missing")

    TARGET.write_text(out, encoding="utf-8")
    print("Lab 07 Language V2 first pass complete; equation/results/Figure wiring unchanged.")


if __name__ == "__main__":
    main()
