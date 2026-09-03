from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "modules"

CSS = '''
.fig-read{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin:-12px 0 30px}.fig-read>div{background:var(--p);border:1px solid var(--l);border-radius:10px;padding:12px 14px}.fig-read b{font-family:Georgia,"Times New Roman","Songti SC",serif;font-size:13px}.fig-read p{font-size:12.8px;line-height:1.65;margin:4px 0 0}@media(max-width:760px){.fig-read{grid-template-columns:1fr}}
'''

GUIDES = {
    "foundations.html": [
        (
            "Wu & Li Fig.1",
            "wu2021-fig1-mechanism-display.webp",
            "先把 AB / BA 的相对注册和相反极化方向对上，再沿红色平移箭头看它们怎样被同一条面内结构通道连接；最后才看单胞能量路径。",
            "相反极化不是来自单层本身，而与界面注册、非中心对称配位和层间电荷转移绑定；计算还给出连接这些注册的低能结构路径。",
            "它建立“堆垛注册 → 极化 → 可由平移连接”的结构机制；低单胞能垒不能证明真实器件会整层同步相干滑移，也没有给出实际翻转动力学。",
        ),
        (
            "Vizner Stern Fig.2",
            "vizner2021-fig2-domains-display.webp",
            "先看 B 中黑白畴是否各自内部近似均匀，再看 C 跨畴壁的电势阶跃；最后看 D/E 怎样把电势量级与界面极化计算联系起来。",
            "AB / BA 空间畴对应稳定而相反的表面电势信号，跨畴壁发生清楚跳变，而且 ΔV_KP 在多种样品条件下具有重复性。",
            "它提供“堆垛畴 ↔ 电学空间信号 ↔ 界面极化”的直接实验链；KPFM 直接测的是表面电势，不是极化矢量本身，也没有告诉我们这些畴怎样动态翻转。",
        ),
        (
            "Meng Fig.3e",
            "meng2022-fig3e-multistate-display.webp",
            "把三层体系的两个界面分开看：初态两个界面偶极同向，中间态只有一个界面翻转，终态两个界面都反向。重点是中间态的偶极组合。",
            "多一个范德华界面后，净极化不必只有 ±P；一个界面先改变时可以出现反平行界面偶极和稳定中间状态。",
            "结合层数依赖与异常稳定态，它支持作者提出的逐界面翻转图景；Fig.3e 本身是与实验相容的模型示意，不是原子级动力学录像，也不能单独证明唯一微观路径。",
        ),
    ],
    "switching-pathways.html": [
        (
            "Yang Fig.3",
            "yang2024-fig3-domain-wall-release.png",
            "先用 a 的 AB / BA 光学读出认清两种极化，再看 c：不同训练电场后真正改变的是哪条空间畴边界的位置；b 的滞回放到最后看。",
            "训练场改变了真实空间中的预存畴壁位置，翻转可以落实为畴壁从局域钉扎中心释放并快速传播，而不是只剩一条平均滞回曲线。",
            "它支持该器件中“局域解钉 + 畴壁传播”对 E_c 和翻转路径的重要作用；不能把这里的 E_c 自动当作热力学 f_c，也不能由此宣布退钉扎普适类。",
        ),
        (
            "Sui Fig.4",
            "sui2024-fig4-atomic-sliding-pathways-display.webp",
            "严格把两类 panel 分开：b/c 是原子像里实际观察到的约 1/3 晶胞相对滑移；d/e 是第一性原理给出的 Path 1 / Path 2 与对应能垒。",
            "实验直接看到层间相对滑移伴随极化反转；计算显示经过 ACACAC 中间堆垛的两步路径可比直达路径更低，并能解释实验中出现的中间结构。",
            "它证明原子级相对滑移和亚稳堆垛可以真实参与反转，但计算路径/能垒不是逐帧实验测得；电子束诱导场条件和 InSe:Y 的能垒也不能直接搬到普通 3R-MoS₂ 器件。",
        ),
        (
            "Liang Fig.4",
            "liang2025-fig4-interface-resolved-pathways.png",
            "先看 a/c 的两阶段跳变和 ABA/BAB 中间态，再看 f 的两条界面畴壁；把哪个界面先释放与哪种中间堆垛一一对应。",
            "三层体系的两个界面可以在不同场值依次解钉；上、下界面畴壁释放顺序改变时，中间态会在 ABA 与 BAB 之间切换。",
            "它支持该三层器件中“钉扎层级选择逐界面路径”的机制；不能把这套释放顺序当成所有多层滑移铁电的固定路径，也没有建立临界退钉扎指数。",
        ),
    ],
    "domain-walls.html": [
        (
            "Ke Fig.1",
            "ke2025-fig1-bec-force.webp",
            "不要先看能量高低，先比较高对称 AB/BA 与对称性破缺构型的非对角 BEC / 面内力分布：净横向力究竟在哪里变成非零。",
            "完整高对称畴内部的横向响应可以抵消，而畴壁附近的局域对称性破缺让非对角 BEC 和净面内力出现，给畴壁运动提供微观驱动。",
            "它支持“面外电场怎样抓住畴壁自由度”的微观机制；图中没有淬火无序、局域阈值或 β/ζ/ν，因此不是退钉扎普适性的证据。",
        ),
        (
            "Chen Fig.2",
            "chen2026-fig2-pinning.webp",
            "沿同一条畴壁看气泡或粗糙边缘附近：低偏压时墙在哪里弯曲/停住，提高偏压后是否越过同一个局域障碍。",
            "真实畴壁会在具体缺陷/边缘位置受阻，并在更强驱动下越过障碍；空间图把“钉扎—解钉”落实到了局域势垒。",
            "它是局域钉扎/解钉的直接空间证据；越过一个障碍不等于建立热力学 critical depinning，单组前后图也给不出 v(E)、β、ζ、ν 或有限尺寸标度。",
        ),
        (
            "Liu Fig.2",
            "liu2026-fig2-raman-switching.webp",
            "先比较不同空间区域是否同步翻转，再看中间堆垛态出现/消失和不同循环中的表观阈值；不要把整片器件压成一个 E_c。",
            "同一器件可分成相对独立的翻转区域，中间态停留与表观临界场会随区域/循环变化，说明局域钉扎景观与历史条件会进入器件尺度响应。",
            "它支持空间非均匀钉扎对器件翻转的重要影响；这些表观阈值不是自动唯一的本征材料常数，也还不是恒场 v(E) 临界曲线或普适性闭合。",
        ),
    ],
}


