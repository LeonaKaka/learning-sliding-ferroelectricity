from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/research-track.html"

REPLACEMENTS = {
    "这个 periodic 模型": "这个周期模型",
    "stacking registry（堆垛配位） 压成": "stacking registry（堆垛配位）压成",
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
        for src, dst in REPLACEMENTS.items():
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    if [equation_body_text(eq) for eq in soup.select(".eq")] != before_eq_bodies:
        raise RuntimeError("Research Track mathematical equation body changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Research Track links changed during term-reuse cleanup")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
