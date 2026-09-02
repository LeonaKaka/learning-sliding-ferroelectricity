from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
import csv
import json
import math
import statistics
import struct

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-12.html"
PYTHON = ROOT / "examples/reproduction-lab/lesson12_thermal_rounding.py"
RECEIPT = ROOT / "assets/reproduction-lab/lesson12_thermal_rounding.txt"
ROUND_CSV = ROOT / "assets/reproduction-lab/lesson12_rounding_raw.csv"
SUB_CSV = ROOT / "assets/reproduction-lab/lesson12_subthreshold_raw.csv"
SOURCE_RECEIPT = ROOT / "assets/reproduction-lab/source-figure-receipt.json"
SOURCE_FIGS = {
    "source-ferrero2013-review-fig1-full.png": (3, (3250, 2550), "Fig. 1"),
    "source-ferrero2021-fig3-full.png": (8, (2883, 1550), "Fig. 3"),
    "source-ferrero2021-fig4-full.png": (8, (3250, 1580), "Fig. 4"),
}
PLOT_FILES = (
    ROOT / "assets/reproduction-lab/lesson12_rounding_vT.png",
    ROOT / "assets/reproduction-lab/lesson12_psi_vs_window.png",
    ROOT / "assets/reproduction-lab/lesson12_subthreshold_vT.png",
    ROOT / "assets/reproduction-lab/lesson12_resolved_fraction.png",
    ROOT / "assets/reproduction-lab/lesson12_halfwindow_stability.png",
)
EXPECTED_SRCS = (
    "../assets/reproduction-lab/source-ferrero2013-review-fig1-full.png",
    "../assets/reproduction-lab/lesson12_rounding_vT.png",
    "../assets/reproduction-lab/lesson12_psi_vs_window.png",
    "../assets/reproduction-lab/source-ferrero2021-fig3-full.png",
    "../assets/reproduction-lab/lesson12_subthreshold_vT.png",
    "../assets/reproduction-lab/source-ferrero2021-fig4-full.png",
    "../assets/reproduction-lab/lesson12_resolved_fraction.png",
    "../assets/reproduction-lab/lesson12_halfwindow_stability.png",
)
EXPECTED_ALTS = (
    "Ferrero 2013 Numerical Approaches 图 1 完整原图区域",
    "各单样本退钉扎阈值处的速度随温度变化",
    "热圆整有效指数随温度拟合区间变化",
    "Ferrero Annual Review 2021 图 3 完整原图区域",
    "阈值下热激活速度随温度变化",
    "Ferrero Annual Review 2021 图 4 完整原图区域",
    "不同温度下已解析热轨迹比例",
    "不同温度下前后半观测窗速度稳定性",
)
REQUIRED_VISIBLE = (
    "thermal rounding（热圆整）≠ creep（蠕变）",
    "错误的 PRE Fig.6",
    "depinning（退钉扎）",
    "Brownian（布朗）",
    "asymptotic regime（渐近区）",
    "extended interface（延展界面）",
    "0.112940%",
    "0.795888%",
    "0.150920 / 0.150587 / 0.150878",
    "0.081861",
    "0.092425",
    "0.108981",
    "0.073079",
    "0.087862",
    "0.105033",
    "0.071115",
    "0.084517",
    "0.101828",
    "0.031953",
    "0.030 判据",
    "[0.029133, 0.034808]",
    "热圆整拟合区间稳定性：未通过",
    "普适 ψ 结论：不授权",
    "0.5625",
    "3.102542",
    "低温蠕变渐近区：尚未解析",
    "蠕变律 / μ 结论：不授权",
    "有限温热圆整现象：可见",
    "普适 ψ 与蠕变 μ 都不授权",
)
FORBIDDEN_VISIBLE = (
    "Lesson 12",
    "Paper2 Method Track",
    "真实 simulation plot",
    "thermal rounding ≠ creep",
    "transport map",
    "regime map",
    "temperature window",
    "activated motion",
    "creep-law fit",
    "full crop with original caption",
    "panels",
    "panel (b)",
    "low-drive",
    "thermally activated transport",
    "threshold authority",
    "sample-specific threshold authority",
    "steady velocity",
    "realization-level aggregation",
    "lo / midpoint / hi",
    "gold test",
    "THERMAL-ROUNDING WINDOW GATE",
    "UNIVERSAL PSI CLAIM",
    "subthreshold run",
    "finite-time activated velocity",
    "creep-law μ fit",
    "barrier picture",
    "creep energetics",
    "Resolved fraction",
    "trajectory fraction",
    "Stationarity diagnostic",
    "median relative difference",
    "LOW-T CREEP ASYMPTOTIC RESOLVED",
    "CREEP-LAW / μ CLAIM",
    "FINITE-T ROUNDING OBSERVED",
    "ASYMPTOTIC EXPONENTS REMAIN OPEN",
    "synthetic ψ pipeline",
    "subthreshold trajectories",
    "run receipt",
    "rounding raw",
    "subthreshold raw",
    "论文截图 receipt",
    "thermal rounding（热圆整）（热圆整）",
    "creep（蠕变）（蠕变）",
)
PYTHON_LOCKS = (
    "PSI_SYNTH=0.15",
    "PSI_WINDOW_GATE=0.03",
    "BOOTSTRAPS=5000",
    "ROUND_SEEDS=8",
    "def brownian_gold(seed=20261201,ntraj=10000,dt=.02,steps=500,f=.17,T=.08):",
    "sig=math.sqrt(2*T*dt)",
    "assert bm_err<.01 and bv_err<.03",
    "def synthetic_psi_gold(Ts,seed=20261202,psi=PSI_SYNTH,n=512):",
    "assert max(abs(x-PSI_SYNTH) for x in synth_fits)<.005",
    "assert len(rounding)==144 and len(sub)==40",
    "assert set(rounding.authority)=={'lo','mid','hi'}",
    "assert len(Ts)==6 and len(rounding.seed.unique())==ROUND_SEEDS",
    "rng=np.random.default_rng(20261212); b6=[]; b4=[]; bd=[]",
    "subthreshold drive              = f = fc_lo - 0.08",
    "creep_resolved=[(rf==1.0 and hd<.2) for _,_,rf,hd in subagg]",
    "assert not lowT_resolved",
    "f'THERMAL-ROUNDING WINDOW GATE    = {\"PASS\" if mid_drift<PSI_WINDOW_GATE else \"NOT PASSED\"}'",
    "'UNIVERSAL PSI CLAIM             = NOT AUTHORIZED'",
    "'LOW-T CREEP ASYMPTOTIC RESOLVED = NO'",
    "'CREEP-LAW / MU CLAIM             = NOT AUTHORIZED'",
    "'FINITE-T ROUNDING OBSERVED; ASYMPTOTIC THERMAL AND CREEP EXPONENTS REMAIN OPEN'",
    "(out/'lesson12_thermal_rounding.txt').write_text",
    "finish(fig,'lesson12_rounding_vT.png')",
    "finish(fig,'lesson12_psi_vs_window.png')",
    "finish(fig,'lesson12_subthreshold_vT.png')",
    "finish(fig,'lesson12_resolved_fraction.png')",
    "finish(fig,'lesson12_halfwindow_stability.png')",
)
RECEIPT_LOCKS = (
    "paper relation                  = v(fc,T) ~ T^psi",
    "rounding statistical unit       = quenched disorder realization",
    "rounding disorder realizations  = 8",
    "rounding thermal repeats/sample = 3",
    "rounding T ladder               = 0.0025, 0.005, 0.01, 0.02, 0.04, 0.08",
    "fc authority audit              = lo, midpoint, hi of each sample bracket",
    "Brownian gold mean rel error    = 0.112940%",
    "Brownian gold variance rel err  = 0.795888%",
    "BROWNIAN NOISE-NORMALIZATION GOLD TEST = PASS",
    "synthetic target psi            = 0.150000",
    "synthetic psi low4/low5/all6    = 0.150920 / 0.150587 / 0.150878",
    "SYNTHETIC THERMAL-EXPONENT GOLD TEST = PASS",
    "lo psi low4/low5/all6          = 0.081861 / 0.092425 / 0.108981",
    "mid psi low4/low5/all6          = 0.073079 / 0.087862 / 0.105033",
    "hi psi low4/low5/all6          = 0.071115 / 0.084517 / 0.101828",
    "midpoint psi window drift      = 0.031953",
    "psi window drift gate          = < 0.030",
    "threshold-authority all6 span  = 0.007152",
    "midpoint psi low4 bootstrap95  = [0.052590, 0.094732]",
    "midpoint psi all6 bootstrap95  = [0.084945, 0.127145]",
    "window-drift bootstrap95       = [0.029133, 0.034808]",
    "THERMAL-ROUNDING WINDOW GATE    = NOT PASSED",
    "UNIVERSAL PSI CLAIM             = NOT AUTHORIZED",
    "subthreshold drive              = f = fc_lo - 0.08",
    "subthreshold thermal repeats    = 2 per disorder sample",
    "sub T=0.020 mean v / resolved / half-diff = 0.020971 / 0.5625 / 3.102542",
    "sub T=0.040 mean v / resolved / half-diff = 0.110550 / 0.9375 / 0.237538",
    "sub T=0.060 mean v / resolved / half-diff = 0.162843 / 1.0000 / 0.117292",
    "sub T=0.080 mean v / resolved / half-diff = 0.198881 / 1.0000 / 0.081750",
    "sub T=0.120 mean v / resolved / half-diff = 0.237164 / 1.0000 / 0.046381",
    "resolved activated-motion rule  = trajectory fraction 1.0 AND median half-diff < 0.2",
    "LOW-T CREEP ASYMPTOTIC RESOLVED = NO",
    "CREEP-LAW / MU CLAIM             = NOT AUTHORIZED",
    "FINITE-T ROUNDING OBSERVED; ASYMPTOTIC THERMAL AND CREEP EXPONENTS REMAIN OPEN",
)
ROUND_TS = (0.0025, 0.005, 0.01, 0.02, 0.04, 0.08)
EXPECTED_PSIS = {
    "lo": (0.081861, 0.092425, 0.108981),
    "mid": (0.073079, 0.087862, 0.105033),
    "hi": (0.071115, 0.084517, 0.101828),
}
SUB_EXPECTED = {
    0.020: (0.020971, 0.5625, 3.102542),
    0.040: (0.110550, 0.9375, 0.237538),
    0.060: (0.162843, 1.0000, 0.117292),
    0.080: (0.198881, 1.0000, 0.081750),
    0.120: (0.237164, 1.0000, 0.046381),
}


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError(f"Lab 12 artifact is not canonical PNG: {path.relative_to(ROOT)}")
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
            raise RuntimeError(f"Lab 12 local link escapes repository: {value}") from exc
        if not resolved.exists():
            raise RuntimeError(f"Lab 12 broken local link: {value}")


