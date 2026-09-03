from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"

TARGET_SOURCE_PAGES = [
    MODULES / "depinning.html",
    MODULES / "disorder-rfim.html",
    MODULES / "numerical-modeling.html",
    MODULES / "current-frontiers.html",
]

SOURCE_RE = re.compile(r'<blockquote\b[^>]*class="[^"]*source-text[^"]*"[^>]*>.*?</blockquote>', re.S)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def insert_before(path: Path, anchor: str, block: str, marker: str) -> None:
    text = read(path)
    require(marker not in text, f"{path.name}: marker already present: {marker}")
    require(text.count(anchor) == 1, f"{path.name}: expected one insertion anchor, found {text.count(anchor)}: {anchor[:80]}")
    write(path, text.replace(anchor, block.rstrip() + "\n" + anchor, 1))


def insert_before_heading_phrase(path: Path, phrase: str, block: str, marker: str) -> None:
    text = read(path)
    require(marker not in text, f"{path.name}: marker already present: {marker}")
    pos = text.find(phrase)
    require(pos >= 0, f"{path.name}: heading phrase not found: {phrase}")
    start = text.rfind("<h2", 0, pos)
    require(start >= 0, f"{path.name}: h2 start not found before: {phrase}")
    write(path, text[:start] + block.rstrip() + "\n" + text[start:])


def insert_before_h2_id(path: Path, h2_id: str, block: str, marker: str) -> None:
    text = read(path)
    require(marker not in text, f"{path.name}: marker already present: {marker}")
    m = re.search(rf'<h2\s+id="{re.escape(h2_id)}"[^>]*>', text)
    require(m is not None, f"{path.name}: h2 id not found: {h2_id}")
    write(path, text[:m.start()] + block.rstrip() + "\n" + text[m.start():])


def insert_after_paragraph_phrase(path: Path, phrase: str, block: str, marker: str) -> None:
    text = read(path)
    require(marker not in text, f"{path.name}: marker already present: {marker}")
    pos = text.find(phrase)
    require(pos >= 0, f"{path.name}: paragraph phrase not found: {phrase}")
    end = text.find("</p>", pos)
    require(end >= 0, f"{path.name}: paragraph close not found after: {phrase}")
    end += len("</p>")
    write(path, text[:end] + "\n" + block.rstrip() + text[end:])


def insert_after_div_phrase(path: Path, phrase: str, block: str, marker: str) -> None:
    text = read(path)
    require(marker not in text, f"{path.name}: marker already present: {marker}")
    pos = text.find(phrase)
    require(pos >= 0, f"{path.name}: div phrase not found: {phrase}")
    start = text.rfind("<div", 0, pos)
    require(start >= 0, f"{path.name}: div start not found before: {phrase}")
    end = text.find("</div>", pos)
    require(end >= 0, f"{path.name}: div close not found after: {phrase}")
    end += len("</div>")
    write(path, text[:end] + "\n" + block.rstrip() + text[end:])


def insert_claim(path: Path, html: str, marker: str) -> None:
    text = read(path)
    require(marker not in text, f"{path.name}: claim marker already present: {marker}")
    pos = text.find('id="claim-check"')
    require(pos >= 0, f"{path.name}: #claim-check not found")
    section_start = text.rfind("<section", 0, pos)
    section_end = text.find("</section>", pos)
    require(section_start >= 0 and section_end >= 0, f"{path.name}: malformed claim-check section")
    write(path, text[:section_end] + html.rstrip() + "\n" + text[section_end:])


def source_receipt() -> dict[str, list[str]]:
    receipt: dict[str, list[str]] = {}
    for path in TARGET_SOURCE_PAGES:
        blocks = SOURCE_RE.findall(read(path))
        receipt[str(path.relative_to(ROOT))] = [hashlib.sha256(x.encode("utf-8")).hexdigest() for x in blocks]
    return receipt


before_sources = source_receipt()

