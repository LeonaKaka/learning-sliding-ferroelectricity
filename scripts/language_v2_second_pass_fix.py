from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
import csv
import json
import math
import re
import struct

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-10.html"
PYTHON = ROOT / "examples/reproduction-lab/lesson10_superrough_zeta.py"
RECEIPT = ROOT / "assets/reproduction-lab/lesson10_superrough_zeta.txt"
SAMPLE_CSV = ROOT / "assets/reproduction-lab/lesson10_superrough_zeta.csv"
CURVES_CSV = ROOT / "assets/reproduction-lab/lesson10_geometry_curves.csv"
SOURCE_RECEIPT = ROOT / "assets/reproduction-lab/source-figure-receipt.json"
PAPER_FIG = ROOT / "assets/reproduction-lab/source-ferrero2013-pre-fig1-full.png"
PLOT_FILES = (
    ROOT / "assets/reproduction-lab/lesson10_profiles.png",
    ROOT / "assets/reproduction-lab/lesson10_Sq.png",
    ROOT / "assets/reproduction-lab/lesson10_Br.png",
    ROOT / "assets/reproduction-lab/lesson10_zeta_vs_size.png",
)
EXPECTED_SRCS = (
    "../assets/reproduction-lab/lesson10_profiles.png",
    "../assets/reproduction-lab/source-ferrero2013-pre-fig1-full.png",
    "../assets/reproduction-lab/lesson10_Sq.png",
    "../assets/reproduction-lab/lesson10_Br.png",
    "../assets/reproduction-lab/lesson10_zeta_vs_size.png",
)
EXPECTED_ALTS = (
    "L=128 与 L=256 的最后钉扎 QEW 界面形貌",
    "Ferrero PRE 2013 图 1 完整原图区域",
    "L=128 与 L=256 的模拟结构因子 S(q)",
    "L=128 与 L=256 的局域粗糙度 B(r)",
    "有效粗糙度指数随系统尺寸变化及样本自助法区间",
)
REQUIRED_VISIBLE = (
    "structure factor（结构因子）",
    "super-rough（超粗糙）",
    "quenched disorder（淬火无序）",
    "Fourier space（傅里叶空间）",
    "已知答案测试通过",
    "小尺寸 QEW 超粗糙特征：通过",
    "热力学 ζ 闭合：未通过",
    "1.315621",
    "1.201060",
    "[1.060960, 1.480197]",
    "[1.016524, 1.431058]",
    "0.114561",
    "0.10 判据",
    "不能挑出 1.316 或 1.201 中的任何一个",
)
FORBIDDEN_VISIBLE = (
    "Lesson 10",
    "Paper2 Method Track",
    "真实 simulation plot",
    "last-pinned wall profile",
    "fit window",
    "size dependence",
    "simulation 里真正的 wall",
    "independent quenched-disorder samples",
    "last-pinned configuration",
    "center of mass",
    "Our simulation output",
    "threshold search",
    "global roughness",
    "original caption",
    "discretization effects",
    "observable-level",
    "exact critical configuration",
    "direct-relaxation last-pinned sample",
    "scaling form",
    "effective slope",
    "real-space height-difference correlation",
    "another estimator",
    "synthetic Fourier interface",
    "same pipeline",
    "gold test PASS",
    "central estimate",
    "SMALL-QEW SUPER-ROUGH SIGNATURE = PASS",
    "THERMODYNAMIC ZETA CLOSURE = NOT PASSED",
    "pre-registered 0.10 gate",
    "run receipt",
    "realization table",
    "plotted curves CSV",
    "论文截图 receipt",
    "structure factor（结构因子）（结构因子）",
    "quenched disorder（淬火无序）（淬火无序）",
)
PYTHON_LOCKS = (
    "DU=0.25; DT=0.05; RF=1.0; THRESH_ITERS=10; TOL=2e-7; MAX_STEPS=400_000",
    "REALIZATIONS=6; BOOTSTRAPS=1000; SYNTH_ZETA=1.25",
    "assert abs(synth_zS-SYNTH_ZETA)<.05 and .85<synth_zB<1.05 and synth_zS-synth_zB>.15",
    "cert_spread=max(r[-1] for r in cert); assert cert_spread<5e-4",
    "r128=qew_ensemble(128,2048,20269128); r256=qew_ensemble(256,4096,20269256)",
    "assert r['span_max']<.35 and .85<r['zB']<1.05 and r['zS']>1.00 and r['zS']-r['zB']>.08",
    "global_drift=abs(r128['zS']-r256['zS']); local_drift=abs(r128['zB']-r256['zB']); THERMO_GATE=.10; thermo_pass=global_drift<THERMO_GATE",
    "'SMALL-QEW SUPER-ROUGH SIGNATURE = PASS'",
    "f\"THERMODYNAMIC ZETA CLOSURE   = {'PASS' if thermo_pass else 'NOT PASSED'}\"",
    "'FINITE-SIZE SCALING REQUIRED BEFORE UNIVERSAL ZETA CLAIM'",
    "(out/'lesson10_superrough_zeta.txt').write_text",
    "out/'lesson10_superrough_zeta.csv'",
    "finish(fig,'lesson10_profiles.png')",
    "finish(fig,'lesson10_Br.png')",
    "finish(fig,'lesson10_Sq.png')",
    "finish(fig,'lesson10_zeta_vs_size.png')",
)
RECEIPT_LOCKS = (
    "synthetic target zeta_global = 1.250000",
    "synthetic zeta_B local       = 0.951442",
    "synthetic zeta_S global      = 1.223335",
    "SYNTHETIC SUPER-ROUGH GOLD TEST = PASS",
    "moving-cert midpoint spread = 0.000000e+00",
    "moving certificate          = 1 period validated against 2 periods on 2 realizations",
    "L=128 M=2048 realizations       = 6",
    "L=128 zeta_B local                  = 0.928961",
    "L=128 zeta_B realization-bootstrap 95% = [0.910299, 0.944262]",
    "L=128 zeta_S global                 = 1.315621",
    "L=128 zeta_S realization-bootstrap 95% = [1.060960, 1.480197]",
    "L=128 max wall-span / u-period      = 0.199629",
    "L=256 M=4096 realizations       = 6",
    "L=256 zeta_B local                  = 0.949576",
    "L=256 zeta_B realization-bootstrap 95% = [0.916449, 0.966650]",
    "L=256 zeta_S global                 = 1.201060",
    "L=256 zeta_S realization-bootstrap 95% = [1.016524, 1.431058]",
    "L=256 max wall-span / u-period      = 0.283296",
    "cross-size zeta_B drift      = 0.020615",
    "cross-size zeta_S drift      = 0.114561",
    "thermodynamic zeta drift gate = < 0.100",
    "SMALL-QEW SUPER-ROUGH SIGNATURE = PASS",
    "THERMODYNAMIC ZETA CLOSURE   = NOT PASSED",
    "FINITE-SIZE SCALING REQUIRED BEFORE UNIVERSAL ZETA CLAIM",
)
EXPECTED_SAMPLE_GROUPS = {
    128: (2048, tuple(range(20269128, 20269134)), 0.19962895694449667),
    256: (4096, tuple(range(20269256, 20269262)), 0.28329573190874063),
}
EXPECTED_ZETA = {
    128: (0.928961, 1.315621),
    256: (0.949576, 1.201060),
}


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError(f"Lab 10 artifact is not canonical PNG: {path.relative_to(ROOT)}")
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
            raise RuntimeError(f"Lab 10 local link escapes repository: {value}") from exc
        if not resolved.exists():
            raise RuntimeError(f"Lab 10 broken local link: {value}")


