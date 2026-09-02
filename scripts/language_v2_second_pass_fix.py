from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

PAGE = ROOT / "modules/reproduction-lab-03.html"
PAPER_FIGURE = ROOT / "assets/reproduction-lab/caballero2020-fig2-time-roughness.webp"
SVG = ROOT / "assets/reproduction-lab/lesson03_ew_roughness_thumbnail.svg"
PYTHON = ROOT / "examples/reproduction-lab/lesson03_ew_roughness.py"

LOCKED_RESULTS = (
    "0.91%", "1.36%", "3.04%",
    "1.39%", "1.86%", "3.40%",
    "1.02%", "1.33%", "2.46%",
    "0.9592",
)

FORBIDDEN_VISIBLE = (
    "Lesson 03",
    "Gold Test",
    "gold test",
    "paper protocol",
    "analytic benchmark",
    "relative error",
    "realization",
    "Hard gate",
    "hard gate",
    "CPU-fast",
    "time horizon",
    "comparison window",
    "thumbnail reproduction",
    " interface ",
    " estimator",
    " implementation",
    " prediction",
    "1D ",
    "2D ",
    "最干净的 一维",
    " gate ",
    " window ",
    " authority ",
    " pipeline ",
    " checkpoint ",
    " benchmark ",
    " raw data",
    " steady velocity",
    " sample-specific threshold",
    " effective exponent",
)

REQUIRED_VISIBLE = (
    "Reproduction Lab（复现实验室）03",
    "thermal roughness（热粗糙度）",
    "thermal noise（热噪声）",
    "bulk-to-line projection（体场到界面线投影）",
    "quenched disorder（冻结无序）",
    "thermal white noise（热白噪声）",
    "finite-time crossover（有限时间交叉）",
    "periodic Laplacian（周期拉普拉斯算子）",
    "FDT noise（涨落耗散噪声）",
    "Monte Carlo（蒙特卡洛）",
    "correlation function（相关函数）",
    "一维 Edwards–Wilkinson Eq. (15)",
    "为什么还没跑二维 GL？",
)


def visible_teaching_text(soup: BeautifulSoup) -> str:
    clone = BeautifulSoup(str(soup), "html.parser")
    for selector in (".eq", ".source-text", "pre", "code", "script", "style", "math"):
        for node in clone.select(selector):
            node.decompose()
    return " ".join(clone.stripped_strings)


def resolve_local(base: Path, href: str) -> Path | None:
    if not href or href.startswith(("http://", "https://", "mailto:", "#")):
        return None
    parsed = urlsplit(href)
    if not parsed.path:
        return None
    return (base.parent / parsed.path).resolve()


def main() -> None:
    raw = PAGE.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    text = visible_teaching_text(soup)

    for token in FORBIDDEN_VISIBLE:
        if token in text:
            raise RuntimeError(f"Lab 03 visible Language V2 residue: {token!r}")
    for token in REQUIRED_VISIBLE:
        if token not in text:
            raise RuntimeError(f"Lab 03 required Language V2 form missing: {token!r}")

    if soup.title is None or soup.title.get_text(strip=True) != "Reproduction Lab（复现实验室）03 · EW 热粗糙化缩略复现":
        raise RuntimeError("Lab 03 title regressed")

    for token in LOCKED_RESULTS:
        if token not in raw:
            raise RuntimeError(f"Lab 03 locked numerical result missing: {token}")

    equations = soup.select(".eq")
    if len(equations) != 8:
        raise RuntimeError(f"Lab 03 expected 8 equation/workflow boxes, found {len(equations)}")
    if "比较区间：4 ≤ r ≤ 64" not in [eq.get_text(" ", strip=True) for eq in equations]:
        raise RuntimeError("Lab 03 predeclared comparison interval changed")

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 03 expected 2 Figures, found {len(figures)}")
    expected_srcs = [
        "../assets/reproduction-lab/caballero2020-fig2-time-roughness.webp",
        "../assets/reproduction-lab/lesson03_ew_roughness_thumbnail.svg",
    ]
    expected_alts = [
        "Caballero 2020 图 2：界面粗糙度随时间演化",
        "本课 EW 数值模拟与 Caballero Eq.19 的粗糙度对照",
    ]
    if [img.get("src") for img in figures] != expected_srcs:
        raise RuntimeError("Lab 03 Figure wiring changed")
    if [img.get("alt") for img in figures] != expected_alts:
        raise RuntimeError("Lab 03 Figure alt text regressed")

    checked = set()
    for a in soup.find_all("a"):
        path = resolve_local(PAGE, a.get("href"))
        if path is None or path in checked:
            continue
        checked.add(path)
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Lab 03 local link escapes repository: {a.get('href')}") from exc
        if not path.is_file():
            raise RuntimeError(f"Lab 03 local link target missing: {a.get('href')}")
    if PYTHON.resolve() not in checked:
        raise RuntimeError("Lab 03 full Python source link missing")

    for path in (PAPER_FIGURE, SVG, PYTHON):
        if not path.is_file():
            raise RuntimeError(f"Lab 03 required asset/source missing: {path.relative_to(ROOT)}")

    svg = SVG.read_text(encoding="utf-8")
    if "NotoSansCJKsc" not in svg:
        raise RuntimeError("Lab 03 SVG no longer contains CJK plot glyphs")
    for token in (
        "EW roughness: simulation vs Caballero Eq. (19)",
        "Declared comparison window",
        "One thermal realization",
        "Reproduction Lab · Lesson 03",
        "simulation t=",
        "|sim-theory| / theory (%)",
        "u(y) + offset",
    ):
        if token in svg:
            raise RuntimeError(f"Lab 03 SVG English label residue: {token!r}")

    py = PYTHON.read_text(encoding="utf-8")
    for token in (
        'plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "DejaVu Sans"]',
        "N = 256",
        "dy = 1.0",
        "dt = 0.1",
        "n_realizations = 64",
        "target_times = (10.0, 100.0, 1000.0)",
        "np.random.default_rng(12345)",
        "fit = (r >= 4.0) & (r <= 64.0)",
        'assert results[t]["median_rel"] < 0.03',
        'assert results[t]["rms_rel"] < 0.04',
        "assert 0.88 < late_ratio < 1.08",
        'label=f"数值模拟 t={t:g}"',
        'ax.set_title("EW 粗糙度：数值模拟与 Caballero Eq. (19) 对照")',
        'ax.set_ylabel("|数值-理论| / 理论 (%)")',
        'ax.set_title("预先声明的比较区间：4 ≤ r ≤ 64")',
        'ax.set_ylabel("u(y) + 纵向偏移")',
        'ax.set_title("单个热噪声样本：粗糙度随时间增长")',
        'fig.suptitle("复现实验室 · 第 03 课 · EW 热粗糙化缩略复现", fontsize=14)',
    ):
        if token not in py:
            raise RuntimeError(f"Lab 03 Python scientific/plot contract changed: {token!r}")

    print(
        f"Lab 03 seal PASS: {len(equations)} equation/workflow boxes, "
        f"{len(figures)} Figures, {len(checked)} local links; HTML/SVG/Python contracts intact."
    )


if __name__ == "__main__":
    main()