# 05 · Depinning: turn the existing warning into an explicit model-validity boundary,
# without changing the first-read Chauve → Rosso → Ferrero → Wiese sequence.
depinning_block = r'''
<div class="warn" id="qew-validity-boundary"><b>第二遍阅读再加一条模型边界：</b>“测到的指数接近 QEW”不能反过来证明 QEW 就是正确的长波理论。标准 QEW 需要界面仍可稳定表示为单值位移场、弹性近似以谐和且倾斜不变的恢复力为主、动力学处于近似过阻尼的界面运动极限，并且没有必须保留的多界面或塑性自由度。若非线性弹性或法向生长产生 KPZ 型非线性，临界行为可以转入 quenched KPZ（淬火 KPZ，qKPZ）而不是 QEW。<br/><span class="rule">补充理论锚点：Mukerjee &amp; Wiese, Phys. Rev. E 107, 054137 (2023), <a href="https://doi.org/10.1103/PhysRevE.107.054137" rel="noopener" target="_blank">DOI 10.1103/PhysRevE.107.054137</a>。这里引用它是为了限定 QEW 的适用条件，不是把滑移铁电预先归入 qKPZ。</span></div>
'''
insert_before_heading_phrase(MODULES / "depinning.html", "进阶研究方法 A · 坍缩验收判据", depinning_block, 'id="qew-validity-boundary"')

# 06 · Disorder: explicitly separate microscopic disorder class from the depinning fixed point.
disorder_block = r'''
<h3 id="rb-rf-depinning">0.5 · RB 与 RF：微观无序不同，不代表退钉扎不动点一定不同</h3>
<p>这里还要补上一个很容易被省略的尺度层级。RB 与 RF 在微观相关函数、平衡态几何以及非普适尺度上可以明显不同；但进入<strong>标准短程、单分量、过阻尼弹性界面</strong>的退钉扎临界区以后，RG 流并不要求它们继续保持两个不同的临界不动点。Rosso、Le Doussal 与 Wiese 直接对 RB 与 RF 势中的弹性线测量了 functional RG（泛函重整化群，FRG）的有效无序相关函数，发现退钉扎处的普适二阶累积量 Δ(u) 对 RB 与 RF 相同，而这与静力学情形不同。</p>
<div class="note"><b>理论锚点：</b>Rosso, Le Doussal &amp; Wiese, Phys. Rev. B 75, 220201(R) (2007), <a href="https://doi.org/10.1103/PhysRevB.75.220201" rel="noopener" target="_blank">DOI 10.1103/PhysRevB.75.220201</a>；两回路 FRG 也给出“退钉扎时 RF 不动点吸引更短程无序”的结果：Chauve, Le Doussal &amp; Wiese, Phys. Rev. Lett. 86, 1785 (2001), <a href="https://doi.org/10.1103/PhysRevLett.86.1785" rel="noopener" target="_blank">DOI 10.1103/PhysRevLett.86.1785</a>。</div>
<div class="warn"><b>因此要分开两种问题：</b>RF 与 RB 得到不同的 f<sub>c</sub>、速度幅度、有限尺度粗糙度或交叉尺度，<strong>不等于</strong>它们已经属于不同退钉扎普适类；反过来，临界指数彼此相容，也<strong>不能</strong>证明两种微观无序等价。这个结论只在弹性界面映射本身成立以后才适用，不能拿来跨过 RFIM、塑性、多界面或长程 / 非线性弹性等模型边界。</div>
'''
insert_before(MODULES / "disorder-rfim.html", '<h2 id="rfim">1 · Dahmen &amp; Sethna 1996', disorder_block, 'id="rb-rf-depinning"')

