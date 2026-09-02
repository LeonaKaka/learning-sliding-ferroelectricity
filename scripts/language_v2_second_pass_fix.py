from language_v2_second_pass import REPLACEMENTS, WHOLE_REPLACEMENTS, main

# Historical hybrid tokens left by the first Language V2 relay batch.
# Repair them explicitly; the base script still rejects any remaining bad token.
REPLACEMENTS.update({
    "无序ed-elastic-体系": "无序弹性界面体系",
    "无序ed-elastic-界面": "无序弹性界面",
    "无序ed 弹性界面": "无序弹性界面",
    "energy-势垒 函数": "能垒函数",
    "wandering/粗糙度 信息": "游走与粗糙度信息",
})

WHOLE_REPLACEMENTS.update({
    "用 关联 函数 B(L) 定量几何涨落，再把静态 ζ 与独立测得的动态 蠕变 指数 μ 放在同一个 无序ed-elastic-体系 框架里。":
        "用关联函数 B(L) 定量几何涨落，再把静态 ζ 与独立测得的动态蠕变指数 μ 放在同一个无序弹性界面框架里。",
    "结论依赖 无序ed-elastic-界面 理论、有效维数与弹性核。":
        "结论依赖无序弹性界面理论、有效维数与弹性核。",
    "其它可由 无序ed 弹性界面 描述的体系相关。":
        "其它可由无序弹性界面描述的体系相关。",
})

if __name__ == "__main__":
    main()
