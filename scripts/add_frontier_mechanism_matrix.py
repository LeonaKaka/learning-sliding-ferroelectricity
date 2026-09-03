from pathlib import Path

path = Path('modules/current-frontiers.html')
text = path.read_text(encoding='utf-8')

marker = '<div class="audit" id="screening-boundary">'
if marker not in text:
    raise SystemExit('screening-boundary anchor missing')
if 'id="mechanism-reconcile"' in text:
    raise SystemExit('mechanism-reconcile already present')

block = '''<div class="audit" id="mechanism-reconcile"><b>这些结果真的互相矛盾吗？先把结构条件对齐。</b><p>“畴壁主导”“无预存畴壁也能翻转”“多界面分阶段”看起来像三套互相排斥的故事，但它们讨论的初态、层数与慢自由度并不相同。比较机制前，先问：样品是单畴还是多畴？初态是否已有畴壁？是否完全公度？有几个滑移界面？</p>
<table class="matrix"><thead><tr><th>工作</th><th>结构条件</th><th>真正说明了什么</th><th>不能据此推出什么</th></tr></thead><tbody>
<tr><td><b>Chen 2026</b></td><td>3R-MoS₂；已有畴壁与局域钉扎结构</td><td>在其研究的含畴壁结构里，翻转可以沿确定的一维畴壁路径进行，并且不需要重新成核反向畴。</td><td>不能推出“任何无预存畴壁的滑移铁电都无法翻转”。</td></tr>
<tr><td><b>Ke 2025</b></td><td>h-BN 理论 / MD；对称性破缺畴壁</td><td>畴壁处非对角 Born 有效电荷产生净面内力，并可支持宽、波状畴壁的高速低摩擦传播。</td><td>不能把“畴壁是这种受力机制的关键自由度”升级成所有结构中预存畴壁都无条件必要。</td></tr>
<tr><td><b>Baek</b></td><td>完全公度单畴 3R-TMD 双层；初态无畴壁 / AA 网络</td><td>无预存畴壁的单畴初态仍可实现铁电翻转，因此“预存畴壁必要性”必须注明结构条件。</td><td>不能据此否定多畴样品中的畴壁介导翻转；该工作也没有实时空间成像翻转轨迹。</td></tr>
<tr><td><b>Liang 2025 / Dai 2026</b></td><td>三层 / 多界面体系；存在中间堆垛态或耦合畴壁</td><td>翻转路径可由界面钉扎、自由载流子屏蔽和畴壁间耦合共同选择；单一畴壁坐标未必够用。</td><td>不能把多界面分阶段动力学直接压成双层单畴壁模型，也不构成对双层结果的直接反例。</td></tr>
</tbody></table>
<p><b>读法：</b>这里真正需要统一的不是一句“滑移铁电究竟靠不靠畴壁”，而是先确定<strong>结构区间</strong>，再问在这个区间里哪一种自由度控制翻转。</p></div>
'''

text = text.replace(marker, block + '\n' + marker, 1)
path.write_text(text, encoding='utf-8')
print('Inserted compact mechanism-reconciliation matrix into Module 08.')
