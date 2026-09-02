from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-06.html"
LOCKED_RESULTS = (
    "1.227%", "6.122%", "0.538906", "0.509213", "0.694308",
    "0.664796", "0.982981", "1.371256", "0.077925",
)

REPLACEMENTS = (
    ("Code", "代码"),
    (" / Reproduction Lab（复现实验室） / Lesson 06", " / 复现实验室 / 第 06 课"),
    ("后续 Paper2", "后续第二篇工作"),
    ("同时跑 二维 Ginzburg–Landau（GL）体场 和映射后的 一维 Edwards–Wilkinson（EW）界面", "同时跑二维 Ginzburg–Landau（GL）体场和映射后的一维 Edwards–Wilkinson（EW）界面"),
    ("再用 real-space roughness（实空间粗糙度） B(r,t) 与 structure factor（傅里叶空间结构因子） S(q,t)", "再用实空间 roughness（粗糙度） B(r,t) 与傅里叶空间 structure factor（结构因子） S(q,t)"),
    ("两个观测量 上", "两个观测量上"),
    ("才能叫 跨模型几何映射通过", "才能叫跨模型几何映射通过"),
    ("而要声称 random-bond ", "而要声称随机键 "),
    ("由 B 与 S 得到的有效指数 在", "由 B 与 S 得到的有效指数在"),
    ("作者把 长时间区间 与 随机键粗糙度", "作者把长时间区间与随机键粗糙度"),
    ("给出的 有效 ζ", "给出的有效 ζ"),
    ("的 估计量", "的估计量"),
    ("GL 与 EW 几何统计 已经", "GL 与 EW 几何统计已经"),
    ("B-derived 和 S-derived ζ", "由 B 与 S 得到的 ζ"),
    ("已复现 随机键普适性", "已复现随机键普适性"),
    ("同一 体场无序物理", "同一体场无序物理"),
    ("提取出的畴壁 和", "提取出的畴壁和"),
    ("的 跨模型一致性 检验", "的跨模型一致性检验"),
    ("使 粗糙指数 接近 随机键平衡值", "使粗糙指数接近随机键平衡值"),
    ("估计量 consistency", "估计量一致性"),
    ("与 尺寸/时间收敛", "与尺寸/时间收敛"),
    ("说 普适性成立", "说普适性成立"),
    ("同一条界面 的", "同一条界面的"),
    ("的 有效 ζ", "的有效 ζ"),
    ("某个 傅里叶尺度区间", "某个傅里叶尺度区间"),
    ("哪些 论文物理设定", "哪些论文物理设定"),
    ("GL wall 估计量", "GL 畴壁估计量"),
    ("这节不是 与 Fig.5", "这节不是与 Fig.5"),
    ("GL→EW 映射 有没有", "GL→EW 映射有没有"),
    ("投给 长时间/大尺寸", "投给长时间/大尺寸"),
    ("同一条 无序传递链", "同一条无序传递链"),
    ("2D bulk", "二维体场"),
    ("Lesson03", "第 03 课"),
    ("Lesson04", "第 04 课"),
    ("Lesson05", "第 05 课"),
    ("Lesson06", "第 06 课"),
    ("finite-T bulk→wall 估计量", "有限温体场→畴壁估计量"),
    ("的 随机键耦合", "的随机键耦合"),
    ("的 随机力", "的随机力"),
    ("验证的 畴壁层钉扎统计", "验证的畴壁层钉扎统计"),
    ("Laplacian 写反了", "Laplacian（拉普拉斯算子）写反了"),
    ("集中到 含无序动力学、有限尺寸/有限时间 或 映射假设", "集中到含无序动力学、有限尺寸/有限时间或映射假设"),
    ("用 对称相对差 比较", "用对称相对差比较"),
    ("强的 跨模型一致性", "强的跨模型一致性"),
    ("这个 checkpoint", "这个阶段验证"),
    ("体场 GL 与 降维后的 EW 对 实空间畴壁几何", "体场 GL 与降维后的 EW 对实空间畴壁几何"),
    ("傅里叶空间 对 小尺度/大尺度过渡", "傅里叶空间对小尺度/大尺度过渡"),
    ("预定义 对数分箱", "预定义对数分箱"),
    ("只用 分箱中心", "只用分箱中心"),
    ("高 q 密集 modes", "高 q 密集模式"),
    ("10% 判据 内", "10% 判据内"),
    ("cross-model mapping", "跨模型映射"),
    ("在 傅里叶观测量 上", "在傅里叶观测量上"),
    ("对数分箱 不是", "对数分箱不是"),
    ("估计量 weight", "估计量权重"),
    ("仍然是 realization", "仍然是独立无序样本"),
    ("明显 跨尺度过渡", "明显的跨尺度过渡"),
    ("一条 估计量 的接近", "一个估计量的接近"),
    ("同一观测量 上", "同一观测量上"),
    ("说明 模型降维 已有", "说明模型降维已有"),
    ("由 B 与 S 得到的指数 尚未", "由 B 与 S 得到的指数尚未"),
    ("同一 标度区间 中", "同一标度区间中"),
    ("作为 论文目标值/斜率参考", "作为论文目标值/斜率参考"),
    ("我们的 测得的渐近指数", "我们测得的渐近指数"),
    ("GL↔EW 一致性 已很好", "GL↔EW 一致性已经很好"),
    ("模型的 几何分析流程", "模型的几何分析流程"),
    ("给不同 有效 ζ", "给出不同的有效 ζ"),
    ("目前 拟合区间 不处在单一 渐近区间", "目前拟合区间不处在单一渐近区间"),
    ("优先做 计算更省的 EW 的 时间/尺寸阶梯", "优先对计算更省的 EW 做时间/尺寸阶梯"),
    ("确认 指数收敛 后", "确认指数收敛后"),
    ("另一个 合理性检查", "另一个合理性检查"),
    ("体场畴壁剖面 还健康吗", "体场畴壁剖面还健康吗"),
    ("如果 无序已", "如果无序已"),
    ("单值界面映射 也可能", "单值界面映射也可能"),
    ("本课的 有限温孤子拟合 给出", "本课的有限温孤子拟合给出"),
    ("接近 干净低温剖面", "接近干净低温剖面"),
    ("当前阶段验证 还在", "当前阶段验证还在"),
    ("以后 disorder 更强时", "以后无序更强时"),
    ("这一层 拓扑/剖面质量检查 必须", "这一层拓扑/剖面质量检查必须"),
    ("CI 保存的最终输出", "自动化测试保存的最终输出"),
    ("Lesson01–06", "第 01–06 课"),
    ("已经覆盖了 干净畴壁", "已经覆盖了干净畴壁"),
    ("服务 第一篇工作的翻转/无序比较 方法可信度", "服务第一篇工作的翻转/无序比较方法可信度"),
    ("这里的 渐近 ζ 判据", "这里的渐近 ζ 判据"),
    ("继续加 时间/尺寸阶梯", "继续增加时间/尺寸阶梯"),
    ("未来 粗糙度精修", "未来粗糙度精修"),
    ("预先存在的 孤立畴壁", "预先存在的孤立畴壁"),
    ("矫顽尺度 可以包含 成核、多墙和 协议速率效应", "矫顽尺度可以包含成核、多墙和协议速率效应"),
    ("退钉扎阈值 是一条预先存在的 wall 在 恒定驱动 下 pinned ↔ moving", "退钉扎阈值是一条预先存在的畴壁在恒定驱动下钉扎态 ↔ 运动态"),
)


