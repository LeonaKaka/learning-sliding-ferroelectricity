# Open-Source Modeling Lab — continuation plan

## Purpose

The Open-Source Modeling Lab is a repository-first learning track inside **Learning Sliding Ferroelectricity**. It is not a GitHub README mirror and not a replacement for the existing eight-module physics route.

The track answers a different question:

> How do real researchers go from a physical problem to degrees of freedom, symmetry, free energy, parameters, numerics and validation — and only then, what does that teach us about the sliding-ferroelectric disorder project?

The site therefore uses a two-pass pedagogy:

1. **Repository-first pass** — enter one codebase at a time and reconstruct the authors' modeling logic on its own terms.
2. **Cross-project synthesis pass** — only after several codebases are understood, compare modeling choices and return to the user's own model.

## Information architecture

The existing eight physics modules remain unchanged. A new first-class track is added:

- Open-Source Modeling Lab overview
- moire_metrology
- Ferroelectric-Phasefield
- Ferret
- FLAM2020-GSFE
- DPmoire
- Twister
- JAX phase-field implementations
- later: cross-project synthesis, parameter provenance, DFT → continuum, disorder construction, Modeling Taste, Back to My Model

The homepage must expose this track in two places:

- the sticky top header;
- a prominent homepage entry card.

The global sidebar must also expose the Lab on every page.

## Quality contract

Every completed repository page must meet or exceed the existing long-form modules.

### Scientific provenance

Each page must record:

- upstream repository;
- branch;
- frozen 40-character commit SHA;
- verification date;
- paper/document/source provenance;
- exact file path plus class/function/symbol whenever code is discussed.

Scientific statements are labeled as one of:

- [源码直接支持]
- [论文直接支持]
- [项目文档支持]
- [推导]
- [合理物理解释]
- [我的项目中的假设]
- [尚未验证]

If a parameter value is present in code but its origin cannot be traced, the page must say so explicitly.

### Five-level learning template

Every repository page contains:

1. Physical question（物理问题）
2. Model construction（模型构造）
3. Parameter origin（参数来源）
4. Numerical implementation（数值实现）
5. Relevance to my project（对我的项目的启发）

The first four levels are taught primarily from the upstream project. Level 5 is intentionally short on the first pass.

### Code pedagogy

Source code is never dumped in bulk. Each code walkthrough follows:

1. the physical question;
2. the equation;
3. a small key excerpt;
4. line-by-line explanation;
5. inputs and outputs;
6. physical assumption → equation → code → numerical result.

### Modeling Taste

Every completed project ends with a Modeling Taste section:

- what the authors decide first;
- where they simplify;
- what they refuse to simplify;
- where parameters come from;
- what is validated;
- which convergence tests matter;
- how they show the result is not a numerical toy.

### UI / reading quality

- Same visual language as the existing site, with denser provenance and code mapping.
- Mobile readable.
- One h1 per page.
- Important English terms receive Chinese explanations at first use.
- No remote scientific images are required for the first repository page; when figures are added later they must follow the existing frozen-asset/evidence policy.

## Learning order

Initial repository-first route:

1. **moire_metrology** — vector displacement, elasticity + GSFE, symmetry-constrained Fourier landscape, material/interface provenance, relaxation solvers.
2. **Ferroelectric-Phasefield** — a smaller and more transparent ferroelectric phase-field implementation, including finite-range random fields.
3. **Ferret** — a mature modular ferroic mesoscale framework and validation culture.
4. **FLAM2020-GSFE** — microscopic random structures → many GSFE curves → barrier statistics.
5. **DPmoire** — DFT → dataset → ML force field → large-scale relaxation.
6. **Twister** — commensurate moiré construction and atomistic structural reconstruction.
7. **JAX phase-field repositories** — software architecture after the physical architecture is understood.

After projects 1–4, start the first cross-project synthesis and update Model Audit.

## Delivery phases

### Phase A — track infrastructure

- homepage header entry;
- homepage Lab card;
- global sidebar Lab section;
- overview page;
- shared Lab stylesheet;
- automated Open-Source Modeling quality seal;
- documented completion contract.

### Phase B — first gold-standard repository page

Complete **moire_metrology** as the template repository page. It must include:

- physical problem and model hierarchy;
- displacement field definition;
- elastic energy;
- GSFE Fourier basis and symmetry;
- parameter provenance;
- code path from materials → interfaces → GSFE → energy → solver → result;
- solver / convergence philosophy;
- validation and limitations;
- Modeling Taste;
- exercises;
- short bridge to the user's scalar sliding-ferroelectric model.

### Phase C — next repositories

Only start the next repository when the previous one passes the quality seal and its scientific provenance has been checked.

### Phase D — synthesis

After four repository pages:

- DFT → Continuum synthesis;
- Disorder Construction synthesis;
- Parameter Provenance matrix;
- Modeling Taste cross-project page;
- first serious Back to My Model audit.

## Definition of done for one repository

A repository is “learned” only when the page can answer:

- What physical problem is being solved?
- Why are these degrees of freedom sufficient?
- Which free-energy terms are symmetry-required, microscopic, phenomenological or numerical?
- Where does every important parameter come from?
- How does the formula become code?
- What is input and what is output?
- What tests establish numerical credibility?
- What can and cannot be transferred to the user's project?

A repository card is not marked complete merely because README text has been summarized.
