from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

PAGE = ROOT / "modules/reproduction-lab-04.html"
SVG = ROOT / "assets/reproduction-lab/lesson04_gl_to_ew_boundary.svg"
PAPER_FIG = ROOT / "assets/reproduction-lab/caballero2020-fig3-temperature-boundary.webp"
PYTHON = ROOT / "examples/reproduction-lab/lesson04_gl_to_ew.py"

LOCKED_RESULTS = (
    "7.67%", "7.57%", "4.49%", "4.36%",
    "0.9879", "1.3738", "0.9870", "1.3740",
    "26.52%", "1.6664", "0.9806", "5.47%",
    "40.51%", "1.7018", "0.9760", "7.23%",
)

FORBIDDEN_VISIBLE = (
    " hard gate",
    "mapping breakdown",
    "Lesson 02",
    "clean wall",
    "finite T",
    "transverse profile",
    "fitting parameters",
    "validity boundary",
    "realization",
    "integrator",
    "只要 体场",
    "第 02 课 在",
    "无序为零畴壁 上",
    "有限温度 下",
    "整个 横向剖面",
    "都作为 拟合参数",
)

REQUIRED_VISIBLE = (
    "model reduction（模型约化）",
    "soliton ansatz（孤子假设）",
    "single-valued interface（单值界面）",
    "thermal noise（热噪声）",
    "低温映射：通过。",
    "高温映射失效：已检测到。",
    "elastic interface（弹性界面）",
    "crossover（交叉）",
    "phase-field（相场）",
    "4≤r≤32 尺度区间",
)


def visible_teaching_text(soup: BeautifulSoup) -> str:
    clone = BeautifulSoup(str(soup), "html.parser")
    for selector in (".eq", "pre", "code", "script", "style", "math"):
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

    if soup.title is None or soup.title.get_text(strip=True) != "Reproduction Lab（复现实验室）04 · GL → EW 适用边界":
        raise RuntimeError("Lab 04 title changed")

    for token in FORBIDDEN_VISIBLE:
        if token in text:
            raise RuntimeError(f"Lab 04 visible Language V2 residue: {token!r}")
    for token in REQUIRED_VISIBLE:
        if token not in text:
            raise RuntimeError(f"Lab 04 required Language V2 form missing: {token!r}")
    for token in LOCKED_RESULTS:
        if token not in raw:
            raise RuntimeError(f"Lab 04 locked numerical result missing: {token}")

    equations = soup.select(".eq")
    if len(equations) != 3:
        raise RuntimeError(f"Lab 04 expected 3 equation blocks, found {len(equations)}")

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 04 expected 2 Figures, found {len(figures)}")
    expected_figures = (
        (
            "../assets/reproduction-lab/caballero2020-fig3-temperature-boundary.webp",
            "Caballero 2020 图 3：温度升高时 GL 到 EW 映射逐渐失效",
        ),
        (
            "../assets/reproduction-lab/lesson04_gl_to_ew_boundary.svg",
            "本课低温 GL→EW 映射通过与高温映射失效对照",
        ),
    )
    for fig, (src, alt) in zip(figures, expected_figures):
        if fig.get("src") != src or fig.get("alt") != alt:
            raise RuntimeError(f"Lab 04 Figure contract changed: {fig.get('src')!r}, {fig.get('alt')!r}")

    checked = set()
    for a in soup.find_all("a"):
        path = resolve_local(PAGE, a.get("href"))
        if path is None or path in checked:
            continue
        checked.add(path)
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Lab 04 local link escapes repository: {a.get('href')}") from exc
        if not path.is_file():
            raise RuntimeError(f"Lab 04 local link target missing: {a.get('href')}")
    if PYTHON.resolve() not in checked:
        raise RuntimeError("Lab 04 Python source link missing")

    for path in (PAPER_FIG, SVG, PYTHON):
        if not path.is_file():
            raise RuntimeError(f"Lab 04 required asset/source missing: {path.relative_to(ROOT)}")

    if "LOW-T MAPPING PASS; HIGH-T BREAKDOWN DETECTED" not in raw:
        raise RuntimeError("Lab 04 machine receipt marker changed in HTML")

    py = PYTHON.read_text(encoding="utf-8")
    required_python = (
        'plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "DejaVu Sans"]',
        "n_realizations = 12",
        "target_times = (10.0, 100.0)",
        "window = (r >= 4.0) & (r <= 32.0)",
        'assert low[t]["median_rel"] < 0.10',
        'assert low[t]["rms_rel"] < 0.10',
        'assert low[100.0]["multi_cross"] < 0.01',
        'assert high[100.0]["median_rel"] > 0.30',
        'assert high[100.0]["W_std"] > 2.0 * low[100.0]["W_std"]',
        'assert high[100.0]["multi_cross"] > 0.03',
        'print("LOW-T MAPPING PASS; HIGH-T BREAKDOWN DETECTED")',
        '"低温：体场 GL 跟随 EW"',
        '"高温：映射失效"',
        'ax.set_title("剖面拟合诊断")',
        'ax.set_title("映射失效时不应强行拟合 ζ")',
    )
    for token in required_python:
        if token not in py:
            raise RuntimeError(f"Lab 04 Python scientific/plot contract changed: {token!r}")

    svg = SVG.read_text(encoding="utf-8")
    for token in (
        "低温：体场 GL 跟随 EW",
        "高温：映射失效",
        "剖面拟合诊断",
        "映射失效时不应强行拟合 ζ",
        "复现实验室 · 第 04 课 · 二维 GL → 一维 EW 适用边界",
    ):
        if token not in svg:
            raise RuntimeError(f"Lab 04 SVG expected localized label missing: {token!r}")
    for token in (
        "Low T: bulk GL follows EW",
        "High T: mapping breaks down",
        "Profile-fit diagnostic",
        "The mapping fails before we force a zeta fit",
        "Reproduction Lab · Lesson 04",
    ):
        if token in svg:
            raise RuntimeError(f"Lab 04 SVG English label residue: {token!r}")

    print(
        f"Lab 04 seal PASS: {len(equations)} equations, {len(checked)} local links, "
        "HTML/paper-Figure/SVG/Python contracts intact."
    )


if __name__ == "__main__":
    main()
