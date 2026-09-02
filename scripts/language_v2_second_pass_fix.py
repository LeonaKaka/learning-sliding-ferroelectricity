from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
import json
import re
import struct

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-07.html"
PYTHON = ROOT / "examples/reproduction-lab/lesson07_threshold_search.py"
RECEIPT = ROOT / "assets/reproduction-lab/lesson07_threshold_search.txt"
SOURCE_RECEIPT = ROOT / "assets/reproduction-lab/source-figure-receipt.json"
PAPER_FIG = ROOT / "assets/reproduction-lab/source-ferrero2013-pre-fig3-full.png"
PLOT_FILES = (
    ROOT / "assets/reproduction-lab/lesson07_bisection.png",
    ROOT / "assets/reproduction-lab/lesson07_last_pinned_profile.png",
    ROOT / "assets/reproduction-lab/lesson07_particle_gold.png",
    ROOT / "assets/reproduction-lab/lesson07_dt_threshold.png",
)

LOCKED_RESULTS = (
    "[0.777636719, 0.777783203]",
    "1.465×10<sup>−4</sup>",
    "f<sub>c</sub> = 1",
    "0.7777",
    "1.916",
)
MACHINE_MARKER = "THRESHOLD GOLD TEST + SMALL-LINE BRACKET PASS"
EXPECTED_SRCS = (
    "../assets/reproduction-lab/source-ferrero2013-pre-fig3-full.png",
    "../assets/reproduction-lab/lesson07_bisection.png",
    "../assets/reproduction-lab/lesson07_last_pinned_profile.png",
    "../assets/reproduction-lab/lesson07_particle_gold.png",
    "../assets/reproduction-lab/lesson07_dt_threshold.png",
)
EXPECTED_ALTS = (
    "Ferrero PRE 2013 图 3 完整原图区域",
    "单个无序样本的阈值二分历史",
    "最终阈值区间下沿的 QEW 钉扎畴壁剖面",
    "解析阈值已知答案测试",
    "阈值区间随积分步长的稳定性",
)
REQUIRED_VISIBLE = (
    "quenched disorder（淬火无序）",
    "thermodynamic critical force（热力学临界力）",
    "depinning（退钉扎）",
    "quenched disorder landscape（淬火无序势景观）",
    "elastic line（弹性界面）",
    "tilted washboard（倾斜搓衣板势）",
    "这里没有得到热力学极限",
    "阈值已知答案测试 + 小尺寸界面阈值区间：通过",
    "L=32，随机种子=20260902",
)
FORBIDDEN_VISIBLE = (
    "panel (a)", "seed=20260902", "exact metastable-state algorithm",
    "threshold classifier", "sample-specific threshold", "last pinned", "first moving",
    "run receipt", "Code gold test", "Our simulation output",
)
PYTHON_LOCKS = (
    "SEED = 20260902",
    "def particle_threshold(dt=0.02, lo=0.7, hi=1.25, n_iter=14):",
    "def relax_line(f, table, du, c=1.0, dt=0.05, max_steps=500_000,",
    "def line_threshold(table, du, dt=0.05, lo=0.4, hi=1.0, n_iter=12):",
    "L, M, du, rf = 32, 256, 0.25, 1.0",
    "for dt in (0.10, 0.05, 0.025):",
    "assert particle_err < 5e-5, particle_err",
    "assert particle_width < 5e-5, particle_width",
    "assert line_width < 2e-4, line_width",
    "assert line_spread < 5e-4, line_spread",
    "assert all(v[0] < v[1] for v in line_runs.values())",
    "receipt_out.write_text(\"\\n\".join(receipt_lines) + \"\\n\", encoding=\"utf-8\")",
    "ax.set_title(f'最后一个钉扎构型：f={lo_line:.6f}（一个无序样本）')",
    "ax.set_title('单个淬火无序弹性界面的阈值搜索')",
    "ax.set_title('减小 dt 后单样本阈值区间保持不变')",
    "ax.set_title('已知答案测试：数值阈值围绕解析 fc=1')",
)
RECEIPT_LINE_LOCKS = (
    "line L, M, du, rf           = 32, 256, 0.250, 1.000",
    "line dt=0.100 bracket       = [0.777636719, 0.777783203]",
    "line dt=0.050 bracket       = [0.777636719, 0.777783203]",
    "line dt=0.025 bracket       = [0.777636719, 0.777783203]",
    "line fc midpoint (dt=.05)   = 0.777709961",
    "line dt-spread              = 0.000e+00",
    "line final bracket width    = 1.465e-04",
    MACHINE_MARKER,
)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError(f"Lab 07 artifact is not canonical PNG: {path.relative_to(ROOT)}")
    return struct.unpack(">II", data[16:24])


def visible_text(soup: BeautifulSoup) -> str:
    clone = BeautifulSoup(str(soup), "html.parser")
    for node in clone.select("style, script, pre, code, .eq"):
        node.decompose()
    return clone.get_text(" ", strip=True)


