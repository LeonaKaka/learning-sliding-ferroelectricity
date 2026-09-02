from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

PAGE = ROOT / "modules/reproduction-lab-05.html"
SVG = ROOT / "assets/reproduction-lab/lesson05_rb_projection_correlator.svg"
PAPER_FIG = ROOT / "assets/reproduction-lab/caballero2020-fig4-pinning-correlator.webp"
RECEIPT = ROOT / "assets/reproduction-lab/lesson05_rb_projection_correlator.txt"
PYTHON = ROOT / "examples/reproduction-lab/lesson05_rb_projection.py"

LOCKED_RESULTS = (
    "0.071833070",
    "0.0000002%",
    "0.0000012%",
    "0.995554",
    "0.222%",
    "0.445%",
    "0.104%",
    "1.039429",
    "1.039472",
    "0.099555",
)

FORBIDDEN_VISIBLE = (
    "barrier-幅度",
    "bulk coupling +",
    "sample 幅度",
    "shape/zero crossing",
    "Lesson 06",
    "体场→界面 这一步",
    "Dirac delta（狄拉克 δ） 之间",
    "而是 解析 Eq.26",
    "零点交叉 和故意错误对照",
    "真实缺陷 必然",
    "同时比较 二维 GL",
    "Reproduction Lab（复现实验室）（复现实验室）",
)

REQUIRED_VISIBLE = (
    "delta-correlated random-bond disorder（δ 相关随机键无序）",
    "domain wall（畴壁）",
    "pinning force（钉扎力）",
    "correlation length（相关长度）",
    "continuum white noise（连续白噪声）",
    "disordered interface（无序界面）",
    "barrier-amplitude coupling（势垒幅度耦合）",
    "effective correlator（有效相关函数）",
    "soliton ansatz（孤子假设）",
    "Kronecker delta（克罗内克 δ）",
    "Dirac delta（狄拉克 δ）",
    "无序投影全部验收条件：通过。",
    "effective force correlator（有效力相关函数）",
    "random-bond roughness（随机键粗糙度）",
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

    if soup.title is None or soup.title.get_text(strip=True) != "Reproduction Lab（复现实验室）05 · 体场 RB → 钉扎力":
        raise RuntimeError("Lab 05 title changed")

    for token in FORBIDDEN_VISIBLE:
        if token in text:
            raise RuntimeError(f"Lab 05 visible Language V2 residue: {token!r}")
    for token in REQUIRED_VISIBLE:
        if token not in text:
            raise RuntimeError(f"Lab 05 required Language V2 form missing: {token!r}")
    for token in LOCKED_RESULTS:
        if token not in raw:
            raise RuntimeError(f"Lab 05 locked numerical result missing: {token}")

    equations = soup.select(".eq")
    if len(equations) != 6:
        raise RuntimeError(f"Lab 05 expected 6 equation blocks, found {len(equations)}")

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 05 expected 2 Figures, found {len(figures)}")
    expected_figures = (
        (
            "../assets/reproduction-lab/caballero2020-fig4-pinning-correlator.webp",
            "Caballero 2020 图 4：钉扎力相关函数",
        ),
        (
            "../assets/reproduction-lab/lesson05_rb_projection_correlator.svg",
            "本课体场随机键无序投影与钉扎力相关函数",
        ),
    )
    for fig, (src, alt) in zip(figures, expected_figures):
        if fig.get("src") != src or fig.get("alt") != alt:
            raise RuntimeError(f"Lab 05 Figure contract changed: {fig.get('src')!r}, {fig.get('alt')!r}")

    checked = set()
    for a in soup.find_all("a"):
        path = resolve_local(PAGE, a.get("href"))
        if path is None or path in checked:
            continue
        checked.add(path)
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Lab 05 local link escapes repository: {a.get('href')}") from exc
        if not path.is_file():
            raise RuntimeError(f"Lab 05 local link target missing: {a.get('href')}")

    for required_link in (PYTHON.resolve(), RECEIPT.resolve()):
        if required_link not in checked:
            raise RuntimeError(f"Lab 05 required source/receipt link missing: {required_link.name}")

    for path in (PAPER_FIG, SVG, RECEIPT, PYTHON):
        if not path.is_file():
            raise RuntimeError(f"Lab 05 required asset/source missing: {path.relative_to(ROOT)}")

    py = PYTHON.read_text(encoding="utf-8")
    required_python = (
        'plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "DejaVu Sans"]',
        "M = 10_000",
        "du = 0.1",
        "n_realizations = 256",
        "rng = np.random.default_rng(20260901)",
        "zeta = base_normal / math.sqrt(du)",
        "zeta_wrong = base_normal",
        "window = np.arange(0, 51)",
        "assert eq25_eq26_rmse < 1e-6",
        "assert eq25_eq26_max < 1e-6",
        "assert rmse_over_Gamma0 < 0.01",
        "assert max_abs_over_Gamma0 < 0.015",
        "assert abs(empirical_zero - theory_zero) < 0.01",
        "assert 0.98 < amp_ratio < 1.02",
        "assert 0.09 < wrong_amp_ratio < 0.11",
        'print("ALL DISORDER-PROJECTION GATES PASS")',
        'ax.set_title("投影钉扎力相关函数")',
        'ax.set_title("四条独立投影钉扎力")',
        'ax.set_title("离散化陷阱：漏掉 du^(-1/2)")',
        '"复现实验室 · 第 05 课 · 体场 RB 无序 → 短程相关钉扎力"',
    )
    for token in required_python:
        if token not in py:
            raise RuntimeError(f"Lab 05 Python scientific/plot contract changed: {token!r}")

    receipt = RECEIPT.read_text(encoding="utf-8")
    for token in LOCKED_RESULTS + ("ALL DISORDER-PROJECTION GATES PASS",):
        if token not in receipt:
            raise RuntimeError(f"Lab 05 run receipt changed/missing: {token!r}")

    svg = SVG.read_text(encoding="utf-8")
    for token in (
        "投影钉扎力相关函数",
        "四条独立投影钉扎力",
        "离散化陷阱：漏掉 du^(-1/2)",
        "复现实验室 · 第 05 课 · 体场 RB 无序 → 短程相关钉扎力",
        "256 个独立无序样本平均",
    ):
        if token not in svg:
            raise RuntimeError(f"Lab 05 SVG expected localized label missing: {token!r}")
    for token in (
        "Projected pinning-force correlator",
        "Four independent projected pinning forces",
        "Discretization trap",
        "Reproduction Lab · Lesson 05",
    ):
        if token in svg:
            raise RuntimeError(f"Lab 05 SVG English label residue: {token!r}")

    print(
        f"Lab 05 seal PASS: {len(equations)} equations, {len(checked)} local links, "
        "HTML/paper-Figure/SVG/Python/receipt contracts intact."
    )


if __name__ == "__main__":
    main()