def log_slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    xm = statistics.fmean(lx)
    ym = statistics.fmean(ly)
    den = sum((x - xm) ** 2 for x in lx)
    return sum((x - xm) * (y - ym) for x, y in zip(lx, ly)) / den


def verify_rounding_csv() -> None:
    with ROUND_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected_header = ["seed", "authority", "T", "v_rep1", "v_rep2", "v_rep3", "v_mean_within_disorder", "max_half_rel_diff"]
    if not rows or list(rows[0].keys()) != expected_header:
        raise RuntimeError("Lab 12 rounding raw CSV header drifted")
    if len(rows) != 144:
        raise RuntimeError(f"Lab 12 rounding raw CSV must contain 144 rows, found {len(rows)}")
    seeds = sorted({int(r["seed"]) for r in rows})
    if len(seeds) != 8:
        raise RuntimeError("Lab 12 rounding data must contain 8 independent disorder seeds")
    authorities = {r["authority"] for r in rows}
    if authorities != {"lo", "mid", "hi"}:
        raise RuntimeError(f"Lab 12 threshold authority set drifted: {authorities}")
    temps = tuple(sorted({float(r["T"]) for r in rows}))
    if temps != ROUND_TS:
        raise RuntimeError(f"Lab 12 rounding temperature ladder drifted: {temps}")

    agg = {}
    for authority in ("lo", "mid", "hi"):
        means = []
        for T in ROUND_TS:
            group = [r for r in rows if r["authority"] == authority and float(r["T"]) == T]
            if len(group) != 8 or len({int(r["seed"]) for r in group}) != 8:
                raise RuntimeError(f"Lab 12 {authority}, T={T} must contain 8 independent disorder rows")
            vals = []
            for row in group:
                reps = [float(row[f"v_rep{i}"]) for i in (1, 2, 3)]
                row_mean = float(row["v_mean_within_disorder"])
                if abs(statistics.fmean(reps) - row_mean) > 2e-12:
                    raise RuntimeError(f"Lab 12 within-disorder thermal-repeat mean drifted for seed={row['seed']}, authority={authority}, T={T}")
                vals.append(row_mean)
            means.append(statistics.fmean(vals))
        agg[authority] = means
        got = tuple(log_slope(list(ROUND_TS[:n]), means[:n]) for n in (4, 5, 6))
        for value, expected in zip(got, EXPECTED_PSIS[authority]):
            if abs(value - expected) > 8e-7:
                raise RuntimeError(f"Lab 12 raw rounding data no longer reproduce psi for {authority}: {got}")

    mid = EXPECTED_PSIS["mid"]
    drift = max(mid) - min(mid)
    if abs(drift - 0.031953) > 8e-7:
        raise RuntimeError(f"Lab 12 midpoint psi window drift changed: {drift:.6f}")
    if drift <= 0.030:
        raise RuntimeError("Lab 12 thermal-rounding failure boundary was weakened")
    all6_span = max(EXPECTED_PSIS[a][2] for a in EXPECTED_PSIS) - min(EXPECTED_PSIS[a][2] for a in EXPECTED_PSIS)
    if abs(all6_span - 0.007153) > 2e-6:
        raise RuntimeError("Lab 12 threshold-authority all6 span unexpectedly changed")


