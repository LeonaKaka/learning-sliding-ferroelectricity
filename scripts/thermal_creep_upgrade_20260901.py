from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"anchor count {n} in {path}: {old[:100]}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")


def build_ferrero_figure() -> None:
    from PIL import Image
    out = ROOT / "assets/pinning-creep/ferrero2021-fig3-finite-temperature.webp"
    out.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as td:
        td = Path(td)
        pdf = td / "ferrero.pdf"
        prefix = td / "page8"
        run([
            "curl", "-L", "--fail", "--retry", "3", "-A", "Mozilla/5.0",
            "https://arxiv.org/pdf/2001.11464", "-o", str(pdf)
        ], check=True)
        if not pdf.read_bytes().startswith(b"%PDF"):
            raise RuntimeError("Ferrero download is not a PDF")
        run(["pdftoppm", "-f", "8", "-l", "8", "-r", "360", "-png", "-singlefile", str(pdf), str(prefix)], check=True)
        im = Image.open(str(prefix) + ".png").convert("RGB")
        # Figure 3 sits at the top of preprint page 8. Keep the two panels + original caption.
        crop = im.crop((int(im.width*0.05), int(im.height*0.02), int(im.width*0.95), int(im.height*0.43)))
        if crop.width < 1800 or crop.height < 900:
            raise RuntimeError(f"unexpected Ferrero crop size {crop.size}")
        crop.save(out, format="WEBP", lossless=True, method=6)


def patch_m04() -> None:
    anchor = '<div class="q">本章最小判断框架：<b>速度高度非线性 → 问是否 creep；形貌“不直” → 定义 u(z)、测 B(L) 与 ζ；局域停滞 → 找 pinning landscape；看到一次“de-pinning” → 先别把它升级成 critical depinning。</b></div>'
    addition = '''<h2 id="finite-temperature">Research recipe · finite-T creep 不是“给 T=0 方程加噪声”就结束</h2>
<p>Ferrero 等 2021 的综述把最关键的逻辑写得很清楚：<b>T=0 时 f&lt;f<sub>c</sub> 没有稳态前进；T&gt;0 后热激活可以跨过 metastable barriers，于是阈值以下出现有限平均速度。</b> 但这不意味着所有 f&lt;f<sub>c</sub> 的有限速度都可以马上塞进一条 creep 直线。</p>
<div class="src"><div class="head"><b>原文 · Ferrero et al. 2021</b>　<span class="rule">Annual Review of Condensed Matter Physics 12, 111–134 · 项目 Drive PDF</span></div><blockquote class="source-text"><p>At finite temperature, the interface has a finite steady velocity v, even below f<sub>c</sub>.</p></blockquote><div class="note">同一节还明确区分两类随机性：thermal-noise average 是在<b>固定 quenched disorder landscape</b> 上重复；这对数值统计非常重要。</div></div>
<figure class="fig"><a href="../assets/pinning-creep/ferrero2021-fig3-finite-temperature.webp" target="_blank" rel="noopener"><img src="../assets/pinning-creep/ferrero2021-fig3-finite-temperature.webp" alt="Ferrero 2021 Figure 3 finite-temperature velocity-force characteristic and creep law"></a><figcaption class="cap"><b>Ferrero 2021 Fig. 3 · finite-T v–f 不是一条单一幂律。</b><span class="zoom">项目 PDF 同版本 arXiv 原 Figure</span><br>左图把 T=0 depinning 与 T&gt;0 creep 放在同一条 velocity–force characteristic；右图回顾 Lemerle 的经典低场 creep 线性化。真正适合拟合 μ 的是<b>低场、低温、可测的 activated window</b>，不是所有 f&lt;f<sub>c</sub> 点。</figcaption></figure>
<div style="font-family:Georgia,'Times New Roman',serif;font-size:18px;text-align:center;padding:15px;margin:20px 0;background:#faf7f0;border:1px solid var(--l);border-radius:10px">γ∂<sub>t</sub>u = c∇²u + f + F<sub>p</sub>(x,u) + η(x,t)<br><small style="font:12px/1.5 system-ui;color:var(--m)">quenched landscape F<sub>p</sub> 固定；η 是 thermal noise。两者不是同一种“seed”。</small></div>
<div class="readgrid"><div class="readbox"><b>Outer block · disorder seed</b><p>定义不同 quenched landscapes。要把结论推广到“disorder realizations”时，统计独立性首先来自这一层。</p></div><div class="readbox"><b>Inner repeat · thermal seed</b><p>同一个 quenched landscape 上的重复 stochastic trajectories，用来估计 conditional thermal average / variance。</p></div><div class="readbox"><b>不是 sample · frames</b><p>同一 trajectory 的时间帧、wall points、waiting-time bins 不是新的 quenched samples，不能把 n 人为放大。</p></div></div>
<div class="warn"><b>层级统计：</b>如果一个 disorder realization 跑了 6 个 thermal seeds，它不是“6 个独立 disorder samples”。最自然的汇总是先在同一 disorder 内处理 thermal repeats，再以 disorder realization 为外层 block 做 uncertainty；或者使用明确的 hierarchical model / block bootstrap。</div>

<h3>什么时候才值得拟合 creep exponent μ？</h3>
<div class="genealogy">
<div class="gene"><b>① 先有 T=0 基线</b><p>先独立确定同一 wall problem 的 T=0 threshold scale；不要用 finite-T creep 数据反推一个最方便的 f<sub>c</sub>。</p></div>
<div class="gene"><b>② 找“可测窗口”</b><p>先从接近阈值但仍 subcritical 的场找得到稳定 drift 的区域，再向低场扩。若绝大多数 run 只给 zero-displacement / velocity upper bound，继续向更低场烧时间通常只增加 censoring。</p></div>
<div class="gene"><b>③ 去掉 transient</b><p>初始 wall relaxation、短时局域抖动和真正长期 forward drift 必须分开。平均速度要来自稳定 observation window，而不是启动后的第一段位移。</p></div>
<div class="gene"><b>④ 检查 switching object</b><p>若升温后 bulk nucleation、bubble、multiple walls 大量出现，那么你测到的是 finite-T switching kinetics，不再是干净的 isolated-wall creep。</p></div>
<div class="gene"><b>⑤ 只在 deep-creep window 拟合</b><p>经典 stretched-exponential creep law 是低 drive 的渐近描述。靠近 f<sub>c</sub> 会进入 crossover / thermal-rounding physics，不能把整个 subcritical 区域强行用一个 μ 吃掉。</p></div>
</div>
<div class="bridge"><b>所以 creep 的负结果也有信息。</b> 如果可测窗口里始终被 nucleation、topology change、非稳态 waiting-time 或强 cutoff dependence 控制，正确结论是“没有建立 clean creep regime”，而不是继续延长拟合区间直到出现一条直线。</div>

'''
    replace_once("modules/pinning-creep.html", anchor, addition + anchor)


