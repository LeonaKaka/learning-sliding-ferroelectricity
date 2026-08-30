window.LSF_DATA = {
  modules: [
    {
      id: 'foundations', number: '01', title: 'What is Sliding Ferroelectricity?', short: '堆垛、对称性与极化',
      question: 'AB/BA/3R 堆垛为什么会产生可翻转的面外极化？所谓 sliding 到底改变了什么？',
      thesis: '先建立材料本身的物理图像。这里不追求把所有二维铁电都学一遍，只把“堆垛 → 对称性破缺 → 层间电荷重分布 → 极化”这条因果链讲清楚。',
      concepts: ['stacking order','inversion symmetry','interlayer charge transfer','out-of-plane polarization','AB / BA / 3R'],
      core: ['wu2021','yasuda2021','stern2021','meng2022','ji2023'],
      supporting: ['Zhang et al. 2025 · Emerging frontiers in 2D sliding ferroelectrics','Woods et al. 2021 · charge-polarized interfacial superlattices in twisted hBN','Enaldiev et al. 2022 · scalable network model for ferroelectric domains'],
      takeaway: '读完后应该能自己解释：为什么一块非极性的单层材料，经过特定堆垛以后会出现面外极化；以及 AB↔BA 与 P↔−P 为什么相连。'
    },
    {
      id: 'pathways', number: '02', title: 'How Does Switching Proceed?', short: '翻转路径与中间态',
      question: '极化翻转真的是整层同步滑过去吗？多层体系为什么会出现中间态和多条路径？',
      thesis: '从“静态堆垛”进入“动态翻转”。重点不是记住多少 stacking 名字，而是看到 switching 是一个路径选择问题，路径会被界面、pinning 与载流子屏蔽改变。',
      concepts: ['switching pathway','intermediate state','metastability','multi-interface','layer-selective switching'],
      core: ['yang2024','sui2024','liang2025'],
      supporting: ['Yang et al. 2023 · shear-transformation-mediated 3R-MoS₂ transistors','Ouyang et al. 2025 · electrically switching ferroelectric order in 3R-MoS₂','Wang et al. 2025 · cluster sliding ferroelectricity'],
      takeaway: '读完后应该能画出 bilayer 与 trilayer 的典型 switching pathway，并说清楚“中间态”究竟是一个新相、一个 metastable stacking，还是局域 DW 运动留下的结果。'
    },
    {
      id: 'walls', number: '03', title: 'Domain Walls: What Actually Moves?', short: '真正运动的自由度',
      question: '如果单畴内部并不会被面外场直接推动，真正完成极化翻转的自由度是什么？',
      thesis: '这是全站最重要的概念转折：从“整层 coherent sliding”切换到“pre-existing domain wall propagation”。随后 pinning、creep、depinning 才有必要出现。',
      concepts: ['pre-existing DW','symmetry breaking','off-diagonal Born effective charge','nucleation-free switching','1D DW pathway'],
      core: ['wangdong2025','ke2025','chen2026','liu2026'],
      supporting: ['Shi et al. 2025 · soliton-like DW motion with ultralow damping','Deng et al. 2025 · deterministic and efficient switching','Jia-Wen Li et al. 2026 · ultralow-barrier sliding and pinning in moiré superlattices'],
      takeaway: '读完后应该能回答“no domain wall, no polarization reversal”这句话依赖什么对称性与实验事实，以及它和早期 coherent-sliding 图像有什么冲突。'
    },
    {
      id: 'pinning', number: '04', title: 'Pinning, Creep & Roughness', short: '真实畴壁为什么走不直',
      question: '真实样品中的 DW 为什么不是匀速平移？缺陷怎样改变速度、形貌和开关场？',
      thesis: '先从传统铁电畴壁学会 disorder 的实验语言。creep 不是一个拟合公式，roughness 也不是“墙看起来很毛”；它们是界面与无序共同作用的可观测结果。',
      concepts: ['pinning centre','creep','roughness','local barrier','collective motion'],
      core: ['tybell2002','paruch2005','kim2014'],
      supporting: ['Kleemann 2007 · universal domain-wall dynamics in disordered ferroics','Jo et al. 2009 · nonlinear DW propagation','Liu & Huber 2011 · electrical creep in BaTiO₃','Guyonnet et al. 2012 · multiscaling of FE DW roughness','Tückmantel et al. 2021 · creep vs depinning event statistics','Bulanadi et al. 2024 · point/extended defects and jerky DW motion','Teng et al. 2025 · point-defect control of FE DW dynamics'],
      takeaway: '读完后应该能看到一张畴壁图像或 v(E) 曲线，就知道哪些特征可能来自 pinning、哪些能用 creep 描述、哪些现象还不能直接叫 depinning。'
    },
    {
      id: 'depinning', number: '05', title: 'Depinning as a Critical Phenomenon', short: '阈值、指数与有限尺寸',
      question: '什么时候一个 pinned interface 真正进入持续运动？为什么 β、ζ、ν 与 finite-size scaling 比“画一条幂律”更重要？',
      thesis: '把 domain wall 抽象成受 quenched disorder 作用的 elastic interface。这里建立 threshold、critical geometry、velocity scaling 与 finite-size scaling 的统一语言。',
      concepts: ['elastic interface','critical force','velocity exponent β','roughness exponent ζ','correlation length','finite-size scaling'],
      core: ['chauve2000','rosso2003','ferrero2013','wiese2022'],
      supporting: ['Ferrero et al. 2021 · creep motion review','Le Doussal et al. 2004 · functional RG for disordered elastic systems','Drossel & Dahmen 1998 · RFIM DW depinning','Zhou et al. 2009 · short-time RFIM DW dynamics','Qian et al. 2023 · nonsteady dynamic depinning'],
      takeaway: '读完后应该能设计一个像样的 depinning 数值实验：先定义 Fc/Ec，再测 v、roughness、相关长度和尺寸依赖，而不是只在单一尺寸上拟合 β。'
    },
    {
      id: 'disorder', number: '06', title: 'Disorder & RFIM', short: '局域随机性怎样变成集体开关',
      question: '如果不把 DW 只看成一条弹性线，而从局域 switching tendency、耦合与驱动出发，会得到什么？',
      thesis: 'RFIM 是另一套粗粒化语言：它帮助理解局域随机场、hysteresis、avalanches 和 disorder-controlled criticality，但网站会始终强调“sliding FE ≠ RFIM”。',
      concepts: ['quenched disorder','random field','random bond','hysteresis','avalanches','scaling collapse'],
      core: ['sethna1993','dahmen1996','dong2012'],
      supporting: ['Seppälä et al. 1998 · RFIM domain-wall roughening','Vives et al. 2005 · hysteresis and avalanches','Chan et al. 2024 · coercivity distribution','Paul et al. 2026 · disorder and multi-domain kinetics in CVD 3R-WSe₂'],
      takeaway: '读完后应该能区分：elastic-interface depinning 和 RFIM switching 各自保留了哪些自由度、适合解释哪些数据、什么时候两种语言可能给出不同预测。'
    },
    {
      id: 'modeling', number: '07', title: 'From Theory to Numerical Modeling', short: 'phase field / TDGL / emergent interface',
      question: '怎样从连续场模型得到畴、畴壁和 driven interface？怎样把 disorder 加进去而不破坏物理尺度？',
      thesis: '这一章不做软件教程，而是建立模型层次：Landau free energy → TDGL/phase field → diffuse wall → emergent elastic interface → disorder-driven dynamics。',
      concepts: ['order parameter','Landau free energy','TDGL','phase field','diffuse interface','coarse graining'],
      core: ['chen2008','caballero2020'],
      supporting: ['Wang et al. 2004 · phase-field polarization switching','Fedeli et al. 2019 · FE domains with defects','Hong & Viswanathan 2020 · open-source phase-field','Zhu et al. 2022 · FE DW memory','Lv & Lynch 2018 · rhombohedral FE domain walls','FerroX 2023 · GPU phase-field framework'],
      takeaway: '读完后应该能说明自己的模拟位于哪个粗粒化层次：哪些参数是材料参数，哪些是有效参数；以及怎样验证 lattice spacing、dx、system size 不在偷偷改变 disorder strength。'
    },
    {
      id: 'frontier', number: '08', title: 'Current Frontiers', short: '把整棵树重新压回 3R-MoS₂ / WSe₂',
      question: '2025–2026 的实验和理论已经把 DW / pinning 证据推进到哪里？还差什么才能谈 universality？',
      thesis: '最后不再引入新基础理论，而是重新读最新 sliding-FE 工作：哪些结果已经很强，哪些只是“看起来像 depinning”，哪些量仍然没人系统测。',
      concepts: ['pinning landscape','cycle-to-cycle variability','partial switching','multidomain kinetics','universality test'],
      core: ['liang2025','wangdong2025','ke2025','chen2026','liu2026'],
      supporting: ['Paul et al. 2026 · disorder dynamics in CVD 3R-WSe₂','Jia-Wen Li et al. 2026 · DW-mediated ultralow-barrier sliding','Remez & Goldstein 2025 · hierarchical ordering transitions','Lee et al. 2025 · theory of slidetronics'],
      takeaway: '最终应该能自己审一篇新 paper：作者观察到 pinning 了吗？有 threshold 吗？有 v(E) 吗？有 ζ/β/ν 吗？有尺寸标度吗？如果没有，就不要把“幂律”直接等同于 universality。'
    }
  ],
  papers: [
    {id:'wu2021',year:2021,title:'Sliding ferroelectricity in 2D van der Waals materials: Related physics and future opportunities',authors:'M. Wu · J. Li',kind:'Review / entry point',module:'foundations',role:'用一篇综述建立全局词汇和材料谱系，替代必须从 2017 ACS 原始工作起步。',question:'sliding FE 的基本定义、材料类型和早期物理问题是什么？',figure:'候选：综述中概括 sliding-induced polarization / switching 的总览示意图。',quote:'摘取作者对 sliding ferroelectricity 定义和“relative interlayer translation”作用的短原句。',next:'yasuda2021'},
    {id:'yasuda2021',year:2021,title:'Stacking-engineered ferroelectricity in bilayer boron nitride',authors:'K. Yasuda et al.',kind:'Experiment',module:'foundations',role:'把“stacking-dependent polarization”从理论概念落到 bilayer hBN 实验。',question:'AB/BA stacking 的相反极化怎样被实验读出？',figure:'候选：AB/BA stacking 与极化示意 + 代表性电输运/畴响应。',quote:'选 Introduction/Discussion 中连接 stacking 与 switchable polarization 的一句。',next:'stern2021'},
    {id:'stern2021',year:2021,title:'Interfacial ferroelectricity by van der Waals sliding',authors:'M. Vizner Stern et al.',kind:'Experiment',module:'foundations',role:'空间上看到相反极化畴，并把 tip-induced switching 与 lateral sliding 联系起来。',question:'怎样从空间畴图像而不是单条 hysteresis 证明 interfacial ferroelectricity？',figure:'候选：相反极化畴的扫描探针图 + bias 驱动畴变化。',quote:'选作者把 polarization reversal 与 van der Waals sliding 联系起来的短句。',next:'meng2022'},
    {id:'meng2022',year:2022,title:'Sliding induced multiple polarization states in two-dimensional ferroelectrics',authors:'P. Meng et al.',kind:'Experiment / multilayer',module:'foundations',role:'从二态进入 multilayer：不同 vdW interface 的极化可以组合，产生中间态。',question:'为什么层数增加后不再只是 +P 与 −P？',figure:'候选：多层 stacking configurations 与对应 polarization states 的主图。',quote:'摘取作者关于 multiple polarization states 来自不同 interlayer sliding configurations 的原句。',next:'ji2023'},
    {id:'ji2023',year:2023,title:'General Theory for Bilayer Stacking Ferroelectricity',authors:'J. Ji et al.',kind:'Theory',module:'foundations',role:'用 symmetry / layer-group 语言把具体材料案例抽象成一般判据。',question:'什么样的 monolayer symmetry 与 stacking operation 能产生 polar bilayer？',figure:'候选：对称操作与 polar/non-polar bilayer 的分类示意。',quote:'选 general criterion 的最短原文表述。',next:'yang2024'},

    {id:'yang2024',year:2024,title:'Non-volatile electrical polarization switching via domain wall release in 3R-MoS₂ bilayer',authors:'D. Yang et al.',kind:'Experiment',module:'pathways',role:'主线关键桥梁：switching event 被解释为 pre-existing DW 从 pinning site 释放并扫过样品。',question:'coercive field 在这里更像“本征成核场”还是“局域 depinning field”？',figure:'优先选：展示 domain wall release / pinning 与 switching field 的核心图，而不是器件结构图。',quote:'摘取作者关于 random pinning potential 导致不同 switching/coercive fields 的原句。',next:'liang2025'},
    {id:'sui2024',year:2024,title:'Atomic-level polarization reversal in sliding ferroelectric semiconductors',authors:'F. Sui et al.',kind:'Atomic-scale experiment',module:'pathways',role:'提供原子尺度 real-time sliding 证据，同时提醒“材料体系不同，switching mechanism 也可能不同”。',question:'什么证据才算真正“看到原子层滑动”？',figure:'Fig. 2：in-situ HRTEM snapshots + I–V / resistance switching；辅以 Fig. 1 的 sliding pathway。',quote:'摘取“step by step and atom by atom”及 1/3-unit-cell sliding 对应 polarization reversal 的短句。',next:'liang2025'},
    {id:'liang2025',year:2025,title:'Resolving polarization switching pathways of sliding ferroelectricity in trilayer 3R-MoS₂',authors:'J. Liang et al.',kind:'Experiment',module:'pathways',role:'把 trilayer 的 ABC/ABA/BAB/CBA 路径真正分辨出来，并把路径选择与 pinning centres、doping 联系起来。',question:'同样的净 polarization 为什么不能唯一决定 stacking state？',figure:'Fig. 1：ABC → ABA → CBA 的两阶段 switching 与 optical identification。',quote:'摘取摘要中“pathway is influenced ... by competition among pinning centres ... and free-carrier screening”的短句。',next:'wangdong2025'},

    {id:'wangdong2025',year:2025,title:'Polarization switching in sliding ferroelectrics: Roles of fluctuation and domain wall',authors:'Z. Wang · S. Dong',kind:'Theory / AIMD',module:'walls',role:'解释面外电场为何能驱动面内 motion：关键是 off-diagonal Born effective charge 与初始 symmetry breaking。',question:'为什么 AB/BA ground state 本身不能被面外场直接“推着滑”？',figure:'Fig. 1：Born effective charge tensor、energy barrier 与 required critical field；随后看 DW/wriggling 结果。',quote:'摘取“nonzero off-diagonal element of Born effective charge”与 symmetry-breaking perturbation 作用的原句。',next:'ke2025'},
    {id:'ke2025',year:2025,title:'Superlubric Motion of Wavelike Domain Walls in Sliding Ferroelectrics',authors:'C. Ke · F. Liu · S. Liu',kind:'Theory / MD',module:'walls',role:'把“DW 才是受力自由度”讲得最干净，并提出宽的 wavelike DW 与 superlubric dynamics。',question:'为什么只有 DW 附近出现非零 in-plane force？为什么 single domain 可以不动？',figure:'Fig. 1：F_IP 位移空间力场；Fig. 2：约 10 nm 宽 DW 与局域受力/传播。',quote:'摘取“only atoms at the DWs ... possess nonzero off-diagonal BEC elements”一句附近的短引文。',next:'chen2026'},
    {id:'chen2026',year:2026,title:'Deterministic 1D Domain Wall Motion with Nucleation-Free Nature in Sliding Ferroelectric Switching',authors:'J. Chen et al.',kind:'PRX · theory + experiment',module:'walls',role:'把机制推到强版本：switching 被限制在已有 DW 的 1D 路径，并提出“no domain wall, no polarization reversal”。',question:'nucleation-free 是怎样被计算、KPFM 与器件行为共同支持的？',figure:'Fig. 1：conventional vs sliding FE switching；Fig. 2：bubble / rough-edge pinning 与 DW depinning。',quote:'摘取“no domain wall, no polarization reversal”及 switching restricted to atoms near DWs 的短句。',next:'liu2026'},
    {id:'liu2026',year:2026,title:'Shear-Mode Raman Imaging of Ferroelectric Switching in Multilayer 3R-MoS₂',authors:'Y. Liu et al.',kind:'PRL · experiment',module:'walls',role:'device-scale 直接结构成像：不同区域独立 switch，中间态寿命变化大，pinning 明确进入 dynamics。',question:'哪些实验现象已经直接要求我们考虑 pinning landscape，而不是单一 intrinsic coercive field？',figure:'Fig. 2：Raman maps 的 region-dependent switching；配合中间态 dwell time 与 apparent critical field 变化。',quote:'摘要中“pinning sites strongly influence the dynamics”及正文 cycle-to-cycle critical-field variation。',next:'tybell2002'},

    {id:'tybell2002',year:2002,title:'Domain Wall Creep in Epitaxial Ferroelectric Thin Films',authors:'T. Tybell et al.',kind:'Classic experiment',module:'pinning',role:'第一次把 FE DW 的低场非线性运动放进 creep / disorder 语言。',question:'为什么低场 DW 速度不是简单线性 mobility？',figure:'核心 v(E) / creep-law 图：看清对数坐标、拟合区间和温度/场依赖。',quote:'摘取作者把 FE DW motion 与 disorder-controlled creep 联系起来的一句。',next:'paruch2005'},
    {id:'paruch2005',year:2005,title:'Domain Wall Roughness in Epitaxial Ferroelectric Thin Films',authors:'P. Paruch · T. Giamarchi · J.-M. Triscone',kind:'Classic experiment',module:'pinning',role:'把“墙长什么样”变成 quantitative observable：roughness exponent 可反推 disorder / elasticity。',question:'怎样从 real-space wall profile 得到 ζ？ζ 能否唯一告诉你 disorder class？',figure:'roughness correlation function B(L) 与 power-law scaling；配真实 DW images。',quote:'摘取 B(L)∝L^{2ζ} 与 disorder interpretation 附近的短句。',next:'kim2014'},
    {id:'kim2014',year:2014,title:'Origins of domain wall pinning in ferroelectric nanocapacitors',authors:'Y. Kim et al.',kind:'Experiment / pinning mechanism',module:'pinning',role:'把“pinning centre”从抽象随机势落回具体缺陷与器件微结构。',question:'哪些实际 defect 可以成为 DW 的 local barrier？',figure:'优先用能把缺陷位置与 DW pinning 对应起来的主图。',quote:'摘取作者对 dominant pinning origin 的结论句。',next:'chauve2000'},

    {id:'chauve2000',year:2000,title:'Creep and depinning in disordered media',authors:'P. Chauve · T. Giamarchi · P. Le Doussal',kind:'Theory / FRG',module:'depinning',role:'把 equilibrium、creep 与 depinning 放在同一受无序弹性系统框架中。',question:'thermal activation 与 zero-temperature depinning 在理论上如何衔接？',figure:'选能展示 creep/depinning regimes 或 characteristic scales 的理论图。',quote:'摘取 depinning threshold 与 creep regime 定义性的短句。',next:'rosso2003'},
    {id:'rosso2003',year:2003,title:'Depinning of Elastic Manifolds',authors:'A. Rosso · A. K. Hartmann · W. Krauth',kind:'Numerical theory',module:'depinning',role:'非常干净的数值 anchor：直接计算 finite sample 的 critical manifold 与 roughness。',question:'怎样在有限系统里定义并找到真正的 critical configuration？',figure:'critical interface geometry + roughness / size scaling 的核心图。',quote:'摘取论文对 critical manifold / depinning threshold 数值构造的定义。',next:'ferrero2013'},
    {id:'ferrero2013',year:2013,title:'Numerical approaches on driven elastic interfaces in random media',authors:'E. E. Ferrero et al.',kind:'Review / numerical methods',module:'depinning',role:'把 equilibrium → creep → depinning → fast flow 与数值算法连成完整路线。',question:'不同驱动 regime 应该测哪些 observable、用哪些算法？',figure:'优先使用概括各动力学 regime / roughness crossover 的综述图。',quote:'摘取 depinning universality 与 driven interface observable 的定义句。',next:'wiese2022'},
    {id:'wiese2022',year:2022,title:'Theory and Experiments for Disordered Elastic Manifolds, Depinning, Avalanches, and Sandpiles',authors:'K. J. Wiese',kind:'Master review',module:'depinning',role:'全站理论母文献：FRG、depinning、avalanches、实验系统和 universality 的总地图。',question:'哪些指数关系来自 universality class，哪些取决于 dimension / elasticity / disorder？',figure:'不要求通读；挑“universality classes / depinning / avalanche”总览图与关键 scaling relations。',quote:'只摘定义性短句；这一页主要靠中文导读而不是大段原文。',next:'sethna1993'},

    {id:'sethna1993',year:1993,title:'Hysteresis and Hierarchies: Dynamics of Disorder-Driven First-Order Phase Transformations',authors:'J. P. Sethna et al.',kind:'RFIM classic',module:'disorder',role:'建立另一种粗粒化图像：局域 random field + neighbor coupling + slow drive 可以产生 hysteresis、avalanches 与 memory。',question:'为什么“很多局域随机阈值 + 耦合”会生成集体 avalanche？',figure:'hysteresis / avalanche / return-point-memory 代表图。',quote:'摘取模型动力学与 disorder-driven transition 的定义句。',next:'dahmen1996'},
    {id:'dahmen1996',year:1996,title:'Hysteresis, Avalanches, and Disorder-Induced Critical Scaling: A Renormalization-Group Approach',authors:'K. Dahmen · J. P. Sethna',kind:'RFIM / RG',module:'disorder',role:'从 phenomenology 进入真正的 critical scaling 与 RG；用来教“有 power law ≠ 已经证明 criticality”。',question:'什么证据才能支持 disorder-induced critical point？',figure:'优先 scaling functions / collapse 与 critical exponents，而不是单独一条 log-log 直线。',quote:'摘取 diverging correlation length / scaling 的核心定义。',next:'dong2012'},
    {id:'dong2012',year:2012,title:'Creep motion of a domain wall in the two-dimensional random-field Ising model with a driving field',authors:'G. Dong et al.',kind:'RFIM dynamics',module:'disorder',role:'把 RFIM、domain wall 与 creep 直接接起来，是两条理论支线的重要桥。',question:'RFIM DW 的 creep 与 elastic-interface creep 相似在哪里、不同在哪里？',figure:'velocity–field / temperature scaling 与界面形貌变化。',quote:'摘取作者对 creep regime 和 disorder effect 的结论句。',next:'chen2008'},

    {id:'chen2008',year:2008,title:'Phase-Field Method of Phase Transitions/Domain Structures in Ferroelectric Thin Films: A Review',authors:'L.-Q. Chen',kind:'Methods review',module:'modeling',role:'建立 phase-field 的基本语法：free-energy functional、order parameter、gradient energy、long-range fields 与 TDGL evolution。',question:'phase field 在保留什么自由度、舍弃什么原子细节？',figure:'选 free-energy / evolution equation 到 domain pattern 的框架性图，而非材料特例。',quote:'摘取 phase-field method 的定义与尺度定位。',next:'caballero2020'},
    {id:'caballero2020',year:2020,title:'From bulk descriptions to emergent interfaces: Connecting the Ginzburg-Landau and elastic-line models',authors:'N. B. Caballero et al.',kind:'Theory bridge',module:'modeling',role:'网站建模章的关键桥：解释 diffuse scalar field 在什么条件下可以 coarse-grain 成 elastic interface。',question:'phase-field DW 什么时候能被当成一条 elastic line？两种模型参数怎么对应？',figure:'GL field configuration ↔ extracted interface ↔ elastic-line comparison 的核心图。',quote:'摘取连接 bulk field description 与 emergent interface 的定义性句子。',next:'frontier'}
  ]
};