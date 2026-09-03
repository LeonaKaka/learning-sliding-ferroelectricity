from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OVERVIEW = ROOT / "modules" / "reproduction-lab-overview.html"
NAV = ROOT / "site-nav.js"
MODULE07 = ROOT / "modules" / "numerical-modeling.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    raw = OVERVIEW.read_text(encoding="utf-8")
    doc = BeautifulSoup(raw, "html.parser")

    require(doc.title is not None and "12 课学习路线" in doc.title.get_text(),
            "Reproduction Lab overview title drifted")
    require(len(doc.select("section.stage")) == 3,
            "Reproduction Lab overview must keep exactly three evidence stages")
    for stage_id in ("stage-a", "stage-b", "stage-c"):
        require(doc.find(id=stage_id) is not None, f"Missing Lab stage: {stage_id}")

    lesson_links = [a.get("href") for a in doc.select("a.lesson")]
    expected = ["reproduction-lab.html"] + [f"reproduction-lab-{i:02d}.html" for i in range(2, 13)]
    require(lesson_links == expected,
            f"Lab overview lesson order/links drifted: {lesson_links}")
    for href in lesson_links:
        require((OVERVIEW.parent / href).exists(), f"Lab lesson target missing: {href}")

    locked = (
        "已知答案测试通过 ≠ 目标物理结论通过",
        "单样本结果 ≠ 热力学极限",
        "一条漂亮幂律 ≠ 普适指数",
        "Stage A · L01–L05",
        "Stage B · L06–L08",
        "Stage C · L09–L12",
        "低温映射通过；高温 breakdown 被检测到，不能把失效润色成成功",
        "几何映射通过；渐近 ζ 判据未通过",
        "只授权有限样本阈值区间；不授权热力学 f<sub>c</sub>",
        "稳态速度估计量通过；本课明确不拟合 β",
        "β 拟合区间判据未通过，普适 β 不授权",
        "超粗糙特征可见；热力学 ζ 尚未闭合",
        "尺寸区间稳定性未通过，普适 ν 不授权",
        "热圆整区间未闭合，ψ 与 creep-law / μ 均不授权",
        "论文线可以换，证据纪律不能换",
    )
    for text in locked:
        require(text in raw, f"Lab overview scientific boundary drifted: {text}")

    nav = NAV.read_text(encoding="utf-8")
    require("modules/reproduction-lab-overview.html" in nav,
            "Global navigation no longer routes to Lab overview")
    require("12 课学习路线 →" in nav,
            "Global Lab overview label missing")
    require("['L01 · TDGL wall','modules/reproduction-lab.html']" in nav,
            "L01 canonical lesson URL changed unexpectedly")
    require("labs.slice(0,6)" in nav and "labs.slice(6)" in nav,
            "Paper1/Paper2 sidebar grouping drifted")

    # Homepage must present one role-based chooser instead of pushing an advanced
    # route as the default first action.
    chooser_locked = (
        "section.id='learning-mode-entry'",
        "先选你现在要解决的问题",
        "第一次系统学",
        "某个概念反复卡住",
        "想把数值规则真正跑成代码",
        "准备把知识接成研究问题",
        "从 01–08 建立完整物理主线",
        "先掌握 03–07，再进入无序、孤立畴壁与证据链设计",
        "href=\"#map\"",
        "href=\"#concept-paths\"",
        "href=\"modules/reproduction-lab-overview.html\"",
        "href=\"modules/research-track.html\"",
    )
    for text in chooser_locked:
        require(text in nav, f"Homepage learning-mode chooser drifted: {text}")
    require("reproduction-lab-entry" not in nav,
            "Legacy Lab-only homepage entry reappeared")

    # Module 07 is a semantic Lab entry point, not an L01-specific lesson link.
    m7_raw = MODULE07.read_text(encoding="utf-8")
    m7 = BeautifulSoup(m7_raw, "html.parser")
    bridge = m7.select_one("#reproduction-lab-bridge")
    require(bridge is not None, "Module 07 Reproduction Lab bridge missing")
    lab_links = [a for a in bridge.find_all("a") if "Reproduction Lab" in a.get_text(" ", strip=True)]
    require(len(lab_links) == 1, f"Module 07 expected one Lab entry link, found {len(lab_links)}")
    require(lab_links[0].get("href") == "reproduction-lab-overview.html",
            f"Module 07 Lab entry must route to overview, got {lab_links[0].get('href')}")
    require('<a href="reproduction-lab.html">Reproduction Lab</a>' not in m7_raw,
            "Legacy Module 07 Lab entry still routes directly to L01")

    print(
        "REPRODUCTION LAB OVERVIEW SEAL PASS: 12 canonical lesson links, three evidence stages, "
        "critical claim boundaries, global/homepage routing, and Module 07 overview entry are locked."
    )


if __name__ == "__main__":
    main()
