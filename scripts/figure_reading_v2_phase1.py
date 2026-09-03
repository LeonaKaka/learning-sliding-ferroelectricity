from __future__ import annotations

from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    '04': ROOT / 'modules/pinning-creep.html',
    '05': ROOT / 'modules/depinning.html',
    '06': ROOT / 'modules/disorder-rfim.html',
}

CSS = '''
.fig-read{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin:-12px 0 30px}.fig-read>div{background:var(--p);border:1px solid var(--l);border-radius:10px;padding:12px 14px}.fig-read b{font-family:Georgia,"Times New Roman","Songti SC",serif;font-size:13px}.fig-read p{font-size:12.8px;line-height:1.65;margin:4px 0 0}@media(max-width:760px){.fig-read{grid-template-columns:1fr}}
'''

GUIDES = {
    '04': {
        'tybell2002-fig3-creep.png': (
            'Tybell Fig.3',
            '先看哪里', '先认横轴是 1/E：越往右驱动力越弱；纵轴是对数速度。再比较三种膜厚是否呈同一种整体趋势。',
            '看到什么', 'E 变弱时速度跨多个数量级迅速下降，三组数据都能被蠕变形式描述，而不是简单的 v∝E 线性响应。',
            '能证明 / 不能证明', '它支持本实验区间的低场热激活蠕变；不能从这张图读出退钉扎 f_c，也不能仅凭 μ 唯一判定 RF 或 RB。',
        ),
        'paruch2005-fig3-roughness.png': (
            'Paruch Fig.3',
            '先看哪里', '先看 (a) 中作者真正拟合的短尺度区间，再看大 L 后的饱和；最后看 (b) 三种膜厚得到的 ζ。',
            '看到什么', '短尺度 B(L) 在双对数坐标中近似线性，给出 ζ≈0.22–0.29；更大尺度并没有继续保持同一条幂律。',
            '能证明 / 不能证明', '它把“墙很弯”变成了可量化的尺度律；结合独立 μ 可约束无序解释，但并没有直接识别某一种微观缺陷。',
        ),
        'kim2014-fig1-pinning-display.webp': (
            'Kim Fig.1',
            '先看哪里', '先看 (a) 翻转面积曲线的蓝/红箭头与平台区，再把同一阶段对应到 (b) 的 PFM 空间位置。',
            '看到什么', '整体翻转面积暂时停止增长时，畴壁也在具体空间位置停住；随后越过该位置后，曲线和畴壁都继续前进。',
            '能证明 / 不能证明', '这是局域势垒造成畴壁停滞—再传播的直接证据；这里的“退钉扎”不是热力学临界退钉扎，也没有 β/ζ/ν 普适性含义。',
        ),
    },
    '05': {
        'rosso2003-fig2-critical-roughness.png': (
            'Rosso Fig.2',
            '先看哪里', '先看主图 W²(L) 随系统尺寸 L 的斜率，再看插图里改变拟合下限 L_min 后 ζ 是否稳定。',
            '看到什么', '临界粗糙度来自多尺寸标度，而不是单一尺寸的一段直线；不同弹性能模型还给出明显不同的 ζ。',
            '能证明 / 不能证明', '它证明在指定弹性流形模型中可稳定提取临界几何，并显示有效弹性会改变结果；不能把该 ζ 直接搬给真实滑移铁电。',
        ),
        'ferrero2013-fig3-nonsteady-velocity.png': (
            'Ferrero Fig.3',
            '先看哪里', '先读 (a) 中 f<f_c、f≈f_c、f>f_c 三类 v(t) 长时间走向，再看 (b) 多曲线联合缩放。',
            '看到什么', '高于阈值的速度最终饱和，低于阈值最终衰减到零；只有临界附近才期待幂律松弛，而且越靠近 f_c 判别所需时间越长。',
            '能证明 / 不能证明', '它提供夹逼 f_c、识别瞬态和联合检查指数的方法；一张视觉上漂亮的坍缩本身仍不能独立证明普适类。',
        ),
        'wiese2022-fig22-depinning-phenomenology.png': (
            'Wiese Fig.22',
            '先看哪里', '左边先看临界界面的粗糙几何，右边再看 T=0 的 v–f 曲线在 f_c 附近如何开启。',
            '看到什么', '退钉扎同时包含阈值、粗糙几何和速度临界开启；远离临界后又逐渐回到普通流动区。',
            '能证明 / 不能证明', '这张综述图用来建立 β、ζ、ν、z 必须互相约束的心智模型；它不能替代你自己的多尺寸数据与阈值收敛。',
        ),
    },
    '06': {
        'drossel1998-fig3a-percolative-wall.png': (
            'Drossel Fig.3(a)',
            '先看哪里', '不要只追最外缘；先找已经侵入区域内部仍留下的白色小岛，再看前沿是否出现分叉、悬垂与多连通结构。',
            '看到什么', '强无序附近推进不是一条干净的单值曲线，侵入区域会绕过局部区域并留下封闭小畴，呈类渗流几何。',
            '能证明 / 不能证明', '它说明 RFIM 的“畴壁”在相关尺度上可能无法写成单值 h(y)；不能据此宣布所有二维铁电畴壁都属于渗流或 RFIM。',
        ),
        'zhou2012-fig2-anomalous-roughness.png': (
            'Zhou Fig.2',
            '先看哪里', '先看 (a) 全局粗糙度随时间的标度，再看 (b) 不同 r 的局域关联；重点比较全局与局域指数是否还能由一个 ζ 描述。',
            '看到什么', '全局与局域标度发生分裂，并出现异常 / 多重标度；这和简单 QEW 单值界面的超粗糙故事不同。',
            '能证明 / 不能证明', '它是“界面映射可能失效”的强诊断；作者把悬垂指为主要来源属于基于对比的猜想，不是对所有模型成立的定理。',
        ),
        'paul2026-fig4-multidomain-disorder.webp': (
            'Paul Fig.4',
            '先看哪里', '把 D2 的慢扫/低温异常响应与 D3 的多次跳变分开看，再对照作者对畴松弛、部分回切和陷阱动力学的解释。',
            '看到什么', '不同结构无序、陷阱和多畴动力学可以同时投影到宏观翻转响应里；同一条回线并不只对应一种微观机制。',
            '能证明 / 不能证明', '它证明真实滑移铁电器件里的“无序”是多来源的；不能直接把某个缺陷唯一映射成静态 Gaussian RF、RB 或 RFIM 普适类。',
        ),
    },
}