def verify_subthreshold_csv() -> None:
    with SUB_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected_header = ["seed", "delta_f", "T", "v_rep1", "v_rep2", "mean_v", "resolved_fraction", "max_half_rel_diff"]
    if not rows or list(rows[0].keys()) != expected_header:
        raise RuntimeError("Lab 12 subthreshold raw CSV header drifted")
    if len(rows) != 40:
        raise RuntimeError(f"Lab 12 subthreshold raw CSV must contain 40 rows, found {len(rows)}")
    if len({int(r["seed"]) for r in rows}) != 8:
        raise RuntimeError("Lab 12 subthreshold data must contain 8 independent disorder seeds")
    if any(abs(float(r["delta_f"]) + 0.08) > 1e-12 for r in rows):
        raise RuntimeError("Lab 12 subthreshold drive offset drifted from -0.08")

    for T, expected in SUB_EXPECTED.items():
        group = [r for r in rows if abs(float(r["T"]) - T) < 1e-12]
        if len(group) != 8 or len({int(r["seed"]) for r in group}) != 8:
            raise RuntimeError(f"Lab 12 subthreshold T={T} must contain 8 independent disorder rows")
        means = []
        resolved = []
        halfdiff = []
        for row in group:
            rep_mean = statistics.fmean([float(row["v_rep1"]), float(row["v_rep2"])])
            mean_v = float(row["mean_v"])
            if abs(rep_mean - mean_v) > 2e-12:
                raise RuntimeError(f"Lab 12 subthreshold thermal-repeat mean drifted for seed={row['seed']}, T={T}")
            means.append(mean_v)
            resolved.append(float(row["resolved_fraction"]))
            halfdiff.append(float(row["max_half_rel_diff"]))
        got = (statistics.fmean(means), statistics.fmean(resolved), statistics.median(halfdiff))
        tolerances = (8e-7, 8e-7, 8e-7)
        for value, target, tol in zip(got, expected, tolerances):
            if abs(value - target) > tol:
                raise RuntimeError(f"Lab 12 subthreshold aggregate drifted at T={T}: {got} vs {expected}")

    low = SUB_EXPECTED[0.020]
    if low[1] == 1.0 and low[2] < 0.2:
        raise RuntimeError("Lab 12 low-T creep failure boundary was weakened")


