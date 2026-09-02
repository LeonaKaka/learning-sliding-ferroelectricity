from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT, source_blocks

# Micro-pass: only two residuals found by reverse scanning the bot-produced HTML.
TARGET = ROOT / "modules/current-frontiers.html"


def main() -> None:
    soup = BeautifulSoup(TARGET.read_text(encoding="utf-8"), "html.parser")
    before_sources = source_blocks(soup)
    before_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]
    before_images = [(img.get("src"), img.get("alt")) for img in soup.find_all("img")]
    before_figure_links = [a.get("href") for a in soup.select("figure a")]

    # The author term is split across a <b> node, so string-level prose
    # replacement could not reach it. Annotate the visible teaching note only.
    candidates = [b for b in soup.find_all("b") if b.get_text(strip=True) == "avalanchelike"]
    if len(candidates) != 1:
        raise RuntimeError(f"Expected one visible avalanchelike term, found {len(candidates)}")
    if candidates[0].find_parent(class_="source-text"):
        raise RuntimeError("Refusing to edit avalanchelike inside source-text")
    candidates[0].string = "avalanchelike（类雪崩）"

    # FSS is not a required preserved abbreviation; keep the evidence matrix
    # readable in Chinese.
    headers = [th for th in soup.select(".matrix th") if th.get_text(" ", strip=True) == "β / ν + FSS"]
    if len(headers) != 1:
        raise RuntimeError(f"Expected one FSS matrix header, found {len(headers)}")
    headers[0].string = "β / ν + 有限尺寸标度"

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 08 source-text changed during final terminology cleanup")
    if [el.get_text(" ", strip=False) for el in soup.select(".eq")] != before_equations:
        raise RuntimeError("Module 08 equation card changed during final terminology cleanup")
    if [(img.get("src"), img.get("alt")) for img in soup.find_all("img")] != before_images:
        raise RuntimeError("Module 08 image wiring changed during final terminology cleanup")
    if [a.get("href") for a in soup.select("figure a")] != before_figure_links:
        raise RuntimeError("Module 08 figure link changed during final terminology cleanup")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
