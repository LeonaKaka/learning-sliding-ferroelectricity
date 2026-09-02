from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
import json
import struct

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-08.html"
PYTHON = ROOT / "examples/reproduction-lab/lesson08_steady_velocity.py"
RECEIPT = ROOT / "assets/reproduction-lab/lesson08_steady_velocity.txt"
SOURCE_RECEIPT = ROOT / "assets/reproduction-lab/source-figure-receipt.json"
PAPER_FIG = ROOT / "assets/reproduction-lab/source-ferrero2013-review-fig1-full.png"
PLOT_FILES = (
    ROOT / "assets/reproduction-lab/lesson08_vf.png",
    ROOT / "assets/reproduction-lab/lesson08_transient_periods.png",
    ROOT / "assets/reproduction-lab/lesson08_dt_error.png",
    ROOT / "assets/reproduction-lab/lesson08_particle_velocity_gold.png",
)

EXPECTED_SRCS = (
    "../assets/reproduction-lab/source-ferrero2013-review-fig1-full.png",
    "../assets/reproduction-lab/lesson08_vf.png",
    "../assets/reproduction-lab/lesson08_transient_periods.png",
    "../assets/reproduction-lab/lesson08_dt_error.png",
    "../assets/reproduction-lab/lesson08_particle_velocity_gold.png",
)
EXPECTED_ALTS = (
    "Ferrero 2013 综述图 1 完整原图区域",
    "模拟得到的稳态速度随驱动力变化",
    "逐个无序周期的平均速度",
    "速度相对误差随积分步长变化",
    "速度估计量的解析已知答案测试",
)
REQUIRED_VISIBLE = (
    "steady velocity（稳态速度）",
    "center-of-mass velocity（质心速度）",
    "depinning（退钉扎）",
    "thermal rounding（热圆整）",
    "creep（蠕变）",
    "fast flow（快速流动）",
    "稳态速度估计量 + dt 收敛：通过",
    "本课不拟合 β",
    "3.47%–4.93%",
    "0.0010%",
    "0.001387%",
    "0.5%",
    "dt=.1 未通过",
    "dt=.025 通过",
)
FORBIDDEN_VISIBLE = (
    "transient removal", "dt convergence", "production dt", "reference dt",
    "measurement window", "run receipt", "Our simulation output", "Code gold test",
    "sample threshold", "critical-window audit", "velocity error", "normalization",
    "observable", "NO BETA FIT IN LESSON 08", "STEADY VELOCITY ESTIMATOR + DT CONVERGENCE PASS",
)
PYTHON_LOCKS = (
    "SEED=20260902",
    "FC_LO,FC_HI=0.77763671875,0.777783203125",
    "DT_GATE=5e-3",
    "def particle_v(f,dt=.02,warm=2,measure=4):",
    "def line_v(f,T,du,u0,dt,warm=1,measure=3):",
    "p_err=max(x[3] for x in particle); assert p_err<2e-5",
    "assert abs(lo-FC_LO)<1e-12 and abs(hi-FC_HI)<1e-12",
    "dfs=np.array([.02,.04,.08,.16])",
    "dts=(.1,.05,.025,.0125)",
    "assert coarse>DT_GATE and prod<DT_GATE and station<5e-4",
    "(out/'lesson08_steady_velocity.txt').write_text('\\n'.join(R)+'\\n')",
    "label='正式计算 dt=0.025'",
    "label='参考 dt=0.0125'",
    "label='L07 阈值区间中点'",
    "ax.set_title('只在单样本阈值上方测量稳态 v(f)')",
    "ax.set_title('第 1 个周期仍含退钉扎瞬态')",
    "label='预设 0.5% 判据'",
    "ax.set_title('速度估计量的 dt 收敛')",
    "ax.set_title('运动态速度估计量的已知答案测试')",
)
RECEIPT_LOCKS = (
    "registered fc bracket        = [0.777636719, 0.777783203]",
    "registered fc midpoint       = 0.777709961",
    "velocity dt gate             = 0.500%",
    "particle max rel error       = 0.001387%",
    "line L, M, du, rf            = 32, 256, 0.250, 1.000",
    "line delta-f ladder          = 0.02, 0.04, 0.08, 0.16",
    "steady protocol             = discard 1 u-period; measure next 3 periods",
    "coarse dt=.100 max error     = 1.010%  FAIL (<0.5% gate)",
    "dt=.050 max error            = 0.439%",
    "production dt=.025 max err  = 0.147%  PASS",
    "reference dt=.0125           = comparison authority for this lesson",
    "first-period transient shift = 3.47% .. 4.93%",
    "steady 3-period spread max   = 0.0010%",
    "df=0.020 f=0.797709961 v(dt=.025)=0.304157138 v(dt=.0125)=0.304576417",
    "df=0.040 f=0.817709961 v(dt=.025)=0.336752820 v(dt=.0125)=0.337223824",
    "df=0.080 f=0.857709961 v(dt=.025)=0.390721774 v(dt=.0125)=0.391295561",
    "df=0.160 f=0.937709961 v(dt=.025)=0.492101344 v(dt=.0125)=0.492828001",
    "NO BETA FIT IN LESSON 08",
    "STEADY VELOCITY ESTIMATOR + DT CONVERGENCE PASS",
)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError(f"Lab 08 artifact is not canonical PNG: {path.relative_to(ROOT)}")
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
            raise RuntimeError(f"Lab 08 local link escapes repository: {value}") from exc
        if not resolved.exists():
            raise RuntimeError(f"Lab 08 broken local link: {value}")