# Research Track 1.2: convert the RF/RB distinction into an operational interpretation rule.
research_disorder_block = r'''
<h3 id="rf-rb-interpretation">1.2 · 先分开两个问题：耦合形式不同，临界普适类未必不同</h3>
<div class="twocol"><div class="card"><b>先比较非普适响应</b><p>在同一匹配规则下比较阈值、速度幅度、有限尺度几何、交叉尺度与路径分布。这些差异可以非常有物理意义，但它们首先回答“耦合形式怎样改变可观测响应”。</p></div><div class="card"><b>再检验临界普适性</b><p>只有在单界面映射成立、临界区被独立定位、多个尺度与多个估计量闭合以后，β / ζ / ν 等渐近量才有资格回答“是否流向同一临界不动点”。</p></div></div>
<div class="warn"><b>解释纪律：</b><i>f</i><sub>c</sub><sup>RF</sup> ≠ <i>f</i><sub>c</sub><sup>RB</sup> 不能推出“两个普适类”；β<sup>RF</sup> ≈ β<sup>RB</sup> 也不能推出“两个微观无序相同”。标准弹性界面退钉扎中，RB 与 RF 可以流向相同的 RF 型临界不动点；Rosso, Le Doussal &amp; Wiese 2007 直接测得两者在退钉扎处相同的普适 Δ(u)。<a href="https://doi.org/10.1103/PhysRevB.75.220201" rel="noopener" target="_blank">查看 APS 记录 →</a></div>
'''
insert_before_h2_id(MODULES / "research-track.html", "protocol", research_disorder_block, 'id="rf-rb-interpretation"')

# Research Track model-validity checklist: falsifiable exits before fitting exponents.
research_validity_block = r'''
<h3 id="qew-validity">在拟合 β / ζ / ν 之前，先检查单界面映射是否还成立</h3>
<p>QEW 不是“看到一堵墙以后默认套用”的公式，而是一组可以被数据证伪的长波假设。下面五项至少要逐项检查；任何一项持续失败，都应该先改模型，而不是继续扩大指数拟合。</p>
<div class="flow"><div><b>几何</b><p>畴壁能否长期稳定写成单值 u(y,t)？持续悬垂、封闭小畴、分叉或脱离小畴说明单值表示正在失效。</p></div><div><b>自由度</b><p>真的只有一堵主要界面吗？若 u<sub>1</sub>,u<sub>2</sub>,… 的相对位移本身是慢变量，就不能无条件压成一个 u。</p></div><div><b>弹性核</b><p>恢复力是否近似局域、谐和？若静电 / 应变产生显著 q 依赖，或非线性弹性不可忽略，应检验长程或 qKPZ 等扩展。</p></div><div><b>无序是否淬火</b><p>一次运行中缺陷景观是否近似固定？若自由载流子屏蔽随 φ、E、时间或历史重排，h(r) 不能再被无条件视为静态背景。</p></div><div><b>动力学</b><p>是否处于过阻尼、主要向前的界面运动极限？强惯性、内部畴壁模、显著回退或塑性重排都需要额外动力学自由度。</p></div></div>
<div class="bridge"><b>允许三种科学出口：</b>① 这些检查在目标尺度内成立 → QEW 映射仍是合理候选；② 只有某一项系统偏离 → 明确写出需要的扩展；③ 单值界面或单自由度本身失效 → <strong>“单界面映射失效”就是结果</strong>。第三种不是没做成，而是对传统受驱界面框架适用范围的直接检验。</div>
'''
insert_before_h2_id(MODULES / "research-track.html", "model", research_validity_block, 'id="qew-validity"')

# 07 · Numerical Modeling: distinguish periodic stacking energy from random-periodic disorder.
periodicity_block = r'''
<div class="warn" id="periodicity-boundary"><b>两种“周期”不要混在一起：</b>上面的局域堆垛势满足类似 <span class="eq" style="display:inline-block;padding:2px 7px;margin:0">V(φ+2π/n)=V(φ)</span>，它表示序参量存在等价堆垛极小值；而 random-periodic disorder（随机周期无序）要求的是<strong>钉扎无序相关函数本身</strong>沿界面位移方向重复，例如 <span class="eq" style="display:inline-block;padding:2px 7px;margin:0">Δ(u+M)=Δ(u)</span>。前者存在，不能自动推出后者。Bustingorry, Kolton &amp; Giamarchi 2010 进一步显示，有限横向周期 M 会让随机流形与随机周期粗糙区间发生尺度交叉，因此大尺度模拟中的周期边界条件本身必须作为有限尺寸变量审计。<a href="https://doi.org/10.1103/PhysRevB.82.094202" rel="noopener" target="_blank">Phys. Rev. B 82, 094202 →</a></div>
'''
insert_before_heading_phrase(MODULES / "numerical-modeling.html", "4.5.4 · Γ 最好在静态性质冻结以后再校准", periodicity_block, 'id="periodicity-boundary"')

