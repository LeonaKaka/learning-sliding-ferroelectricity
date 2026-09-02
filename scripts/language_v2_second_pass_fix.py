from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/research-track.html"
OLD = "同一 Ising 模型"
NEW = "同一伊辛模型"


def equation_body_text(eq) -> str:
    clone = BeautifulSoup(str(eq), "html.parser").select_one(".eq")
    for small in clone.select("small"):
        small.decompose()
    return clone.get_text(" ", strip=False)


def main() -> None:
    soup = BeautifulSoup(TARGET.read_text(encoding="utf-8"), "html.parser")
    before_eq = [equation_body_text(eq) for eq in soup.select(".eq")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString):
            continue
        parent = node.parent
        if parent is None or parent.name in {"script", "style", "pre", "math"}:
            continue
        if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
            continue
        old = str(node)
        new = old.replace(OLD, NEW)
        if new != old:
            node.replace_with(new)

    visible = " ".join(soup.stripped_strings)
    if OLD in visible:
        raise RuntimeError("Research Track still contains later bare Ising term reuse")
    if NEW not in visible:
        raise RuntimeError("Research Track expected Chinese follow-up '同一伊辛模型' is missing")
    if [equation_body_text(eq) for eq in soup.select(".eq")] != before_eq:
        raise RuntimeError("Research Track equation body changed during Ising cleanup")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Research Track links changed during Ising cleanup")

    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
