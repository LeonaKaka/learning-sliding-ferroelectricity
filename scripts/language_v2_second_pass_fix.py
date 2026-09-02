from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

PAGE = ROOT / "modules/reproduction-lab.html"
SVG = ROOT / "assets/reproduction-lab/lesson01_tdgl_wall_result.svg"
PYTHON = ROOT / "examples/reproduction-lab/lesson01_tdgl_wall.py"

FORBIDDEN_VISIBLE = (
    "Lesson 01",
    "Gold Test",
    "gold test",
    "Hard gate",
    "validation unit",
    "sanity check",
    "threshold campaign",
    "criticality",
    "无序为零的情形的",
    "Reproduction Lab（复现实验室）（复现实验室）",
    " gate ",
    " window ",
    " authority ",
    " pipeline ",
    " checkpoint ",
    " benchmark ",
    " realization",
    " raw data",
    " steady velocity",
    " sample-specific threshold",
    " effective exponent",
)

REQUIRED_VISIBLE = (
    "Reproduction Lab（复现实验室）01",
    "TDGL Domain Wall（畴壁）",
    "已知答案测试",
    "tanh kink（双曲正切扭结）",
    "order parameter（序参量）",
    "overdamped Langevin（过阻尼朗之万）",
    "Model A（A 型模型）",
    "stationary soliton（定态孤子）",
    "roughness（粗糙度）",
    "structure factor（结构因子）",
    "Laplacian（拉普拉斯算子）",
    "Euler（欧拉）",
    "sliding ferroelectricity（滑移铁电）",
    "phase-field（相场）",
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

    for token in FORBIDDEN_VISIBLE:
        if token in text:
            raise RuntimeError(f"Lab 01 visible Language V2 residue: {token!r}")
    for token in REQUIRED_VISIBLE:
        if token not in text:
            raise RuntimeError(f"Lab 01 required Language V2 form missing: {token!r}")

    if "9.75×10<sup>−5</sup>" not in raw:
        raise RuntimeError("Lab 01 HTML RMSE result changed")
    for token in ("1.415395", "0.0835%"):
        if token not in raw:
            raise RuntimeError(f"Lab 01 HTML locked numerical result missing: {token}")

    equations = soup.select(".eq")
    if len(equations) != 4:
        raise RuntimeError(f"Lab 01 expected 4 equations, found {len(equations)}")

    figure = soup.select_one("figure.fig img")
    if figure is None:
        raise RuntimeError("Lab 01 result Figure missing")
    if figure.get("src") != "../assets/reproduction-lab/lesson01_tdgl_wall_result.svg":
        raise RuntimeError(f"Lab 01 Figure wiring changed: {figure.get('src')}")
    if figure.get("alt") != "TDGL 畴壁向解析扭结弛豫与自由能收敛":
        raise RuntimeError("Lab 01 Figure alt text regressed")

    checked = set()
    for a in soup.find_all("a"):
        path = resolve_local(PAGE, a.get("href"))
        if path is None or path in checked:
            continue
        checked.add(path)
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Lab 01 local link escapes repository: {a.get('href')}") from exc
        if not path.is_file():
            raise RuntimeError(f"Lab 01 local link target missing: {a.get('href')}")
    if PYTHON.resolve() not in checked:
        raise RuntimeError("Lab 01 full Python source link missing")

    if not SVG.is_file() or not PYTHON.is_file():
        raise RuntimeError("Lab 01 source/plot asset missing")

    svg = SVG.read_text(encoding="utf-8")
    for token in (
        "TDGL 畴壁弛豫与自由能收敛",
        "向解析扭结弛豫",
        "解析解",
        "TDGL 下自由能下降",
        "剖面 RMSE = 9.75×10⁻⁵",
        "宽度误差 = 0.0835%",
    ):
        if token not in svg:
            raise RuntimeError(f"Lab 01 SVG expected label/result missing: {token!r}")
    for token in (
        "Relaxation toward analytic kink",
        ">analytic</text>",
        "Free energy decreases under TDGL",
        "profile RMSE =",
        "width error =",
    ):
        if token in svg:
            raise RuntimeError(f"Lab 01 SVG English label residue: {token!r}")

    py = PYTHON.read_text(encoding="utf-8")
    for token in (
        "assert rmse < 5e-4",
        "assert width_error < 5e-3",
        'label="解析扭结"',
        'ax1.set_title("畴壁剖面弛豫")',
        'ax2.set_title("TDGL 下自由能下降")',
    ):
        if token not in py:
            raise RuntimeError(f"Lab 01 Python scientific/plot contract changed: {token!r}")

    print(
        f"Lab 01 seal PASS: {len(equations)} equations, {len(checked)} local links, "
        "HTML/SVG/Python contracts intact."
    )


if __name__ == "__main__":
    main()
