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

TARGET = ROOT / "modules/reproduction-lab-11.html"
PYTHON = ROOT / "examples/reproduction-lab/lesson11_fss_nu.py"
RECEIPT = ROOT / "assets/reproduction-lab/lesson11_fss_nu.txt"
RAW_CSV = ROOT / "assets/reproduction-lab/lesson11_fc_raw.csv"
SOURCE_RECEIPT = ROOT / "assets/reproduction-lab/source-figure-receipt.json"
PAPER_FIG = ROOT / "assets/reproduction-lab/source-ferrero2013-pre-fig2-full.png"
PLOT_FILES = (
    ROOT / "assets/reproduction-lab/lesson11_mean_fc.png",
    ROOT / "assets/reproduction-lab/lesson11_std_fc.png",
    ROOT / "assets/reproduction-lab/lesson11_nu_vs_window.png",
    ROOT / "assets/reproduction-lab/lesson11_collapse_score.png",
)
EXPECTED_SRCS = (
    "../assets/reproduction-lab/source-ferrero2013-pre-fig2-full.png",
    "../assets/reproduction-lab/lesson11_mean_fc.png",
    "../assets/reproduction-lab/lesson11_std_fc.png",
    "../assets/reproduction-lab/lesson11_nu_vs_window.png",
    "../assets/reproduction-lab/lesson11_collapse_score.png",
)
EXPECTED_ALTS = (
    "Ferrero PRE 2013 图 2 完整原图区域",
    "单样本临界力的平均值随系统尺寸变化",
    "阈值标准差随系统尺寸变化及有限尺寸拟合",
    "不同有限尺寸区间给出的有效 ν",
    "不同假设 ν 下的分位数坍缩评分",
)
REQUIRED_VISIBLE = (
    "finite-size scaling（有限尺寸标度）",
    "finite-size correction（有限尺寸修正）",
    "quenched disorder（淬火无序）",
    "ν=1.318867",
    "1.557481",
    "1.503976",
    "1.709690",
    "0.205713",
    "0.15 判据",
    "尺寸区间稳定性：未通过",
    "有限尺寸趋势：存在",
    "普适 ν 结论：不授权",
    "[1.241478, 1.903499]",
    "ν=1.405",
    "评分=0.117003",
    "评分=0.120858",
    "评分=0.123243",
)
FORBIDDEN_VISIBLE = (
    "Lesson 11",
    "Paper2 Method Track",
    "真实 simulation plot",
    "finite-size threshold",
    "sample-to-sample",
    "mean finite-size threshold",
    "aspect protocol",
    "ν-sensitive observable",
    "size-window gate",
    "finite-size critical force",
    "aspect-ratio",
    "original caption",
    "thermodynamic critical force",
    "Our simulation output",
    "quenched-disorder realizations",
    "sample threshold",
    "observable-level bridge",
    "M grid",
    "independent realizations",
    "disorder normalization",
    "force units",
    "critical-state algorithm",
    "finite geometry",
    "distribution width",
    "sample-specific thresholds",
    "sample-to-sample fluctuation",
    "48-realization distribution width",
    "log–log effective fit",
    "same regression",
    "synthetic data",
    "gold test PASS",
    "all-four",
    "raw threshold table",
    "size-window audit",
    "pre-registered",
    "SIZE-WINDOW STABILITY GATE",
    "thermodynamic ν",
    "distribution collapse",
    "quantile-collapse score",
    "variance fit",
    "best scan",
    "optimum",
    "FINITE-SIZE TREND EXISTS",
    "UNIVERSAL NU CLAIM",
    "bootstrap 95%",
    "run receipt",
    "192-row threshold table",
    "论文截图 receipt",
    "finite-size scaling（有限尺寸标度）（有限尺寸标度）",
    "quenched disorder（淬火无序）（淬火无序）",
)
PYTHON_LOCKS = (
    "TARGET_NU=4/3",
    "WINDOW_DRIFT_GATE=0.15",
    "BOOTSTRAPS=3000",
    "EXPECTED={32:320,64:736,128:1728,256:4096}",
    "N_PER_SIZE=48",
    "assert len(rr)==N_PER_SIZE",
    "assert all(r['M']==M for r in rr)",
    "assert len({r['seed'] for r in rr})==N_PER_SIZE",
    "assert all(abs((r['fc_hi']-r['fc_lo'])-1/512)<1e-12 for r in rr)",
    "def fit_nu(Ls,stds):",
    "def collapse_score(rows,Ls,nu,probs=np.linspace(.1,.9,9)):",
    "def synthetic_gold(Ls,nu=TARGET_NU,seed=20261110):",
    "assert abs(syn_nu-TARGET_NU)<.05",
    "rng=np.random.default_rng(20261111); boot=[]",
    "grid=np.linspace(.8,2.2,281)",
    "window_pass=window_drift<WINDOW_DRIFT_GATE",
    "f'SIZE-WINDOW STABILITY GATE     = {\"PASS\" if window_pass else \"NOT PASSED\"}'",
    "'UNIVERSAL NU CLAIM              = NOT AUTHORIZED'",
    "'FINITE-SIZE TREND EXISTS; THERMODYNAMIC CLOSURE REQUIRES LARGER-SCALE EVIDENCE'",
    "(out/'lesson11_fss_nu.txt').write_text",
    "finish(fig,'lesson11_mean_fc.png')",
    "finish(fig,'lesson11_std_fc.png')",
    "finish(fig,'lesson11_nu_vs_window.png')",
    "finish(fig,'lesson11_collapse_score.png')",
)
RECEIPT_LOCKS = (
    "paper relation                 = Var(fc_sample) ~ L^(-2/nu_dep)",
    "paper aspect protocol          = M_phys ~ L^zeta_dep with zeta_dep=1.25",
    "raw statistical unit           = disorder realization",
    "realizations per L            = 48",
    "L ladder                       = 32, 64, 128, 256",
    "M grid ladder                  = 320, 736, 1728, 4096",
    "moving certificate             = 1 u-period",
    "fc bracket width               = 0.001953125",
    "synthetic target nu           = 1.333333",
    "synthetic recovered nu        = 1.318867",
    "SYNTHETIC FSS GOLD TEST         = PASS",
    "L= 32 M= 320 mean fc             = 0.819978841",
    "L= 32 M= 320 std(fc)             = 0.064453427",
    "L= 64 M= 736 mean fc             = 0.823315430",
    "L= 64 M= 736 std(fc)             = 0.033881635",
    "L=128 M=1728 mean fc             = 0.823396810",
    "L=128 M=1728 std(fc)             = 0.026465858",
    "L=256 M=4096 mean fc             = 0.821850586",
    "L=256 M=4096 std(fc)             = 0.015059779",
    "nu all four sizes             = 1.503976",
    "nu smallest three             = 1.557481",
    "nu largest three              = 1.709690",
    "size-window nu drift          = 0.205713",
    "size-window drift gate        = < 0.150",
    "realization-bootstrap 95% nu  = [1.241478, 1.903499]",
    "quantile-collapse best nu      = 1.405000",
    "collapse score best            = 0.117003",
    "collapse score nu=4/3          = 0.120858",
    "collapse score variance-fit nu = 0.123243",
    "SIZE-WINDOW STABILITY GATE     = NOT PASSED",
    "UNIVERSAL NU CLAIM              = NOT AUTHORIZED",
    "FINITE-SIZE TREND EXISTS; THERMODYNAMIC CLOSURE REQUIRES LARGER-SCALE EVIDENCE",
)
EXPECTED_M = {32: 320, 64: 736, 128: 1728, 256: 4096}
EXPECTED_MEAN = {32: 0.819978841, 64: 0.823315430, 128: 0.823396810, 256: 0.821850586}
EXPECTED_STD = {32: 0.064453427, 64: 0.033881635, 128: 0.026465858, 256: 0.015059779}
EXPECTED_NU = (1.557481, 1.503976, 1.709690)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError(f"Lab 11 artifact is not canonical PNG: {path.relative_to(ROOT)}")
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
            raise RuntimeError(f"Lab 11 local link escapes repository: {value}") from exc
        if not resolved.exists():
            raise RuntimeError(f"Lab 11 broken local link: {value}")