def extract(raw: str, pattern: str) -> list[str]:
    return re.findall(pattern, raw, flags=re.S | re.I)


def guide_html(name: str, see: str, observe: str, boundary: str) -> str:
    return (
        f'<div class="fig-read" data-figure-read="{name}">'
        f'<div><b>先看哪里</b><p>{see}</p></div>'
        f'<div><b>看到什么</b><p>{observe}</p></div>'
        f'<div><b>能证明 / 不能证明</b><p>{boundary}</p></div>'
        f'</div>'
    )


def main() -> None:
    changed: list[str] = []
    for filename, guides in GUIDES.items():
        page = MOD / filename
        raw = page.read_text(encoding="utf-8")
        before_sources = extract(raw, r'<blockquote\b[^>]*class=["\'][^"\']*source-text[^"\']*["\'][^>]*>.*?</blockquote>')
        before_figures = extract(raw, r'<figure\b[^>]*>.*?</figure>')
        before_eqs = extract(raw, r'<div\b[^>]*class=["\'][^"\']*\beq\b[^"\']*["\'][^>]*>.*?</div>')
        before_hrefs = re.findall(r'href=["\']([^"\']+)["\']', raw, flags=re.I)

        if 'class="fig-read"' in raw or '.fig-read{' in raw:
            raise RuntimeError(f"{filename}: Figure Reading V2 already present; refusing to duplicate")
        if raw.count('</style>') < 1:
            raise RuntimeError(f"{filename}: no style block found")

        updated = raw.replace('</style>', CSS + '</style>', 1)
        for name, asset, see, observe, boundary in guides:
            if f'data-figure-read="{name}"' in updated:
                raise RuntimeError(f"{filename}: duplicate guide name {name}")
            pattern = re.compile(
                r'(<figure\b[^>]*>.*?<img\b[^>]*src=["\'][^"\']*' + re.escape(asset) + r'[^"\']*["\'][^>]*>.*?</figure>)',
                flags=re.S | re.I,
            )
            matches = list(pattern.finditer(updated))
            if len(matches) != 1:
                raise RuntimeError(f"{filename}: expected one target figure for {asset}, found {len(matches)}")
            block = matches[0].group(1)
            updated = updated[:matches[0].start()] + block + guide_html(name, see, observe, boundary) + updated[matches[0].end():]

        after_sources = extract(updated, r'<blockquote\b[^>]*class=["\'][^"\']*source-text[^"\']*["\'][^>]*>.*?</blockquote>')
        after_figures = extract(updated, r'<figure\b[^>]*>.*?</figure>')
        after_eqs = extract(updated, r'<div\b[^>]*class=["\'][^"\']*\beq\b[^"\']*["\'][^>]*>.*?</div>')
        after_hrefs = re.findall(r'href=["\']([^"\']+)["\']', updated, flags=re.I)

        if before_sources != after_sources:
            raise RuntimeError(f"{filename}: source-text blocks changed")
        if before_figures != after_figures:
            raise RuntimeError(f"{filename}: source figures/captions changed")
        if before_eqs != after_eqs:
            raise RuntimeError(f"{filename}: equation blocks changed")
        if before_hrefs != after_hrefs:
            raise RuntimeError(f"{filename}: href wiring changed")
        if updated.count('class="fig-read"') != len(guides):
            raise RuntimeError(f"{filename}: expected {len(guides)} guides after update")
        for name, asset, *_ in guides:
            pos_fig = updated.index(asset)
            pos_guide = updated.index(f'data-figure-read="{name}"')
            if pos_guide <= pos_fig:
                raise RuntimeError(f"{filename}: guide {name} not placed after its figure")

        page.write_text(updated, encoding="utf-8")
        changed.append(filename)

    print("FIGURE READING V2 01-03 WRITER PASS:", ", ".join(changed))


if __name__ == "__main__":
    main()