def patch_m05() -> None:
    anchor = '<div class="bridge">到这里，问题已经从“墙会不会动”变成“哪一种无序与哪一种有效界面理论控制它怎么动”。下一章必须把 disorder 本身拆开：random-bond、random-field 与 RFIM 到底各自意味着什么。</div>'
    addition = '''<h2 id="thermal-rounding">6 · Thermal rounding：T&gt;0 把 sharp depinning 圆滑掉，ψ 该怎么测？</h2>
<p>有限温度下，f&lt;f<sub>c</sub> 已经有 thermal activation，因此严格的 pinned/moving 非解析点被圆滑。Bustingorry、Kolton 与 Giamarchi 对一维 elastic string 的数值研究使用一个新的 thermal-rounding exponent ψ：在<b>独立知道的 sample critical force</b> 上测试</p>
<div class="eq" style="text-align:center;padding:14px;background:#faf7f0;border:1px solid var(--l);border-radius:10px">v(f<sub>c</sub>,T) ∼ T<sup>ψ</sup></div>
<p>并进一步用联合 scaling function 检查 field 与 temperature 是否由同一临界结构控制：</p>
<div class="eq" style="text-align:center;padding:14px;background:#faf7f0;border:1px solid var(--l);border-radius:10px">v(f,T) = T<sup>ψ</sup> G[(f−f<sub>c</sub>) T<sup>−ψ/β</sup>]</div>
<div class="src"><div class="head"><b>方法锚点 · Bustingorry, Kolton & Giamarchi 2012</b>　<span class="rule">Phys. Rev. E 85, 021144 · APS official record</span></div><div class="note">作者在特定的 1D elastic-string / uncorrelated-disorder 模型中得到 ψ≈0.15，并用 steady-state structure factor、transient dynamics 与 joint velocity scaling function 交叉检查。<b>这个数值不是 sliding FE 的先验目标。</b></div></div>
<div class="claims"><div class="claim"><h3>为什么“先知道 f<sub>c</sub>”很关键</h3><p>finite-T 曲线本来就被 rounding；如果同时用这批数据自由调 f<sub>c</sub> 和 ψ，很容易把 crossover 调成漂亮 power law。T=0 threshold 应先独立闭合。</p></div><div class="claim"><h3>sample-specific f<sub>c</sub> 什么时候合理</h3><p>有限随机样本确实有自己的 f<sub>c</sub><sup>(i)</sup>。理论工作可以在每个样本独立测得的 T=0 f<sub>c</sub><sup>(i)</sup> 上评估 thermal rounding，以去掉 threshold-distribution broadening；但不能从同一批 finite-T velocity data 事后给每个 seed 找最有利的 f<sub>c</sub><sup>(i)</sup>。</p></div></div>
<div class="warn"><b>不要把 ψ 当成必然存在的纯幂律。</b> 对某些 activated dynamics，near-threshold scaling 会出现非标准行为或 logarithmic corrections；Purrello et al. 2017 甚至显示标准 thermal-rounding scaling 在 Arrhenius activation 的一个 qEW-class 模型里可以失效。对 sliding FE，collapse 应该是待检验结果，不是数据预处理步骤。</div>

<h3>一套最小但严谨的 finite-T 测量顺序</h3>
<div class="checks"><div class="check"><b>A · freeze T=0 authority</b><p>固定 geometry、disorder definition、L、dx 与独立 threshold protocol；先有 f<sub>c</sub> / f<sub>c</sub><sup>(i)</sup>。</p></div><div class="check"><b>B · 小 thermal pilot</b><p>先用少数 T 和 f/f<sub>c</sub> 检查 stochastic integrator、velocity floor、所需 observation time、wall topology。</p></div><div class="check"><b>C · 分层重复</b><p>同一 disorder realization 下跑多个 thermal seeds；uncertainty 不把这些 inner repeats 冒充新的 quenched samples。</p></div><div class="check"><b>D · 分开两个问题</b><p>deep subcritical window 测 creep；f≈f<sub>c</sub> 测 rounding。不要用一套拟合函数覆盖两个 regime。</p></div><div class="check"><b>E · 先 v，再 geometry</b><p>若 velocity scaling 有候选，再检查 finite-T structure factor / roughness crossover 是否给出相容的 characteristic length。</p></div><div class="check"><b>F · failure 也要保留</b><p>若 finite T 触发 nucleation、multiple walls 或 scaling 对窗口极敏感，记录为 mapping breakdown / crossover，而不是删掉“不漂亮”的 runs。</p></div></div>
<div class="bridge"><a href="pinning-creep.html#finite-temperature">回到 Module 04 的 finite-T creep recipe</a>：那里负责 f&lt;f<sub>c</sub> 的 activated window；这里负责 f≈f<sub>c</sub> 的 thermal rounding。两者相邻，但不是同一个 fit。</div>

'''
    replace_once("modules/depinning.html", anchor, addition + anchor)


