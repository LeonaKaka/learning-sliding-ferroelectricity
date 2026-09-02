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
    ("<tr><th>max Δf</th><th>β<sub>eff</sub></th></tr>", "<tr><th>最大 Δf</th><th>有效 β</th></tr>"),
    ("<h2>4 · bootstrap（自助法）置信区间为什么也不能救？</h2>", "<h2>4 · 自助法置信区间为什么也不能救？</h2>"),
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
            raise RuntimeError(f"Lab 09 expected cleanup fragment missing: {src}")
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
        "最大 Δf",
        "有效 β",
        "自助法置信区间为什么也不能救",
        "拟合区间稳定性：未通过",
        "普适 β 结论：不授权",
        "0.102183",
        "0.001004",
    )
    for token in required:
        if token not in visible:
            raise RuntimeError(f"Lab 09 required Language V2 text missing: {token}")
    forbidden = (
        "max Δf", "βeff", "β_eff", "4 · bootstrap（自助法）",
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
    print("Lab 09 second Language V2 audit complete; beta failure boundary/results/Figure wiring unchanged.")


if __name__ == "__main__":
    main()
