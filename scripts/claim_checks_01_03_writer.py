from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "modules"

CSS = '''
.claim-check{margin:54px 0 30px;padding-top:28px;border-top:1px solid var(--l)}.claim-check h2{margin:0 0 8px}.claim-check .quiz-intro{margin:0 0 15px;color:#666}.claim-check details{margin:9px 0;border:1px solid var(--l);border-radius:10px;background:var(--p);padding:12px 14px}.claim-check summary{cursor:pointer;font-weight:650}.claim-check details p{margin:10px 0 2px}.claim-check .answer{font-weight:700}
'''

QUESTIONS = {
    "foundations.html": [
        (
            "Wu & Li 的单胞滑移能垒较低，所以真实器件一定通过整层同步相干滑移完成翻转。对还是错？",
            "答案：错。",
            "低能垒只说明一条给定结构通道在能量上可能可达；它没有决定真实器件由整层同步滑移、成核、畴壁传播还是局域路径选择来完成翻转。结构路径与动力学路径必须分开。",
        ),
        (
            "Vizner Stern 的 KPFM 黑白畴可以直接当作‘测到了极化矢量 Pz 本身’吗？",
            "答案：不能。",
            "KPFM 直接测的是表面电势。AB/BA 结构归属、稳定的电势差、跨样品重复性与极化计算共同支持界面极化解释，但不能把仪器的直接可观测量偷换成极化矢量本身。",
        ),
        (
            "Meng 的三层中间态和 Fig. 3e 是否已经唯一证明‘两个界面必定按固定顺序逐个翻转’？",
            "答案：没有。",
            "层数对照与稳定异常状态支持多界面偶极组合和逐界面翻转模型；Fig. 3e 是与实验相容的机制图，不是原子级动力学录像。真正的路径顺序还需要后续空间或界面分辨证据。",
        ),
    ],
    "switching-pathways.html": [
        (
            "Yang 中不同循环或不同器件的 E_c 不一样，是否就说明材料本征滑移能垒本身在变化？",
            "答案：不一定。",
            "作者把 E_c 的变化与随机分布的局域钉扎势联系起来：预存畴壁何时从不同钉扎中心释放就会改变表观矫顽场。因此 E_c 在这里不能自动等于均匀晶体的本征能垒或热力学 f_c。",
        ),
        (
            "Sui 中 Path 2 能垒更低，而且看到了 ACACAC / ε-InSe 中间结构，能否把 Path 2 当成所有滑移铁电器件的唯一翻转轨迹？",
            "答案：不能。",
            "实验直接看到的是 InSe:Y 在电子束诱导场下的原子级相对滑移；Path 1/2 与能垒来自该材料的计算。中间结构让 Path 2 更有物理依据，但驱动条件、材料和可用路径都不能无条件外推到其他体系。",
        ),
        (
            "Liang 的 ABA / BAB 中间态是否意味着出现了一个与路径无关的新‘第三体相’？",
            "答案：不是。",
            "三层有两个界面；一个界面畴壁先释放、另一个仍未翻转时就会形成 ABA 或 BAB。不同钉扎中心的强弱改变释放顺序，所以中间态本身正是路径依赖的界面堆垛组合。",
        ),
    ],
    "domain-walls.html": [
        (
            "只要 AB→BA 的结构能垒低，面外电场 E_z 就足以直接推动完整高对称单畴沿某个面内方向滑动。对还是错？",
            "答案：错。",
            "高对称 AB/BA 的 C3 对称性会让可选面内方向等价；没有非对角响应时，E_z 不能自动选出唯一横向驱动力。畴壁的局域对称性破缺正是 Ke/Wang 机制链里的关键。",
        ),
        (
            "Chen 的‘no domain wall, no polarization reversal’是否已经证明所有滑移铁电都必须预先存在畴壁才能翻转？",
            "答案：没有。",
            "这是 Chen 在其 3R-MoS2 模型、样品和器件条件下的强机制结论。Baek 的完全共格单畴 3R-TMD 结果提供了结构条件反例，因此更准确的问题是‘什么结构条件选择畴壁路径’。",
        ),
        (
            "KPFM 里看到畴壁被气泡钉住、提高偏压后越过障碍，是否已经建立了临界退钉扎普适性？",
            "答案：远远不够。",
            "这能证明局域钉扎/解钉事件，但 critical depinning 还需要独立阈值、恒场稳态 v(E)、粗糙度、系统尺寸和临界指数等证据链。‘越过一个障碍’不能直接升级成普适类。",
        ),
    ],
}


