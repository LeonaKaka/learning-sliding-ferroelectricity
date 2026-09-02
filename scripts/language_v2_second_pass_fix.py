from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-06.html"
LOCKED_RESULTS = (
    "1.227%", "6.122%", "0.538906", "0.509213", "0.694308",
    "0.664796", "0.982981", "1.371256", "0.077925",
)

REPLACEMENTS = (
    ("第二篇工作 的一张图", "第二篇工作的一张图"),
    ("还必须要求 由 B 与 S", "还必须要求由 B 与 S"),
    ("这需要 估计量一致性 与尺寸/时间收敛", "这需要估计量一致性与尺寸/时间收敛"),
    ("傅里叶尺度区间 看起来", "傅里叶尺度区间看起来"),
    ("二维体场 继续使用 第 05 课 的随机键耦合", "二维体场继续使用第 05 课的随机键耦合"),
    ("使用 第 05 课 已经验证的", "使用第 05 课已经验证的"),
    ("第 03 课 已锁死", "第 03 课已锁死"),
    ("第 04 课 已锁死", "第 04 课已锁死"),
    ("第 05 课 已锁死", "第 05 课已锁死"),
    ("第 06 课 如果出问题", "第 06 课如果出问题"),
    ("这个阶段验证 上", "这个阶段验证上"),
    ("对实空间畴壁几何 的描述", "对实空间畴壁几何的描述"),
    ("小尺度/大尺度过渡 的权重", "小尺度/大尺度过渡的权重"),
    ("分箱中心 比较", "分箱中心比较"),
    ("密集模式 机械支配", "密集模式机械支配"),
    ("所以 跨模型映射 在", "所以跨模型映射在"),
    ("不是 傅里叶模式", "不是傅里叶模式"),
    ("但 由 B 与 S", "但由 B 与 S"),
    ("几何分析流程 不是", "几何分析流程不是"),
    ("第 01–06 课 已经", "第 01–06 课已经"),
    ("渐近 ζ 判据 仍然", "渐近 ζ 判据仍然"),
    ("不把 第 06 课 写成", "不把第 06 课写成"),
    ("时间/尺寸阶梯 仍然", "时间/尺寸阶梯仍然"),
    ("运动态 的临界点", "运动态的临界点"),
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
        raise RuntimeError("Lab 06 equations changed")
    if before_pre != [x.get_text() for x in soup.select("pre")]:
        raise RuntimeError("Lab 06 machine/code blocks changed")
    if before_hrefs != [x.get("href") for x in soup.find_all("a")]:
        raise RuntimeError("Lab 06 href wiring changed")
    if before_srcs != [x.get("src") for x in soup.find_all("img")]:
        raise RuntimeError("Lab 06 Figure wiring changed")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 06 locked result changed: {token}")
    if "渐近 ζ 判据：未通过。" not in after:
        raise RuntimeError("Lab 06 asymptotic-zeta failure boundary missing")
    if "CROSS-MODEL GEOMETRY PASS; ASYMPTOTIC ZETA GATE NOT PASSED" not in "\n".join(before_pre):
        raise RuntimeError("Lab 06 machine verdict marker changed")

    TARGET.write_text(after, encoding="utf-8")
    print("Lab 06 Chinese prose spacing pass complete; science/results unchanged.")


if __name__ == "__main__":
    main()
