from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-04.html"
LOCKED_RESULTS = (
    "7.67%", "7.57%", "4.49%", "4.36%",
    "0.9879", "1.3738", "0.9870", "1.3740",
    "26.52%", "1.6664", "0.9806", "5.47%",
    "40.51%", "1.7018", "0.9760", "7.23%",
)

REPLACEMENTS = (
    ("只要 体场到弹性线映射 的诊断", "只要体场到弹性线映射的诊断"),
    ("第 02 课 在 T=0 的 无序为零畴壁 上用 φ=0 零点交叉 很合适", "第 02 课在 T=0 的无序为零畴壁上用 φ=0 零点交叉很合适"),
    ("但论文在 有限温度 下采用", "但论文在有限温度下采用"),
    ("整个 横向剖面 φ(x,y,t)", "整个横向剖面 φ(x,y,t)"),
    ("都作为 拟合参数。", "都作为拟合参数。"),
)


def blocked(node: NavigableString) -> bool:
    p = node.parent
    if p is None or p.name in {"script", "style", "pre", "code", "math"}:
        return True
    return bool(p.find_parent(class_="eq") or "eq" in p.get("class", []))


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [x.get_text(" ", strip=False) for x in soup.select(".eq")]
    before_pre = [x.get_text() for x in soup.select("pre")]
    before_hrefs = [x.get("href") for x in soup.find_all("a")]
    before_srcs = [x.get("src") for x in soup.find_all("img")]
    before_results = {x: raw.count(x) for x in LOCKED_RESULTS}

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in REPLACEMENTS:
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    after = str(soup)
    if before_eq != [x.get_text(" ", strip=False) for x in soup.select(".eq")]:
        raise RuntimeError("Lab 04 equations changed")
    if before_pre != [x.get_text() for x in soup.select("pre")]:
        raise RuntimeError("Lab 04 machine/code blocks changed")
    if before_hrefs != [x.get("href") for x in soup.find_all("a")]:
        raise RuntimeError("Lab 04 href wiring changed")
    if before_srcs != [x.get("src") for x in soup.find_all("img")]:
        raise RuntimeError("Lab 04 Figure wiring changed")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 04 locked result changed: {token}")

    TARGET.write_text(after, encoding="utf-8")
    print("Lab 04 Chinese prose spacing pass complete; science/results unchanged.")


if __name__ == "__main__":
    main()