def extract(raw: str, pattern: str) -> list[str]:
    return re.findall(pattern, raw, flags=re.S | re.I)


def section_html(items: list[tuple[str, str, str]]) -> str:
    details = "".join(
        f'<details><summary>{q}</summary><p><span class="answer">{a}</span> {why}</p></details>'
        for q, a, why in items
    )
    return (
        '<section class="claim-check" id="claim-check">'
        '<h2>结论边界 · 判断自测</h2>'
        '<p class="quiz-intro">先判断，再展开答案。这里不考名词，专门检查你有没有把“证据支持”写成“证据已经证明”。</p>'
        f'{details}</section>'
    )


def main() -> None:
    changed: list[str] = []
    for filename, items in QUESTIONS.items():
        page = MOD / filename
        raw = page.read_text(encoding="utf-8")
        if 'id="claim-check"' in raw or 'class="claim-check"' in raw:
            raise RuntimeError(f"{filename}: claim check already exists")

        before_sources = extract(raw, r'<blockquote\b[^>]*class=["\'][^"\']*source-text[^"\']*["\'][^>]*>.*?</blockquote>')
        before_figures = extract(raw, r'<figure\b[^>]*>.*?</figure>')
        before_guides = extract(raw, r'<div\b[^>]*class=["\'][^"\']*fig-read[^"\']*["\'][^>]*>.*?</div></div></div>')
        before_eqs = extract(raw, r'<div\b[^>]*class=["\'][^"\']*\beq\b[^"\']*["\'][^>]*>.*?</div>')
        before_hrefs = re.findall(r'href=["\']([^"\']+)["\']', raw, flags=re.I)

        if raw.count('<div class="next">') != 1:
            raise RuntimeError(f"{filename}: expected exactly one final navigation block")
        updated = raw.replace('</style>', CSS + '</style>', 1)
        updated = updated.replace('<div class="next">', section_html(items) + '<div class="next">', 1)

        after_sources = extract(updated, r'<blockquote\b[^>]*class=["\'][^"\']*source-text[^"\']*["\'][^>]*>.*?</blockquote>')
        after_figures = extract(updated, r'<figure\b[^>]*>.*?</figure>')
        after_guides = extract(updated, r'<div\b[^>]*class=["\'][^"\']*fig-read[^"\']*["\'][^>]*>.*?</div></div></div>')
        after_eqs = extract(updated, r'<div\b[^>]*class=["\'][^"\']*\beq\b[^"\']*["\'][^>]*>.*?</div>')
        after_hrefs = re.findall(r'href=["\']([^"\']+)["\']', updated, flags=re.I)

        if before_sources != after_sources:
            raise RuntimeError(f"{filename}: source-text changed")
        if before_figures != after_figures:
            raise RuntimeError(f"{filename}: figures/captions changed")
        if before_guides != after_guides:
            raise RuntimeError(f"{filename}: Figure Reading V2 guides changed")
        if before_eqs != after_eqs:
            raise RuntimeError(f"{filename}: equations changed")
        if before_hrefs != after_hrefs:
            raise RuntimeError(f"{filename}: links changed")
        if updated.count('<details>') - raw.count('<details>') != len(items):
            raise RuntimeError(f"{filename}: wrong claim-check count")

        page.write_text(updated, encoding="utf-8")
        changed.append(filename)

    print("CLAIM CHECK 01-03 WRITER PASS:", ", ".join(changed))


if __name__ == "__main__":
    main()