def snapshot(raw: str) -> dict:
    soup = BeautifulSoup(raw, 'html.parser')
    return {
        'source': Counter(str(x) for x in soup.select('.source-text')),
        'href': Counter(x.get('href') for x in soup.find_all('a')),
        'img': Counter((x.get('src'), x.get('alt')) for x in soup.find_all('img')),
        'eq': Counter(x.get_text(' ', strip=True) for x in soup.select('.eq')),
        'captions': Counter(x.get_text(' ', strip=True) for x in soup.find_all('figcaption')),
    }


def guide_html(spec: tuple[str, ...]) -> str:
    name, h1, p1, h2, p2, h3, p3 = spec
    return (
        f'<div class="fig-read" data-figure-read="{name}">'
        f'<div><b>{h1}</b><p>{p1}</p></div>'
        f'<div><b>{h2}</b><p>{p2}</p></div>'
        f'<div><b>{h3}</b><p>{p3}</p></div>'
        '</div>'
    )


def insert_after_figure(raw: str, asset: str, block: str, label: str) -> str:
    if raw.count(asset) < 1:
        raise RuntimeError(f'{label}: asset not found: {asset}')
    pos = raw.index(asset)
    end = raw.find('</figure>', pos)
    if end < 0:
        raise RuntimeError(f'{label}: figure closing tag not found')
    end += len('</figure>')
    if 'data-figure-read=' in raw[end:end + 300]:
        raise RuntimeError(f'{label}: guide already present')
    return raw[:end] + '\n' + block + raw[end:]


def main() -> None:
    for key, page in PAGES.items():
        raw = page.read_text(encoding='utf-8')
        before = snapshot(raw)
        out = raw
        if '.fig-read{' in out:
            raise RuntimeError(f'{page.name}: Figure Reading V2 CSS already exists')
        if out.count('@media(max-width:760px)') != 1:
            raise RuntimeError(f'{page.name}: responsive CSS anchor not unique')
        out = out.replace('@media(max-width:760px)', CSS + '@media(max-width:760px)', 1)

        for asset, spec in GUIDES[key].items():
            out = insert_after_figure(out, asset, guide_html(spec), f'{page.name}/{asset}')

        after = snapshot(out)
        for locked in ('source', 'href', 'img', 'eq', 'captions'):
            if before[locked] != after[locked]:
                raise RuntimeError(f'{page.name}: locked {locked} changed')
        expected = len(GUIDES[key])
        if out.count('class="fig-read"') != expected:
            raise RuntimeError(f'{page.name}: expected {expected} figure guides')
        for spec in GUIDES[key].values():
            if spec[0] not in out or spec[-1] not in out:
                raise RuntimeError(f'{page.name}: figure guide content missing: {spec[0]}')

        page.write_text(out, encoding='utf-8')

    print('FIGURE READING V2 PHASE 1 PASS: 9 core figures in modules 04–06 now have read→observe→claim-boundary guides.')
    print('Original figures, captions, source text, equations, hrefs and image wiring are unchanged.')


if __name__ == '__main__':
    main()
