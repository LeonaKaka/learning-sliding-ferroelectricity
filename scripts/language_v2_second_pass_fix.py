from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
import csv
import json
import struct

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-09.html"
PYTHON = ROOT / "examples/reproduction-lab/lesson09_beta_window.py"
RECEIPT = ROOT / "assets/reproduction-lab/lesson09_beta_window.txt"
CSV = ROOT / "assets/reproduction-lab/lesson09_beta_window.csv"
SOURCE_RECEIPT = ROOT / "assets/reproduction-lab/source-figure-receipt.json"
PAPER_FIG = ROOT / "assets/reproduction-lab/source-ferrero2013-pre-fig5-full.png"
PLOT_FILES = (
    ROOT / "assets/reproduction-lab/lesson09_mean_v_loglog.png",
    ROOT / "assets/reproduction-lab/lesson09_beta_vs_window.png",
    ROOT / "assets/reproduction-lab/lesson09_threshold_sensitivity.png",
    ROOT / "assets/reproduction-lab/lesson09_bootstrap_beta.png",
)
EXPECTED_SRCS = (
    "../assets/reproduction-lab/source-ferrero2013-pre-fig5-full.png",
    "../assets/reproduction-lab/lesson09_mean_v_loglog.png",
    "../assets/reproduction-lab/lesson09_beta_vs_window.png",
    "../assets/reproduction-lab/lesson09_threshold_sensitivity.png",
    "../assets/reproduction-lab/lesson09_bootstrap_beta.png",
)
EXPECTED_ALTS = (
    "Ferrero PRE 2013 图 5 完整原图区域",
    "无序平均速度随 Δf 的双对数图",
    "有效 β 随拟合区间上界变化",
    "β 对单样本阈值区间边缘的敏感性",
    "β 的样本自助法分布",
)
REQUIRED_VISIBLE = (
    "mesoscopic corrections（介观修正）",
    "effective exponent（有效指数）",
    "corrections-to-scaling（标度修正）",
    "asymptotic exponent（渐近指数）",
    "crossover（交叉）",
    "quenched disorder（淬火无序）",
    "bootstrap（自助法）",
    "最大 Δf",
    "有效 β",
    "自助法置信区间为什么也不能救",
    "拟合区间稳定性：未通过",
    "普适 β 结论：不授权",
    "0.267993",
    "0.229890",
    "0.195041",
    "0.165810",
    "0.102183",
    "0.030",
    "0.001004",
    "0.245",
)
FORBIDDEN_VISIBLE = (
    "max Δf", "βeff", "β_eff", "4 · bootstrap（自助法）",
    "β window audit", "disorder realizations", "post-hoc tuning", "effective slopes",
    "mean velocity", "β vs window", "authorization gate", "window drift", "panel (a)",
    "power-law guide", "registered window", "sample threshold", "central gate",
    "QEW benchmark", "bracket midpoint", "low/high edge", "all-six", "sample bootstrap",
    "current estimator", "asymptotic critical window", "Our simulation output",
    "Regression pipeline gold test PASS", "UNIVERSAL BETA CLAIM = NOT AUTHORIZED",
    "WINDOW-STABILITY GATE NOT PASSED", "run receipt",
)
PYTHON_LOCKS = (
    "SEEDS=np.arange(20260902,20260910,dtype=np.int64)",
    "L,M,DU,RF=32,256,0.25,1.0",
    "DT_THRESHOLD=0.05",
    "DT_VELOCITY=0.025",
    "DFS=np.array([0.015,0.025,0.040,0.065,0.105,0.170])",
    "WINDOW_MAX=np.array([0.170,0.105,0.065,0.040])",
    "WINDOW_DRIFT_GATE=0.030",
    "BOOTSTRAPS=10000",
    "assert particle_beta_err<0.005",
    "assert np.max(bracket_width)<2e-4",
    "window_pass=window_drift<WINDOW_DRIFT_GATE",
    "assert threshold_edge_span<0.005",
    "(out/'lesson09_beta_window.csv').write_text",
    "(out/'lesson09_beta_window.txt').write_text",
    "label='8 个独立无序样本的算术平均'",
    "ax.set_title('同一批数据：不同预登记拟合区间给出不同斜率')",
    "label='Ferrero QEW 文献基准 β≈0.245'",
    "ax.set_title('β 无稳定平台：缩窄拟合区间时指数持续漂移')",
    "ax.set_title('在单样本阈值区间内移动 fc 几乎不改变 β')",
    "ax.set_title('样本自助法分布较窄，但拟合区间稳定性仍未通过')",
)
RECEIPT_LOCKS = (
    "independent disorder n       = 8",
    "statistical unit             = disorder realization (not df points)",
    "seeds                        = 20260902..20260909",
    "line L, M, du, rf            = 32, 256, 0.250, 1.000",
    "threshold dt                 = 0.0500",
    "velocity dt                  = 0.0250",
    "steady protocol              = discard 1 u-period; measure next 3 periods",
    "delta-f ladder                = 0.015, 0.025, 0.040, 0.065, 0.105, 0.170",
    "particle beta windows         = 0.503850, 0.502473, 0.501617",
    "particle max |beta-0.5|       = 0.003850",
    "max threshold bracket width  = 0.000146484",
    "df=0.015 disorder-mean v     = 0.250404439",
    "df=0.025 disorder-mean v     = 0.268473880",
    "df=0.040 disorder-mean v     = 0.294751204",
    "df=0.065 disorder-mean v     = 0.333295069",
    "df=0.105 disorder-mean v     = 0.392643257",
    "df=0.170 disorder-mean v     = 0.482420250",
    "max df=0.170 beta             = 0.267993",
    "max df=0.105 beta             = 0.229890",
    "max df=0.065 beta             = 0.195041",
    "max df=0.040 beta             = 0.165810",
    "window beta drift            = 0.102183",
    "window drift gate            = < 0.030",
    "all-six beta                 = 0.267993",
    "sample bootstrap 95% CI      = [0.247165, 0.289579]",
    "bootstrap median             = 0.268270",
    "threshold-edge beta span     = 0.001004",
    "UNIVERSAL BETA CLAIM          = NOT AUTHORIZED",
    "WINDOW-STABILITY GATE         = NOT PASSED",
)
EXPECTED_THRESHOLDS = (
    ("20260902", "0.777636719", "0.777783203"),
    ("20260903", "0.811035156", "0.811181641"),
    ("20260904", "0.755371094", "0.755517578"),
    ("20260905", "0.800488281", "0.800634766"),
    ("20260906", "0.730908203", "0.731054687"),
    ("20260907", "0.777343750", "0.777490234"),
    ("20260908", "0.709521484", "0.709667969"),
    ("20260909", "0.799902344", "0.800048828"),
)
EXPECTED_MEAN_V = (
    0.250404439,
    0.268473880,
    0.294751204,
    0.333295069,
    0.392643257,
    0.482420250,
)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError(f"Lab 09 artifact is not canonical PNG: {path.relative_to(ROOT)}")
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
            raise RuntimeError(f"Lab 09 local link escapes repository: {value}") from exc
        if not resolved.exists():
            raise RuntimeError(f"Lab 09 broken local link: {value}")


