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
    ("我们这里只借用 panel (a) 的物理判据", "我们这里只借用子图 (a) 的物理判据"),
    ("但“钉扎态 ↔ 运动态”的物理分界指向同一个退钉扎问题。", "但“钉扎态 ↔ 运动态”的物理分界指向同一个 depinning（退钉扎）问题。"),
    ("quenched landscape（淬火无序势景观）", "quenched disorder landscape（淬火无序势景观）"),
    ("<td>L=32, seed=20260902</td>", "<td>L=32，随机种子=20260902</td>"),
    ("这不是 Ferrero 的 exact metastable-state algorithm（精确亚稳态算法）", "这不是 Ferrero 的精确亚稳态算法"),
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
            raise RuntimeError(f"Lab 07 expected source fragment missing: {src}")
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
    required = (
        "quenched disorder（淬火无序）",
        "thermodynamic critical force（热力学临界力）",
        "depinning（退钉扎）",
        "quenched disorder landscape（淬火无序势景观）",
        "elastic line（弹性界面）",
        "tilted washboard（倾斜搓衣板势）",
        "这里没有得到热力学极限",
        "阈值已知答案测试 + 小尺寸界面阈值区间：通过",
    )
    for token in required:
        if token not in visible:
            raise RuntimeError(f"Lab 07 required teaching text missing: {token}")
    forbidden = (
        "panel (a)", "seed=20260902", "exact metastable-state algorithm",
        "threshold classifier", "sample-specific threshold", "last pinned", "first moving",
        "run receipt", "Code gold test", "Our simulation output",
    )
    for token in forbidden:
        if token in visible:
            raise RuntimeError(f"Lab 07 ordinary workflow English remains visible: {token}")

    TARGET.write_text(out, encoding="utf-8")
    print("Lab 07 targeted Language V2 audit complete; science/results/Figure wiring unchanged.")


if __name__ == "__main__":
    main()