def verify_source_provenance() -> None:
    data = json.loads(SOURCE_RECEIPT.read_text(encoding="utf-8"))
    if data.get("render_dpi", 0) < 500:
        raise RuntimeError("Lab 12 source-figure receipt render DPI drifted")
    by_file = {x.get("file"): x for x in data.get("figures", [])}
    for name, (page, size, fig_marker) in SOURCE_FIGS.items():
        if name not in by_file:
            raise RuntimeError(f"Lab 12 source provenance missing: {name}")
        entry = by_file[name]
        if entry.get("source_page") != page or tuple(entry.get("pixel_size", [])) != size:
            raise RuntimeError(f"Lab 12 source provenance page/size drifted: {name}")
        if fig_marker not in entry.get("citation", ""):
            raise RuntimeError(f"Lab 12 source citation identity drifted: {name}")
        actual = png_size(ROOT / "assets/reproduction-lab" / name)
        if actual != size:
            raise RuntimeError(f"Lab 12 source Figure dimensions no longer match receipt: {name} {actual}")


def main() -> None:
    source_paths = tuple(ROOT / "assets/reproduction-lab" / name for name in SOURCE_FIGS)
    for path in (TARGET, PYTHON, RECEIPT, ROUND_CSV, SUB_CSV, SOURCE_RECEIPT, *source_paths, *PLOT_FILES):
        if not path.exists():
            raise RuntimeError(f"Lab 12 required artifact missing: {path.relative_to(ROOT)}")

    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    if title != "Reproduction Lab（复现实验室）12 · 热圆整与蠕变边界":
        raise RuntimeError(f"Lab 12 title drifted: {title!r}")

    visible = visible_text(soup)
    for token in REQUIRED_VISIBLE:
        if token not in visible:
            raise RuntimeError(f"Lab 12 required Language V2 text missing: {token}")
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f"Lab 12 ordinary workflow English remains visible: {token}")

    figures = soup.select("figure.figure img")
    if tuple(x.get("src") for x in figures) != EXPECTED_SRCS:
        raise RuntimeError("Lab 12 Figure wiring drifted")
    if tuple(x.get("alt") for x in figures) != EXPECTED_ALTS:
        raise RuntimeError("Lab 12 Figure alt text drifted")
    verify_local_links(soup)

    py = PYTHON.read_text(encoding="utf-8")
    for token in PYTHON_LOCKS:
        if token not in py:
            raise RuntimeError(f"Lab 12 Python contract drifted: {token}")

    receipt = RECEIPT.read_text(encoding="utf-8")
    for token in RECEIPT_LOCKS:
        if token not in receipt:
            raise RuntimeError(f"Lab 12 receipt/result/failure boundary drifted: {token}")

    verify_rounding_csv()
    verify_subthreshold_csv()
    verify_source_provenance()

    for plot in PLOT_FILES:
        w, h = png_size(plot)
        if w < 900 or h < 500:
            raise RuntimeError(f"Lab 12 code plot below evidence resolution contract: {plot.name} {w}x{h}")
        if plot.stat().st_size < 10_000:
            raise RuntimeError(f"Lab 12 code plot suspiciously small: {plot.name}")

    print("Lab 12 read-only Language V2 seal PASS; Brownian/synthetic tests, psi-window failure, unresolved low-T creep, raw data, provenance, Figures and links preserved.")


if __name__ == "__main__":
    main()
