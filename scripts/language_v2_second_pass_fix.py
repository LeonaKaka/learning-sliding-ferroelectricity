from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

TARGET = ROOT / "modules/numerical-modeling.html"

REPLACEMENTS = {
    "“only allows continuous and univalued 界面”": "“只允许连续、单值界面”",
    "原 Figure 精裁": "原论文图精裁",
    "原 Figure 面板精裁": "原论文图面板精裁",
    "畴壁 snapshot": "畴壁快照",
    "Fourier 空间": "Fourier（傅里叶）空间",
    "reduced 模型": "约化模型",
    "畴壁-extraction 方法": "畴壁提取方法",
    "相邻层的 DW 位于": "相邻层的畴壁位于",
    "Hamiltonian（哈密顿量）（哈密顿量）": "Hamiltonian（哈密顿量）",
    "有限尺寸 defect": "有限尺寸缺陷",
}


def formula_blocks(soup: BeautifulSoup) -> list[str]:
    out: list[str] = []
    for el in soup.select(".eq"):
        clone = BeautifulSoup(str(el), "html.parser").select_one(".eq")
        if clone is None:
            continue
        for small in clone.find_all("small"):
            small.decompose()
        out.append(clone.get_text(" ", strip=False))
    return out


def inside_eq_small(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None:
        return False
    small = parent if parent.name == "small" else parent.find_parent("small")
    return small is not None and small.find_parent(class_="eq") is not None


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    in_eq = "eq" in parent.get("class", []) or parent.find_parent(class_="eq") is not None
    if in_eq and not inside_eq_small(node):
        return True
    return False


def main() -> None:
    soup = BeautifulSoup(TARGET.read_text(encoding="utf-8"), "html.parser")
    before_sources = source_blocks(soup)
    before_formulae = formula_blocks(soup)
    before_images = [(img.get("src"), img.get("alt")) for img in soup.find_all("img")]
    before_links = [a.get("href") for a in soup.select("figure a")]

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
        raise RuntimeError("Module 07 source-text changed during reverse audit")
    if formula_blocks(soup) != before_formulae:
        raise RuntimeError("Module 07 mathematical formula changed during reverse audit")
    if [(img.get("src"), img.get("alt")) for img in soup.find_all("img")] != before_images:
        raise RuntimeError("Module 07 image wiring changed during reverse audit")
    if [a.get("href") for a in soup.select("figure a")] != before_links:
        raise RuntimeError("Module 07 figure link changed during reverse audit")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
