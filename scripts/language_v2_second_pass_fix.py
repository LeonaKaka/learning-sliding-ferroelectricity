from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/research-track.html"

# Small, idempotent cleanup found by reverse-scanning the first-pass bot HTML.
TEXT_REPLACEMENTS = {
    "Module 04 · UV/IR mask": "模块 04 · UV/IR 尺度掩膜",
    "Module 05 · objective": "模块 05 · 目标函数",
    "去 Module 07 看运行记录 / 来源追踪约定": "去模块 07 看运行记录 / 来源追踪约定",
    "去 Module 07 看无量纲化 / 可辨识性": "去模块 07 看无量纲化 / 可辨识性",
    "不能因为把突发事件叫作 avalanche 就把它当成雪崩": "不能因为把突发事件叫作“雪崩”就把它当成雪崩临界现象",
    "幂律-consistent 区间": "与幂律相容的区间",
    "、work、事件大小统计": "、回线功、事件大小统计",
    "同一个文件里有很多 rows，不代表 n 很大": "同一个文件里有很多记录行，不代表 n 很大",
    "由内部 rows 数量放大的 n": "由内部记录行数量放大的 n",
    "无序-总体推断": "无序总体推断",
    "去模块 06 看完整统计边界": "去模块 06 看完整统计边界",
    "07 Numerical Modeling（数值建模）": "07 Numerical Modeling（数值建模）",
}

SMALL_REPLACEMENTS = {
    "二维 网格单元平均 white 无序：std ∝ 1/dx。该缩放只针对明确的 δ 相关连续场约定。":
        "二维网格单元平均白噪声无序：std ∝ 1/dx。该缩放只针对明确的 δ 相关连续场约定。",
}


def equation_body_text(eq) -> str:
    clone = BeautifulSoup(str(eq), "html.parser").select_one(".eq")
    for small in clone.select("small"):
        small.decompose()
    return clone.get_text(" ", strip=False)


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "math", "small"}:
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    soup = BeautifulSoup(TARGET.read_text(encoding="utf-8"), "html.parser")
    before_eq_bodies = [equation_body_text(eq) for eq in soup.select(".eq")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in TEXT_REPLACEMENTS.items():
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    # Equation mathematical bodies are immutable; only human-readable <small>
    # guides may be localized.
    for small in soup.select(".eq small"):
        old = small.get_text()
        new = SMALL_REPLACEMENTS.get(old, old)
        if new != old:
            small.string = new

    if [equation_body_text(eq) for eq in soup.select(".eq")] != before_eq_bodies:
        raise RuntimeError("Research Track mathematical equation body changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Research Track links changed during second audit")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
