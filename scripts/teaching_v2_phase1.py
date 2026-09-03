from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

P04 = ROOT / "modules/pinning-creep.html"
P05 = ROOT / "modules/depinning.html"
P06 = ROOT / "modules/disorder-rfim.html"


def snapshot(raw: str) -> dict:
    soup = BeautifulSoup(raw, "html.parser")
    return {
        "source_text": [str(x) for x in soup.select(".source-text")],
        "hrefs": [x.get("href") for x in soup.find_all("a")],
        "images": [(x.get("src"), x.get("alt")) for x in soup.find_all("img")],
        "eq": [x.get_text(" ", strip=True) for x in soup.select(".eq")],
    }


def assert_locked(before: dict, after_raw: str, page: str) -> None:
    after = snapshot(after_raw)
    for key in ("source_text", "hrefs", "images", "eq"):
        if before[key] != after[key]:
            raise RuntimeError(f"{page}: locked {key} changed")


def replace_once(raw: str, old: str, new: str, label: str) -> str:
    count = raw.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return raw.replace(old, new, 1)


def improve_04() -> None:
    raw = P04.read_text(encoding="utf-8")
    before = snapshot(raw)
    out = raw

    h1 = '<h2>1 · Tybell 2002：先从速度律建立蠕变的实验语言</h2>'
    first_read = (
        '<div class="paper-role"><b>第一次读这一章：</b>'
        '先只抓三件事——Tybell 看“速度为什么高度非线性”，Paruch 看“粗糙度怎样被定义和测量”，'
        'Kim 看“统计钉扎如何落回单个局域事件”。标成“进阶研究方法”的段落第二遍再读，不影响主线。</div>\n'
    )
    out = replace_once(out, h1, first_read + h1, "04 first-read route")
    out = replace_once(
        out,
        '<h2 id="roughness-gate">2.7 · 粗糙度验收判据：ζ 不是从任意双对数直线里读出来</h2>',
        '<h2 id="roughness-gate">进阶研究方法 · 粗糙度验收判据：ζ 不是从任意双对数直线里读出来</h2>',
        "04 advanced roughness heading",
    )

    assert_locked(before, out, "04")
    for token in (
        "第一次读这一章",
        "Tybell 看“速度为什么高度非线性”",
        "Paruch 看“粗糙度怎样被定义和测量”",
        "Kim 看“统计钉扎如何落回单个局域事件”",
        "进阶研究方法 · 粗糙度验收判据",
        "局域退钉扎与临界退钉扎不是同一个概念",
    ):
        if token not in out:
            raise RuntimeError(f"04 missing teaching anchor: {token}")
    P04.write_text(out, encoding="utf-8")


def improve_05() -> None:
    raw = P05.read_text(encoding="utf-8")
    before = snapshot(raw)
    out = raw

    old_bridge = (
        '<div class="bridge"><b>方法谱系接力：</b>模块 04 已经把 Lemerle → Tybell → Paruch → Metaxas 串起来：'
        '先把畴壁运动从完整翻转中隔离，再从蠕变扩到完整速度–场区间。本章继续补上 '
        '<b>临界阈值、有限尺寸、瞬态修正与标度关系</b>，而不是重新从一条幂律开始。'
        '<a href="pinning-creep.html">回看方法谱系 →</a></div>'
    )
    new_bridge = (
        '<div class="bridge"><b>第一次读本章，先走四步：</b>'
        'Chauve 先分清蠕变 / 退钉扎 / 流动 → Rosso 看临界几何 ζ → Ferrero 学会夹逼 f<sub>c</sub> 并排除瞬态 → '
        'Wiese 用 β、ζ、ν、z 做闭环。模块 04 已经完成“低场蠕变 + 粗糙度 + 局域钉扎”的铺垫；'
        'Jeudy、热圆整与后面的“进阶研究方法”第二遍再读。<a href="pinning-creep.html">回看模块 04 →</a></div>'
    )
    out = replace_once(out, old_bridge, new_bridge, "05 first-read route")

    out = replace_once(
        out,
        '<h2 id="collapse-gate">6.6 · 坍缩验收判据：把“看起来叠上了”变成可否证的检验</h2>',
        '<h2 id="collapse-gate">进阶研究方法 A · 坍缩验收判据：把“看起来叠上了”变成可否证的检验</h2>',
        "05 collapse heading",
    )
    out = replace_once(
        out,
        '<h2 id="threshold-ladder">6.8 · 阈值推断阶梯：先证明运行有资格，再给 f<sub>c</sub></h2>',
        '<h2 id="threshold-ladder">进阶研究方法 B · 阈值推断阶梯：先证明运行有资格，再给 f<sub>c</sub></h2>',
        "05 threshold heading",
    )
    out = replace_once(
        out,
        '<h2 id="fit-discipline">7 · 指数提取纪律：漂亮直线最容易骗人</h2>',
        '<h2 id="fit-discipline">进阶研究方法 C · 指数提取纪律：漂亮直线最容易骗人</h2>',
        "05 fit heading",
    )

    next_bridge = (
        '<div class="bridge">到这里，问题已经从“墙会不会动”变成“哪一种无序与哪一种有效界面理论控制它怎么动”。'
        '下一章必须把无序本身拆开：随机键、随机场与 RFIM 到底各自意味着什么。</div>'
    )
    if out.count(next_bridge) != 1:
        raise RuntimeError("05 next-chapter bridge not uniquely found")
    out = out.replace(next_bridge, "", 1)
    next_nav = '<div class="next"><a href="pinning-creep.html">← 04 Pinning（钉扎）、Creep（蠕变）与 Roughness（粗糙度）</a><a href="disorder-rfim.html">06 Disorder（无序）与 RFIM →</a></div>'
    out = replace_once(out, next_nav, next_bridge + "\n" + next_nav, "05 move next-chapter bridge")

    assert_locked(before, out, "05")
    if not (
        out.index('进阶研究方法 A') < out.index('进阶研究方法 B') < out.index('进阶研究方法 C') < out.index(next_bridge)
    ):
        raise RuntimeError("05 teaching order still broken")
    for token in (
        "第一次读本章，先走四步",
        "有阈值 + 一条幂律",
        "普适性结论",
        "下一章必须把无序本身拆开",
    ):
        if token not in out:
            raise RuntimeError(f"05 missing teaching/science anchor: {token}")
    P05.write_text(out, encoding="utf-8")


