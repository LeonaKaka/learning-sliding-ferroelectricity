from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

TARGET = ROOT / "modules/numerical-modeling.html"

REPLACEMENTS = {
    "sine-Gordon kink（孤子）（孤子）（孤子）": "sine-Gordon kink（孤子）",
    "sine-Gordon kink（孤子）（孤子）": "sine-Gordon kink（孤子）",
    "L01 解析 kink（孤子）": "L01 解析孤子",
    "驱动耦合相对局域 periodic energy 尺度": "驱动耦合相对局域周期性能量尺度",
    "畴壁看到的 energy 景观": "畴壁看到的能量景观",
    "有限尺寸 defect": "有限尺寸缺陷",
    "Research Track 的 fair matching": "Research Track 的公平匹配",
    "对常迁移率、加性噪声的 overdamped（过阻尼）TDGL / 模型 A 约定": "对常迁移率、加性噪声的过阻尼 TDGL / 模型 A 约定",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    # This micro-pass does not need to edit any equation card.
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
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

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 07 source-text changed during terminology polish")
    if [el.get_text(" ", strip=False) for el in soup.select(".eq")] != before_equations:
        raise RuntimeError("Module 07 equation card changed during terminology polish")
    if [(img.get("src"), img.get("alt")) for img in soup.find_all("img")] != before_images:
        raise RuntimeError("Module 07 image wiring changed during terminology polish")
    if [a.get("href") for a in soup.select("figure a")] != before_figure_links:
        raise RuntimeError("Module 07 figure link changed during terminology polish")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
