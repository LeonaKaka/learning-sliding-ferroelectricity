from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-05.html"
LOCKED_RESULTS = (
    "0.071833070", "0.0000002%", "0.0000012%", "0.995554", "0.222%",
    "0.445%", "0.104%", "1.039429", "1.039472", "0.099555",
)

REPLACEMENTS = (
    ("在 体场 Ginzburg–Landau", "在体场 Ginzburg–Landau"),
    ("投影核自相关函数 必须", "投影核自相关函数必须"),
    (" 的 样本相关函数 必须", " 的样本相关函数必须"),
    ("continuum white noise（连续白噪声） 的离散幅度", "continuum white noise（连续白噪声）的离散幅度"),
    ("动力学 前的 相关函数已知答案测试", "动力学前的相关函数已知答案测试"),
    ("先生成 按连续极限归一化的体场", "先生成按连续极限归一化的体场"),
    ("检查 体场→界面", "检查体场→界面"),
    ("先改 体场 double-well barrier", "先改体场 double-well barrier"),
    ("是 零均值、δ 相关", "是零均值、δ 相关"),
    ("barrier-幅度 coupling（势垒幅度耦合）/ 类随机键耦合", "barrier-amplitude coupling（势垒幅度耦合）/ 类随机键耦合"),
    ("你的 势垒幅度无序 也是", "你的势垒幅度无序也是"),
    ("的 耦合思路", "的耦合思路"),
    ("把 无序为零的 soliton ansatz", "把无序为零的 soliton ansatz"),
    ("独立的 体场 ζ", "独立的体场 ζ"),
    ("原样传给 wall", "原样传给畴壁"),
    ("只在 畴壁附近显著", "只在畴壁附近显著"),
    ("给出 投影核 的积分定义", "给出投影核的积分定义"),
    ("把 孤子剖面 代入", "把孤子剖面代入"),
    ("correlation scale 与 Γ 幅度 都由 bulk coupling + 孤子剖面 决定。", "相关尺度与 Γ 幅度都由体场耦合和孤子剖面决定。"),
    ("4 · 一个特别容易错的地方：continuum white noise（连续白噪声） 不是", "4 · 一个特别容易错的地方：连续白噪声不是"),
    ("Kronecker delta 与 Dirac delta", "Kronecker delta（克罗内克 δ）与 Dirac delta（狄拉克 δ）"),
    ("幅度缩放 则是", "幅度缩放则是"),
    ("Eq.23 projection", "Eq.23 投影"),
    ("解析 Eq.26、Eq.25 projection、sample 幅度/shape/zero crossing", "解析 Eq.26、Eq.25 投影、样本幅度/形状/零点交叉"),
    ("没有 时间积分", "没有时间积分"),
    ("论文同规模的相关函数测试 很轻", "论文同规模的相关函数测试很轻"),
    ("RB 体场耦合 经过有限宽度 孤子投影", "RB 体场耦合经过有限宽度孤子投影"),
    ("Eq.25 numerical projection 与 解析 Eq.26", "Eq.25 数值投影与解析 Eq.26"),
    ("连续白噪声归一化 正确", "连续白噪声归一化正确"),
    ("没有证明 退钉扎指数", "没有证明退钉扎指数"),
    ("也没有证明 滑移铁电中的真实缺陷", "也没有证明滑移铁电中的真实缺陷"),
    ("你的 RF 项 与 势垒幅度项 具有不同的 φ 依赖", "你的 RF 项与势垒幅度项具有不同的 φ 依赖"),
    ("各自投影到畴壁 后", "各自投影到畴壁后"),
    ("effective force correlator（有效力相关函数） 未必只差一个 幅度", "effective force correlator（有效力相关函数）未必只差一个幅度"),
    ("RF↔RB 孤立畴壁普适性比较 时", "RF↔RB 孤立畴壁普适性比较时"),
    ("9 · Lesson 06：从 相关函数已知答案测试 进入真正的 disordered wall geometry", "9 · 第 06 课：从相关函数已知答案测试进入真正的无序畴壁几何"),
    ("2D GL 与 1D EW", "二维 GL 与一维 EW"),
    ("大尺度粗糙度 离开", "大尺度粗糙度离开"),
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
    before_code = [x.get_text() for x in soup.select("code")]
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

    after = str(soup)
    if before_eq != [x.get_text(" ", strip=False) for x in soup.select(".eq")]:
        raise RuntimeError("Lab 05 equations changed")
    if before_pre != [x.get_text() for x in soup.select("pre")]:
        raise RuntimeError("Lab 05 machine/code pre blocks changed")
    if before_code != [x.get_text() for x in soup.select("code")]:
        raise RuntimeError("Lab 05 inline code changed")
    if before_hrefs != [x.get("href") for x in soup.find_all("a")]:
        raise RuntimeError("Lab 05 href wiring changed")
    if before_srcs != [x.get("src") for x in soup.find_all("img")]:
        raise RuntimeError("Lab 05 Figure wiring changed")
    for token, count in before_results.items():
        if after.count(token) != count:
            raise RuntimeError(f"Lab 05 locked result changed: {token}")

    TARGET.write_text(after, encoding="utf-8")
    print("Lab 05 targeted second pass complete; science/results/wiring unchanged.")


if __name__ == "__main__":
    main()
