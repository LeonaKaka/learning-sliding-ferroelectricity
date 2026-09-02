from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

PAGE = ROOT / "modules/reproduction-lab-02.html"
PAPER_FIGURE = ROOT / "assets/interface-scaling/caballero2020-fig1-bulk-to-interface.png"
SVG = ROOT / "assets/reproduction-lab/lesson02_2d_wall_extract.svg"
PYTHON = ROOT / "examples/reproduction-lab/lesson02_2d_wall_extract.py"

FORBIDDEN_VISIBLE = (
    "Lesson 02",
    "Gold Test",
    "gold test",
    "topology gate",
    "periodic boundary",
    "论文 Figure",
    "scaling curve",
    "small-system",
    "thumbnail reproduction",
    "prediction",
    "复现实验室（复现实验室）",
    "论文图 并排",
    "强调的 拓扑",
    "原论文图 告诉",
    "论文展示 二维",
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
    "Reproduction Lab（复现实验室）02",
    "已知答案测试",
    "model reduction（模型约化）",
    "Ginzburg–Landau（GL）",
    "diffuse wall（弥散畴壁）",
    "roughness（粗糙度）",
    "structure factor（结构因子）",
    "Laplacian（拉普拉斯算子）",
    "gradient energy（梯度能）",
    "line tension（线张力）",
    "elastic line（弹性线）",
    "single-valued mapping（单值映射）",
    "phase field（相场）",
    "thermal white noise（热白噪声）",
    "Edwards–Wilkinson（EW）",
    "拓扑判据",
    "周期边界",
)

LOCKED_RESULTS = (
    "48/48",
    "2.629×10<sup>−3</sup>",
    "2.764×10<sup>−5</sup>",
    "4.020×10<sup>−4</sup>",
    "0.870339",
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
            raise RuntimeError(f"Lab 02 visible Language V2 residue: {token!r}")
    for token in REQUIRED_VISIBLE:
        if token not in text:
            raise RuntimeError(f"Lab 02 required Language V2 form missing: {token!r}")

    for token in LOCKED_RESULTS:
        if token not in raw:
            raise RuntimeError(f"Lab 02 locked numerical result missing: {token}")

    equations = soup.select(".eq")
    if len(equations) != 5:
        raise RuntimeError(f"Lab 02 expected 5 equations, found {len(equations)}")

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 02 expected 2 Figures, found {len(figures)}")
    expected_srcs = [
        "../assets/interface-scaling/caballero2020-fig1-bulk-to-interface.png",
        "../assets/reproduction-lab/lesson02_2d_wall_extract.svg",
    ]
    actual_srcs = [img.get("src") for img in figures]
    if actual_srcs != expected_srcs:
        raise RuntimeError(f"Lab 02 Figure wiring changed: {actual_srcs}")
    expected_alts = [
        "Caballero 2020 图 1：二维 GL 体场与提取界面",
        "本课二维 GL 场、提取畴壁、B(r) 与解析剖面对照",
    ]
    actual_alts = [img.get("alt") for img in figures]
    if actual_alts != expected_alts:
        raise RuntimeError(f"Lab 02 Figure alt text regressed: {actual_alts}")

    checked = set()
    for a in soup.find_all("a"):
        path = resolve_local(PAGE, a.get("href"))
        if path is None or path in checked:
            continue
        checked.add(path)
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(f"Lab 02 local link escapes repository: {a.get('href')}") from exc
        if not path.is_file():
            raise RuntimeError(f"Lab 02 local link target missing: {a.get('href')}")
    if PYTHON.resolve() not in checked:
        raise RuntimeError("Lab 02 full Python source link missing")

    for path in (PAPER_FIGURE, SVG, PYTHON):
        if not path.is_file():
            raise RuntimeError(f"Lab 02 required source/asset missing: {path.relative_to(ROOT)}")

    svg = SVG.read_text(encoding="utf-8")
    if "NotoSansCJKsc" not in svg:
        raise RuntimeError("Lab 02 SVG no longer contains the CJK plot font")
    for token in (
        "2D bulk field after relaxation",
        "initial wavy wall",
        "final extracted wall",
        "Diffuse field -> single-valued interface",
        "Flat-wall gold test",
        "mean numerical profile",
        "Reproduction Lab · Lesson 02",
    ):
        if token in svg:
            raise RuntimeError(f"Lab 02 SVG English label residue: {token!r}")

    py = PYTHON.read_text(encoding="utf-8")
    for token in (
        'plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "DejaVu Sans"]',
        "assert wall_rms < 5e-3",
        "assert wall_max < 8e-3",
        "assert B_max < 5e-5",
        "assert profile_rmse < 8e-4",
        "assert energy_drop > 0.0",
        "assert np.all(np.diff(energy_F) <= 2e-9)",
        'label=r"提取的 $u(y)$"',
        'ax.set_title("弛豫后的二维体场")',
        'label="初始起伏畴壁"',
        'label="最终提取畴壁"',
        'ax.set_title("弥散场 → 单值界面")',
        'ax.set_title(r"平直畴壁已知答案测试：$B(r)\\rightarrow0$")',
        'label="数值平均剖面"',
        'label="解析 tanh"',
        'ax.set_title(f"横向剖面 RMSE = {profile_rmse:.2e}")',
        '"复现实验室 · 第 02 课 · 二维 GL 场 → u(y) → B(r)"',
    ):
        if token not in py:
            raise RuntimeError(f"Lab 02 Python scientific/plot contract changed: {token!r}")

    print(
        f"Lab 02 seal PASS: {len(equations)} equations, {len(figures)} Figures, "
        f"{len(checked)} local links; HTML/SVG/Python contracts intact."
    )


if __name__ == "__main__":
    main()
