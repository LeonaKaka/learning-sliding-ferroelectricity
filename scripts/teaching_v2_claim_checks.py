from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

QUIZZES = {
    'pinning-creep.html': '''
<style>
.claim-check{margin:54px 0 30px;padding-top:28px;border-top:1px solid #d9d4ca}.claim-check h2{margin:0 0 8px}.claim-check .quiz-intro{margin:0 0 15px;color:#666}.claim-check details{margin:9px 0;border:1px solid #d9d4ca;border-radius:10px;background:#fffdf8;padding:12px 14px}.claim-check summary{cursor:pointer;font-weight:650}.claim-check details p{margin:10px 0 2px}.claim-check .answer{font-weight:700}
</style>
<section class="claim-check" id="claim-check">
<h2>判断自测 · 这份证据允许你说到哪里？</h2>
<p class="quiz-intro">先自己判断“对 / 错”，再展开答案。这里不考记忆，专门检查结论有没有越过证据。</p>
<details><summary>1 · 只要低场仍测到非零且强烈非线性的 v(E)，就可以仅凭这条曲线确定无序类别和普适性。</summary><p><span class="answer">答案：错。</span> Tybell 的速度数据建立了热激活畴壁运动的关键证据，但仅凭动力学曲线不能唯一识别有效无序；还需要独立的几何 / 粗糙度信息，并检查是否真的进入相应渐近区。</p></details>
<details><summary>2 · 从 B(L) 提取 ζ 时，如果换一个合理尺度区间结果明显漂移，就不应只挑最接近文献值的那一个。</summary><p><span class="answer">答案：对。</span> 此时更稳妥的是报告尺度区间依赖或有效 ζ，并继续做区间稳定性检查；一条漂亮双对数直线本身不是普适性闭合。</p></details>
<details><summary>3 · 观察到 Kim 式的单个局域退钉扎事件，就等于已经证明系统存在热力学退钉扎临界点 f<sub>c</sub>。</summary><p><span class="answer">答案：错。</span> 局域事件证明具体缺陷可以钉扎并释放畴壁，但“局域退钉扎”与整个受驱无序界面的临界退钉扎不是同一个命题。</p></details>
</section>
''',
    'depinning.html': '''
<style>
.claim-check{margin:54px 0 30px;padding-top:28px;border-top:1px solid #d9d4ca}.claim-check h2{margin:0 0 8px}.claim-check .quiz-intro{margin:0 0 15px;color:#666}.claim-check details{margin:9px 0;border:1px solid #d9d4ca;border-radius:10px;background:#fffdf8;padding:12px 14px}.claim-check summary{cursor:pointer;font-weight:650}.claim-check details p{margin:10px 0 2px}.claim-check .answer{font-weight:700}
</style>
<section class="claim-check" id="claim-check">
<h2>判断自测 · 退钉扎证据链有没有闭合？</h2>
<p class="quiz-intro">先判断，再展开。重点不是背 β，而是判断阈值、稳态、尺度和指数之间的先后关系。</p>
<details><summary>1 · 扫描驱动力时第一次看到平均速度变成非零，这个点就可以直接当成精确的 f<sub>c</sub>。</summary><p><span class="answer">答案：错。</span> 临界附近会有很长瞬态，有限观察时间还会把“最终停止”和“仍在缓慢衰减”混在一起。阈值需要独立的时间演化判据和收敛检查。</p></details>
<details><summary>2 · β 的拟合应建立在已经独立约束的 f<sub>c</sub> 上，因为阈值偏差会直接污染幂律斜率。</summary><p><span class="answer">答案：对。</span> 若一边移动 f<sub>c</sub> 一边追求最漂亮的 β，指数很容易吸收阈值误差；“阈值先于指数”是证据链纪律。</p></details>
<details><summary>3 · 标度坍缩应该被当成待检验结果，而不是先调参数把数据压到一起，再据此宣布普适性。</summary><p><span class="answer">答案：对。</span> 坍缩需要预先定义变量、尺度范围和失败判据。若只有某个精调参数组合看起来漂亮，它不能独立构成普适性证据。</p></details>
<details><summary>4 · 只要测得一个与文献值接近的 β，就足以确认系统属于同一个退钉扎普适类。</summary><p><span class="answer">答案：错。</span> 普适性至少还要求阈值、稳态速度、临界几何、有限尺寸和不同估计量彼此兼容；“一个指数接近”只能算线索。</p></details>
</section>
''',
    'disorder-rfim.html': '''
<style>
.claim-check{margin:54px 0 30px;padding-top:28px;border-top:1px solid #d9d4ca}.claim-check h2{margin:0 0 8px}.claim-check .quiz-intro{margin:0 0 15px;color:#666}.claim-check details{margin:9px 0;border:1px solid #d9d4ca;border-radius:10px;background:#fffdf8;padding:12px 14px}.claim-check summary{cursor:pointer;font-weight:650}.claim-check details p{margin:10px 0 2px}.claim-check .answer{font-weight:700}
</style>
<section class="claim-check" id="claim-check">
<h2>判断自测 · 从“有缺陷”到 RF / RB / RFIM 还差几步？</h2>
<p class="quiz-intro">先判断，再展开。这里专门防止把真实缺陷名称直接等同于某个统计无序模型。</p>
<details><summary>1 · 实验发现某种缺陷会钉扎畴壁，因此可以直接把该材料称为 RFIM。</summary><p><span class="answer">答案：错。</span> “会钉扎”只说明缺陷进入了有效无序。要叫 RF、RB 或 RFIM，还必须说明它耦合到什么自由度、相关统计是什么，以及粗粒化后保留了哪些结构。</p></details>
<details><summary>2 · 弹性流形理论里的 random-field disorder（随机场无序）与 RFIM 中直接耦合体相序参量的随机场不是同一个模型对象。</summary><p><span class="answer">答案：对。</span> 名字里都有“random field”并不意味着模型相同；自由度、哈密顿量和允许的几何结构都不同。</p></details>
<details><summary>3 · 如果界面出现大量悬垂或封闭小畴，单值 h(y) 的弹性线映射可能失效，此时 ζ 的解释也必须重新检查。</summary><p><span class="answer">答案：对。</span> 一旦几何不再能稳定表示成单值界面，原本针对弹性线定义的粗糙度与临界指数就不能无条件照搬。</p></details>
<details><summary>4 · Paul 2026 展示真实滑移铁电中的多来源无序后，就已经唯一判定了这些缺陷对应 RF、RB 还是 RFIM。</summary><p><span class="answer">答案：错。</span> 这类材料证据说明结构无序、陷阱和多畴路径会共同影响动力学，但并没有自动完成从微观缺陷到唯一统计无序类别的粗粒化判别。</p></details>
</section>
''',
}


