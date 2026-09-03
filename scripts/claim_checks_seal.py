from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'pinning-creep.html': 3,
    'depinning.html': 4,
    'disorder-rfim.html': 4,
    'numerical-modeling.html': 4,
}

ANCHORS = {
    'pinning-creep.html': (
        '仅凭动力学曲线不能唯一识别有效无序',
        '报告尺度区间依赖或有效 ζ',
        '“局域退钉扎”与整个受驱无序界面的临界退钉扎不是同一个命题',
    ),
    'depinning.html': (
        '阈值需要独立的时间演化判据和收敛检查',
        '“阈值先于指数”是证据链纪律',
        '标度坍缩应该被当成待检验结果',
        '“一个指数接近”只能算线索',
        '看完整翻转与孤立畴壁流程对照 →',
    ),
    'disorder-rfim.html': (
        '要叫 RF、RB 或 RFIM，还必须说明它耦合到什么自由度',
        'random-field disorder（随机场无序）与 RFIM 中直接耦合体相序参量的随机场不是同一个模型对象',
        '单值 h(y) 的弹性线映射可能失效',
        '并没有自动完成从微观缺陷到唯一统计无序类别的粗粒化判别',
    ),
    'numerical-modeling.html': (
        '固定连续体 Δ 时应有 σ<sub>grid</sub> ∝ dx<sup>−1</sup>',
        '噪声率标准差随 dt<sup>−1/2</sup>，每步随机增量随 dt<sup>+1/2</sup>',
        '同一淬火景观下的热噪声内层重复',
        '并不自动等于畴壁质心速度',
        '没参与校准的留出可观测量',
    ),
}

FORBIDDEN = (
    '完整的完整翻转',
    '完整翻转 vs 孤立畴壁',
)


def main() -> None:
    total = 0
    for name, expected in EXPECTED.items():
        path = ROOT / 'modules' / name
        raw = path.read_text(encoding='utf-8')
        doc = BeautifulSoup(raw, 'html.parser')

        sections = doc.select('section#claim-check')
        if len(sections) != 1:
            raise RuntimeError(f'{name}: expected exactly one #claim-check, found {len(sections)}')
        section = sections[0]
        heading = section.find('h2')
        if heading is None or '判断自测' not in heading.get_text(' ', strip=True):
            raise RuntimeError(f'{name}: claim-check heading missing')

        details = section.find_all('details', recursive=False)
        if len(details) != expected:
            raise RuntimeError(f'{name}: expected {expected} claim checks, found {len(details)}')
        for i, item in enumerate(details, 1):
            summary = item.find('summary')
            if summary is None or not summary.get_text(' ', strip=True):
                raise RuntimeError(f'{name}: question {i} missing summary')
            answer = item.find('span', class_='answer')
            if answer is None or '答案：' not in answer.get_text(' ', strip=True):
                raise RuntimeError(f'{name}: question {i} missing folded answer label')
            if item.find('p') is None:
                raise RuntimeError(f'{name}: question {i} missing explanation')

        nxt = section.find_next_sibling('div', class_='next')
        if nxt is None:
            raise RuntimeError(f'{name}: claim-check is not immediately before final navigation')

        for anchor in ANCHORS[name]:
            if anchor not in raw:
                raise RuntimeError(f'{name}: claim-boundary anchor drifted: {anchor}')
        for token in FORBIDDEN:
            if token in raw:
                raise RuntimeError(f'{name}: Teaching V2 prose residue: {token}')

        total += len(details)

    if total != 15:
        raise RuntimeError(f'claim-check total drifted: {total}')
    print('CLAIM CHECK SEAL PASS: modules 04/05/06/07 keep 3/4/4/4 folded evidence-to-claim judgments (15 total) with locked scientific boundaries.')


if __name__ == '__main__':
    main()
