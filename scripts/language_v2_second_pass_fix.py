from __future__ import annotations

import re
from pathlib import Path
from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

# Module 08 is now in seal mode: validate the final HTML, never rewrite it.
TARGET = ROOT / "modules/current-frontiers.html"

# These are ordinary research-workflow / mixed-language residues that must not
# remain in visible teaching prose. Paper originals, equations, titles and
# non-visible attributes are excluded from this scan.
FORBIDDEN_VISIBLE = (
    "项目项目 Drive PDF",
    "无序 无序样本",
    "前沿 verdict",
    "cycle-dependent",
    "competition",
    "readout",
    "device-level",
    "waiting 时间",
    "stepwise",
    "variability",
    " observations",
    "FSS",
    "KPFM/Raman",
    "Raman 图",
    " gate ",
    " pipeline ",
    " authority ",
    " checkpoint ",
    " benchmark ",
    " realization",
    " estimator",
    " fit window",
    " fit-window",
    " raw data",
    " steady velocity",
    " sample-specific threshold",
    " effective exponent",
)


def visible_teaching_text(soup: BeautifulSoup) -> str:
    clone = BeautifulSoup(str(soup), "html.parser")
    for selector in (".source-text", ".eq", "script", "style", "pre", "math"):
        for node in clone.select(selector):
            node.decompose()
    return " ".join(clone.stripped_strings)


def resolve_local_asset(src: str) -> Path:
    # HTML sits in modules/, so resolve relative paths from TARGET.parent.
    return (TARGET.parent / src).resolve()


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")

    text = visible_teaching_text(soup)
    for token in FORBIDDEN_VISIBLE:
        if token in text:
            raise RuntimeError(f"Module 08 visible Language V2 residue: {token!r}")

    # Catch repeated bilingual annotations and the known quote-doubling scar.
    repeated_patterns = (
        r"（类雪崩）（类雪崩）",
        r"Born effective charge（Born 有效电荷）（Born 有效电荷）",
        r"Raman（拉曼）（拉曼）",
        r"““|””",
    )
    for pattern in repeated_patterns:
        if re.search(pattern, text):
            raise RuntimeError(f"Module 08 mechanical-language scar: {pattern}")

    # The genuine terms we intentionally keep must have a clean first-use form.
    required_visible = (
        "Born effective charge（Born 有效电荷）",
        "avalanchelike（类雪崩）",
        "Raman（拉曼）",
        "β / ν + 有限尺寸标度",
    )
    for token in required_visible:
        if token not in text:
            raise RuntimeError(f"Module 08 required Language V2 form missing: {token!r}")

    # Every quoted paper block must still carry an untouched English source and
    # an adjacent Chinese guide; this validates structure without rewriting it.
    source_blocks = soup.select(".source-text")
    if len(source_blocks) < 5:
        raise RuntimeError(f"Module 08 unexpectedly has only {len(source_blocks)} source-text blocks")
    for source in source_blocks:
        parent = source.find_parent(class_="src")
        if parent is None or parent.select_one(".translation") is None:
            raise RuntimeError("Module 08 source-text block lost its Chinese guide")

    # Check every local Figure image and Figure link against the checkout.
    checked = set()
    for node, attr in [(img, "src") for img in soup.select("figure img")] + [
        (a, "href") for a in soup.select("figure a")
    ]:
        value = node.get(attr)
        if not value or value.startswith(("http://", "https://", "#")):
            continue
        path = resolve_local_asset(value)
        if path in checked:
            continue
        checked.add(path)
        if not path.is_file():
            raise RuntimeError(f"Module 08 Figure asset missing: {value}")
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Module 08 Figure path escapes repository: {value}") from exc

    if len(checked) < 4:
        raise RuntimeError(f"Module 08 unexpectedly validates only {len(checked)} Figure assets")

    print(
        f"Module 08 seal PASS: {len(source_blocks)} source blocks, "
        f"{len(checked)} local Figure assets, no forbidden visible residues."
    )


if __name__ == "__main__":
    main()