def verify_local_links(soup: BeautifulSoup) -> None:
    for tag in soup.find_all(["a", "img"]):
        value = tag.get("href") if tag.name == "a" else tag.get("src")
        if not value:
            continue
        parts = urlsplit(value)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        resolved = (TARGET.parent / parts.path).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Lab 07 local link escapes repository: {value}") from exc
        if not resolved.exists():
            raise RuntimeError(f"Lab 07 broken local link: {value}")


def verify_particle_gold(receipt: str) -> None:
    if "particle exact fc           = 1.000000000" not in receipt:
        raise RuntimeError("Lab 07 analytic particle threshold marker missing")
    particle = re.findall(
        r"particle dt=(0\.040|0\.020|0\.010) bracket\s+= \[([0-9.]+), ([0-9.]+)\]",
        receipt,
    )
    if len(particle) != 3:
        raise RuntimeError(f"Lab 07 expected 3 particle brackets, found {len(particle)}")
    for dt, slo, shi in particle:
        lo, hi = float(slo), float(shi)
        if not (lo < 1.0 < hi):
            raise RuntimeError(f"Lab 07 particle dt={dt} bracket does not cover exact fc=1")
        if hi - lo >= 5e-5:
            raise RuntimeError(f"Lab 07 particle dt={dt} bracket width gate failed")
    match = re.search(r"particle max \|fc-1\|\s+= ([0-9.eE+-]+)", receipt)
    if not match or float(match.group(1)) >= 5e-5:
        raise RuntimeError("Lab 07 particle gold-test error gate failed")


def verify_source_provenance() -> None:
    data = json.loads(SOURCE_RECEIPT.read_text(encoding="utf-8"))
    if data.get("render_dpi", 0) < 500:
        raise RuntimeError("Lab 07 source-figure receipt render DPI drifted")
    matches = [x for x in data.get("figures", []) if x.get("file") == PAPER_FIG.name]
    if len(matches) != 1:
        raise RuntimeError("Lab 07 Ferrero Fig.3 provenance entry missing or duplicated")
    entry = matches[0]
    if entry.get("source_page") != 6:
        raise RuntimeError("Lab 07 Ferrero Fig.3 source page drifted")
    if entry.get("pixel_size") != [1784, 2666]:
        raise RuntimeError("Lab 07 Ferrero Fig.3 receipt dimensions drifted")
    if "Fig. 3" not in entry.get("citation", ""):
        raise RuntimeError("Lab 07 Ferrero Fig.3 citation identity drifted")
    if png_size(PAPER_FIG) != (1784, 2666):
        raise RuntimeError("Lab 07 Ferrero Fig.3 file dimensions no longer match receipt")


def main() -> None:
    required_files = (TARGET, PYTHON, RECEIPT, SOURCE_RECEIPT, PAPER_FIG, *PLOT_FILES)
    for path in required_files:
        if not path.exists():
            raise RuntimeError(f"Lab 07 required artifact missing: {path.relative_to(ROOT)}")

    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    if title != "Reproduction Lab（复现实验室）07 · 退钉扎阈值搜索":
        raise RuntimeError(f"Lab 07 title drifted: {title!r}")

    visible = visible_text(soup)
    for token in REQUIRED_VISIBLE:
        if token not in visible:
            raise RuntimeError(f"Lab 07 required Language V2 text missing: {token}")
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f"Lab 07 ordinary workflow English remains visible: {token}")
    for token in LOCKED_RESULTS:
        if token not in raw:
            raise RuntimeError(f"Lab 07 locked result missing: {token}")

    equations = soup.select(".eq")
    if len(equations) != 1:
        raise RuntimeError(f"Lab 07 expected 1 equation block, found {len(equations)}")
    if "du/dt = f − sin u" not in equations[0].get_text(" ", strip=True):
        raise RuntimeError("Lab 07 analytic gold-test equation changed")

    figures = soup.select("figure.figure img")
    if tuple(x.get("src") for x in figures) != EXPECTED_SRCS:
        raise RuntimeError("Lab 07 Figure wiring drifted")
    if tuple(x.get("alt") for x in figures) != EXPECTED_ALTS:
        raise RuntimeError("Lab 07 Figure alt text drifted")
    verify_local_links(soup)

    py = PYTHON.read_text(encoding="utf-8")
    for token in PYTHON_LOCKS:
        if token not in py:
            raise RuntimeError(f"Lab 07 Python contract drifted: {token}")

    receipt = RECEIPT.read_text(encoding="utf-8")
    verify_particle_gold(receipt)
    for token in RECEIPT_LINE_LOCKS:
        if token not in receipt:
            raise RuntimeError(f"Lab 07 receipt/QEW result drifted: {token}")

    verify_source_provenance()
    for plot in PLOT_FILES:
        w, h = png_size(plot)
        if w < 900 or h < 500:
            raise RuntimeError(f"Lab 07 code plot below evidence resolution contract: {plot.name} {w}x{h}")
        if plot.stat().st_size < 10_000:
            raise RuntimeError(f"Lab 07 code plot suspiciously small: {plot.name}")

    print("Lab 07 read-only Language V2 seal PASS; prose/science/results/provenance/Figures/links preserved.")


if __name__ == "__main__":
    main()
