from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"
SOURCE_RE = re.compile(r'<blockquote\b[^>]*class="[^"]*source-text[^"]*"[^>]*>.*?</blockquote>', re.S)

ANCHORS = {
    "depinning.html": (
        'id="qew-validity-boundary"',
        '指数接近 QEW”不能反过来证明 QEW',
        'quenched KPZ（淬火 KPZ，qKPZ）',
        '反过来证明滑移铁电畴壁一定属于 QEW',
    ),
    "disorder-rfim.html": (
        'id="rb-rf-depinning"',
        '微观无序不同，不代表退钉扎不动点一定不同',
        '不等于</strong>它们已经属于不同退钉扎普适类',
        '临界指数彼此相容，也<strong>不能</strong>证明两种微观无序等价',
        '不同的临界阈值，能否据此宣布',
    ),
    "research-track.html": (
        'id="rf-rb-interpretation"',
        '耦合形式不同，临界普适类未必不同',
        'id="qew-validity"',
        '在拟合 β / ζ / ν 之前，先检查单界面映射是否还成立',
        '无序是否淬火',
        '单界面映射失效”就是结果',
    ),
    "numerical-modeling.html": (
        'id="periodicity-boundary"',
        '两种“周期”不要混在一起',
        'Δ(u+M)=Δ(u)',
        'id="multi-interface-extension"',
        'd<sub>ij</sub>=u<sub>i</sub>−u<sub>j</sub>',
        '是否因此可以把界面无序称为 random-periodic',
    ),
    "current-frontiers.html": (
        '结构状态直接验证；翻转过程未做实时空间成像',
        'id="mechanism-reconcile"',
        '这些结果真的互相矛盾吗？先把结构条件对齐。',
        '不能推出“任何无预存畴壁的滑移铁电都无法翻转”',
        '不能据此否定多畴样品中的畴壁介导翻转',
        '单一畴壁坐标未必够用',
        'id="screening-boundary"',
        '无序在一次动力学过程中严格淬火',
        '是否已经直接证明淬火无序 QEW 失效',
    ),
    "concept-paths.html": (
        '即使 RF 与 RB 给出不同阈值或有限尺度几何，也不能据此宣布不同退钉扎普适类',
        '临界指数相容也不能证明两种微观无序等价',
    ),
    "reproduction-lab-10.html": (
        'id="periodic-crossover-diagnostic"',
        '当前两尺寸数据并没有证明已经发生这种交叉',
        '不能拿来解释或挽救本课未通过的热力学 ζ 闭合',
    ),
    "reproduction-lab-11.html": (
        'id="transverse-geometry-diagnostic"',
        '后续若要闭合 ν，应把 k 或 M 的变化作为独立有限几何检验',
        '普适 ν 仍不授权',
    ),
}

FORBIDDEN_NEW = (
    'mapping checkpoint',
    'QEW gate',
    'universality gate',
    'fit-window gate',
    'Science V3 workflow',
)


def main() -> None:
    for name, anchors in ANCHORS.items():
        raw = (MODULES / name).read_text(encoding="utf-8")
        for anchor in anchors:
            if anchor not in raw:
                raise RuntimeError(f"{name}: Science V3 anchor missing: {anchor}")
        for token in FORBIDDEN_NEW:
            if token in raw:
                raise RuntimeError(f"{name}: Science V3 visible prose residue: {token}")

    l10 = (MODULES / "reproduction-lab-10.html").read_text(encoding="utf-8")
    l11 = (MODULES / "reproduction-lab-11.html").read_text(encoding="utf-8")
    for locked in (
        '小尺寸 QEW 超粗糙特征：通过',
        '热力学 ζ 闭合：未通过',
    ):
        if locked not in l10:
            raise RuntimeError(f"L10 locked result drifted: {locked}")
    for locked in (
        '尺寸区间稳定性：未通过',
        '普适 ν 结论：不授权',
    ):
        if locked not in l11:
            raise RuntimeError(f"L11 locked result drifted: {locked}")

    receipt = json.loads((ROOT / "scripts" / "science_v3_source_text_receipt.json").read_text(encoding="utf-8"))
    for rel, expected in receipt["blocks"].items():
        raw = (ROOT / rel).read_text(encoding="utf-8")
        blocks = SOURCE_RE.findall(raw)
        actual = [hashlib.sha256(x.encode("utf-8")).hexdigest() for x in blocks]
        if actual != expected:
            raise RuntimeError(f"{rel}: original .source-text receipt mismatch")

    print("SCIENCE V3 SEAL PASS: RF/RB fixed-point boundary, QEW validity, periodicity crossover, screening, multi-interface mapping, Baek evidence level, mechanism reconciliation, L10/L11 diagnostics, and source-text hashes locked.")


if __name__ == "__main__":
    main()
