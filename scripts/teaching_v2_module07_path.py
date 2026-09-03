from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'modules/numerical-modeling.html'

BLOCK = '''
<style>
.first-read{margin:24px 0 28px;border:1px solid var(--l);border-radius:13px;background:var(--p);padding:17px 18px}.first-read>p{margin:0 0 12px;color:#4f4b45}.first-read-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.first-read-grid a{display:block;text-decoration:none;border:1px solid var(--l);border-radius:10px;padding:12px;background:#faf7f0;color:var(--i)}.first-read-grid b{display:block;font-family:Georgia,"Songti SC",serif;margin-bottom:4px}.first-read-grid small{display:block;color:var(--m);line-height:1.5}.second-read{margin-top:11px;font-size:12.5px;color:#65615a}.second-read a{color:#504c46}@media(max-width:760px){.first-read-grid{grid-template-columns:1fr}}
</style>
<section class="first-read" id="first-read">
<p><b>第一次读这一章，只抓四个支点：</b>先把“模型是什么”与“数值怎么实现”分开。下面四步能讲清，再进入后面的研究级验收细节。</p>
<div class="first-read-grid">
<a href="#tdgl"><b>① 场 + 自由能 + 动力学</b><small>先理解 TDGL：状态变量是谁，F 里有哪些物理项，时间演化为什么这样写。</small></a>
<a href="#reduction"><b>② φ(r,t) 什么时候能变成 u(y,t)</b><small>畴壁是从体场涌现的界面；先验几何不过关，就不要直接套弹性线指数。</small></a>
<a href="#disorder-axes"><b>③ 无序到底随机了什么</b><small>区分耦合方式、物理强度和关联长度；真实缺陷不能只压成一个 σ。</small></a>
<a href="#grid"><b>④ dx / dt 不能偷偷改物理</b><small>先掌握淬火白噪声的空间归一化，再看热噪声的空间 + 时间归一化。</small></a>
</div>
<div class="second-read"><b>第二遍再读：</b><a href="#identifiability">参数可辨识性与留出验证</a> → <a href="#velocity-estimator">稳态速度估计</a> → <a href="#run-receipt">运行记录与证据追溯</a>。这些决定研究结果是否可发表，但不应挡在初学者第一次建立模型心智图之前。</div>
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


def main() -> None:
    raw = PAGE.read_text(encoding='utf-8')
    if 'id="first-read"' in raw:
        raise RuntimeError('Module 07 first-read route already exists')
    before = protected(raw)
    marker = '<p class="rule">核心来源：'
    pos = raw.find(marker)
    if pos < 0:
        raise RuntimeError('Module 07 core-source marker missing')
    out = raw[:pos] + BLOCK + '\n' + raw[pos:]
    if protected(out) != before:
        raise RuntimeError('Module 07 first-read insertion changed protected evidence/equation/figure/code content')

    doc = BeautifulSoup(out, 'html.parser')
    section = doc.find('section', id='first-read')
    if section is None:
        raise RuntimeError('Module 07 first-read section missing after insertion')
    links = [a.get('href') for a in section.find_all('a')]
    expected = ['#tdgl', '#reduction', '#disorder-axes', '#grid', '#identifiability', '#velocity-estimator', '#run-receipt']
    if links != expected:
        raise RuntimeError(f'Module 07 first-read links drifted: {links}')
    ids = {x.get('id') for x in doc.find_all(id=True)}
    for href in expected:
        if href[1:] not in ids:
            raise RuntimeError(f'Module 07 first-read target missing: {href}')
    if raw.count('<p class="rule">核心来源：') != out.count('<p class="rule">核心来源：'):
        raise RuntimeError('Module 07 core-source block count changed')

    PAGE.write_text(out, encoding='utf-8')
    print('MODULE 07 TEACHING V2 PASS: first-read 4-step route + second-read research layer inserted; scientific evidence unchanged.')


if __name__ == '__main__':
    main()
