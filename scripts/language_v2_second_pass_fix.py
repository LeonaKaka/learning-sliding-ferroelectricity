from __future__ import annotations

import re
from bs4 import BeautifulSoup, NavigableString
import language_v2_second_pass as base

# Language V2 is being repaired page by page. Keep this relay scoped to
# Module 04 so later lessons cannot be rewritten before they are reviewed.
TARGET = base.ROOT / "modules/pinning-creep.html"
base.FILES = [TARGET]

# Exact prose repairs for the ordinary teaching layer. base.main() protects
# .source-text, equations, code, paper titles and links from these replacements.
base.REPLACEMENTS.update({
    "短尺度 slope": "短尺度斜率",
    "退钉扎 simulation": "退钉扎模拟",
    "畴壁 extraction": "畴壁提取",
    "scaling 区间": "标度区间",
    "谱 scaling 分裂": "谱标度分裂",
    "局域 关联 functions": "局域关联函数",
    "anomalous / 超粗糙标度": "异常 / 超粗糙标度",
    "尺度 mask": "尺度屏蔽范围",
    "畴壁 core": "畴壁核",
    "体系 size": "体系尺寸",
    "畴壁 width": "畴壁宽度",
    "grid、diffuse-core、等值线 jitter": "网格、弥散畴壁核、等值线抖动",
    "finite size": "有限尺寸",
    "periodicity": "周期性",
    "有效斜率 stability": "有效斜率稳定性",
    "Extraction 敏感性": "提取方法敏感性",
    "extraction method": "提取方法",
    "坍缩 outcome": "坍缩结果",
    "generic anomalous-标度类型": "一般异常标度类型",
    "局域 无序 variations": "局域无序变化",
    "quenched source i": "独立无序样本 i",
    "valid wall snapshot / steady ensemble": "有效畴壁快照 / 稳态集合",
    "来源 uncertainty": "样本层级不确定性",
    "场 或 time": "场或时间",
    "映射 failure": "映射失效",
    "界面 density": "界面密度",
    "R0 · visual": "R0 · 目视",
    "R1 · stable 区间": "R1 · 稳定区间",
    "R3 · cross-可观测量": "R3 · 跨可观测量",
    "apparent / illustrative 粗糙度": "表观 / 示意性粗糙度",
    "粗糙度 scaling supported over tested 尺度": "已测试尺度内的粗糙度标度得到支持",
    "strong 普适性 证据, not 指数 匹配 alone": "较强的普适性证据，但不能只靠指数匹配",
    "switched-area 平台区": "翻转面积平台区",
    "curve 平台区": "曲线平台区",
    "PFM 钉扎 image": "PFM 钉扎图像",
    "局域 point 缺陷": "局域点缺陷",
    "实空间 pause": "实空间停滞",
    "panel (c)": "分图 (c)",
    "畴 itself 是缺陷": "畴本身就是缺陷",
    "pristine-畴 positions": "原始畴位置",
    "immobile/局域 缺陷态": "不动的局域缺陷态",
    "畴壁 bowing": "畴壁弯曲",
    "thermodynamic 临界 阈值": "热力学临界阈值",
    "velocity–场 characteristic": "速度–场特征曲线",
    "亚稳 barriers": "亚稳势垒",
    "热-噪声 average": "热噪声平均",
    "固定 quenched 无序景观": "固定淬火无序景观",
    "velocity–force characteristic": "速度–驱动力特征曲线",
    "activated 区间": "热激活区间",
    "quenched 景观": "淬火无序景观",
    "条件 热 average / 方差": "条件热平均 / 方差",
    "畴壁 points": "畴壁上的点",
    "做 uncertainty": "估计不确定性",
    "分层 模型": "分层模型",
    "畴壁 problem": "畴壁问题",
    "zero-displacement / velocity 上界": "零位移 / 速度上界",
    "畴壁 relaxation": "畴壁弛豫",
    "forward 漂移": "前向漂移",
    "翻转 object": "翻转对象",
    "multiple walls": "多畴壁",
    "deep-蠕变 区间": "深蠕变区间",
    "低 drive": "低驱动力",
    "热-rounding": "热圆滑",
    "waiting-time": "等待时间",
    "截止 dependence": "截止尺度依赖",
    "clean 蠕变 区间": "可靠的蠕变区间",
    "提高 drive": "提高驱动力",
    "退钉扎 as a 临界 phenomenon": "作为临界现象的退钉扎",
    "long 瞬态": "长瞬态",
    "one μ": "一个 μ",
    "random 流形": "随机流形",
    "微观 来源 remains to be determined": "微观来源仍有待确定",
    "偶极 interactions": "偶极相互作用",
    "point 缺陷": "点缺陷",
})