def verify_source_provenance() -> None:
    data = json.loads(SOURCE_RECEIPT.read_text(encoding="utf-8"))
    if data.get("render_dpi", 0) < 500:
        raise RuntimeError("Lab 11 source-figure receipt render DPI drifted")
    matches = [x for x in data.get("figures", []) if x.get("file") == PAPER_FIG.name]
    if len(matches) != 1:
        raise RuntimeError("Lab 11 Ferrero Fig.2 provenance missing or duplicated")
    entry = matches[0]
    if entry.get("source_page") != 5 or entry.get("pixel_size") != [1783, 1550]:
        raise RuntimeError("Lab 11 Ferrero Fig.2 provenance dimensions/page drifted")
    if "Fig. 2" not in entry.get("citation", ""):
        raise RuntimeError("Lab 11 Ferrero Fig.2 citation identity drifted")
    if png_size(PAPER_FIG) != (1783, 1550):
        raise RuntimeError("Lab 11 Ferrero Fig.2 actual dimensions no longer match receipt")


def slope(points: list[tuple[float, float]]) -> float:
    xs = [math.log(x) for x, _ in points]
    ys = [math.log(y) for _, y in points]
    xm = sum(xs) / len(xs)
    ym = sum(ys) / len(ys)
    den = sum((x - xm) ** 2 for x in xs)
    return sum((x - xm) * (y - ym) for x, y in zip(xs, ys)) / den


def fit_nu(Ls: list[int], stds: list[float]) -> float:
    return -1.0 / slope(list(zip(Ls, stds)))


