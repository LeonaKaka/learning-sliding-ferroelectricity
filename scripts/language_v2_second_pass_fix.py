from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab.html"

TEXT_REPLACEMENTS = {
    "Reproduction Lab 01 · TDGL Domain Wall Gold Test": "Reproduction Lab（复现实验室）01 · TDGL Domain Wall（畴壁）已知答案测试",
    "Reproduction Lab": "Reproduction Lab（复现实验室）",
    "· Lesson 01 · Gold Test": "· 第 01 课 · 已知答案测试",
    "Code": "代码",
    "Result": "结果",
    " / Reproduction Lab / Lesson 01": " / 复现实验室 / 第 01 课",
    "普通 CPU 很快就能验收的 gold test": "普通 CPU 很快就能验收的已知答案测试",
    "数值 domain wall 必须收敛到论文 Eq. (7–8) 的 tanh kink": "数值 domain wall（畴壁）必须收敛到论文 Eq. (7–8) 的 tanh kink（双曲正切扭结）",
    "profile RMSE、wall width、free-energy descent 三关都过，才允许进入 2D wall": "剖面 RMSE、畴壁宽度、自由能下降三关都过，才允许进入二维畴壁",
    "bulk level 使用非守恒标量 order parameter φ(r,t)、双井 φ⁴ potential 和 overdamped Langevin / Model-A dynamics；clean case 的 stationary soliton 给出一堵解析可知的 domain wall": "体场层面使用非守恒标量 order parameter（序参量） φ(r,t)、双井 φ⁴ 势和 overdamped Langevin（过阻尼朗之万）/ Model A（A 型模型）动力学；无无序情形的 stationary soliton（定态孤子）给出一堵解析可知的畴壁",
    "这是从同一模型和解析结果抽出的最小 validation unit": "这是从同一模型和解析结果抽出的最小验证单元",
    "roughness / structure factor 后面再复现": "roughness（粗糙度）/ structure factor（结构因子）后面再复现",
    "为什么故意从一个错误的 wall 开始": "为什么故意从一堵错误的畴壁开始",
    "如果一开始就填 analytic tanh，代码“不动”并不能证明 integrator 正确": "如果一开始就填解析 tanh，代码“不动”并不能证明积分器正确",
    "初始 wall 比 equilibrium wall 宽三倍，强迫 TDGL 真正发生 relaxation": "初始畴壁比平衡畴壁宽三倍，强迫 TDGL 真正发生弛豫",
    "正确代码应把 wall 收缩到 w，同时 free energy 下降": "正确代码应把畴壁收缩到 w，同时自由能下降",
    "① Grid": "① 网格",
    "1D x 网格；无 disorder、无 thermal noise": "一维 x 网格；无无序、无热噪声",
    "② Laplacian": "② Laplacian（拉普拉斯算子）",
    "显式 Euler 更新": "显式 Euler（欧拉）更新",
    "④ Boundaries": "④ 边界条件",
    "将来 sliding-FE periodic potential、RF、RB 也应该从 free energy 一项项取 derivative，而不是凭感觉往 update 里塞 force": "将来 sliding ferroelectricity（滑移铁电）的周期势、RF、RB 也应该从自由能一项项求导，而不是凭感觉往更新式里塞力",
    "3 · Hard gate 怎么写": "3 · 硬性验收条件怎么写",
    "数值结果用两个独立量验": "数值结果用两个独立量验证",
    "不是肉眼验收，而是程序自己 fail": "不是肉眼验收，而是程序自己报错",
    "故意过宽的 wall 逐步收敛到 analytic kink；右：TDGL relaxation 让 F(t)−F(final) 下降。此图由配套脚本生成，不是论文原 Figure": "故意过宽的畴壁逐步收敛到解析扭结；右：TDGL 弛豫让 F(t)−F(final) 下降。此图由配套脚本生成，不是论文原图",
    "Wall width": "畴壁宽度",
    "Profile RMSE": "剖面 RMSE",
    "Free energy": "自由能",
    "relaxation 应下降": "弛豫过程中应下降",
    "PASS": "通过",
    "第一层永远先选有解析答案或极强 sanity check 的问题": "第一层永远先选有解析答案或极强合理性检查的问题",
    "和你的 sliding-FE 项目怎么接": "和你的滑移铁电项目怎么接",
    "φ⁴ potential": "φ⁴ 势",
    "periodic stacking / polarization effective potential": "周期堆垛 / 极化有效势",
    "换成 sliding-specific landscape": "换成滑移铁电特定能量景观",
    "clean single wall": "无无序单畴壁",
    "single-wall initialization / E=0 relaxation": "单畴壁初始化 / E=0 弛豫",
    "做真正的 wall-stability certificate": "做真正的畴壁稳定性验证",
    "wall width": "畴壁宽度",
    "grid-resolution sanity": "网格分辨率合理性检查",
    "确认 dx 能 resolve wall，避免假 depinning": "确认 dx 能分辨畴壁，避免伪退钉扎",
    "TDGL update": "TDGL 更新",
    "phase-field time evolution": "phase-field（相场）时间演化",
    "再加 constant E、quenched RF/RB、thermal noise": "再加恒定 E、淬火 RF/RB、热噪声",
    "hard regression test": "硬性回归测试",
    "solver 改动后的最低验收": "求解器改动后的最低验收",
    "gold test 过了才跑 threshold campaign": "已知答案测试通过后才跑阈值批量扫描",
    "clean object 是对的，再证明 estimator 是对的，再增加 disorder 和 drive，最后才谈 criticality": "无无序对象是对的，再证明估计量是对的，再增加无序和驱动，最后才谈临界性",
    "dt 与显式 diffusion 稳定性": "dt 与显式扩散稳定性",
    "width 偏差很大": "畴壁宽度偏差很大",
    "dx、边界距离、Laplacian": "dx、边界距离、拉普拉斯算子离散",
    "wall 消失": "畴壁消失",
    "depinning": "退钉扎",
    "integrator / energy implementation": "积分器 / 能量实现",
    "thermal activation——本课 T=0": "热激活——本课 T=0",
    "脚本会自己打印 width / RMSE，并在不达标时直接 assert 失败": "脚本会自己打印畴壁宽度 / RMSE，并在不达标时直接触发 assert（断言）失败",
    "Lesson 02 已上线：2D bulk → u(y) → B(r)": "第 02 课已上线：二维体场 → u(y) → B(r)",
    "2D wall": "二维畴壁",
    "Extract u(y)": "提取 u(y)",
    "从 diffuse field 中找 wall position": "从 diffuse field（弥散场）中找畴壁位置",
    "Gold test": "已知答案测试",
    "flat wall 应有 B(r)≈0": "平直畴壁应有 B(r)≈0",
    "Then T>0": "然后 T>0",
    "开始复现 Caballero clean roughness growth": "开始复现 Caballero 的无无序粗糙度增长",
    "论文原式 → 最小代码 → 即时 gold test → 小尺寸 paper thumbnail → 对应回你的项目源码": "论文原式 → 最小代码 → 即时已知答案测试 → 小尺寸论文图缩略图 → 对应回你的项目源码",
    "← 回 Module 07": "← 回模块 07",
}

