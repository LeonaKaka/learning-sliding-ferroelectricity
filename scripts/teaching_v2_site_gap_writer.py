from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
FOUND = ROOT / 'modules/foundations.html'
TRACK = ROOT / 'modules/research-track.html'

FOUND_BLOCK = '''
<style>
.handoff{margin:32px 0 22px;padding:17px 19px;border-left:4px solid var(--accent);background:#eee8dc;font:17px/1.65 Georgia,"Times New Roman","Songti SC",serif}.handoff b{font-weight:700}
</style>
<div class="handoff" id="next-question"><b>这一章结束后，为什么下一步必须进入 Switching Pathways？</b><br>到这里，我们只证明了“不同堆垛注册可以对应不同 P<sub>z</sub>，而且某些面内平移能把它们连接起来”。但<strong>存在一条低能结构通道，不等于真实器件会沿这条通道整层同步翻转</strong>。下一章因此把“单胞结构路径”和“真实空间翻转过程”拆开：到底谁先动、是否经过亚稳堆垛、预存畴壁与局域钉扎又怎样选择实际路径。</div>
'''

TRACK_BLOCK = '''
<style>
.entry-check{margin:24px 0 30px;border:1px solid var(--l);border-radius:13px;background:var(--p);padding:17px 18px}.entry-check>p{margin:0 0 12px}.entry-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.entry-grid a{display:block;text-decoration:none;border:1px solid var(--l);border-radius:10px;padding:12px;background:#faf7f0;color:var(--i)}.entry-grid b{display:block;font-family:Georgia,"Songti SC",serif;margin-bottom:4px}.entry-grid small{display:block;color:var(--m);line-height:1.5}.entry-hold{margin-top:11px;font-size:12.5px;color:#65615a}@media(max-width:780px){.entry-grid{grid-template-columns:1fr}}
</style>
<section class="entry-check" id="entry-check">
<p><b>什么时候再进入 Research Track？</b> 这页不是用来提前接触“更高级公式”的。先确认下面四件事已经能用自己的话讲清楚：</p>
<div class="entry-grid">
<a href="domain-walls.html"><b>① 运动对象</b><small>为什么低滑移势垒不等于整层会被 E<sub>z</sub> 同步推动？畴壁为什么能成为实际运动自由度？</small></a>
<a href="pinning-creep.html"><b>② 钉扎与蠕变</b><small>为什么“看到一次局域退钉扎”还不是临界退钉扎？低场热激活运动又需要哪些独立几何证据？</small></a>
<a href="depinning.html"><b>③ 临界证据链</b><small>为什么 f<sub>c</sub> 必须先独立约束，再谈 β、ζ、ν 与有限尺寸闭合？</small></a>
<a href="numerical-modeling.html"><b>④ 数值纪律</b><small>为什么 dx / dt、无序归一化、统计独立性和留出验证会直接决定物理结论是否可信？</small></a>
</div>
<div class="entry-hold">如果这四项里有两项还说不清，先回 03–07；Research Track 的价值在于<strong>把已经理解的部件接成研究问题</strong>，不是替基础模块重新讲一遍。</div>
</section>
'''


def protected(raw: str) -> dict[str, list[str | None]]:
    doc = BeautifulSoup(raw, 'html.parser')
    return {
        'source': [str(x) for x in doc.select('.source-text')],
        'eq': [str(x) for x in doc.select('.eq')],
        'fig': [str(x) for x in doc.find_all('figure')],
        'src': [x.get('src') for x in doc.find_all('img')],
        'pre': [str(x) for x in doc.find_all('pre')],
        'code': [str(x) for x in doc.find_all('code')],
    }


def add_foundations() -> None:
    raw = FOUND.read_text(encoding='utf-8')
    if 'id="next-question"' in raw:
        raise RuntimeError('Foundations handoff already exists')
    before = protected(raw)
    marker = '<div class="next">'
    pos = raw.rfind(marker)
    if pos < 0:
        raise RuntimeError('Foundations final navigation missing')
    out = raw[:pos] + FOUND_BLOCK + '\n' + raw[pos:]
    if protected(out) != before:
        raise RuntimeError('Foundations handoff changed protected evidence')
    doc = BeautifulSoup(out, 'html.parser')
    handoff = doc.find(id='next-question')
    if handoff is None or handoff.find_next_sibling('div', class_='next') is None:
        raise RuntimeError('Foundations handoff placement invalid')
    for anchor in (
        '存在一条低能结构通道，不等于真实器件会沿这条通道整层同步翻转',
        '单胞结构路径',
        '真实空间翻转过程',
    ):
        if anchor not in out:
            raise RuntimeError(f'Foundations handoff boundary missing: {anchor}')
    FOUND.write_text(out, encoding='utf-8')


def add_track() -> None:
    raw = TRACK.read_text(encoding='utf-8')
    if 'id="entry-check"' in raw:
        raise RuntimeError('Research Track entry check already exists')
    before = protected(raw)
    marker = '<p class="rule">边界：本页只公开研究问题、有效模型与测量逻辑'
    pos = raw.find(marker)
    if pos < 0:
        raise RuntimeError('Research Track boundary rule missing')
    out = raw[:pos] + TRACK_BLOCK + '\n' + raw[pos:]
    if protected(out) != before:
        raise RuntimeError('Research Track entry check changed protected evidence/equations')
    doc = BeautifulSoup(out, 'html.parser')
    section = doc.find('section', id='entry-check')
    if section is None:
        raise RuntimeError('Research Track entry check missing after insertion')
    hrefs = tuple(a.get('href') for a in section.select('.entry-grid > a'))
    expected = ('domain-walls.html', 'pinning-creep.html', 'depinning.html', 'numerical-modeling.html')
    if hrefs != expected:
        raise RuntimeError(f'Research Track prerequisite links drifted: {hrefs}')
    for href in hrefs:
        if not (TRACK.parent / href).exists():
            raise RuntimeError(f'Research Track prerequisite page missing: {href}')
    for anchor in (
        '这页不是用来提前接触“更高级公式”的',
        '把已经理解的部件接成研究问题',
        '为什么 f<sub>c</sub> 必须先独立约束',
    ):
        if anchor not in out:
            raise RuntimeError(f'Research Track entry boundary missing: {anchor}')
    TRACK.write_text(out, encoding='utf-8')


def main() -> None:
    add_foundations()
    add_track()
    print('TEACHING V2 SITE GAP PASS: Foundations→Pathways handoff + Research Track prerequisite gate inserted; protected evidence unchanged.')


if __name__ == '__main__':
    main()
