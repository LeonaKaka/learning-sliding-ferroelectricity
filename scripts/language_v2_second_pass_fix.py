from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab.html"
LOCKED_NUMERIC_STRINGS = ("1.415395", "0.0835%", "9.75×10⁻⁵")

TEXT_REPLACEMENTS = {
    " / Lesson 01": " / 第 01 课",
    "无序为零的情形的 stationary soliton（定态孤子）": "无序为零时，stationary soliton（定态孤子）",
}


def equation_body_text(eq) -> str:
    clone = BeautifulSoup(str(eq), "html.parser").select_one(".eq")
    for small in clone.select("small"):
        small.decompose()
    return clone.get_text(" ", strip=False)


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math", "small"}:
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [equation_body_text(eq) for eq in soup.select(".eq")]
    before_pre = [pre.get_text() for pre in soup.select("pre")]
    before_code = [code.get_text() for code in soup.select("code")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]
    before_img_src = [img.get("src") for img in soup.find_all("img")]
    before_numeric_counts = {token: raw.count(token) for token in LOCKED_NUMERIC_STRINGS}

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in TEXT_REPLACEMENTS.items():
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    header_small = soup.select_one("header .bar small")
    if header_small is None:
        raise RuntimeError("Lab 01 header lesson label missing")
    header_small.string = "· 第 01 课 · 已知答案测试"

    figure = soup.select_one("figure.fig img")
    if figure is None:
        raise RuntimeError("Lab 01 result Figure missing")
    figure["alt"] = "TDGL 畴壁向解析扭结弛豫与自由能收敛"

    if [equation_body_text(eq) for eq in soup.select(".eq")] != before_eq:
        raise RuntimeError("Lab 01 equation body changed")
    if [pre.get_text() for pre in soup.select("pre")] != before_pre:
        raise RuntimeError("Lab 01 preformatted code/output changed")
    if [code.get_text() for code in soup.select("code")] != before_code:
        raise RuntimeError("Lab 01 inline code changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Lab 01 links changed")
    if [img.get("src") for img in soup.find_all("img")] != before_img_src:
        raise RuntimeError("Lab 01 Figure path changed")

    rendered = str(soup)
    after_numeric_counts = {token: rendered.count(token) for token in LOCKED_NUMERIC_STRINGS}
    if after_numeric_counts != before_numeric_counts:
        raise RuntimeError(f"Lab 01 locked numerical results changed: {before_numeric_counts} -> {after_numeric_counts}")

    TARGET.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