def verify_source_provenance() -> None:
    data = json.loads(SOURCE_RECEIPT.read_text(encoding="utf-8"))
    if data.get("render_dpi", 0) < 500:
        raise RuntimeError("Lab 09 source-figure receipt render DPI drifted")
    matches = [x for x in data.get("figures", []) if x.get("file") == PAPER_FIG.name]
    if len(matches) != 1:
        raise RuntimeError("Lab 09 Ferrero Fig.5 provenance missing or duplicated")
    entry = matches[0]
    if entry.get("source_page") != 7 or entry.get("pixel_size") != [1867, 1966]:
        raise RuntimeError("Lab 09 Ferrero Fig.5 provenance dimensions/page drifted")
    if "Fig. 5" not in entry.get("citation", ""):
        raise RuntimeError("Lab 09 Ferrero Fig.5 citation identity drifted")
    if png_size(PAPER_FIG) != (1867, 1966):
        raise RuntimeError("Lab 09 Ferrero Fig.5 actual dimensions no longer match receipt")


def verify_csv() -> None:
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    velocity_keys = ["v_df_0.015", "v_df_0.025", "v_df_0.040", "v_df_0.065", "v_df_0.105", "v_df_0.170"]
    expected_header = ["seed", "fc_lo", "fc_hi", *velocity_keys]
    if not rows or list(rows[0].keys()) != expected_header:
        raise RuntimeError("Lab 09 CSV header drifted")
    if len(rows) != 8:
        raise RuntimeError(f"Lab 09 CSV must contain 8 independent disorder rows, found {len(rows)}")
    for row, expected in zip(rows, EXPECTED_THRESHOLDS):
        if (row["seed"], row["fc_lo"], row["fc_hi"]) != expected:
            raise RuntimeError(f"Lab 09 CSV threshold row drifted for expected seed {expected[0]}")
        for key in velocity_keys:
            if float(row[key]) <= 0:
                raise RuntimeError(f"Lab 09 non-positive velocity in CSV: seed={row['seed']} {key}")
    means = tuple(sum(float(row[key]) for row in rows) / len(rows) for key in velocity_keys)
    for got, expected in zip(means, EXPECTED_MEAN_V):
        if abs(got - expected) > 5e-10:
            raise RuntimeError(f"Lab 09 CSV ensemble mean drifted: {got:.9f} vs {expected:.9f}")


