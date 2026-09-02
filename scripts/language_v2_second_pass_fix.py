from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-03.html"
LOCKED_RESULTS = (
    "0.91%", "1.36%", "3.04%",
    "1.39%", "1.86%", "3.40%",
    "1.02%", "1.33%", "2.46%",
    "0.9592",
)

TEXT_REPLACEMENTS = {
    "最干净的 一维 Edwards–Wilkinson 层": "最干净的一维 Edwards–Wilkinson 层",
    "1D Edwards–Wilkinson Eq. (15)": "一维 Edwards–Wilkinson Eq. (15)",
    "8 · 为什么还没跑 2D GL？": "8 · 为什么还没跑二维 GL？",
    "放回 2D GL": "放回二维 GL",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    return False


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [eq.get_text(" ", strip=False) for eq in soup.select(".eq")]
    before_pre = [pre.get_text() for pre in soup.select("pre")]
    before_code = [code.get_text() for code in soup.select("code")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]
    before_src = [img.get("src") for img in soup.find_all("img")]
    before_sources = [node.get_text() for node in soup.select(".source-text")]
    before_results = {token: raw.count(token) for token in LOCKED_RESULTS}

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in TEXT_REPLACEMENTS.items():
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    if soup.title:
        soup.title.string = "Reproduction Lab（复现实验室）03 · EW 热粗糙化缩略复现"

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 03 expected 2 Figures, found {len(figures)}")
    figures[0]["alt"] = "Caballero 2020 图 2：界面粗糙度随时间演化"
    figures[1]["alt"] = "本课 EW 数值模拟与 Caballero Eq.19 的粗糙度对照"

    if [eq.get_text(" ", strip=False) for eq in soup.select(".eq")] != before_eq:
        raise RuntimeError("Lab 03 equation body changed")
    if [pre.get_text() for pre in soup.select("pre")] != before_pre:
        raise RuntimeError("Lab 03 code/output block changed")
    if [code.get_text() for code in soup.select("code")] != before_code:
        raise RuntimeError("Lab 03 inline code changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Lab 03 links changed")
    if [img.get("src") for img in soup.find_all("img")] != before_src:
        raise RuntimeError("Lab 03 Figure wiring changed")
    if [node.get_text() for node in soup.select(".source-text")] != before_sources:
        raise RuntimeError("Lab 03 paper source text changed")

    rendered = str(soup)
    after_results = {token: rendered.count(token) for token in LOCKED_RESULTS}
    if after_results != before_results:
        raise RuntimeError(f"Lab 03 locked results changed: {before_results} -> {after_results}")
    TARGET.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
