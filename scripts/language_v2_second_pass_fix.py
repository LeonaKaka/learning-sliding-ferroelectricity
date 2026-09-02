from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab.html"

TEXT_REPLACEMENTS = {
    "Reproduction Lab（复现实验室）（复现实验室）01": "Reproduction Lab（复现实验室）01",
    "Reproduction Lab（复现实验室） ": "复现实验室 ",
    "· Lesson 01 · Gold Test": "· 第 01 课 · 已知答案测试",
    " / Reproduction Lab（复现实验室） / Lesson 01": " / 复现实验室 / 第 01 课",
    "M07": "模块 07",
    "大尺寸 2D GL ↔ elastic-line 结果": "大尺寸二维 GL ↔ elastic-line model（弹性线模型）结果",
    "Caballero 的 体场层面": "Caballero 的体场层面",
    "无无序情形": "无序为零的情形",
    "不是“复现论文 Fig. 1”": "不是“复现论文图 1”",
    "一维 x 网格；无无序、无热噪声": "一维 x 网格；无序为零、无热噪声",
    "无无序单畴壁": "无序为零的单畴壁",
    "它先证明 无无序对象是对的": "它先证明无序为零时的对象是对的",
    "Caballero 的无无序粗糙度增长": "Caballero 在无序为零时的粗糙度增长",
}

SMALL_REPLACEMENTS = {
    "本课只取 h=0、T=0 的无无序一维验证单元。": "本课只取 h=0、T=0、无序为零的一维验证单元。",
}

LOCKED_NUMERIC_STRINGS = ("1.415395", "0.0835%", "9.75×10⁻⁵")


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

    for small in soup.select(".eq small"):
        old = small.get_text()
        new = SMALL_REPLACEMENTS.get(old, old)
        if new != old:
            small.string = new

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
