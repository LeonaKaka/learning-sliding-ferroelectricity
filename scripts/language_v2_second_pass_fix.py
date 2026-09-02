from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT, source_blocks

TARGET = ROOT / "modules/numerical-modeling.html"
OLD = "多个拟合区间s"
NEW = "多个拟合区间"


def main() -> None:
    html = TARGET.read_text(encoding="utf-8")
    if html.count(OLD) != 1:
        raise RuntimeError(f"Expected exactly one Module 07 residual {OLD!r}, found {html.count(OLD)}")

    before = BeautifulSoup(html, "html.parser")
    before_sources = source_blocks(before)
    before_equations = [el.get_text(" ", strip=False) for el in before.select(".eq")]
    before_images = [(img.get("src"), img.get("alt")) for img in before.find_all("img")]
    before_links = [a.get("href") for a in before.select("figure a")]

    repaired = html.replace(OLD, NEW)
    after = BeautifulSoup(repaired, "html.parser")

    if source_blocks(after) != before_sources:
        raise RuntimeError("Module 07 source-text changed while fixing interval typo")
    if [el.get_text(" ", strip=False) for el in after.select(".eq")] != before_equations:
        raise RuntimeError("Module 07 equation card changed while fixing interval typo")
    if [(img.get("src"), img.get("alt")) for img in after.find_all("img")] != before_images:
        raise RuntimeError("Module 07 image wiring changed while fixing interval typo")
    if [a.get("href") for a in after.select("figure a")] != before_links:
        raise RuntimeError("Module 07 figure link changed while fixing interval typo")

    TARGET.write_text(repaired, encoding="utf-8")


if __name__ == "__main__":
    main()