def improve_06() -> None:
    raw = P06.read_text(encoding="utf-8")
    before = snapshot(raw)
    out = raw

    h0 = '<h2>0 · 先拆掉最容易混淆的三个词</h2>'
    route = (
        '<div class="bridge"><b>第一次读本章，先把问题分成四层：</b>'
        '① 分清“弹性界面里的 RF/RB”和“RFIM 的随机场”；② 看 RFIM 如何改变雪崩与翻转形态；'
        '③ 用悬垂、封闭小畴和异常粗糙度判断单值界面映射是否还有效；④ 最后才回到真实滑移铁电，讨论具体缺陷可能粗粒化成什么。'
        '不要从“样品有缺陷”直接跳到“它就是 RFIM”。</div>\n'
    )
    out = replace_once(out, h0, route + h0, "06 first-read route")

    start = out.find('<h2 id="material-disorder">研究桥接 · 真实滑移铁电里的无序到底是什么？</h2>')
    theory_start = out.find('<h2 id="rfim">1 · Dahmen &amp; Sethna 1996：无序不是“加点噪声”，它能改变整个翻转形态</h2>')
    if start < 0 or theory_start < 0 or theory_start <= start:
        raise RuntimeError("06 material/theory block boundaries not found")
    material_block = out[start:theory_start]
    out = out[:start] + out[theory_start:]

    material_block = material_block.replace(
        '<div class="bridge">有了这个边界，再去读 RFIM 才不会犯最常见的错：<b>实验里看见无序，不等于已经知道它属于哪个统计无序类别。</b></div>',
        '<div class="bridge">现在把理论类别与真实样品重新并排看，边界会更清楚：<b>实验里看见无序，不等于已经知道它属于哪个统计无序类别。</b></div>',
        1,
    )
    if '再去读 RFIM' in material_block:
        raise RuntimeError("06 moved material block still points forward to already-read RFIM")

    return_h2 = '<h2>回到滑移铁电：什么时候该用哪一级模型？</h2>'
    out = replace_once(out, return_h2, material_block + return_h2, "06 move material bridge")

    assert_locked(before, out, "06")
    if not (
        out.index('0 · 先拆掉最容易混淆的三个词')
        < out.index('1 · Dahmen &amp; Sethna 1996')
        < out.index('2 · Drossel &amp; Dahmen 1998')
        < out.index('3 · Zhou, Zheng &amp; He')
        < out.index('研究桥接 · 真实滑移铁电里的无序到底是什么？')
        < out.index('回到滑移铁电：什么时候该用哪一级模型？')
    ):
        raise RuntimeError("06 teaching order still broken")
    for token in (
        "第一次读本章，先把问题分成四层",
        "弹性流形的 “随机场类别” ≠ “用了 RFIM”",
        "实验里看见无序，不等于已经知道它属于哪个统计无序类别",
        "RFIM 是一个体相序参量模型",
    ):
        if token not in out:
            raise RuntimeError(f"06 missing teaching/science anchor: {token}")
    P06.write_text(out, encoding="utf-8")


def main() -> None:
    improve_04()
    improve_05()
    improve_06()
    print("Teaching V2 phase 1 PASS: 04–06 learning path reordered; source text, equations, figures, and links unchanged.")


if __name__ == "__main__":
    main()