def signature(raw: str) -> dict[str, list[str | None]]:
    doc = BeautifulSoup(raw, 'html.parser')
    return {
        'sources': [str(x) for x in doc.select('.source-text')],
        'equations': [str(x) for x in doc.select('.eq')],
        'figures': [str(x) for x in doc.find_all('figure')],
        'hrefs': [x.get('href') for x in doc.find_all('a')],
        'srcs': [x.get('src') for x in doc.find_all('img')],
        'pre': [str(x) for x in doc.find_all('pre')],
        'code': [str(x) for x in doc.find_all('code')],
    }


def main() -> None:
    for name, quiz in QUIZZES.items():
        path = ROOT / 'modules' / name
        raw = path.read_text(encoding='utf-8')
        if 'id="claim-check"' in raw:
            raise RuntimeError(f'{name}: claim-check already exists')
        before = signature(raw)
        marker = '<div class="next">'
        pos = raw.rfind(marker)
        if pos < 0:
            raise RuntimeError(f'{name}: final navigation marker not found')
        out = raw[:pos] + quiz + '\n' + raw[pos:]
        after = signature(out)
        if before != after:
            raise RuntimeError(f'{name}: protected paper/equation/figure/link/code wiring changed')
        doc = BeautifulSoup(out, 'html.parser')
        section = doc.find('section', id='claim-check')
        if section is None:
            raise RuntimeError(f'{name}: inserted claim-check missing')
        expected = 3 if name == 'pinning-creep.html' else 4
        if len(section.find_all('details', recursive=False)) != expected:
            raise RuntimeError(f'{name}: expected {expected} judgment questions')
        if section.find_next_sibling('div', class_='next') is None:
            raise RuntimeError(f'{name}: claim-check not placed immediately before final navigation')
        path.write_text(out, encoding='utf-8')
        print(f'{name}: CLAIM CHECK PASS ({expected} questions)')


if __name__ == '__main__':
    main()