def main() -> None:
    for path in (TARGET, PYTHON, RECEIPT, CSV, SOURCE_RECEIPT, PAPER_FIG, *PLOT_FILES):
        if not path.exists():
            raise RuntimeError(f"Lab 09 required artifact missing: {path.relative_to(ROOT)}")

    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    if title != "Reproduction Lab（复现实验室）09 · β 拟合区间稳定性":
        raise RuntimeError(f"Lab 09 title drifted: {title!r}")

    visible = visible_text(soup)
    for token in REQUIRED_VISIBLE:
        if token not in visible:
            raise RuntimeError(f"Lab 09 required Language V2 text missing: {token}")
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f"Lab 09 ordinary workflow English remains visible: {token}")

    figures = soup.select("figure.figure img")
    if tuple(x.get("src") for x in figures) != EXPECTED_SRCS:
        raise RuntimeError("Lab 09 Figure wiring drifted")
    if tuple(x.get("alt") for x in figures) != EXPECTED_ALTS:
        raise RuntimeError("Lab 09 Figure alt text drifted")
    verify_local_links(soup)

    py = PYTHON.read_text(encoding="utf-8")
    for token in PYTHON_LOCKS:
        if token not in py:
            raise RuntimeError(f"Lab 09 Python contract drifted: {token}")

    receipt = RECEIPT.read_text(encoding="utf-8")
    for token in RECEIPT_LOCKS:
        if token not in receipt:
            raise RuntimeError(f"Lab 09 receipt/result/failure boundary drifted: {token}")

    verify_csv()
    verify_source_provenance()
    for plot in PLOT_FILES:
        w, h = png_size(plot)
        if w < 900 or h < 500:
            raise RuntimeError(f"Lab 09 code plot below evidence resolution contract: {plot.name} {w}x{h}")
        if plot.stat().st_size < 10_000:
            raise RuntimeError(f"Lab 09 code plot suspiciously small: {plot.name}")

    print("Lab 09 read-only Language V2 seal PASS; beta failure boundary/prose/results/provenance/Figures/links preserved.")


if __name__ == "__main__":
    main()
