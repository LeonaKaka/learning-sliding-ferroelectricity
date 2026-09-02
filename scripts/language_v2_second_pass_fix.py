from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab-03.html"
LOCKED_RESULTS = (
    "0.91%", "1.36%", "3.04%",
    "1.39%", "1.86%", "3.40%",
    "1.02%", "1.33%", "2.46%",
    "0.9592",
)

TEXT_REPLACEMENTS = {
    " / 复现实验室 / Lesson 03": " / 复现实验室 / 第 03 课",
    "前两课都还是 已知答案测试：先验证 畴壁剖面，再验证 畴壁提取器。": "前两课都还是已知答案测试：先验证畴壁剖面，再验证畴壁提取器。",
    "从完全平的 interface 出发": "从完全平直的界面出发",
    "thermal noise（热噪声） 逐步建立": "thermal noise（热噪声）逐步建立",
    "既有论文 Figure，也有 精确解析基准": "既有论文图，也有精确解析基准",
    "而是 论文方案 → 解析 Eq.19 → 我们的数值模拟 三层对照": "而是论文方案 → 解析 Eq.19 → 我们的数值模拟三层对照",
    "再看 相对误差": "再看相对误差",
    "作者从 平直界面 出发": "作者从平直界面出发",
    "黑色点线是 长时热粗糙度": "黑色点线是长时热粗糙度",
    "右上直接画 相对误差": "右上直接画相对误差",
    "明确的 可观测量、时间演化 和 解析基准": "明确的可观测量、时间演化和解析基准",
    "还不能叫 完整复现": "还不能叫完整复现",
    "1 · 先把 论文方案 写下来": "1 · 先把论文方案写下来",
    "Eq.19 误差验收条件 约束": "Eq.19 误差验收条件约束",
    "不是 方案参数完全一致": "并不代表方案参数完全一致",
    "“我们 独立样本数 更多”": "“我们的独立样本更多”",
    "系统尺寸 与 时间跨度 更小": "系统尺寸与时间跨度更小",
    "仍然是 缩略复现": "仍然是缩略复现",
    "bulk-to-line projection（体场到界面线投影） 得到": "bulk-to-line projection（体场到界面线投影）得到",
    "因此 扩散比": "因此扩散比",
    "的 热噪声增量 是": "的热噪声增量是",
    "这和你的 二维 quenched disorder（冻结无序） 缩放": "这和你的 quenched disorder（冻结无序）二维缩放",
    "thermal white noise（热白噪声） 同时是 空间与时间 δ 相关": "thermal white noise（热白噪声）同时具有空间与时间 δ 相关",
    "依赖 网格尺寸 和 dt": "依赖网格尺寸和 dt",
    "给了 平直初态 下": "给了平直初态下",
    "检查 长时短尺度热区间": "检查长时短尺度热区间",
    "periodic Laplacian（周期拉普拉斯算子） 对应 界面线弹性": "periodic Laplacian（周期拉普拉斯算子）对应界面线弹性",
    "第二行是 确定性弛豫": "第二行是确定性弛豫",
    "5 · B(r,t) 不是拿一条 interface 就结束": "5 · B(r,t) 不是拿一条界面就结束",
    "同时平均 y 和 independent thermal 独立样本数": "同时对 y 和独立热噪声样本求平均",
    "10 条 独立样本 的离散程度": "10 条独立样本的离散程度",
    "采样噪声 用 64 独立样本数": "采样噪声，用 64 个独立样本",
    "但最终 统计单位 仍然是 独立样本": "但最终统计单位仍然是独立样本",
    "同一批 界面样本": "同一批界面样本",
    "correlation function（相关函数） 的不同 间距": "correlation function（相关函数）的不同间距",
    "最靠近 晶格尺度 的 r": "最靠近晶格尺度的 r",
    "感受到 有限尺寸 / 周期边界效应": "感受到有限尺寸 / 周期边界效应",
    "<th>time</th>": "<th>时刻</th>",
    "<th>median 相对误差</th>": "<th>相对误差中位数</th>",
    "<th>RMS 相对误差</th>": "<th>相对误差 RMS</th>",
    "<th>max 相对误差</th>": "<th>最大相对误差</th>",
    "接近 long-time thermal slope": "接近长时热斜率",
    "Eq.19 relative error": "Eq.19 相对误差",
    "先证明 B(r,t) 实现 和 thermal FDT 没问题": "先证明 B(r,t) 实现和热噪声 FDT 没问题",
    "同一 映射参数 放回": "同一映射参数放回",
    "检验 体场→界面线映射": "检验体场→界面线映射",
    "区分是 求解器/噪声 错": "区分是求解器/噪声出错",
    "还是 有限畴壁宽度 / 体场涨落 引起": "还是有限畴壁宽度 / 体场涨落引起",
    "放 一维 EW 理论、一维 EW 数值模拟、二维 GL 提取畴壁 三者": "放一维 EW 理论、一维 EW 数值模拟、二维 GL 提取畴壁三者",
    "向 界面线预测 靠近": "向界面线预测靠近",
    "同一套 提取器/B(r)/S(q) 迁到 滑移铁电周期模型": "同一套提取器/B(r)/S(q) 迁到滑移铁电周期模型",
    "← 第 02 课 · bulk → u(y)": "← 第 02 课 · 体场 → u(y)",
    "第 04 课 · GL → EW validity boundary →": "第 04 课 · GL → EW 适用边界 →",
}


def blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    if parent.find_parent(class_="eq") or "eq" in parent.get("class", []):
        return True
    if parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []):
        return True
    return False


def main() -> None:
    raw = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    before_eq = [eq.get_text(" ", strip=False) for eq in soup.select(".eq")]
    before_pre = [pre.get_text() for pre in soup.select("pre")]
    before_code = [code.get_text() for code in soup.select("code")]
    before_hrefs = [a.get("href") for a in soup.find_all("a")]
    before_src = [img.get("src") for img in soup.find_all("img")]
    before_sources = [node.get_text() for node in soup.select(".source-text")]
    before_results = {token: raw.count(token) for token in LOCKED_RESULTS}

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or blocked(node):
            continue
        old = str(node)
        new = old
        for src, dst in TEXT_REPLACEMENTS.items():
            new = new.replace(src, dst)
        if new != old:
            node.replace_with(new)

    # Table headings are elements, so localize them without touching numerical cells.
    for th in soup.find_all("th"):
        mapping = {
            "time": "时刻",
            "median 相对误差": "相对误差中位数",
            "RMS 相对误差": "相对误差 RMS",
            "max 相对误差": "最大相对误差",
        }
        if th.get_text(strip=True) in mapping:
            th.string = mapping[th.get_text(strip=True)]

    if soup.title:
        soup.title.string = "Reproduction Lab（复现实验室）03 · EW 热粗糙化缩略复现"

    figures = soup.select("figure.fig img")
    if len(figures) != 2:
        raise RuntimeError(f"Lab 03 expected 2 Figures, found {len(figures)}")
    figures[0]["alt"] = "Caballero 2020 图 2：界面粗糙度随时间演化"
    figures[1]["alt"] = "本课 EW 数值模拟与 Caballero Eq.19 的粗糙度对照"

    if [eq.get_text(" ", strip=False) for eq in soup.select(".eq")] != before_eq:
        raise RuntimeError("Lab 03 equation body changed")
    if [pre.get_text() for pre in soup.select("pre")] != before_pre:
        raise RuntimeError("Lab 03 code/output block changed")
    if [code.get_text() for code in soup.select("code")] != before_code:
        raise RuntimeError("Lab 03 inline code changed")
    if [a.get("href") for a in soup.find_all("a")] != before_hrefs:
        raise RuntimeError("Lab 03 links changed")
    if [img.get("src") for img in soup.find_all("img")] != before_src:
        raise RuntimeError("Lab 03 Figure wiring changed")
    if [node.get_text() for node in soup.select(".source-text")] != before_sources:
        raise RuntimeError("Lab 03 paper source text changed")

    rendered = str(soup)
    after_results = {token: rendered.count(token) for token in LOCKED_RESULTS}
    if after_results != before_results:
        raise RuntimeError(f"Lab 03 locked results changed: {before_results} -> {after_results}")
    TARGET.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