multi_interface_block = r'''
<div class="twocol" id="multi-interface-extension"><div class="card"><b>单界面约化</b><div class="eq">u(y,t)</div><p>只保留一堵主要畴壁的位置；所有内部结构都被假定为快变量或可忽略修正。</p></div><div class="card"><b>多界面约化</b><div class="eq">u(y,t) → {u<sub>1</sub>(y,t), u<sub>2</sub>(y,t), …}</div><p>当相邻滑移界面的畴壁可独立移动时，相对位移 d<sub>ij</sub>=u<sub>i</sub>−u<sub>j</sub>、中间畴宽度与 wall–wall correlation（畴壁间关联）都成为新的慢可观测量。</p></div></div>
<div class="bridge"><b>这不是“给 QEW 多加一个参数”。</b> 一旦 d<sub>ij</sub> 本身携带慢动力学和分阶段翻转信息，把 {u<sub>i</sub>} 强行投影成单个 u 会丢掉可观测自由度。Dai 2026 因而更适合作为“单界面约化何时失效”的材料级反例，而不是拿来给单界面 QEW 指数做直接背书。</div>
'''
insert_after_paragraph_phrase(MODULES / "numerical-modeling.html", "多层滑移铁电会出现更直接的失效模式", multi_interface_block, 'id="multi-interface-extension"')

# 08 · Current Frontiers: downgrade Baek's evidence cell and promote screening to a model assumption test.
frontier = MODULES / "current-frontiers.html"
text = read(frontier)
old_baek = '<td class="yes">✓ DF-TEM / HAADF-STEM 结构验证</td>'
new_baek = '<td class="partial">结构状态直接验证；翻转过程未做实时空间成像</td>'
require(text.count(old_baek) == 1, f"current-frontiers.html: Baek evidence cell anchor count = {text.count(old_baek)}")
write(frontier, text.replace(old_baek, new_baek, 1))

screening_block = r'''
<div class="audit" id="screening-boundary"><b>材料证据怎样改变模型假设：自由载流子屏蔽不是“再加一个缺陷参数”。</b><p>Liang 2025 的直接结论是 switching pathway（翻转路径）同时受不同界面钉扎中心与化学掺杂相关的 free-carrier screening（自由载流子屏蔽）影响。它<strong>没有</strong>直接证明 QEW 已失效；但它让“无序在一次动力学过程中严格淬火”从默认前提变成了必须检验的假设。如果有效局域景观会随极化状态、外场、时间或历史重排，那么更一般的写法应允许 h(r) → h<sub>eff</sub>(r,φ,E,t,history)，此时固定的 h(r) 只能作为受控近似。</p></div>
'''
insert_after_div_phrase(frontier, "前沿判断：", screening_block, 'id="screening-boundary"')

# Concept Paths: keep 5-step structure, strengthen only the RF/RB stop condition.
concept = MODULES / "concept-paths.html"
text = read(concept)
old_stop_tail = '要叫 RF、RB 或 RFIM，还需要说明它耦合到什么自由度、相关函数是什么、粗粒化后哪些结构被保留。</div>'
new_stop_tail = '要叫 RF、RB 或 RFIM，还需要说明它耦合到什么自由度、相关函数是什么、粗粒化后哪些结构被保留。即使 RF 与 RB 给出不同阈值或有限尺度几何，也不能据此宣布不同退钉扎普适类；反过来，临界指数相容也不能证明两种微观无序等价。</div>'
require(text.count(old_stop_tail) == 1, f"concept-paths.html: disorder stop anchor count = {text.count(old_stop_tail)}")
write(concept, text.replace(old_stop_tail, new_stop_tail, 1))

