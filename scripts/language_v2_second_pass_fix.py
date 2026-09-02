from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

TARGET = ROOT / "modules/disorder-rfim.html"

REPLACEMENTS = {
    "项目项目 Drive PDF": "项目 Drive PDF",
    "封闭封闭小畴": "封闭小畴",
    "更强 Se-vacancy 陷阱动力学": "更强的 Se 空位陷阱动力学",
    "局域偏置（RF-like）": "局域偏置（类 RF）",
    "静态 Gaussian RF": "静态 Gaussian RF（高斯随机场）",
    "原始 Figure 对象": "原论文图对象",
    "Introduction": "引言",
    "Conclusion": "结论",
    "本征异常标度与 spatial 多重标度": "本征异常标度与空间多重标度",
    "提出的 conjecture": "提出的猜想",
    "体相场 / lattice 模型": "体相场 / 晶格模型",
    "回到 sliding ferroelectricity（滑移铁电）": "回到滑移铁电",
    "Figure 只取": "论文图只取",
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
    text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    before_sources = source_blocks(soup)
    before_equations = [el.get_text(" ", strip=False) for el in soup.select(".eq")]

    # Introduce the genuinely useful English terms once, then keep later prose Chinese.
    q = soup.select_one(".q")
    if q and "随机键、弹性流形随机场" in q.get_text():
        for node in list(q.find_all(string=True)):
            old = str(node)
            if "随机键、弹性流形随机场" in old:
                node.replace_with(old.replace(
                    "随机键、弹性流形随机场",
                    "random-bond（随机键）、弹性流形中的 random-field（随机场）",
                ))
                break
    nav = soup.select("header .bar span a")
    if len(nav) >= 4:
        nav[3].string = "悬垂"

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
        raise RuntimeError("Module 06 source-text changed during second Language V2 audit")
    if [el.get_text(" ", strip=False) for el in soup.select(".eq")] != before_equations:
        raise RuntimeError("Module 06 displayed equation changed during second Language V2 audit")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
