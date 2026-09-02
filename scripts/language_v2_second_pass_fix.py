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
    ("Eq.19 hard gate", "Eq.19 的硬性验收条件"),
    ("bulk→line mapping", "体场到弹性线映射"),
    ("mapping breakdown", "映射失效"),
    ("Lesson 02", "第 02 课"),
    ("clean wall", "无序为零畴壁"),
    ("φ=0 crossing", "φ=0 零点交叉"),
    ("干净 crossing", "干净的零点交叉"),
    ("finite T", "有限温度"),
    ("更严格的 estimator", "更严格的估计量"),
    ("transverse profile", "横向剖面"),
    ("拟合 soliton", "拟合孤子"),
    ("fitting parameters", "拟合参数"),
    ("先取两端测试 validity 边界条件", "先取两端测试适用边界"),
    ("fit {φ₀,w,u(y)}", "拟合 {φ₀,w,u(y)}"),
    ("2D GL 在低温", "二维 GL 在低温"),
    ("Fig.3: t=1000", "Fig.3：t=1000"),
)


def eq_text(eq):
    return eq.get_text(" ", strip=False)


def blocked(node: NavigableString) -> bool:
    p = node.parent
    if p is None or p.name in {"script", "style", "pre", "code", "math"}:
        return True
    return bool(p.find_parent(class_="eq") or "eq" in p.get("class", []))


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [eq_text(x) for x in soup.select(".eq")]
    before_pre = [x.get_text() for x in soup.select("pre")]
    before_code = [x.get_text() for x in soup.select("code")]
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
    if before_eq != [eq_text(x) for x in soup.select(".eq")]:
        raise RuntimeError("Lab 04 equations changed")
    if before_pre != [x.get_text() for x in soup.select("pre")]:
        raise RuntimeError("Lab 04 machine/code pre blocks changed")
    if before_code != [x.get_text() for x in soup.select("code")]:
        raise RuntimeError("Lab 04 inline code changed")
    if before_hrefs != [x.get("href") for x in soup.find_all("a")]:
        raise RuntimeError("Lab 04 href wiring changed")
    if before_srcs != [x.get("src") for x in soup.find_all("img")]:
        raise RuntimeError("Lab 04 Figure wiring changed")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 04 locked result changed: {token}")

    TARGET.write_text(after, encoding="utf-8")
    print("Lab 04 targeted second pass complete; scientific/result contracts unchanged.")


if __name__ == "__main__":
    main()