# L10/L11: add diagnostics without altering any PASS / NOT PASSED decision.
l10_block = r'''
<div class="figure-note" id="periodic-crossover-diagnostic"><b>还要排除一种有限尺寸机制：</b>本课的界面在位移方向使用有限横向周期 M。随机周期介质的研究表明，M 可以引入 random-manifold → random-periodic（随机流形 → 随机周期）粗糙度交叉；因此 ζ 随尺寸漂移时，不能只问“L 是否还不够大”，还要检查横向周期与纵向尺寸的共同标度。<strong>当前两尺寸数据并没有证明已经发生这种交叉</strong>，所以它只是下一轮应独立排除的诊断假设，不能拿来解释或挽救本课未通过的热力学 ζ 闭合。<a href="https://doi.org/10.1103/PhysRevB.82.094202" rel="noopener" target="_blank">理论来源 →</a></div>
'''
insert_before(MODULES / "reproduction-lab-10.html", "\n<h2>5 · 可复查数据</h2>", l10_block, 'id="periodic-crossover-diagnostic"')

l11_block = r'''
<div class="warn" id="transverse-geometry-diagnostic"><b>横向几何不是附属参数：</b>论文 Fig.2 已经用 M=kL<sup>ζ</sup> 明确展示临界力的有限尺寸行为依赖纵横比方案。更一般的随机周期研究也表明横向周期 M 能控制随机流形 / 随机周期交叉。因此当前 ν 的尺寸区间漂移不能被唯一归因于“样本还少”或“L 还小”；后续若要闭合 ν，应把 k 或 M 的变化作为独立有限几何检验。<strong>这条诊断不改变本课结论：</strong>当前尺寸区间稳定性仍然未通过，普适 ν 仍不授权。</div>
'''
insert_before(MODULES / "reproduction-lab-11.html", "\n<h2>4 · 分布坍缩为什么也不能单独救场？</h2>", l11_block, 'id="transverse-geometry-diagnostic"')

# Add four evidence→claim questions; keep them inside the existing final claim-check section.
insert_claim(MODULES / "depinning.html", r'''
<details><summary>如果 β、ζ 很接近 QEW 文献值，能否反过来证明滑移铁电畴壁一定属于 QEW？</summary><p><span class="answer">答案：不能。</span> 指数相容只是必要线索之一。还要独立检查单值界面、弹性核、动力学与自由度是否满足 QEW 的长波假设；如果这些条件失效，数值接近可能只是有限尺度巧合或交叉区。</p></details>
''', "反过来证明滑移铁电畴壁一定属于 QEW")

insert_claim(MODULES / "disorder-rfim.html", r'''
<details><summary>RF 与 RB 得到不同的临界阈值，能否据此宣布它们属于不同退钉扎普适类？</summary><p><span class="answer">答案：不能。</span> 阈值和交叉尺度是非普适量；在标准弹性界面退钉扎中，微观 RB 与 RF 可以流向相同的 RF 型临界不动点。要区分普适类，必须比较有效临界标度，同时先证明界面映射适用。</p></details>
''', "不同的临界阈值，能否据此宣布")

insert_claim(MODULES / "numerical-modeling.html", r'''
<details><summary>局域堆垛势 V(φ) 是周期函数，是否因此可以把界面无序称为 random-periodic（随机周期无序）？</summary><p><span class="answer">答案：不能。</span> 周期堆垛势描述序参量的等价极小值；随机周期类别要求钉扎无序相关函数沿界面位移方向周期重复。两种“周期”属于不同模型层级。</p></details>
''', "是否因此可以把界面无序称为 random-periodic")

insert_claim(MODULES / "current-frontiers.html", r'''
<details><summary>Liang 观察到自由载流子屏蔽影响翻转路径，是否已经直接证明淬火无序 QEW 失效？</summary><p><span class="answer">答案：没有。</span> 这项实验直接支持 screening 会参与路径选择；它进一步提出一个必须检验的问题：有效景观在目标时间尺度内是否仍可近似为固定的淬火无序。只有观察到与状态 / 时间 / 历史耦合的景观重排并证明它影响目标界面动力学，才有资格升级为模型失效证据。</p></details>
''', "是否已经直接证明淬火无序 QEW 失效")

