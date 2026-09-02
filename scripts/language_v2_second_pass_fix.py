from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/research-track.html"


def equation_body_text(eq) -> str:
    clone = BeautifulSoup(str(eq), "html.parser").select_one(".eq")
    for small in clone.select("small"):
        small.decompose()
    return clone.get_text(" ", strip=False)


def main() -> None:
    soup = BeautifulSoup(TARGET.read_text(encoding="utf-8"), "html.parser")
    before_eq = [equation_body_text(eq) for eq in soup.select(".eq")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]

    changed = 0
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString):
            continue
        parent = node.parent
        if parent is None or parent.name in {"script", "style", "pre", "math"}:
            continue
        if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
            continue
        old = str(node)
        new = old.replace("同一 Ising 模型", "同一伊辛模型")
        if new != old:
            node.replace_with(new)
            changed += 1

    if changed != 1:
        raise RuntimeError(f"Expected exactly one Research Track Ising reuse fix, got {changed}")
    if [equation_body_text(eq) for eq in soup.select(".eq")] != before_eq:
        raise RuntimeError("Research Track equation body changed during Ising cleanup")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Research Track links changed during Ising cleanup")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