SMALL_REPLACEMENTS = {
    "本课只取 h=0、T=0 的 clean 1D validation unit。": "本课只取 h=0、T=0 的无无序一维验证单元。",
}

LOCKED_NUMERIC_STRINGS = ("1.415395", "0.0835%", "9.75×10⁻⁵")


def equation_body_text(eq) -> str:
    clone = BeautifulSoup(str(eq), "html.parser").select_one(".eq")
    for small in clone.select("small"):
        small.decompose()
    return clone.get_text(" ", strip=False)


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math", "small"}:
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    return False


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [equation_body_text(eq) for eq in soup.select(".eq")]
    before_pre = [pre.get_text() for pre in soup.select("pre")]
    before_code = [code.get_text() for code in soup.select("code")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]
    before_img_src = [img.get("src") for img in soup.find_all("img")]
    before_numeric_counts = {token: raw.count(token) for token in LOCKED_NUMERIC_STRINGS}

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in TEXT_REPLACEMENTS.items():
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    for small in soup.select(".eq small"):
        old = small.get_text()
        new = SMALL_REPLACEMENTS.get(old, old)
        if new != old:
            small.string = new

    if [equation_body_text(eq) for eq in soup.select(".eq")] != before_eq:
        raise RuntimeError("Lab 01 equation body changed")
    if [pre.get_text() for pre in soup.select("pre")] != before_pre:
        raise RuntimeError("Lab 01 preformatted code/output changed")
    if [code.get_text() for code in soup.select("code")] != before_code:
        raise RuntimeError("Lab 01 inline code changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Lab 01 links changed")
    if [img.get("src") for img in soup.find_all("img")] != before_img_src:
        raise RuntimeError("Lab 01 Figure path changed")

    rendered = str(soup)
    after_numeric_counts = {token: rendered.count(token) for token in LOCKED_NUMERIC_STRINGS}
    if after_numeric_counts != before_numeric_counts:
        raise RuntimeError(f"Lab 01 locked numerical results changed: {before_numeric_counts} -> {after_numeric_counts}")

    TARGET.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