def verify_source_provenance() -> None:
    data = json.loads(SOURCE_RECEIPT.read_text(encoding="utf-8"))
    if data.get("render_dpi", 0) < 500:
        raise RuntimeError("Lab 08 source-figure receipt render DPI drifted")
    matches = [x for x in data.get("figures", []) if x.get("file") == PAPER_FIG.name]
    if len(matches) != 1:
        raise RuntimeError("Lab 08 Ferrero review Fig.1 provenance missing or duplicated")
    entry = matches[0]
    if entry.get("source_page") != 3:
        raise RuntimeError("Lab 08 Ferrero review Fig.1 source page drifted")
    if entry.get("pixel_size") != [3250, 2550]:
        raise RuntimeError("Lab 08 Ferrero review Fig.1 receipt dimensions drifted")
    if "Fig. 1" not in entry.get("citation", ""):
        raise RuntimeError("Lab 08 Ferrero review Fig.1 citation identity drifted")
    if png_size(PAPER_FIG) != (3250, 2550):
        raise RuntimeError("Lab 08 Ferrero review Fig.1 file dimensions no longer match receipt")


def main() -> None:
    for path in (TARGET, PYTHON, RECEIPT, SOURCE_RECEIPT, PAPER_FIG, *PLOT_FILES):
        if not path.exists():
            raise RuntimeError(f"Lab 08 required artifact missing: {path.relative_to(ROOT)}")

    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    if title != "Reproduction Lab（复现实验室）08 · 稳态速度":
        raise RuntimeError(f"Lab 08 title drifted: {title!r}")

    visible = visible_text(soup)
    for token in REQUIRED_VISIBLE:
        if token not in visible:
            raise RuntimeError(f"Lab 08 required Language V2 text missing: {token}")
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f"Lab 08 ordinary workflow English remains visible: {token}")

    figures = soup.select("figure.figure img")
    if tuple(x.get("src") for x in figures) != EXPECTED_SRCS:
        raise RuntimeError("Lab 08 Figure wiring drifted")
    if tuple(x.get("alt") for x in figures) != EXPECTED_ALTS:
        raise RuntimeError("Lab 08 Figure alt text drifted")
    verify_local_links(soup)

    py = PYTHON.read_text(encoding="utf-8")
    for token in PYTHON_LOCKS:
        if token not in py:
            raise RuntimeError(f"Lab 08 Python contract drifted: {token}")

    receipt = RECEIPT.read_text(encoding="utf-8")
    for token in RECEIPT_LOCKS:
        if token not in receipt:
            raise RuntimeError(f"Lab 08 receipt/result drifted: {token}")

    verify_source_provenance()
    for plot in PLOT_FILES:
        w, h = png_size(plot)
        if w < 900 or h < 500:
            raise RuntimeError(f"Lab 08 code plot below evidence resolution contract: {plot.name} {w}x{h}")
        if plot.stat().st_size < 10_000:
            raise RuntimeError(f"Lab 08 code plot suspiciously small: {plot.name}")

    print("Lab 08 read-only Language V2 seal PASS; prose/science/results/provenance/Figures/links preserved.")


if __name__ == "__main__":
    main()