# Update the existing claim-check count seal without weakening any old anchors.
claim_seal = ROOT / "scripts" / "claim_checks_seal.py"
text = read(claim_seal)
for old, new in (
    ("'depinning.html': 4,", "'depinning.html': 5,"),
    ("'disorder-rfim.html': 4,", "'disorder-rfim.html': 5,"),
    ("'numerical-modeling.html': 4,", "'numerical-modeling.html': 5,"),
    ("'current-frontiers.html': 4,", "'current-frontiers.html': 5,"),
    ("if total != 28:", "if total != 32:"),
    ("claim-check total drifted: {total}", "claim-check total drifted after Science V3: {total}"),
    ("(28 total)", "(32 total)"),
):
    require(old in text, f"claim_checks_seal.py: missing anchor {old}")
    text = text.replace(old, new, 1)
write(claim_seal, text)

# Confirm this update never touched any original paper-text block, then persist a receipt.
after_sources = source_receipt()
require(before_sources == after_sources, "Science V3 changed one or more .source-text blocks")
receipt_path = ROOT / "scripts" / "science_v3_source_text_receipt.json"
write(receipt_path, json.dumps({"algorithm": "sha256", "blocks": after_sources}, ensure_ascii=False, indent=2) + "\n")

science_seal = r'''from __future__ import annotations

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

    print("SCIENCE V3 SEAL PASS: RF/RB fixed-point boundary, QEW validity, periodicity crossover, screening, multi-interface mapping, Baek evidence level, L10/L11 diagnostics, and source-text hashes locked.")


if __name__ == "__main__":
    main()
'''
write(ROOT / "scripts" / "science_v3_seal.py", science_seal)

science_workflow = r'''name: Science V3 seal

on:
  workflow_dispatch:
  push:
    paths:
      - 'modules/depinning.html'
      - 'modules/disorder-rfim.html'
      - 'modules/numerical-modeling.html'
      - 'modules/current-frontiers.html'
      - 'modules/research-track.html'
      - 'modules/concept-paths.html'
      - 'modules/reproduction-lab-10.html'
      - 'modules/reproduction-lab-11.html'
      - 'scripts/science_v3_seal.py'
      - 'scripts/science_v3_source_text_receipt.json'
      - 'scripts/claim_checks_seal.py'
      - 'scripts/language_v2_second_pass.py'
      - 'scripts/site_gap_teaching_seal.py'
      - 'scripts/concept_paths_seal.py'
      - '.github/workflows/science-v3-seal.yml'

permissions:
  contents: read

jobs:
  science-v3:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install parser
        run: python -m pip install --disable-pip-version-check beautifulsoup4
      - name: Verify Science V3 scientific boundaries
        run: python scripts/science_v3_seal.py
      - name: Verify Language V2 remains read-only clean
        run: python scripts/language_v2_second_pass.py
      - name: Verify Teaching V2 order and scientific anchors
        run: python scripts/site_gap_teaching_seal.py
      - name: Verify Concept Paths structure and stop conditions
        run: python scripts/concept_paths_seal.py
      - name: Verify evidence-to-claim checks
        run: python scripts/claim_checks_seal.py
      - name: Verify Module 07 first-read structure
        run: python scripts/module07_teaching_seal.py
      - name: Verify Module 08 evidence frame
        run: python scripts/module08_teaching_seal.py
'''
write(ROOT / ".github" / "workflows" / "science-v3-seal.yml", science_workflow)

# Final internal sanity checks before the workflow commits anything.
for page, marker in (
    (MODULES / "depinning.html", 'id="qew-validity-boundary"'),
    (MODULES / "disorder-rfim.html", 'id="rb-rf-depinning"'),
    (MODULES / "research-track.html", 'id="qew-validity"'),
    (MODULES / "numerical-modeling.html", 'id="periodicity-boundary"'),
    (MODULES / "current-frontiers.html", 'id="screening-boundary"'),
    (MODULES / "reproduction-lab-10.html", 'id="periodic-crossover-diagnostic"'),
    (MODULES / "reproduction-lab-11.html", 'id="transverse-geometry-diagnostic"'),
):
    require(marker in read(page), f"post-write marker missing: {page.name} {marker}")

print("SCIENCE V3 APPLY PASS: content staged; source-text blocks unchanged; persistent read-only seal/workflow written.")
