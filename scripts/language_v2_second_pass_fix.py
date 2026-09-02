from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/research-track.html"

FORBIDDEN_VISIBLE = (
    "无序 is not one number",
    "方案 split",
    "anti-overfit rule",
    "自助法 draw",
    "quenched 无序样本",
    "nested 自助法",
    "bound 信息",
    "无序 无序样本",
    "这个 periodic 模型",
    "stacking registry（堆垛配位） 压成",
    "Module 04",
    "Module 05",
    "Module 07",
    " objective ",
    " rows",
    "work、事件",
    "幂律-consistent",
    " gate ",
    " window ",
    " fit ",
    " authority ",
    " pipeline ",
    " checkpoint ",
    " benchmark ",
    " realization",
    " estimator",
    " raw data",
    " steady velocity",
    " sample-specific threshold",
    " effective exponent",
)

REQUIRED_VISIBLE = (
    "Research Track（研究路线）",
    "Depinning（退钉扎）",
    "periodic scalar model（周期标量模型）",
    "Hamiltonian（哈密顿量）",
    "Gaussian white random field（高斯白噪声随机场）",
    "数据 → 估计量 → 证据 → 结论",
    "配对与分层不确定度",
    "失效不是“没做成”",
)


def visible_teaching_text(soup: BeautifulSoup) -> str:
    clone = BeautifulSoup(str(soup), "html.parser")
    for selector in (".eq", "script", "style", "pre", "math"):
        for node in clone.select(selector):
            node.decompose()
    return " ".join(clone.stripped_strings)


def local_target(href: str) -> Path | None:
    if not href or href.startswith(("http://", "https://", "mailto:", "#")):
        return None
    parsed = urlsplit(href)
    if not parsed.path:
        return None
    return (TARGET.parent / parsed.path).resolve()


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    text = visible_teaching_text(soup)

    for token in FORBIDDEN_VISIBLE:
        if token in text:
            raise RuntimeError(f"Research Track visible Language V2 residue: {token!r}")

    for token in REQUIRED_VISIBLE:
        if token not in text:
            raise RuntimeError(f"Research Track required Language V2 form missing: {token!r}")

    for pattern in (
        r"无序\s*无序样本",
        r"（周期标量模型）（周期标量模型）",
        r"（哈密顿量）（哈密顿量）",
        r"““|””",
    ):
        if re.search(pattern, text):
            raise RuntimeError(f"Research Track mechanical-language scar: {pattern}")

    equations = soup.select(".eq")
    if len(equations) < 5:
        raise RuntimeError(f"Research Track unexpectedly has only {len(equations)} equations")

    checked = set()
    for a in soup.find_all("a"):
        href = a.get("href")
        path = local_target(href)
        if path is None or path in checked:
            continue
        checked.add(path)
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Research Track local link escapes repository: {href}") from exc
        if not path.is_file():
            raise RuntimeError(f"Research Track local link target missing: {href}")

    if len(checked) < 4:
        raise RuntimeError(f"Research Track unexpectedly validates only {len(checked)} local link targets")

    print(
        f"Research Track seal PASS: {len(equations)} equations, "
        f"{len(checked)} local link targets, no forbidden visible residues."
    )


if __name__ == "__main__":
    main()