def verify_source_provenance() -> None:
    data = json.loads(SOURCE_RECEIPT.read_text(encoding="utf-8"))
    if data.get("render_dpi", 0) < 500:
        raise RuntimeError("Lab 10 source-figure receipt render DPI drifted")
    matches = [x for x in data.get("figures", []) if x.get("file") == PAPER_FIG.name]
    if len(matches) != 1:
        raise RuntimeError("Lab 10 Ferrero Fig.1 provenance missing or duplicated")
    entry = matches[0]
    if entry.get("source_page") != 5 or entry.get("pixel_size") != [1800, 1684]:
        raise RuntimeError("Lab 10 Ferrero Fig.1 provenance dimensions/page drifted")
    if "Fig. 1" not in entry.get("citation", ""):
        raise RuntimeError("Lab 10 Ferrero Fig.1 citation identity drifted")
    if png_size(PAPER_FIG) != (1800, 1684):
        raise RuntimeError("Lab 10 Ferrero Fig.1 actual dimensions no longer match receipt")


def verify_sample_csv() -> None:
    with SAMPLE_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected_header = ["L", "M", "seed", "fc_lo", "fc_hi", "fc_mid", "wall_span_over_period"]
    if not rows or list(rows[0].keys()) != expected_header:
        raise RuntimeError("Lab 10 sample CSV header drifted")
    if len(rows) != 12:
        raise RuntimeError(f"Lab 10 sample CSV must contain 12 independent disorder rows, found {len(rows)}")
    for L, (M, seeds, expected_max_span) in EXPECTED_SAMPLE_GROUPS.items():
        group = [row for row in rows if int(row["L"]) == L]
        if len(group) != 6:
            raise RuntimeError(f"Lab 10 L={L} must contain 6 disorder rows")
        if tuple(int(row["seed"]) for row in group) != seeds:
            raise RuntimeError(f"Lab 10 L={L} seed identities drifted")
        if any(int(row["M"]) != M for row in group):
            raise RuntimeError(f"Lab 10 L={L} M drifted")
        spans = []
        for row in group:
            lo, hi, mid = map(float, (row["fc_lo"], row["fc_hi"], row["fc_mid"]))
            if not (lo < mid < hi and abs(mid - 0.5 * (lo + hi)) < 1e-12):
                raise RuntimeError(f"Lab 10 malformed fc bracket for seed {row['seed']}")
            if abs((hi - lo) - 0.0009765625) > 1e-12:
                raise RuntimeError(f"Lab 10 threshold bracket width drifted for seed {row['seed']}")
            span = float(row["wall_span_over_period"])
            if not (0 < span < 0.35):
                raise RuntimeError(f"Lab 10 wall span contract failed for seed {row['seed']}")
            spans.append(span)
        if abs(max(spans) - expected_max_span) > 1e-12:
            raise RuntimeError(f"Lab 10 L={L} max wall span drifted")


