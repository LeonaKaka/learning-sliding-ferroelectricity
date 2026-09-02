from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-05.html"
LOCKED_RESULTS = (
    "0.071833070", "0.0000002%", "0.0000012%", "0.995554", "0.222%",
    "0.445%", "0.104%", "1.039429", "1.039472", "0.099555",
)

REPLACEMENTS = (
    ("体场→界面 这一步", "体场→界面这一步"),
    ("Dirac delta（狄拉克 δ） 之间", "Dirac delta（狄拉克 δ）之间"),
    ("而是 解析 Eq.26", "而是解析 Eq.26"),
    ("零点交叉 和故意错误对照", "零点交叉和故意错误对照"),
    ("所以 论文同规模的相关函数测试很轻", "所以论文同规模的相关函数测试很轻"),
    ("滑移铁电中的真实缺陷 必然", "滑移铁电中的真实缺陷必然"),
    ("同时比较 二维 GL", "同时比较二维 GL"),
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
        raise RuntimeError("Lab 05 equations changed")
    if before_pre != [x.get_text() for x in soup.select("pre")]:
        raise RuntimeError("Lab 05 machine/code blocks changed")
    if before_hrefs != [x.get("href") for x in soup.find_all("a")]:
        raise RuntimeError("Lab 05 href wiring changed")
    if before_srcs != [x.get("src") for x in soup.find_all("img")]:
        raise RuntimeError("Lab 05 Figure wiring changed")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 05 locked result changed: {token}")

    TARGET.write_text(after, encoding="utf-8")
    print("Lab 05 Chinese prose spacing pass complete; science/results unchanged.")


if __name__ == "__main__":
    main()