def patch_research_track() -> None:
    anchor = '<h2 id="model">3 · 从 stacking registry 到一个可控的 sliding-FE effective model</h2>'
    addition = '''<h2 id="temperature">2.5 · Temperature 是新的实验轴，不是把 random seed 多跑几次</h2>
<p>当 isolated-wall T=0 protocol 稳定以后，有限温度自然分成两个不同的问题：</p>
<div class="twocol"><div class="card"><b>Deep subcritical · creep</b><p>f&lt;f<sub>c</sub> 且离阈值足够远：问 thermally activated barriers 是否产生可测的长期 drift，是否存在稳定 creep window 与 μ candidate。</p></div><div class="card"><b>Near threshold · thermal rounding</b><p>f≈f<sub>c</sub>：问 T=0 singularity 怎样被温度圆滑，是否存在 v(f<sub>c</sub>,T)∼T<sup>ψ</sup> 与 joint field–temperature scaling。</p></div></div>
<table class="matrix"><thead><tr><th>层次</th><th>应该固定什么</th><th>重复什么</th><th>独立统计单元</th></tr></thead><tbody><tr><td>quenched disorder</td><td>一个 landscape h(r)/δV(r)</td><td>换 disorder seed</td><td>用于 disorder population inference 的 outer block</td></tr><tr><td>thermal noise</td><td>同一个 quenched landscape</td><td>换 Langevin/noise seed</td><td>同一 landscape 内的 conditional repeat</td></tr><tr><td>trajectory frames</td><td>同一次 run</td><td>随时间采样</td><td>不是新的 disorder sample</td></tr></tbody></table>
<div class="warn"><b>最重要的 anti-overfit rule：</b>thermal rounding 必须继承独立 T=0 threshold。若允许每个 disorder seed 在同一批 finite-T 数据里自由移动自己的 f<sub>c</sub>，再去优化 ψ / collapse，就可能人为抹掉 sample-to-sample threshold variation。</div>
<div class="bridge"><a href="pinning-creep.html#finite-temperature">Module 04：怎么找可测 creep window</a>　·　<a href="depinning.html#thermal-rounding">Module 05：怎么测 thermal rounding / ψ</a></div>

'''
    replace_once("modules/research-track.html", anchor, addition + anchor)


if __name__ == "__main__":
    build_ferrero_figure()
    patch_m04()
    patch_m05()
    patch_research_track()
    print("thermal/creep content upgrade applied")