# These tokens can occur in elements intentionally skipped by base.main()
# (rules, equations, links, navigation), so apply them only in this reviewed
# page-specific pass. Source quotes remain excluded.
POST_REPLACEMENTS = {
    "中的 正式发表 PDF": "中的正式发表 PDF",
    "连字 与数学": "连字与数学",
    "留到 Module 05": "留到模块 05",
    "完整段落s": "完整段落",
    "“rough”在这里有数学定义": "这里的“粗糙”有明确数学定义",
    "B、S 与 W 的 scaling 形式": "B、S 与 W 的标度形式",
    "UV · r≈dx / 畴壁宽度": "短尺度端 · r≈dx / 畴壁宽度",
    "IR · r≈L / few q 模式": "长尺度端 · r≈L / 少数 q 模式",
    "log–log 图": "双对数图",
    "一段 log–log 近似直线": "一段双对数近似直线",
    "quenched source i → valid wall snapshot / steady ensemble": "独立无序样本 i → 有效畴壁快照 / 稳态集合",
    "局域畴壁 pause": "局域畴壁停滞",
    "一条 switched-area 曲线": "一条翻转面积曲线",
    "畴壁 wandering": "畴壁游走",
    "APS official record": "APS 官方记录",
    "测 velocity": "测速度",
    "新的 quenched 样本": "新的淬火无序样本",
    "“无序无序样本”": "“无序样本总体”",
    "项目 Drive PDF": "项目 Google Drive PDF",
}


def hard_blocked(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or parent.name in {"script", "style", "pre", "code", "math"}:
        return True
    return bool(parent.find_parent(class_="source-text") or "source-text" in parent.get("class", []))


def polish_all_visible_text() -> None:
    before_text = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(before_text, "html.parser")
    before_sources = base.source_blocks(soup)

    # Navigation is intentionally outside the generic replacement layer.
    header_small = soup.select_one("header .bar b small")
    if header_small:
        header_small.string = "· 04 Pinning（钉扎）、Creep（蠕变）与 Roughness（粗糙度）"
    header_links = soup.select("header .bar span a")
    if len(header_links) >= 3:
        header_links[0].string = "知识图谱"
        header_links[1].string = "粗糙度"
        header_links[2].string = "钉扎"
    kicker = soup.select_one(".kicker")
    if kicker:
        kicker.string = "模块 04 · Pinning（钉扎）、Creep（蠕变）与 Roughness（粗糙度）"
    breadcrumb = soup.select_one("main > .rule")
    if breadcrumb:
        for node in list(breadcrumb.find_all(string=True)):
            if "Module 04" in str(node):
                node.replace_with(str(node).replace("Module 04", "模块 04"))
    next_links = soup.select(".next a")
    if len(next_links) >= 2:
        next_links[1].string = "05 Depinning（退钉扎）· 临界现象 →"
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta["content"] = "以 Tybell 2002、Paruch 2005、Kim 2014 与有限温界面理论为证据链，学习铁电畴壁的钉扎、蠕变与粗糙度。"

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or hard_blocked(node):
            continue
        old = str(node)
        new = old
        for a, b in sorted(POST_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
            new = new.replace(a, b)
        # Repair whitespace inserted between ordinary Chinese words by the
        # historical mechanical pass; source quotes are excluded above.
        new = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", new)
        new = re.sub(r"\s+([，。；：！？、）])", r"\1", new)
        new = re.sub(r"（\s+", "（", new)
        new = new.replace("published PDF", "正式发表 PDF")
        new = new.replace("完整 paragraph", "完整段落")
        new = new.replace("完整 paragraphs", "完整段落")
        new = new.replace("ligature", "连字")
        new = new.replace("Figure 均", "论文图均")
        new = new.replace("点击 Figure 看", "点击图片查看")
        new = new.replace("原 Figure", "原论文图")
        new = new.replace("paper PDF", "论文 PDF")
        new = new.replace("PFM snapshots", "PFM 快照")
        new = new.replace("Fourier 模式", "傅里叶模式")
        if new != old:
            node.replace_with(new)

    if base.source_blocks(soup) != before_sources:
        raise RuntimeError("Module 04 source-text changed during page-specific polish")
    TARGET.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    base.main()
    polish_all_visible_text()
