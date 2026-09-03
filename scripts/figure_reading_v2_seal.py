from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "modules"

EXPECTED = {
    "foundations.html": {
        "Wu & Li Fig.1": "wu2021-fig1-mechanism-display.webp",
        "Vizner Stern Fig.2": "vizner2021-fig2-domains-display.webp",
        "Meng Fig.3e": "meng2022-fig3e-multistate-display.webp",
    },
    "switching-pathways.html": {
        "Yang Fig.3": "yang2024-fig3-domain-wall-release.png",
        "Sui Fig.4": "sui2024-fig4-atomic-sliding-pathways-display.webp",
        "Liang Fig.4": "liang2025-fig4-interface-resolved-pathways.png",
    },
    "domain-walls.html": {
        "Ke Fig.1": "ke2025-fig1-bec-force.webp",
        "Chen Fig.2": "chen2026-fig2-pinning.webp",
        "Liu Fig.2": "liu2026-fig2-raman-switching.webp",
    },
    "pinning-creep.html": {
        "Tybell Fig.3": "tybell2002-fig3-creep.png",
        "Paruch Fig.3": "paruch2005-fig3-roughness.png",
        "Kim Fig.1": "kim2014-fig1-pinning-display.webp",
    },
    "depinning.html": {
        "Rosso Fig.2": "rosso2003-fig2-critical-roughness.png",
        "Ferrero Fig.3": "ferrero2013-fig3-nonsteady-velocity.png",
        "Wiese Fig.22": "wiese2022-fig22-depinning-phenomenology.png",
    },
    "disorder-rfim.html": {
        "Drossel Fig.3(a)": "drossel1998-fig3a-percolative-wall.png",
        "Zhou Fig.2": "zhou2012-fig2-anomalous-roughness.png",
        "Paul Fig.4": "paul2026-fig4-multidomain-disorder.webp",
    },
}

NEW_BOUNDARY_MARKERS = {
    "foundations.html": (
        "低单胞能垒不能证明真实器件会整层同步相干滑移",
        "KPFM 直接测的是表面电势，不是极化矢量本身",
        "不是原子级动力学录像，也不能单独证明唯一微观路径",
    ),
    "switching-pathways.html": (
        "不能把这里的 E_c 自动当作热力学 f_c",
        "电子束诱导场条件和 InSe:Y 的能垒也不能直接搬到普通 3R-MoS₂ 器件",
        "不能把这套释放顺序当成所有多层滑移铁电的固定路径",
    ),
    "domain-walls.html": (
        "不是退钉扎普适性的证据",
        "不等于建立热力学 critical depinning",
        "这些表观阈值不是自动唯一的本征材料常数",
    ),
}


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise RuntimeError(msg)


def main() -> None:
    total = 0
    for filename, expected in EXPECTED.items():
        page = MOD / filename
        raw = page.read_text(encoding="utf-8")
        soup = BeautifulSoup(raw, "html.parser")
        guides = soup.select(".fig-read[data-figure-read]")
        require(len(guides) == len(expected),
                f"{filename}: expected {len(expected)} Figure Reading guides, found {len(guides)}")
        names = [g.get("data-figure-read") for g in guides]
        require(set(names) == set(expected), f"{filename}: guide names drifted: {names}")

        for guide in guides:
            name = guide.get("data-figure-read") or ""
            text = " ".join(guide.stripped_strings)
            for heading in ("先看哪里", "看到什么", "能证明 / 不能证明"):
                require(heading in text, f"{filename}: {name} missing heading {heading}")
            previous = guide.find_previous_sibling()
            require(previous is not None and previous.name == "figure",
                    f"{filename}: {name} must immediately follow its Figure")
            img = previous.find("img")
            src = img.get("src", "") if img else ""
            require(expected[name] in src,
                    f"{filename}: {name} attached to wrong Figure asset: {src}")
            total += 1

        require(".fig-read{" in raw, f"{filename}: Figure Reading CSS missing")
        require("@media(max-width:760px){.fig-read{grid-template-columns:1fr}}" in raw,
                f"{filename}: responsive Figure Reading CSS missing")
        for marker in NEW_BOUNDARY_MARKERS.get(filename, ()):
            require(marker in raw, f"{filename}: Figure Reading claim boundary drifted: {marker}")

    require(total == 18, f"expected 18 core Figure Reading guides across modules 01-06, found {total}")
    print("FIGURE READING V2 SEAL PASS: 18 core Figures across modules 01-06 keep correct bindings, three-step reading guides, responsive layout, and claim boundaries.")


if __name__ == "__main__":
    main()
