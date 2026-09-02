from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-06.html"
PYTHON = ROOT / "examples/reproduction-lab/lesson06_disordered_geometry.py"
SVG = ROOT / "assets/reproduction-lab/lesson06_disordered_geometry_checkpoint.svg"
RECEIPT = ROOT / "assets/reproduction-lab/lesson06_disordered_geometry_checkpoint.txt"
PAPER_FIG = ROOT / "assets/reproduction-lab/caballero2020-fig5-disordered-geometry.webp"

LOCKED_RESULTS = (
    "1.227%", "6.122%", "0.538906", "0.509213", "0.694308",
    "0.664796", "0.982981", "1.371256", "0.077925",
)
MACHINE_MARKER = "CROSS-MODEL GEOMETRY PASS; ASYMPTOTIC ZETA GATE NOT PASSED"
EXPECTED_FIGURES = (
    "../assets/reproduction-lab/caballero2020-fig5-disordered-geometry.webp",
    "../assets/reproduction-lab/lesson06_disordered_geometry_checkpoint.svg",
)
EXPECTED_ALTS = (
    "Caballero 2020 图 5：含无序 GL 与 EW 的粗糙度和结构因子",
    "本课含无序 GL 与 EW 几何阶段验证",
)
FORBIDDEN_VISIBLE = (
    "checkpoint", "realizations", "estimator", "fit window", "benchmark",
    "Paper1", "Paper2", "Lesson0", "pinned", " moving", "modes", " weight",
    "consistency",
)
REQUIRED_VISIBLE = (
    "random-bond（随机键）",
    "Ginzburg–Landau（GL）",
    "Edwards–Wilkinson（EW）",
    "roughness（粗糙度）",
    "structure factor（结构因子）",
    "Laplacian（拉普拉斯算子）",
    "depinning（退钉扎）",
    "跨模型映射通过",
    "渐近 ζ 判据：未通过。",
)
PYTHON_LOCKS = (
    "T = 0.05",
    "epsilon = 0.1",
    "Lx, Ly = 64.0, 128.0",
    "n_realizations = 8",
    "t_final = 1000.0",
    "n_steps = int(round(t_final / dt))",
    "du = 0.1",
    "M = 1024",
    "zeta = base / math.sqrt(du)",
    "b_window = (r >= 4.0) & (r <= 32.0)",
    "b_fit = (r >= 4.0) & (r <= 20.0)",
    "q_fit = (q >= 0.1) & (q <= 0.5)",
    "assert B_median_rel < 0.05, B_median_rel",
    "assert S_binned_median_rel < 0.10, S_binned_median_rel",
    "assert abs(zeta_B_gl - zeta_B_ew) < 0.06",
    "assert abs(zeta_S_gl - zeta_S_ew) < 0.06",
    "assert 0.95 < A_mean < 1.02",
    "assert 1.20 < W_mean < 1.50",
    "assert abs(zeta_B_gl - zeta_S_gl) > 0.10",
    "assert abs(zeta_B_ew - zeta_S_ew) > 0.10",
    MACHINE_MARKER,
    'label="二维 GL 提取畴壁"',
    'label="一维 EW"',
    'label="GL 对数分箱"',
    'label="EW 对数分箱"',
    'ax.set_title("t=1000 的实空间粗糙度")',
    'ax.set_title("傅里叶空间结构因子")',
    'ax.set_title("代表性界面")',
    'ax.set_ylabel("有效 ζ")',
    'ax.set_title("几何映射先通过，渐近指数尚未闭合")',
    'fig.suptitle("复现实验室 · 第 06 课 · 含无序 GL 与 EW 几何对照", fontsize=14)',
)
SVG_REQUIRED = (
    "t=1000 的实空间粗糙度",
    "傅里叶空间结构因子",
    "代表性界面",
    "几何映射先通过，渐近指数尚未闭合",
    "复现实验室 · 第 06 课 · 含无序 GL 与 EW 几何对照",
)
SVG_FORBIDDEN = (
    "Real-space roughness at t=1000",
    "Fourier-space structure factor",
    "Representative interfaces",
    "Mapping passes before asymptotic exponent closes",
    "Reproduction Lab · Lesson 06 · disordered GL vs EW geometry",
)


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
            raise RuntimeError(f"Lab 06 local link escapes repository: {value}") from exc
        if not resolved.exists():
            raise RuntimeError(f"Lab 06 broken local link: {value}")


def main() -> None:
    for path in (TARGET, PYTHON, SVG, RECEIPT, PAPER_FIG):
        if not path.exists():
            raise RuntimeError(f"Lab 06 required artifact missing: {path.relative_to(ROOT)}")

    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    if title != "Reproduction Lab（复现实验室）06 · 含无序 GL ↔ EW 几何":
        raise RuntimeError(f"Lab 06 title drifted: {title!r}")

    visible = visible_text(soup)
    for token in REQUIRED_VISIBLE:
        if token not in visible:
            raise RuntimeError(f"Lab 06 required Language V2 text missing: {token}")
    for token in FORBIDDEN_VISIBLE:
        if token in visible:
            raise RuntimeError(f"Lab 06 ordinary workflow English remains visible: {token}")
    for token in LOCKED_RESULTS:
        if token not in raw:
            raise RuntimeError(f"Lab 06 locked result missing: {token}")

    equations = soup.select(".eq")
    if len(equations) != 4:
        raise RuntimeError(f"Lab 06 expected 4 equation blocks, found {len(equations)}")

    figures = soup.select("figure.fig img")
    if tuple(x.get("src") for x in figures) != EXPECTED_FIGURES:
        raise RuntimeError("Lab 06 Figure wiring drifted")
    if tuple(x.get("alt") for x in figures) != EXPECTED_ALTS:
        raise RuntimeError("Lab 06 Figure alt text drifted")

    pre_text = "\n".join(x.get_text() for x in soup.select("pre"))
    if MACHINE_MARKER not in pre_text:
        raise RuntimeError("Lab 06 visible machine verdict marker changed")
    verify_local_links(soup)

    py = PYTHON.read_text(encoding="utf-8")
    for token in PYTHON_LOCKS:
        if token not in py:
            raise RuntimeError(f"Lab 06 Python contract drifted: {token}")

    receipt = RECEIPT.read_text(encoding="utf-8")
    receipt_locks = (
        "B median rel, r=4..32  = 1.227%",
        "S log-bin median rel   = 6.122%",
        "zeta_B GL / EW         = 0.538906 / 0.509213",
        "zeta_S GL / EW         = 0.694308 / 0.664796",
        "GL fitted A, w         = 0.982981, 1.371256",
        "GL profile-fit RMSE    = 0.077925",
        MACHINE_MARKER,
    )
    for token in receipt_locks:
        if token not in receipt:
            raise RuntimeError(f"Lab 06 receipt drifted: {token}")

    svg = SVG.read_text(encoding="utf-8")
    for token in SVG_REQUIRED:
        if token not in svg:
            raise RuntimeError(f"Lab 06 localized SVG label missing: {token}")
    for token in SVG_FORBIDDEN:
        if token in svg:
            raise RuntimeError(f"Lab 06 old English SVG label remains: {token}")
    if "NotoSansCJK" not in svg:
        raise RuntimeError("Lab 06 SVG does not contain embedded CJK glyph definitions")

    print("Lab 06 read-only Language V2 seal PASS; science/results/Figures/links preserved.")


if __name__ == "__main__":
    main()