def linear_slope(points: list[tuple[float, float]]) -> float:
    xs = [math.log(x) for x, _ in points]
    ys = [math.log(y) for _, y in points]
    xm = sum(xs) / len(xs)
    ym = sum(ys) / len(ys)
    den = sum((x - xm) ** 2 for x in xs)
    if den <= 0:
        raise RuntimeError("Lab 10 degenerate log-fit window")
    return sum((x - xm) * (y - ym) for x, y in zip(xs, ys)) / den


def verify_curve_csv() -> None:
    with CURVES_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected_header = ["L", "observable", "x", "mean_value", "fit_window"]
    if not rows or list(rows[0].keys()) != expected_header:
        raise RuntimeError("Lab 10 curve CSV header drifted")
    for L, (expected_zB, expected_zS) in EXPECTED_ZETA.items():
        bfit = [(float(r["x"]), float(r["mean_value"])) for r in rows if int(r["L"]) == L and r["observable"] == "B(r)" and r["fit_window"] == "1"]
        sfit = [(float(r["x"]), float(r["mean_value"])) for r in rows if int(r["L"]) == L and r["observable"] == "S(q)" and r["fit_window"] == "1"]
        if len(bfit) != 7:
            raise RuntimeError(f"Lab 10 L={L} B(r) fit window must be r=2..8")
        expected_s_n = 13 if L == 128 else 25
        if len(sfit) != expected_s_n:
            raise RuntimeError(f"Lab 10 L={L} S(q) fractional fit-window row count drifted")
        zB = 0.5 * linear_slope(bfit)
        zS = -0.5 * (linear_slope(sfit) + 1.0)
        if abs(zB - expected_zB) > 8e-7:
            raise RuntimeError(f"Lab 10 L={L} B(r) curve no longer reproduces zeta_B: {zB:.6f}")
        if abs(zS - expected_zS) > 8e-7:
            raise RuntimeError(f"Lab 10 L={L} S(q) curve no longer reproduces zeta_S: {zS:.6f}")


def verify_receipt_consistency() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    for token in RECEIPT_LOCKS:
        if token not in receipt:
            raise RuntimeError(f"Lab 10 receipt/result/failure boundary drifted: {token}")
    m = re.search(r"cross-size zeta_S drift\s+= ([0-9.]+)", receipt)
    if not m or abs(float(m.group(1)) - abs(EXPECTED_ZETA[128][1] - EXPECTED_ZETA[256][1])) > 1e-6:
        raise RuntimeError("Lab 10 cross-size zeta_S drift inconsistent with locked estimates")
    if float(m.group(1)) <= 0.100:
        raise RuntimeError("Lab 10 thermodynamic closure failure boundary was weakened")


def main() -> None:
    for path in (TARGET, PYTHON, RECEIPT, SAMPLE_CSV, CURVES_CSV, SOURCE_RECEIPT, PAPER_FIG, *PLOT_FILES):
        if not path.exists():
            raise RuntimeError(f"Lab 10 required artifact missing: {path.relative_to(ROOT)}")

    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    if title != "Reproduction Lab（复现实验室）10 · 超粗糙几何":
        raise RuntimeError(f"Lab 10 title drifted: {title!r}")

    visible = visible_text(soup)
    for token in REQUIRED_VISIBLE:
        if token not in visible:
            raise RuntimeError(f"Lab 10 required Language V2 text missing: {token}")
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f"Lab 10 ordinary workflow English remains visible: {token}")

    figures = soup.select("figure.figure img")
    if tuple(x.get("src") for x in figures) != EXPECTED_SRCS:
        raise RuntimeError("Lab 10 Figure wiring drifted")
    if tuple(x.get("alt") for x in figures) != EXPECTED_ALTS:
        raise RuntimeError("Lab 10 Figure alt text drifted")
    verify_local_links(soup)

    py = PYTHON.read_text(encoding="utf-8")
    for token in PYTHON_LOCKS:
        if token not in py:
            raise RuntimeError(f"Lab 10 Python contract drifted: {token}")

    verify_receipt_consistency()
    verify_sample_csv()
    verify_curve_csv()
    verify_source_provenance()

    for plot in PLOT_FILES:
        w, h = png_size(plot)
        if w < 900 or h < 500:
            raise RuntimeError(f"Lab 10 code plot below evidence resolution contract: {plot.name} {w}x{h}")
        if plot.stat().st_size < 10_000:
            raise RuntimeError(f"Lab 10 code plot suspiciously small: {plot.name}")

    print("Lab 10 read-only Language V2 seal PASS; super-rough signature/thermodynamic-zeta failure/provenance/curves/Figures/links preserved.")


if __name__ == "__main__":
    main()
