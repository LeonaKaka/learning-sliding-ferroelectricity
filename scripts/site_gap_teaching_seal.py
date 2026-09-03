from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"
FOUND = MODULES / "foundations.html"
TRACK = MODULES / "research-track.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def seal_foundations() -> None:
    raw = FOUND.read_text(encoding="utf-8")
    doc = BeautifulSoup(raw, "html.parser")

    nodes = doc.select("#next-question")
    require(len(nodes) == 1, f"Foundations handoff count drifted: {len(nodes)}")
    handoff = nodes[0]
    require("handoff" in (handoff.get("class") or []), "Foundations handoff class missing")

    next_nav = handoff.find_next_sibling("div", class_="next")
    require(next_nav is not None, "Foundations handoff is no longer directly before final navigation")
    require(next_nav.find("a", href="switching-pathways.html") is not None,
            "Foundations → Switching Pathways navigation missing")

    locked = (
        "这一章结束后，为什么下一步必须进入 Switching Pathways？",
        "存在一条低能结构通道，不等于真实器件会沿这条通道整层同步翻转",
        "单胞结构路径",
        "真实空间翻转过程",
        "预存畴壁与局域钉扎又怎样选择实际路径",
    )
    for text in locked:
        require(text in raw, f"Foundations handoff boundary drifted: {text}")

    require(len(doc.select(".source-text")) == 5,
            "Foundations source-text evidence count drifted")
    require(len(doc.find_all("figure")) == 5,
            "Foundations Figure count drifted")


def seal_track() -> None:
    raw = TRACK.read_text(encoding="utf-8")
    doc = BeautifulSoup(raw, "html.parser")

    sections = doc.select("section#entry-check.entry-check")
    require(len(sections) == 1, f"Research Track entry gate count drifted: {len(sections)}")
    section = sections[0]

    cards = section.select(".entry-grid > a")
    require(len(cards) == 4, f"Research Track prerequisite count drifted: {len(cards)}")
    hrefs = tuple(a.get("href") for a in cards)
    expected = (
        "domain-walls.html",
        "pinning-creep.html",
        "depinning.html",
        "numerical-modeling.html",
    )
    require(hrefs == expected, f"Research Track prerequisite order/targets drifted: {hrefs}")
    for href in hrefs:
        require((MODULES / href).exists(), f"Research Track prerequisite target missing: {href}")

    labels = tuple(a.get_text(" ", strip=True) for a in cards)
    for marker in ("① 运动对象", "② 钉扎与蠕变", "③ 临界证据链", "④ 数值纪律"):
        require(any(marker in label for label in labels), f"Research Track prerequisite marker missing: {marker}")

    locked = (
        "这页不是用来提前接触“更高级公式”的",
        "为什么“看到一次局域退钉扎”还不是临界退钉扎",
        "为什么 f<sub>c</sub> 必须先独立约束，再谈 β、ζ、ν 与有限尺寸闭合",
        "为什么 dx / dt、无序归一化、统计独立性和留出验证会直接决定物理结论是否可信",
        "如果这四项里有两项还说不清，先回 03–07",
        "把已经理解的部件接成研究问题",
    )
    for text in locked:
        require(text in raw, f"Research Track entry boundary drifted: {text}")

    rule = doc.find("p", class_="rule", string=lambda s: s and "边界：本页只公开研究问题" in s)
    require(rule is not None, "Research Track public/unpublished-data boundary rule missing")
    require(section.find_next_sibling("p", class_="rule") == rule,
            "Research Track entry gate no longer sits immediately before the page boundary rule")


def main() -> None:
    seal_foundations()
    seal_track()
    print(
        "TEACHING V2 SITE GAP SEAL PASS: Foundations→Pathways handoff and "
        "Research Track four-prerequisite gate are structurally and scientifically locked."
    )


if __name__ == "__main__":
    main()
