from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT, source_blocks

# Validation-only seal for Module 07. Intentionally does not rewrite HTML.
TARGET = ROOT / "modules/numerical-modeling.html"
EXPECTED_FIGURES = {
    "../assets/interface-scaling/caballero2020-fig1-bulk-to-interface.png",
    "../assets/interface-scaling/caballero2020-fig5-roughness.png",
    "../assets/interface-scaling/caballero2020-fig5-structure-factor.png",
}
BANNED_VISIBLE_FRAGMENTS = {
    "项目项目 Drive PDF",
    "无无序",
    "区间s",
    "局部 局部呼吸模",
    "elastic-line model（elastic-line model（弹性线模型））",
    "sine-Gordon kink（孤子）（孤子）",
    "Hamiltonian（哈密顿量）（哈密顿量）",
    "畴壁 snapshot",
    "reduced 模型",
    "畴壁-extraction 方法",
    "fair matching",
    "numerical 数值证明",
}


def visible_text_without_sources_or_equations(soup: BeautifulSoup) -> str:
    clone = BeautifulSoup(str(soup), "html.parser")
    for el in clone.select(".source-text,.eq,script,style,pre,code"):
        el.decompose()
    return clone.get_text(" ", strip=True)


def main() -> None:
    html = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    sources = source_blocks(soup)
    if len(sources) < 3:
        raise RuntimeError(f"Module 07 unexpectedly has only {len(sources)} source-text blocks")

    figure_srcs = {img.get("src") for img in soup.select("figure img")}
    missing = EXPECTED_FIGURES - figure_srcs
    if missing:
        raise RuntimeError(f"Module 07 missing expected figure wiring: {sorted(missing)}")

    visible = visible_text_without_sources_or_equations(soup)
    bad = sorted(fragment for fragment in BANNED_VISIBLE_FRAGMENTS if fragment in visible)
    if bad:
        raise RuntimeError(f"Module 07 Language V2 residuals remain: {bad}")

    # No write: a successful run means the reviewed HTML remains byte-for-byte unchanged.


if __name__ == "__main__":
    main()
