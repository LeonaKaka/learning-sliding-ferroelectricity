from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

# Second, narrow reverse-audit pass for Module 08.  Do not repeat the broad
# normalization: only repair terminology and prose that survived the first pass.
TARGET = ROOT / "modules/current-frontiers.html"

REPLACEMENTS = {
    "KPFM、Raman、DFT/BEC": "KPFM、Raman（拉曼）、DFT/BEC",
    "Raman（拉曼）成像把器件": "拉曼成像把器件",
    "KPFM/Raman 图": "KPFM / 拉曼图",
    "作者使用 avalanchelike 描述": "作者使用 avalanchelike（类雪崩）描述",
    "分步 / 区域依赖翻转是对无序敏感的动力学的证据": "分步 / 区域依赖翻转是动力学对无序敏感的证据",
    "这把 Chen 的 ““无畴壁，不反转””": "这把 Chen 的“无畴壁，不反转”",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    soup = BeautifulSoup(TARGET.read_text(encoding="utf-8"), "html.parser")
    before_sources = source_blocks(soup)
    before_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]
    before_images = [(img.get("src"), img.get("alt")) for img in soup.find_all("img")]
    before_figure_links = [a.get("href") for a in soup.select("figure a")]

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for a, b in sorted(REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
            new = new.replace(a, b)
        if new != old:
            node.replace_with(new)

    # First pedagogical occurrence of the full BEC term: keep the English
    # recognition form once, then retain Chinese prose afterwards.
    h3 = None
    for h2 in soup.find_all("h2"):
        if h2.get_text(" ", strip=True).startswith("3 · Wang & Dong"):
            h3 = h2
            break
    if h3 is None:
        raise RuntimeError("Module 08 Wang/Ke section not found")
    intro = h3.find_next_sibling("p")
    if intro is None or "Born 有效电荷" not in intro.get_text():
        raise RuntimeError("Module 08 first Born effective charge teaching occurrence not found")
    for node in list(intro.find_all(string=True)):
        old = str(node)
        if "非对角 Born 有效电荷" in old:
            node.replace_with(old.replace(
                "非对角 Born 有效电荷",
                "非对角 Born effective charge（Born 有效电荷）",
                1,
            ))
            break

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 08 source-text changed during terminology audit")
    if [el.get_text(" ", strip=False) for el in soup.select(".eq")] != before_equations:
        raise RuntimeError("Module 08 equation card changed during terminology audit")
    if [(img.get("src"), img.get("alt")) for img in soup.find_all("img")] != before_images:
        raise RuntimeError("Module 08 image wiring changed during terminology audit")
    if [a.get("href") for a in soup.select("figure a")] != before_figure_links:
        raise RuntimeError("Module 08 figure link changed during terminology audit")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
