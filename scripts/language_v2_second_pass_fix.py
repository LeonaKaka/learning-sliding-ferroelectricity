from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/research-track.html"

REQUIRED_VISIBLE = (
    "Research Track（研究路线）",
    "周期标量模型是教学 / 研究用有效模型",
    "RMS（均方根）",
    "Gaussian white random field（高斯白噪声随机场）",
    "stacking registry（堆垛配位）",
    "Langevin（朗之万）",
    "临近阈值 · 热圆整",
    "热圆整必须继承独立 T=0 阈值",
    "有效钉扎态直到 E",
    "迟发运动",
    "畴壁提取",
    "事件大小定义",
    "置信区间 / 自助法 / 模型的最外层重采样单元",
    "热噪声 / 事件 / 循环等内层重复",
    "跨翻转阶段一致的碎裂排序",
    "失效不是“没做成”",
    "候选普适类；或明确映射失效",
    "不展示项目未发表数值",
    "不能因为数值上“像一个阈值”就重命名成退钉扎临界场",
    "← 回到 07 数值建模",
)

FORBIDDEN_VISIBLE = (
    "periodic scalar model（周期标量模型）",
    "RMS、能量方差、局域力 RMS",
    "热圆滑",
    " up to E",
    "late 运动",
    "畴壁 extraction",
    "extraction 敏感性",
    "size 定义",
    "CI / 自助法",
    "cycle 等内层重复",
    "跨 stage",
    "Numerical 模型ing",
    "held-out",
    "sample-specific",
    "source-level",
    "checkpoint",
    "pipeline",
    "authority",
)

REQUIRED_RAW = (
    'F<sub>RF</sub> = −h(r) cos[φ−α(r)]',
    'F<sub>RB</sub> = δV(r)[1−cos(nφ)]',
    'v∼(E−E<sub>c</sub>)<sup>β</sup>',
    'v(f<sub>c</sub>,T)∼T<sup>ψ</sup>',
    'P(φ)=P<sub>0</sub> sinφ',
    'std(h<sub>cell</sub>)∝dx<sup>−d/2</sup>',
    'β<sub>eff</sub> 持续漂移',
    'id="roughness-gate-bridge"',
    'href="pinning-creep.html#roughness-gate"',
    'id="collapse-gate-bridge"',
    'href="depinning.html#collapse-gate"',
)

REQUIRED_HREFS = (
    "../index.html",
    "../index.html#map",
    "https://doi.org/10.1038/nmat2114",
    "https://doi.org/10.1103/PhysRevLett.103.157203",
    "pinning-creep.html#finite-temperature",
    "depinning.html#thermal-rounding",
    "numerical-modeling.html#thermal-noise",
    "numerical-modeling.html#identifiability",
    "pinning-creep.html#roughness-gate",
    "depinning.html#collapse-gate",
    "disorder-rfim.html#avalanche-statistics",
    "numerical-modeling.html#run-receipt",
    "numerical-modeling.html",
    "depinning.html",
)

EXPECTED_EQUATIONS = (
    "F RF = −h(r) cos[φ−α(r)]",
    "τ RF ∝ −h sin(φ−α)",
    "F RB = δV(r)[1−cos(nφ)]",
    "τ RB ∝ −nδV sin(nφ)",
    "P(φ)=P 0 sinφ",
    "F[φ]=∫d²r { κ/2 |∇φ|² + V 0 [1−cos(nφ)] − E P 0 sinφ + F dis [φ,r] }",
    "⟨h(r)h(r′)⟩=Δδ (d) (r−r′) ⇒ std(h cell )∝dx −d/2 二维网格单元平均白噪声无序：std ∝ 1/dx。该缩放只针对明确的 δ 相关连续场约定。",
    "Δ i = y A,i − y B,i ； Δ̄ = N −1 Σ i=1 N Δ i",
    "ȳ i,c = M i,c −1 Σ j y i,c,j ； Δ i = ȳ i,A − ȳ i,B",
)


def visible_text(soup: BeautifulSoup) -> str:
    clone = BeautifulSoup(str(soup), "html.parser")
    for node in clone.select("style, script"):
        node.decompose()
    return clone.get_text(" ", strip=True)


def verify_local_links(soup: BeautifulSoup) -> None:
    hrefs = [a.get("href") for a in soup.find_all("a") if a.get("href")]
    for required in REQUIRED_HREFS:
        if required not in hrefs:
            raise RuntimeError(f"Research Track required link missing: {required}")

    for value in hrefs:
        parts = urlsplit(value)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        resolved = (TARGET.parent / parts.path).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Research Track local link escapes repository: {value}") from exc
        if not resolved.exists():
            raise RuntimeError(f"Research Track broken local link: {value}")


def main() -> None:
    if not TARGET.exists():
        raise RuntimeError("Research Track page missing")

    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    if not soup.title or soup.title.get_text(" ", strip=True) != "Research Track（研究路线） · 无序 → Depinning（退钉扎） · Learning Sliding Ferroelectricity":
        raise RuntimeError("Research Track title drifted")

    meta = soup.find("meta", attrs={"name": "description"})
    if not meta or meta.get("content") != "从滑移铁电翻转、无序耦合到孤立畴壁退钉扎与普适性检验的研究路线。":
        raise RuntimeError("Research Track Chinese description drifted")

    visible = visible_text(soup)
    for token in REQUIRED_VISIBLE:
        if token not in visible:
            raise RuntimeError(f"Research Track required Language V2 text missing: {token}")
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f"Research Track ordinary workflow English remains visible: {token}")

    for token in REQUIRED_RAW:
        if token not in raw:
            raise RuntimeError(f"Research Track scientific/link contract drifted: {token}")

    equations = tuple(x.get_text(" ", strip=True) for x in soup.select(".eq"))
    for expected in EXPECTED_EQUATIONS:
        if expected not in equations:
            raise RuntimeError(f"Research Track equation drifted: {expected}")

    # Claim-boundary locks: this page defines a research contract, not unpublished results.
    claim_locks = (
        "目标不是预设“必然普适”",
        "它不等于说模型已经变成 RFIM",
        "beta",  # intentionally absent below; this placeholder is not checked directly
    )
    if claim_locks[0] not in visible or claim_locks[1] not in visible:
        raise RuntimeError("Research Track universality/model-boundary wording drifted")
    if "候选退钉扎临界区间" not in visible or "候选普适类；或明确映射失效" not in visible:
        raise RuntimeError("Research Track evidence ladder was overclaimed")
    if "不展示项目未发表数值、内部批次标签或当前判据状态" not in visible:
        raise RuntimeError("Research Track public/unpublished boundary drifted")

    verify_local_links(soup)
    print("Research Track read-only Language V2 seal PASS; prose, equations, links, hierarchy and non-overclaim boundaries preserved.")


if __name__ == "__main__":
    main()