def blocked(node: NavigableString) -> bool:
    p = node.parent
    if p is None or p.name in {"script", "style", "pre", "code", "math"}:
        return True
    return bool(p.find_parent(class_="eq") or "eq" in p.get("class", []))


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [x.get_text(" ", strip=False) for x in soup.select(".eq")]
    before_pre = [x.get_text() for x in soup.select("pre")]
    before_hrefs = [x.get("href") for x in soup.find_all("a")]
    before_srcs = [x.get("src") for x in soup.find_all("img")]
    before_results = {x: raw.count(x) for x in LOCKED_RESULTS}

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in REPLACEMENTS:
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 06 expected 2 Figures, found {len(figures)}")
    figures[0]["alt"] = "Caballero 2020 图 5：含无序 GL 与 EW 的粗糙度和结构因子"
    figures[1]["alt"] = "本课含无序 GL 与 EW 几何阶段验证"

    after = str(soup)
    if before_eq != [x.get_text(" ", strip=False) for x in soup.select(".eq")]:
        raise RuntimeError("Lab 06 equations changed")
    if before_pre != [x.get_text() for x in soup.select("pre")]:
        raise RuntimeError("Lab 06 machine/code blocks changed")
    if before_hrefs != [x.get("href") for x in soup.find_all("a")]:
        raise RuntimeError("Lab 06 href wiring changed")
    if before_srcs != [x.get("src") for x in soup.find_all("img")]:
        raise RuntimeError("Lab 06 Figure wiring changed")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 06 locked result changed: {token}")
    if "渐近 ζ 判据：未通过。" not in after:
        raise RuntimeError("Lab 06 asymptotic-zeta failure boundary missing")
    if "CROSS-MODEL GEOMETRY PASS; ASYMPTOTIC ZETA GATE NOT PASSED" not in "\n".join(before_pre):
        raise RuntimeError("Lab 06 machine verdict marker changed")

    TARGET.write_text(after, encoding="utf-8")
    print("Lab 06 targeted Language V2 audit complete; science/results unchanged.")


if __name__ == "__main__":
    main()
