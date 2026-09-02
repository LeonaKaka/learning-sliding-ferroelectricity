from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-02.html"
LOCKED_RESULTS = (
    "48/48",
    "2.629×10<sup>−3</sup>",
    "2.764×10<sup>−5</sup>",
    "4.020×10<sup>−4</sup>",
    "0.870339",
)

TEXT_REPLACEMENTS = {
    "复现实验室（复现实验室）02": "Reproduction Lab（复现实验室）02",
    " / 复现实验室 / Lesson 02": " / 复现实验室 / 第 02 课",
    "对每个固定 y": "对每个固定的 y",
    "这一列中，寻找唯一一对相邻格点满足": "列，寻找唯一一对相邻格点满足",
    " 列，寻找唯一一对相邻格点满足": "，在对应的 x 列中寻找唯一一对相邻格点满足",
    "在 第 03 课给它加热噪声": "在第 03 课给它加热噪声",
    "B(r,t) scaling curve 与我们的 small-system curve 并排，做真正的 thumbnail reproduction，并用解析 EW prediction 检查有限尺寸偏差。":
        "B(r,t) 标度曲线与我们的小系统曲线并排，做真正的缩略复现，并用解析 EW 预测检查有限尺寸偏差。",
    " scaling curve 与我们的 small-system curve 并排，做真正的 thumbnail reproduction，并用解析 EW prediction 检查有限尺寸偏差。":
        " 标度曲线与我们的小系统曲线并排，做真正的缩略复现，并用解析 EW 预测检查有限尺寸偏差。",
    "论文 Figure": "论文图",
    "topology gate（拓扑判据）": "拓扑判据",
    "periodic boundary（周期边界）": "周期边界",
    "论文图 并排比": "论文图并排比",
    "强调的 拓扑判据": "强调的拓扑判据",
    "原论文图 告诉": "原论文图告诉",
    "论文展示 二维 GL 场": "论文展示二维 GL 场",
}


def equation_body_text(eq) -> str:
    clone = BeautifulSoup(str(eq), "html.parser").select_one(".eq")
    for small in clone.select("small"):
        small.decompose()
    return clone.get_text(" ", strip=False)


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
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
    before_src = [img.get("src") for img in soup.find_all("img")]
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

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 02 expected 2 Figures, found {len(figures)}")
    figures[0]["alt"] = "Caballero 2020 图 1：二维 GL 体场与提取界面"

    if [equation_body_text(eq) for eq in soup.select(".eq")] != before_eq:
        raise RuntimeError("Lab 02 equation body changed")
    if [pre.get_text() for pre in soup.select("pre")] != before_pre:
        raise RuntimeError("Lab 02 preformatted code/output changed")
    if [code.get_text() for code in soup.select("code")] != before_code:
        raise RuntimeError("Lab 02 inline code changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Lab 02 links changed")
    if [img.get("src") for img in soup.find_all("img")] != before_src:
        raise RuntimeError("Lab 02 Figure wiring changed")

    rendered = str(soup)
    after_results = {token: rendered.count(token) for token in LOCKED_RESULTS}
    if after_results != before_results:
        raise RuntimeError(f"Lab 02 locked results changed: {before_results} -> {after_results}")

    TARGET.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