def verify_raw_csv() -> None:
    with RAW_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected_header = ["L", "M", "seed", "fc_lo", "fc_hi", "fc_mid"]
    if not rows or list(rows[0].keys()) != expected_header:
        raise RuntimeError("Lab 11 raw threshold CSV header drifted")
    if len(rows) != 192:
        raise RuntimeError(f"Lab 11 raw threshold CSV must contain 192 rows, found {len(rows)}")

    means = {}
    stds = {}
    for L, M in EXPECTED_M.items():
        group = [row for row in rows if int(row["L"]) == L]
        if len(group) != 48:
            raise RuntimeError(f"Lab 11 L={L} must contain 48 independent disorder rows")
        if any(int(row["M"]) != M for row in group):
            raise RuntimeError(f"Lab 11 L={L} M grid drifted")
        if len({int(row["seed"]) for row in group}) != 48:
            raise RuntimeError(f"Lab 11 L={L} seed identities are not independent/unique")
        vals = []
        for row in group:
            lo, hi, mid = map(float, (row["fc_lo"], row["fc_hi"], row["fc_mid"]))
            if abs((hi - lo) - 1 / 512) > 1e-12:
                raise RuntimeError(f"Lab 11 fc bracket width drifted for L={L}, seed={row['seed']}")
            if abs(mid - 0.5 * (lo + hi)) > 1e-12:
                raise RuntimeError(f"Lab 11 fc midpoint inconsistent for L={L}, seed={row['seed']}")
            vals.append(mid)
        means[L] = statistics.fmean(vals)
        stds[L] = statistics.stdev(vals)
        if abs(means[L] - EXPECTED_MEAN[L]) > 5e-10:
            raise RuntimeError(f"Lab 11 L={L} mean fc drifted: {means[L]:.9f}")
        if abs(stds[L] - EXPECTED_STD[L]) > 5e-10:
            raise RuntimeError(f"Lab 11 L={L} std(fc) drifted: {stds[L]:.9f}")

    Ls = [32, 64, 128, 256]
    ss = [stds[L] for L in Ls]
    nu_small = fit_nu(Ls[:3], ss[:3])
    nu_all = fit_nu(Ls, ss)
    nu_large = fit_nu(Ls[1:], ss[1:])
    for got, expected in zip((nu_small, nu_all, nu_large), EXPECTED_NU):
        if abs(got - expected) > 8e-7:
            raise RuntimeError(f"Lab 11 raw CSV no longer reproduces nu: {got:.6f} vs {expected:.6f}")
    drift = max(nu_small, nu_all, nu_large) - min(nu_small, nu_all, nu_large)
    if abs(drift - 0.205713) > 8e-7:
        raise RuntimeError(f"Lab 11 size-window drift changed: {drift:.6f}")
    if drift <= 0.15:
        raise RuntimeError("Lab 11 size-window failure boundary was weakened")


def main() -> None:
    for path in (TARGET, PYTHON, RECEIPT, RAW_CSV, SOURCE_RECEIPT, PAPER_FIG, *PLOT_FILES):
        if not path.exists():
            raise RuntimeError(f"Lab 11 required artifact missing: {path.relative_to(ROOT)}")

    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    if title != "Reproduction Lab（复现实验室）11 · 有限尺寸标度与 ν":
        raise RuntimeError(f"Lab 11 title drifted: {title!r}")

    visible = visible_text(soup)
    for token in REQUIRED_VISIBLE:
        if token not in visible:
            raise RuntimeError(f"Lab 11 required Language V2 text missing: {token}")
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f"Lab 11 ordinary workflow English remains visible: {token}")

    figures = soup.select("figure.figure img")
    if tuple(x.get("src") for x in figures) != EXPECTED_SRCS:
        raise RuntimeError("Lab 11 Figure wiring drifted")
    if tuple(x.get("alt") for x in figures) != EXPECTED_ALTS:
        raise RuntimeError("Lab 11 Figure alt text drifted")
    verify_local_links(soup)

    py = PYTHON.read_text(encoding="utf-8")
    for token in PYTHON_LOCKS:
        if token not in py:
            raise RuntimeError(f"Lab 11 Python contract drifted: {token}")

    receipt = RECEIPT.read_text(encoding="utf-8")
    for token in RECEIPT_LOCKS:
        if token not in receipt:
            raise RuntimeError(f"Lab 11 receipt/result/failure boundary drifted: {token}")

    verify_raw_csv()
    verify_source_provenance()
    for plot in PLOT_FILES:
        w, h = png_size(plot)
        if w < 900 or h < 500:
            raise RuntimeError(f"Lab 11 code plot below evidence resolution contract: {plot.name} {w}x{h}")
        if plot.stat().st_size < 10_000:
            raise RuntimeError(f"Lab 11 code plot suspiciously small: {plot.name}")

    print("Lab 11 read-only Language V2 seal PASS; synthetic gold test/size-window failure/raw thresholds/provenance/Figures/links preserved.")


if __name__ == "__main__":
    main()
