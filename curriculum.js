window.LSF_DATA = {
  modules: [
    {
      id: 'foundations', number: '01', title: 'What is Sliding Ferroelectricity?', short: '堆垛、对称性与极化',
      question: 'AB / BA / 3R 堆垛为什么会产生可翻转的面外极化？所谓 sliding ferroelectricity（滑移铁电）真正改变的是什么？',
      thesis: '先建立材料本身的物理图像。这里不追求把所有二维铁电都学一遍，只把“堆垛 → 对称性破缺 → 层间电荷重分布 → 极化”这条因果链讲清楚。',
      concepts: ['stacking order（堆垛次序）','inversion symmetry（反演对称性）','interlayer charge transfer（层间电荷转移）','out-of-plane polarization（面外极化）','AB / BA / 3R'],
      core: ['wu2021','yasuda2021','stern2021','meng2022','ji2023'],
      supporting: ['Zhang et al. 2025 · Emerging frontiers in 2D sliding ferroelectrics','Woods et al. 2021 · charge-polarized interfacial superlattices in twisted hBN','Enaldiev et al. 2022 · scalable network model for ferroelectric domains'],
      takeaway: '读完后应该能自己解释：为什么一块非极性的单层材料经过特定堆垛后会出现面外极化，以及 AB ↔ BA 与 P ↔ −P 为什么相连。'
    },
    {
      id: 'pathways', number: '02', title: 'How Does Switching Proceed?', short: '翻转路径与中间态',
      question: '极化翻转真的是整层同步滑过去吗？多层体系为什么会出现中间态和多条翻转路径？',
      thesis: '从“静态堆垛”进入“动态翻转”。重点不是记住多少堆垛名称，而是理解 switching pathway（翻转路径）为什么会受到界面、钉扎以及载流子屏蔽的影响。',
      concepts: ['switching pathway（翻转路径）','intermediate state（中间态）','metastability（亚稳性）','multi-interface（多界面）','layer-selective switching（层选择性翻转）'],
      core: ['yang2024','sui2024','liang2025'],
      supporting: ['Yang et al. 2023 · shear-transformation-mediated 3R-MoS₂ transistors','Ouyang et al. 2025 · electrically switching ferroelectric order in 3R-MoS₂','Wang et al. 2025 · cluster sliding ferroelectricity','Dai et al. 2026 · coupled DW dynamics in trilayer γ-InSe'],
      takeaway: '读完后应该能画出双层与三层体系的典型翻转路径，并说清楚“中间态”究竟是一个新相、一个亚稳堆垛，还是局域畴壁运动留下的结果。'
    },
    {
      id: 'walls', number: '03', title: 'Domain Walls: What Actually Moves?', short: '真正运动的自由度',
      question: '什么结构条件下，极化翻转主要由 pre-existing domain wall（预存畴壁）完成？完全共格的单畴样品为什么又可能出现无畴壁翻转？',
      thesis: '这是全站最重要的机制边界：许多含畴壁的滑移铁电样品中，翻转主要由预存畴壁传播完成；但完全共格单畴样品说明，畴壁并不是所有滑移铁电翻转的无条件必要条件。后续的钉扎、蠕变和退钉扎，只针对“畴壁介导”这条受控研究路径展开。',
      concepts: ['pre-existing DW（预存畴壁）','symmetry breaking（对称性破缺）','off-diagonal Born effective charge（非对角 Born 有效电荷）','nucleation-free switching（无成核翻转）','1D DW pathway（一维畴壁路径）'],
      core: ['wangdong2025','ke2025','chen2026','liu2026'],
      supporting: ['Shi et al. 2025 · soliton-like DW motion with ultralow damping','Deng et al. 2025 · deterministic and efficient switching','Jia-Wen Li et al. 2026 · ultralow-barrier sliding and pinning in moiré superlattices','Baek et al. 2026 · DW-free switching in fully commensurate 3R-TMD bilayers'],
      takeaway: '读完后应该能把“no domain wall, no polarization reversal”改写成带条件的机制命题：它在哪类含畴壁的 3R-MoS₂ 实验中有强证据，以及为什么不能外推成所有滑移铁电的一般定律。'
    },
    {
      id: 'pinning', number: '04', title: 'Pinning, Creep & Roughness', short: '真实畴壁为什么走不直',
      question: '真实样品中的畴壁为什么不是匀速平移？缺陷怎样改变畴壁速度、形貌和开关场？',
      thesis: '先从传统铁电畴壁学习 disorder（无序）的实验语言。creep（蠕变）不是一个拟合公式，roughness（粗糙度）也不是“墙看起来很毛”；它们都是界面与无序共同作用后产生的可观测结果。',
      concepts: ['pinning centre（钉扎中心）','creep（蠕变）','roughness（粗糙度）','local barrier（局域势垒）','collective motion（集体运动）'],
      core: ['tybell2002','paruch2005','kim2014'],
      supporting: ['Lemerle et al. 1998 · magnetic DW creep + wandering','Kleemann 2007 · universal domain-wall dynamics in disordered ferroics','Metaxas et al. 2007 · creep-to-flow velocity regimes','Guyonnet et al. 2012 · multiscaling of FE DW roughness','Jeudy et al. 2016 · universal pinning-energy barrier','Tückmantel et al. 2021 · creep vs depinning event statistics','Bulanadi et al. 2024 · point/extended defects and jerky DW motion','Teng et al. 2025 · point-defect control of FE DW dynamics'],
      takeaway: '读完后应该能看到一张畴壁图像或 v(E) 曲线，就知道哪些特征可能来自钉扎、哪些可以用蠕变描述，以及哪些现象还不能直接称为退钉扎。'
    },
    {
      id: 'depinning', number: '05', title: 'Depinning as a Critical Phenomenon', short: '阈值、指数与有限尺寸',
      question: '什么时候一个被钉扎的界面真正进入持续运动？为什么 β、ζ、ν 与 finite-size scaling（有限尺寸标度）比“画出一条幂律”更重要？',
      thesis: '把畴壁抽象成受 quenched disorder（淬火无序）作用的 elastic interface（弹性界面）。这里建立临界驱动力、临界几何、速度标度和有限尺寸标度的统一语言。',
      concepts: ['elastic interface（弹性界面）','critical force（临界驱动力）','velocity exponent β（速度指数 β）','roughness exponent ζ（粗糙度指数 ζ）','correlation length（关联长度）','finite-size scaling（有限尺寸标度）'],
      core: ['chauve2000','rosso2003','ferrero2013','wiese2022'],
      supporting: ['Jeudy et al. 2016 · cross-material barrier collapse','Ferrero et al. 2021 · creep motion review','Le Doussal et al. 2004 · functional RG for disordered elastic systems','Drossel & Dahmen 1998 · RFIM DW depinning','Zhou et al. 2009 · short-time RFIM DW dynamics','Qian et al. 2023 · nonsteady dynamic depinning'],
      takeaway: '读完后应该能设计一个规范的退钉扎数值实验：先定义 f_c / E_c，再测稳态速度 v、粗糙度、关联长度和尺寸依赖，而不是只在单一尺寸上拟合 β。'
    },
    {
      id: 'disorder', number: '06', title: 'Disorder & RFIM', short: '局域随机性怎样变成集体开关',
      question: '如果不把畴壁只看成一条弹性线，而从局域翻转倾向、相互耦合与外驱动出发，会得到什么？',
      thesis: 'RFIM（随机场 Ising 模型）提供了另一套粗粒化语言：它帮助理解局域随机场、hysteresis（滞回）、avalanches（雪崩）以及无序控制的临界行为；但网站会始终强调“sliding FE ≠ RFIM”。',
      concepts: ['quenched disorder（淬火无序）','random field（随机场）','random bond（随机键）','hysteresis（滞回）','avalanches（雪崩）','scaling collapse（标度坍缩）'],
      core: ['sethna1993','dahmen1996','dong2012'],
      supporting: ['Seppälä et al. 1998 · RFIM domain-wall roughening','Vives et al. 2005 · hysteresis and avalanches','Chan et al. 2024 · coercivity distribution','Paul et al. 2026 · disorder and multi-domain kinetics in CVD 3R-WSe₂'],
      takeaway: '读完后应该能区分：弹性界面退钉扎与 RFIM 翻转各自保留了哪些自由度、适合解释哪些数据，以及什么时候两种语言可能给出不同预测。'
    },
    {
      id: 'modeling', number: '07', title: 'From Theory to Numerical Modeling', short: '相场、TDGL 与涌现界面',
      question: '怎样从连续场模型得到畴、畴壁和受驱界面？怎样加入无序而不让离散化偷偷改变物理尺度？',
      thesis: '这一章不做软件教程，而是建立模型层次：Landau free energy（Landau 自由能）→ TDGL / phase field（相场）→ diffuse wall（弥散畴壁）→ emergent elastic interface（涌现弹性界面）→ 无序驱动动力学。',
      concepts: ['order parameter（序参量）','Landau free energy（Landau 自由能）','TDGL','phase field（相场）','diffuse interface（弥散界面）','coarse graining（粗粒化）'],
      core: ['chen2008','caballero2020'],
      supporting: ['Wang et al. 2004 · phase-field polarization switching','Fedeli et al. 2019 · FE domains with defects','Hong & Viswanathan 2020 · open-source phase-field','Dai et al. 2026 · multilayer coupled-interface boundary','Zhu et al. 2022 · FE DW memory','Lv & Lynch 2018 · rhombohedral FE domain walls','FerroX 2023 · GPU phase-field framework'],
      takeaway: '读完后应该能说明自己的模拟位于哪个粗粒化层次：哪些参数是材料参数，哪些是有效参数；并知道怎样验证晶格间距、dx 和系统尺寸没有偷偷改变无序强度。'
    },
    {
      id: 'frontier', number: '08', title: 'Current Frontiers', short: '回到 3R-MoS₂ / WSe₂ 的前沿证据',
      question: '2025–2026 年的实验和理论已经把畴壁与钉扎证据推进到哪里？距离讨论 universality（普适性）还缺什么？',
      thesis: '最后不再引入新的基础理论，而是重新阅读最新滑移铁电工作：哪些样品由畴壁主导、哪些结构允许无畴壁翻转、多层体系何时需要考虑耦合界面，以及哪些关键标度量仍然没有被系统测量。',
      concepts: ['pinning landscape（钉扎景观）','cycle-to-cycle variability（周期间波动）','partial switching（部分翻转）','multidomain kinetics（多畴动力学）','universality test（普适性检验）'],
      core: ['liang2025','wangdong2025','ke2025','chen2026','liu2026'],
      supporting: ['Paul et al. 2026 · disorder dynamics in CVD 3R-WSe₂','Baek et al. 2026 · fully commensurate DW-free switching','Dai et al. 2026 · coupled DW dynamics in trilayer γ-InSe','Jia-Wen Li et al. 2026 · DW-mediated ultralow-barrier sliding','Remez & Goldstein 2025 · hierarchical ordering transitions','Lee et al. 2025 · theory of slidetronics'],
      takeaway: '最终应该能自己审一篇新论文：作者观察到钉扎了吗？有明确阈值吗？测了 v(E) 吗？测了 ζ / β / ν 吗？做了尺寸标度吗？如果没有，就不要把“幂律”直接等同于普适性。'
    }
  ],
  papers: [
    {id:'wu2021',year:2021,title:'Sliding ferroelectricity in 2D van der Waals materials: Related physics and future opportunities',authors:'M. Wu · J. Li',kind:'综述 / 入门',module:'foundations',role:'用一篇综述建立全局词汇和材料谱系，不要求从最早的 2017 年工作逐篇追起。',question:'滑移铁电的基本定义、主要材料类型和早期物理问题是什么？',figure:'综述中概括滑移诱导极化与翻转机制的总览示意图。',quote:'重点读作者如何定义 sliding ferroelectricity（滑移铁电），以及 relative interlayer translation（层间相对平移）在其中起什么作用。',next:'yasuda2021'},
    {id:'yasuda2021',year:2021,title:'Stacking-engineered ferroelectricity in bilayer boron nitride',authors:'K. Yasuda et al.',kind:'实验',module:'foundations',role:'把“堆垛依赖极化”从理论概念落实到双层 hBN 实验。',question:'AB / BA 堆垛对应的相反极化怎样被实验读出？',figure:'AB / BA 堆垛与极化示意，以及代表性的电学或畴响应。',quote:'重点读作者怎样把堆垛结构与可翻转极化联系起来。',next:'stern2021'},
    {id:'stern2021',year:2021,title:'Interfacial ferroelectricity by van der Waals sliding',authors:'M. Vizner Stern et al.',kind:'实验',module:'foundations',role:'在真实空间看到相反极化畴，并把探针诱导的翻转与层间横向滑移联系起来。',question:'怎样依靠空间畴图像，而不是只看一条滞回曲线，证明界面铁电性？',figure:'相反极化畴的扫描探针图，以及外加偏压驱动后的畴变化。',quote:'重点读作者如何把 polarization reversal（极化反转）与 van der Waals sliding（范德华滑移）联系起来。',next:'meng2022'},
    {id:'meng2022',year:2022,title:'Sliding induced multiple polarization states in two-dimensional ferroelectrics',authors:'P. Meng et al.',kind:'实验 / 多层体系',module:'foundations',role:'从双层二态进入多层体系：不同范德华界面的偶极可以组合，因此出现稳定中间态。',question:'为什么层数增加后，体系不再只有 +P 与 −P 两种状态？',figure:'多层堆垛构型与对应极化状态的主图。',quote:'重点读作者如何把 multiple polarization states（多极化态）与不同界面的滑移构型联系起来。',next:'ji2023'},
    {id:'ji2023',year:2023,title:'General Theory for Bilayer Stacking Ferroelectricity',authors:'J. Ji et al.',kind:'理论',module:'foundations',role:'用 symmetry（对称性）和 layer group（层群）语言，把具体材料案例抽象成一般判据。',question:'什么样的单层对称性与堆垛操作能够产生极性的双层结构？',figure:'对称操作与极性 / 非极性双层结构的分类示意。',quote:'重点读作者给出的双层堆垛铁电一般判据。',next:'yang2024'},

    {id:'yang2024',year:2024,title:'Non-volatile electrical polarization switching via domain wall release in 3R-MoS₂ bilayer',authors:'D. Yang et al.',kind:'实验',module:'pathways',role:'主线中的关键桥梁：一次翻转事件被解释为预存畴壁从钉扎位置释放并扫过样品。',question:'这里的 coercive field（矫顽场）更像“本征成核场”，还是局域的 depinning field（退钉扎场）？',figure:'优先看直接展示畴壁释放、钉扎位置与翻转场关系的核心图，而不是器件结构图。',quote:'重点读作者如何用随机钉扎势解释不同位置或不同循环中的翻转场 / 矫顽场差异。',next:'liang2025'},
    {id:'sui2024',year:2024,title:'Atomic-level polarization reversal in sliding ferroelectric semiconductors',authors:'F. Sui et al.',kind:'原子尺度实验',module:'pathways',role:'提供原子尺度的实时滑移证据，同时提醒：材料体系不同，实际翻转机制也可能不同。',question:'什么样的实验信息才算真正“看到原子层滑动”？',figure:'Fig. 2 的原位 HRTEM 连续图像与电学翻转结果，并结合 Fig. 1 的滑移路径。',quote:'重点读作者关于“逐步、逐原子”滑移，以及 1/3 晶胞平移与极化反转对应关系的表述。',next:'liang2025'},
    {id:'liang2025',year:2025,title:'Resolving polarization switching pathways of sliding ferroelectricity in trilayer 3R-MoS₂',authors:'J. Liang et al.',kind:'实验',module:'pathways',role:'真正区分三层 3R-MoS₂ 的 ABC / ABA / BAB / CBA 路径，并把路径选择与钉扎中心和载流子屏蔽联系起来。',question:'为什么相同的净极化不能唯一决定具体堆垛状态？',figure:'Fig. 1：ABC → ABA → CBA 的两阶段翻转，以及对应的光学识别。',quote:'重点读作者怎样说明路径选择受到钉扎中心竞争和自由载流子屏蔽共同影响。',next:'wangdong2025'},

    {id:'wangdong2025',year:2025,title:'Polarization switching in sliding ferroelectrics: Roles of fluctuation and domain wall',authors:'Z. Wang · S. Dong',kind:'理论 / AIMD',module:'walls',role:'解释为什么面外电场能够最终驱动面内运动：关键在于非对角 Born 有效电荷与初始对称性破缺。',question:'为什么 AB / BA 基态本身不能简单理解成被面外电场直接“推着滑”？',figure:'Fig. 1：Born 有效电荷张量、能垒和所需临界场；随后再看畴壁和局域起伏相关结果。',quote:'重点读非零非对角 Born 有效电荷以及对称性破缺扰动所起的作用。',next:'ke2025'},
    {id:'ke2025',year:2025,title:'Superlubric Motion of Wavelike Domain Walls in Sliding Ferroelectrics',authors:'C. Ke · F. Liu · S. Liu',kind:'理论 / 分子动力学',module:'walls',role:'把“真正受力的自由度是畴壁附近原子”讲得很清楚，并提出宽的波状畴壁及其近超润滑动力学。',question:'为什么只有畴壁附近出现非零面内受力？为什么均匀单畴可以保持不动？',figure:'Fig. 1 的面内力场，以及 Fig. 2 中约 10 nm 宽畴壁的局域受力与传播。',quote:'重点读作者关于“只有畴壁附近原子具有非零非对角 BEC 元素”的论述。',next:'chen2026'},
    {id:'chen2026',year:2026,title:'Deterministic 1D Domain Wall Motion with Nucleation-Free Nature in Sliding Ferroelectric Switching',authors:'J. Chen et al.',kind:'PRX · 理论 + 实验',module:'walls',role:'把机制推进到强版本：在他们研究的体系中，翻转被限制在已有畴壁附近的一维路径，并提出“no domain wall, no polarization reversal”。',question:'“无成核”这一机制怎样同时得到计算、KPFM 和器件行为的支持？',figure:'Fig. 1 对比传统铁电与滑移铁电翻转；Fig. 2 展示 bubble / rough-edge 钉扎和畴壁退钉扎。',quote:'重点读“no domain wall, no polarization reversal”以及翻转局限于畴壁附近原子的论述。',next:'liu2026'},
    {id:'liu2026',year:2026,title:'Shear-Mode Raman Imaging of Ferroelectric Switching in Multilayer 3R-MoS₂',authors:'Y. Liu et al.',kind:'PRL · 实验',module:'walls',role:'在器件尺度直接进行结构成像：不同区域可以独立翻转，中间态寿命差异很大，钉扎明确进入动力学。',question:'哪些实验现象已经要求我们考虑 pinning landscape（钉扎景观），而不能只用单一“本征矫顽场”解释？',figure:'Fig. 2 的 Raman 空间图：不同区域的翻转行为；再结合中间态停留时间和表观临界场的变化。',quote:'重点读作者关于“pinning sites strongly influence the dynamics”以及周期间临界场变化的论述。',next:'tybell2002'},

    {id:'tybell2002',year:2002,title:'Domain Wall Creep in Epitaxial Ferroelectric Thin Films',authors:'T. Tybell et al.',kind:'经典实验',module:'pinning',role:'把铁电畴壁的低场非线性运动正式放进 creep（蠕变）与 disorder（无序）的语言中。',question:'为什么低场畴壁速度不能用简单线性迁移率描述？',figure:'核心 v(E) / 蠕变律图：看清对数坐标、拟合区间以及温度 / 电场依赖。',quote:'重点读作者如何把铁电畴壁运动与无序控制的蠕变联系起来。',next:'paruch2005'},
    {id:'paruch2005',year:2005,title:'Domain Wall Roughness in Epitaxial Ferroelectric Thin Films',authors:'P. Paruch · T. Giamarchi · J.-M. Triscone',kind:'经典实验',module:'pinning',role:'把“畴壁长什么样”变成可量化的 observable（可观测量）：roughness exponent（粗糙度指数）可以反映无序和弹性的共同作用。',question:'怎样从真实空间畴壁轮廓得到 ζ？ζ 又能不能唯一判定无序类型？',figure:'粗糙度相关函数 B(L) 及其幂律标度，并配合真实畴壁图像。',quote:'重点读 B(L) ∝ L^{2ζ} 的定义，以及作者如何解释粗糙度与无序之间的关系。',next:'kim2014'},
    {id:'kim2014',year:2014,title:'Origins of domain wall pinning in ferroelectric nanocapacitors',authors:'Y. Kim et al.',kind:'实验 / 钉扎机制',module:'pinning',role:'把抽象的“钉扎中心”落回真实缺陷和器件微结构。',question:'哪些实际缺陷能够成为畴壁运动的局域势垒？',figure:'优先看能够把缺陷位置与畴壁钉扎对应起来的主图。',quote:'重点读作者关于主要钉扎来源的结论。',next:'chauve2000'},

    {id:'chauve2000',year:2000,title:'Creep and depinning in disordered media',authors:'P. Chauve · T. Giamarchi · P. Le Doussal',kind:'理论 / FRG',module:'depinning',role:'把平衡态、蠕变和退钉扎放在同一套无序弹性系统框架中。',question:'热激活蠕变与零温退钉扎在理论上怎样衔接？',figure:'能够展示蠕变 / 退钉扎动力学区间或特征尺度的理论图。',quote:'重点读 depinning threshold（退钉扎阈值）和 creep regime（蠕变区间）的定义。',next:'rosso2003'},
    {id:'rosso2003',year:2003,title:'Depinning of Elastic Manifolds',authors:'A. Rosso · A. K. Hartmann · W. Krauth',kind:'数值理论',module:'depinning',role:'非常干净的数值锚点：直接计算有限样本的临界界面构型与粗糙度。',question:'怎样在有限系统中定义并找到真正的临界构型？',figure:'临界界面几何，以及粗糙度 / 尺寸标度的核心图。',quote:'重点读作者如何定义 critical manifold（临界界面）并数值构造退钉扎阈值。',next:'ferrero2013'},
    {id:'ferrero2013',year:2013,title:'Numerical approaches on driven elastic interfaces in random media',authors:'E. E. Ferrero et al.',kind:'综述 / 数值方法',module:'depinning',role:'把平衡态 → 蠕变 → 退钉扎 → 快速流动与对应的数值算法连成完整路线。',question:'不同驱动区间应该测哪些可观测量、使用哪些算法？',figure:'概括不同动力学区间和粗糙度 crossover（交叉）的综述图。',quote:'重点读退钉扎普适性以及受驱界面主要可观测量的定义。',next:'wiese2022'},
    {id:'wiese2022',year:2022,title:'Theory and Experiments for Disordered Elastic Manifolds, Depinning, Avalanches, and Sandpiles',authors:'K. J. Wiese',kind:'大型综述',module:'depinning',role:'全站理论母文献：把 FRG、退钉扎、雪崩、实验系统与普适性放在一张总地图中。',question:'哪些指数关系来自 universality class（普适类），哪些会依赖维度、弹性核或无序类型？',figure:'优先看普适类、退钉扎和雪崩的总览图，以及关键标度关系；不要求通读全文。',quote:'只需要抓住定义性表述；这一页主要靠中文导读建立结构。',next:'sethna1993'},

    {id:'sethna1993',year:1993,title:'Hysteresis and Hierarchies: Dynamics of Disorder-Driven First-Order Phase Transformations',authors:'J. P. Sethna et al.',kind:'RFIM 经典工作',module:'disorder',role:'建立另一种粗粒化图像：局域随机场 + 邻近耦合 + 缓慢驱动可以产生滞回、雪崩和记忆效应。',question:'为什么“许多局域随机阈值 + 相互耦合”能够生成集体雪崩？',figure:'代表性的滞回、雪崩和 return-point memory（回返点记忆）图。',quote:'重点读模型动力学以及 disorder-driven transition（无序驱动转变）的定义。',next:'dahmen1996'},
    {id:'dahmen1996',year:1996,title:'Hysteresis, Avalanches, and Disorder-Induced Critical Scaling: A Renormalization-Group Approach',authors:'K. Dahmen · J. P. Sethna',kind:'RFIM / RG',module:'disorder',role:'从现象学进入真正的临界标度与重整化群，用来建立“出现幂律 ≠ 已经证明临界性”的判断标准。',question:'什么证据才能支持一个由无序诱导的临界点？',figure:'优先看 scaling function（标度函数）、scaling collapse（标度坍缩）和临界指数，而不是只看一条 log-log 直线。',quote:'重点读 diverging correlation length（发散关联长度）和标度形式的核心定义。',next:'dong2012'},
    {id:'dong2012',year:2012,title:'Creep motion of a domain wall in the two-dimensional random-field Ising model with a driving field',authors:'G. Dong et al.',kind:'RFIM 动力学',module:'disorder',role:'把 RFIM、畴壁和蠕变直接接起来，是两条理论支线之间的重要桥梁。',question:'RFIM 畴壁的蠕变与弹性界面蠕变相似在哪里，又不同在哪里？',figure:'速度–驱动力 / 温度标度，以及界面形貌随驱动变化的图。',quote:'重点读作者如何定义蠕变区间，以及无序怎样影响动力学。',next:'chen2008'},

    {id:'chen2008',year:2008,title:'Phase-Field Method of Phase Transitions/Domain Structures in Ferroelectric Thin Films: A Review',authors:'L.-Q. Chen',kind:'方法综述',module:'modeling',role:'建立 phase field（相场）的基本语法：自由能泛函、序参量、梯度能、长程场以及 TDGL 演化。',question:'相场模型保留了哪些自由度，又舍弃了哪些原子尺度细节？',figure:'从自由能 / 演化方程到畴结构的框架性图，而不是某一个材料特例。',quote:'重点读相场方法的定义，以及它所处的空间和时间尺度层次。',next:'caballero2020'},
    {id:'caballero2020',year:2020,title:'From bulk descriptions to emergent interfaces: Connecting the Ginzburg-Landau and elastic-line models',authors:'N. B. Caballero et al.',kind:'理论桥接',module:'modeling',role:'建模章的关键桥梁：解释 diffuse scalar field（弥散标量场）在什么条件下可以 coarse-grain（粗粒化）成 elastic interface（弹性界面）。',question:'相场畴壁什么时候可以被当成一条弹性线？两种模型的参数怎样对应？',figure:'GL 场构型 ↔ 提取出的界面 ↔ 弹性线模型比较的核心图。',quote:'重点读作者怎样连接 bulk field description（体场描述）与 emergent interface（涌现界面）。',next:'frontier'}
  ]
};