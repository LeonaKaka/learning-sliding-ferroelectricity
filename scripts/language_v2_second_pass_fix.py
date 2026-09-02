from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT, source_blocks

# Final page-scoped cleanup for Module 04.  Do not broaden this into a bulk
# replacement pass: Language V2 pages are now reviewed and repaired one by one.
TARGET = ROOT / "modules/pinning-creep.html"


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    return bool(parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []))


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    before_sources = source_blocks(soup)

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old.replace("log–log 斜率", "双对数斜率")
        new = new.replace("任意 log–log 直线", "任意双对数直线")
        if new != old:
            node.replace_with(new)

    if source_blocks(soup) != before_sources:
        raise RuntimeError("Module 04 source-text changed during final cleanup")
    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
